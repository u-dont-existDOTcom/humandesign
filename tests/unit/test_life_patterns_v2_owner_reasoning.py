from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_pattern_first import PatternFirstOpenAIConversationModel
from hdmatch.api.life_patterns_v2_owner_reasoning import (
    ADAPTIVE_HTML,
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
            "hypothesis_proposition": "The reported pattern is straightforward and person-specific.",
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
    assert "Simple is fine; generic is not" in instructions
    assert "PERSON-SPECIFIC SIGNAL" in instructions
    assert "Explanatory novelty is NOT required" in instructions
    assert "SELF-VIEW VS OBSERVER-VIEW" in instructions
    assert "AUTOMATIC VS DELIBERATE" in instructions
    assert "CAPACITY VS PREFERRED USE" in instructions
    assert result.move_type == "surface_hypothesis"


def test_specificity_gate_contract_redirects_clearly_generic_pattern(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_call(self, **kwargs):
        calls.append(kwargs)
        return {
            "decision": "redirect_generic",
            "reply": (
                "Getting hungry after not eating is a common human regularity, so by itself it tells us "
                "little about what is distinctive about you. Is there something characteristic about how "
                "hunger works for you, or would you rather choose another pattern?"
            ),
            "internal_reason": "The statement has very high base-rate content and no individual modifier.",
        }

    monkeypatch.setattr(PatternFirstOpenAIConversationModel, "_conversation_call_json", fake_call)
    model = AdaptivePatternFirstOpenAIConversationModel(api_key="test")

    decision, reply = model.assess_pattern_focus(
        pattern_text="I get hungry every day.",
        recent_conversation=(),
    )

    assert decision == "redirect_generic"
    assert "distinctive" in reply
    assert len(calls) == 1
    assert calls[0]["schema_name"] == "life_patterns_pattern_specificity_v1"
    instructions = str(calls[0]["instructions"])
    assert "PERSON-SPECIFIC INFORMATION" in instructions
    assert "getting hungry after not eating" in instructions
    assert "Do not infer that every common emotion or behavior is generic" in instructions
    assert "If uncertain, choose continue" in instructions
    assert "broad evaluative self-label" in instructions
    assert "people who know the participant well" in instructions


def test_refinement_prompt_is_non_repetitive_target_blind_and_discriminating(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_call(self, **kwargs):
        calls.append(kwargs)
        return {
            "reply": "Do people who know you well tend to describe you as steady too, or differently?",
            "move_type": "follow_up",
            "hypothesis_proposition": None,
            "evidence_fact_ids": [],
        }

    monkeypatch.setattr(PatternFirstOpenAIConversationModel, "_conversation_call_json", fake_call)
    model = AdaptivePatternFirstOpenAIConversationModel(api_key="test")

    result = model.plan_refinement_turn(
        current_proposition="I generally experience myself as steady across the day.",
        refinement_mode="continue",
        current_episode_id=None,
        episodes=(),
        operative_facts=(),
        recent_conversation=(),
    )

    assert result.move_type == "follow_up"
    assert "people who know" in result.reply
    assert len(calls) == 1
    assert calls[0]["schema_name"] == "life_patterns_refinement_move_v1"
    instructions = str(calls[0]["instructions"])
    assert "MUST NOT repeat" in instructions
    assert "SELF-VIEW VS OBSERVER-VIEW" in instructions
    assert "AUTOMATIC VS DELIBERATE" in instructions
    assert "CAPACITY VS PREFERRED USE" in instructions
    assert "people who know you well" in instructions
    lowered = instructions.lower()
    assert "astrology" not in lowered
    assert "human design" not in lowered


class GenericThenSpecificFocusModel:
    configured = True

    def assess_pattern_focus(self, *, pattern_text: str, **kwargs) -> tuple[str, str]:
        if pattern_text == "I get hungry every day.":
            return (
                "redirect_generic",
                "That is a common human regularity, so by itself it tells us little about what is distinctive about you. Is there a characteristic variation, or choose another pattern.",
            )
        return (
            "continue",
            "Give me one real situation where that personally characteristic focus-and-hunger pattern showed up clearly.",
        )


def test_generic_pattern_is_redirected_before_any_episode_evidence() -> None:
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=GenericThenSpecificFocusModel(),  # type: ignore[arg-type]
    )

    generic = session.turn("I get hungry every day.")

    assert generic["generic_pattern_redirected"] is True
    assert generic["pattern_focus_established"] is False
    assert generic["episode_count"] == 0
    assert session.core.record.episodes == ()
    assert session.core.record.episode_facts == ()
    assert session.pattern_focus_established is False

    specific = session.turn(
        "When I get deeply focused on work, I can go many hours without feeling hungry until hunger abruptly breaks my focus."
    )

    assert specific["generic_pattern_redirected"] is False
    assert specific["pattern_focus_established"] is True
    assert specific["episode_count"] == 0
    assert "real situation" in specific["reply"]
    assert session.core.record.episodes == ()


class OneEpisodeSpecificRecurringModel:
    configured = True

    def extract_turn(self, **kwargs) -> TurnExtraction:
        return TurnExtraction(
            episode_summary="Focused work hunger interruption",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief",
                    proposition=(
                        "When I become deeply absorbed in work, I often go for many hours without "
                        "feeling hunger until it abruptly breaks my focus."
                    ),
                ),
            ),
        )

    def plan_turn(self, **kwargs) -> ConversationMove:
        fact_id = kwargs["operative_facts"][0].fact_id
        proposition = (
            "When I become deeply absorbed in work, I often go for many hours without feeling "
            "hunger until it abruptly breaks my focus."
        )
        return ConversationMove(
            reply=f"A tentative pattern is: {proposition} Does that fit?",
            move_type="surface_hypothesis",
            hypothesis_proposition=proposition,
            evidence_fact_ids=(fact_id,),
        )


def test_one_grounded_episode_plus_specific_recurring_self_report_can_surface_pattern() -> None:
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=OneEpisodeSpecificRecurringModel(),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True

    result = session.turn(
        "When I become deeply absorbed in work, I often go for many hours without feeling hunger until it abruptly breaks my focus."
    )

    assert result["pattern_active"] is True
    assert result["episode_count"] == 1
    assert session.core.active_proposal_id is not None


class EpisodeOnlyRestatementModel:
    configured = True

    def extract_turn(self, **kwargs) -> TurnExtraction:
        return TurnExtraction(
            episode_summary="Single event",
            facts=(
                HiddenFactCandidate(
                    assertion_type="positive_occurrence",
                    proposition="Today I lost track of hunger while focused on work.",
                ),
            ),
        )

    def plan_turn(self, **kwargs) -> ConversationMove:
        fact_id = kwargs["operative_facts"][0].fact_id
        return ConversationMove(
            reply="Does this describe your general pattern?",
            move_type="surface_hypothesis",
            hypothesis_proposition="Today I lost track of hunger while focused on work.",
            evidence_fact_ids=(fact_id,),
        )


def test_single_occurrence_is_not_silently_promoted_to_person_level_pattern() -> None:
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=EpisodeOnlyRestatementModel(),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True

    result = session.turn("Today I lost track of hunger while focused on work.")

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
                        proposition="When intensely focused, I often lose awareness of hunger for hours.",
                    ),
                ),
            )
        return TurnExtraction(episode_summary="No new fact")

    def plan_turn(self, **kwargs) -> ConversationMove:
        if self.call_count == 1:
            return ConversationMove(
                reply="Can you think of an exception where intense focus did not have that effect?",
                move_type="boundary_question",
            )
        fact_id = kwargs["operative_facts"][0].fact_id
        return ConversationMove(
            reply="You are not sure about exceptions, but the narrow recurring pattern is already clear. Does this fit?",
            move_type="surface_hypothesis",
            hypothesis_proposition="When intensely focused, I often lose awareness of hunger for hours.",
            evidence_fact_ids=(fact_id,),
        )


def test_unknown_counterexample_does_not_force_more_interrogation() -> None:
    model = UnknownDoesNotBlockModel()
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=model,  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True

    first = session.turn("When intensely focused, I often lose awareness of hunger for hours.")
    assert first["move_type"] == "boundary_question"
    assert session.pending_boundary_question is True

    second = session.turn("I don't know.")

    assert second["pattern_active"] is True
    assert second["move_type"] == "surface_hypothesis"
    assert session.core.active_proposal_id is not None


class KeepTryingRefinementModel:
    configured = True

    def plan_refinement_turn(self, **kwargs) -> ConversationMove:
        assert kwargs["refinement_mode"] == "continue"
        return ConversationMove(
            reply="Do people who know you well tend to describe you as steady too, or differently?",
            move_type="follow_up",
        )


def test_keep_trying_asks_for_new_information_instead_of_repeating_synthesis() -> None:
    session = AdaptiveRefinablePatternSession(
        session_id="OWNER-TEST",
        model=KeepTryingRefinementModel(),  # type: ignore[arg-type]
    )
    old = "A tentative pattern is that you generally experience yourself as steady across the day."
    session.core.active_proposal_id = "PROP-TEST"
    session.conversation.append({"turn_id": "TURN-OLD", "role": "assistant", "text": old})

    result = session.continue_pattern()

    assert result["move_type"] == "follow_up"
    assert result["reply"] != old
    assert "people who know" in result["reply"]
    assert session.conversation[-2]["role"] == "user"
    assert session.conversation[-2]["text"] == "Keep trying to pin it down."
    assert "bubble('user','Keep trying to pin it down.')" in ADAPTIVE_HTML


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
