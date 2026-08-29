from __future__ import annotations

from datetime import UTC, date, datetime, time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from hdmatch.api.relationship_study_app import create_relationship_study_app_from_env
from hdmatch.relationship.study import (
    BirthTimeSource,
    NoisePolicyStatus,
    PredictionLayerStatus,
    RelationshipBirthInput,
    RelationshipStudyIntake,
    bind_noise_policy,
    public_preflight,
)
from hdmatch.relationship.study_prediction import build_prediction_freeze


def _birth(*, day: int, hour: int | None) -> RelationshipBirthInput:
    return RelationshipBirthInput(
        birth_date=date(1990, 1, day),
        local_time=time(hour, 30) if hour is not None else None,
        birthplace="Example City, Example Country",
        iana_timezone="UTC",
        time_source=(BirthTimeSource.BIRTH_CERTIFICATE if hour is not None else BirthTimeSource.UNKNOWN),
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
    assert statuses["astro_rrf_directional_v0_4"] is PredictionLayerStatus.PENDING_ENGINE
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


def test_study_api_saves_intake_but_blocks_answers_before_predictions(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HDMATCH_RELATIONSHIP_STORE", str(tmp_path / "sessions"))
    monkeypatch.setenv("HDMATCH_REPO_ROOT", str(Path.cwd()))
    monkeypatch.delenv("HDMATCH_EPHEMERIS_PATH", raising=False)
    app = create_relationship_study_app_from_env()
    client = TestClient(app)
    response = client.post(
        "/api/study/intake",
        json={
            "intake": _intake(partner_hour=10).model_dump(mode="json"),
            "consent_to_llm_processing": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["preflight"]["birth_intake_complete"] is True
    assert body["preflight"]["confirmatory_ready"] is False
    assert "do not need to save" in body["participant_message"]

    blocked = client.post(
        f"/api/sessions/{body['session_id']}/answers",
        json={
            "token": body["resume_token"],
            "question_id": "RRQ_TRAJECTORY_CONTEXT",
            "field_answers": [],
        },
    )
    assert blocked.status_code == 409
    assert "prediction layers" in blocked.json()["detail"]
