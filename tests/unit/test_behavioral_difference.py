from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from hdmatch.evaluation.behavioral_difference import (
    audit_behavioral_difference,
    require_behavioral_difference,
)
from hdmatch.schemas import (
    BehavioralResponse,
    CandidateState,
    ChartFeatures,
    LocalDateOverlap,
    ScoredState,
)


def _response(question_id: str, answer: str, cluster: str) -> BehavioralResponse:
    return BehavioralResponse(
        question_id=question_id,
        cluster_id=cluster,
        answer=answer,
        behavioral_confidence=1.0,
        measurement_reliability=1.0,
    )


def _state(state_id: str, *, channel: str, day: int) -> CandidateState:
    start = datetime(2000, 1, day, tzinfo=UTC)
    chart = ChartFeatures(
        personality_utc=start,
        design_utc=start - timedelta(days=88),
        type="generator",
        strategy="wait_to_respond",
        authority="sacral",
        profile="3/5",
        definition="single_definition",
        defined_centers=("g", "throat"),
        channels=(channel,),
        activations={},
    )
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=start + timedelta(hours=1),
        chart_features_hash=("a" if state_id.endswith("A") else "b") * 64,
        chart_features=chart,
        local_date_overlaps=(
            LocalDateOverlap(date=start.date(), seconds=3600.0),
        ),
    )


class _FakeModelA:
    model_sha256 = "1" * 64
    mapping_sha256 = "2" * 64
    question_bank_sha256 = "3" * 64
    library = SimpleNamespace(frozen_mappings=())

    def score_signature(self, chart: ChartFeatures) -> tuple[object, ...]:
        return (
            chart.type,
            chart.strategy,
            chart.authority,
            chart.profile,
            chart.defined_centers,
        )

    def oracle_responses(self, chart: ChartFeatures) -> tuple[BehavioralResponse, ...]:
        return (_response("A01", "wait_to_respond", "core"),)

    def score(
        self,
        state: CandidateState,
        responses: object,
        prevalence: object,
    ) -> ScoredState:
        return _score(state.state_id, 1.0)


class _FakeModelB:
    model_sha256 = "4" * 64
    mapping_sha256 = "5" * 64
    question_bank_sha256 = "3" * 64

    def oracle_responses(self, chart: ChartFeatures) -> tuple[BehavioralResponse, ...]:
        answer = "distinctly_own" if "1-8" in chart.channels else "unknown"
        return (
            _response("A01", "wait_to_respond", "core"),
            _response("T01", answer, "original"),
        )

    def prepare_prevalence(self, states: object) -> object:
        return object()

    def score(
        self,
        state: CandidateState,
        responses: object,
        prevalence: object,
    ) -> ScoredState:
        items = tuple(responses)  # type: ignore[arg-type]
        answer = next(item.answer for item in items if item.question_id == "T01")
        matches = answer == "distinctly_own" and "1-8" in state.chart_features.channels
        return _score(state.state_id, 2.0 if matches else 0.0)


class _NoDifferenceModelB(_FakeModelB):
    def oracle_responses(self, chart: ChartFeatures) -> tuple[BehavioralResponse, ...]:
        return (
            _response("A01", "wait_to_respond", "core"),
            _response("T01", "unknown", "original"),
        )


class _AdverseModelB(_FakeModelB):
    def score(
        self,
        state: CandidateState,
        responses: object,
        prevalence: object,
    ) -> ScoredState:
        items = tuple(responses)  # type: ignore[arg-type]
        answer = next(item.answer for item in items if item.question_id == "T01")
        adverse = answer == "distinctly_own" and "1-8" not in state.chart_features.channels
        return _score(state.state_id, 2.0 if adverse else 0.0)


def _score(state_id: str, value: float) -> ScoredState:
    return ScoredState(
        state_id=state_id,
        net_rubric_bits=value,
        evidence_rubric_bits=value,
        contradiction_rubric_bits=0.0,
        detailed_support=100.0 if value > 1.0 else 0.0,
        core_fit=100.0,
        meaningful_contradictions=0,
    )


def test_answer_key_free_audit_requires_response_delta_and_tie_split() -> None:
    states = (
        _state("STATE-A", channel="1-8", day=1),
        _state("STATE-B", channel="28-38", day=2),
    )

    audit = audit_behavioral_difference(  # type: ignore[arg-type]
        states,
        _FakeModelA(),
        _FakeModelB(),
    )

    assert audit.status == "passed"
    assert audit.answer_keys_used is False
    assert audit.candidate_truth_used is False
    assert audit.groups_with_non_unknown_response_delta == 1
    assert audit.groups_with_pairwise_tie_split == 1
    assert audit.groups_with_source_favoring_tie_split == 1
    assert audit.groups_with_adverse_tie_split == 0
    assert audit.witnesses[0].non_unknown_detailed_delta_question_ids == ("T01",)
    assert audit.witnesses[0].model_a_pair_relation == "tie"
    assert audit.witnesses[0].model_b_pair_relation == "source_above_comparison"
    require_behavioral_difference(audit)


def test_failed_difference_is_preserved_and_gate_fails_closed() -> None:
    states = (
        _state("STATE-A", channel="1-8", day=1),
        _state("STATE-B", channel="28-38", day=2),
    )

    audit = audit_behavioral_difference(  # type: ignore[arg-type]
        states,
        _FakeModelA(),
        _NoDifferenceModelB(),
    )

    assert audit.status == "failed"
    assert audit.witnesses == ()
    assert audit.failure_reasons
    with pytest.raises(ValueError, match="difference gate failed"):
        require_behavioral_difference(audit)


def test_adverse_only_tie_split_cannot_pass_difference_gate() -> None:
    states = (
        _state("STATE-A", channel="1-8", day=1),
        _state("STATE-B", channel="28-38", day=2),
    )

    audit = audit_behavioral_difference(  # type: ignore[arg-type]
        states,
        _FakeModelA(),
        _AdverseModelB(),
    )

    assert audit.status == "failed"
    assert audit.groups_with_source_favoring_tie_split == 0
    assert audit.groups_with_adverse_tie_split == 1
    assert audit.witnesses[0].model_b_pair_relation == "comparison_above_source"
    with pytest.raises(ValueError, match="difference gate failed"):
        require_behavioral_difference(audit)
