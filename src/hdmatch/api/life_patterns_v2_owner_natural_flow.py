"""Natural-flow Life Patterns interview for owner development testing.

Two distinctions are enforced here:

* completing a measurement area does not require manufacturing a participant-level synthesis;
* participant judgment of an already-surfaced synthesis must not wait on another LLM coverage pass.

The runtime remains target-theory-blind. Recovery snapshots remain unvalidated audit checkpoints.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from types import MethodType
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import ConversationMove
from .life_patterns_v2_owner_liveness import create_life_patterns_v2_owner_liveness_app
from .life_patterns_v2_owner_natural_flow_ui import NATURAL_FLOW_RECOVERABILITY_HTML
from .life_patterns_v2_owner_persistent import (
    PersistentRecoverabilityCoverageSession,
    RecoveryRestoreRequest,
    VisibleRecoveryRestoreRequest,
    _canonical_sha,
)
from .life_patterns_v2_owner_reasoning import _ADAPTIVE_INTERVIEW_INSTRUCTIONS
from .life_patterns_v2_owner_resilient import (
    ResilientRecoverabilityOpenAIModel,
    _THREAD_DISCIPLINE,
)
from .life_patterns_v2_owner_recoverability import RecoverabilityCoverageRuntime


_NATURAL_COMPLETION_INSTRUCTIONS = (
    "MEASUREMENT COMPLETION IS NOT THE SAME AS AN INSIGHTFUL SYNTHESIS. The larger interview has a fixed "
    "measurement surface, but not every adequately measured area should become a named Life Pattern. Use "
    "topic_complete when the current material is specific enough that another question has low expected "
    "information gain, but any proposed person-level synthesis would mainly repackage, paraphrase, or enumerate "
    "what the participant just said. topic_complete is a successful local ending, not a failure: reply briefly that "
    "this gives enough information for this area and that the interview can move on. Do not summarize all their "
    "details again and do not ask a question. For topic_complete return hypothesis_proposition=null and "
    "evidence_fact_ids=[]. Use surface_hypothesis only when the synthesis adds a genuinely useful person-specific "
    "integration, conditional, contrast, boundary, recurring sequence, or other compression that is meaningfully "
    "more informative than the participant's immediately preceding statements. A synthesis does not need to be "
    "surprising, but participant approval should not be spent on a near-verbatim fact summary."
)


@dataclass(frozen=True)
class TopicCompleteMove:
    reply: str
    move_type: Literal["topic_complete"] = "topic_complete"
    hypothesis_proposition: None = None
    evidence_fact_ids: tuple[str, ...] = ()


class NaturalFlowRecoverabilityOpenAIModel(ResilientRecoverabilityOpenAIModel):
    """Allow the planner to finish a measured area without forcing a trivial synthesis."""

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes: tuple[Any, ...],
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
        boundary_answered: bool,
    ) -> ConversationMove | TopicCompleteMove:
        schema = self._move_schema()
        move_enum = schema["properties"]["move_type"]["enum"]
        if "topic_complete" not in move_enum:
            move_enum.append("topic_complete")
        result = self._conversation_call_json(
            instructions=(
                _ADAPTIVE_INTERVIEW_INSTRUCTIONS
                + "\n\n"
                + _THREAD_DISCIPLINE
                + "\n\n"
                + _NATURAL_COMPLETION_INSTRUCTIONS
            ),
            payload={
                "current_episode_id": current_episode_id,
                "episodes": [
                    {"episode_id": episode.episode_id, "neutral_summary": episode.neutral_summary}
                    for episode in episodes
                ],
                "operative_facts": [
                    {
                        "fact_id": fact.fact_id,
                        "episode_id": fact.episode_id,
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in operative_facts
                ],
                "recent_conversation": list(recent_conversation[-80:]),
                "boundary_answered": boundary_answered,
                "boundary_answered_is_advisory_not_a_gate": True,
            },
            schema=schema,
            effort="medium",
            max_output_tokens=1800,
            schema_name="life_patterns_conversation_move_v1",
        )
        if str(result.get("move_type", "")) == "topic_complete":
            reply = str(result.get("reply", "")).strip() or (
                "That gives me enough information for this area; we can move on."
            )
            return TopicCompleteMove(reply=reply)
        return ConversationMove.model_validate(result)


class NaturalFlowRecoverabilitySession(PersistentRecoverabilityCoverageSession):
    """Persistent session with explicit topic completion and low-latency adjudication."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self._topic_complete_ready = False

    def _snapshot_state(self) -> tuple[Any, ...]:
        return (super()._snapshot_state(), self._topic_complete_ready)

    def _restore_state(self, snapshot: tuple[Any, ...]) -> None:
        base, topic_complete_ready = snapshot
        super()._restore_state(base)
        self._topic_complete_ready = bool(topic_complete_ready)

    def turn(self, message: str) -> dict[str, Any]:
        result = super().turn(message)
        if result.get("move_type") == "topic_complete":
            self._topic_complete_ready = True
            result["topic_complete"] = True
            # Topic completion is itself a progress boundary. Refresh coverage now so the
            # participant sees the just-completed measurement area credited immediately.
            return self._attach_periodic_progress(result, force=True)
        self._topic_complete_ready = False
        return result

    def adjudicate(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        """Commit participant judgment without blocking on another coverage-model call."""

        snapshot = self._snapshot_state()
        try:
            self._materialize_draft()
            result = self.core.adjudicate_pattern(request)
            self.core.active_proposal_id = None
            self._draft_move = None
            self._topic_complete_ready = False
            # A surfaced synthesis already forced an in-thread coverage refresh. Reuse that
            # measurement metadata instead of making Yes/Reject wait on a second LLM call.
            if self._last_progress_report is not None:
                result["coverage"] = self._last_progress_report
            return result
        except Exception:
            self._restore_state(snapshot)
            raise

    def recovery_snapshot(self) -> dict[str, Any]:
        body = super().recovery_snapshot()
        body.pop("recovery_sha256", None)
        body["topic_complete_ready"] = self._topic_complete_ready
        body["recovery_sha256"] = _canonical_sha(body)
        return body

    def restore_recovery_snapshot(self, snapshot: dict[str, Any]) -> None:
        super().restore_recovery_snapshot(snapshot)
        self._topic_complete_ready = bool(snapshot.get("topic_complete_ready", False))

    def visible_recovery_seed(self, turns: list[dict[str, Any]]) -> None:
        super().visible_recovery_seed(turns)
        self._topic_complete_ready = False

    def recovery_status(self) -> dict[str, Any]:
        status = super().recovery_status()
        if self._topic_complete_ready and not status.get("pattern_active"):
            status["workflow_phase"] = "topic_complete"
        status["topic_complete_ready"] = self._topic_complete_ready
        return status


def _create_natural_session(
    runtime: RecoverabilityCoverageRuntime,
) -> NaturalFlowRecoverabilitySession:
    session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
    session = NaturalFlowRecoverabilitySession(session_id=session_id, model=runtime.model)
    runtime.sessions[session_id] = session
    return session


def create_life_patterns_v2_owner_natural_flow_app() -> FastAPI:
    """Serve the natural-flow owner interview while retaining current recovery/liveness seams."""

    app = create_life_patterns_v2_owner_liveness_app()
    runtime = app.state.recoverability_runtime
    runtime.model = NaturalFlowRecoverabilityOpenAIModel.from_env()
    runtime.create_session = MethodType(_create_natural_session, runtime)

    # Replace the root and restore constructors so restored sessions have the same behavior
    # as newly-created sessions. Other inherited routes keep using the shared runtime object.
    app.router.routes[:] = [
        route
        for route in app.router.routes
        if getattr(route, "path", None)
        not in {
            "/",
            "/api/owner-v2/conversation/sessions/restore",
            "/api/owner-v2/conversation/sessions/restore-visible",
        }
    ]

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return NATURAL_FLOW_RECOVERABILITY_HTML

    @app.post("/api/owner-v2/conversation/sessions/restore")
    def restore_recovery(request: RecoveryRestoreRequest) -> dict[str, Any]:
        raw_id = str(request.snapshot.get("session_id", "")).strip()
        session_id = (
            raw_id if raw_id.startswith("OWNER-") else f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        )
        session = NaturalFlowRecoverabilitySession(session_id=session_id, model=runtime.model)
        try:
            session.restore_recovery_snapshot(request.snapshot)
        except (TypeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        runtime.sessions[session_id] = session
        status = session.recovery_status()
        if session.recovery_quality == "reconstructed_visible_transcript":
            status["reconstructed_working_ledger_restored"] = True
            status["resume_capable"] = True
        return status

    @app.post("/api/owner-v2/conversation/sessions/restore-visible")
    def restore_visible(request: VisibleRecoveryRestoreRequest) -> dict[str, Any]:
        session = _create_natural_session(runtime)
        try:
            session.visible_recovery_seed(request.turns)
        except ValueError as exc:
            runtime.sessions.pop(session.session_id, None)
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return session.recovery_status()

    app.state.natural_topic_completion = True
    app.state.pattern_adjudication_uses_cached_progress = True
    app.state.progress_and_liveness_at_active_end = True
    return app
