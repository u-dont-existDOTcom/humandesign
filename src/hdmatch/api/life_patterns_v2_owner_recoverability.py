"""Recoverability-oriented standardized coverage for the Life Patterns interview.

Participant execution remains target-theory-blind. Historical AstroHD mappings live
outside this runtime and may be applied only after a fresh owner measurement is frozen.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .life_patterns_recoverability_domains import RECOVERABILITY_DOMAINS
from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import (
    ConversationTurnRequest,
    CreateConversationSessionResponse,
    OwnerConversationModel,
)
from .life_patterns_v2_owner_coverage import (
    COVERAGE_COMPLETE_STATUSES,
    COVERAGE_HTML,
    COVERAGE_STATUSES,
    CoverageDomain,
    CoverageSessionRequest,
    StandardizedCoverageOpenAIModel,
)
from .life_patterns_v2_owner_pattern_first import TemporaryModelProviderError
from .life_patterns_v2_owner_reasoning import ADAPTIVE_OPENING, AdaptiveRefinablePatternSession

RECOVERABILITY_BLUEPRINT_VERSION = "life-patterns-recoverability-coverage-v2"
_DOMAIN_BY_ID = {domain.domain_id: domain for domain in RECOVERABILITY_DOMAINS}


def _blueprint_payload() -> list[dict[str, str]]:
    return [
        {
            "domain_id": domain.domain_id,
            "title": domain.title,
            "definition": domain.definition,
            "canonical_screener": domain.canonical_screener,
        }
        for domain in RECOVERABILITY_DOMAINS
    ]


RECOVERABILITY_BLUEPRINT_SHA256 = hashlib.sha256(
    json.dumps(
        {"version": RECOVERABILITY_BLUEPRINT_VERSION, "domains": _blueprint_payload()},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()


class RecoverabilityCoverageOpenAIModel(StandardizedCoverageOpenAIModel):
    """Target-blind assessor for the fixed neutral recoverability dimensions."""

    def assess_required_coverage(
        self,
        *,
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> dict[str, Any]:
        domain_ids = [domain.domain_id for domain in RECOVERABILITY_DOMAINS]
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["assessments"],
            "properties": {
                "assessments": {
                    "type": "array",
                    "minItems": len(domain_ids),
                    "maxItems": len(domain_ids),
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["domain_id", "status", "evidence_fact_ids", "reason"],
                        "properties": {
                            "domain_id": {"type": "string", "enum": domain_ids},
                            "status": {"type": "string", "enum": list(COVERAGE_STATUSES)},
                            "evidence_fact_ids": {
                                "type": "array",
                                "maxItems": 16,
                                "items": {"type": "string"},
                            },
                            "reason": {"type": "string", "minLength": 1, "maxLength": 700},
                        },
                    },
                }
            },
        }
        return self._conversation_call_json(
            instructions=(
                "Assess standardized behavioral-dimension COVERAGE only. The dimensions are neutral; you are not "
                "given any external theory, chart, target mapping, score, or expected answer direction. Return exactly "
                "one row for every required dimension. Use unassessed for no meaningful information; partial for "
                "relevant information that does not yet support a stable person-specific characterization; sufficient "
                "for a narrow interpretable person-specific characterization; unknown only when the participant "
                "directly addressed the dimension and cannot tell; inapplicable only when the participant says it "
                "genuinely does not apply; declined only for explicit refusal. Silence is never absence. Generic human "
                "regularities are not sufficient. Preserve context, intensity/duration, capacity-versus-preference, "
                "developmental change, and self-versus-observer distinctions when they materially affect meaning. Do "
                "not require a fixed number of episodes. For partial or sufficient, cite only supplied operative fact "
                "IDs that actually support the status.\n\nREQUIRED DIMENSIONS:\n"
                + "\n".join(
                    f"- {domain.domain_id}: {domain.definition}" for domain in RECOVERABILITY_DOMAINS
                )
            ),
            payload={
                "operative_facts": [
                    {
                        "fact_id": fact.fact_id,
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in operative_facts
                ],
                "recent_conversation": list(recent_conversation[-30:]),
            },
            schema=schema,
            effort="medium",
            max_output_tokens=3600,
            schema_name="life_patterns_recoverability_coverage_v2",
        )


def _normalize_recoverability_coverage(
    raw: dict[str, Any], *, operative_facts: tuple[Any, ...]
) -> dict[str, Any]:
    known_fact_ids = {fact.fact_id for fact in operative_facts}
    rows = raw.get("assessments", [])
    by_id: dict[str, dict[str, Any]] = {
        str(row["domain_id"]): row
        for row in rows
        if isinstance(row, dict) and row.get("domain_id") in _DOMAIN_BY_ID
    } if isinstance(rows, list) else {}

    assessments: list[dict[str, Any]] = []
    for domain in RECOVERABILITY_DOMAINS:
        row = by_id.get(domain.domain_id, {})
        status = str(row.get("status", "unassessed"))
        if status not in COVERAGE_STATUSES:
            status = "unassessed"
        evidence_ids = list(
            dict.fromkeys(
                fact_id
                for fact_id in row.get("evidence_fact_ids", [])
                if isinstance(fact_id, str) and fact_id in known_fact_ids
            )
        )
        if status in {"partial", "sufficient"} and not evidence_ids:
            status = "unassessed"
        assessments.append(
            {
                "domain_id": domain.domain_id,
                "title": domain.title,
                "status": status,
                "evidence_fact_ids": evidence_ids,
                "reason": str(row.get("reason", "No supported assessment returned.")),
            }
        )

    return {
        "blueprint_version": RECOVERABILITY_BLUEPRINT_VERSION,
        "blueprint_sha256": RECOVERABILITY_BLUEPRINT_SHA256,
        "assessments": assessments,
        "complete_domain_count": sum(
            1 for row in assessments if row["status"] in COVERAGE_COMPLETE_STATUSES
        ),
        "required_domain_count": len(RECOVERABILITY_DOMAINS),
    }


class RecoverabilityCoverageSession(AdaptiveRefinablePatternSession):
    def coverage_report(self) -> dict[str, Any]:
        assessor = getattr(self.model, "assess_required_coverage", None)
        if not callable(assessor):
            return _normalize_recoverability_coverage(
                {}, operative_facts=self.core.operative_facts()
            )
        raw = assessor(
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation),
        )
        return _normalize_recoverability_coverage(
            raw, operative_facts=self.core.operative_facts()
        )

    def adjudicate(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        result = super().adjudicate(request)
        result["coverage"] = self.coverage_report()
        return result


@dataclass
class RecoverabilityCoverageRuntime:
    model: OwnerConversationModel
    sessions: dict[str, RecoverabilityCoverageSession] = field(default_factory=dict)

    def create_session(self) -> RecoverabilityCoverageSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = RecoverabilityCoverageSession(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def create_coverage_session(
        self, domain_id: str
    ) -> tuple[RecoverabilityCoverageSession, CoverageDomain]:
        domain = _DOMAIN_BY_ID.get(domain_id)
        if domain is None:
            raise ValueError("unknown required coverage domain")
        session = self.create_session()
        session.pattern_focus_established = True
        session.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "assistant",
                "text": domain.canonical_screener,
            }
        )
        return session, domain

    def get(self, session_id: str) -> RecoverabilityCoverageSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def create_life_patterns_v2_owner_recoverability_app(
    *, model: OwnerConversationModel | None = None,
) -> FastAPI:
    resolved_model = model or RecoverabilityCoverageOpenAIModel.from_env()
    runtime = RecoverabilityCoverageRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns recoverability development interview", version="1.2")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return COVERAGE_HTML

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "development_surface": True,
            "target_theory_blind": True,
            "hidden_evidence_ledger": True,
            "pattern_first": True,
            "person_specificity_gate": True,
            "observer_triangulation": True,
            "neutral_person_model_discriminators": True,
            "refinement_repetition_guard": True,
            "standardized_required_coverage": True,
            "recoverability_preservation_candidate": True,
            "coverage_blueprint_version": RECOVERABILITY_BLUEPRINT_VERSION,
            "coverage_blueprint_sha256": RECOVERABILITY_BLUEPRINT_SHA256,
            "required_domain_count": len(RECOVERABILITY_DOMAINS),
            "adaptive_wording_with_fixed_domains": True,
            "fixed_episode_quota": False,
            "mandatory_counterexample_gate": False,
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.get("/api/owner-v2/conversation/coverage/blueprint")
    def coverage_blueprint() -> dict[str, Any]:
        return {
            "version": RECOVERABILITY_BLUEPRINT_VERSION,
            "sha256": RECOVERABILITY_BLUEPRINT_SHA256,
            "statuses": list(COVERAGE_STATUSES),
            "complete_statuses": sorted(COVERAGE_COMPLETE_STATUSES),
            "domains": _blueprint_payload(),
        }

    @app.post("/api/owner-v2/conversation/sessions")
    def create_session() -> CreateConversationSessionResponse:
        session = runtime.create_session()
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=ADAPTIVE_OPENING,
        )

    @app.post("/api/owner-v2/conversation/coverage/sessions")
    def create_coverage_session(
        request: CoverageSessionRequest,
    ) -> CreateConversationSessionResponse:
        try:
            session, domain = runtime.create_coverage_session(request.domain_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=domain.canonical_screener,
        )

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def interview_turn(session_id: str, request: ConversationTurnRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).turn(request.message)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/continue")
    def continue_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).continue_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/disagree")
    def disagree_with_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).disagree_with_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/adjudicate")
    def adjudicate_pattern(
        session_id: str, request: PatternAdjudicationRequest
    ) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_recoverability_app()
