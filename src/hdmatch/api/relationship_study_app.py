"""Full relationship-study preflight layered on the live OpenAI questionnaire app.

The existing pilot routes remain available for development sessions. New confirmatory
study sessions enter through ``/api/study/intake`` and are behavior-locked until the
pre-answer prediction freeze is genuinely complete.
"""

from __future__ import annotations

import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from hdmatch.api.relationship_openai_app import create_relationship_openai_app_from_env
from hdmatch.api.relationship_public_app import RelationshipFileStore
from hdmatch.relationship.study import (
    RelationshipPredictionFreeze,
    RelationshipStudyIntake,
    bind_noise_policy,
    public_preflight,
)
from hdmatch.relationship.study_prediction import build_prediction_freeze


class StudyIntakeRequest(BaseModel):
    intake: RelationshipStudyIntake
    consent_to_llm_processing: bool


class StudyTokenRequest(BaseModel):
    token: str


def create_relationship_study_app_from_env() -> FastAPI:
    app = create_relationship_openai_app_from_env()
    app.title = "Relationship Pattern Lab"
    app.version = "0.6.0"

    store_value = os.environ.get("HDMATCH_RELATIONSHIP_STORE", "").strip()
    if not store_value:
        raise RuntimeError("HDMATCH_RELATIONSHIP_STORE is required")
    store = RelationshipFileStore(Path(store_value))
    repo_root = Path(os.environ.get("HDMATCH_REPO_ROOT", "/app"))
    questionnaire_path = Path(
        os.environ.get(
            "HDMATCH_RELATIONSHIP_QUESTIONNAIRE",
            "reference/relationship/relationship_dynamic_questionnaire_v1.json",
        )
    )
    noise_value = os.environ.get("HDMATCH_SURVEY_NOISE_POLICY", "").strip()
    default_noise = repo_root / "state/SURVEY-V2-NOISE-AUDIT.json"
    noise_path = Path(noise_value) if noise_value else default_noise

    @app.middleware("http")
    async def confirmatory_preanswer_guard(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        session_match = re.fullmatch(r"/api/sessions/([^/]+)/answers(?:/[^/]+)?", request.url.path)
        quality = request.url.path == "/api/quality"
        if request.method in {"POST", "PUT"} and (session_match or quality):
            body: dict[str, Any] | None = None
            try:
                body = cast(dict[str, Any], await request.json())
            except (json.JSONDecodeError, TypeError, ValueError):
                body = None
            if body:
                session_id = (
                    session_match.group(1)
                    if session_match is not None
                    else str(body.get("session_id", ""))
                )
                token = str(body.get("token", ""))
                if session_id and token:
                    try:
                        payload = store.read(session_id, token)
                    except HTTPException:
                        payload = None
                    if payload and payload.get("study_schema_version") == "relationship-study-v1":
                        freeze_raw = payload.get("prediction_freeze")
                        if not isinstance(freeze_raw, dict):
                            return JSONResponse(
                                status_code=409,
                                content={"detail": "pre-answer prediction freeze is missing"},
                            )
                        freeze = RelationshipPredictionFreeze.model_validate(freeze_raw)
                        if not freeze.confirmatory_ready:
                            return JSONResponse(
                                status_code=409,
                                content={
                                    "detail": (
                                        "confirmatory survey is locked until all required "
                                        "prediction layers are computed and frozen"
                                    )
                                },
                            )
            # Starlette needs a replayable body after middleware consumes request.json().
            if body is not None:
                encoded = json.dumps(body).encode()

                async def receive() -> dict[str, Any]:
                    return {"type": "http.request", "body": encoded, "more_body": False}

                request = Request(request.scope, receive)
        return await call_next(request)

    @app.post("/api/study/intake")
    def create_study_intake(request: StudyIntakeRequest) -> dict[str, Any]:
        if not request.consent_to_llm_processing:
            raise HTTPException(status_code=400, detail="LLM-processing consent is required")
        payload, token = store.create()
        payload["format_version"] = "guided-fields-v2"
        payload["study_schema_version"] = "relationship-study-v1"
        payload["study_intake"] = request.intake.model_dump(mode="json")
        payload["contact_email_lookup_sha256"] = request.intake.contact_email_lookup_sha256
        payload["email_verification_status"] = "not_configured"
        payload["llm_processing_consent_at"] = datetime.now(UTC).isoformat()
        noise_policy = bind_noise_policy(noise_path if noise_path.exists() else None)
        freeze = build_prediction_freeze(
            session_id=str(payload["session_id"]),
            intake=request.intake,
            repo_root=repo_root,
            questionnaire_path=questionnaire_path,
            noise_policy=noise_policy,
            code_commit=(
                os.environ.get("RAILWAY_GIT_COMMIT_SHA")
                or os.environ.get("HDMATCH_CODE_COMMIT")
                or "runtime_commit_unbound"
            ),
        )
        payload["prediction_freeze"] = freeze.model_dump(mode="json")
        payload["prediction_freeze_sha256"] = freeze.freeze_sha256
        payload["behavior_capture_unlocked"] = freeze.confirmatory_ready
        store.save(payload)
        preflight = public_preflight(
            session_id=str(payload["session_id"]),
            intake=request.intake,
            prediction_freeze=freeze,
        )
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "preflight": preflight.model_dump(mode="json"),
            "participant_message": _participant_preflight_message(preflight.confirmatory_ready),
        }

    @app.get("/api/study/sessions/{session_id}/preflight")
    def get_study_preflight(session_id: str, token: str) -> dict[str, Any]:
        payload = store.read(session_id, token)
        intake_raw = payload.get("study_intake")
        if not isinstance(intake_raw, dict):
            raise HTTPException(status_code=404, detail="study intake not found")
        intake = RelationshipStudyIntake.model_validate(intake_raw)
        freeze_raw = payload.get("prediction_freeze")
        freeze = (
            RelationshipPredictionFreeze.model_validate(freeze_raw)
            if isinstance(freeze_raw, dict)
            else None
        )
        return public_preflight(
            session_id=session_id,
            intake=intake,
            prediction_freeze=freeze,
            email_verification_status=cast(
                Any, payload.get("email_verification_status", "not_configured")
            ),
        ).model_dump(mode="json")

    @app.post("/api/study/sessions/{session_id}/refresh-prediction-freeze")
    def refresh_prediction_freeze(
        session_id: str,
        request: StudyTokenRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload.get("answers"):
            raise HTTPException(
                status_code=409,
                detail="prediction freeze cannot be regenerated after behavioral answers exist",
            )
        intake_raw = payload.get("study_intake")
        if not isinstance(intake_raw, dict):
            raise HTTPException(status_code=404, detail="study intake not found")
        intake = RelationshipStudyIntake.model_validate(intake_raw)
        noise_policy = bind_noise_policy(noise_path if noise_path.exists() else None)
        freeze = build_prediction_freeze(
            session_id=session_id,
            intake=intake,
            repo_root=repo_root,
            questionnaire_path=questionnaire_path,
            noise_policy=noise_policy,
            code_commit=(
                os.environ.get("RAILWAY_GIT_COMMIT_SHA")
                or os.environ.get("HDMATCH_CODE_COMMIT")
                or "runtime_commit_unbound"
            ),
        )
        payload["prediction_freeze"] = freeze.model_dump(mode="json")
        payload["prediction_freeze_sha256"] = freeze.freeze_sha256
        payload["behavior_capture_unlocked"] = freeze.confirmatory_ready
        store.save(payload)
        preflight = public_preflight(
            session_id=session_id,
            intake=intake,
            prediction_freeze=freeze,
        )
        return {
            "preflight": preflight.model_dump(mode="json"),
            "participant_message": _participant_preflight_message(preflight.confirmatory_ready),
        }

    return app


def _participant_preflight_message(confirmatory_ready: bool) -> str:
    if confirmatory_ready:
        return (
            "Your birth data and hidden pre-answer predictions are sealed. You can begin "
            "the blind relationship questionnaire; you do not need to save the SHA receipt."
        )
    return (
        "Your private intake is saved, but the confirmatory questionnaire is not unlocked "
        "because at least one required prediction layer is not yet computable. The SHA "
        "receipt is research provenance; participants are not expected to manage it."
    )
