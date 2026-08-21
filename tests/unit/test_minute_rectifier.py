from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from fractions import Fraction

import pytest

from hdmatch.schemas import Activation, CandidateState, ChartFeatures, ScoredState
from hdmatch.search.candidate_universe import split_interval_by_local_date
from hdmatch.search.minute_rectifier import (
    identify_revealed_interval,
    rank_known_date_intervals,
)
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


def _state(
    state_id: str,
    start_utc: datetime,
    end_utc: datetime,
    *,
    timezone_name: str = "UTC",
) -> CandidateState:
    chart = _chart(start_utc)
    return CandidateState(
        state_id=state_id,
        start_utc=start_utc,
        end_utc=end_utc,
        chart_features_hash=sha256_json(chart),
        chart_features=chart,
        local_date_overlaps=split_interval_by_local_date(
            start_utc, end_utc, timezone_name
        ),
    )


def _score(state_id: str, net: float) -> ScoredState:
    return ScoredState(
        state_id=state_id,
        net_rubric_bits=net,
        evidence_rubric_bits=max(net, 0),
        contradiction_rubric_bits=max(-net, 0),
        detailed_support=50,
        core_fit=50,
        meaningful_contradictions=0,
    )


def _three_state_day() -> tuple[tuple[CandidateState, ...], dict[str, ScoredState]]:
    start = datetime(2024, 1, 2, tzinfo=UTC)
    states = (
        _state("a", start, start + timedelta(hours=8)),
        _state("b", start + timedelta(hours=8), start + timedelta(hours=16)),
        _state("c", start + timedelta(hours=16), start + timedelta(days=1)),
    )
    return states, {"a": _score("a", 3), "b": _score("b", 5), "c": _score("c", 5)}


def test_ranks_descending_with_exact_tie_groups_and_is_deterministic() -> None:
    states, scores = _three_state_day()
    first = rank_known_date_intervals(reversed(states), scores, date(2024, 1, 2), "UTC")
    second = rank_known_date_intervals(states, scores, date(2024, 1, 2), "UTC")

    assert first == second
    assert [group.net_rubric_bits for group in first.groups] == [5, 3]
    assert [record.state_id for record in first.records] == ["b", "c", "a"]
    assert first.groups[0].rank_start == 1
    assert first.groups[0].rank_end == 2
    assert first.groups[0].midrank == Fraction(3, 2)
    assert first.groups[0].tied
    assert first.groups[1].rank_start == first.groups[1].rank_end == 3
    assert first.records[0].midrank == Fraction(3, 2)


def test_near_scores_are_not_treated_as_exact_ties() -> None:
    states, scores = _three_state_day()
    scores["b"] = _score("b", 5.0)
    scores["c"] = _score("c", 5.0 + 1e-13)

    ranking = rank_known_date_intervals(states, scores, date(2024, 1, 2), "UTC")

    assert [record.state_id for record in ranking.records] == ["c", "b", "a"]
    assert all(not group.tied for group in ranking.groups)


def test_revealed_truth_uses_half_open_boundaries() -> None:
    states, scores = _three_state_day()
    ranking = rank_known_date_intervals(states, scores, date(2024, 1, 2), "UTC")
    day_start = datetime(2024, 1, 2, tzinfo=UTC)

    assert identify_revealed_interval(ranking, day_start).interval.state_id == "a"
    assert (
        identify_revealed_interval(ranking, day_start + timedelta(hours=8)).interval.state_id
        == "b"
    )
    assert (
        identify_revealed_interval(ranking, day_start + timedelta(hours=16)).interval.state_id
        == "c"
    )
    with pytest.raises(ValueError, match="outside the declared local date"):
        identify_revealed_interval(ranking, day_start + timedelta(days=1))
    with pytest.raises(ValueError, match="timezone-aware"):
        identify_revealed_interval(ranking, datetime(2024, 1, 2, 1))


def test_cross_date_intervals_keep_full_stable_width_and_exact_eligible_width() -> None:
    first = _state(
        "cross-in",
        datetime(2024, 1, 1, 22, tzinfo=UTC),
        datetime(2024, 1, 2, 6, tzinfo=UTC),
    )
    second = _state(
        "cross-out",
        datetime(2024, 1, 2, 6, tzinfo=UTC),
        datetime(2024, 1, 3, 2, tzinfo=UTC),
    )
    ranking = rank_known_date_intervals(
        [second, first],
        {"cross-in": _score("cross-in", 1), "cross-out": _score("cross-out", 2)},
        date(2024, 1, 2),
        "UTC",
    )

    by_id = {record.state_id: record for record in ranking.records}
    assert by_id["cross-in"].start_utc == datetime(2024, 1, 1, 22, tzinfo=UTC)
    assert by_id["cross-in"].end_utc == datetime(2024, 1, 2, 6, tzinfo=UTC)
    assert by_id["cross-in"].stable_width == timedelta(hours=8)
    assert by_id["cross-in"].eligible_width == timedelta(hours=6)
    assert by_id["cross-out"].stable_width == timedelta(hours=20)
    assert by_id["cross-out"].eligible_width == timedelta(hours=18)
    assert ranking.chronological_records[0].state_id == "cross-in"


@pytest.mark.parametrize(
    ("first_end", "second_start", "error"),
    [
        (timedelta(hours=11), timedelta(hours=12), "gap"),
        (timedelta(hours=13), timedelta(hours=12), "overlapping"),
    ],
)
def test_rejects_gaps_and_overlaps(
    first_end: timedelta, second_start: timedelta, error: str
) -> None:
    start = datetime(2024, 1, 2, tzinfo=UTC)
    first = _state("first", start, start + first_end)
    second = _state("second", start + second_start, start + timedelta(days=1))

    with pytest.raises(ValueError, match=error):
        rank_known_date_intervals(
            [first, second],
            {"first": _score("first", 1), "second": _score("second", 2)},
            date(2024, 1, 2),
            "UTC",
        )


def test_rejects_missing_extra_and_mismatched_scores() -> None:
    states, scores = _three_state_day()
    with pytest.raises(ValueError, match="missing scores"):
        rank_known_date_intervals(states, {"a": scores["a"]}, date(2024, 1, 2), "UTC")

    with pytest.raises(ValueError, match="unknown or wrong-date"):
        rank_known_date_intervals(
            states,
            {**scores, "other": _score("other", 2)},
            date(2024, 1, 2),
            "UTC",
        )

    mismatched = {**scores, "a": _score("not-a", 3)}
    with pytest.raises(ValueError, match="contains score for state"):
        rank_known_date_intervals(states, mismatched, date(2024, 1, 2), "UTC")


def test_rejects_candidate_from_wrong_declared_date() -> None:
    wrong = _state(
        "wrong",
        datetime(2024, 1, 3, tzinfo=UTC),
        datetime(2024, 1, 4, tzinfo=UTC),
    )
    with pytest.raises(ValueError, match="does not intersect declared local date"):
        rank_known_date_intervals(
            [wrong], {"wrong": _score("wrong", 1)}, date(2024, 1, 2), "UTC"
        )
