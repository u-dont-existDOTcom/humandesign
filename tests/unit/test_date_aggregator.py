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


def test_aggregate_dates_uses_midrank_for_exact_tie() -> None:
    first, first_score = _state("a", 1, 4)
    second, second_score = _state("b", 2, 4)
    ranked = aggregate_dates(
        [first, second], {"a": first_score, "b": second_score}, AggregationMode.BEST_STATE
    )
    assert [item.date_rank for item in ranked] == [1.5, 1.5]
    assert all(item.tied for item in ranked)
