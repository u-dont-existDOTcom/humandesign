from datetime import UTC, date, datetime, timedelta

from hdmatch.schemas import (
    Activation,
    CandidateState,
    ChartFeatures,
    LocalDateOverlap,
    ScoredState,
)
from hdmatch.search.date_aggregator import AggregationMode, aggregate_dates
from hdmatch.util import sha256_json


def _chart(moment: datetime) -> ChartFeatures:
    activation = Activation(body="sun", side="personality", longitude=0, gate=25, line=1)
    return ChartFeatures(
        personality_utc=moment,
        design_utc=moment - timedelta(days=88),
        type="Projector",
        strategy="Wait for the Invitation",
        authority="Splenic",
        profile="1/3",
        definition="single",
        activations={"personality.sun": activation},
    )


def _state(identifier: str, day: int, score: float) -> tuple[CandidateState, ScoredState]:
    start = datetime(2024, 1, day, tzinfo=UTC)
    chart = _chart(start)
    state = CandidateState(
        state_id=identifier,
        start_utc=start,
        end_utc=start + timedelta(days=1),
        chart_features_hash=sha256_json(chart),
        chart_features=chart,
        local_date_overlaps=(LocalDateOverlap(date=date(2024, 1, day), seconds=86400),),
    )
    scored = ScoredState(
        state_id=identifier,
        net_rubric_bits=score,
        evidence_rubric_bits=max(score, 0),
        contradiction_rubric_bits=max(-score, 0),
        detailed_support=50,
        core_fit=50,
        meaningful_contradictions=0,
    )
    return state, scored


def _same_date_state(
    identifier: str,
    *,
    start: datetime,
    core_fit: float,
) -> tuple[CandidateState, ScoredState]:
    chart = _chart(start)
    state = CandidateState(
        state_id=identifier,
        start_utc=start,
        end_utc=start + timedelta(hours=12),
        chart_features_hash=sha256_json(chart),
        chart_features=chart,
        local_date_overlaps=(LocalDateOverlap(date=start.date(), seconds=12 * 60 * 60),),
    )
    score = ScoredState(
        state_id=identifier,
        net_rubric_bits=1.0,
        evidence_rubric_bits=1.0,
        contradiction_rubric_bits=0.0,
        detailed_support=50.0,
        core_fit=core_fit,
        meaningful_contradictions=0,
    )
    return state, score


def test_aggregate_dates_uses_midrank_for_exact_tie() -> None:
    first, first_score = _state("a", 1, 4)
    second, second_score = _state("b", 2, 4)
    ranked = aggregate_dates(
        [first, second], {"a": first_score, "b": second_score}, AggregationMode.BEST_STATE
    )
    assert [item.date_rank for item in ranked] == [1.5, 1.5]
    assert all(item.tied for item in ranked)


def test_date_best_state_ignores_core_fit_when_evidence_fields_tie() -> None:
    start = datetime(2024, 1, 1, tzinfo=UTC)
    first, first_score = _same_date_state(
        "a-higher-core",
        start=start,
        core_fit=90.0,
    )
    second, second_score = _same_date_state(
        "z-lower-core",
        start=start + timedelta(hours=12),
        core_fit=10.0,
    )

    original = aggregate_dates(
        (first, second),
        {first.state_id: first_score, second.state_id: second_score},
        AggregationMode.BEST_STATE,
    )
    reversed_core_fit = aggregate_dates(
        (first, second),
        {
            first.state_id: first_score.model_copy(update={"core_fit": 10.0}),
            second.state_id: second_score.model_copy(update={"core_fit": 90.0}),
        },
        AggregationMode.BEST_STATE,
    )

    assert len(original) == len(reversed_core_fit) == 1
    assert original[0].best_state.state_id == "z-lower-core"
    assert reversed_core_fit[0].best_state.state_id == "z-lower-core"
    assert original[0].date_score == reversed_core_fit[0].date_score == 1.0
    assert original[0].date_rank == reversed_core_fit[0].date_rank == 1.0
