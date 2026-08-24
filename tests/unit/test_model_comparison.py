from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.evaluation.model_comparison import (
    audit_structural_discrimination,
    model_a_core_signature,
    model_b_detailed_signature,
)
from hdmatch.model_b.compiler import build_model_b_artifact
from hdmatch.schemas import Activation, CandidateState, ChartFeatures, LocalDateOverlap

ROOT = Path(__file__).parents[2]


def _activation(side: str, body: str, gate: int, line: int) -> Activation:
    return Activation(side=side, body=body, longitude=0.0, gate=gate, line=line)


def _chart(*, earth_gate: int = 45, chart_type: str = "projector") -> ChartFeatures:
    activations = {
        "personality:sun": _activation("personality", "sun", 26, 4),
        "personality:earth": _activation("personality", "earth", earth_gate, 4),
        "design:sun": _activation("design", "sun", 44, 2),
        "design:earth": _activation("design", "earth", 24, 2),
        "personality:north_node": _activation("personality", "north_node", 13, 3),
        "personality:south_node": _activation("personality", "south_node", 7, 3),
        "design:north_node": _activation("design", "north_node", 1, 5),
        "design:south_node": _activation("design", "south_node", 2, 5),
        "personality:moon": _activation("personality", "moon", 26, 1),
    }
    return ChartFeatures(
        personality_utc=datetime(2000, 1, 1, tzinfo=UTC),
        design_utc=datetime(1999, 10, 1, tzinfo=UTC),
        type=chart_type,
        strategy="wait_for_invitation",
        authority="splenic",
        profile="4/2",
        definition="split_definition",
        defined_centers=("heart_ego", "spleen", "throat"),
        channels=("26-44",),
        activations=activations,
    )


def _state(
    state_id: str,
    start: datetime,
    seconds: int,
    *,
    earth_gate: int = 45,
    chart_type: str = "projector",
) -> CandidateState:
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=start + timedelta(seconds=seconds),
        chart_features_hash=(state_id[-1].lower() * 64),
        chart_features=_chart(earth_gate=earth_gate, chart_type=chart_type),
        local_date_overlaps=(LocalDateOverlap(date=date(2000, 1, 1), seconds=seconds),),
    )


def test_exact_duration_weighted_equivalence_groups_and_upper_bound_label() -> None:
    artifact = build_model_b_artifact(ROOT)
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _state("STATE-A", start, 10),
        _state("STATE-B", start + timedelta(seconds=10), 20, earth_gate=46),
        _state("STATE-C", start + timedelta(seconds=30), 30, chart_type="generator"),
    )

    audit = audit_structural_discrimination(states, artifact)

    assert audit.answer_keys_used is False
    assert audit.comparison_kind == "structural_resolution_upper_bound_not_behavioral_recovery"
    assert audit.detailed_behavioral_mapping_status.value == "unresolved"
    assert audit.model_a.unique_signature_count == 2
    assert audit.model_b.unique_signature_count == 3
    assert audit.signature_count_gain == 1
    assert audit.model_a_groups_split_by_model_b == 1
    assert audit.model_a_groups_not_split_by_model_b == 1
    assert audit.model_a.total_duration_microseconds == 60_000_000
    assert sorted(group.duration_microseconds for group in audit.model_a.equivalence_groups) == [
        30_000_000,
        30_000_000,
    ]
    assert audit.model_a.duration_collision_numerator_microseconds_squared == 2 * 30_000_000**2
    assert audit.model_a.duration_collision_denominator_microseconds_squared == 60_000_000**2
    assert sorted(group.duration_microseconds for group in audit.model_b.equivalence_groups) == [
        10_000_000,
        20_000_000,
        30_000_000,
    ]
    assert "upper bound" in audit.model_b.interpretation
    assert any("not questionnaire recovery" in item for item in audit.limitations)


def test_signatures_are_explicit_composite_and_input_order_independent() -> None:
    artifact = build_model_b_artifact(ROOT)
    start = datetime(2000, 1, 1, tzinfo=UTC)
    first = _state("STATE-A", start, 10)
    second = _state("STATE-B", start + timedelta(seconds=10), 20, earth_gate=46)

    core = model_a_core_signature(first)
    detailed = model_b_detailed_signature(first, artifact)
    forward = audit_structural_discrimination((first, second), artifact)
    reverse = audit_structural_discrimination((second, first), artifact)

    assert core == (
        "type=projector",
        "strategy=wait_for_invitation",
        "authority=splenic",
        "profile=4/2",
        "defined_centers=heart_ego,spleen,throat",
    )
    assert all(f"model_a::{item}" in detailed for item in core)
    assert "model_b_anchor::cardinal_gate:personality:earth:45" in detailed
    assert forward == reverse


def test_duplicate_ids_empty_universe_and_non_utc_offsets_fail_closed() -> None:
    artifact = build_model_b_artifact(ROOT)
    start = datetime(2000, 1, 1, tzinfo=UTC)
    state = _state("STATE-A", start, 10)

    with pytest.raises(ValueError, match="cannot be empty"):
        audit_structural_discrimination((), artifact)
    with pytest.raises(ValueError, match="IDs must be unique"):
        audit_structural_discrimination((state, state), artifact)

    non_utc = state.model_copy(
        update={
            "start_utc": datetime.fromisoformat("2000-01-01T01:00:00+01:00"),
            "end_utc": datetime.fromisoformat("2000-01-01T01:00:10+01:00"),
        }
    )
    with pytest.raises(ValueError, match="UTC offset zero"):
        audit_structural_discrimination((non_utc,), artifact)

    gap = _state("STATE-B", start + timedelta(seconds=11), 10)
    with pytest.raises(ValueError, match="contiguous exact partition"):
        audit_structural_discrimination((state, gap), artifact)
