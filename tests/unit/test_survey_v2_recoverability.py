from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from hdmatch.evaluation.survey_v2_recoverability import audit_perfect_match_recoverability
from hdmatch.schemas import CandidateState, LocalDateOverlap, StructuralChartFeatures


def test_every_perfect_match_reaches_unique_rank_one_via_blind_adaptive_questions() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("a", start, profile="1/3", mars=1),
        _state("b", start + timedelta(hours=1), profile="2/4", mars=1),
        _state("c", start + timedelta(hours=2), profile="2/4", mars=2),
    )
    report = audit_perfect_match_recoverability(
        states,
        {"mappings": [], "contradictions": []},
        allowed_tie_breakers=("profile", "activation:personality:mars"),
    )

    assert report.recovered_rank1_count == 3
    assert report.recovered_rank1_fraction == 1.0
    assert report.all_candidates_recover_rank1
    assert report.all_candidates_uniquely_recovered
    assert report.unresolved_candidate_count == 0
    assert report.maximum_questions_asked == 2
    assert not report.selection_uses_birth_metadata
    assert not report.selection_uses_candidate_rank


def test_audit_fails_closed_when_frozen_questions_cannot_split_a_tie() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("a", start, profile="1/3", mars=1),
        _state("b", start + timedelta(hours=1), profile="1/3", mars=1),
    )
    report = audit_perfect_match_recoverability(
        states,
        {"mappings": [], "contradictions": []},
        allowed_tie_breakers=("profile", "activation:personality:mars"),
    )

    assert not report.all_candidates_recover_rank1
    assert not report.all_candidates_uniquely_recovered
    assert report.unresolved_candidate_count == 2


def _state(
    state_id: str,
    start: datetime,
    *,
    profile: str,
    mars: int,
) -> CandidateState:
    end = start + timedelta(hours=1)
    activations = {
        "personality:moon": 1,
        "design:moon": 1,
        "personality:mercury": 1,
        "design:mercury": 1,
        "personality:venus": 1,
        "design:venus": 1,
        "personality:mars": mars,
    }
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash="0" * 64,
        chart_features=StructuralChartFeatures(
            type="generator",
            strategy="wait_to_respond",
            authority="sacral",
            profile=profile,
            definition="single",
            defined_centers=("sacral",),
            channels=("1-8",),
            activation_gates=activations,
        ),
        local_date_overlaps=(LocalDateOverlap(date=date(2000, 1, 1), seconds=3600.0),),
    )
