from __future__ import annotations

import asyncio
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

import pytest
import yaml
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import Mount
from starlette.types import Message, Scope

import hdmatch.api.relationship_launch_app as relationship_launch_app
import hdmatch.api.relationship_public_app as relationship_base_app
from hdmatch.api.natal_pilot_app import NatalPilotConfig, create_natal_pilot_app
from hdmatch.api.natal_pilot_ui import render_natal_pilot_html
from hdmatch.participant.models import (
    BirthIntake,
    ConfirmatoryLock,
    EvidenceInput,
    EvidenceRecord,
    FrozenDimensionBinding,
    PredictionFreezeRef,
    PublicProgress,
    RankScope,
    SessionMode,
    SessionPhase,
    SessionRecord,
    StoredEvidenceInput,
)
from hdmatch.participant.service import ParticipantSessionService
from hdmatch.runtime.century_cache import (
    GlobalCandidateState,
    structural_features_sha256,
    write_verified_century_cache,
)
from hdmatch.runtime.chart_adapter import ExactChartAdapter
from hdmatch.schemas import StructuralChartFeatures

PROJECT_ROOT = Path(__file__).parents[2]


@dataclass(frozen=True)
class AsgiResponse:
    status_code: int
    headers: dict[str, str]
    body: bytes

    @property
    def text(self) -> str:
        return self.body.decode("utf-8")

    @property
    def json(self) -> dict[str, Any]:
        value = json.loads(self.body)
        assert isinstance(value, dict)
        return cast(dict[str, Any], value)


class FakeSessions:
    def __init__(self) -> None:
        self.created: list[BirthIntake] = []
        self.appended: list[EvidenceInput] = []
        self.lock_calls: list[str] = []
        self.lock_quality_flags: list[bool] = []

    def create_session(self, intake: BirthIntake) -> SessionRecord:
        self.created.append(intake)
        return SessionRecord(
            session_id="HD-" + "A" * 32,
            mode=SessionMode.SCIENTIFIC_BLIND,
            ranking_scope=RankScope.KNOWN_BIRTH_MONTH,
            created_at_utc=datetime(2026, 8, 31, 20, 0, tzinfo=UTC),
            prediction_freeze_sha256="b" * 64,
        )

    def public_progress(self, session_id: str) -> PublicProgress:
        return PublicProgress(
            session_id=session_id,
            phase=SessionPhase.CONFIRMATORY_BLIND,
            confirmatory_observation_count=len(self.appended),
            scoreable_observation_count=len(self.appended),
            non_natal_observation_count=0,
            mapped_scoreable_question_count=len(self.appended),
            mapped_scoreable_coverage=0.0,
            adequately_assessed_mapped_question_count=0,
            unassessed_mapped_question_count=len(self.appended),
            mapped_question_quality_gate_passed=False,
        )

    def append_evidence(
        self,
        session_id: str,
        evidence: EvidenceInput,
    ) -> EvidenceRecord:
        self.appended.append(evidence)
        stored = StoredEvidenceInput.model_validate(evidence.model_dump())
        if evidence.question_id is not None:
            stored = stored.model_copy(
                update={
                    "frozen_dimension_binding": FrozenDimensionBinding(
                        question_id=evidence.question_id,
                        resolved_cluster_id="SERVER-ONLY",
                        freeze_ref=PredictionFreezeRef(
                            session_id=session_id,
                            freeze_sha256="f" * 64,
                        ),
                        dimension_index=0,
                        resolved_at_utc=datetime(2026, 8, 31, 20, 1, tzinfo=UTC),
                    )
                }
            )
        return EvidenceRecord(
            evidence_id=f"EV-{len(self.appended)}",
            session_id=session_id,
            phase="confirmatory_blind",
            created_at_utc=datetime(2026, 8, 31, 20, 1, tzinfo=UTC),
            evidence=stored,
        )

    def lock_confirmatory(
        self,
        session_id: str,
        *,
        require_mapped_question_quality: bool = False,
    ) -> ConfirmatoryLock:
        self.lock_calls.append(session_id)
        self.lock_quality_flags.append(require_mapped_question_quality)
        return ConfirmatoryLock(
            session_id=session_id,
            locked_at_utc=datetime(2026, 8, 31, 20, 2, tzinfo=UTC),
            evidence_ids=(),
            scoring_responses=(),
            scoring_responses_sha256="c" * 64,
            excluded_non_natal_evidence_count=0,
            adequately_assessed_mapped_question_count=0,
            mapped_scoreable_question_count=0,
        )


def _request(
    app: FastAPI,
    method: str,
    url: str,
    *,
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> AsgiResponse:
    parsed = urlsplit(url)
    encoded = b"" if body is None else json.dumps(body).encode("utf-8")
    raw_headers = [(b"accept", b"application/json")]
    if body is not None:
        raw_headers.extend(
            (
                (b"content-type", b"application/json"),
                (b"content-length", str(len(encoded)).encode("ascii")),
            )
        )
    raw_headers.extend(
        (name.lower().encode("ascii"), value.encode("utf-8"))
        for name, value in (headers or {}).items()
    )
    scope: Scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": method,
        "scheme": "https",
        "path": parsed.path,
        "raw_path": parsed.path.encode("ascii"),
        "query_string": parsed.query.encode("ascii"),
        "root_path": "",
        "headers": raw_headers,
        "client": ("test", 123),
        "server": ("testserver", 443),
        "state": {},
    }
    sent: list[Message] = []
    delivered = False

    async def receive() -> Message:
        nonlocal delivered
        if delivered:
            return {"type": "http.disconnect"}
        delivered = True
        return {"type": "http.request", "body": encoded, "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    asyncio.run(app(scope, receive, send))
    start = next(message for message in sent if message["type"] == "http.response.start")
    response_body = b"".join(
        message.get("body", b"") for message in sent if message["type"] == "http.response.body"
    )
    response_headers = {
        key.decode("latin-1"): value.decode("latin-1") for key, value in start["headers"]
    }
    return AsgiResponse(start["status"], response_headers, response_body)


def _app(tmp_path: Path, sessions: FakeSessions, token: str = "owner-code") -> FastAPI:
    template = (
        PROJECT_ROOT / "reference/custom_gpt/participant_interviewer_action_openapi_v1.yaml"
    ).read_text(encoding="utf-8")
    config = NatalPilotConfig(
        invite_token_sha256=hashlib.sha256(token.encode()).hexdigest(),
        invite_state_root=tmp_path / "invites",
        health_probe_root=tmp_path / "sessions" / ".health",
        public_base_url="https://example.test",
        interviewer_url="https://chatgpt.com/g/g-test-astrohd",
        interviewer_model_receipt="custom-gpt-test-config:gpt-5.6",
        action_schema_template=template,
        runtime_receipt={
            "model_version": "test-model",
            "automatic_model_updates": False,
        },
    )
    return create_natal_pilot_app(
        sessions=cast(ParticipantSessionService, sessions),
        config=config,
    )


def _birth() -> dict[str, Any]:
    return {
        "local_datetime": "1994-01-28T00:35:07",
        "birthplace": "Istanbul, Türkiye",
        "iana_timezone": "Europe/Istanbul",
        "fold": None,
        "mode": "scientific_blind",
        "ranking_scope": "known_birth_month",
    }


def test_intake_is_natal_first_explicit_time_and_truthfully_versioned(tmp_path: Path) -> None:
    app = _app(tmp_path, FakeSessions())
    response = _request(app, "GET", "/")

    assert response.status_code == 200
    assert "first real blinded test of astrology and Human Design" in response.text
    assert "Please do not take this interview in a rush" in response.text
    assert "an incomplete interview will not produce a scientific result" in response.text
    assert 'id="effortAcknowledgment"' in response.text
    assert "One-time owner-test invitation code" in response.text
    assert "Copy both credentials" in response.text
    assert "There is deliberately no credential-bearing magic link" in response.text
    assert "rare case when daylight-saving clocks" in response.text
    assert 'id="birthHour"' in response.text
    assert 'id="birthMinute"' in response.text
    assert 'id="birthSecond"' in response.text
    assert 'type="datetime-local"' not in response.text
    assert "does not silently retrain" in response.text
    assert "developmental symbolic model" in response.text
    assert "https://chatgpt.com/g/g-test-astrohd" in response.text
    assert 'id="openAIConsent"' in response.text
    assert "exact birth record and raw chart stay on this trusted site" in response.text
    assert "localStorage" not in response.text


def test_copy_failure_handler_preserves_the_credential_container() -> None:
    html = render_natal_pilot_html(None)
    function = re.search(r"function showCredentialCopyFailure\([^}]+\}", html)
    assert function is not None
    assert "catch(error){showCredentialCopyFailure(copyMessage,error)}" in html
    probe = (
        function.group(0)
        + """
const credentials={textContent:'one-time-session-id and token'};
const classes=[];
const message={textContent:'',classList:{add:value=>classes.push(value)}};
showCredentialCopyFailure(message,new Error('copy failed'));
if(credentials.textContent!=='one-time-session-id and token')process.exit(2);
if(!classes.includes('error'))process.exit(3);
if(!message.textContent.includes('still shown above'))process.exit(4);
"""
    )
    completed = subprocess.run(
        ["node", "-e", probe],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert completed.returncode == 0, completed.stderr


def test_interviewer_url_is_validated_and_script_escaped(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="chatgpt.com"):
        NatalPilotConfig(
            invite_token_sha256="a" * 64,
            invite_state_root=tmp_path / "invites",
            health_probe_root=tmp_path / "health",
            public_base_url="https://example.test",
            interviewer_url="https://example.test/g/not-chatgpt",
            interviewer_model_receipt="test",
            action_schema_template="openapi: 3.1.0",
            runtime_receipt={},
        )

    rendered = render_natal_pilot_html("https://chatgpt.com/g/test</script><script>alert(1)")
    assert "</script><script>alert(1)" not in rendered
    assert "\\u003c/script>" in rendered


def test_single_use_invite_requires_consent_and_never_stores_raw_token(
    tmp_path: Path,
) -> None:
    sessions = FakeSessions()
    app = _app(tmp_path, sessions)
    headers = {
        "x-astrohd-pilot-token": "owner-code",
        "x-astrohd-storage-consent": "yes",
        "x-astrohd-openai-consent": "yes",
        "x-astrohd-development-consent": "yes",
    }

    missing_openai_consent = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
        },
    )
    assert missing_openai_consent.status_code == 400
    assert not (tmp_path / "invites").exists()

    missing = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )
    assert missing.status_code == 403
    assert missing.json["error"]["message"] == "invalid or unavailable pilot access code"

    created = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers=headers,
    )
    assert created.status_code == 200
    assert created.json["session_id"] == "HD-" + "A" * 32
    session_token = str(created.json["session_token"])
    assert len(session_token) >= 32
    assert len(sessions.created) == 1

    receipt_path = next((tmp_path / "invites").glob("*.json"))
    receipt = receipt_path.read_text(encoding="utf-8")
    assert "owner-code" not in receipt
    assert session_token not in receipt
    assert '"consent_to_private_research_storage": true' in receipt
    assert '"consent_to_future_deidentified_model_development": true' in receipt
    assert '"consent_to_openai_redacted_interview_processing": true' in receipt
    assert oct(receipt_path.stat().st_mode & 0o777) == "0o600"
    access_path = tmp_path / "invites" / "session-access" / f"{created.json['session_id']}.json"
    access_receipt = access_path.read_text(encoding="utf-8")
    assert session_token not in access_receipt
    assert hashlib.sha256(session_token.encode()).hexdigest() in access_receipt
    assert oct(access_path.stat().st_mode & 0o777) == "0o600"

    replay = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers=headers,
    )
    assert replay.status_code == 410
    assert len(sessions.created) == 1


def test_invite_rotation_preserves_and_migrates_existing_session_access(tmp_path: Path) -> None:
    sessions = FakeSessions()
    original = _app(tmp_path, sessions, token="owner-code")
    created = _request(
        original,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )
    session_id = str(created.json["session_id"])
    session_token = str(created.json["session_token"])
    access_path = tmp_path / "invites" / "session-access" / f"{session_id}.json"
    access_path.unlink()

    rotated = _app(tmp_path, sessions, token="fresh-owner-code")
    progress = _request(
        rotated,
        "POST",
        "/v1/interviewer/progress",
        body={"session_id": session_id, "session_token": session_token},
    )

    assert progress.status_code == 200
    assert access_path.exists()


def test_validation_failure_does_not_consume_invite_and_has_structured_error(
    tmp_path: Path,
) -> None:
    sessions = FakeSessions()
    app = _app(tmp_path, sessions)
    headers = {
        "x-astrohd-pilot-token": "owner-code",
        "x-astrohd-storage-consent": "yes",
        "x-astrohd-openai-consent": "yes",
    }
    invalid = _birth()
    invalid["local_datetime"] = "not-a-date"

    rejected = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=invalid,
        headers=headers,
    )
    assert rejected.status_code == 422
    assert rejected.json["error"]["code"] == "REQUEST_VALIDATION_FAILED"
    assert not (tmp_path / "invites").exists()

    accepted = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers=headers,
    )
    assert accepted.status_code == 200
    assert len(sessions.created) == 1


def test_health_probes_private_storage_and_action_schema_excludes_birth_intake(
    tmp_path: Path,
) -> None:
    app = _app(tmp_path, FakeSessions())

    health = _request(app, "GET", "/healthz")
    assert health.status_code == 200
    assert health.json["scope"] == "owner_only_exact_time_natal_pilot"
    assert health.json["predictions_frozen_before_answers"] is True
    assert health.json["automatic_model_updates"] is False
    assert list((tmp_path / "sessions" / ".health").iterdir()) == []

    schema = _request(app, "GET", "/interviewer-action-openapi.yaml")
    assert schema.status_code == 200
    assert "https://example.test/astrohd" in schema.text
    assert "https://YOUR_API_HOST" not in schema.text
    assert "BirthIntake" not in schema.text
    assert "X-AstroHD-Session-Token" not in schema.text
    assert "in: header" not in schema.text
    reveal_route = next(
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.path == "/v1/interviewer/reveal"
    )
    response_fields = reveal_route.response_model.model_fields  # type: ignore[union-attr]
    assert "birth" not in response_fields
    assert "chart" not in response_fields


def test_session_id_alone_cannot_access_interview_routes(tmp_path: Path) -> None:
    app = _app(tmp_path, FakeSessions())
    created = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )
    session_id = str(created.json["session_id"])

    missing = _request(app, "GET", f"/v1/participant-sessions/{session_id}/progress")
    wrong = _request(
        app,
        "GET",
        f"/v1/participant-sessions/{session_id}/progress",
        headers={"x-astrohd-session-token": "wrong"},
    )

    assert missing.status_code == 403
    assert wrong.status_code == 403
    assert missing.json["error"]["message"] == "invalid session access"


def test_interviewer_body_capability_rejects_missing_or_wrong_token(
    tmp_path: Path,
) -> None:
    sessions = FakeSessions()
    app = _app(tmp_path, sessions)
    created = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )
    session_id = str(created.json["session_id"])
    session_token = str(created.json["session_token"])

    missing = _request(
        app,
        "POST",
        "/v1/interviewer/progress",
        body={"session_id": session_id},
    )
    wrong = _request(
        app,
        "POST",
        "/v1/interviewer/progress",
        body={"session_id": session_id, "session_token": "x" * 32},
    )
    allowed = _request(
        app,
        "POST",
        "/v1/interviewer/progress",
        body={"session_id": session_id, "session_token": session_token},
    )

    assert missing.status_code == 422
    assert wrong.status_code == 403
    assert wrong.json["error"]["message"] == "invalid session access"
    assert allowed.status_code == 200
    assert allowed.json["true_birth_rank_concealed"] is True


def test_hidden_cluster_or_prediction_is_not_exposed_to_action(tmp_path: Path) -> None:
    sessions = FakeSessions()
    app = _app(tmp_path, sessions)
    created = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )
    session_id = str(created.json["session_id"])
    response = _request(
        app,
        "POST",
        "/v1/interviewer/evidence",
        body={
            "session_id": session_id,
            "session_token": str(created.json["session_token"]),
            "evidence": {
                "domain": "trait",
                "question_id": "Q-TEST",
                "answer": "sometimes",
                "narrative": "It depends strongly on context.",
                "minimum_evidence_passed": True,
                "consistency_status": "consistent",
                "quality_rationale": "The participant supplied the required context.",
            },
        },
    )

    assert response.status_code == 200
    assert response.json["evidence"]["narrative"] == "It depends strongly on context."
    assert "cluster_id" not in response.json["evidence"]
    assert "frozen_dimension_binding" not in response.json["evidence"]
    assert len(sessions.appended) == 1
    assert sessions.appended[0].question_id == "Q-TEST"


@pytest.mark.parametrize(
    "field",
    ["cluster_id", "resolved_cluster_id", "frozen_cluster_id", "frozen_dimension_ref"],
)
def test_interviewer_evidence_rejects_client_binding_fields(
    tmp_path: Path,
    field: str,
) -> None:
    sessions = FakeSessions()
    app = _app(tmp_path, sessions)
    created = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )
    evidence = {"domain": "trait", "narrative": "Stable pattern.", field: "injected"}
    response = _request(
        app,
        "POST",
        "/v1/interviewer/evidence",
        body={
            "session_id": str(created.json["session_id"]),
            "session_token": str(created.json["session_token"]),
            "evidence": evidence,
        },
    )

    assert response.status_code == 422
    assert response.json["error"]["issues"][0]["location"][-1] == field
    assert sessions.appended == []


def test_lock_routes_apply_the_owner_pilot_quality_gate_and_redact_receipts(
    tmp_path: Path,
) -> None:
    sessions = FakeSessions()
    app = _app(tmp_path, sessions)
    created = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=_birth(),
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )
    session_id = str(created.json["session_id"])
    session_token = str(created.json["session_token"])

    generic = _request(
        app,
        "POST",
        f"/v1/participant-sessions/{session_id}/lock",
        headers={"x-astrohd-session-token": session_token},
    )
    interviewer = _request(
        app,
        "POST",
        "/v1/interviewer/lock",
        body={"session_id": session_id, "session_token": session_token},
    )

    assert generic.status_code == 200
    assert interviewer.status_code == 200
    assert sessions.lock_calls == [session_id, session_id]
    assert sessions.lock_quality_flags == [True, True]
    for response in (generic, interviewer):
        assert "scoring_responses" not in response.json
        assert "evidence_ids" not in response.json
        assert "cluster_id" not in response.text


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("mode", "self_discovery", "scientific_blind"),
        ("ranking_scope", "century_global", "known_birth_month"),
    ],
)
def test_owner_endpoint_rejects_wrong_mode_or_scope_without_consuming_invite(
    tmp_path: Path,
    field: str,
    value: str,
    message: str,
) -> None:
    app = _app(tmp_path, FakeSessions())
    body = _birth()
    body[field] = value
    response = _request(
        app,
        "POST",
        "/v1/participant-sessions",
        body=body,
        headers={
            "x-astrohd-pilot-token": "owner-code",
            "x-astrohd-storage-consent": "yes",
            "x-astrohd-openai-consent": "yes",
        },
    )

    assert response.status_code == 400
    assert message in response.json["error"]["message"]
    assert not (tmp_path / "invites").exists()


def test_action_openapi_has_no_cluster_id() -> None:
    schema = (
        PROJECT_ROOT / "reference/custom_gpt/participant_interviewer_action_openapi_v1.yaml"
    ).read_text(encoding="utf-8")
    assert "createParticipantSession" not in schema
    assert "BirthIntake" not in schema
    assert "X-AstroHD-Session-Token" not in schema
    assert "in: header" not in schema
    assert "{session_id}" not in schema
    assert schema.count("/v1/interviewer/") == 7
    assert schema.count("    post:") == 7
    assert "required: [session_id, session_token]" in schema
    assert "minimum_evidence_passed" in schema
    assert "consistency_status" in schema
    assert "quality_rationale" in schema
    assert "cluster_id" not in schema
    action_contract = yaml.safe_load(schema)
    components = action_contract["components"]["schemas"]
    progress_response = components["ProgressResponse"]
    next_question_response = components["NextQuestionResponse"]
    assert "mapped_scoreable_coverage" in progress_response["required"]
    assert progress_response["properties"]["mapped_scoreable_coverage"]["maximum"] == 1
    assert progress_response["properties"]["mapped_scoreable_coverage"]["description"] == (
        "Coverage of the frozen mapped questions by scoreable evidence."
    )
    assert "mapped_question_quality_gate_passed" in progress_response["required"]
    assert "completion_policy_status" not in progress_response["properties"]
    assert "cluster_id" not in components["EvidenceInput"]["properties"]
    assert set(progress_response["properties"]["phase"]["enum"]) == {
        phase.value for phase in SessionPhase
    }
    assert "minimum_evidence" in next_question_response["required"]
    assert next_question_response["properties"]["minimum_evidence"]["type"] == "string"

    instructions = (
        PROJECT_ROOT / "reference/custom_gpt/participant_interviewer_instructions_under_8000_v1.md"
    ).read_text()
    assert len(instructions.encode()) < 8000
    assert "I learned chess very quickly" in " ".join(instructions.split())
    assert "random, joke-like" in instructions
    assert "mapped_question_quality_gate_passed" in instructions
    assert "completion policy" not in instructions.lower()
    assert "Never send `cluster_id`" in instructions
    assert "writeOnly: true" in schema
    assert "#/components/parameters/" not in schema
    assert "schema: {type: object, additionalProperties: true}" not in schema
    assert "revealParticipantResult" in schema
    assert "finalizeParticipantExploratoryProfile" in schema

    generic_schema = (
        PROJECT_ROOT / "reference/custom_gpt/participant_action_openapi_v1.yaml"
    ).read_text(encoding="utf-8")
    generic_contract = yaml.safe_load(generic_schema)
    generic_evidence = generic_contract["components"]["schemas"]["EvidenceInput"]["properties"]
    assert "cluster_id" not in generic_evidence
    assert {
        "minimum_evidence_passed",
        "consistency_status",
        "quality_rationale",
    } <= set(generic_evidence)


def test_pr_and_state_prose_record_owner_correction_without_fake_policy() -> None:
    prose = "\n".join(
        (PROJECT_ROOT / relative).read_text(encoding="utf-8")
        for relative in (
            "CURRENT_PLAN.md",
            "state/CURRENT-STATE.md",
            "docs/36_astrohd_owner_pilot.md",
        )
    )

    assert "there was never a completion policy" in prose.lower()
    assert "OWNER-CORRECTION-2026-09-02.md" in prose
    assert "SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED" not in prose


def test_launch_factory_keeps_relationship_route_and_mounts_natal_first(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(PROJECT_ROOT)
    monkeypatch.setenv("HDMATCH_RELATIONSHIP_STORE", str(tmp_path / "relationship"))
    monkeypatch.setenv("HDMATCH_NATAL_PILOT_ENABLED", "1")
    natal = FastAPI()

    @natal.get("/")
    async def natal_home() -> str:
        return "natal"

    monkeypatch.setattr(
        relationship_launch_app,
        "create_natal_pilot_app_from_env",
        lambda: natal,
    )
    original_html = relationship_base_app._HTML
    try:
        app = relationship_launch_app.create_relationship_launch_app_from_env()
        routes = {route.path: route for route in app.routes}
        landing_html = cast(APIRoute, routes["/"]).endpoint()
        relationship_html = cast(APIRoute, routes["/relationship"]).endpoint()
        natal_mount = cast(Mount, routes["/astrohd"])
    finally:
        relationship_base_app._HTML = original_html

    assert "Start with one person" in landing_html
    assert "Seal prediction &amp; begin questionnaire" in relationship_html
    assert natal_mount.app is natal


def test_production_factory_verifies_real_pinned_cache_when_ephemeris_installed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not tuple((PROJECT_ROOT / "data/ephemeris").glob("*.se1")):
        pytest.skip("official Swiss Ephemeris files are not installed")
    monkeypatch.chdir(PROJECT_ROOT)
    monkeypatch.setenv("HDMATCH_REPO_ROOT", str(PROJECT_ROOT))
    monkeypatch.setenv(
        "HDMATCH_RELATIONSHIP_QUESTIONNAIRE",
        str(PROJECT_ROOT / "reference/relationship/relationship_dynamic_questionnaire_v1.json"),
    )
    monkeypatch.setenv(
        "HDMATCH_RELATIONSHIP_GUIDED_FIELDS",
        str(PROJECT_ROOT / "reference/relationship/relationship_guided_response_fields_v1.json"),
    )
    monkeypatch.setenv("HDMATCH_RELATIONSHIP_STORE", str(tmp_path / "relationship"))
    monkeypatch.setenv("HDMATCH_NATAL_PILOT_ENABLED", "1")
    monkeypatch.setenv(
        "HDMATCH_EPHEMERIS_PATH",
        str(PROJECT_ROOT / "data/ephemeris"),
    )
    monkeypatch.setenv(
        "HDMATCH_MAPPING_PATH",
        str(PROJECT_ROOT / "mappings/mapping_library_v1.json"),
    )
    monkeypatch.setenv(
        "HDMATCH_QUESTION_BANK_PATH",
        str(PROJECT_ROOT / "reference/core/question_bank_v1.json"),
    )
    monkeypatch.setenv("HDMATCH_PARTICIPANT_STORE", str(tmp_path / "natal"))
    engine_fingerprint = ExactChartAdapter(str(PROJECT_ROOT / "data/ephemeris")).fingerprint
    cache_root = tmp_path / "century"
    start = datetime(2000, 1, 1, tzinfo=UTC)
    chart_a = StructuralChartFeatures(
        type="Generator",
        strategy="Respond",
        authority="Sacral",
        profile="1/3",
        definition="Single",
        defined_centers=("Sacral",),
    )
    chart_b = chart_a.model_copy(update={"profile": "2/4"})
    manifest = write_verified_century_cache(
        cache_root,
        (
            GlobalCandidateState(
                state_id="TEST-A",
                start_utc=start,
                end_utc=start + timedelta(hours=12),
                chart_features_hash=structural_features_sha256(chart_a),
                chart_features=chart_a,
            ),
            GlobalCandidateState(
                state_id="TEST-B",
                start_utc=start + timedelta(hours=12),
                end_utc=start + timedelta(days=1),
                chart_features_hash=structural_features_sha256(chart_b),
                chart_features=chart_b,
            ),
        ),
        engine_fingerprint=engine_fingerprint,
        generation_commit="test",
        created_at_utc=datetime(2026, 8, 31, tzinfo=UTC),
    )
    monkeypatch.setenv("HDMATCH_CENTURY_CACHE", str(cache_root))
    monkeypatch.setenv(
        "HDMATCH_CENTURY_MANIFEST_SHA256",
        hashlib.sha256((cache_root / "manifest.json").read_bytes()).hexdigest(),
    )
    monkeypatch.setenv(
        "HDMATCH_CENTURY_CANONICAL_ROWS_SHA256",
        manifest.canonical_rows_sha256,
    )
    monkeypatch.setenv(
        "HDMATCH_NATAL_PILOT_TOKEN_SHA256",
        hashlib.sha256(b"owner-code").hexdigest(),
    )
    monkeypatch.setenv("HDMATCH_PUBLIC_BASE_URL", "https://example.test")
    monkeypatch.setenv("HDMATCH_CODE_COMMIT", "a" * 40)
    original_html = relationship_base_app._HTML
    try:
        app = relationship_launch_app.create_relationship_launch_app_from_env()
        routes = {route.path: route for route in app.routes}
        root_route = cast(APIRoute, routes["/"])
        relationship_route = cast(APIRoute, routes["/relationship"])
        natal_mount = cast(Mount, routes["/astrohd"])
        natal_routes = {route.path: route for route in natal_mount.app.routes}
        natal_home = cast(APIRoute, natal_routes["/"])
        natal_health_route = cast(APIRoute, natal_routes["/healthz"])

        landing_html = root_route.endpoint()
        relationship_html = relationship_route.endpoint()
        natal_html = asyncio.run(natal_home.endpoint())
        natal_health = asyncio.run(natal_health_route.endpoint())
    finally:
        relationship_base_app._HTML = original_html

    assert "Start with one person" in landing_html
    assert "Seal prediction &amp; begin questionnaire" in relationship_html
    assert "first real blinded test of astrology and Human Design" in natal_html
    assert natal_health["status"] == "ok"
    assert natal_health["ranking_scope"] == "known_birth_month"
    assert natal_health["month_universe_source"] == "pinned_verified_century_cache_slice"
