from __future__ import annotations

from hdmatch.api.life_patterns_v2_owner_recoverability import RecoverabilityCoverageOpenAIModel
from hdmatch.api.life_patterns_v2_owner_scope import (
    GLOBAL_LABEL_SCOPE_INSTRUCTIONS,
    ScopeAwareRecoverabilityOpenAIModel,
    create_life_patterns_v2_owner_scope_app,
)


def _fake_parent_call(calls: list[dict[str, object]]):
    def fake(self, **kwargs):
        calls.append(kwargs)
        schema_name = kwargs["schema_name"]
        if schema_name == "life_patterns_pattern_specificity_v1":
            return {
                "decision": "continue",
                "reply": "When you say balanced in general, does that apply beyond mood too?",
                "internal_reason": "The label is global while the current evidence is narrower.",
            }
        return {
            "reply": "When you say balanced in general, does that apply beyond mood too?",
            "move_type": "follow_up",
            "hypothesis_proposition": None,
            "evidence_fact_ids": [],
        }

    return fake


def test_global_label_scope_guard_reaches_normal_planner(monkeypatch) -> None:
    calls: list[dict[str, object]] = []
    monkeypatch.setattr(
        RecoverabilityCoverageOpenAIModel,
        "_conversation_call_json",
        _fake_parent_call(calls),
    )
    model = ScopeAwareRecoverabilityOpenAIModel(api_key="test")

    result = model.plan_turn(
        current_episode_id=None,
        episodes=(),
        operative_facts=(),
        recent_conversation=(
            {"turn_id": "T1", "role": "user", "text": "I'm balanced in general."},
            {"turn_id": "T2", "role": "user", "text": "I don't have many moods through the day."},
        ),
        boundary_answered=False,
    )

    assert result.move_type == "follow_up"
    instructions = str(calls[0]["instructions"])
    assert "GLOBAL-LABEL SCOPE" in instructions
    assert "must not be silently reduced to the first subdomain" in instructions
    assert "work/rest or work-life balance" in instructions
    assert "practical versus spiritual priorities" in instructions
    assert "mostly one domain" in instructions


def test_global_label_scope_guard_reaches_refinement_planner(monkeypatch) -> None:
    calls: list[dict[str, object]] = []
    monkeypatch.setattr(
        RecoverabilityCoverageOpenAIModel,
        "_conversation_call_json",
        _fake_parent_call(calls),
    )
    model = ScopeAwareRecoverabilityOpenAIModel(api_key="test")

    result = model.plan_refinement_turn(
        current_proposition="The participant is emotionally steady across the day.",
        refinement_mode="continue",
        current_episode_id=None,
        episodes=(),
        operative_facts=(),
        recent_conversation=(
            {
                "turn_id": "T3",
                "role": "user",
                "text": "That fits, but you only checked my mood rather than whether balance applies elsewhere.",
            },
        ),
    )

    assert result.move_type == "follow_up"
    instructions = str(calls[0]["instructions"])
    assert "GLOBAL-LABEL SCOPE" in instructions
    assert "prioritize this scope question over another observer-view question" in instructions


def test_global_label_scope_guard_reaches_initial_focus_triage(monkeypatch) -> None:
    calls: list[dict[str, object]] = []
    monkeypatch.setattr(
        RecoverabilityCoverageOpenAIModel,
        "_conversation_call_json",
        _fake_parent_call(calls),
    )
    model = ScopeAwareRecoverabilityOpenAIModel(api_key="test")

    decision, _ = model.assess_pattern_focus(
        pattern_text="I'm pretty balanced in general.",
        recent_conversation=(),
    )

    assert decision == "continue"
    assert "GLOBAL-LABEL SCOPE" in str(calls[0]["instructions"])


def test_scope_app_marks_guard_active() -> None:
    app = create_life_patterns_v2_owner_scope_app()
    assert app.state.global_label_scope_guard is True
    assert GLOBAL_LABEL_SCOPE_INSTRUCTIONS.startswith("GLOBAL-LABEL SCOPE")
