"""Adaptive chart-blind relationship capture service.

This layer adds single-construct v2 fields, live answer-usability feedback,
bounded semantic clarification, visible progress, and targeted legacy addenda.
It receives no birth data, charts, candidate identities, or Astro/HD predictions.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

import hdmatch.api.relationship_public_app as base_app
from hdmatch.api.relationship_adaptive_ui import HTML as ADAPTIVE_HTML
from hdmatch.api.relationship_public_app import (
    CreateSessionRequest,
    FreezeRequest,
    GuidedRegistry,
    RelationshipFileStore,
    _legacy_session,
    _load_guided_registry,
    _next_question,
    _public_question,
)
from hdmatch.relationship.answer_audit import (
    AUDIT_VERSION,
    ClarificationItem,
    FieldEvidence,
    FieldStatus,
    assess_field_answer,
    build_clarification_queue,
    legacy_clarification_queue,
)
from hdmatch.relationship.questionnaire import (
    RelationshipQuestionnaireSpec,
    load_relationship_questionnaire,
)

MAX_CLARIFICATIONS = 6
MAX_LEGACY_CLARIFICATIONS = 8


class QualityRequest(BaseModel):
    field_id: str = Field(min_length=1)
    status: FieldStatus
    answer: str = Field(default="", max_length=12000)
    clarification: str = Field(default="", max_length=12000)


class ClarificationAnswerRequest(BaseModel):
    token: str = Field(min_length=16)
    clarification_id: str = Field(min_length=1)
    status: Literal["answered", "unknown"]
    answer: str = Field(default="", max_length=12000)


def _field_prompts(registry: GuidedRegistry) -> dict[str, str]:
    return {
        field.id: field.label
        for question in registry.questions.values()
        for field in question.fields
    }


def _field_question_map(registry: GuidedRegistry) -> dict[str, tuple[str, str]]:
    return {
        field.id: (question_id, field.label)
        for question_id, question in registry.questions.items()
        for field in question.fields
    }


def _answers(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], payload.get("answers", []))


def _flatten_evidence(answers: list[dict[str, Any]]) -> tuple[FieldEvidence, ...]:
    evidence: list[FieldEvidence] = []
    for record in answers:
        question_id = str(record["question_id"])
        for raw in cast(list[dict[str, Any]], record.get("fields", [])):
            evidence.append(
                FieldEvidence(
                    question_id=question_id,
                    field_id=str(raw["field_id"]),
                    status=cast(FieldStatus, str(raw["status"])),
                    answer=str(raw.get("answer", "")),
                    clarification=str(raw.get("clarification", "")),
                )
            )
    return tuple(evidence)


def _audit_answers(audit: dict[str, Any]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], audit.setdefault("answers", []))


def _audit_queue(audit: dict[str, Any]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], audit.get("queue", []))


def _audit_answered_ids(audit: dict[str, Any]) -> set[str]:
    return {str(row["clarification_id"]) for row in _audit_answers(audit)}


def _next_audit_item(audit: dict[str, Any]) -> ClarificationItem | None:
    answered = _audit_answered_ids(audit)
    for raw in _audit_queue(audit):
        item = ClarificationItem.model_validate(raw)
        if item.id not in answered:
            return item
    return None


def _audit_progress(audit: dict[str, Any], *, cap: int) -> dict[str, Any]:
    total = len(_audit_queue(audit))
    completed = len(_audit_answers(audit))
    percent = 100 if total == 0 else 85 + round(15 * completed / total)
    return {
        "percent": min(percent, 100),
        "label": (
            "Core complete · no extra clarification needed"
            if total == 0
            else f"Clarification {min(completed + 1, total)} of {total} · hard cap {cap}"
        ),
        "clarifications_completed": completed,
        "clarifications_total": total,
        "clarification_cap": cap,
    }


def _public_audit_state(audit: dict[str, Any], *, cap: int) -> dict[str, Any]:
    item = _next_audit_item(audit)
    return {
        "complete": item is None,
        "next_clarification": item.model_dump() if item else None,
        "answers": _audit_answers(audit),
        "field_quality": audit.get("field_quality", []),
        "progress": _audit_progress(audit, cap=cap),
        "audit_version": audit.get("audit_version", AUDIT_VERSION),
    }


def _build_core_audit(payload: dict[str, Any], registry: GuidedRegistry) -> dict[str, Any]:
    evidence = _flatten_evidence(_answers(payload))
    queue = build_clarification_queue(
        evidence,
        field_prompts=_field_prompts(registry),
        max_items=MAX_CLARIFICATIONS,
    )
    field_quality = [
        {
            "question_id": row.question_id,
            "field_id": row.field_id,
            **assess_field_answer(
                row.field_id,
                row.status,
                row.answer,
                row.clarification,
            ).model_dump(),
        }
        for row in evidence
    ]
    return {
        "mode": "core_v2",
        "audit_version": AUDIT_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "queue": [item.model_dump() for item in queue],
        "answers": [],
        "field_quality": field_quality,
    }


def _core_complete(payload: dict[str, Any], spec: RelationshipQuestionnaireSpec) -> bool:
    answered = {str(row["question_id"]) for row in _answers(payload)}
    return set(spec.core_question_ids).issubset(answered)


def _content_digest(payload: dict[str, Any], audit: dict[str, Any]) -> str:
    frozen = {
        "session_id": payload["session_id"],
        "format_version": payload.get("format_version"),
        "answers": _answers(payload),
        "semantic_audit": {
            "audit_version": audit.get("audit_version", AUDIT_VERSION),
            "queue": _audit_queue(audit),
            "answers": _audit_answers(audit),
            "field_quality": audit.get("field_quality", []),
        },
    }
    encoded = json.dumps(frozen, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def _addendum_digest(addendum: dict[str, Any]) -> str:
    frozen = {
        "parent_freeze_sha256": addendum["parent_freeze_sha256"],
        "audit_version": addendum["audit_version"],
        "queue": _audit_queue(addendum),
        "answers": _audit_answers(addendum),
    }
    encoded = json.dumps(frozen, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def create_relationship_adaptive_app_from_env() -> FastAPI:
    """Build the deployable adaptive relationship app from environment settings."""
    os.environ.setdefault(
        "HDMATCH_RELATIONSHIP_GUIDED_FIELDS",
        "reference/relationship/relationship_guided_response_fields_v2.json",
    )
    questionnaire_path = Path(
        os.environ.get(
            "HDMATCH_RELATIONSHIP_QUESTIONNAIRE",
            "reference/relationship/relationship_dynamic_questionnaire_v1.json",
        )
    )
    guided_path = Path(os.environ["HDMATCH_RELATIONSHIP_GUIDED_FIELDS"])
    store_value = os.environ.get("HDMATCH_RELATIONSHIP_STORE", "").strip()
    if not store_value:
        raise RuntimeError(
            "HDMATCH_RELATIONSHIP_STORE is required; point it at a private persistent volume"
        )

    spec = load_relationship_questionnaire(questionnaire_path)
    registry = _load_guided_registry(guided_path, spec)
    store = RelationshipFileStore(Path(store_value))

    base_app._HTML = ADAPTIVE_HTML
    app = base_app.create_relationship_public_app_from_env()
    app.title = "Relationship X-Ray Adaptive Pilot"
    app.version = "0.3.0"

    @app.middleware("http")
    async def adaptive_integrity_guard(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        base_freeze = re.fullmatch(r"/api/sessions/([^/]+)/freeze", request.url.path)
        edit_match = re.fullmatch(r"/api/sessions/([^/]+)/answers/([^/]+)", request.url.path)
        token: str | None = None
        if request.method in {"POST", "PUT"} and (base_freeze or edit_match):
            try:
                body_obj = cast(dict[str, Any], await request.json())
                token = str(body_obj.get("token", ""))
            except (json.JSONDecodeError, TypeError, ValueError):
                token = None

        if base_freeze and request.method == "POST" and token:
            payload = store.read(base_freeze.group(1), token)
            if payload.get("format_version") == "guided-fields-v2":
                return JSONResponse(
                    status_code=409,
                    content={"detail": "use adaptive freeze so clarifications are sealed too"},
                )

        response = await call_next(request)
        if edit_match and request.method == "PUT" and token and response.status_code < 300:
            payload = store.read(edit_match.group(1), token)
            if payload.get("format_version") == "guided-fields-v2":
                payload["semantic_audit"] = None
                payload["semantic_audit_invalidated_at"] = datetime.now(UTC).isoformat()
                store.save(payload)
        return response

    @app.post("/api/adaptive/sessions")
    def create_adaptive_session(request: CreateSessionRequest) -> dict[str, Any]:
        if not request.consent_to_store_responses:
            raise HTTPException(status_code=400, detail="consent is required")
        payload, token = store.create()
        payload["format_version"] = "guided-fields-v2"
        payload["semantic_audit_version"] = AUDIT_VERSION
        payload["semantic_audit"] = None
        store.save(payload)
        question = _next_question(spec, _answers(payload))
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "next_question": _public_question(question, registry) if question else None,
            "progress": {
                "percent": 0,
                "label": (
                    f"Core section 1 of 6 · at most {MAX_CLARIFICATIONS} "
                    "clarifications afterward"
                ),
            },
        }

    @app.post("/api/quality")
    def quality(request: QualityRequest) -> dict[str, Any]:
        return assess_field_answer(
            request.field_id,
            request.status,
            request.answer,
            request.clarification,
        ).model_dump()

    @app.post("/api/sessions/{session_id}/semantic-audit")
    def semantic_audit(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        if payload.get("format_version") != "guided-fields-v2":
            raise HTTPException(status_code=409, detail="semantic audit requires v2 fields")
        if not _core_complete(payload, spec):
            raise HTTPException(status_code=409, detail="complete all six core sections first")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict):
            audit = _build_core_audit(payload, registry)
            payload["semantic_audit"] = audit
            store.save(payload)
        return _public_audit_state(audit, cap=MAX_CLARIFICATIONS)

    @app.post("/api/sessions/{session_id}/semantic-audit/answers")
    def submit_semantic_clarification(
        session_id: str,
        request: ClarificationAnswerRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict):
            raise HTTPException(status_code=409, detail="semantic audit has not been generated")
        expected = _next_audit_item(audit)
        if expected is None:
            raise HTTPException(status_code=409, detail="no clarification is pending")
        if request.clarification_id != expected.id:
            raise HTTPException(status_code=409, detail="answer does not match pending clarification")
        answer = request.answer.strip()
        if request.status == "answered" and not answer:
            raise HTTPException(status_code=422, detail="write a clarification or mark it unknown")
        _audit_answers(audit).append(
            {
                "clarification_id": expected.id,
                "source_question_id": expected.source_question_id,
                "source_field_id": expected.source_field_id,
                "reason_code": expected.reason_code,
                "status": request.status,
                "answer": answer,
                "answered_at": datetime.now(UTC).isoformat(),
            }
        )
        store.save(payload)
        return _public_audit_state(audit, cap=MAX_CLARIFICATIONS)

    @app.post("/api/adaptive/sessions/{session_id}/freeze")
    def freeze_adaptive(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] == "frozen":
            return {"status": "frozen", "freeze_sha256": payload["freeze_sha256"]}
        if payload.get("format_version") != "guided-fields-v2":
            raise HTTPException(status_code=409, detail="adaptive freeze requires v2 session")
        if not _core_complete(payload, spec):
            raise HTTPException(status_code=409, detail="complete all six core sections first")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict):
            raise HTTPException(status_code=409, detail="run chart-blind audit before freezing")
        if _next_audit_item(audit) is not None:
            raise HTTPException(status_code=409, detail="complete targeted clarifications first")
        payload["status"] = "frozen"
        payload["freeze_sha256"] = _content_digest(payload, audit)
        payload["frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {"status": "frozen", "freeze_sha256": payload["freeze_sha256"]}

    @app.post("/api/sessions/{session_id}/legacy-targeted-audit")
    def start_legacy_targeted_audit(
        session_id: str,
        request: FreezeRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "frozen" or not _legacy_session(payload):
            raise HTTPException(
                status_code=409,
                detail="targeted clarification is only for frozen legacy-format sessions",
            )
        addendum = payload.get("semantic_legacy_addendum")
        if not isinstance(addendum, dict):
            broad = {
                str(row["question_id"]): str(row.get("answer", ""))
                for row in _answers(payload)
            }
            queue = legacy_clarification_queue(
                broad,
                field_questions=_field_question_map(registry),
                max_items=MAX_LEGACY_CLARIFICATIONS,
            )
            addendum = {
                "mode": "legacy_targeted_v2",
                "audit_version": AUDIT_VERSION,
                "status": "in_progress",
                "parent_freeze_sha256": payload["freeze_sha256"],
                "generated_at": datetime.now(UTC).isoformat(),
                "queue": [item.model_dump() for item in queue],
                "answers": [],
                "freeze_sha256": None,
            }
            payload["semantic_legacy_addendum"] = addendum
            store.save(payload)
        state = _public_audit_state(addendum, cap=MAX_LEGACY_CLARIFICATIONS)
        state["status"] = addendum["status"]
        state["freeze_sha256"] = addendum.get("freeze_sha256")
        return state

    @app.post("/api/sessions/{session_id}/legacy-targeted-audit/answers")
    def submit_legacy_targeted_audit(
        session_id: str,
        request: ClarificationAnswerRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("semantic_legacy_addendum")
        if not isinstance(addendum, dict) or addendum.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="targeted clarification is not active")
        expected = _next_audit_item(addendum)
        if expected is None:
            raise HTTPException(status_code=409, detail="no targeted clarification is pending")
        if request.clarification_id != expected.id:
            raise HTTPException(status_code=409, detail="answer does not match pending clarification")
        answer = request.answer.strip()
        if request.status == "answered" and not answer:
            raise HTTPException(status_code=422, detail="write a clarification or mark it unknown")
        _audit_answers(addendum).append(
            {
                "clarification_id": expected.id,
                "source_question_id": expected.source_question_id,
                "source_field_id": expected.source_field_id,
                "reason_code": expected.reason_code,
                "status": request.status,
                "answer": answer,
                "answered_at": datetime.now(UTC).isoformat(),
            }
        )
        store.save(payload)
        state = _public_audit_state(addendum, cap=MAX_LEGACY_CLARIFICATIONS)
        state["status"] = addendum["status"]
        return state

    @app.post("/api/sessions/{session_id}/legacy-targeted-audit/freeze")
    def freeze_legacy_targeted_audit(
        session_id: str,
        request: FreezeRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("semantic_legacy_addendum")
        if not isinstance(addendum, dict):
            raise HTTPException(status_code=409, detail="no targeted clarification addendum")
        if addendum.get("status") == "frozen":
            return {"status": "frozen", "freeze_sha256": addendum["freeze_sha256"]}
        if _next_audit_item(addendum) is not None:
            raise HTTPException(status_code=409, detail="complete targeted clarifications first")
        addendum["status"] = "frozen"
        addendum["freeze_sha256"] = _addendum_digest(addendum)
        addendum["frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {"status": "frozen", "freeze_sha256": addendum["freeze_sha256"]}

    return app
