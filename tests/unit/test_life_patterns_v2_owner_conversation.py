from __future__ import annotations

import inspect

from hdmatch.api.life_patterns_v2_owner_app import (
    ExtractedEpisode,
    PatternAdjudicationRequest,
    PatternSuggestion,
)
from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    ConversationalOwnerSession,
    HiddenFactCandidate,
    HiddenFactCorrection,
    TurnExtraction,
)
from hdmatch.evaluation.participant_adjudicated_v2 import EpisodeFactV2


class ScriptedConversationModel:
    configured = True

    def __init__(self, *, moves: list[str], correction_on_turn: int | None = None) -> None:
        self.moves = moves
        self.turn_index = 0
        self.correction_on_turn = correction_on_turn

    def extract_episode(self, episode_text: str, episode_id: str) -> ExtractedEpisode:
        raise AssertionError("legacy surfaced-fact path must not be used")

    def propose_pattern(self, facts: tuple[EpisodeFactV2, ...]) -> PatternSuggestion:
        raise AssertionError("legacy pattern proposer must not be used")

    def extract_turn(
        self,
        *,
        message: str,
        current_episode_id: str | None,
        operative_facts: tuple[EpisodeFactV2, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> TurnExtraction:
        self.turn_index += 1
        if self.correction_on_turn == self.turn_index and operative_facts:
            return TurnExtraction(
                episode_summary="Current situation",
                corrections=(
                    HiddenFactCorrection(
                        fact_id=operative_facts[0].fact_id,
                        corrected_proposition="The participant paused before deciding.",
                    ),
                ),
            )
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
                reply="What changed your interpretation at that point?",
                move_type="follow_up",
            )
        if move == "request_contrast":
            return ConversationMove(
                reply="Give me a contrasting situation where you handled the uncertainty differently.",
                move_type="request_contrast",
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
            evidence = tuple(by_episode.values())
            return ConversationMove(
                reply=(
                    "Across the situations, I wonder if the difference is not complexity itself "
                    "but whether you think more information can resolve the uncertainty. Does that fit?"
                ),
                move_type="surface_hypothesis",
                hypothesis_proposition=(
                    "I seek structure when I expect more information can resolve the uncertainty."
                ),
                evidence_fact_ids=evidence,
            )
        raise AssertionError(move)


def test_first_turn_creates_hidden_fact_and_asks_one_information_gain_followup() -> None:
    model = ScriptedConversationModel(moves=["follow_up"])
    session = ConversationalOwnerSession(session_id="OWNER-TEST", model=model)

    result = session.turn("I had to choose whether to take on a complicated project.")

    assert result["move_type"] == "follow_up"
    assert "What changed your interpretation" in result["reply"]
    assert len(session.core.record.episode_facts) == 1
    assert len(session.core.record.episodes) == 1
    assert "supported" not in result["reply"].lower()
    assert "fact" not in result["reply"].lower()


def test_conversation_requests_contrast_without_surfacing_fact_checklist() -> None:
    model = ScriptedConversationModel(moves=["request_contrast"])
    session = ConversationalOwnerSession(session_id="OWNER-TEST", model=model)

    result = session.turn("I made a checklist before I started.")

    assert result["move_type"] == "request_contrast"
    assert session.awaiting_new_episode is True
    assert session.current_episode_id is None
    assert result["pattern_active"] is False


def test_hidden_participant_correction_is_append_only() -> None:
    model = ScriptedConversationModel(
        moves=["follow_up", "follow_up"],
        correction_on_turn=2,
    )
    session = ConversationalOwnerSession(session_id="OWNER-TEST", model=model)
    session.turn("I acted immediately.")
    first = session.core.record.episode_facts[0]

    session.turn("Actually, I paused before deciding.")

    assert len(session.core.record.episode_facts) == 2
    revised = session.core.record.episode_facts[-1]
    assert revised.supersedes_fact_id == first.fact_id
    assert revised.fact_lineage_id == first.fact_lineage_id
    assert revised.revision_index == 1
    assert revised.proposition == "The participant paused before deciding."
    assert session.core.operative_facts()[0].fact_id == revised.fact_id


def test_surface_hypothesis_is_withheld_until_boundary_check_is_answered() -> None:
    model = ScriptedConversationModel(moves=["request_contrast", "surface_hypothesis"])
    session = ConversationalOwnerSession(session_id="OWNER-TEST", model=model)
    session.turn("In one project I wrote a plan first.")

    result = session.turn("In another project I started immediately.")

    assert result["pattern_active"] is False
    assert result["move_type"] == "boundary_question"
    assert "Before I turn that into a pattern" in result["reply"]
    assert session.pending_boundary_question is True


def test_cross_episode_hypothesis_after_boundary_check_uses_grounded_facts() -> None:
    model = ScriptedConversationModel(
        moves=["request_contrast", "boundary_question", "surface_hypothesis"]
    )
    session = ConversationalOwnerSession(session_id="OWNER-TEST", model=model)

    session.turn("For a complicated project I mapped out the steps.")
    second = session.turn("For a simple project I started immediately.")
    assert second["move_type"] == "boundary_question"
    assert session.pending_boundary_question is True

    result = session.turn("The contrast breaks down when I think more information will not help.")

    assert result["move_type"] == "surface_hypothesis"
    assert result["pattern_active"] is True
    assert session.core.active_proposal_id is not None
    proposal = session.core.record.pattern_proposals[-1]
    links = [
        link
        for link in session.core.record.pattern_evidence_links
        if link.proposal_id == proposal.proposal_id
    ]
    assert len({link.episode_id for link in links}) >= 2
    assert all(link.acquisition_phase == "pre_first_proposal" for link in links)


def test_explicit_participant_adjudication_still_controls_person_level_pattern() -> None:
    model = ScriptedConversationModel(
        moves=["request_contrast", "boundary_question", "surface_hypothesis"]
    )
    session = ConversationalOwnerSession(session_id="OWNER-TEST", model=model)
    session.turn("For a complicated project I mapped out the steps.")
    session.turn("For a simple project I started immediately.")
    session.turn("The contrast breaks down when more information would not help.")

    result = session.adjudicate(PatternAdjudicationRequest(decision="accept"))

    assert result["status"] == "accepted"
    assert result["accepted_pattern_count"] == 1
    assert result["wording"] == (
        "I seek structure when I expect more information can resolve the uncertainty."
    )


def test_ui_keeps_ledger_hidden_and_removes_annotation_workflow() -> None:
    from hdmatch.api.life_patterns_v2_owner_conversation_ui import HTML

    assert "hidden evidence ledger" in HTML
    assert "Here’s what I think happened" not in HTML
    assert "Yes, that is supported" not in HTML
    assert "Save my review" not in HTML
    assert "keep/edit/reject" not in HTML
    assert "If it mostly paraphrases you, this version fails too." in HTML


def test_conversation_module_has_no_historical_map_or_target_theory_language() -> None:
    import hdmatch.api.life_patterns_v2_owner_conversation as module

    source = inspect.getsource(module)
    assert "OpenAILifePatternsMapper" not in source
    assert '"/map"' not in source
    assert "Human Design" not in source
    assert "astrology" not in source
    assert "birth" not in source.lower()
    assert "chart" not in source.lower()
