from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hdmatch.api.life_patterns_v2_owner_app import ExtractedEpisode, PatternSuggestion
from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    OpenAIConversationModel,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_pattern_first import (
    OPENING,
    PatternFirstConversationalOwnerSession,
    PatternFirstOpenAIConversationModel,
    TemporaryModelProviderError,
    _normalize_conversation_move_payload,
    create_life_patterns_v2_owner_pattern_first_app,
)
from hdmatch.evaluation.participant_adjudicated_v2 import EpisodeFactV2


class ScriptedModel:
    configured = True

    def __init__(self, *, moves: list[str] | None = None, fail_planner: bool = False) -> None:
        self.moves = list(moves or [])
        self.turn_index = 0
        self.fail_planner = fail_planner

    def extract_episode(self, episode_text: str, episode_id: str) -> ExtractedEpisode:
        raise AssertionError("legacy surfaced-fact path must not be used")

    def propose_pattern(self, facts: tuple[EpisodeFactV2, ...]) -> PatternSuggestion:
        raise AssertionError("legacy surfaced-pattern path must not be used")

    def extract_turn(
        self,
        *,
        message: str,
        current_episode_id: str | None,
        operative_facts: tuple[EpisodeFactV2, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> TurnExtraction:
        self.turn_index += 1
        return TurnExtraction(
            episode_summary=f"Situation {self.turn_index}",
            facts=(
                HiddenFactCandidate(
                    assertion_type="positive_occurrence",
                    proposition=f"Participant detail from turn {self.turn_index}.",
                ),
            ),
        )

    def plan_turn(
        self,
        *,
        current_episode_id: str | None,
        episodes,
        operative_facts: tuple[EpisodeFactV2, ...],
        recent_conversation: tuple[dict[str, str], ...],
        boundary_answered: bool,
    ) -> ConversationMove:
        if self.fail_planner:
            raise RuntimeError("planner failed after extraction")
        move = self.moves.pop(0)
        if move == "follow_up":
            return ConversationMove(
                reply="What changed your interpretation at that point?",
                move_type="follow_up",
            )
        if move == "request_contrast":
            return ConversationMove(
                reply="Give me a contrasting real situation.",
                move_type="request_contrast",
            )
        raise AssertionError(move)


class TemporaryFailureModel(ScriptedModel):
    def extract_turn(
        self,
        *,
        message: str,
        current_episode_id: str | None,
        operative_facts: tuple[EpisodeFactV2, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> TurnExtraction:
        raise TemporaryModelProviderError(
            "The model service is temporarily unavailable after automatic retries. "
            "Nothing from this turn was saved; please try Send again in a moment."
        )


def test_provider_overpopulation_is_normalized_before_strict_move_validation(monkeypatch) -> None:
    raw = {
        "reply": "What did you see as the actual disagreement?",
        "move_type": "follow_up",
        "hypothesis_proposition": "An unused premature hypothesis",
        "evidence_fact_ids": ["EP-1-F-1"],
    }

    def fake_provider_call(self, **kwargs):
        return raw

    monkeypatch.setattr(OpenAIConversationModel, "_conversation_call_json", fake_provider_call)
    model = PatternFirstOpenAIConversationModel(api_key="test")

    move = model.plan_turn(
        current_episode_id=None,
        episodes=(),
        operative_facts=(),
        recent_conversation=(),
        boundary_answered=False,
    )

    assert move.move_type == "follow_up"
    assert move.hypothesis_proposition is None
    assert move.evidence_fact_ids == ()


def test_transient_provider_520_retries_then_succeeds(monkeypatch) -> None:
    calls = 0
    raw = {
        "reply": "What changed after that?",
        "move_type": "follow_up",
        "hypothesis_proposition": None,
        "evidence_fact_ids": [],
    }

    def flaky_provider_call(self, **kwargs):
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("Owner Life Patterns model HTTP 520: error code: 520")
        return raw

    monkeypatch.setattr(OpenAIConversationModel, "_conversation_call_json", flaky_provider_call)
    monkeypatch.setattr(
        "hdmatch.api.life_patterns_v2_owner_pattern_first.time.sleep", lambda _seconds: None
    )
    model = PatternFirstOpenAIConversationModel(api_key="test")

    move = model.plan_turn(
        current_episode_id=None,
        episodes=(),
        operative_facts=(),
        recent_conversation=(),
        boundary_answered=False,
    )

    assert calls == 3
    assert move.move_type == "follow_up"
    assert move.reply == "What changed after that?"


def test_exhausted_temporary_provider_error_returns_503() -> None:
    client = TestClient(create_life_patterns_v2_owner_pattern_first_app(model=TemporaryFailureModel()))
    created = client.post("/api/owner-v2/conversation/sessions")
    assert created.status_code == 200
    session_id = created.json()["session_id"]

    first = client.post(
        f"/api/owner-v2/conversation/sessions/{session_id}/turns",
        json={"message": "People ask me questions but then do not actually want the answer."},
    )
    assert first.status_code == 200

    second = client.post(
        f"/api/owner-v2/conversation/sessions/{session_id}/turns",
        json={"message": "A friend asked what I thought, then rejected the answer immediately."},
    )

    assert second.status_code == 503
    assert "temporarily unavailable" in second.json()["detail"]
    assert "Nothing from this turn was saved" in second.json()["detail"]


def test_normalizer_keeps_surface_hypothesis_strict() -> None:
    raw = {
        "reply": "Maybe there is a pattern here.",
        "move_type": "surface_hypothesis",
        "hypothesis_proposition": None,
        "evidence_fact_ids": [],
    }

    normalized = _normalize_conversation_move_payload(raw)

    with pytest.raises(ValueError, match="surface_hypothesis requires hypothesis_proposition"):
        ConversationMove.model_validate(normalized)


def test_pattern_first_opening_does_not_create_fake_episode() -> None:
    model = ScriptedModel()
    session = PatternFirstConversationalOwnerSession(session_id="OWNER-TEST", model=model)

    result = session.turn("I often challenge claims that strike me as too sweeping.")

    assert "one real situation" in result["reply"].lower()
    assert result["episode_count"] == 0
    assert session.core.record.episodes == ()
    assert session.core.record.episode_facts == ()
    assert session.core.record.source_provenance == ()
    assert model.turn_index == 0
    assert "pattern you notice" in OPENING.lower()


def test_second_turn_becomes_first_concrete_anchor() -> None:
    model = ScriptedModel(moves=["follow_up"])
    session = PatternFirstConversationalOwnerSession(session_id="OWNER-TEST", model=model)
    session.turn("I often challenge claims that strike me as too sweeping.")

    result = session.turn("Yesterday in a group discussion I challenged one of those claims.")

    assert result["move_type"] == "follow_up"
    assert result["episode_count"] == 1
    assert len(session.core.record.episodes) == 1
    assert len(session.core.record.episode_facts) == 1


def test_failed_planner_rolls_back_hidden_ledger_and_conversation() -> None:
    model = ScriptedModel(fail_planner=True)
    session = PatternFirstConversationalOwnerSession(session_id="OWNER-TEST", model=model)
    session.turn("I often challenge claims that strike me as too sweeping.")

    before_conversation = list(session.conversation)
    before_record = session.core.record
    before_flags = (
        session.current_episode_id,
        session.awaiting_new_episode,
        session.pending_boundary_question,
        session.boundary_answered,
    )

    with pytest.raises(RuntimeError, match="planner failed after extraction"):
        session.turn("Yesterday in a group discussion I challenged one of those claims.")

    assert session.conversation == before_conversation
    assert session.core.record == before_record
    assert session.core.pending_episodes == {}
    assert session.core.proposal_support == {}
    assert session.core.active_proposal_id is None
    assert (
        session.current_episode_id,
        session.awaiting_new_episode,
        session.pending_boundary_question,
        session.boundary_answered,
    ) == before_flags
