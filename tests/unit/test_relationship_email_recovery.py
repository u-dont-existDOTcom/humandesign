from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi import HTTPException

from hdmatch.api.relationship_email_recovery import (
    EmailRecoveryService,
    EmailRecoverySettings,
)
from hdmatch.api.relationship_public_app import RelationshipFileStore
from hdmatch.relationship.study import normalize_email


def _settings() -> EmailRecoverySettings:
    return EmailRecoverySettings(
        smtp_host="smtp.example.test",
        smtp_port=587,
        smtp_security="starttls",
        smtp_username="study@example.test",
        smtp_password="railway-secret-only",
        from_address="study@example.test",
        public_base_url="https://relationship.example.test",
    )


def _study_session(
    store: RelationshipFileStore,
    email: str = "person@example.com",
) -> tuple[str, str]:
    payload, resume_token = store.create()
    payload["study_schema_version"] = "relationship-study-v1"
    normalized = normalize_email(email)
    payload["contact_email_lookup_sha256"] = hashlib.sha256(normalized.encode()).hexdigest()
    payload["email_verification_status"] = "unverified"
    store.save(payload)
    return str(payload["session_id"]), resume_token


def test_otp_recovery_stores_only_hashes_and_rotates_resume_token(tmp_path: Path) -> None:
    store = RelationshipFileStore(tmp_path)
    session_id, original_resume_token = _study_session(store)
    deliveries: list[tuple[str, str, str, str]] = []

    def capture_delivery(
        settings: EmailRecoverySettings,
        recipient: str,
        delivered_session_id: str,
        magic_token: str,
        otp: str,
    ) -> None:
        assert settings.smtp_password == "railway-secret-only"
        deliveries.append((recipient, delivered_session_id, magic_token, otp))

    service = EmailRecoveryService(
        store,
        _settings(),
        sender=capture_delivery,
        clock=lambda: datetime(2026, 8, 29, 22, 0, tzinfo=UTC),
        magic_token_factory=lambda: "m" * 43,
        resume_token_factory=lambda: "r" * 43,
        otp_factory=lambda: "654321",
    )
    service.request(" Person@Example.COM ")

    assert deliveries == [("person@example.com", session_id, "m" * 43, "654321")]
    saved = store.read_private(session_id)
    serialized = json.dumps(saved)
    assert "m" * 43 not in serialized
    assert "654321" not in serialized
    assert saved["email_recovery"]["delivery_status"] == "sent"
    assert saved["email_recovery"]["verification_attempts"] == 0

    recovered = service.verify_otp("person@example.com", "654321")
    assert recovered is not None
    assert recovered.session_id == session_id
    assert recovered.resume_token == "r" * 43
    assert service.verify_otp("person@example.com", "654321") is None
    with pytest.raises(HTTPException) as old_token_error:
        store.read(session_id, original_resume_token)
    assert old_token_error.value.status_code == 403
    assert store.read(session_id, "r" * 43)["email_verification_status"] == "verified"
    assert "r" * 43 not in json.dumps(store.read_private(session_id))


def test_magic_link_is_single_use_and_expires(tmp_path: Path) -> None:
    store = RelationshipFileStore(tmp_path)
    session_id, _ = _study_session(store)
    now = [datetime(2026, 8, 29, 22, 0, tzinfo=UTC)]
    service = EmailRecoveryService(
        store,
        _settings(),
        sender=lambda settings, recipient, sid, magic, otp: None,
        clock=lambda: now[0],
        magic_token_factory=lambda: "a" * 43,
        resume_token_factory=lambda: "b" * 43,
        otp_factory=lambda: "123456",
    )
    service.request("person@example.com")
    now[0] += timedelta(minutes=14, seconds=59)
    recovered = service.verify_magic(session_id, "a" * 43)
    assert recovered is not None
    assert service.verify_magic(session_id, "a" * 43) is None

    second_session_id, _ = _study_session(store, "second@example.com")
    service.request("second@example.com")
    now[0] += timedelta(minutes=15)
    assert service.verify_magic(second_session_id, "a" * 43) is None


def test_requests_are_throttled_and_unknown_email_has_same_noop_surface(
    tmp_path: Path,
) -> None:
    store = RelationshipFileStore(tmp_path)
    _study_session(store)
    deliveries: list[str] = []
    now = [datetime(2026, 8, 29, 22, 0, tzinfo=UTC)]
    service = EmailRecoveryService(
        store,
        _settings(),
        sender=lambda settings, recipient, sid, magic, otp: deliveries.append(recipient),
        clock=lambda: now[0],
    )
    service.request("person@example.com")
    service.request("person@example.com")
    service.request("missing@example.com")
    assert deliveries == ["person@example.com"]

    for _ in range(4):
        now[0] += timedelta(seconds=61)
        service.request("person@example.com")
    assert len(deliveries) == 5
    now[0] += timedelta(seconds=61)
    service.request("person@example.com")
    assert len(deliveries) == 5


def test_verification_attempt_limit_locks_both_recovery_credentials(tmp_path: Path) -> None:
    store = RelationshipFileStore(tmp_path)
    session_id, _ = _study_session(store)
    settings = replace(_settings(), max_verification_attempts=2)
    service = EmailRecoveryService(
        store,
        settings,
        sender=lambda settings, recipient, sid, magic, otp: None,
        clock=lambda: datetime(2026, 8, 29, 22, 0, tzinfo=UTC),
        magic_token_factory=lambda: "a" * 43,
        resume_token_factory=lambda: "b" * 43,
        otp_factory=lambda: "123456",
    )
    service.request("person@example.com")
    assert service.verify_otp("person@example.com", "000000") is None
    assert service.verify_magic(session_id, "wrong" * 9) is None
    assert service.verify_otp("person@example.com", "123456") is None
    record = store.read_private(session_id)["email_recovery"]
    assert record["verification_attempts"] == 2
    assert record["locked_at_utc"] is not None


def test_environment_defaults_require_only_the_railway_password_secret() -> None:
    assert EmailRecoverySettings.from_env({}) is None
    settings = EmailRecoverySettings.from_env(
        {"HDMATCH_SMTP_PASSWORD": "not-committed"}
    )
    assert settings is not None
    assert settings.smtp_host == "smtp.porkbun.com"
    assert settings.smtp_port == 587
    assert settings.smtp_security == "starttls"
    assert settings.smtp_username == "joel@u-dont-exist.com"
    assert settings.from_address == "joel@u-dont-exist.com"
    assert settings.smtp_password == "not-committed"
    assert settings.public_base_url == (
        "https://relationship-web-production.up.railway.app"
    )
