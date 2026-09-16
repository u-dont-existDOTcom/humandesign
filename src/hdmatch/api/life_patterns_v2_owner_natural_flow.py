"""Natural-flow Life Patterns interview for owner development testing.

The participant should only be asked to adjudicate an interviewer inference. A person-specific
pattern the participant has already stated in their own words can be recorded from that original
source without repeating it back for confirmation. Generic/high-base-rate material still does not
become a Life Pattern merely because it was stated directly.

Participant judgment of an actual interviewer inference must not wait on another LLM coverage pass.
The runtime remains target-theory-blind. Recovery snapshots remain unvalidated audit checkpoints.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from types import MethodType
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from hdmatch.evaluation.participant_adjudicated_v2 import (
    ParticipantAdjudicationV2,
    PatternEvidenceLinkV2,
    PatternProposalV2,
)

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
    "DIRECT REPORT VERSUS INFERENCE: Whether a pattern feels obvious is irrelevant. A Life Pattern may be obvious to "
    "the participant and still be highly person-specific. The important distinctions are (a) PERSON-SPECIFIC versus "
    "generic/high-base-rate, and (b) DIRECTLY STATED BY THE PARTICIPANT versus INFERRED BY THE INTERVIEWER. Do not "
    "discard a person-specific pattern merely because it is an obvious restatement of what the participant already "
    "knows. If the participant has ALREADY explicitly stated the person-specific pattern and no new inferential relation "
    "is being added, use surface_hypothesis but set hypothesis_proposition to an EXACT CONTIGUOUS VERBATIM substring "
    "from one participant message that itself states the pattern. Cite only operative facts derived from that same "
    "participant message, including at least one reported_appraisal_or_belief fact. In that direct-report case, do NOT "
    "repeat the pattern in reply and do NOT ask whether it fits; reply briefly that this area gives enough information "
    "to move on. The runtime will recognize the exact participant-authored wording and record it using the original "
    "participant provenance without another approval step. If you add ANY synthesis, comparison, causal/conditional "
    "relation, scope claim, compression, or other proposition the participant did not explicitly state, that is an "
    "INTERVIEWER INFERENCE: use surface_hypothesis normally, phrase the inferred synthesis tentatively, and ask the "
    "participant to judge it.\n\n"
    "TOPIC COMPLETION: Use topic_complete only when the current measurement area has enough information and there is no "
    "useful person-specific Life Pattern to record from it—for example the available material is generic to people in "
    "general, merely contextual, or otherwise does not support a person-level pattern. topic_complete is a successful "
    "local ending, not a failure. Do not use topic_complete merely because a valid person-specific pattern is obvious or "
    "already known to the participant. For topic_complete return hypothesis_proposition=null and evidence_fact_ids=[]."
)


@dataclass(frozen=True)
class TopicCompleteMove:
    reply: str
    move_type: Literal["topic_complete"] = "topic_complete"
    hypothesis_proposition: None = None
    evidence_fact_ids: tuple[str, ...] = ()


class NaturalFlowRecoverabilityOpenAIModel(ResilientRecoverabilityOpenAIModel):
    """Allow clean topic completion while distinguishing direct reports from inference."""

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes: tuple[Any, ...],
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
        boundary_answered: bool,
    ) -> Any:
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
                        "source_provenance_ids": list(fact.source_provenance_ids),
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
    """Persistent session with direct-report recording and inference-only confirmation."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self._topic_complete_ready = False
        self._auto_recorded_direct_result: dict[str, Any] | None = None

    def _snapshot_state(self) -> tuple[Any, ...]:
        return (
            super()._snapshot_state(),
            self._topic_complete_ready,
            self._auto_recorded_direct_result,
        )

    def _restore_state(self, snapshot: tuple[Any, ...]) -> None:
        base, topic_complete_ready, auto_recorded = snapshot
        super()._restore_state(base)
        self._topic_complete_ready = bool(topic_complete_ready)
        self._auto_recorded_direct_result = auto_recorded

    def _direct_report_source(
        self, move: ConversationMove
    ) -> tuple[str, str, tuple[str, ...]] | None:
        """Return exact participant wording/source/evidence only for a mechanically direct report.

        This intentionally uses a strict test. If the model paraphrases, combines multiple user turns,
        cites evidence from another source turn, or otherwise adds interpretation, the move remains an
        ordinary tentative synthesis and requires participant judgment.
        """

        wording = (move.hypothesis_proposition or "").strip()
        if not wording or not move.evidence_fact_ids:
            return None

        source_ids = {row.source_provenance_id for row in self.core.record.source_provenance}
        matching_source: str | None = None
        for row in reversed(self.conversation):
            if row.get("role") != "user":
                continue
            text = str(row.get("text", ""))
            if wording not in text:
                continue
            turn_id = str(row.get("turn_id", ""))
            source_id = f"SRC-{turn_id}"
            if source_id in source_ids:
                matching_source = source_id
                break
        if matching_source is None:
            return None

        fact_by_id = self._operative_by_id()
        evidence_ids = tuple(dict.fromkeys(move.evidence_fact_ids))
        if not set(evidence_ids).issubset(fact_by_id):
            return None
        evidence = tuple(fact_by_id[fact_id] for fact_id in evidence_ids)
        if any(matching_source not in fact.source_provenance_ids for fact in evidence):
            return None
        if not any(fact.assertion_type == "reported_appraisal_or_belief" for fact in evidence):
            return None
        return wording, matching_source, evidence_ids

    def _record_direct_reported_pattern(
        self,
        *,
        wording: str,
        source_id: str,
        evidence_ids: tuple[str, ...],
    ) -> dict[str, Any]:
        """Record a participant-authored person-level pattern without inventing a second approval."""

        fact_by_id = self._operative_by_id()
        proposal_id = f"PROP-{uuid.uuid4().hex[:10].upper()}"
        grouped: dict[str, list[str]] = {}
        for fact_id in evidence_ids:
            grouped.setdefault(fact_by_id[fact_id].episode_id, []).append(fact_id)
        links = tuple(
            PatternEvidenceLinkV2(
                evidence_link_id=f"LINK-{uuid.uuid4().hex[:10].upper()}",
                proposal_id=proposal_id,
                episode_id=episode_id,
                fact_ids=tuple(fact_ids),
                role="preproposal_anchor",
                acquisition_phase="pre_first_proposal",
            )
            for episode_id, fact_ids in grouped.items()
        )
        proposal = PatternProposalV2(
            proposal_id=proposal_id,
            pattern_thread_id=f"THREAD-{uuid.uuid4().hex[:10].upper()}",
            revision_index=0,
            proposition=wording,
            question_text="Participant directly stated this person-level pattern; no inferential confirmation was requested.",
            evidence_link_ids=tuple(link.evidence_link_id for link in links),
            grounding_evidence_link_ids=tuple(link.evidence_link_id for link in links),
        )
        adjudication = ParticipantAdjudicationV2(
            adjudication_id=f"ADJ-{uuid.uuid4().hex[:10].upper()}",
            proposal_id=proposal_id,
            decision="accept",
            participant_response_provenance_ids=(source_id,),
            participant_approved_wording=wording,
        )
        self.core.record = self.core.record.model_copy(
            update={
                "pattern_proposals": self.core.record.pattern_proposals + (proposal,),
                "pattern_evidence_links": self.core.record.pattern_evidence_links + links,
                "participant_adjudications": self.core.record.participant_adjudications
                + (adjudication,),
            }
        )
        self.core.proposal_support[proposal_id] = frozenset(evidence_ids)
        self.core.active_proposal_id = proposal_id
        result = self.core._final_result()
        self.core.active_proposal_id = None
        result.update(
            {
                "direct_pattern_recorded": True,
                "pattern_active": False,
                "pattern_proposition": None,
                "topic_complete": True,
                "move_type": "direct_pattern",
                "reply": "That gives me enough information for this area; we can move on.",
            }
        )
        return result

    def _create_pattern(self, move: ConversationMove) -> None:
        direct = self._direct_report_source(move)
        if direct is not None:
            wording, source_id, evidence_ids = direct
            self._auto_recorded_direct_result = self._record_direct_reported_pattern(
                wording=wording,
                source_id=source_id,
                evidence_ids=evidence_ids,
            )
            self._topic_complete_ready = True
            self._draft_move = None
            return
        self._auto_recorded_direct_result = None
        super()._create_pattern(move)

    def turn(self, message: str) -> dict[str, Any]:
        self._auto_recorded_direct_result = None
        result = super().turn(message)
        if self._auto_recorded_direct_result is not None:
            direct_result = dict(self._auto_recorded_direct_result)
            # The base turn has already appended the planner reply to conversation. Replace
            # the response metadata, not the source conversation, with the direct-record result.
            direct_result["reply"] = result.get("reply") or direct_result["reply"]
            direct_result["episode_count"] = len(self.core.record.episodes)
            self._auto_recorded_direct_result = None
            return self._attach_periodic_progress(direct_result, force=True)
        if result.get("move_type") == "topic_complete":
            self._topic_complete_ready = True
            result["topic_complete"] = True
            return self._attach_periodic_progress(result, force=True)
        self._topic_complete_ready = False
        return result

    def adjudicate(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        """Commit an actual inferred-synthesis judgment without another coverage-model call."""

        snapshot = self._snapshot_state()
        try:
            self._materialize_draft()
            result = self.core.adjudicate_pattern(request)
            self.core.active_proposal_id = None
            self._draft_move = None
            self._topic_complete_ready = False
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
        self._auto_recorded_direct_result = None

    def visible_recovery_seed(self, turns: list[dict[str, Any]]) -> None:
        super().visible_recovery_seed(turns)
        self._topic_complete_ready = False
        self._auto_recorded_direct_result = None

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
    app.state.direct_participant_patterns_skip_redundant_confirmation = True
    app.state.inferred_patterns_require_participant_judgment = True
    app.state.pattern_adjudication_uses_cached_progress = True
    app.state.progress_and_liveness_at_active_end = True
    return app
