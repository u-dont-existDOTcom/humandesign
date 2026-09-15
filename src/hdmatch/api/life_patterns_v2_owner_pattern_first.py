"""Pattern-first owner conversation layered over the accepted Life Patterns v2 substrate.

The participant starts from a recurring/changing pattern in their own words. Concrete situations
are then used as evidence anchors while the v2 evidence ledger remains hidden.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import (
    ConversationalOwnerSession,
    ConversationTurnRequest,
    CreateConversationSessionResponse,
    OpenAIConversationModel,
    OwnerConversationModel,
)
from .life_patterns_v2_owner_conversation_ui import HTML

_NON_HYPOTHESIS_MOVES = frozenset({"follow_up", "request_contrast", "boundary_question"})
_TRANSIENT_MODEL_ERROR_MARKERS = (
    "HTTP 408:",
    "HTTP 500:",
    "HTTP 502:",
    "HTTP 503:",
    "HTTP 504:",
    "HTTP 520:",
    "HTTP 521:",
    "HTTP 522:",
    "HTTP 523:",
    "HTTP 524:",
    "model network error:",
)
_MODEL_PROVIDER_ATTEMPTS = 3


class TemporaryModelProviderError(RuntimeError):
    """Transient upstream failure after the bounded retry budget is exhausted."""


def _normalize_conversation_move_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize provider overpopulation without weakening the strict move contract."""

    normalized = dict(payload)
    if normalized.get("move_type") in _NON_HYPOTHESIS_MOVES:
        normalized["hypothesis_proposition"] = None
        normalized["evidence_fact_ids"] = []
    return normalized


def _is_transient_model_error(exc: RuntimeError) -> bool:
    detail = str(exc)
    return any(marker in detail for marker in _TRANSIENT_MODEL_ERROR_MARKERS)


class PatternFirstOpenAIConversationModel(OpenAIConversationModel):
    """Provider adapter with narrow normalization and bounded transient retries."""

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
                "\n\nThe conversation may begin with an ungrounded participant-reported pattern. "
                "Treat that description as conversational context, not ep"
                "isode evidence. After an anchor exists, "
                "prefer questions that sharpen scope, context, life-phase"
                " change, meaningful exceptions, mechanism, "
                "or a genuinely discriminating contrast. For follow_up, r"
                "equest_contrast, and boundary_question, "
                "return hypothesis_proposition=null and evidence_fact_ids=[]."
            )

        result: dict[str, Any] | None = None
        for attempt in range(_MODEL_PROVIDER_ATTEMPTS):
            try:
                result = super()._conversation_call_json(
                    instructions=instructions,
                    payload=payload,
                    schema=schema,
                    effort=effort,
                    max_output_tokens=max_output_tokens,
                    schema_name=schema_name,
                )
                break
            except RuntimeError as exc:
                if not _is_transient_model_error(exc):
                    raise
                if attempt + 1 >= _MODEL_PROVIDER_ATTEMPTS:
                    raise TemporaryModelProviderError(
                        "The model service is temporarily unavailable after automatic retries. "
                        "Nothing from this turn was saved; please try Send again in a moment."
                    ) from exc
                time.sleep(0.35 * (2**attempt))

        assert result is not None
        if schema_name == "life_patterns_conversation_move_v1":
            return _normalize_conversation_move_payload(result)
        return result


class PatternFirstConversationalOwnerSession(ConversationalOwnerSession):
    """Transactional session that keeps the initial pattern claim out of the episode ledger."""

    def __init__(self, *, session_id: str, model: OwnerConversationModel) -> None:
        super().__init__(session_id=session_id, model=model)
        self.pattern_focus_established = False

    def _snapshot_state(self) -> tuple[Any, ...]:
        return (
            list(self.conversation),
            self.current_episode_id,
            self.awaiting_new_episode,
            self.pending_boundary_question,
            self.boundary_answered,
            self.pattern_focus_established,
            self.core.record,
            dict(self.core.pending_episodes),
            dict(self.core.proposal_support),
            self.core.active_proposal_id,
        )

    def _restore_state(self, snapshot: tuple[Any, ...]) -> None:
        (
            conversation,
            current_episode_id,
            awaiting_new_episode,
            pending_boundary_question,
            boundary_answered,
            pattern_focus_established,
            record,
            pending_episodes,
            proposal_support,
            active_proposal_id,
        ) = snapshot
        self.conversation = conversation
        self.current_episode_id = current_episode_id
        self.awaiting_new_episode = awaiting_new_episode
        self.pending_boundary_question = pending_boundary_question
        self.boundary_answered = boundary_answered
        self.pattern_focus_established = pattern_focus_established
        self.core.record = record
        self.core.pending_episodes = pending_episodes
        self.core.proposal_support = proposal_support
        self.core.active_proposal_id = active_proposal_id

    def _start_from_pattern(self, clean: str) -> dict[str, Any]:
        turn_id = f"TURN-{uuid.uuid4().hex[:10].upper()}"
        self.conversation.append({"turn_id": turn_id, "role": "user", "text": clean})
        self.pattern_focus_established = True
        reply = (
            "Give me one real situation where that pattern showed up clearly. What happened? "
            "A representative example is fine; if the pattern is cont"
            "ext-dependent, choose a case that helps show the differe"
            "nce."
        )
        self.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "assistant",
                "text": reply,
            }
        )
        return {
            "reply": reply,
            "move_type": "follow_up",
            "pattern_active": False,
            "pattern_proposition": None,
            "episode_count": 0,
        }

    def turn(self, message: str) -> dict[str, Any]:
        clean = message.strip()
        if not clean:
            raise ValueError("message is required")
        if self.core.active_proposal_id is not None:
            raise ValueError("judge the current synthesis before continuing the interview")

        snapshot = self._snapshot_state()
        try:
            if not self.pattern_focus_established and not self.conversation:
                return self._start_from_pattern(clean)
            return super().turn(clean)
        except Exception:
            self._restore_state(snapshot)
            raise


@dataclass
class PatternFirstConversationRuntime:
    model: OwnerConversationModel
    sessions: dict[str, PatternFirstConversationalOwnerSession] = field(default_factory=dict)

    def create_session(self) -> PatternFirstConversationalOwnerSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = PatternFirstConversationalOwnerSession(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> PatternFirstConversationalOwnerSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


OPENING = (
    "Start with a pattern you notice in your life—something t"
    "hat tends to repeat, changes with context, "
    "has shifted over time, or puzzles you. Describe the patt"
    "ern in your own words. I’ll use concrete "
    "situations to test and sharpen it rather than treating one memory as the pattern itself."
)


def create_life_patterns_v2_owner_pattern_first_app(
    *, model: OwnerConversationModel | None = None
) -> FastAPI:
    resolved_model = model or PatternFirstOpenAIConversationModel.from_env()
    runtime = PatternFirstConversationRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns v2 pattern-first owner conversation", version="0.3")

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

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/adjudicate")
    def adjudicate_pattern(session_id: str, request: PatternAdjudicationRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_pattern_first_app()
