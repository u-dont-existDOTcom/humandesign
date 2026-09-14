from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import FastAPI

from hdmatch.api.life_patterns_v2_owner_app import ExtractedEpisode, PatternSuggestion
from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    ConversationTurnRequest,
    HiddenFactCandidate,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_refinement import (
    HTML,
    RefinablePatternFirstConversationalOwnerSession,
    create_life_patterns_v2_owner_refinement_app,
)
from hdmatch.evaluation.participant_adjudicated_v2 import EpisodeFactV2


class RefinementScriptedModel:
    configured = True

    def __init__(self, moves: list[str]) -> None:
        self.moves = list(moves)
        self.turn_index = 0

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
        move = self.moves.pop(0)
        if move == "follow_up":
            return ConversationMove(
                reply="What else would distinguish those cases?", move_type="follow_up"
            )
        if move == "request_contrast":
            return ConversationMove(
                reply="Give me a contrasting real situation.", move_type="request_contrast"
            )
        if move == "boundary_question":
            return ConversationMove(
                reply="What would be a case where that contrast stops holding?",
                move_type="boundary_question",
            )
        if move == "surface_hypothesis":
            by_episode: dict[str, str] = {}
            for fact in operative_facts:
                by_episode.setdefault(fact.episode_id, fact.fact_id)
            return ConversationMove(
                reply="A tentative synthesis is ready. Does that fit?",
                move_type="surface_hypothesis",
                hypothesis_proposition="The response changes with the context.",
                evidence_fact_ids=tuple(by_episode.values()),
            )
        raise AssertionError(move)


def _surface_pattern(session: RefinablePatternFirstConversationalOwnerSession) -> None:
    session.turn("I notice a recurring pattern that changes depending on the person.")
    session.turn("In one real situation I disengaged quickly.")
    session.turn("In another real situation I stayed involved despite more difficulty.")
    result = session.turn("The difference may be whether I can understand what is happening.")
    assert result["pattern_active"] is True


def _endpoint(app: FastAPI, path: str, method: str) -> Callable[..., Any]:
    for route in app.routes:
        if getattr(route, "path", None) == path and method in getattr(route, "methods", set()):
            return route.endpoint
    raise AssertionError(f"missing {method} route {path}")


def test_continue_keeps_active_proposal_open_without_terminal_adjudication() -> None:
    model = RefinementScriptedModel(
        ["request_contrast", "boundary_question", "surface_hypothesis", "follow_up"]
    )
    session = RefinablePatternFirstConversationalOwnerSession(session_id="OWNER-TEST", model=model)
    _surface_pattern(session)

    active_proposal_id = session.core.active_proposal_id
    proposal_count = len(session.core.record.pattern_proposals)
    response = session.continue_pattern()

    assert response["pattern_active"] is True
    assert response["pattern_refining"] is True
    assert response["move_type"] == "follow_up"
    assert session.core.active_proposal_id == active_proposal_id
    assert len(session.core.record.pattern_proposals) == proposal_count
    assert session.core.record.participant_adjudications == ()


def test_postproposal_answer_adds_evidence_but_cannot_auto_create_replacement_proposal() -> None:
    model = RefinementScriptedModel(
        [
            "request_contrast",
            "boundary_question",
            "surface_hypothesis",
            "surface_hypothesis",
        ]
    )
    session = RefinablePatternFirstConversationalOwnerSession(session_id="OWNER-TEST", model=model)
    _surface_pattern(session)

    active_proposal_id = session.core.active_proposal_id
    proposal_count = len(session.core.record.pattern_proposals)
    fact_count = len(session.core.record.episode_facts)
    response = session.turn("There is another distinction I have not pinned down yet.")

    assert response["pattern_refining"] is True
    assert response["move_type"] == "follow_up"
    assert session.core.active_proposal_id == active_proposal_id
    assert len(session.core.record.pattern_proposals) == proposal_count
    assert len(session.core.record.episode_facts) == fact_count + 1
    assert session.core.record.participant_adjudications == ()


def test_continue_route_preserves_same_backend_session_without_extra_http_dependency() -> None:
    model = RefinementScriptedModel(
        ["request_contrast", "boundary_question", "surface_hypothesis", "follow_up"]
    )
    app = create_life_patterns_v2_owner_refinement_app(model=model)
    create_session = _endpoint(app, "/api/owner-v2/conversation/sessions", "POST")
    interview_turn = _endpoint(
        app, "/api/owner-v2/conversation/sessions/{session_id}/turns", "POST"
    )
    continue_pattern = _endpoint(
        app, "/api/owner-v2/conversation/sessions/{session_id}/patterns/continue", "POST"
    )

    session_id = create_session().session_id
    for message in (
        "I notice a recurring pattern that changes depending on the person.",
        "In one real situation I disengaged quickly.",
        "In another real situation I stayed involved despite more difficulty.",
        "The difference may be whether I can understand what is happening.",
    ):
        payload = interview_turn(session_id, ConversationTurnRequest(message=message))
        assert isinstance(payload, dict)

    continued = continue_pattern(session_id)
    assert continued["pattern_active"] is True
    assert continued["pattern_refining"] is True


def test_ui_makes_continuation_explicit_without_target_theory_leakage() -> None:
    assert "Keep trying to pin it down" in HTML
    assert "Leave it unresolved for now" in HTML
    assert "will not contribute a settled person-level pattern to later analysis" in HTML
    assert "/patterns/continue" in HTML
    assert "astrolog" not in HTML.lower()
    assert "predictive power" not in HTML.lower()
