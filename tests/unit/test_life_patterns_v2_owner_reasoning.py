from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_pattern_first import PatternFirstOpenAIConversationModel
from hdmatch.api.life_patterns_v2_owner_reasoning import (
    AdaptivePatternFirstOpenAIConversationModel,
    AdaptiveRefinablePatternSession,
)


def test_adaptive_planner_restores_followup_gate_without_second_audit(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_call(self, **kwargs):
        calls.append(kwargs)
        return {
            "reply": "A narrow supported synthesis.",
            "move_type": "surface_hypothesis",
            "hypothesis_proposition": "The reported pattern is straightforward.",
            "evidence_fact_ids": ["F1"],
        }

    monkeypatch.setattr(PatternFirstOpenAIConversationModel, "_conversation_call_json", fake_call)
    model = AdaptivePatternFirstOpenAIConversationModel(api_key="test")

    result = model.plan_turn(
        current_episode_id=None,
        episodes=(),
        operative_facts=(),
        recent_conversation=(),
        boundary_answered=False,
    )

    assert len(calls) == 1
    instructions = str(calls[0]["instructions"])
    assert "NO fixed episode quota" in instructions
    assert "never a mandatory ritual" in instructions
    assert "If the answer would not materially change" in instructions
    assert "DO NOT ask the question" in instructions
    assert "Do not manufacture depth" in instructions
    assert "explanatory novelty is NOT required" in instructions
    assert result.move_type == "surface_hypothesis"


class OneEpisodeRecurringModel:
    configured = True

    def extract_turn(self, **kwargs) -> TurnExtraction:
        return TurnExtraction(
            episode_summary="Ordinary hunger example",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief",
                    proposition="I tend to get hungry after not eating for a while.",
                ),
            ),
        )

    def plan_turn(self, **kwargs) -> ConversationMove:
        fact_id = kwargs["operative_facts"][0].fact_id
        return ConversationMove(
            reply="A tentative pattern is that you tend to get hungry after not eating for a while. Does that fit?",
            move_type="surface_hypothesis",
            hypothesis_proposition="I tend to get hungry after not eating for a while.",
            evidence_fact_ids=(fact_id,),
        )


def test_one_grounded_episode_plus_recurring_self_report_can_surface_pattern() -> None:
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=OneEpisodeRecurringModel(),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True

    result = session.turn("I tend to get hungry after not eating for a while.")

    assert result["pattern_active"] is True
    assert result["episode_count"] == 1
    assert session.boundary_answered is False
    assert session.core.active_proposal_id is not None


class EpisodeOnlyRestatementModel:
    configured = True

    def extract_turn(self, **kwargs) -> TurnExtraction:
        return TurnExtraction(
            episode_summary="Single event",
            facts=(
                HiddenFactCandidate(
                    assertion_type="positive_occurrence",
                    proposition="Today I felt hungry after not eating.",
                ),
            ),
        )

    def plan_turn(self, **kwargs) -> ConversationMove:
        fact_id = kwargs["operative_facts"][0].fact_id
        return ConversationMove(
            reply="Does this describe your general pattern?",
            move_type="surface_hypothesis",
            hypothesis_proposition="Today I felt hungry after not eating.",
            evidence_fact_ids=(fact_id,),
        )


def test_single_occurrence_is_not_silently_promoted_to_person_level_pattern() -> None:
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=EpisodeOnlyRestatementModel(),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True

    result = session.turn("Today I felt hungry after not eating.")

    assert result["pattern_active"] is False
    assert result["move_type"] == "follow_up"
    assert session.core.active_proposal_id is None


class UnknownDoesNotBlockModel:
    configured = True

    def __init__(self) -> None:
        self.call_count = 0

    def extract_turn(self, **kwargs) -> TurnExtraction:
        self.call_count += 1
        if self.call_count == 1:
            return TurnExtraction(
                episode_summary="Recurring pattern anchor",
                facts=(
                    HiddenFactCandidate(
                        assertion_type="reported_appraisal_or_belief",
                        proposition="I tend to get hungry after long gaps without food.",
                    ),
                ),
            )
        return TurnExtraction(episode_summary="No new fact")

    def plan_turn(self, **kwargs) -> ConversationMove:
        if self.call_count == 1:
            return ConversationMove(
                reply="Can you think of an exception?",
                move_type="boundary_question",
            )
        fact_id = kwargs["operative_facts"][0].fact_id
        return ConversationMove(
            reply="You are not sure about exceptions, but the narrow recurring pattern is already clear. Does this fit?",
            move_type="surface_hypothesis",
            hypothesis_proposition="I tend to get hungry after long gaps without food.",
            evidence_fact_ids=(fact_id,),
        )


def test_unknown_counterexample_does_not_force_more_interrogation() -> None:
    model = UnknownDoesNotBlockModel()
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=model,  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True

    first = session.turn("I tend to get hungry after long gaps without food.")
    assert first["move_type"] == "boundary_question"
    assert session.pending_boundary_question is True

    second = session.turn("I don't know.")

    assert second["pattern_active"] is True
    assert second["move_type"] == "surface_hypothesis"
    assert session.core.active_proposal_id is not None


class RejectionReasoningModel:
    configured = True

    def plan_turn(self, **kwargs) -> ConversationMove:
        return ConversationMove(
            reply="I may have added a distinction the conversation did not support. The narrower pattern may be enough.",
            move_type="follow_up",
        )


def test_rejected_synthesis_uses_model_led_diagnosis() -> None:
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=RejectionReasoningModel(),  # type: ignore[arg-type]
    )
    session.core.active_proposal_id = "PROP-TEST"

    result = session.disagree_with_pattern()

    assert result["pattern_refining"] is True
    assert result["move_type"] == "follow_up"
    assert "distinction" in result["reply"]
    assert session.core.active_proposal_id == "PROP-TEST"
