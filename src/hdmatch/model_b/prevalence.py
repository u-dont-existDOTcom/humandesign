"""Exact duration-weighted conditional prevalence for detailed Model B anchors."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

from hdmatch.model_b.types import (
    ConditionalLevel,
    DurationWeightedChartState,
    FrozenAnchorSpec,
    ReferenceUniverse,
)

_DURATION_TOLERANCE_SECONDS: Final = 1e-6


@dataclass(frozen=True, slots=True)
class DenominatorAttempt:
    """Audit record for one level of the frozen conditional backoff hierarchy."""

    level_id: str
    parent_anchor_ids: tuple[str, ...]
    conditioning_values: tuple[tuple[str, str], ...]
    denominator_duration_seconds: float
    effective_state_equivalents: float
    minimum_reference_size_met: bool


@dataclass(frozen=True, slots=True)
class PrevalenceEstimate:
    """Transparent duration numerator and denominator for one candidate context."""

    anchor_id: str
    universe_id: str
    universe_sha256: str
    selected_level_id: str
    selected_parent_anchor_ids: tuple[str, ...]
    selected_conditioning_values: tuple[tuple[str, str], ...]
    numerator_duration_seconds: float
    denominator_duration_seconds: float
    effective_state_equivalents: float
    minimum_reference_size_met: bool
    prevalence: float
    duration_weighted: bool
    segmentation: str
    backoff_level: int
    attempts: tuple[DenominatorAttempt, ...]


class ConditionalPrevalenceEngine:
    """Immutable lookup over a frozen, exactly segmented reference universe."""

    def __init__(
        self,
        anchor_specs: tuple[FrozenAnchorSpec, ...],
        states: tuple[DurationWeightedChartState, ...],
        universe: ReferenceUniverse,
    ) -> None:
        if not anchor_specs:
            raise ValueError("at least one frozen prevalence anchor is required")
        if not states:
            raise ValueError("reference universe must contain stable chart states")
        anchors = {item.anchor_id: item for item in anchor_specs}
        if len(anchors) != len(anchor_specs):
            raise ValueError("prevalence anchor IDs must be unique")
        unknown_parents = sorted(
            {
                parent_id
                for anchor in anchor_specs
                for level in anchor.conditional_levels
                for parent_id in level.parent_anchor_ids
                if parent_id not in anchors
            }
        )
        if unknown_parents:
            raise ValueError(f"unknown conditional parent anchors: {unknown_parents}")
        self_references = sorted(
            anchor.anchor_id
            for anchor in anchor_specs
            if any(
                anchor.anchor_id in level.parent_anchor_ids for level in anchor.conditional_levels
            )
        )
        if self_references:
            raise ValueError(
                f"prevalence anchors cannot condition on themselves: {self_references}"
            )
        total_duration = math.fsum(state.duration_seconds for state in states)
        allowed_error = max(
            _DURATION_TOLERANCE_SECONDS,
            universe.expected_total_duration_seconds * 1e-12,
        )
        if abs(total_duration - universe.expected_total_duration_seconds) > allowed_error:
            raise ValueError(
                "reference-state durations do not equal frozen universe duration: "
                f"{total_duration} != {universe.expected_total_duration_seconds}"
            )
        self._anchors = anchors
        self._states = states
        self._universe = universe

    @property
    def universe(self) -> ReferenceUniverse:
        return self._universe

    def estimate(self, anchor_id: str, chart: object) -> PrevalenceEstimate:
        """Select the first sufficiently sized frozen denominator, backing off as declared."""

        try:
            anchor = self._anchors[anchor_id]
        except KeyError as error:
            raise KeyError(f"unknown prevalence anchor {anchor_id}") from error

        attempts: list[DenominatorAttempt] = []
        selected: (
            tuple[
                int,
                ConditionalLevel,
                tuple[tuple[str, str], ...],
                float,
                float,
                bool,
            ]
            | None
        ) = None
        for backoff_level, level in enumerate(anchor.conditional_levels):
            values = tuple(
                sorted(
                    (dimension.dimension_id, dimension.value(chart))
                    for dimension in level.dimensions
                )
            )
            denominator = math.fsum(
                state.duration_seconds
                for state in self._states
                if self._matches_denominator(state.chart, level, values)
            )
            equivalents = denominator / self._universe.state_equivalent_duration_seconds
            threshold_met = equivalents >= self._universe.minimum_effective_state_equivalents
            attempts.append(
                DenominatorAttempt(
                    level_id=level.level_id,
                    parent_anchor_ids=level.parent_anchor_ids,
                    conditioning_values=values,
                    denominator_duration_seconds=denominator,
                    effective_state_equivalents=equivalents,
                    minimum_reference_size_met=threshold_met,
                )
            )
            is_last_level = backoff_level == len(anchor.conditional_levels) - 1
            if denominator > 0.0 and (threshold_met or is_last_level):
                selected = (
                    backoff_level,
                    level,
                    values,
                    denominator,
                    equivalents,
                    threshold_met,
                )
                break

        if selected is None:
            raise ValueError(
                f"all frozen denominators are empty for anchor {anchor_id} in candidate context"
            )
        backoff_level, level, values, denominator, equivalents, threshold_met = selected
        numerator = math.fsum(
            state.duration_seconds
            for state in self._states
            if self._matches_denominator(state.chart, level, values)
            and anchor.predicate.matches(state.chart)
        )
        prevalence = numerator / denominator
        if not 0.0 <= prevalence <= 1.0:
            raise AssertionError("conditional prevalence escaped [0, 1]")
        return PrevalenceEstimate(
            anchor_id=anchor_id,
            universe_id=self._universe.universe_id,
            universe_sha256=self._universe.universe_sha256,
            selected_level_id=level.level_id,
            selected_parent_anchor_ids=level.parent_anchor_ids,
            selected_conditioning_values=values,
            numerator_duration_seconds=numerator,
            denominator_duration_seconds=denominator,
            effective_state_equivalents=equivalents,
            minimum_reference_size_met=threshold_met,
            prevalence=prevalence,
            duration_weighted=True,
            segmentation=self._universe.segmentation,
            backoff_level=backoff_level,
            attempts=tuple(attempts),
        )

    def _matches_denominator(
        self,
        chart: object,
        level: ConditionalLevel,
        conditioning_values: tuple[tuple[str, str], ...],
    ) -> bool:
        if any(
            not self._anchors[parent_id].predicate.matches(chart)
            for parent_id in level.parent_anchor_ids
        ):
            return False
        expected = dict(conditioning_values)
        return all(
            dimension.value(chart) == expected[dimension.dimension_id]
            for dimension in level.dimensions
        )
