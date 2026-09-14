"""Reasoning-guarded owner-only Life Patterns conversation.

Adds an epistemic audit before a tentative synthesis reaches the participant and makes
proposal disagreement trigger model-led diagnosis rather than asking the participant to
restate an obvious unsupported leap. The accepted v2 evidence semantics remain unchanged.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import (
    ConversationTurnRequest,
    CreateConversationSessionResponse,
    OwnerConversationModel,
)
from .life_patterns_v2_owner_pattern_first import (
    OPENING,
    PatternFirstOpenAIConversationModel,
    TemporaryModelProviderError,
)
from .life_patterns_v2_owner_refinement import (
    HTML,
    RefinablePatternFirstConversationalOwnerSession,
)


class ReasoningGuardedPatternFirstOpenAIConversationModel(PatternFirstOpenAIConversationModel):
    """Require proposition-level support before exposing a synthesis."""

    def _conversation_call_json(
        self,
        *,
        instructions: str,
        payload: dict[str, Any],
        schema: dict[str, Any],
        effort: Literal["low", "medium"],
        max_output_tokens: int,
        schema_name: str,
    ) -> dict[str, Any]:
        if schema_name == "life_patterns_conversation_move_v1":
            instructions += (
                "\n\nEPISTEMIC DISCIPLINE FOR SYNTHESIS: Treat each participant-supplied factor as additive "
                "unless the evidence actually compares its importance with another factor. Never infer that a subject, "
                "cause, or context matters less/more, mainly, primarily, or rather than another merely because the "
                "participant introduced an additional factor. Do not transfer a factor observed in one episode/context "
                "to another episode/context without direct support. Keep distinct reported outcomes distinct (for example "
                "curiosity, meaning, attention, energy) unless the participant explicitly links them. Do not use an umbrella "
                "label such as 'mental state' as explanatory compression when it merely renames the thing being explained. "
                "If a requested counterexample/boundary answer merely adds another possible factor without actually resolving "
                "the requested contrast, ask the discriminating follow-up instead of treating the boundary as established. "
                "If the latest participant message rejects a synthesis, first inspect the synthesis against the existing "
                "evidence and target the weakest unsupported leap with one specific question; do not default to asking the "
                "participant to explain what was obvious from the transcript, and do not immediately surface another synthesis."
            )

        result = super()._conversation_call_json(
            instructions=instructions,
            payload=payload,
            schema=schema,
            effort=effort,
            max_output_tokens=max_output_tokens,
            schema_name=schema_name,
        )
        if schema_name != "life_patterns_conversation_move_v1":
            return result
        if result.get("move_type") != "surface_hypothesis":
            return result

        audit_schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["acceptable", "issue_type", "repair_question", "internal_reason"],
            "properties": {
                "acceptable": {"type": "boolean"},
                "issue_type": {
                    "type": "string",
                    "enum": [
                        "none",
                        "unsupported_comparison",
                        "unsupported_causal_weight",
                        "cross_context_projection",
                        "construct_conflation",
                        "circular_abstraction",
                        "boundary_not_resolved",
                        "quantifier_strengthening",
                        "other_unsupported_inference",
                    ],
                },
                "repair_question": {
                    "anyOf": [
                        {"type": "string", "minLength": 1, "maxLength": 1200},
                        {"type": "null"},
                    ]
                },
                "internal_reason": {"type": "string", "minLength": 1, "maxLength": 700},
            },
        }
        audit = super()._conversation_call_json(
            instructions=(
                "Audit a tentative Life Patterns synthesis for epistemic support before it is shown. Judge only what the "
                "supplied episode facts and conversation establish, not what sounds psychologically plausible. Fail the "
                "candidate if any material clause: (1) ranks or displaces factors without a direct comparison; (2) assigns "
                "causal weight not established by the evidence; (3) projects a factor from one context into another; (4) "
                "merges distinct constructs without support; (5) uses a broad abstraction that merely renames the outcome; "
                "(6) treats a non-answer to a requested contrast/counterexample as if that boundary were resolved; or (7) "
                "strengthens frequency, scope, or certainty beyond the participant's report. Multiple contributing factors "
                "never imply that one matters less than another unless the participant supplied discriminating evidence. "
                "If unacceptable, write one participant-facing repair_question aimed at the exact unresolved distinction. "
                "Do not ask 'what did I get wrong?' when the unsupported leap is already visible from the supplied record. "
                "The question must remain target-theory-blind and must not mention hidden facts or this audit."
            ),
            payload={
                "candidate": result,
                "episodes": payload.get("episodes", []),
                "operative_facts": payload.get("operative_facts", []),
                "recent_conversation": payload.get("recent_conversation", []),
                "boundary_answered_flag": payload.get("boundary_answered"),
            },
            schema=audit_schema,
            effort="medium",
            max_output_tokens=1100,
            schema_name="life_patterns_hypothesis_audit_v1",
        )
        if audit.get("acceptable"):
            return result

        repair_question = (audit.get("repair_question") or "").strip()
        if not repair_question:
            repair_question = (
                "I may be combining factors the examples have not actually compared. "
                "What real contrast would separate the leading possibilities?"
            )
        return {
            "reply": repair_question,
            "move_type": "follow_up",
            "hypothesis_proposition": None,
            "evidence_fact_ids": [],
        }


class ReasoningRefinablePatternSession(RefinablePatternFirstConversationalOwnerSession):
    """Use the interviewer to diagnose a rejected synthesis before burdening the participant."""

    def disagree_with_pattern(self) -> dict[str, Any]:
        if self.core.active_proposal_id is None:
            raise ValueError("no active pattern proposal to disagree with")
        snapshot = self._snapshot_state()
        try:
            self.conversation.append(
                {
                    "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                    "role": "user",
                    "text": "No — that synthesis does not fit.",
                }
            )
            return self._apply_refinement_move(self._plan_refinement_move())
        except Exception:
            self._restore_state(snapshot)
            raise


@dataclass
class ReasoningRefinableRuntime:
    model: OwnerConversationModel
    sessions: dict[str, ReasoningRefinablePatternSession] = field(default_factory=dict)

    def create_session(self) -> ReasoningRefinablePatternSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = ReasoningRefinablePatternSession(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> ReasoningRefinablePatternSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def create_life_patterns_v2_owner_reasoning_app(
    *, model: OwnerConversationModel | None = None
) -> FastAPI:
    resolved_model = model or ReasoningGuardedPatternFirstOpenAIConversationModel.from_env()
    runtime = ReasoningRefinableRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns v2 reasoning-guarded owner conversation", version="0.6")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return HTML

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "owner_only": True,
            "target_theory_blind": True,
            "hidden_evidence_ledger": True,
            "pattern_first": True,
            "unresolved_thread_continuation": True,
            "rejected_synthesis_continuation": True,
            "hypothesis_support_audit": True,
            "rejection_reasoning_recovery": True,
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.post("/api/owner-v2/conversation/sessions")
    def create_session() -> CreateConversationSessionResponse:
        session = runtime.create_session()
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=OPENING,
        )

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def interview_turn(session_id: str, request: ConversationTurnRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).turn(request.message)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/continue")
    def continue_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).continue_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/disagree")
    def disagree_with_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).disagree_with_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
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
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_reasoning_app()
