"""Adaptive chart-blind relationship capture service with LLM answer auditing.

Participant answers are stored privately and may be sent to a configured LLM only
after explicit LLM-processing consent. The LLM receives questionnaire semantics and
responses only: never birth data, charts, candidate identities, AstroRRF predictions,
or model fit.
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
    FreezeRequest,
    GuidedField,
    GuidedRegistry,
    RelationshipFileStore,
    _load_guided_registry,
    _next_question,
    _public_question,
)
from hdmatch.relationship.llm_audit import (
    LLM_AUDIT_VERSION,
    FieldAuditInput,
    FieldStatus,
    LLMAuditProviderError,
    LLMAuditUnavailableError,
    LLMClarificationItem,
    LLMSessionAuditResult,
    OpenRouterRelationshipAuditor,
)
from hdmatch.relationship.questionnaire import (
    RelationshipQuestionnaireSpec,
    load_relationship_questionnaire,
)

MAX_CLARIFICATIONS = 6
MAX_POST_FREEZE_CLARIFICATIONS = 8


class AdaptiveCreateSessionRequest(BaseModel):
    consent_to_store_responses: bool
    consent_to_llm_processing: bool


class QualityRequest(BaseModel):
    session_id: str = Field(min_length=1)
    token: str = Field(min_length=16)
    field_id: str = Field(min_length=1)
    status: FieldStatus
    answer: str = Field(default="", max_length=12000)
    clarification: str = Field(default="", max_length=12000)


class ClarificationAnswerRequest(BaseModel):
    token: str = Field(min_length=16)
    clarification_id: str = Field(min_length=1)
    status: Literal["answered", "unknown"]
    answer: str = Field(default="", max_length=12000)


class LLMAddendumStartRequest(BaseModel):
    token: str = Field(min_length=16)
    consent_to_llm_processing: bool


def _answers(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], payload.get("answers", []))


def _audit_answers(audit: dict[str, Any]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], audit.setdefault("answers", []))


def _audit_queue(audit: dict[str, Any]) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], audit.get("queue", []))


def _audit_answered_ids(audit: dict[str, Any]) -> set[str]:
    return {str(row["clarification_id"]) for row in _audit_answers(audit)}


def _next_audit_item(audit: dict[str, Any]) -> LLMClarificationItem | None:
    answered = _audit_answered_ids(audit)
    for raw in _audit_queue(audit):
        item = LLMClarificationItem.model_validate(raw)
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
            "Core complete · LLM found no extra clarification needed"
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
        "audit_version": audit.get("audit_version", LLM_AUDIT_VERSION),
        "provider_receipt": audit.get("provider_receipt"),
        "status": audit.get("status", "in_progress"),
        "freeze_sha256": audit.get("freeze_sha256"),
    }


def _core_complete(payload: dict[str, Any], spec: RelationshipQuestionnaireSpec) -> bool:
    answered = {str(row["question_id"]) for row in _answers(payload)}
    return set(spec.core_question_ids).issubset(answered)


def _field_definition(
    registry: GuidedRegistry,
    question_id: str,
    field_id: str,
) -> tuple[str, GuidedField]:
    question = registry.questions.get(question_id)
    if question is None:
        raise HTTPException(status_code=422, detail="unknown questionnaire section")
    for field in question.fields:
        if field.id == field_id:
            return question.title, field
    raise HTTPException(status_code=422, detail="unknown questionnaire field")


def _field_inputs(payload: dict[str, Any], registry: GuidedRegistry) -> tuple[FieldAuditInput, ...]:
    fields: list[FieldAuditInput] = []
    for record in _answers(payload):
        question_id = str(record.get("question_id", ""))
        raw_fields = cast(list[dict[str, Any]], record.get("fields", []))
        if not raw_fields:
            continue
        for raw in raw_fields:
            field_id = str(raw.get("field_id", ""))
            title, definition = _field_definition(registry, question_id, field_id)
            fields.append(
                FieldAuditInput(
                    question_id=question_id,
                    question_title=title,
                    field_id=field_id,
                    field_label=definition.label,
                    field_hint=definition.placeholder,
                    status=cast(FieldStatus, str(raw.get("status", "unknown"))),
                    answer=str(raw.get("answer", "")),
                    clarification=str(raw.get("clarification", "")),
                )
            )
    return tuple(fields)


def _field_input_by_id(
    payload: dict[str, Any],
    registry: GuidedRegistry,
    field_id: str,
    *,
    status: FieldStatus,
    answer: str,
    clarification: str,
) -> FieldAuditInput:
    for question_id, question in registry.questions.items():
        for definition in question.fields:
            if definition.id == field_id:
                return FieldAuditInput(
                    question_id=question_id,
                    question_title=question.title,
                    field_id=field_id,
                    field_label=definition.label,
                    field_hint=definition.placeholder,
                    status=status,
                    answer=answer,
                    clarification=clarification,
                )
    raise HTTPException(status_code=422, detail="unknown questionnaire field")


def _source_excerpt(field: FieldAuditInput) -> str:
    pieces = [part.strip() for part in (field.answer, field.clarification) if part.strip()]
    if not pieces:
        return f"[{field.status}]"
    text = " | ".join(pieces)
    return text if len(text) <= 700 else text[:697] + "..."


def _prior_clarifications(payload: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    old = payload.get("semantic_audit")
    if not isinstance(old, dict):
        return ()
    queue_lookup = {
        str(row.get("id", "")): row for row in cast(list[dict[str, Any]], old.get("queue", []))
    }
    result: list[dict[str, Any]] = []
    for answer in cast(list[dict[str, Any]], old.get("answers", [])):
        clarification_id = str(answer.get("clarification_id", ""))
        source = queue_lookup.get(clarification_id, {})
        result.append(
            {
                "source_field_id": source.get("source_field_id"),
                "old_prompt": source.get("prompt"),
                "status": answer.get("status"),
                "answer": answer.get("answer"),
            }
        )
    return tuple(result)


def _build_llm_audit(
    payload: dict[str, Any],
    registry: GuidedRegistry,
    auditor: OpenRouterRelationshipAuditor,
    *,
    max_clarifications: int,
    mode: str,
    include_prior_clarifications: bool = False,
) -> dict[str, Any]:
    fields = _field_inputs(payload, registry)
    if not fields:
        raise HTTPException(
            status_code=409,
            detail="this frozen session predates structured fields and cannot use this addendum path",
        )
    try:
        result = auditor.audit_session(
            fields,
            max_clarifications=max_clarifications,
            prior_clarifications=(
                _prior_clarifications(payload) if include_prior_clarifications else ()
            ),
        )
    except LLMAuditUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LLMAuditProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail="The LLM answer auditor failed. Your saved answers were not changed; try again.",
        ) from exc
    return _enrich_llm_result(fields, result, mode=mode)


def _enrich_llm_result(
    fields: tuple[FieldAuditInput, ...],
    result: LLMSessionAuditResult,
    *,
    mode: str,
) -> dict[str, Any]:
    lookup = {(field.question_id, field.field_id): field for field in fields}
    queue: list[dict[str, Any]] = []
    for draft in sorted(result.audit.clarifications, key=lambda row: row.priority):
        source = lookup[(draft.source_question_id, draft.source_field_id)]
        digest = hashlib.sha256(
            (
                f"{LLM_AUDIT_VERSION}|{draft.source_question_id}|{draft.source_field_id}|"
                f"{draft.reason}|{draft.prompt}"
            ).encode("utf-8")
        ).hexdigest()[:16]
        queue.append(
            LLMClarificationItem(
                id=f"RLLM-{digest}",
                source_question_id=draft.source_question_id,
                source_field_id=draft.source_field_id,
                source_label=source.field_label,
                source_answer_excerpt=_source_excerpt(source),
                reason=draft.reason,
                prompt=draft.prompt,
                priority=draft.priority,
            ).model_dump()
        )
    return {
        "mode": mode,
        "audit_version": LLM_AUDIT_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "provider_receipt": result.receipt.model_dump(),
        "queue": queue,
        "answers": [],
        "field_quality": [row.model_dump() for row in result.audit.field_quality],
    }


def _content_digest(payload: dict[str, Any], audit: dict[str, Any]) -> str:
    frozen = {
        "session_id": payload["session_id"],
        "format_version": payload.get("format_version"),
        "answers": _answers(payload),
        "semantic_audit": {
            "audit_version": audit.get("audit_version"),
            "provider_receipt": audit.get("provider_receipt"),
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
        "provider_receipt": addendum.get("provider_receipt"),
        "queue": _audit_queue(addendum),
        "answers": _audit_answers(addendum),
        "field_quality": addendum.get("field_quality", []),
    }
    encoded = json.dumps(frozen, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def _uses_llm_audit(payload: dict[str, Any]) -> bool:
    audit = payload.get("semantic_audit")
    return isinstance(audit, dict) and audit.get("audit_version") == LLM_AUDIT_VERSION


def _can_llm_addendum(payload: dict[str, Any], registry: GuidedRegistry) -> bool:
    if payload.get("status") != "frozen" or _uses_llm_audit(payload):
        return False
    try:
        return bool(_field_inputs(payload, registry))
    except HTTPException:
        return False


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
    auditor = OpenRouterRelationshipAuditor.from_env()

    base_app._HTML = ADAPTIVE_HTML
    app = base_app.create_relationship_public_app_from_env()
    app.title = "Relationship X-Ray LLM Pilot"
    app.version = "0.4.0"

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
                    content={"detail": "use adaptive freeze so LLM clarifications are sealed too"},
                )

        response = await call_next(request)
        if edit_match and request.method == "PUT" and token and response.status_code < 300:
            payload = store.read(edit_match.group(1), token)
            if payload.get("format_version") == "guided-fields-v2":
                payload["semantic_audit"] = None
                payload["semantic_audit_invalidated_at"] = datetime.now(UTC).isoformat()
                store.save(payload)
        return response

    @app.get("/api/llm-status")
    def llm_status() -> dict[str, Any]:
        return auditor.public_configuration()

    @app.post("/api/adaptive/sessions")
    def create_adaptive_session(request: AdaptiveCreateSessionRequest) -> dict[str, Any]:
        if not request.consent_to_store_responses:
            raise HTTPException(status_code=400, detail="storage consent is required")
        if not request.consent_to_llm_processing:
            raise HTTPException(status_code=400, detail="LLM-processing consent is required")
        if not auditor.available:
            raise HTTPException(
                status_code=503,
                detail="The LLM auditor is not configured yet; the survey is temporarily unavailable.",
            )
        payload, token = store.create()
        payload["format_version"] = "guided-fields-v2"
        payload["semantic_audit_version"] = LLM_AUDIT_VERSION
        payload["semantic_audit"] = None
        payload["llm_processing_consent_at"] = datetime.now(UTC).isoformat()
        payload["llm_provider"] = auditor.public_configuration()
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
                    "LLM clarifications afterward"
                ),
            },
        }

    @app.get("/api/adaptive/sessions/{session_id}")
    def adaptive_session_state(session_id: str, token: str) -> dict[str, Any]:
        payload = store.read(session_id, token)
        question = None
        if payload.get("status") == "in_progress":
            question = _next_question(spec, _answers(payload))
        audit = payload.get("semantic_audit")
        addendum = payload.get("llm_addendum")
        return {
            "session_id": session_id,
            "status": payload.get("status"),
            "answers": _answers(payload),
            "next_question": _public_question(question, registry) if question else None,
            "freeze_sha256": payload.get("freeze_sha256"),
            "semantic_audit": (
                _public_audit_state(audit, cap=MAX_CLARIFICATIONS)
                if isinstance(audit, dict) and audit.get("audit_version") == LLM_AUDIT_VERSION
                else None
            ),
            "llm_addendum": (
                _public_audit_state(addendum, cap=MAX_POST_FREEZE_CLARIFICATIONS)
                if isinstance(addendum, dict)
                else None
            ),
            "llm": auditor.public_configuration(),
            "can_start_llm_addendum": (
                auditor.available
                and _can_llm_addendum(payload, registry)
                and not isinstance(addendum, dict)
            ),
        }

    @app.post("/api/quality")
    def quality(request: QualityRequest) -> dict[str, Any]:
        payload = store.read(request.session_id, request.token)
        if payload.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="session is not editable")
        if not payload.get("llm_processing_consent_at"):
            raise HTTPException(status_code=403, detail="LLM-processing consent is missing")
        field = _field_input_by_id(
            payload,
            registry,
            request.field_id,
            status=request.status,
            answer=request.answer,
            clarification=request.clarification,
        )
        try:
            result = auditor.assess_field(field)
        except LLMAuditUnavailableError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except LLMAuditProviderError as exc:
            raise HTTPException(
                status_code=502,
                detail="AI quality review is temporarily unavailable.",
            ) from exc
        return {
            **result.quality.model_dump(),
            "provider": result.receipt.provider,
            "model": result.receipt.model,
            "audit_version": result.receipt.audit_version,
        }

    @app.post("/api/sessions/{session_id}/semantic-audit")
    def semantic_audit(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        if payload.get("format_version") != "guided-fields-v2":
            raise HTTPException(status_code=409, detail="LLM audit requires v2 fields")
        if not payload.get("llm_processing_consent_at"):
            raise HTTPException(status_code=403, detail="LLM-processing consent is missing")
        if not _core_complete(payload, spec):
            raise HTTPException(status_code=409, detail="complete all six core sections first")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict) or audit.get("audit_version") != LLM_AUDIT_VERSION:
            audit = _build_llm_audit(
                payload,
                registry,
                auditor,
                max_clarifications=MAX_CLARIFICATIONS,
                mode="core_llm_v1",
            )
            payload["semantic_audit"] = audit
            store.save(payload)
        return _public_audit_state(audit, cap=MAX_CLARIFICATIONS)

    @app.post("/api/sessions/{session_id}/semantic-audit/answers")
    def submit_semantic_clarification(
        session_id: str,
        request: ClarificationAnswerRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict) or audit.get("audit_version") != LLM_AUDIT_VERSION:
            raise HTTPException(status_code=409, detail="LLM audit has not been generated")
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
        if payload.get("status") == "frozen":
            return {"status": "frozen", "freeze_sha256": payload.get("freeze_sha256")}
        if payload.get("format_version") != "guided-fields-v2":
            raise HTTPException(status_code=409, detail="adaptive freeze requires v2 session")
        if not _core_complete(payload, spec):
            raise HTTPException(status_code=409, detail="complete all six core sections first")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict) or audit.get("audit_version") != LLM_AUDIT_VERSION:
            raise HTTPException(status_code=409, detail="run the LLM audit before freezing")
        if _next_audit_item(audit) is not None:
            raise HTTPException(status_code=409, detail="complete LLM clarifications first")
        payload["status"] = "frozen"
        payload["freeze_sha256"] = _content_digest(payload, audit)
        payload["frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {"status": "frozen", "freeze_sha256": payload["freeze_sha256"]}

    @app.post("/api/sessions/{session_id}/llm-addendum")
    def start_llm_addendum(
        session_id: str,
        request: LLMAddendumStartRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload.get("status") != "frozen":
            raise HTTPException(status_code=409, detail="LLM addendum requires a frozen session")
        if not request.consent_to_llm_processing:
            raise HTTPException(status_code=400, detail="LLM-processing consent is required")
        if not _can_llm_addendum(payload, registry):
            raise HTTPException(
                status_code=409,
                detail="this session cannot use the post-freeze LLM addendum path",
            )
        addendum = payload.get("llm_addendum")
        if not isinstance(addendum, dict):
            addendum = _build_llm_audit(
                payload,
                registry,
                auditor,
                max_clarifications=MAX_POST_FREEZE_CLARIFICATIONS,
                mode="post_freeze_llm_addendum_v1",
                include_prior_clarifications=True,
            )
            addendum["status"] = "in_progress"
            addendum["parent_freeze_sha256"] = payload.get("freeze_sha256")
            addendum["freeze_sha256"] = None
            payload["llm_addendum"] = addendum
            payload["llm_addendum_consent_at"] = datetime.now(UTC).isoformat()
            store.save(payload)
        return _public_audit_state(addendum, cap=MAX_POST_FREEZE_CLARIFICATIONS)

    @app.post("/api/sessions/{session_id}/llm-addendum/answers")
    def submit_llm_addendum_answer(
        session_id: str,
        request: ClarificationAnswerRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("llm_addendum")
        if not isinstance(addendum, dict) or addendum.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="LLM addendum is not active")
        expected = _next_audit_item(addendum)
        if expected is None:
            raise HTTPException(status_code=409, detail="no LLM clarification is pending")
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
                "status": request.status,
                "answer": answer,
                "answered_at": datetime.now(UTC).isoformat(),
            }
        )
        store.save(payload)
        return _public_audit_state(addendum, cap=MAX_POST_FREEZE_CLARIFICATIONS)

    @app.post("/api/sessions/{session_id}/llm-addendum/freeze")
    def freeze_llm_addendum(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("llm_addendum")
        if not isinstance(addendum, dict):
            raise HTTPException(status_code=409, detail="no LLM addendum exists")
        if addendum.get("status") == "frozen":
            return {"status": "frozen", "freeze_sha256": addendum.get("freeze_sha256")}
        if _next_audit_item(addendum) is not None:
            raise HTTPException(status_code=409, detail="complete LLM clarifications first")
        addendum["status"] = "frozen"
        addendum["freeze_sha256"] = _addendum_digest(addendum)
        addendum["frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {"status": "frozen", "freeze_sha256": addendum["freeze_sha256"]}

    return app
