from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta, timezone
from pathlib import Path

import pytest

from hdmatch.relationship.study import (
    BirthTimeSource,
    NoisePolicyStatus,
    PredictionLayerStatus,
    RelationshipBirthInput,
    RelationshipStudyIntake,
    bind_noise_policy,
    file_sha256,
    public_preflight,
)
from hdmatch.relationship.study_prediction import (
    ASTRO_RRF_ATOMIC_SCHEMA_FILE,
    build_prediction_freeze,
)


def _birth(*, day: int, hour: int | None) -> RelationshipBirthInput:
    return RelationshipBirthInput(
        birth_date=date(1990, 1, day),
        local_time=time(hour, 30) if hour is not None else None,
        birthplace="Example City, Example Country",
        iana_timezone="UTC",
        time_source=(
            BirthTimeSource.BIRTH_CERTIFICATE
            if hour is not None
            else BirthTimeSource.UNKNOWN
        ),
    )


def _intake(*, partner_hour: int | None = None) -> RelationshipStudyIntake:
    return RelationshipStudyIntake(
        contact_email=" Person@Example.COM ",
        respondent_birth=_birth(day=1, hour=12),
        partner_birth=_birth(day=2, hour=partner_hour),
        consent_to_store_private_research_data=True,
        consent_to_process_partner_birth_data=True,
        created_at_utc=datetime(2026, 8, 29, 20, 0, tzinfo=UTC),
    )


def test_intake_normalizes_email_and_hashes_birth_separately() -> None:
    intake = _intake()
    assert intake.contact_email == "person@example.com"
    assert intake.contact_email_lookup_sha256 is not None
    assert len(intake.contact_email_lookup_sha256) == 64
    assert len(intake.birth_input_sha256) == 64
    assert "person@example.com" not in intake.birth_input_sha256


def test_unknown_time_is_explicit_and_cannot_have_uncertainty_window() -> None:
    with pytest.raises(ValueError, match="unknown birth time"):
        RelationshipBirthInput(
            birth_date=date(1990, 1, 1),
            local_time=None,
            birthplace="Example",
            iana_timezone="UTC",
            time_source=BirthTimeSource.UNKNOWN,
            uncertainty_minutes=60,
        )


def test_local_birth_time_rejects_offsets_and_fractional_seconds() -> None:
    with pytest.raises(ValueError, match="must not include a UTC offset"):
        RelationshipBirthInput(
            birth_date=date(1990, 1, 1),
            local_time=time(10, 30, tzinfo=timezone(timedelta(hours=1))),
            birthplace="Example",
            iana_timezone="UTC",
            time_source=BirthTimeSource.BIRTH_CERTIFICATE,
        )

    with pytest.raises(ValueError, match="whole-second precision"):
        RelationshipBirthInput(
            birth_date=date(1990, 1, 1),
            local_time=time(10, 30, 0, 1),
            birthplace="Example",
            iana_timezone="UTC",
            time_source=BirthTimeSource.BIRTH_CERTIFICATE,
        )


def test_noise_binding_is_pending_until_artifact_exists(tmp_path: Path) -> None:
    pending = bind_noise_policy(None)
    assert pending.status is NoisePolicyStatus.PENDING_AUTHORITATIVE_ARTIFACT
    artifact = tmp_path / "noise.json"
    artifact.write_text('{"schema_version":"noise-v1","ok":true}\n', encoding="utf-8")
    bound = bind_noise_policy(artifact)
    assert bound.status is NoisePolicyStatus.ARTIFACT_BOUND
    assert bound.source_schema_version == "noise-v1"
    assert bound.source_sha256 is not None


def test_prediction_freeze_binds_models_but_stays_locked_without_engines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("HDMATCH_EPHEMERIS_PATH", raising=False)
    root = Path.cwd()
    intake = _intake(partner_hour=10)
    freeze = build_prediction_freeze(
        session_id="RR-TEST",
        intake=intake,
        repo_root=root,
        questionnaire_path=Path("reference/relationship/relationship_dynamic_questionnaire_v1.json"),
        noise_policy=bind_noise_policy(None),
        code_commit="test-commit",
    )
    statuses = {layer.layer_id: layer.status for layer in freeze.layers}
    assert statuses["human_design_connection_v1"] is PredictionLayerStatus.PENDING_ENGINE
    assert statuses["astro_rrf_directional_v0_4"] is PredictionLayerStatus.INSUFFICIENT_BIRTH_DATA
    astro_layer = next(
        layer for layer in freeze.layers if layer.layer_id == "astro_rrf_directional_v0_4"
    )
    receipts = {
        item["path"]: item["sha256"] for item in astro_layer.payload["frozen_model_files"]
    }
    assert receipts[ASTRO_RRF_ATOMIC_SCHEMA_FILE] == file_sha256(
        root / ASTRO_RRF_ATOMIC_SCHEMA_FILE
    )
    assert freeze.confirmatory_ready is False
    assert len(freeze.freeze_sha256) == 64

    preflight = public_preflight(
        session_id="RR-TEST",
        intake=intake,
        prediction_freeze=freeze,
    )
    dumped = preflight.model_dump_json()
    assert preflight.contact_email_on_file is True
    assert preflight.confirmatory_ready is False
    assert "person@example.com" not in dumped
    assert "Example City" not in dumped


def test_birth_change_changes_prediction_freeze_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HDMATCH_EPHEMERIS_PATH", raising=False)
    root = Path.cwd()
    first = _intake(partner_hour=10)
    second = RelationshipStudyIntake(
        contact_email=first.contact_email,
        respondent_birth=first.respondent_birth,
        partner_birth=RelationshipBirthInput(
            birth_date=date(1990, 1, 3),
            local_time=time(10, 30),
            birthplace="Example City, Example Country",
            iana_timezone="UTC",
            time_source=BirthTimeSource.BIRTH_CERTIFICATE,
        ),
        consent_to_store_private_research_data=True,
        consent_to_process_partner_birth_data=True,
        created_at_utc=first.created_at_utc,
    )
    kwargs = {
        "session_id": "RR-TEST",
        "repo_root": root,
        "questionnaire_path": Path(
            "reference/relationship/relationship_dynamic_questionnaire_v1.json"
        ),
        "noise_policy": bind_noise_policy(None),
        "code_commit": "test-commit",
    }
    freeze_a = build_prediction_freeze(intake=first, **kwargs)
    freeze_b = build_prediction_freeze(intake=second, **kwargs)
    assert freeze_a.birth_input_sha256 != freeze_b.birth_input_sha256
    assert freeze_a.freeze_sha256 != freeze_b.freeze_sha256
