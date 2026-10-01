from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast

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
        local_date_overlaps=(LocalDateOverlap(date=start.date(), seconds=float(duration_seconds)),),
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


def _score(
    state_id: str,
    *,
    net: float = 1.0,
    meaningful_contradictions: int = 0,
    detailed_support: float = 50.0,
    core_fit: float = 50.0,
) -> ScoredState:
    return ScoredState(
        state_id=state_id,
        net_rubric_bits=net,
        evidence_rubric_bits=max(net, 0.0),
        contradiction_rubric_bits=max(-net, 0.0),
        detailed_support=detailed_support,
        core_fit=core_fit,
        meaningful_contradictions=meaningful_contradictions,
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


def test_core_fit_does_not_split_or_order_an_evidence_tie() -> None:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("LOW", start=start, duration_seconds=60, gate=1),
        _state("HIGH", start=start + timedelta(seconds=60), duration_seconds=60, gate=2),
    )
    scores = {
        "LOW": _score("LOW", core_fit=66.66666666666667),
        "HIGH": _score("HIGH", core_fit=78.57142857142857),
    }
    backend = object.__new__(AstroHDParticipantBackend)

    ranked = backend._rank_states(states, scores)

    assert [item.state.state_id for item in ranked] == ["LOW", "HIGH"]
    assert {item.state.state_id: item.rank for item in ranked} == {"LOW": 1.5, "HIGH": 1.5}
    assert backend._top_net_margin(ranked) == 0.0


def test_core_fit_cannot_override_authorized_ranking_fields() -> None:
    start = datetime(2001, 1, 1, tzinfo=UTC)
    states = (
        _state("OTHER", start=start, duration_seconds=60, gate=1),
        _state(
            "PREFERRED",
            start=start + timedelta(seconds=60),
            duration_seconds=60,
            gate=2,
        ),
    )
    controls = (
        (
            _score("PREFERRED", net=2.0, core_fit=0.0),
            _score("OTHER", net=1.0, core_fit=100.0),
        ),
        (
            _score("PREFERRED", meaningful_contradictions=0, core_fit=0.0),
            _score("OTHER", meaningful_contradictions=1, core_fit=100.0),
        ),
        (
            _score("PREFERRED", detailed_support=60.0, core_fit=0.0),
            _score("OTHER", detailed_support=50.0, core_fit=100.0),
        ),
    )
    backend = object.__new__(AstroHDParticipantBackend)

    for preferred, other in controls:
        ranked = backend._rank_states(
            states,
            {"PREFERRED": preferred, "OTHER": other},
        )
        assert [item.state.state_id for item in ranked] == ["PREFERRED", "OTHER"]
        assert [item.rank for item in ranked] == [1.0, 2.0]


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
    cast(Any, backend).model = model

    scores = backend._score_states(states, (response,), {"anchor": 0.5})

    assert model.calls == 1
    assert set(scores) == {"A", "B"}
    assert scores["A"].state_id == "A"
    assert scores["B"].state_id == "B"
    assert scores["A"].net_rubric_bits == scores["B"].net_rubric_bits == 1.0
