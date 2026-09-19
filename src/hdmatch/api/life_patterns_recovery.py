"""Email OTP recovery for Discover Your Unique Life Patterns sessions.

Only a normalized-email SHA-256 lookup and domain-separated OTP hashes are persisted.
Successful recovery rotates the normal resume token. The plaintext email is used only
for SMTP delivery and is not written into the research-session record.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import smtplib
import ssl
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email.message import EmailMessage
from typing import Any

from .life_patterns_app import LifePatternsFileStore

Clock = Callable[[], datetime]
OtpFactory = Callable[[], str]
TokenFactory = Callable[[], str]
RecoverySender = Callable[["LifePatternsRecoverySettings", str, str], None]


def normalize_email(value: str) -> str:
    normalized = value.strip().casefold()
    if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
        raise ValueError("enter a valid email address")
    local, domain = normalized.rsplit("@", 1)
    if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
        raise ValueError("enter a valid email address")
    return normalized


@dataclass(frozen=True)
class LifePatternsRecoverySettings:
    smtp_host: str
    smtp_port: int
    smtp_security: str
    smtp_username: str
    smtp_password: str
    from_address: str
    credential_ttl: timedelta = timedelta(minutes=15)
    issue_cooldown: timedelta = timedelta(seconds=60)
    issue_window: timedelta = timedelta(hours=1)
    max_issues_per_window: int = 5
    max_verification_attempts: int = 8
    smtp_timeout_seconds: float = 20.0

    @classmethod
    def from_env(
        cls, values: Mapping[str, str] | None = None
    ) -> LifePatternsRecoverySettings | None:
        environment = os.environ if values is None else values
        password = environment.get("HDMATCH_SMTP_PASSWORD", "")
        if not password:
            return None
        security = environment.get("HDMATCH_SMTP_SECURITY", "starttls").strip().lower()
        if security not in {"starttls", "ssl"}:
            raise RuntimeError("HDMATCH_SMTP_SECURITY must be 'starttls' or 'ssl'")
        default_port = "465" if security == "ssl" else "587"
        try:
            port = int(environment.get("HDMATCH_SMTP_PORT", default_port))
        except ValueError as exc:
            raise RuntimeError("HDMATCH_SMTP_PORT must be an integer") from exc
        if not 1 <= port <= 65535:
            raise RuntimeError("HDMATCH_SMTP_PORT must be between 1 and 65535")
        username = environment.get("HDMATCH_SMTP_USERNAME", "joel@u-dont-exist.com").strip()
        sender = environment.get("HDMATCH_SMTP_FROM", username).strip()
        host = environment.get("HDMATCH_SMTP_HOST", "smtp.porkbun.com").strip()
        if not host or not username or not sender:
            raise RuntimeError("SMTP host, username, and sender are required")
        return cls(
            smtp_host=host,
            smtp_port=port,
            smtp_security=security,
            smtp_username=username,
            smtp_password=password,
            from_address=sender,
        )


@dataclass(frozen=True)
class RecoveredLifePatternsSession:
    session_id: str
    resume_token: str


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _random_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def _parse_utc(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(UTC)


def _credential_sha256(session_id: str, otp: str) -> str:
    return hashlib.sha256(
        f"life-patterns-recovery-v1\x00{session_id}\x00otp\x00{otp}".encode()
    ).hexdigest()


def send_recovery_email(
    settings: LifePatternsRecoverySettings,
    recipient: str,
    otp: str,
) -> None:
    message = EmailMessage()
    message["Subject"] = "Resume Discover Your Unique Life Patterns"
    message["From"] = settings.from_address
    message["To"] = recipient
    minutes = max(1, int(settings.credential_ttl.total_seconds() // 60))
    message.set_content(
        "Use this one-time code to resume your private Life Patterns interview:\n\n"
        f"{otp}\n\n"
        f"The code expires in {minutes} minutes. If you did not request this, ignore this email."
    )
    context = ssl.create_default_context()
    if settings.smtp_security == "ssl":
        with smtplib.SMTP_SSL(
            settings.smtp_host,
            settings.smtp_port,
            timeout=settings.smtp_timeout_seconds,
            context=context,
        ) as client:
            client.login(settings.smtp_username, settings.smtp_password)
            client.send_message(message)
        return
    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port,
        timeout=settings.smtp_timeout_seconds,
    ) as client:
        client.ehlo()
        client.starttls(context=context)
        client.ehlo()
        client.login(settings.smtp_username, settings.smtp_password)
        client.send_message(message)


class LifePatternsRecoveryService:
    def __init__(
        self,
        store: LifePatternsFileStore,
        settings: LifePatternsRecoverySettings | None,
        *,
        sender: RecoverySender = send_recovery_email,
        clock: Clock = _now_utc,
        otp_factory: OtpFactory = _random_otp,
        resume_token_factory: TokenFactory = lambda: secrets.token_urlsafe(32),
    ) -> None:
        self._store = store
        self._settings = settings
        self._sender = sender
        self._clock = clock
        self._otp_factory = otp_factory
        self._resume_token_factory = resume_token_factory
        self._lock = threading.Lock()

    @property
    def configured(self) -> bool:
        return self._settings is not None

    def request(self, email: str) -> None:
        settings = self._settings
        if settings is None:
            return
        normalized = normalize_email(email)
        lookup = hashlib.sha256(normalized.encode()).hexdigest()
        now = self._normalized_now()
        with self._lock:
            payload = self._latest_matching_payload(lookup)
            if payload is None or not self._issuance_allowed(payload, now, settings):
                return
            session_id = str(payload["session_id"])
            otp = self._otp_factory()
            if len(otp) != 6 or not otp.isdigit():
                raise RuntimeError("OTP factory must return exactly six digits")
            previous_raw = payload.get("email_recovery")
            previous = previous_raw if isinstance(previous_raw, dict) else {}
            window_started, issue_count = self._next_issue_window(previous, now, settings)
            issued_at = now.isoformat()
            payload["email_recovery"] = {
                "schema_version": "life-patterns-email-recovery-v1",
                "issued_at_utc": issued_at,
                "expires_at_utc": (now + settings.credential_ttl).isoformat(),
                "otp_sha256": _credential_sha256(session_id, otp),
                "verification_attempts": 0,
                "max_verification_attempts": settings.max_verification_attempts,
                "used_at_utc": None,
                "issue_window_started_at_utc": window_started.isoformat(),
                "issue_count_in_window": issue_count,
                "delivery_status": "attempting",
            }
            self._store.save(payload)
        try:
            self._sender(settings, normalized, otp)
        except (OSError, smtplib.SMTPException):
            self._mark_delivery(session_id, issued_at, "failed")
            return
        self._mark_delivery(session_id, issued_at, "sent")

    def verify(self, email: str, otp: str) -> RecoveredLifePatternsSession | None:
        normalized = normalize_email(email)
        lookup = hashlib.sha256(normalized.encode()).hexdigest()
        with self._lock:
            payload = self._latest_matching_payload(lookup)
            if payload is None:
                return None
            record_raw = payload.get("email_recovery")
            if not isinstance(record_raw, dict):
                return None
            record = record_raw
            now = self._normalized_now()
            expires = _parse_utc(record.get("expires_at_utc"))
            if record.get("used_at_utc") is not None or expires is None or now >= expires:
                return None
            attempts_raw = record.get("verification_attempts", 0)
            maximum_raw = record.get("max_verification_attempts", 0)
            attempts = attempts_raw if isinstance(attempts_raw, int) else 0
            maximum = maximum_raw if isinstance(maximum_raw, int) else 0
            if maximum < 1 or attempts >= maximum:
                return None
            attempts += 1
            record["verification_attempts"] = attempts
            record["last_attempt_at_utc"] = now.isoformat()
            session_id = str(payload["session_id"])
            expected = record.get("otp_sha256")
            valid = isinstance(expected, str) and secrets.compare_digest(
                expected, _credential_sha256(session_id, otp)
            )
            if not valid:
                if attempts >= maximum:
                    record["locked_at_utc"] = now.isoformat()
                self._store.save(payload)
                return None
            resume_token = self._resume_token_factory()
            if len(resume_token) < 32:
                raise RuntimeError("resume token factory returned an undersized credential")
            payload["token_sha256"] = hashlib.sha256(resume_token.encode()).hexdigest()
            record["otp_sha256"] = None
            record["used_at_utc"] = now.isoformat()
            self._store.save(payload)
            return RecoveredLifePatternsSession(
                session_id=session_id,
                resume_token=resume_token,
            )

    def _normalized_now(self) -> datetime:
        value = self._clock()
        if value.tzinfo is None or value.utcoffset() is None:
            raise RuntimeError("recovery clock must be timezone-aware")
        return value.astimezone(UTC)

    def _private_records(self) -> tuple[dict[str, Any], ...]:
        records: list[dict[str, Any]] = []
        for path in sorted(self._store.root.glob("LP-*.json")):
            try:
                raw: Any = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, UnicodeError):
                continue
            if not isinstance(raw, dict):
                continue
            session_id = raw.get("session_id")
            if not isinstance(session_id, str):
                continue
            try:
                expected = self._store.read_private(session_id)
            except Exception:  # noqa: BLE001 - malformed private records are ignored for recovery lookup
                continue
            records.append(expected)
        return tuple(records)

    def _latest_matching_payload(self, lookup: str) -> dict[str, Any] | None:
        matches = [
            payload
            for payload in self._private_records()
            if isinstance(payload.get("contact_email_lookup_sha256"), str)
            and secrets.compare_digest(str(payload["contact_email_lookup_sha256"]), lookup)
        ]
        if not matches:
            return None
        return max(matches, key=lambda payload: str(payload.get("updated_at", "")))

    @staticmethod
    def _next_issue_window(
        previous: dict[str, Any],
        now: datetime,
        settings: LifePatternsRecoverySettings,
    ) -> tuple[datetime, int]:
        started = _parse_utc(previous.get("issue_window_started_at_utc"))
        count_raw = previous.get("issue_count_in_window", 0)
        count = count_raw if isinstance(count_raw, int) and count_raw >= 0 else 0
        if started is None or now - started >= settings.issue_window:
            return now, 1
        return started, count + 1

    @staticmethod
    def _issuance_allowed(
        payload: dict[str, Any],
        now: datetime,
        settings: LifePatternsRecoverySettings,
    ) -> bool:
        previous = payload.get("email_recovery")
        if not isinstance(previous, dict):
            return True
        issued = _parse_utc(previous.get("issued_at_utc"))
        if issued is not None and now - issued < settings.issue_cooldown:
            return False
        started = _parse_utc(previous.get("issue_window_started_at_utc"))
        count_raw = previous.get("issue_count_in_window", 0)
        count = count_raw if isinstance(count_raw, int) else 0
        return not (
            started is not None
            and now - started < settings.issue_window
            and count >= settings.max_issues_per_window
        )

    def _mark_delivery(self, session_id: str, issued_at: str, status: str) -> None:
        with self._lock:
            try:
                payload = self._store.read_private(session_id)
            except Exception:  # noqa: BLE001 - recovery delivery should not expose private lookup failures
                return
            record = payload.get("email_recovery")
            if not isinstance(record, dict) or record.get("issued_at_utc") != issued_at:
                return
            record["delivery_status"] = status
            record["delivery_updated_at_utc"] = self._normalized_now().isoformat()
            self._store.save(payload)
