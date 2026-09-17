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
    session.conversation.append({"turn_id": "TURN-OLD", "role": "user", "text": "Previous answer"})
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


def test_continuous_ui_uses_one_renderer_and_one_labeled_text_channel() -> None:
    html = CONTINUOUS_FLOW_RECOVERABILITY_HTML
    assert 'for="message"' in html
    assert html.count("<textarea") == 1
    assert "function render()" in html
    assert "async function perform(" in html
    assert "/operations" in html
    assert "pending_operation" in html
    assert "Finish for now" in html
    assert "Resume interview" in html
    assert "Your patterns" in html
    assert "prefers-reduced-motion" in html
    assert "function resumeOrStart" not in html
    assert "editExactWording" not in html


def test_cross_area_gate_can_stop_without_closing_unmeasured_domains(monkeypatch) -> None:
    model = ContinuousFlowRecoverabilityOpenAIModel(api_key="test")
    calls = []

    def call(**kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        if kwargs["schema_name"] == "life_patterns_dynamic_coverage_next_v1":
            return {
                "primary_domain_id": "recurring_mystery",
                "opening": "Already answered?",
                "internal_reason": "draft",
            }
        assert "no_useful_question" in kwargs["schema"]["required"]
        return {
            "primary_domain_id": None,
            "opening": None,
            "no_useful_question": True,
            "changed_candidate": True,
            "missing_discriminator": "None worth asking now",
            "decision_impact": "No meaningful change",
            "redundancy_check": "Already answered",
        }

    monkeypatch.setattr(model, "_conversation_call_json", call)
    result = model.plan_continuation_question(
        open_domains=RECOVERABILITY_DOMAINS,
        aggregate_coverage=[],
        completed_results=[],
        answer_memory=[],
        recent_conversation=(),
        operative_facts=(),
    )
    assert result["no_useful_question"] is True and result["opening"] is None
    assert result["question_admission"]["decision"] == "stop"
    assert len(calls) == 2


def test_model_routes_receive_old_source_context_not_only_their_recent_tail(monkeypatch) -> None:
    from hdmatch.api.life_patterns_v2_owner_context import interview_context
    from hdmatch.api.life_patterns_v2_owner_natural_flow import NaturalFlowRecoverabilityOpenAIModel

    captured = []

    def capture(self, **kwargs: Any) -> dict[str, Any]:
        captured.append(kwargs)
        return {}

    monkeypatch.setattr(NaturalFlowRecoverabilityOpenAIModel, "_conversation_call_json", capture)
    model = ContinuousFlowRecoverabilityOpenAIModel(api_key="not-used")
    history = [{"role": "user", "text": "An older condition that still matters."}] + [
        {"role": "assistant", "text": f"Unrelated turn {i}"} for i in range(150)
    ]
    context = {
        "conversation": history,
        "participant_corrections": [{"text": "Only in unfamiliar groups."}],
        "admission_sink": [],
    }
    with interview_context(lambda: context):
        for schema_name in [
            "life_patterns_hidden_ledger_turn_v1",
            "life_patterns_refinement_move_v1",
            "life_patterns_question_admission_v1",
            "life_patterns_dynamic_coverage_next_v1",
        ]:
            model._conversation_call_json(
                instructions="Test",
                payload={"recent_conversation": history[-20:]},
                schema={},
                effort="low",
                max_output_tokens=10,
                schema_name=schema_name,
            )
    assert len(captured) == 4
    for call in captured:
        assert call["payload"]["recent_conversation"][0] == history[0]
        assert call["payload"]["shared_evidence_context"]["participant_corrections"]
        assert "admission_sink" not in call["payload"]["shared_evidence_context"]

