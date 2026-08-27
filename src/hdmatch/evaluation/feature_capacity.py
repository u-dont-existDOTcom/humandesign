"""Measure unused structural discrimination in the verified century cache.

These metrics describe deterministic partition capacity only.  They do not imply
that a Human Design feature predicts behavior, nor that a high-information
feature deserves a behavioral mapping without independent evidence.
"""

from __future__ import annotations

from collections.abc import Hashable, Sequence

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.discrimination import FingerprintMetrics, summarize_fingerprints
from hdmatch.runtime.century_cache import CenturyCacheManifest
from hdmatch.schemas import CandidateState, StructuralChartFeatures


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class StructuralFeatureCapacity(_FrozenModel):
    feature_id: str = Field(min_length=1)
    feature_kind: str = Field(min_length=1)
    unique_values: int = Field(ge=1)
    combined_unique_fingerprints: int = Field(ge=1)
    incremental_uniform_bits: float = Field(ge=0.0)
    incremental_duration_weighted_bits: float = Field(ge=0.0)
    uniform_top1_ceiling: float = Field(ge=0.0, le=1.0)
    duration_weighted_top1_ceiling: float = Field(ge=0.0, le=1.0)
    tie_size_p50: int = Field(ge=1)
    tie_size_p95: int = Field(ge=1)
    tie_size_max: int = Field(ge=1)


class StructuralFeatureCapacityAudit(_FrozenModel):
    schema_version: str = "structural-feature-capacity-audit-v1"
    cache_interval_count: int = Field(ge=1)
    cache_engine_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    cache_canonical_rows_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    baseline: FingerprintMetrics
    feature_count: int = Field(ge=1)
    ranked_features: tuple[StructuralFeatureCapacity, ...]


def audit_structural_feature_capacity(
    states: Sequence[CandidateState],
    manifest: CenturyCacheManifest,
) -> StructuralFeatureCapacityAudit:
    """Rank cached structural fields by information added beyond the current coarse key."""

    if not states:
        raise ValueError("feature-capacity audit requires candidate states")
    if len(states) != manifest.interval_count:
        raise ValueError("candidate state count does not match century-cache manifest")

    structural = tuple(_require_structural(state) for state in states)
    durations = tuple((state.end_utc - state.start_utc).total_seconds() for state in states)
    base = tuple(_coarse_key(features) for features in structural)
    baseline = summarize_fingerprints(base, durations)

    activation_keys = tuple(
        sorted({key for features in structural for key in features.activation_gates})
    )
    feature_vectors: list[tuple[str, str, tuple[Hashable, ...]]] = [
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
        side_keys = tuple(key for key in activation_keys if _activation_side(key) == side)
        if side_keys:
            feature_vectors.extend(
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

    feature_vectors.append(
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
        feature_vectors.append(
            (
                f"activation:{key}",
                "activation_position",
                tuple(features.activation_gates.get(key) for features in structural),
            )
        )

    ranked = tuple(
        sorted(
            (
                _capacity_result(
                    feature_id=feature_id,
                    feature_kind=feature_kind,
                    base=base,
                    values=values,
                    durations=durations,
                    baseline=baseline,
                )
                for feature_id, feature_kind, values in feature_vectors
            ),
            key=lambda item: (
                -item.incremental_duration_weighted_bits,
                -item.incremental_uniform_bits,
                item.feature_id,
            ),
        )
    )
    return StructuralFeatureCapacityAudit(
        cache_interval_count=manifest.interval_count,
        cache_engine_fingerprint=manifest.engine_fingerprint,
        cache_canonical_rows_sha256=manifest.canonical_rows_sha256,
        baseline=baseline,
        feature_count=len(ranked),
        ranked_features=ranked,
    )


def _capacity_result(
    *,
    feature_id: str,
    feature_kind: str,
    base: Sequence[Hashable],
    values: Sequence[Hashable],
    durations: Sequence[float],
    baseline: FingerprintMetrics,
) -> StructuralFeatureCapacity:
    combined = tuple(zip(base, values, strict=True))
    metrics = summarize_fingerprints(combined, durations)
    return StructuralFeatureCapacity(
        feature_id=feature_id,
        feature_kind=feature_kind,
        unique_values=len(set(values)),
        combined_unique_fingerprints=metrics.unique_fingerprints,
        incremental_uniform_bits=max(
            0.0, metrics.uniform_information_bits - baseline.uniform_information_bits
        ),
        incremental_duration_weighted_bits=max(
            0.0,
            metrics.duration_weighted_information_bits
            - baseline.duration_weighted_information_bits,
        ),
        uniform_top1_ceiling=metrics.uniform_top1_ceiling,
        duration_weighted_top1_ceiling=metrics.duration_weighted_top1_ceiling,
        tie_size_p50=metrics.tie_size_p50,
        tie_size_p95=metrics.tie_size_p95,
        tie_size_max=metrics.tie_size_max,
    )


def _require_structural(state: CandidateState) -> StructuralChartFeatures:
    if not isinstance(state.chart_features, StructuralChartFeatures):
        raise ValueError("feature-capacity audit requires structural chart features")
    return state.chart_features


def _coarse_key(features: StructuralChartFeatures) -> Hashable:
    return (
        features.type,
        features.strategy,
        features.authority,
        features.profile,
        tuple(sorted(features.defined_centers)),
    )


def _activation_side(key: str) -> str | None:
    side, separator, _ = key.partition(":")
    if separator and side in {"personality", "design"}:
        return side
    return None
