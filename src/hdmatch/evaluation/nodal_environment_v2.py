"""Secondary nodal environment/perspective survey layer and capacity audit.

This module intentionally keeps nodal claims separate from the primary natal
trait/behavior score.  The deterministic capacity audit asks whether the official
HD environment/perspective claims can resolve structural ties left by the primary
v2 bank; it is not empirical validation of those claims.
"""

from __future__ import annotations

import json
import math
from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.adaptive_survey_v2 import PRIMARY_NATAL_BODIES
from hdmatch.evaluation.discrimination import FingerprintMetrics, summarize_fingerprints
from hdmatch.evaluation.holistic_profile_information import observable_id, predicate_matches
from hdmatch.runtime.century_cache import CenturyCacheManifest
from hdmatch.schemas import CandidateState, StructuralChartFeatures


NODE_KEYS: tuple[str, ...] = (
    "design:south_node",
    "design:north_node",
    "personality:south_node",
    "personality:north_node",
)


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


@dataclass(frozen=True, slots=True)
class NodalEnvironmentV2Item:
    question_id: str
    side: Literal["design", "personality"]
    node: Literal["south_node", "north_node"]
    gate: int
    domain: Literal["environment", "perspective"]
    life_stage: Literal["earlier_life", "later_life_or_emerging"]
    construct: str
    prompt: str
    response_format: str
    followups: tuple[str, ...]
    reliability: float


class NodalFamilyMetric(_FrozenModel):
    family_id: str
    incremental_uniform_bits: float = Field(ge=0.0)
    incremental_duration_weighted_bits: float = Field(ge=0.0)
    combined: FingerprintMetrics


class NodalEnvironmentV2Audit(_FrozenModel):
    schema_version: str = "nodal-environment-v2-capacity-audit-v1"
    cache_interval_count: int = Field(ge=1)
    cache_engine_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    cache_canonical_rows_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    generated_item_count: int = Field(ge=1)
    primary: FingerprintMetrics
    family_metrics: tuple[NodalFamilyMetric, ...]
    primary_plus_nodes: FingerprintMetrics
    incremental_uniform_bits: float = Field(ge=0.0)
    incremental_duration_weighted_bits: float = Field(ge=0.0)
    remaining_uniform_identity_gap_bits: float = Field(ge=0.0)
    exact_interval_identity_reached: bool


def load_nodal_environment_v2_items(
    *,
    gate_catalog_path: str | Path,
    nodal_roles_path: str | Path,
) -> tuple[NodalEnvironmentV2Item, ...]:
    gates_doc = _load_json(gate_catalog_path)
    roles_doc = _load_json(nodal_roles_path)
    gates = tuple(gates_doc["gates"])
    roles = roles_doc["roles"]
    if {int(item["gate"]) for item in gates} != set(range(1, 65)):
        raise ValueError("nodal v2 gate catalog must contain each gate 1 through 64")
    if set(roles) != set(NODE_KEYS):
        raise ValueError("nodal v2 role catalog must define all four side/node roles")
    response_format = _response_format(roles_doc["response_scale"])
    followups = tuple(str(item) for item in roles_doc["shared_followups"])

    items: list[NodalEnvironmentV2Item] = []
    for raw_key in NODE_KEYS:
        side, node = raw_key.split(":", 1)
        role = roles[raw_key]
        for gate_record in gates:
            gate = int(gate_record["gate"])
            items.append(
                NodalEnvironmentV2Item(
                    question_id=_opaque_question_id(f"node|{side}|{node}|{gate}"),
                    side=side,  # type: ignore[arg-type]
                    node=node,  # type: ignore[arg-type]
                    gate=gate,
                    domain=str(role["domain"]),  # type: ignore[arg-type]
                    life_stage=str(role["life_stage"]),  # type: ignore[arg-type]
                    construct=f"{role['domain']}: {gate_record['construct']}",
                    prompt=str(role["prompt_template"]).format(
                        theme_clause=str(gate_record["theme_clause"])
                    ),
                    response_format=response_format,
                    followups=followups,
                    reliability=0.60 if node == "north_node" else 0.75,
                )
            )
    question_ids = [item.question_id for item in items]
    if len(items) != 256 or len(question_ids) != len(set(question_ids)):
        raise ValueError("nodal v2 item generation must yield 256 unique questions")
    return tuple(items)


def audit_nodal_environment_v2(
    states: Sequence[CandidateState],
    manifest: CenturyCacheManifest,
    v36_model: Mapping[str, Any],
    items: Sequence[NodalEnvironmentV2Item],
) -> NodalEnvironmentV2Audit:
    if not states:
        raise ValueError("nodal v2 audit requires candidate states")
    if len(states) != manifest.interval_count:
        raise ValueError("candidate state count does not match century-cache manifest")
    structural = tuple(_require_structural(state) for state in states)
    durations = tuple((state.end_utc - state.start_utc).total_seconds() for state in states)
    baseline = _clean_observable_patterns(structural, v36_model)
    primary_planets = _activation_vector(structural, PRIMARY_NATAL_BODIES)
    primary_values = tuple(
        (planet_values, _channels_value(features))
        for planet_values, features in zip(primary_planets, structural, strict=True)
    )
    primary_fingerprint: tuple[Hashable, ...] = tuple(
        (base, value) for base, value in zip(baseline, primary_values, strict=True)
    )
    primary_metrics = summarize_fingerprints(primary_fingerprint, durations)

    families: dict[str, tuple[Hashable, ...]] = {
        "design_nodes": _activation_keys(
            structural, ("design:south_node", "design:north_node")
        ),
        "personality_nodes": _activation_keys(
            structural, ("personality:south_node", "personality:north_node")
        ),
        "south_nodes": _activation_keys(
            structural, ("design:south_node", "personality:south_node")
        ),
        "north_nodes": _activation_keys(
            structural, ("design:north_node", "personality:north_node")
        ),
    }
    family_metrics = tuple(
        _family_metric(
            family_id=family_id,
            primary=primary_fingerprint,
            values=values,
            durations=durations,
            primary_metrics=primary_metrics,
        )
        for family_id, values in families.items()
    )

    all_nodes = _activation_keys(structural, NODE_KEYS)
    combined: tuple[Hashable, ...] = tuple(
        (primary_value, node_value)
        for primary_value, node_value in zip(primary_fingerprint, all_nodes, strict=True)
    )
    combined_metrics = summarize_fingerprints(combined, durations)
    return NodalEnvironmentV2Audit(
        cache_interval_count=manifest.interval_count,
        cache_engine_fingerprint=manifest.engine_fingerprint,
        cache_canonical_rows_sha256=manifest.canonical_rows_sha256,
        generated_item_count=len(items),
        primary=primary_metrics,
        family_metrics=family_metrics,
        primary_plus_nodes=combined_metrics,
        incremental_uniform_bits=max(
            0.0,
            combined_metrics.uniform_information_bits
            - primary_metrics.uniform_information_bits,
        ),
        incremental_duration_weighted_bits=max(
            0.0,
            combined_metrics.duration_weighted_information_bits
            - primary_metrics.duration_weighted_information_bits,
        ),
        remaining_uniform_identity_gap_bits=max(
            0.0,
            combined_metrics.maximum_identity_bits
            - combined_metrics.uniform_information_bits,
        ),
        exact_interval_identity_reached=combined_metrics.unique_fingerprints == len(states),
    )


def select_nodal_split_item(
    *,
    states: Sequence[CandidateState],
    weights: Sequence[float],
    items: Sequence[NodalEnvironmentV2Item],
    answered_question_ids: frozenset[str],
) -> tuple[NodalEnvironmentV2Item, float] | None:
    """Select a frozen secondary-layer item by reliability-adjusted split entropy."""

    if len(states) != len(weights):
        raise ValueError("state and weight counts differ")
    total = sum(max(0.0, weight) for weight in weights)
    if total <= 0.0:
        raise ValueError("nodal selection requires positive candidate weight")
    best: tuple[NodalEnvironmentV2Item, float] | None = None
    for item in items:
        if item.question_id in answered_question_ids:
            continue
        carrier = sum(
            max(0.0, weight)
            for state, weight in zip(states, weights, strict=True)
            if item_matches(_require_structural(state), item)
        )
        probability = carrier / total
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
    item: NodalEnvironmentV2Item,
) -> bool:
    return features.activation_gates.get(f"{item.side}:{item.node}") == item.gate


def _family_metric(
    *,
    family_id: str,
    primary: Sequence[Hashable],
    values: Sequence[Hashable],
    durations: Sequence[float],
    primary_metrics: FingerprintMetrics,
) -> NodalFamilyMetric:
    combined: tuple[Hashable, ...] = tuple(
        (left, right) for left, right in zip(primary, values, strict=True)
    )
    metrics = summarize_fingerprints(combined, durations)
    return NodalFamilyMetric(
        family_id=family_id,
        incremental_uniform_bits=max(
            0.0, metrics.uniform_information_bits - primary_metrics.uniform_information_bits
        ),
        incremental_duration_weighted_bits=max(
            0.0,
            metrics.duration_weighted_information_bits
            - primary_metrics.duration_weighted_information_bits,
        ),
        combined=metrics,
    )


def _clean_observable_patterns(
    structural: Sequence[StructuralChartFeatures],
    model: Mapping[str, Any],
) -> tuple[Hashable, ...]:
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
    by_observable: dict[str, list[Mapping[str, Any]]] = {}
    for mapping in mappings:
        by_observable.setdefault(observable_id(mapping), []).append(mapping)
    result: list[Hashable] = []
    for features in structural:
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
        result.append(tuple(values))
    return tuple(result)


def _activation_vector(
    structural: Sequence[StructuralChartFeatures], bodies: Sequence[str]
) -> tuple[Hashable, ...]:
    keys = tuple(
        f"{side}:{body}"
        for body in bodies
        for side in ("personality", "design")
    )
    return _activation_keys(structural, keys)


def _activation_keys(
    structural: Sequence[StructuralChartFeatures], keys: Sequence[str]
) -> tuple[Hashable, ...]:
    return tuple(
        tuple((key, features.activation_gates.get(key)) for key in keys)
        for features in structural
    )


def _channels_value(features: StructuralChartFeatures) -> tuple[str, ...]:
    return tuple(sorted(_canonical_channel(channel) for channel in features.channels))


def _canonical_channel(raw_channel: str) -> str:
    parts = raw_channel.replace("/", "-").split("-")
    if len(parts) != 2:
        raise ValueError(f"invalid channel identifier: {raw_channel!r}")
    left, right = (int(part.strip()) for part in parts)
    first, second = sorted((left, right))
    return f"{first}-{second}"


def _load_json(path: str | Path) -> Mapping[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping):
        raise ValueError(f"expected JSON object in {path}")
    return raw


def _response_format(records: object) -> str:
    if not isinstance(records, list):
        raise ValueError("response_scale must be a JSON list")
    labels: list[str] = []
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("response_scale entries must be JSON objects")
        labels.append(str(record["label"]))
    return " / ".join(labels)


def _opaque_question_id(seed: str) -> str:
    return "Q2N-" + sha256(seed.encode("utf-8")).hexdigest()[:16].upper()


def _binary_entropy(probability: float) -> float:
    return -probability * math.log2(probability) - (1.0 - probability) * math.log2(
        1.0 - probability
    )


def _require_structural(state: CandidateState) -> StructuralChartFeatures:
    if not isinstance(state.chart_features, StructuralChartFeatures):
        raise ValueError("nodal v2 requires structural chart features")
    return state.chart_features
