from __future__ import annotations

from typing import Any, Literal

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

    def __init__(self, *, mode: Literal["topic", "direct", "inference"] = "topic") -> None:
        self.mode = mode

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
        if self.mode == "topic":
            return TopicCompleteMove(
                reply="That gives me enough information for this area; we can move on."
            )
        fact = kwargs["operative_facts"][0]
        if self.mode == "direct":
            return ConversationMove(
                reply="That gives me enough information for this area; we can move on.",
                move_type="surface_hypothesis",
                hypothesis_proposition="Quiet helps me recover.",
                evidence_fact_ids=(fact.fact_id,),
            )
        return ConversationMove(
            reply="A tentative pattern is that you rely on quiet more as depletion rises. Does that fit?",
            move_type="surface_hypothesis",
            hypothesis_proposition=(
                "The participant appears to rely increasingly on quiet as depletion rises."
            ),
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


def test_topic_complete_is_for_covered_area_without_person_specific_pattern() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-TOPIC",
        model=FakeNaturalModel(mode="topic"),  # type: ignore[arg-type]
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
    assert not session.core.record.pattern_proposals
    assert not session.core.record.participant_adjudications

    snapshot = session.recovery_snapshot()
    restored = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-TOPIC",
        model=FakeNaturalModel(mode="topic"),  # type: ignore[arg-type]
    )
    restored.restore_recovery_snapshot(snapshot)
    assert restored.recovery_status()["workflow_phase"] == "topic_complete"


def test_direct_participant_pattern_records_without_redundant_confirmation() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-DIRECT",
        model=FakeNaturalModel(mode="direct"),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True
    session.coverage_report = lambda: _coverage()  # type: ignore[method-assign]

    result = session.turn("Quiet helps me recover.")

    assert result["direct_pattern_recorded"] is True
    assert result["move_type"] == "direct_pattern"
    assert result["topic_complete"] is True
    assert result["status"] == "accepted"
    assert result["wording"] == "Quiet helps me recover."
    assert result["pattern_active"] is False
    assert session._draft_move is None
    assert session.core.active_proposal_id is None
    assert len(session.core.record.pattern_proposals) == 1
    assert len(session.core.record.participant_adjudications) == 1
    adjudication = session.core.record.participant_adjudications[0]
    assert adjudication.decision == "accept"
    assert adjudication.participant_approved_wording == "Quiet helps me recover."
    assert adjudication.participant_response_provenance_ids == (
        session.core.record.episode_facts[0].source_provenance_ids[0],
    )
    assert all(
        "participant-pattern-decision" not in source.locator
        for source in session.core.record.source_provenance
    )
    assert session.recovery_status()["workflow_phase"] == "topic_complete"


def test_model_paraphrase_or_inference_still_requires_participant_judgment() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-INFERENCE",
        model=FakeNaturalModel(mode="inference"),  # type: ignore[arg-type]
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
    assert "direct_pattern_recorded" not in surfaced
    assert session._draft_move is not None
    assert calls == 1

    result = session.adjudicate(PatternAdjudicationRequest(decision="accept"))

    assert result["status"] == "accepted"
    assert result["coverage"]["complete_domain_count"] == 1
    assert calls == 1
    assert session.core.active_proposal_id is None
    assert session._draft_move is None


def test_direct_report_detection_fails_closed_if_wording_is_not_verbatim() -> None:
    session = NaturalFlowRecoverabilitySession(
        session_id="OWNER-NATURAL-NONVERBATIM",
        model=FakeNaturalModel(mode="inference"),  # type: ignore[arg-type]
    )
    session.pattern_focus_established = True
    session.coverage_report = lambda: _coverage()  # type: ignore[method-assign]

    result = session.turn("Quiet helps me recover.")

    assert result["pattern_active"] is True
    assert len(session.core.record.participant_adjudications) == 0


def test_progress_and_working_indicators_are_moved_to_active_end_at_runtime() -> None:
    html = NATURAL_FLOW_RECOVERABILITY_HTML

    assert "__naturalMain.appendChild(op)" in html
    assert "__naturalMain.appendChild(progress)" in html
    assert "move_type==='topic_complete'" in html
    assert "direct_pattern_recorded" in html
    assert "Thinking about that…" in html
    assert "True, but too obvious" not in html
    assert "/patterns/obvious" not in html
