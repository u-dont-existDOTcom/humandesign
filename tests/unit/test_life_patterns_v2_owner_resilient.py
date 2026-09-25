from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_app import PatternAdjudicationRequest
from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    HiddenFactCorrection,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_resilient import (
    ResilientRecoverabilityCoverageSession,
    ResilientRecoverabilityOpenAIModel,
)
from hdmatch.api.life_patterns_v2_owner_resilient_ui import RESILIENT_RECOVERABILITY_HTML
from hdmatch.api.life_patterns_v2_owner_scope import ScopeAwareRecoverabilityOpenAIModel


class MinimalModel:
    configured = True


def test_refinement_can_end_with_updated_synthesis_and_sees_full_thread(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_call(self, **kwargs):
        calls.append(kwargs)
        return {
            "reply": "An updated tentative pattern is that later corrections narrow the original claim.",
            "move_type": "surface_hypothesis",
            "hypothesis_proposition": "Later corrections narrow the original claim.",
            "evidence_fact_ids": ["F-CURRENT"],
        }

    monkeypatch.setattr(ScopeAwareRecoverabilityOpenAIModel, "_conversation_call_json", fake_call)
    model = ResilientRecoverabilityOpenAIModel(api_key="test")
    conversation = tuple(
        {"turn_id": f"T{i}", "role": "user" if i % 2 else "assistant", "text": f"turn {i}"}
        for i in range(60)
    )

    move = model.plan_refinement_turn(
        current_proposition="Old draft",
        refinement_mode="answer",
        current_episode_id=None,
        episodes=(),
        operative_facts=(
            type(
                "Fact",
                (),
                {
                    "fact_id": "F-CURRENT",
                    "episode_id": "EP-1",
                    "assertion_type": "reported_appraisal_or_belief",
                    "proposition": "Later corrections narrow the original claim.",
                },
            )(),
        ),
        recent_conversation=conversation,
    )

    assert move.move_type == "surface_hypothesis"
    payload = calls[0]["payload"]
    assert isinstance(payload, dict)
    assert len(payload["recent_conversation"]) == 60
    instructions = str(calls[0]["instructions"])
    assert "participant needs an actual synthesis to judge" in instructions
    assert "Rewording a previously answered question is still repetition" in instructions


def test_tentative_synthesis_stays_ephemeral_until_adjudication_and_rebinds_to_correction() -> None:
    session = ResilientRecoverabilityCoverageSession(
        session_id="OWNER-TEST",
        model=MinimalModel(),  # type: ignore[arg-type]
    )
    first = TurnExtraction(
        episode_summary="self-description",
        facts=(
            HiddenFactCandidate(
                assertion_type="reported_appraisal_or_belief",
                proposition="The participant reports that caregiving makes them balanced.",
            ),
        ),
        corrections=(),
    )
    session._apply_extraction(
        extraction=first,
        turn_id="TURN-1",
        message="Caregiving makes me balanced.",
        start_new_episode=True,
    )
    old_fact_id = session.core.operative_facts()[0].fact_id
    initial = ConversationMove(
        reply="A tentative pattern is that caregiving makes you balanced.",
        move_type="surface_hypothesis",
        hypothesis_proposition="Caregiving makes you balanced.",
        evidence_fact_ids=(old_fact_id,),
    )
    session._create_pattern(initial)

    assert session._draft_move is not None
    assert session.core.record.pattern_proposals == ()

    correction = TurnExtraction(
        episode_summary="correction",
        facts=(),
        corrections=(
            HiddenFactCorrection(
                fact_id=old_fact_id,
                corrected_proposition=(
                    "The participant reports that caregiving focuses attention on another person but does not itself make them feel balanced."
                ),
            ),
        ),
    )
    session._apply_extraction(
        extraction=correction,
        turn_id="TURN-2",
        message="Actually it focuses me on them; it doesn't make me balanced.",
        start_new_episode=False,
    )
    current_fact_id = session.core.operative_facts()[0].fact_id
    assert current_fact_id != old_fact_id

    revised = ConversationMove(
        reply="A revised tentative pattern is that caregiving redirects your attention toward the other person and can compete with your own self-care.",
        move_type="surface_hypothesis",
        hypothesis_proposition=(
            "Caregiving redirects the participant's attention toward the other person and can compete with their own self-care."
        ),
        evidence_fact_ids=(current_fact_id,),
    )
    surfaced = session._apply_draft_move(revised)
    assert surfaced["synthesis_updated"] is True
    assert session.core.record.pattern_proposals == ()

    result = session.adjudicate(PatternAdjudicationRequest(decision="accept"))
    assert result["status"] == "accepted"
    assert result["wording"] == revised.hypothesis_proposition
    assert len(session.core.record.pattern_proposals) == 1
    assert session.core.record.participant_adjudications[0].proposal_id == (
        session.core.record.pattern_proposals[0].proposal_id
    )


def test_resilient_ui_merges_in_thread_progress_and_keeps_local_recovery_copy() -> None:
    html = RESILIENT_RECOVERABILITY_HTML
    assert "if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}" in html
    assert "lifePatternsLocalRecoveryV1" in html
    assert "Download local recovery copy" in html
    assert "not the scientific freeze" in html
