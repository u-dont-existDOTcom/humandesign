from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import pytest

from hdmatch.model_b.prevalence import ConditionalPrevalenceEngine
from hdmatch.model_b.types import (
    ConditionalLevel,
    DurationWeightedChartState,
    FrozenAnchorSpec,
    ReferenceUniverse,
)


@dataclass(frozen=True)
class FieldEquals:
    field: str
    expected: object

    def matches(self, chart: object) -> bool:
        assert isinstance(chart, Mapping)
        return chart.get(self.field) == self.expected


@dataclass(frozen=True)
class FieldDimension:
    dimension_id: str
    field: str

    def value(self, chart: object) -> str:
        assert isinstance(chart, Mapping)
        return str(chart[self.field])


def _universe(*, minimum: float = 4.0) -> ReferenceUniverse:
    return ReferenceUniverse(
        universe_id="reference-interval",
        universe_sha256="a" * 64,
        expected_total_duration_seconds=100.0,
        state_equivalent_duration_seconds=10.0,
        minimum_effective_state_equivalents=minimum,
    )


def _states() -> tuple[DurationWeightedChartState, ...]:
    return (
        DurationWeightedChartState(
            {"gate_active": True, "line": 3, "complement_active": False, "hanging": True},
            10.0,
        ),
        DurationWeightedChartState(
            {"gate_active": True, "line": 4, "complement_active": True, "hanging": False},
            30.0,
        ),
        DurationWeightedChartState(
            {"gate_active": False, "line": 3, "complement_active": False, "hanging": False},
            60.0,
        ),
    )


def _anchors() -> tuple[FrozenAnchorSpec, ...]:
    unconditional = (ConditionalLevel("global"),)
    return (
        FrozenAnchorSpec("active-gate", FieldEquals("gate_active", True), unconditional),
        FrozenAnchorSpec(
            "line-3",
            FieldEquals("line", 3),
            (
                ConditionalLevel("given-active-gate", ("active-gate",)),
                ConditionalLevel("global"),
            ),
        ),
        FrozenAnchorSpec(
            "hanging-gate",
            FieldEquals("hanging", True),
            (
                ConditionalLevel("given-active-gate", ("active-gate",)),
                ConditionalLevel("global"),
            ),
        ),
    )


def test_line_and_hanging_gate_use_explicit_conditional_duration_denominators() -> None:
    engine = ConditionalPrevalenceEngine(_anchors(), _states(), _universe())
    candidate = {"gate_active": True, "line": 3, "complement_active": False}

    line = engine.estimate("line-3", candidate)
    hanging = engine.estimate("hanging-gate", candidate)

    assert line.selected_level_id == "given-active-gate"
    assert line.numerator_duration_seconds == 10.0
    assert line.denominator_duration_seconds == 40.0
    assert line.prevalence == pytest.approx(0.25)
    assert hanging.numerator_duration_seconds == 10.0
    assert hanging.denominator_duration_seconds == 40.0
    assert hanging.prevalence == pytest.approx(0.25)
    # A state-count estimate would be 1/2; exact duration weighting is 10/40.
    assert hanging.prevalence != pytest.approx(0.5)


def test_small_conditional_denominator_backs_off_only_along_frozen_hierarchy() -> None:
    engine = ConditionalPrevalenceEngine(_anchors(), _states(), _universe(minimum=5.0))

    result = engine.estimate("hanging-gate", {"gate_active": True})

    assert result.selected_level_id == "global"
    assert result.backoff_level == 1
    assert result.prevalence == pytest.approx(0.10)
    assert result.attempts[0].denominator_duration_seconds == 40.0
    assert result.attempts[0].minimum_reference_size_met is False
    assert result.attempts[1].minimum_reference_size_met is True


def test_candidate_relative_dimensions_are_recorded_in_denominator_audit() -> None:
    kind = FieldDimension("kind", "kind")
    anchor = FrozenAnchorSpec(
        "detail",
        FieldEquals("detail", True),
        (
            ConditionalLevel("same-kind", dimensions=(kind,)),
            ConditionalLevel("global"),
        ),
    )
    states = (
        DurationWeightedChartState({"kind": "A", "detail": True}, 20.0),
        DurationWeightedChartState({"kind": "A", "detail": False}, 30.0),
        DurationWeightedChartState({"kind": "B", "detail": True}, 50.0),
    )
    universe = ReferenceUniverse(
        universe_id="candidate-relative",
        universe_sha256="b" * 64,
        expected_total_duration_seconds=100.0,
        state_equivalent_duration_seconds=10.0,
        minimum_effective_state_equivalents=5.0,
    )

    result = ConditionalPrevalenceEngine((anchor,), states, universe).estimate(
        "detail", {"kind": "A"}
    )

    assert result.selected_conditioning_values == (("kind", "A"),)
    assert result.denominator_duration_seconds == 50.0
    assert result.prevalence == pytest.approx(0.4)


def test_reference_states_must_cover_exact_frozen_universe_duration() -> None:
    with pytest.raises(ValueError, match="do not equal frozen universe duration"):
        ConditionalPrevalenceEngine(
            _anchors(),
            (DurationWeightedChartState({"gate_active": True}, 99.0),),
            _universe(),
        )


def test_backoff_hierarchy_cannot_add_a_new_condition() -> None:
    with pytest.raises(ValueError, match="cannot add conditions"):
        FrozenAnchorSpec(
            "invalid",
            FieldEquals("x", True),
            (
                ConditionalLevel("specific", ("parent-a",)),
                ConditionalLevel("not-a-backoff", ("parent-b",)),
                ConditionalLevel("global"),
            ),
        )


def test_conditional_hierarchy_requires_explicit_unconditional_fallback() -> None:
    with pytest.raises(ValueError, match="unconditional terminal backoff"):
        FrozenAnchorSpec(
            "invalid",
            FieldEquals("x", True),
            (ConditionalLevel("only-specific", ("parent-a",)),),
        )
