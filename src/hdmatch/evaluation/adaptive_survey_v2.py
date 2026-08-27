"""Template-driven adaptive survey v2 and century discrimination audit.

The v2 bank turns pre-existing gate/channel meanings into candidate-blind questions.
Capacity metrics describe deterministic predicted-claim partitions only. They are
not empirical evidence that Human Design predicts behavior.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.discrimination import FingerprintMetrics, summarize_fingerprints
from hdmatch.evaluation.holistic_profile_information import observable_id, predicate_matches
from hdmatch.runtime.century_cache import CenturyCacheManifest
from hdmatch.schemas import CandidateState, StructuralChartFeatures


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


@dataclass(frozen=True, slots=True)
class AdaptiveSurveyV2Item:
    question_id: str
    kind: Literal["planet_gate", "channel"]
    family: str
    construct: str
    prompt: str
    response_format: str
    followups: tuple[str, ...]
    reliability: float
    side: str | None = None
    body: str | None = None
    gate: int | None = None
    channel: str | None = None


class V2FamilyMetric(_FrozenModel):
    family_id: str
    incremental_uniform_bits: float = Field(ge=0.0)
    incremental_duration_weighted_bits: float = Field(ge=0.0)
    combined: FingerprintMetrics


class V2GreedyStep(_FrozenModel):
    family_id: str
    incremental_uniform_bits: float = Field(ge=0.0)
    cumulative_uniform_bits: float = Field(ge=0.0)
    cumulative_duration_weighted_bits: float = Field(ge=0.0)
    unique_fingerprints: int = Field(ge=1)
    tie_size_p50: int = Field(ge=1)
    tie_size_p95: int = Field(ge=1)
    tie_size_max: int = Field(ge=1)


class AdaptiveSurveyV2Audit(_FrozenModel):
    schema_version: str = "adaptive-survey-v2-capacity-audit-v1"
    cache_interval_count: int = Field(ge=1)
    cache_engine_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    cache_canonical_rows_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    generated_item_count: int = Field(ge=1)
    planet_gate_item_count: int = Field(ge=1)
    channel_item_count: int = Field(ge=1)
    baseline_observable_count: int = Field(ge=1)
    baseline: FingerprintMetrics
    family_metrics: tuple[V2FamilyMetric, ...]
    greedy_family_sequence: tuple[V2GreedyStep, ...]
    full_v2: FingerprintMetrics
    remaining_uniform_identity_gap_bits: float = Field(ge=0.0)
    exact_interval_identity_reached: bool


def load_adaptive_v2_items(
    *,
    gate_catalog_path: str | Path,
    channel_catalog_path: str | Path,
    planet_roles_path: str | Path,
) -> tuple[AdaptiveSurveyV2Item, ...]:
    gates_doc = _load_json(gate_catalog_path)
    channels_doc = _load_json(channel_catalog_path)
    roles_doc = _load_json(planet_roles_path)

    gates = tuple(gates_doc["gates"])
    channels = tuple(channels_doc["channels"])
    roles = roles_doc["roles"]
    sides = roles_doc["sides"]
    shared_followups = tuple(str(item) for item in roles_doc["shared_followups"])
    design_followup = str(roles_doc["design_side_followup"])
    response_format = _response_format(roles_doc["response_scale"])

    if {int(item["gate"]) for item in gates} != set(range(1, 65)):
        raise ValueError("v2 gate catalog must contain each gate 1 through 64 exactly once")
    bodies = ("sun", "earth", "moon", "mercury", "venus", "mars")
    if set(roles) != set(bodies):
        raise ValueError("v2 planet role catalog must define exactly the six preregistered bodies")
    if set(sides) != {"personality", "design"}:
        raise ValueError("v2 planet role catalog must define personality and design sides")

    items: list[AdaptiveSurveyV2Item] = []
    for side in ("personality", "design"):
        for body in bodies:
            role = roles[body]
            for gate_record in gates:
                gate = int(gate_record["gate"])
                theme_clause = str(gate_record["theme_clause"])
                followups = shared_followups
                reliability = 0.80
                if side == "design":
                    followups = (*followups, design_followup)
                    reliability = 0.70
                items.append(
                    AdaptiveSurveyV2Item(
                        question_id=_opaque_question_id(
                            f"planet|{side}|{body}|{gate}"
                        ),
                        kind="planet_gate",
                        family=body,
                        construct=f"{role['construct']}: {gate_record['construct']}",
                        prompt=str(role["prompt_template"]).format(
                            theme_clause=theme_clause
                        ),
                        response_format=response_format,
                        followups=followups,
                        reliability=reliability,
                        side=side,
                        body=body,
                        gate=gate,
                    )
                )

    channel_response_format = _response_format(channels_doc["response_scale"])
    channel_followups = tuple(str(item) for item in channels_doc["followups"])
    for record in channels:
        channel = _canonical_channel(str(record["channel"]))
        items.append(
            AdaptiveSurveyV2Item(
                question_id=_opaque_question_id(f"channel|{channel}"),
                kind="channel",
                family="channels",
                construct=str(record["construct"]),
                prompt=str(channels_doc["question_template"]).format(
                    theme_clause=str(record["theme_clause"])
                ),
                response_format=channel_response_format,
                followups=channel_followups,
                reliability=0.80,
                channel=channel,
            )
        )

    question_ids = [item.question_id for item in items]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("opaque v2 question IDs collided")
    if len(items) != 804:
        raise ValueError(f"expected 804 v2 items, got {len(items)}")
    return tuple(items)


def audit_adaptive_survey_v2(
    states: Sequence[CandidateState],
    manifest: CenturyCacheManifest,
    v36_model: Mapping[str, Any],
    items: Sequence[AdaptiveSurveyV2Item],
) -> AdaptiveSurveyV2Audit:
    if not states:
        raise ValueError("adaptive survey v2 audit requires candidate states")
    if len(states) != manifest.interval_count:
        raise ValueError("candidate state count does not match century-cache manifest")

    structural = tuple(_require_structural(state) for state in states)
    durations = tuple((state.end_utc - state.start_utc).total_seconds() for state in states)
    baseline, observable_count = _clean_observable_patterns(structural, v36_model)
    baseline_metrics = summarize_fingerprints(baseline, durations)

    family_values = {
        "moon": _planet_pair_values(structural, ("moon",)),
        "channels": tuple(_channels_value(features) for features in structural),
        "mercury": _planet_pair_values(structural, ("mercury",)),
        "venus": _planet_pair_values(structural, ("venus",)),
        "sun_earth": _planet_pair_values(structural, ("sun", "earth")),
        "mars": _planet_pair_values(structural, ("mars",)),
    }
    family_metrics = tuple(
        _family_metric(
            family_id=family_id,
            baseline=baseline,
            values=values,
            durations=durations,
            baseline_metrics=baseline_metrics,
        )
        for family_id, values in family_values.items()
    )

    greedy = _greedy_family_sequence(
        baseline=baseline,
        family_values=family_values,
        durations=durations,
    )
    all_planet_values = _planet_pair_values(
        structural, ("sun", "earth", "moon", "mercury", "venus", "mars")
    )
    full_values = tuple(
        (planet_value, _channels_value(features))
        for planet_value, features in zip(all_planet_values, structural, strict=True)
    )
    full_fingerprint = tuple(
        (base, value) for base, value in zip(baseline, full_values, strict=True)
    )
    full_metrics = summarize_fingerprints(full_fingerprint, durations)
    identity_gap = max(
        0.0, full_metrics.maximum_identity_bits - full_metrics.uniform_information_bits
    )
    planet_items = sum(item.kind == "planet_gate" for item in items)
    channel_items = sum(item.kind == "channel" for item in items)

    return AdaptiveSurveyV2Audit(
        cache_interval_count=manifest.interval_count,
        cache_engine_fingerprint=manifest.engine_fingerprint,
        cache_canonical_rows_sha256=manifest.canonical_rows_sha256,
        generated_item_count=len(items),
        planet_gate_item_count=planet_items,
        channel_item_count=channel_items,
        baseline_observable_count=observable_count,
        baseline=baseline_metrics,
        family_metrics=family_metrics,
        greedy_family_sequence=greedy,
        full_v2=full_metrics,
        remaining_uniform_identity_gap_bits=identity_gap,
        exact_interval_identity_reached=full_metrics.unique_fingerprints == len(states),
    )


def select_structural_split_item(
    *,
    states: Sequence[CandidateState],
    weights: Sequence[float],
    items: Sequence[AdaptiveSurveyV2Item],
    answered_question_ids: frozenset[str],
) -> tuple[AdaptiveSurveyV2Item, float] | None:
    """Choose the frozen item with maximum reliability-adjusted binary split entropy.

    This utility does not use participant answers to invent mappings. A non-carrier
    state is neutral rather than predicted-negative; the entropy is therefore only
    a candidate-partition engineering score.
    """

    if len(states) != len(weights):
        raise ValueError("state and weight counts differ")
    total_weight = sum(max(0.0, weight) for weight in weights)
    if total_weight <= 0.0:
        raise ValueError("adaptive selection requires positive candidate weight")

    best: tuple[AdaptiveSurveyV2Item, float] | None = None
    for item in items:
        if item.question_id in answered_question_ids:
            continue
        carrier_weight = 0.0
        for state, raw_weight in zip(states, weights, strict=True):
            weight = max(0.0, raw_weight)
            if weight and item_matches(_require_structural(state), item):
                carrier_weight += weight
        probability = carrier_weight / total_weight
        if probability <= 0.0 or probability >= 1.0:
            continue
        entropy = _binary_entropy(probability) * item.reliability
        if best is None or entropy > best[1] or (
            math.isclose(entropy, best[1]) and item.question_id < best[0].question_id
        ):
            best = (item, entropy)
    return best


def item_matches(
    features: StructuralChartFeatures,
    item: AdaptiveSurveyV2Item,
) -> bool:
    if item.kind == "planet_gate":
        assert item.side is not None
        assert item.body is not None
        assert item.gate is not None
        return features.activation_gates.get(f"{item.side}:{item.body}") == item.gate
    assert item.channel is not None
    return item.channel in {_canonical_channel(channel) for channel in features.channels}


def _family_metric(
    *,
    family_id: str,
    baseline: Sequence[Hashable],
    values: Sequence[Hashable],
    durations: Sequence[float],
    baseline_metrics: FingerprintMetrics,
) -> V2FamilyMetric:
    combined = tuple(zip(baseline, values, strict=True))
    metrics = summarize_fingerprints(combined, durations)
    return V2FamilyMetric(
        family_id=family_id,
        incremental_uniform_bits=max(
            0.0, metrics.uniform_information_bits - baseline_metrics.uniform_information_bits
        ),
        incremental_duration_weighted_bits=max(
            0.0,
            metrics.duration_weighted_information_bits
            - baseline_metrics.duration_weighted_information_bits,
        ),
        combined=metrics,
    )


def _greedy_family_sequence(
    *,
    baseline: Sequence[Hashable],
    family_values: Mapping[str, Sequence[Hashable]],
    durations: Sequence[float],
) -> tuple[V2GreedyStep, ...]:
    remaining = set(family_values)
    current: tuple[Hashable, ...] = tuple(baseline)
    current_metrics = summarize_fingerprints(current, durations)
    steps: list[V2GreedyStep] = []

    while remaining:
        candidates: list[
            tuple[float, str, tuple[Hashable, ...], FingerprintMetrics]
        ] = []
        for family_id in sorted(remaining):
            values = family_values[family_id]
            combined_pattern: tuple[Hashable, ...] = tuple(
                (left, right)
                for left, right in zip(current, values, strict=True)
            )
            metrics = summarize_fingerprints(combined_pattern, durations)
            gain = max(
                0.0,
                metrics.uniform_information_bits - current_metrics.uniform_information_bits,
            )
            candidates.append((gain, family_id, combined_pattern, metrics))
        gain, family_id, selected_pattern, metrics = max(
            candidates, key=lambda item: (item[0], item[1])
        )
        remaining.remove(family_id)
        current = selected_pattern
        current_metrics = metrics
        steps.append(
            V2GreedyStep(
                family_id=family_id,
                incremental_uniform_bits=gain,
                cumulative_uniform_bits=metrics.uniform_information_bits,
                cumulative_duration_weighted_bits=metrics.duration_weighted_information_bits,
                unique_fingerprints=metrics.unique_fingerprints,
                tie_size_p50=metrics.tie_size_p50,
                tie_size_p95=metrics.tie_size_p95,
                tie_size_max=metrics.tie_size_max,
            )
        )
    return tuple(steps)


def _planet_pair_values(
    structural: Sequence[StructuralChartFeatures],
    bodies: Sequence[str],
) -> tuple[Hashable, ...]:
    keys = tuple(
        f"{side}:{body}"
        for body in bodies
        for side in ("personality", "design")
    )
    return tuple(
        tuple((key, features.activation_gates.get(key)) for key in keys)
        for features in structural
    )


def _channels_value(features: StructuralChartFeatures) -> tuple[str, ...]:
    return tuple(sorted({_canonical_channel(channel) for channel in features.channels}))


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


def _load_json(path: str | Path) -> Mapping[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping):
        raise ValueError(f"expected JSON object in {path}")
    return raw


def _response_format(records: object) -> str:
    if not isinstance(records, list):
        raise ValueError("response_scale must be a JSON list")
    labels = []
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("response_scale entries must be JSON objects")
        labels.append(str(record["label"]))
    return " / ".join(labels)


def _opaque_question_id(seed: str) -> str:
    return "Q2-" + sha256(seed.encode("utf-8")).hexdigest()[:16].upper()


def _canonical_channel(raw_channel: str) -> str:
    parts = raw_channel.replace("/", "-").split("-")
    if len(parts) != 2:
        raise ValueError(f"invalid channel identifier: {raw_channel!r}")
    left, right = (int(part.strip()) for part in parts)
    if left == right or not (1 <= left <= 64 and 1 <= right <= 64):
        raise ValueError(f"invalid channel identifier: {raw_channel!r}")
    first, second = sorted((left, right))
    return f"{first}-{second}"


def _binary_entropy(probability: float) -> float:
    return -probability * math.log2(probability) - (1.0 - probability) * math.log2(
        1.0 - probability
    )


def _require_structural(state: CandidateState) -> StructuralChartFeatures:
    if not isinstance(state.chart_features, StructuralChartFeatures):
        raise ValueError("adaptive survey v2 requires structural chart features")
    return state.chart_features
