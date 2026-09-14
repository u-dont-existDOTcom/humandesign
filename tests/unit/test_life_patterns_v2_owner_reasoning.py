from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_conversation import ConversationMove, TurnExtraction
from hdmatch.api.life_patterns_v2_owner_pattern_first import PatternFirstOpenAIConversationModel
from hdmatch.api.life_patterns_v2_owner_reasoning import (
    ReasoningGuardedPatternFirstOpenAIConversationModel,
    ReasoningRefinablePatternSession,
)


def test_unsupported_comparison_is_intercepted(monkeypatch) -> None:
    calls: list[str] = []

    def fake_call(self, **kwargs):
        schema_name = kwargs["schema_name"]
        calls.append(schema_name)
        if schema_name == "life_patterns_conversation_move_v1":
            return {
                "reply": "A tentative synthesis.",
                "move_type": "surface_hypothesis",
                "hypothesis_proposition": "Factor A matters less than factor B.",
                "evidence_fact_ids": ["F1", "F2"],
            }
        return {
            "acceptable": False,
            "issue_type": "unsupported_comparison",
            "repair_question": "When B is similar, does A still change the response?",
            "internal_reason": (
                "The record lists both factors but does not compare their importance."
            ),
        }

    monkeypatch.setattr(PatternFirstOpenAIConversationModel, "_conversation_call_json", fake_call)
    model = ReasoningGuardedPatternFirstOpenAIConversationModel(api_key="test")

    result = model._conversation_call_json(
        instructions="interview",
        payload={
            "episodes": [],
            "operative_facts": [],
            "recent_conversation": [],
            "boundary_answered": True,
        },
        schema={},
        effort="medium",
        max_output_tokens=500,
        schema_name="life_patterns_conversation_move_v1",
    )

    assert calls == ["life_patterns_conversation_move_v1", "life_patterns_hypothesis_audit_v1"]
    assert result["move_type"] == "follow_up"
    assert result["hypothesis_proposition"] is None
    assert result["reply"] == "When B is similar, does A still change the response?"


def test_supported_synthesis_survives_audit(monkeypatch) -> None:
    candidate = {
        "reply": "A tentative synthesis.",
        "move_type": "surface_hypothesis",
        "hypothesis_proposition": "The response changes with explicitly reported context.",
        "evidence_fact_ids": ["F1", "F2"],
    }

    def fake_call(self, **kwargs):
        if kwargs["schema_name"] == "life_patterns_conversation_move_v1":
            return candidate
        return {
            "acceptable": True,
            "issue_type": "none",
            "repair_question": None,
            "internal_reason": "Every material clause is directly supported.",
        }

    monkeypatch.setattr(PatternFirstOpenAIConversationModel, "_conversation_call_json", fake_call)
    model = ReasoningGuardedPatternFirstOpenAIConversationModel(api_key="test")

    result = model._conversation_call_json(
        instructions="interview",
        payload={
            "episodes": [],
            "operative_facts": [],
            "recent_conversation": [],
            "boundary_answered": True,
        },
        schema={},
        effort="medium",
        max_output_tokens=500,
        schema_name="life_patterns_conversation_move_v1",
    )

    assert result == candidate


class RejectionReasoningModel:
    configured = True

    def plan_turn(self, **kwargs) -> ConversationMove:
        return ConversationMove(
            reply=(
                "I may have ranked two factors the examples never compare"
                "d. Can we test that directly?"
            ),
            move_type="follow_up",
        )


def test_rejected_synthesis_uses_model_led_diagnosis() -> None:
    session = ReasoningRefinablePatternSession(
        session_id="OWNER-TEST",
        model=RejectionReasoningModel(),  # type: ignore[arg-type]
    )
    session.core.active_proposal_id = "PROP-TEST"

    result = session.disagree_with_pattern()

    assert result["pattern_refining"] is True
    assert result["move_type"] == "follow_up"
    assert "ranked two factors" in result["reply"]
    assert session.core.active_proposal_id == "PROP-TEST"


class BoundaryAwareModel:
    configured = True

    def __init__(self) -> None:
        self.boundary_flags: list[bool] = []

    def boundary_answer_resolved(self, **kwargs) -> bool:
        return False

    def extract_turn(self, **kwargs) -> TurnExtraction:
        return TurnExtraction(episode_summary="Current situation")

    def plan_turn(self, **kwargs) -> ConversationMove:
        self.boundary_flags.append(bool(kwargs["boundary_answered"]))
        return ConversationMove(
            reply="That adds another possible factor, but it does not yet answer the contrast.",
            move_type="follow_up",
        )


def test_reply_does_not_open_synthesis_gate_when_boundary_is_not_semantically_resolved() -> None:
    model = BoundaryAwareModel()
    session = ReasoningRefinablePatternSession(
        session_id="OWNER-TEST",
        model=model,  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True
    session.conversation.append(
        {
            "turn_id": "TURN-QUESTION",
            "role": "assistant",
            "text": "Can you give a case that breaks the apparent contrast?",
        }
    )
    session.pending_boundary_question = True

    result = session.turn("There may also be another state-dependent factor.")

    assert model.boundary_flags == [False]
    assert session.boundary_answered is False
    assert result["move_type"] == "follow_up"
    assert result["pattern_active"] is False
