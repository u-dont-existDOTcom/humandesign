from __future__ import annotations

from typing import Any

from hdmatch.api.life_patterns_v2_owner_continuous_flow import (
    ContinuousAdvanceRequest,
    ContinuousFlowRecoverabilityOpenAIModel,
    _advance_existing_session,
)
from hdmatch.api.life_patterns_v2_owner_continuous_flow_ui import (
    CONTINUOUS_FLOW_RECOVERABILITY_HTML,
)
from hdmatch.api.life_patterns_v2_owner_conversation import ConversationMove, TurnExtraction
from hdmatch.api.life_patterns_v2_owner_natural_flow import NaturalFlowRecoverabilitySession
from hdmatch.api.life_patterns_v2_owner_recoverability import RECOVERABILITY_DOMAINS


class FakeAdvanceModel:
    configured = True

    def plan_continuation_question(self, **kwargs: Any) -> dict[str, Any]:
        assert kwargs["answer_memory"] == ["I already answered the old topic."]
        assert kwargs["recent_conversation"][-1]["text"] == "Previous answer"
        return {
            "primary_domain_id": kwargs["open_domains"][0].domain_id,
            "opening": "What happens when a method works for others but not for you?",
            "question_admission": {
                "stage": "cross_area_pre_send",
                "decision": "replace",
                "candidate_question": "Do you follow established methods?",
                "final_question": "What happens when a method works for others but not for you?",
                "missing_discriminator": "adaptation threshold",
                "decision_impact": "Different answers separate adoption from replacement.",
                "redundancy_check": "The prior answer did not address this contrast.",
            },
        }


class MinimalSessionModel:
    configured = True

    def extract_turn(self, **_kwargs: Any) -> TurnExtraction:
        return TurnExtraction(episode_summary="x", facts=(), corrections=())


def test_advance_keeps_same_session_and_appends_one_admitted_question() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-CONTINUOUS",
        model=MinimalSessionModel(),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True
    session.conversation.append(
        {"turn_id": "TURN-OLD", "role": "user", "text": "Previous answer"}
    )
    request = ContinuousAdvanceRequest(
        aggregate_coverage=[
            {
                "domain_id": "recurring_mystery",
                "status": "sufficient",
                "reason": "Already covered.",
            }
        ],
        completed_results=[],
        answer_memory=["I already answered the old topic."],
    )

    result = _advance_existing_session(
        session=session,
        model=FakeAdvanceModel(),  # type: ignore[arg-type]
        request=request,
    )

    assert result["session_id"] == "OWNER-CONTINUOUS"
    assert result["complete"] is False
    assert result["opening"] == "What happens when a method works for others but not for you?"
    assert result["question_admission"]["missing_discriminator"] == "adaptation threshold"
    assert session.conversation[-1]["role"] == "assistant"
    assert session.conversation[-1]["text"] == result["opening"]
    assert session.current_episode_id is None
    assert session.awaiting_new_episode is True


def test_advance_reports_complete_without_creating_a_new_session() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-COMPLETE",
        model=MinimalSessionModel(),  # type: ignore[arg-type]
    )
    coverage = [
        {"domain_id": domain.domain_id, "status": "sufficient", "reason": "covered"}
        for domain in RECOVERABILITY_DOMAINS
    ]
    result = _advance_existing_session(
        session=session,
        model=FakeAdvanceModel(),  # type: ignore[arg-type]
        request=ContinuousAdvanceRequest(aggregate_coverage=coverage),
    )
    assert result == {
        "session_id": "OWNER-COMPLETE",
        "complete": True,
        "opening": None,
        "primary_domain_id": None,
    }


def test_in_thread_admission_can_replace_and_expose_audit_reason(monkeypatch) -> None:
    model = ContinuousFlowRecoverabilityOpenAIModel(api_key="test")

    def fake_call(**kwargs: Any) -> dict[str, Any]:
        assert kwargs["schema_name"] == "life_patterns_question_admission_v1"
        return {
            "decision": "replace",
            "reply": "What concrete sign tells you the situation has crossed your threshold?",
            "move_type": "follow_up",
            "missing_discriminator": "the participant's actual threshold cue",
            "decision_impact": "The answer distinguishes immediate cues from later reasoning.",
            "redundancy_check": "No earlier answer identified the cue.",
        }

    monkeypatch.setattr(model, "_conversation_call_json", fake_call)
    result = model._admit_in_thread_question(
        candidate=ConversationMove(
            reply="Do you generally try to make good decisions?",
            move_type="follow_up",
        ),
        operative_facts=(),
        recent_conversation=(),
    )
    assert result.move_type == "follow_up"
    assert result.reply.startswith("What concrete sign")
    admission = model.pop_question_admission(result.reply)
    assert admission is not None
    assert admission["decision"] == "replace"
    assert admission["candidate_question"] == "Do you generally try to make good decisions?"
    assert admission["missing_discriminator"] == "the participant's actual threshold cue"
    assert model.pop_question_admission(result.reply) is None


def test_continuous_ui_auto_advances_and_simplifies_synthesis_controls() -> None:
    html = CONTINUOUS_FLOW_RECOVERABILITY_HTML
    assert "/advance" in html
    assert "await advanceInterview()" in html
    assert "answer_memory" in html
    assert "question_admission_log" in html
    assert "rememberQuestionAdmission" in html
    assert "Finish for now" in html
    assert "position='fixed'" in html
    assert "Write exact wording to record" in html
    assert "explainRevision.classList.add('hidden')" in html
    assert "continueButton.classList.add('hidden')" in html
    assert "The normal textbox already handles" in html
