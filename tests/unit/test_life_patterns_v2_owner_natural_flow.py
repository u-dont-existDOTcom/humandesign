from __future__ import annotations

from typing import Any

from hdmatch.api.life_patterns_v2_owner_app import PatternAdjudicationRequest
from hdmatch.api.life_patterns_v2_owner_conversation import (
    ConversationMove,
    HiddenFactCandidate,
    TurnExtraction,
)
from hdmatch.api.life_patterns_v2_owner_natural_flow import (
    NaturalFlowRecoverabilitySession,
    TopicCompleteMove,
)
from hdmatch.api.life_patterns_v2_owner_natural_flow_ui import NATURAL_FLOW_RECOVERABILITY_HTML


class FakeNaturalModel:
    configured = True

    def __init__(self, *, surface: bool = False) -> None:
        self.surface = surface

    def extract_turn(self, **_kwargs: Any) -> TurnExtraction:
        return TurnExtraction(
            episode_summary="Owner test situation",
            facts=(
                HiddenFactCandidate(
                    assertion_type="reported_appraisal_or_belief",
                    proposition="The participant reports that quiet helps them recover.",
                ),
            ),
            corrections=(),
        )

    def plan_turn(self, **kwargs: Any) -> ConversationMove | TopicCompleteMove:
        if not self.surface:
            return TopicCompleteMove(
                reply="That gives me enough information for this area; we can move on."
            )
        fact = kwargs["operative_facts"][0]
        return ConversationMove(
            reply="A tentative pattern is that quiet is an important recovery condition for you.",
            move_type="surface_hypothesis",
            hypothesis_proposition="The participant reports relying on quiet as a recovery condition.",
            evidence_fact_ids=(fact.fact_id,),
        )


def _coverage() -> dict[str, Any]:
    return {
        "blueprint_version": "life-patterns-recoverability-coverage-v2",
        "blueprint_sha256": "0" * 64,
        "assessments": [],
        "complete_domain_count": 1,
        "required_domain_count": 23,
    }


def test_topic_complete_ends_area_without_forcing_pattern() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-TOPIC",
        model=FakeNaturalModel(),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True
    calls = 0

    def coverage_report() -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return _coverage()

    session.coverage_report = coverage_report  # type: ignore[method-assign]
    result = session.turn("A quiet night's sleep usually helps me recover.")

    assert result["move_type"] == "topic_complete"
    assert result["topic_complete"] is True
    assert result["pattern_active"] is False
    assert result["coverage"]["complete_domain_count"] == 1
    assert calls == 1
    assert session._topic_complete_ready is True

    snapshot = session.recovery_snapshot()
    restored = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-TOPIC",
        model=FakeNaturalModel(),  # type: ignore[arg-type]
    )
    restored.restore_recovery_snapshot(snapshot)
    assert restored.recovery_status()["workflow_phase"] == "topic_complete"


def test_accept_reuses_cached_progress_instead_of_another_coverage_call() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-ACCEPT",
        model=FakeNaturalModel(surface=True),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True
    calls = 0

    def coverage_report() -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return _coverage()

    session.coverage_report = coverage_report  # type: ignore[method-assign]
    surfaced = session.turn("Quiet helps me recover.")
    assert surfaced["pattern_active"] is True
    assert calls == 1

    result = session.adjudicate(PatternAdjudicationRequest(decision="accept"))

    assert result["status"] == "accepted"
    assert result["coverage"]["complete_domain_count"] == 1
    assert calls == 1
    assert session.core.active_proposal_id is None
    assert session._draft_move is None


def test_progress_and_working_indicators_live_at_document_end() -> None:
    html = NATURAL_FLOW_RECOVERABILITY_HTML
    progress = html.index('id="interviewProgress"')
    working = html.index('id="operationStatus"')
    composer = html.index('id="composer"')
    continuation = html.index('id="continuation"')
    main_end = html.index("</main>")

    assert composer < continuation < working < progress < main_end
    assert "move_type==='topic_complete'" in html
    assert "Thinking about that…" in html
