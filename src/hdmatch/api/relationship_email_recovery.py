"""Private SMTP magic-link and one-time-code recovery for relationship sessions.

The persistent session record contains only domain-separated SHA-256 credential
hashes. A successful recovery rotates the normal resume token, so an emailed
credential is single-use and the previous browser credential is invalidated.
"""

from __future__ import annotations

import base64
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
from typing import Any, Literal, cast

from fastapi import HTTPException

from hdmatch.api.relationship_public_app import RelationshipFileStore
from hdmatch.relationship.study import normalize_email

SMTP_SECURITY = Literal["starttls", "ssl"]
Clock = Callable[[], datetime]
SecretFactory = Callable[[], str]
OtpFactory = Callable[[], str]
RecoverySender = Callable[["EmailRecoverySettings", str, str, str, str], None]


@dataclass(frozen=True)
class EmailRecoverySettings:
    smtp_host: str
    smtp_port: int
    smtp_security: SMTP_SECURITY
    smtp_username: str
    smtp_password: str
    from_address: str
    public_base_url: str
    credential_ttl: timedelta = timedelta(minutes=15)
    issue_cooldown: timedelta = timedelta(seconds=60)
    issue_window: timedelta = timedelta(hours=1)
    max_issues_per_window: int = 5
    max_verification_attempts: int = 8
    smtp_timeout_seconds: float = 20.0

    @classmethod
    def from_env(
        cls, values: Mapping[str, str] | None = None
    ) -> EmailRecoverySettings | None:
        environment = os.environ if values is None else values
        password = environment.get("HDMATCH_SMTP_PASSWORD", "")
        if not password:
            return None
        security_raw = environment.get("HDMATCH_SMTP_SECURITY", "starttls").strip().lower()
        if security_raw not in {"starttls", "ssl"}:
            raise RuntimeError("HDMATCH_SMTP_SECURITY must be 'starttls' or 'ssl'")
        security = cast(SMTP_SECURITY, security_raw)
        port_default = "465" if security == "ssl" else "587"
        try:
            port = int(environment.get("HDMATCH_SMTP_PORT", port_default))
        except ValueError as exc:
            raise RuntimeError("HDMATCH_SMTP_PORT must be an integer") from exc
        if not 1 <= port <= 65535:
            raise RuntimeError("HDMATCH_SMTP_PORT must be between 1 and 65535")
        username = environment.get(
            "HDMATCH_SMTP_USERNAME", "joel@u-dont-exist.com"
        ).strip()
        from_address = environment.get("HDMATCH_SMTP_FROM", username).strip()
        host = environment.get("HDMATCH_SMTP_HOST", "smtp.porkbun.com").strip()
        public_base_url = environment.get(
            "HDMATCH_PUBLIC_BASE_URL",
            "https://relationship-web-production.up.railway.app",
        ).strip().rstrip("/")
        if not host or not username or not from_address or not public_base_url:
            raise RuntimeError("SMTP host, username, sender, and public base URL are required")
        return cls(
            smtp_host=host,
            smtp_port=port,
            smtp_security=security,
            smtp_username=username,
            smtp_password=password,
            from_address=from_address,
            public_base_url=public_base_url,
        )


@dataclass(frozen=True)
class RecoveredSession:
    session_id: str
    resume_token: str


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _random_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def _credential_sha256(session_id: str, kind: str, credential: str) -> str:
    encoded = f"relationship-recovery-v1\x00{session_id}\x00{kind}\x00{credential}".encode()
    return hashlib.sha256(encoded).hexdigest()


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


def _recovery_fragment(session_id: str, magic_token: str) -> str:
    payload = json.dumps(
        {"session_id": session_id, "magic_token": magic_token},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return base64.urlsafe_b64encode(payload).decode().rstrip("=")


def send_recovery_email(
    settings: EmailRecoverySettings,
    recipient: str,
    session_id: str,
    magic_token: str,
    otp: str,
) -> None:
    """Send one recovery email over authenticated TLS without logging credentials."""

    magic_link = (
        f"{settings.public_base_url}/#recovery="
        f"{_recovery_fragment(session_id, magic_token)}"
    )
    minutes = max(1, int(settings.credential_ttl.total_seconds() // 60))
    message = EmailMessage()
    message["Subject"] = "Resume your Relationship Pattern Lab study"
    message["From"] = settings.from_address
    message["To"] = recipient
    message.set_content(
        "Resume your private Relationship Pattern Lab study.\n\n"
        f"Magic link (single use): {magic_link}\n\n"
        f"Or enter this one-time code: {otp}\n"
        f"Session reference: {session_id}\n\n"
        f"The link and code expire in {minutes} minutes. If you did not request "
        "this email, you can ignore it."
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


class EmailRecoveryService:
    """Issue and consume private recovery credentials with persistent rate bounds."""

    def __init__(
        self,
        store: RelationshipFileStore,
        settings: EmailRecoverySettings | None,
        *,
        sender: RecoverySender = send_recovery_email,
        clock: Clock = _now_utc,
        magic_token_factory: SecretFactory = lambda: secrets.token_urlsafe(32),
        resume_token_factory: SecretFactory = lambda: secrets.token_urlsafe(32),
        otp_factory: OtpFactory = _random_otp,
    ) -> None:
        self._store = store
        self._settings = settings
        self._sender = sender
        self._clock = clock
        self._magic_token_factory = magic_token_factory
        self._resume_token_factory = resume_token_factory
        self._otp_factory = otp_factory
        self._lock = threading.Lock()

    @property
    def configured(self) -> bool:
        return self._settings is not None

    def request(self, email: str) -> None:
        """Issue recovery privately; callers must always return a generic response."""

        settings = self._settings
        if settings is None:
            return
        normalized = normalize_email(email)
        email_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        now = self._normalized_now()
        with self._lock:
            payload = self._latest_matching_payload(email_sha256)
            if payload is None or not self._issuance_allowed(payload, now, settings):
                return
            session_id = str(payload["session_id"])
            magic_token = self._magic_token_factory()
            otp = self._otp_factory()
            if len(magic_token) < 32:
                raise RuntimeError("magic token factory returned an undersized credential")
            if len(otp) != 6 or not otp.isdigit():
                raise RuntimeError("OTP factory must return exactly six digits")
            previous = payload.get("email_recovery")
            previous_record = previous if isinstance(previous, dict) else {}
            window_started, issue_count = self._next_issue_window(
                previous_record, now, settings
            )
            issued_at = now.isoformat()
            payload["email_recovery"] = {
                "schema_version": "relationship-email-recovery-v1",
                "issued_at_utc": issued_at,
                "expires_at_utc": (now + settings.credential_ttl).isoformat(),
                "magic_token_sha256": _credential_sha256(
                    session_id, "magic", magic_token
                ),
                "otp_sha256": _credential_sha256(session_id, "otp", otp),
                "verification_attempts": 0,
                "max_verification_attempts": settings.max_verification_attempts,
                "used_at_utc": None,
                "issue_window_started_at_utc": window_started.isoformat(),
                "issue_count_in_window": issue_count,
                "delivery_status": "attempting",
            }
            payload["email_verification_status"] = "pending"
            self._store.save(payload)
        try:
            self._sender(settings, normalized, session_id, magic_token, otp)
        except (OSError, smtplib.SMTPException):
            self._mark_delivery(session_id, issued_at, "failed")
            return
        self._mark_delivery(session_id, issued_at, "sent")

    def verify_otp(self, email: str, otp: str) -> RecoveredSession | None:
        normalized = normalize_email(email)
        email_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        with self._lock:
            payload = self._latest_matching_payload(email_sha256)
            if payload is None:
                return None
            return self._consume(payload, "otp", otp)

    def verify_magic(self, session_id: str, magic_token: str) -> RecoveredSession | None:
        with self._lock:
            try:
                payload = self._store.read_private(session_id)
            except HTTPException:
                return None
            if payload.get("study_schema_version") != "relationship-study-v1":
                return None
            return self._consume(payload, "magic", magic_token)

    def _normalized_now(self) -> datetime:
        value = self._clock()
        if value.tzinfo is None or value.utcoffset() is None:
            raise RuntimeError("email recovery clock must be timezone-aware")
        return value.astimezone(UTC)

    def _latest_matching_payload(self, email_sha256: str) -> dict[str, Any] | None:
        matches = [
            payload
            for payload in self._store.private_records()
            if payload.get("study_schema_version") == "relationship-study-v1"
            and isinstance(payload.get("contact_email_lookup_sha256"), str)
            and secrets.compare_digest(
                str(payload["contact_email_lookup_sha256"]), email_sha256
            )
        ]
        if not matches:
            return None
        return max(matches, key=lambda payload: str(payload.get("updated_at", "")))

    @staticmethod
    def _next_issue_window(
        previous: dict[str, Any],
        now: datetime,
        settings: EmailRecoverySettings,
    ) -> tuple[datetime, int]:
        window_started = _parse_utc(previous.get("issue_window_started_at_utc"))
        count_raw = previous.get("issue_count_in_window", 0)
        count = count_raw if isinstance(count_raw, int) and count_raw >= 0 else 0
        if window_started is None or now - window_started >= settings.issue_window:
            return now, 1
        return window_started, count + 1

    @staticmethod
    def _issuance_allowed(
        payload: dict[str, Any],
        now: datetime,
        settings: EmailRecoverySettings,
    ) -> bool:
        previous = payload.get("email_recovery")
        if not isinstance(previous, dict):
            return True
        last_issued = _parse_utc(previous.get("issued_at_utc"))
        if last_issued is not None and now - last_issued < settings.issue_cooldown:
            return False
        window_started = _parse_utc(previous.get("issue_window_started_at_utc"))
        count_raw = previous.get("issue_count_in_window", 0)
        count = count_raw if isinstance(count_raw, int) else 0
        return not (
            window_started is not None
            and now - window_started < settings.issue_window
            and count >= settings.max_issues_per_window
        )

    def _mark_delivery(self, session_id: str, issued_at: str, status: str) -> None:
        with self._lock:
            try:
                payload = self._store.read_private(session_id)
            except HTTPException:
                return
            record = payload.get("email_recovery")
            if not isinstance(record, dict) or record.get("issued_at_utc") != issued_at:
                return
            record["delivery_status"] = status
            record["delivery_updated_at_utc"] = self._normalized_now().isoformat()
            self._store.save(payload)

    def _consume(
        self,
        payload: dict[str, Any],
        kind: Literal["magic", "otp"],
        supplied: str,
    ) -> RecoveredSession | None:
        record_raw = payload.get("email_recovery")
        if not isinstance(record_raw, dict):
            return None
        record = cast(dict[str, Any], record_raw)
        now = self._normalized_now()
        expires_at = _parse_utc(record.get("expires_at_utc"))
        if (
            record.get("used_at_utc") is not None
            or expires_at is None
            or now >= expires_at
        ):
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
        expected = record.get(f"{kind}_token_sha256" if kind == "magic" else "otp_sha256")
        session_id = str(payload.get("session_id", ""))
        supplied_hash = _credential_sha256(session_id, kind, supplied)
        valid = isinstance(expected, str) and secrets.compare_digest(expected, supplied_hash)
        if not valid:
            if attempts >= maximum:
                record["locked_at_utc"] = now.isoformat()
            self._store.save(payload)
            return None
        resume_token = self._resume_token_factory()
        if len(resume_token) < 32:
            raise RuntimeError("resume token factory returned an undersized credential")
        payload["token_sha256"] = hashlib.sha256(resume_token.encode()).hexdigest()
        payload["email_verification_status"] = "verified"
        record["used_at_utc"] = now.isoformat()
        record["verification_method"] = kind
        record["magic_token_sha256"] = None
        record["otp_sha256"] = None
        self._store.save(payload)
        return RecoveredSession(session_id=session_id, resume_token=resume_token)
