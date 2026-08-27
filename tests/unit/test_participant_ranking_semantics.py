from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from hdmatch.participant.backend import AstroHDParticipantBackend
from hdmatch.schemas import (
    BehavioralResponse,
    CandidateState,
    LocalDateOverlap,
    ScoredState,
    StructuralChartFeatures,
)


def _state(
    state_id: str,
    *,
    start: datetime,
    duration_seconds: int,
    gate: int,
) -> CandidateState:
    end = start + timedelta(seconds=duration_seconds)
    features = StructuralChartFeatures(
        type="Projector",
        strategy="Wait for the Invitation",
        authority="Splenic",
        profile="2/4",
        definition="Single",
        defined_centers=("Spleen", "G"),
        channels=("1-8",),
        activation_gates={"personality:sun": gate},
    )
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=f"{gate:064x}"[-64:],
        chart_features=features,
        local_date_overlaps=(
            LocalDateOverlap(date=start.date(), seconds=float(duration_seconds)),
        ),
    )


def _zero_score(state_id: str) -> ScoredState:
    return ScoredState(
        state_id=state_id,
        net_rubric_bits=0.0,
        evidence_rubric_bits=0.0,
        contradiction_rubric_bits=0.0,
        detailed_support=0.0,
        core_fit=0.0,
        meaningful_contradictions=0,
    )


def test_zero_evidence_state_rank_is_not_broken_by_interval_duration() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("A", start=start, duration_seconds=10, gate=1),
        _state("B", start=start + timedelta(seconds=10), duration_seconds=100, gate=2),
        _state("C", start=start + timedelta(seconds=110), duration_seconds=1000, gate=3),
    )
    scores = {state.state_id: _zero_score(state.state_id) for state in states}
    backend = object.__new__(AstroHDParticipantBackend)

    ranked = backend._rank_states(states, scores)

    assert {item.rank for item in ranked} == {2.0}


class _CountingModel:
    def __init__(self) -> None:
        self.calls = 0

    @staticmethod
    def scoring_signature(
        chart: StructuralChartFeatures,
    ) -> tuple[str, str, str, str, tuple[str, ...]]:
        return (
            chart.type,
            chart.strategy,
            chart.authority,
            chart.profile,
            tuple(sorted(chart.defined_centers)),
        )

    def score(
        self,
        state: CandidateState,
        responses: tuple[BehavioralResponse, ...],
        prevalence: dict[str, float],
    ) -> ScoredState:
        del responses, prevalence
        self.calls += 1
        return ScoredState(
            state_id=state.state_id,
            net_rubric_bits=1.0,
            evidence_rubric_bits=1.0,
            contradiction_rubric_bits=0.0,
            detailed_support=50.0,
            core_fit=50.0,
            meaningful_contradictions=0,
        )


def test_scoring_runs_once_for_same_model_visible_signature() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("A", start=start, duration_seconds=10, gate=1),
        _state("B", start=start + timedelta(seconds=10), duration_seconds=10, gate=2),
    )
    response = BehavioralResponse(
        question_id="Q",
        cluster_id="C",
        answer="yes",
        behavioral_confidence=1.0,
        measurement_reliability=1.0,
    )
    model = _CountingModel()
    backend = object.__new__(AstroHDParticipantBackend)
    setattr(backend, "model", model)

    scores = backend._score_states(states, (response,), {"anchor": 0.5})

    assert model.calls == 1
    assert set(scores) == {"A", "B"}
    assert scores["A"].state_id == "A"
    assert scores["B"].state_id == "B"
    assert scores["A"].net_rubric_bits == scores["B"].net_rubric_bits == 1.0
