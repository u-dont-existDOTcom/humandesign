"""Resilient owner interview overlay for Life Patterns recoverability development.

This layer addresses three consumer-seam failures without exposing target mappings:

* long threads could forget earlier questions because the planner only received a short
  tail of the conversation;
* refinement could finish with no new synthesis, leaving an old proposal grounded in a
  fact the participant had since corrected;
* overall progress stayed at zero until a pattern was finally adjudicated.

Tentative model syntheses remain ephemeral until the participant makes an adjudication.
That prevents post-proposal fact corrections from invalidating a durable proposal that the
participant never accepted. A bounded coverage assessment is attached periodically during
an active thread so the client can update its progress horizon before final adjudication.
"""

from __future__ import annotations

import uuid
from types import MethodType
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .life_patterns_recoverability_domains import RECOVERABILITY_DOMAINS
from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import ConversationMove, TurnExtraction
from .life_patterns_v2_owner_reasoning import (
    AdaptiveRefinablePatternSession,
    _ADAPTIVE_INTERVIEW_INSTRUCTIONS,
    _REFINEMENT_INSTRUCTIONS,
)
from .life_patterns_v2_owner_recoverability import (
    RecoverabilityCoverageRuntime,
    create_life_patterns_v2_owner_recoverability_app,
)
from .life_patterns_v2_owner_resilient_ui import RESILIENT_RECOVERABILITY_HTML
from .life_patterns_v2_owner_scope import (
    ScopeAwareRecoverabilityOpenAIModel,
    TransactionalRecoverabilityCoverageSession,
)

_THREAD_DISCIPLINE = (
    "THREAD DISCIPLINE: Keep this thread about the participant's current pattern. The larger interview has a separate "
    "finite coverage process, so do NOT expand this one thread into every adjacent personality dimension merely because "
    "the topic could connect to them. Once the original pattern's central meaning, scope, and the few modifiers that "
    "materially change it are clear, surface a synthesis and leave unrelated dimensions for later interview questions. "
    "Before asking anything, scan the FULL supplied conversation for the same semantic question or an answer that already "
    "settles it. Rewording a previously answered question is still repetition. If the participant says something was "
    "already asked or answered, do not ask a neighboring version of it unless genuinely new contradictory evidence makes "
    "the distinction decision-changing."
)

_REFINEMENT_WITH_SYNTHESIS = _REFINEMENT_INSTRUCTIONS.replace(
    "Do not return surface_hypothesis in this refinement call. Ask at most one question, and ask it only if plausible answers could "
    "materially change or qualify the person-level formulation. If no useful unresolved discriminator remains, say "
    "briefly that you do not see another high-value question rather than inventing one.",
    "If another answer could materially change the person-level formulation, ask at most one question. If no useful "
    "unresolved discriminator remains, return surface_hypothesis with a NEW final tentative synthesis grounded only in "
    "current operative facts. Do not merely announce that questioning is done. The participant needs an actual synthesis "
    "to judge. If later participant evidence corrected or narrowed an earlier premise, the new synthesis must use the "
    "corrected current evidence rather than preserving the old draft.",
).replace(
    "Keep the runtime interviewer free of external framework labels or target mappings. For every allowed move return "
    "hypothesis_proposition=null and evidence_fact_ids=[].",
    "Keep the runtime interviewer free of external framework labels or target mappings. For follow_up, request_contrast, "
    "and boundary_question return hypothesis_proposition=null and evidence_fact_ids=[]. For surface_hypothesis return "
    "the revised proposition plus only current operative evidence_fact_ids that actually ground it.",
)


class ResilientRecoverabilityOpenAIModel(ScopeAwareRecoverabilityOpenAIModel):
    """Planner that preserves full thread memory and can finish refinement with a synthesis."""

    def _move_schema(self, *, refinement: bool = False) -> dict[str, Any]:
        # Refinement must be allowed to end in a revised synthesis. The participant-facing
        # draft remains ephemeral until adjudication, so this does not create an automatic
        # person-level claim.
        return super()._move_schema(refinement=False)

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes: tuple[Any, ...],
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
        boundary_answered: bool,
    ) -> ConversationMove:
        result = self._conversation_call_json(
            instructions=_ADAPTIVE_INTERVIEW_INSTRUCTIONS + "\n\n" + _THREAD_DISCIPLINE,
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
                # The prior 20-turn window caused real duplicate questions in owner testing.
                # Keep the whole practical thread in view while still bounding pathological size.
                "recent_conversation": list(recent_conversation[-80:]),
                "boundary_answered": boundary_answered,
                "boundary_answered_is_advisory_not_a_gate": True,
            },
            schema=self._move_schema(),
            effort="medium",
            max_output_tokens=1800,
            schema_name="life_patterns_conversation_move_v1",
        )
        return ConversationMove.model_validate(result)

    def plan_refinement_turn(
        self,
        *,
        current_proposition: str,
        refinement_mode: str,
        current_episode_id: str | None,
        episodes: tuple[Any, ...],
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> ConversationMove:
        result = self._conversation_call_json(
            instructions=_REFINEMENT_WITH_SYNTHESIS + "\n\n" + _THREAD_DISCIPLINE,
            payload={
                "refinement_mode": refinement_mode,
                "current_tentative_synthesis": current_proposition,
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
            },
            schema=self._move_schema(refinement=True),
            effort="medium",
            max_output_tokens=1800,
            schema_name="life_patterns_refinement_move_v1",
        )
        return ConversationMove.model_validate(result)


class ResilientRecoverabilityCoverageSession(TransactionalRecoverabilityCoverageSession):
    """Keep tentative syntheses outside the v2 record until participant judgment."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self._draft_move: ConversationMove | None = None
        self._last_progress_user_turn_count = 0
        self._last_progress_report: dict[str, Any] | None = None

    def _snapshot_state(self) -> tuple[Any, ...]:
        return (
            super()._snapshot_state(),
            self._draft_move,
            self._last_progress_user_turn_count,
            self._last_progress_report,
        )

    def _restore_state(self, snapshot: tuple[Any, ...]) -> None:
        base, draft, progress_turn_count, progress_report = snapshot
        super()._restore_state(base)
        self._draft_move = draft
        self._last_progress_user_turn_count = progress_turn_count
        self._last_progress_report = progress_report

    def _create_pattern(self, move: ConversationMove) -> None:
        """Validate and hold a working synthesis without committing a v2 proposal yet."""

        fact_by_id = self._operative_by_id()
        evidence_ids = tuple(dict.fromkeys(move.evidence_fact_ids))
        if not evidence_ids:
            raise ValueError("conversation hypothesis requires grounded evidence")
        if not set(evidence_ids).issubset(fact_by_id):
            raise ValueError("conversation hypothesis cited unknown or superseded fact IDs")
        proposition = (move.hypothesis_proposition or "").strip()
        if not proposition:
            raise ValueError("conversation hypothesis requires a proposition")
        exact_matches = [
            fact_by_id[fact_id]
            for fact_id in evidence_ids
            if proposition.casefold() == fact_by_id[fact_id].proposition.strip().casefold()
        ]
        if exact_matches and not any(
            fact.assertion_type == "reported_appraisal_or_belief" for fact in exact_matches
        ):
            raise ValueError("an episode-only fact cannot be promoted unchanged into a person-level pattern")
        self._draft_move = move.model_copy(update={"evidence_fact_ids": evidence_ids})

    def _active_proposition(self) -> str:
        if self._draft_move is not None:
            return (self._draft_move.hypothesis_proposition or "").strip()
        return super()._active_proposition()

    def _plan_draft_refinement(self, refinement_mode: str) -> ConversationMove:
        planner = getattr(self.model, "plan_refinement_turn", None)
        if callable(planner):
            move = planner(
                current_proposition=self._active_proposition(),
                refinement_mode=refinement_mode,
                current_episode_id=self.current_episode_id,
                episodes=self.core.record.episodes,
                operative_facts=self.core.operative_facts(),
                recent_conversation=tuple(self.conversation),
            )
        else:
            move = self.model.plan_turn(
                current_episode_id=self.current_episode_id,
                episodes=self.core.record.episodes,
                operative_facts=self.core.operative_facts(),
                recent_conversation=tuple(self.conversation),
                boundary_answered=False,
            )
        if move.move_type == "request_contrast" and self.current_episode_id is None:
            return ConversationMove(reply=move.reply, move_type="follow_up")
        if move.move_type == "boundary_question" and not self.core.record.episodes:
            return ConversationMove(reply=move.reply, move_type="follow_up")
        return ConversationMove.model_validate(move)

    def _apply_draft_move(self, move: ConversationMove) -> dict[str, Any]:
        if move.move_type != "surface_hypothesis":
            return super()._apply_refinement_move(move)
        self._create_pattern(move)
        self.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "assistant",
                "text": move.reply,
            }
        )
        return {
            "reply": move.reply,
            "move_type": "surface_hypothesis",
            "pattern_active": True,
            "pattern_proposition": move.hypothesis_proposition,
            "episode_count": len(self.core.record.episodes),
            "pattern_refining": False,
            "synthesis_updated": True,
        }

    def _continue_draft(self, clean: str) -> dict[str, Any]:
        if self.pending_boundary_question:
            self.pending_boundary_question = False
        turn_id = f"TURN-{uuid.uuid4().hex[:10].upper()}"
        self.conversation.append({"turn_id": turn_id, "role": "user", "text": clean})
        start_new_episode = self.awaiting_new_episode or self.current_episode_id is None
        extraction = self.model.extract_turn(
            message=clean,
            current_episode_id=self.current_episode_id,
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation),
        )
        self._apply_extraction(
            extraction=extraction,
            turn_id=turn_id,
            message=clean,
            start_new_episode=start_new_episode,
        )
        return self._apply_draft_move(self._plan_draft_refinement("answer"))

    def _participant_user_turn_count(self) -> int:
        return sum(1 for row in self.conversation if row.get("role") == "user")

    def _attach_periodic_progress(self, result: dict[str, Any], *, force: bool = False) -> dict[str, Any]:
        """Refresh progress every few substantive turns without making it a per-turn extra model call."""

        count = self._participant_user_turn_count()
        should_refresh = force or (
            count >= 3 and count - self._last_progress_user_turn_count >= 3
        )
        if should_refresh:
            try:
                report = self.coverage_report()
            except Exception:
                # Progress is auxiliary. Never fail a successful interview turn because the
                # coverage estimate could not be refreshed.
                report = self._last_progress_report
            if report is not None:
                self._last_progress_report = report
                self._last_progress_user_turn_count = count
        if self._last_progress_report is not None:
            result["coverage"] = self._last_progress_report
        return result

    def turn(self, message: str) -> dict[str, Any]:
        clean = message.strip()
        if not clean:
            raise ValueError("message is required")
        snapshot = self._snapshot_state()
        try:
            if self._draft_move is not None:
                result = self._continue_draft(clean)
            else:
                result = super().turn(clean)
                if self._draft_move is not None:
                    result["pattern_active"] = True
                    result["pattern_proposition"] = self._draft_move.hypothesis_proposition
                    result["pattern_refining"] = False
            return self._attach_periodic_progress(
                result,
                force=bool(result.get("pattern_active")),
            )
        except Exception:
            self._restore_state(snapshot)
            raise

    def continue_pattern(self) -> dict[str, Any]:
        if self._draft_move is None:
            raise ValueError("no active tentative synthesis to continue")
        snapshot = self._snapshot_state()
        try:
            self.conversation.append(
                {
                    "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                    "role": "user",
                    "text": "Keep investigating.",
                }
            )
            return self._attach_periodic_progress(
                self._apply_draft_move(self._plan_draft_refinement("continue"))
            )
        except Exception:
            self._restore_state(snapshot)
            raise

    def disagree_with_pattern(self) -> dict[str, Any]:
        if self._draft_move is None:
            raise ValueError("no active tentative synthesis to disagree with")
        snapshot = self._snapshot_state()
        try:
            self.conversation.append(
                {
                    "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                    "role": "user",
                    "text": "The current synthesis does not fit.",
                }
            )
            return self._attach_periodic_progress(
                self._apply_draft_move(self._plan_draft_refinement("rejected"))
            )
        except Exception:
            self._restore_state(snapshot)
            raise

    def _materialize_draft(self) -> None:
        if self._draft_move is None:
            raise ValueError("no active tentative synthesis to adjudicate")
        # Call the parent implementation explicitly: our override intentionally keeps
        # drafts ephemeral, while this step creates the actual v2 proposal immediately
        # before participant adjudication.
        AdaptiveRefinablePatternSession._create_pattern(self, self._draft_move)

    def adjudicate(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        snapshot = self._snapshot_state()
        try:
            self._materialize_draft()
            result = super().adjudicate(request)
            self._draft_move = None
            return result
        except Exception:
            self._restore_state(snapshot)
            raise


def _create_resilient_session(
    runtime: RecoverabilityCoverageRuntime,
) -> ResilientRecoverabilityCoverageSession:
    session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
    session = ResilientRecoverabilityCoverageSession(
        session_id=session_id,
        model=runtime.model,
    )
    runtime.sessions[session_id] = session
    return session


def create_life_patterns_v2_owner_resilient_app() -> FastAPI:
    """Serve the current owner interview candidate with recovery-oriented seams."""

    model = ResilientRecoverabilityOpenAIModel.from_env()
    app = create_life_patterns_v2_owner_recoverability_app(model=model)
    runtime = app.state.recoverability_runtime
    runtime.create_session = MethodType(_create_resilient_session, runtime)

    # Replace the inherited root route so the client can merge in-thread progress and
    # keep a browser-local recovery copy of visible turns. The backup is not a scientific
    # freeze and never leaves the participant's browser unless they download it.
    app.router.routes[:] = [
        route for route in app.router.routes if getattr(route, "path", None) != "/"
    ]

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return RESILIENT_RECOVERABILITY_HTML

    app.state.resilient_refinement_synthesis = True
    app.state.ephemeral_pre_adjudication_synthesis = True
    app.state.full_thread_question_memory = True
    app.state.periodic_in_thread_progress = True
    app.state.browser_local_recovery_copy = True
    return app
