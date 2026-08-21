"""Exact-duration prevalence preparation for Model A plus V2 detailed anchors."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType

from hdmatch.model import MappingLibrary
from hdmatch.model_b.prevalence import ConditionalPrevalenceEngine
from hdmatch.model_b.types import (
    ConditionalLevel,
    DurationWeightedChartState,
    FrozenAnchorSpec,
    ReferenceUniverse,
)
from hdmatch.schemas import CandidateState
from hdmatch.util import sha256_json

from .artifacts import CompiledModelArtifact, CompiledPathway
from .selectors import parent_dimension_extractors, selector_predicate


@dataclass(frozen=True, slots=True)
class PreparedPrevalence:
    """Both prevalence contexts required by the composite V2 runtime."""

    base_flat: Mapping[str, float]
    detailed_context: ConditionalPrevalenceEngine
    universe_id: str
    universe_sha256: str
    total_duration_seconds: float


def prepare_prevalence(
    states: Sequence[CandidateState],
    base_library: MappingLibrary,
    artifact: CompiledModelArtifact,
) -> PreparedPrevalence:
    """Prepare exact duration-weighted base and conditional detailed prevalence."""

    state_tuple = tuple(states)
    if not state_tuple:
        raise ValueError("prevalence preparation requires candidate states")
    durations = tuple((state.end_utc - state.start_utc).total_seconds() for state in state_tuple)
    if any(not math.isfinite(item) or item <= 0.0 for item in durations):
        raise ValueError("candidate states must have finite positive durations")
    total_duration = math.fsum(durations)
    universe_hash = sha256_json(
        [
            {
                "state_id": state.state_id,
                "start_utc": state.start_utc.isoformat(),
                "end_utc": state.end_utc.isoformat(),
                "chart_features_hash": state.chart_features_hash,
            }
            for state in state_tuple
        ]
    )
    universe_id = f"v2-new-reference-{universe_hash[:16]}"
    base = _base_flat_prevalence(state_tuple, durations, total_duration, base_library)
    detailed_states = tuple(
        DurationWeightedChartState(
            chart=state.chart_features,
            duration_seconds=duration,
        )
        for state, duration in zip(state_tuple, durations, strict=True)
    )
    specs = _anchor_specs(artifact)
    if not specs:
        raise ValueError("compiled V2 model has no scoreable detailed anchors")
    universe = ReferenceUniverse(
        universe_id=universe_id,
        universe_sha256=universe_hash,
        expected_total_duration_seconds=total_duration,
        state_equivalent_duration_seconds=total_duration / len(state_tuple),
        minimum_effective_state_equivalents=float(
            artifact.constants.minimum_effective_reference_size
        ),
        segmentation=artifact.constants.boundary_segmentation,
    )
    return PreparedPrevalence(
        base_flat=MappingProxyType(base),
        detailed_context=ConditionalPrevalenceEngine(specs, detailed_states, universe),
        universe_id=universe_id,
        universe_sha256=universe_hash,
        total_duration_seconds=total_duration,
    )


def _base_flat_prevalence(
    states: tuple[CandidateState, ...],
    durations: tuple[float, ...],
    total_duration: float,
    library: MappingLibrary,
) -> dict[str, float]:
    result: dict[str, float] = {}
    for mapping in library.frozen_mappings:
        anchor_id = mapping.anchor_id
        if anchor_id in result:
            continue
        assert mapping.chart_feature_predicate is not None
        matching = math.fsum(
            duration
            for state, duration in zip(states, durations, strict=True)
            if mapping.chart_feature_predicate.matches(state.chart_features)
        )
        if matching > 0.0:
            result[anchor_id] = matching / total_duration
    return dict(sorted(result.items()))


def _anchor_specs(artifact: CompiledModelArtifact) -> tuple[FrozenAnchorSpec, ...]:
    pathways: dict[str, CompiledPathway] = {}
    for rule in artifact.rules_for_scope():
        candidates = (rule.primary, *rule.alternatives)
        if rule.corroborator is not None:
            candidates = (*candidates, rule.corroborator)
        for pathway in candidates:
            previous = pathways.setdefault(pathway.anchor_id, pathway)
            if (
                previous.selector != pathway.selector
                or previous.conditional_parent_levels != pathway.conditional_parent_levels
            ):
                raise ValueError(
                    f"anchor {pathway.anchor_id} has conflicting selector/prevalence definitions"
                )
    return tuple(
        FrozenAnchorSpec(
            anchor_id=pathway.anchor_id,
            predicate=selector_predicate(pathway.selector),
            conditional_levels=tuple(
                ConditionalLevel(
                    level_id=level.level_id,
                    dimensions=parent_dimension_extractors(level.dimensions),
                )
                for level in pathway.conditional_parent_levels
            ),
        )
        for _, pathway in sorted(pathways.items())
    )
