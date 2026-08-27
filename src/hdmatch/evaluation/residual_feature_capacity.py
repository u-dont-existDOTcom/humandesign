"""Rank cached structural features after the clean V3.6 observable fingerprint.

This is a survey-design diagnostic.  It asks which still-unused chart distinctions
could split states that the old holistic behavioral profile leaves tied.  A high
capacity feature is only a target for interpretation research; it is not evidence
that the feature has a valid behavioral correlate.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.discrimination import FingerprintMetrics, summarize_fingerprints
from hdmatch.evaluation.holistic_profile_information import observable_id, predicate_matches
from hdmatch.runtime.century_cache import CenturyCacheManifest
from hdmatch.schemas import CandidateState, StructuralChartFeatures


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class ResidualFeatureCapacity(_FrozenModel):
    feature_id: str = Field(min_length=1)
    feature_kind: str = Field(min_length=1)
    unique_values: int = Field(ge=1)
    combined_unique_fingerprints: int = Field(ge=1)
    incremental_uniform_bits: float = Field(ge=0.0)
    incremental_duration_weighted_bits: float = Field(ge=0.0)
    uniform_top1_ceiling: float = Field(ge=0.0, le=1.0)
    tie_size_p50: int = Field(ge=1)
    tie_size_p95: int = Field(ge=1)
    tie_size_max: int = Field(ge=1)
    reference_baseline_tie_size: int = Field(ge=1)
    reference_distinct_values_within_tie: int = Field(ge=1)
    reference_tie_size_after_feature: int = Field(ge=1)
    reference_is_unique_after_feature: bool


class V36ResidualFeatureAudit(_FrozenModel):
    schema_version: str = "v36-residual-feature-capacity-v1"
    cache_interval_count: int = Field(ge=1)
    cache_engine_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    cache_canonical_rows_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    baseline_observable_count: int = Field(ge=1)
    baseline: FingerprintMetrics
    reference_timestamp_utc: datetime
    reference_state_id: str
    reference_baseline_tie_size: int = Field(ge=1)
    feature_count: int = Field(ge=1)
    ranked_features: tuple[ResidualFeatureCapacity, ...]


def audit_v36_residual_feature_capacity(
    states: Sequence[CandidateState],
    manifest: CenturyCacheManifest,
    model: Mapping[str, Any],
    *,
    reference_timestamp: datetime = datetime(1985, 1, 29, 0, 22, 30, tzinfo=UTC),
) -> V36ResidualFeatureAudit:
    """Measure structural information remaining after the clean V3.6 observables."""

    if not states:
        raise ValueError("residual feature audit requires candidate states")
    if len(states) != manifest.interval_count:
        raise ValueError("candidate state count does not match century-cache manifest")
    structural = tuple(_require_structural(state) for state in states)
    durations = tuple((state.end_utc - state.start_utc).total_seconds() for state in states)
    baseline, observable_count = _clean_observable_patterns(structural, model)
    baseline_metrics = summarize_fingerprints(baseline, durations)

    reference_index = next(
        (
            index
            for index, state in enumerate(states)
            if state.start_utc <= reference_timestamp < state.end_utc
        ),
        None,
    )
    if reference_index is None:
        raise ValueError("reference timestamp is outside the candidate universe")
    reference_fingerprint = baseline[reference_index]
    reference_tie_indices = tuple(
        index for index, fingerprint in enumerate(baseline) if fingerprint == reference_fingerprint
    )

    feature_vectors = _feature_vectors(structural)
    ranked = tuple(
        sorted(
            (
                _capacity_result(
                    feature_id=feature_id,
                    feature_kind=feature_kind,
                    base=baseline,
                    values=values,
                    durations=durations,
                    baseline_metrics=baseline_metrics,
                    reference_index=reference_index,
                    reference_tie_indices=reference_tie_indices,
                )
                for feature_id, feature_kind, values in feature_vectors
            ),
            key=lambda item: (
                -item.incremental_uniform_bits,
                item.reference_tie_size_after_feature,
                item.feature_id,
            ),
        )
    )
    return V36ResidualFeatureAudit(
        cache_interval_count=manifest.interval_count,
        cache_engine_fingerprint=manifest.engine_fingerprint,
        cache_canonical_rows_sha256=manifest.canonical_rows_sha256,
        baseline_observable_count=observable_count,
        baseline=baseline_metrics,
        reference_timestamp_utc=reference_timestamp,
        reference_state_id=states[reference_index].state_id,
        reference_baseline_tie_size=len(reference_tie_indices),
        feature_count=len(ranked),
        ranked_features=ranked,
    )


def _clean_observable_patterns(
    features_by_state: Sequence[StructuralChartFeatures],
    model: Mapping[str, Any],
) -> tuple[tuple[tuple[int, ...], ...], int]:
    mappings = tuple(
        mapping for mapping in model["mappings"] if not bool(mapping.get("post_selection", False))
    )
    contradictions = tuple(model.get("contradictions", ()))
    observable_ids = tuple(
        sorted(
            {observable_id(mapping) for mapping in mappings}
            | {f"CONTRADICTION:{item['cluster']}" for item in contradictions}
        )
    )
    by_observable: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for mapping in mappings:
        by_observable[observable_id(mapping)].append(mapping)

    patterns: list[tuple[int, ...]] = []
    for features in features_by_state:
        values: list[int] = []
        for item_id in observable_ids:
            if item_id.startswith("CONTRADICTION:"):
                cluster = item_id.split(":", 1)[1]
                matched = any(
                    str(item["cluster"]) == cluster
                    and predicate_matches(features, item["predicate"])
                    for item in contradictions
                )
            else:
                matched = any(
                    predicate_matches(features, mapping["predicate"])
                    for mapping in by_observable[item_id]
                )
            values.append(1 if matched else 0)
        patterns.append(tuple(values))
    return tuple(patterns), len(observable_ids)


def _feature_vectors(
    structural: Sequence[StructuralChartFeatures],
) -> tuple[tuple[str, str, tuple[Hashable, ...]], ...]:
    activation_keys = tuple(
        sorted({key for features in structural for key in features.activation_gates})
    )
    vectors: list[tuple[str, str, tuple[Hashable, ...]]] = [
        (
            "definition",
            "bodygraph",
            tuple(features.definition for features in structural),
        ),
        (
            "channels",
            "bodygraph",
            tuple(tuple(sorted(features.channels)) for features in structural),
        ),
        (
            "definition+channels",
            "bodygraph_combination",
            tuple(
                (features.definition, tuple(sorted(features.channels)))
                for features in structural
            ),
        ),
        (
            "active_gate_set:any_side",
            "activation_gate_set",
            tuple(
                tuple(sorted(set(features.activation_gates.values())))
                for features in structural
            ),
        ),
    ]
    for side in ("personality", "design"):
        side_keys = tuple(key for key in activation_keys if key.startswith(f"{side}:"))
        if not side_keys:
            continue
        vectors.extend(
            (
                (
                    f"active_gate_set:{side}",
                    "activation_gate_set",
                    tuple(
                        tuple(
                            sorted(
                                {
                                    features.activation_gates[key]
                                    for key in side_keys
                                    if key in features.activation_gates
                                }
                            )
                        )
                        for features in structural
                    ),
                ),
                (
                    f"activation_vector:{side}",
                    "activation_vector",
                    tuple(
                        tuple((key, features.activation_gates.get(key)) for key in side_keys)
                        for features in structural
                    ),
                ),
            )
        )
    vectors.append(
        (
            "activation_vector:all",
            "activation_vector",
            tuple(
                tuple((key, features.activation_gates.get(key)) for key in activation_keys)
                for features in structural
            ),
        )
    )
    for key in activation_keys:
        vectors.append(
            (
                f"activation:{key}",
                "activation_position",
                tuple(features.activation_gates.get(key) for features in structural),
            )
        )
    return tuple(vectors)


def _capacity_result(
    *,
    feature_id: str,
    feature_kind: str,
    base: Sequence[Hashable],
    values: Sequence[Hashable],
    durations: Sequence[float],
    baseline_metrics: FingerprintMetrics,
    reference_index: int,
    reference_tie_indices: Sequence[int],
) -> ResidualFeatureCapacity:
    combined = tuple(zip(base, values, strict=True))
    metrics = summarize_fingerprints(combined, durations)
    reference_value = values[reference_index]
    tie_values = {values[index] for index in reference_tie_indices}
    remaining_reference = sum(
        values[index] == reference_value for index in reference_tie_indices
    )
    return ResidualFeatureCapacity(
        feature_id=feature_id,
        feature_kind=feature_kind,
        unique_values=len(set(values)),
        combined_unique_fingerprints=metrics.unique_fingerprints,
        incremental_uniform_bits=max(
            0.0, metrics.uniform_information_bits - baseline_metrics.uniform_information_bits
        ),
        incremental_duration_weighted_bits=max(
            0.0,
            metrics.duration_weighted_information_bits
            - baseline_metrics.duration_weighted_information_bits,
        ),
        uniform_top1_ceiling=metrics.uniform_top1_ceiling,
        tie_size_p50=metrics.tie_size_p50,
        tie_size_p95=metrics.tie_size_p95,
        tie_size_max=metrics.tie_size_max,
        reference_baseline_tie_size=len(reference_tie_indices),
        reference_distinct_values_within_tie=len(tie_values),
        reference_tie_size_after_feature=remaining_reference,
        reference_is_unique_after_feature=remaining_reference == 1,
    )


def _require_structural(state: CandidateState) -> StructuralChartFeatures:
    if not isinstance(state.chart_features, StructuralChartFeatures):
        raise ValueError("residual feature audit requires structural chart features")
    return state.chart_features
