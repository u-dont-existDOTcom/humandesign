"""Information-capacity audit for the frozen V3.6 holistic profile model.

The old V3.6 audit was a rich descriptive mapping family rather than the compact
participant questionnaire.  This module measures how much deterministic chart
structure that family can expose at two levels:

* ``observable`` collapses multiple HD pathways that were intended to support the
  same participant-observable behavioral construct.  This is the conservative
  survey-visible quantity.
* ``mapping_pathway`` keeps every matched structural mapping distinct.  It is an
  upper bound on what the model can distinguish mechanically, not information a
  participant necessarily supplies.

These are capacity measurements only.  They do not validate Human Design or turn
post-selection mappings into independent evidence.
"""

from __future__ import annotations

import copy
import json
import math
from collections import Counter, defaultdict
from collections.abc import Hashable, Iterable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.discrimination import FingerprintMetrics, summarize_fingerprints
from hdmatch.runtime.century_cache import CenturyCacheManifest
from hdmatch.schemas import CandidateState, StructuralChartFeatures


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class TargetResolution(_FrozenModel):
    timestamp_utc: datetime
    state_id: str
    tie_size: int = Field(ge=1)
    uniform_information_bits: float = Field(ge=0.0)
    duration_weighted_information_bits: float = Field(ge=0.0)


class GreedyObservableStep(_FrozenModel):
    observable_id: str
    incremental_uniform_bits: float = Field(ge=0.0)
    cumulative_uniform_bits: float = Field(ge=0.0)
    cumulative_duration_weighted_bits: float = Field(ge=0.0)
    distinct_fingerprints: int = Field(ge=1)
    largest_tie_group: int = Field(ge=1)


class HolisticVariantAudit(_FrozenModel):
    include_post_selection_carriers: bool
    active_mapping_count: int = Field(ge=1)
    observable_count: int = Field(ge=1)
    observable_fingerprint: FingerprintMetrics
    mapping_pathway_fingerprint: FingerprintMetrics
    reference_1985_observable: TargetResolution
    reference_1985_mapping_pathway: TargetResolution
    greedy_observable_sequence: tuple[GreedyObservableStep, ...]


class V36HolisticProfileInformationAudit(_FrozenModel):
    schema_version: str = "v36-holistic-profile-information-audit-v1"
    cache_interval_count: int = Field(ge=1)
    cache_engine_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    cache_canonical_rows_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    base_mapping_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    overlay_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    target_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    raw_mapping_count: int = Field(ge=1)
    contradiction_count: int = Field(ge=0)
    clean_variant: HolisticVariantAudit
    best_current_variant: HolisticVariantAudit


def load_legacy_v36_model(base_path: str | Path, overlay_path: str | Path) -> dict[str, Any]:
    """Load the frozen V3.6 mapping plus its pre-ranking overlay."""

    base = json.loads(Path(base_path).read_text(encoding="utf-8"))
    overlay = json.loads(Path(overlay_path).read_text(encoding="utf-8"))
    model: dict[str, Any] = copy.deepcopy(base)
    by_id = {str(mapping["id"]): mapping for mapping in model["mappings"]}
    for mapping_id, patch in overlay.get("overrides", {}).items():
        if mapping_id not in by_id:
            raise KeyError(f"overlay override references missing mapping: {mapping_id}")
        by_id[mapping_id].update(patch)
    seen = set(by_id)
    for raw_mapping in overlay.get("add_mappings", []):
        mapping = copy.deepcopy(raw_mapping)
        mapping_id = str(mapping["id"])
        if mapping_id in seen:
            raise ValueError(f"duplicate overlay mapping id: {mapping_id}")
        model["mappings"].append(mapping)
        seen.add(mapping_id)
    return model


def audit_v36_holistic_profile_information(
    states: Sequence[CandidateState],
    manifest: CenturyCacheManifest,
    model: Mapping[str, Any],
    *,
    base_mapping_sha256: str,
    overlay_sha256: str,
    target_sha256: str,
) -> V36HolisticProfileInformationAudit:
    """Measure survey-visible and mechanism-level discrimination of V3.6."""

    if not states:
        raise ValueError("holistic profile audit requires candidate states")
    if len(states) != manifest.interval_count:
        raise ValueError("candidate state count does not match century-cache manifest")
    for state in states:
        if not isinstance(state.chart_features, StructuralChartFeatures):
            raise ValueError("holistic profile audit requires structural chart features")

    return V36HolisticProfileInformationAudit(
        cache_interval_count=manifest.interval_count,
        cache_engine_fingerprint=manifest.engine_fingerprint,
        cache_canonical_rows_sha256=manifest.canonical_rows_sha256,
        base_mapping_sha256=base_mapping_sha256,
        overlay_sha256=overlay_sha256,
        target_sha256=target_sha256,
        raw_mapping_count=len(model["mappings"]),
        contradiction_count=len(model.get("contradictions", [])),
        clean_variant=_audit_variant(states, model, include_post_selection=False),
        best_current_variant=_audit_variant(states, model, include_post_selection=True),
    )


def predicate_matches(features: StructuralChartFeatures, predicate: Mapping[str, Any]) -> bool:
    """Evaluate the legacy frozen predicate vocabulary against cache-v2 features."""

    feature = str(predicate["feature"])
    if feature == "type":
        return features.type == str(predicate["equals"])
    if feature == "authority":
        return features.authority == str(predicate["equals"])
    if feature == "center":
        present = str(predicate["name"]) in set(features.defined_centers)
        return present is bool(predicate["defined"])
    if feature == "profile":
        return features.profile == str(predicate["equals"])
    if feature == "profile_has_line":
        expected = str(predicate["line"])
        return expected in features.profile.split("/")
    if feature == "channel":
        return _canonical_channel(str(predicate["equals"])) in {
            _canonical_channel(channel) for channel in features.channels
        }
    if feature == "gate":
        return int(predicate["equals"]) in set(features.activation_gates.values())
    if feature == "activation":
        key = f"{predicate['side']}:{predicate['body']}"
        return features.activation_gates.get(key) == int(predicate["gate"])
    raise ValueError(f"unknown legacy predicate feature: {feature}")


def observable_id(mapping: Mapping[str, Any]) -> str:
    """Map structural alternatives to the participant-observable construct they share.

    The V3.6 overlay deliberately used the same dependency cluster for channel and
    hanging-gate alternatives.  Those alternatives should not become extra survey
    bits.  The three profile mappings are the exception: their stored behavioral
    statements are genuinely different observables, so they stay separate.
    """

    cluster = str(mapping["cluster"])
    if cluster == "PROFILE_STRUCTURE":
        return str(mapping["id"])
    return cluster


def _audit_variant(
    states: Sequence[CandidateState],
    model: Mapping[str, Any],
    *,
    include_post_selection: bool,
) -> HolisticVariantAudit:
    mappings = tuple(
        mapping
        for mapping in model["mappings"]
        if include_post_selection or not bool(mapping.get("post_selection", False))
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

    observable_patterns: list[tuple[int, ...]] = []
    pathway_patterns: list[tuple[str, ...]] = []
    durations: list[float] = []
    for state in states:
        features = state.chart_features
        assert isinstance(features, StructuralChartFeatures)
        observable = []
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
            observable.append(1 if matched else 0)
        observable_patterns.append(tuple(observable))
        matched_paths = [
            str(mapping["id"])
            for mapping in mappings
            if predicate_matches(features, mapping["predicate"])
        ]
        matched_paths.extend(
            f"CONTRADICTION:{item['id']}"
            for item in contradictions
            if predicate_matches(features, item["predicate"])
        )
        pathway_patterns.append(tuple(sorted(matched_paths)))
        durations.append((state.end_utc - state.start_utc).total_seconds())

    reference = datetime(1985, 1, 29, 0, 22, 30, tzinfo=UTC)
    return HolisticVariantAudit(
        include_post_selection_carriers=include_post_selection,
        active_mapping_count=len(mappings),
        observable_count=len(observable_ids),
        observable_fingerprint=summarize_fingerprints(observable_patterns, durations),
        mapping_pathway_fingerprint=summarize_fingerprints(pathway_patterns, durations),
        reference_1985_observable=_target_resolution(
            states, observable_patterns, durations, reference
        ),
        reference_1985_mapping_pathway=_target_resolution(
            states, pathway_patterns, durations, reference
        ),
        greedy_observable_sequence=_greedy_observable_sequence(
            observable_ids, observable_patterns, durations
        ),
    )


def _target_resolution(
    states: Sequence[CandidateState],
    fingerprints: Sequence[Hashable],
    durations: Sequence[float],
    timestamp: datetime,
) -> TargetResolution:
    target_index = next(
        (
            index
            for index, state in enumerate(states)
            if state.start_utc <= timestamp < state.end_utc
        ),
        None,
    )
    if target_index is None:
        raise ValueError(f"reference timestamp outside candidate universe: {timestamp}")
    fingerprint = fingerprints[target_index]
    matching = [index for index, value in enumerate(fingerprints) if value == fingerprint]
    group_duration = sum(durations[index] for index in matching)
    total_duration = sum(durations)
    return TargetResolution(
        timestamp_utc=timestamp,
        state_id=states[target_index].state_id,
        tie_size=len(matching),
        uniform_information_bits=math.log2(len(states) / len(matching)),
        duration_weighted_information_bits=-math.log2(group_duration / total_duration),
    )


def _greedy_observable_sequence(
    observable_ids: Sequence[str],
    patterns: Sequence[tuple[int, ...]],
    durations: Sequence[float],
) -> tuple[GreedyObservableStep, ...]:
    """Greedy noiseless question order by state-uniform information gain."""

    compressed: dict[tuple[int, ...], tuple[int, float]] = {}
    counts = Counter(patterns)
    duration_totals: dict[tuple[int, ...], float] = defaultdict(float)
    for pattern, duration in zip(patterns, durations, strict=True):
        duration_totals[pattern] += duration
    for pattern, count in counts.items():
        compressed[pattern] = (count, duration_totals[pattern])

    selected: list[int] = []
    remaining = set(range(len(observable_ids)))
    previous_uniform = 0.0
    result: list[GreedyObservableStep] = []
    while remaining:
        best_index = -1
        best_uniform = -1.0
        best_duration = 0.0
        best_groups: dict[tuple[int, ...], int] = {}
        for index in sorted(remaining, key=lambda item: observable_ids[item]):
            trial = (*selected, index)
            group_counts: dict[tuple[int, ...], int] = defaultdict(int)
            group_durations: dict[tuple[int, ...], float] = defaultdict(float)
            for pattern, (count, duration) in compressed.items():
                key = tuple(pattern[item] for item in trial)
                group_counts[key] += count
                group_durations[key] += duration
            uniform_entropy = _entropy_from_weights(group_counts.values())
            if uniform_entropy > best_uniform + 1e-12:
                best_index = index
                best_uniform = uniform_entropy
                best_duration = _entropy_from_weights(group_durations.values())
                best_groups = dict(group_counts)
        assert best_index >= 0
        incremental = max(0.0, best_uniform - previous_uniform)
        result.append(
            GreedyObservableStep(
                observable_id=observable_ids[best_index],
                incremental_uniform_bits=incremental,
                cumulative_uniform_bits=best_uniform,
                cumulative_duration_weighted_bits=best_duration,
                distinct_fingerprints=len(best_groups),
                largest_tie_group=max(best_groups.values()),
            )
        )
        selected.append(best_index)
        remaining.remove(best_index)
        previous_uniform = best_uniform
    return tuple(result)


def _entropy_from_weights(weights: Iterable[int | float]) -> float:
    values = tuple(float(weight) for weight in weights)
    total = sum(values)
    if total <= 0.0:
        raise ValueError("entropy weights require positive total")
    return -sum(
        (weight / total) * math.log2(weight / total)
        for weight in values
        if weight > 0.0
    )


def _canonical_channel(value: str) -> str:
    left_text, right_text = value.replace("/", "-").split("-", 1)
    left, right = sorted((int(left_text), int(right_text)))
    return f"{left}-{right}"
