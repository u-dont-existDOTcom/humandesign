from __future__ import annotations

import inspect

from hdmatch.api.life_patterns_v2_owner_app import (
    ExtractedEpisode,
    ExtractedFact,
    FactReview,
    OwnerV2Session,
    PatternAdjudicationRequest,
    PatternSuggestion,
)
from hdmatch.evaluation.participant_adjudicated_v2 import EpisodeFactV2


class FakeModel:
    def extract_episode(self, episode_text: str, episode_id: str) -> ExtractedEpisode:
        return ExtractedEpisode(
            neutral_summary=f"Summary: {episode_text[:30]}",
            facts=(
                ExtractedFact(
                    fact_id="F1",
                    assertion_type="positive_occurrence",
                    proposition=f"The participant acted in {episode_id}.",
                ),
            ),
        )

    def propose_pattern(self, facts: tuple[EpisodeFactV2, ...]) -> PatternSuggestion:
        return PatternSuggestion(
            has_candidate=True,
            proposition="I tend to pause before acting.",
            question_text="Across these examples, do you tend to pause before acting?",
            evidence_fact_ids=tuple(fact.fact_id for fact in facts),
        )


def _review_one(session: OwnerV2Session, text: str, *, correction: str | None = None) -> None:
    pending = session.add_episode(text)
    fact_id = pending.extracted.facts[0].fact_id
    if correction is None:
        reviews = (FactReview(fact_id=fact_id, action="accept"),)
    else:
        reviews = (
            FactReview(
                fact_id=fact_id,
                action="correct",
                corrected_proposition=correction,
            ),
        )
    session.review_episode(pending.episode_id, reviews)


def test_two_real_episodes_can_reach_participant_accepted_pattern() -> None:
    session = OwnerV2Session(session_id="OWNER-TEST", model=FakeModel())
    _review_one(session, "First concrete situation.")
    _review_one(session, "Second concrete situation.")

    suggestion = session.propose_pattern()
    assert suggestion.has_candidate is True
    result = session.adjudicate_pattern(PatternAdjudicationRequest(decision="accept"))

    assert result["status"] == "accepted"
    assert result["wording"] == "I tend to pause before acting."
    assert result["accepted_pattern_count"] == 1


def test_fact_correction_is_append_only_and_operative_revision_changes() -> None:
    session = OwnerV2Session(session_id="OWNER-TEST", model=FakeModel())
    pending = session.add_episode("A concrete situation.")
    base_id = pending.extracted.facts[0].fact_id
    session.review_episode(
        pending.episode_id,
        (
            FactReview(
                fact_id=base_id,
                action="correct",
                corrected_proposition="The participant waited before acting.",
            ),
        ),
    )

    assert [fact.fact_id for fact in session.record.episode_facts] == [base_id, f"{base_id}-R1"]
    assert session.record.episode_facts[1].supersedes_fact_id == base_id
    assert session.operative_facts()[0].proposition == "The participant waited before acting."


def test_not_supported_facts_do_not_enter_authoritative_record() -> None:
    session = OwnerV2Session(session_id="OWNER-TEST", model=FakeModel())
    pending = session.add_episode("A concrete situation.")
    result = session.review_episode(
        pending.episode_id,
        (FactReview(fact_id=pending.extracted.facts[0].fact_id, action="not_supported"),),
    )

    assert result["episode_saved"] is False
    assert session.record.episodes == ()
    assert session.record.episode_facts == ()


def test_revised_wording_from_other_situations_is_not_laundered_into_support() -> None:
    session = OwnerV2Session(session_id="OWNER-TEST", model=FakeModel())
    _review_one(session, "First concrete situation.")
    _review_one(session, "Second concrete situation.")
    session.propose_pattern()

    result = session.adjudicate_pattern(
        PatternAdjudicationRequest(
            decision="revise",
            revised_wording="It depends on how complex the task is.",
            grounding_source="other_situations",
        )
    )

    assert result["status"] == "unresolved"
    assert result["needs_more_evidence"] is True
    assert result["wording"] == "It depends on how complex the task is."
    assert result["accepted_pattern_count"] == 0


def test_revision_supported_by_examples_can_be_accepted() -> None:
    session = OwnerV2Session(session_id="OWNER-TEST", model=FakeModel())
    _review_one(session, "First concrete situation.")
    _review_one(session, "Second concrete situation.")
    session.propose_pattern()

    result = session.adjudicate_pattern(
        PatternAdjudicationRequest(
            decision="revise",
            revised_wording="I pause when the task is complex.",
            grounding_source="examples",
            final_decision="accept",
        )
    )

    assert result["status"] == "accepted"
    assert result["wording"] == "I pause when the task is complex."


def test_owner_app_does_not_import_historical_auto_map_authority() -> None:
    import hdmatch.api.life_patterns_v2_owner_app as module

    source = inspect.getsource(module)
    assert "life_patterns_app" not in source
    assert "OpenAILifePatternsMapper" not in source
    assert "/map" not in source


def test_html_uses_natural_language_grounding_choices() -> None:
    from hdmatch.api.life_patterns_v2_owner_ui import HTML

    assert "These examples show it" in HTML
    assert "I know it from other situations" in HTML
    assert "accept/correct/not-supported" not in HTML
    assert "birth data" in HTML.lower()
