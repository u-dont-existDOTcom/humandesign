from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_pattern_first import PatternFirstOpenAIConversationModel
from hdmatch.api.life_patterns_v2_owner_reasoning import (
    ReasoningGuardedPatternFirstOpenAIConversationModel,
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
            "internal_reason": "The record lists both factors but does not compare their importance.",
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
