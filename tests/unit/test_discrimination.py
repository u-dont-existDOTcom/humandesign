from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from hdmatch.evaluation.discrimination import audit_partition, greedy_question_sequence
from hdmatch.schemas import CandidateState, LocalDateOverlap, StructuralChartFeatures


def _state(state_id: str, start_minute: int, duration_seconds: int, profile: str) -> CandidateState:
    start = datetime(2000, 1, 1, tzinfo=UTC) + timedelta(minutes=start_minute)
    end = start + timedelta(seconds=duration_seconds)
    features = StructuralChartFeatures(
        type="Projector",
        strategy="Wait for the Invitation",
        authority="Splenic",
        profile=profile,
        definition="Single",
        defined_centers=("G", "Spleen"),
        channels=("1-8",),
        activation_gates={"personality:sun": 1},
    )
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=(state_id.encode().hex() + "0" * 64)[:64],
        chart_features=features,
        local_date_overlaps=(
            LocalDateOverlap(date=start.date(), seconds=float(duration_seconds)),
        ),
    )


def test_partition_audit_reports_ties_and_ceiling() -> None:
    states = (
        _state("a", 0, 60, "2/4"),
        _state("b", 1, 60, "2/4"),
        _state("c", 2, 120, "3/5"),
    )
    audit = audit_partition(states, lambda state: state.chart_features.profile)

    assert audit.state_count == 3
    assert audit.group_count == 2
    assert audit.singleton_groups == 1
    assert audit.min_tie_size == 1
    assert audit.median_tie_size == 1.5
    assert audit.max_tie_size == 2
    assert audit.exact_state_ceiling == pytest.approx(2 / 3)
    assert audit.top5_state_ceiling == 1.0
    assert audit.state_uniform_entropy_bits == pytest.approx(0.918295834, rel=1e-8)
    assert audit.duration_weighted_entropy_bits == pytest.approx(1.0)
    assert audit.duration_weighted_residual_bits == pytest.approx(0.5)


def test_greedy_question_sequence_picks_most_informative_first() -> None:
    states = tuple(_state(letter, index, 60, "2/4") for index, letter in enumerate("abcd"))
    answers = {
        "a": {"Q1": "yes", "Q2": "x"},
        "b": {"Q1": "yes", "Q2": "y"},
        "c": {"Q1": "no", "Q2": "z"},
        "d": {"Q1": "no", "Q2": "z"},
    }

    steps = greedy_question_sequence(states, answers)

    assert steps[0].question_id == "Q2"
    assert steps[0].cumulative_entropy_bits == pytest.approx(1.5)
    assert steps[0].fingerprint_groups == 3
    assert steps[1].question_id == "Q1"
    assert steps[1].cumulative_entropy_bits == pytest.approx(1.5)
    assert steps[1].incremental_bits == pytest.approx(0.0)
