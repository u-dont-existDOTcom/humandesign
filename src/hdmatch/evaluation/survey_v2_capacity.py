"""Joint structural ceiling for the proposed survey-v2 behavioral domains.

This is not a behavioral-validity estimate. It asks how much candidate-state
identity would be available if narrative classification of each proposed domain
were perfect. The calculation conditions on the clean V3.6 participant-observable
fingerprint so correlated information is not double-counted.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.discrimination import FingerprintMetrics, summarize_fingerprints
from hdmatch.evaluation.holistic_profile_information import observable_id, predicate_matches
from hdmatch.schemas import CandidateState, StructuralChartFeatures


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class SurveyV2TargetStep(_FrozenModel):
    feature_id: str
    incremental_uniform_bits: float = Field(ge=0.0)
    cumulative_uniform_bits: float = Field(ge=0.0)
    unique_fingerprints: int = Field(ge=1)
    uniform_top1_ceiling: float = Field(ge=0.0, le=1.0)
    reference_1985_tie_size: int = Field(ge=1)


class SurveyV2CapacityAudit(_FrozenModel):
    schema_version: str = "survey-v2-capacity-audit-v1"
    candidate_count: int = Field(ge=1)
    baseline: FingerprintMetrics
    joint_target: FingerprintMetrics
    incremental_uniform_bits: float = Field(ge=0.0)
    remaining_identity_gap_bits: float = Field(ge=0.0)
    reference_1985_baseline_tie_size: int = Field(ge=1)
    reference_1985_joint_tie_size: int = Field(ge=1)
    greedy_target_sequence: tuple[SurveyV2TargetStep, ...]


TARGET_FEATURES = (
    "personality:moon",
    "design:moon",
    "personality:mercury",
    "design:mercury",
    "personality:venus",
    "design:venus",
    "channels",
)


def audit_survey_v2_capacity(
    states: Sequence[CandidateState], model: Mapping[str, Any]
) -> SurveyV2CapacityAudit:
    if not states:
        raise ValueError("survey-v2 capacity audit requires candidate states")
    structural = tuple(_require_structural(state) for state in states)
    durations = tuple((state.end_utc - state.start_utc).total_seconds() for state in states)
    base = _clean_observable_patterns(structural, model)
    baseline = summarize_fingerprints(base, durations)
    values = {feature: _feature_values(structural, feature) for feature in TARGET_FEATURES}
    joint = tuple(
        (base[index],) + tuple(values[feature][index] for feature in TARGET_FEATURES)
        for index in range(len(states))
    )
    joint_metrics = summarize_fingerprints(joint, durations)
    maximum_identity_bits = baseline.maximum_identity_bits
    reference = datetime(1985, 1, 29, 0, 22, 30, tzinfo=UTC)
    ref_index = _reference_index(states, reference)
    base_ref_tie = _tie_size(base, ref_index)
    joint_ref_tie = _tie_size(joint, ref_index)

    selected: list[str] = []
    current = base
    current_metrics = baseline
    steps: list[SurveyV2TargetStep] = []
    remaining = set(TARGET_FEATURES)
    while remaining:
        choices = []
        for feature in sorted(remaining):
            candidate = tuple(
                (current[index], values[feature][index]) for index in range(len(states))
            )
            metrics = summarize_fingerprints(candidate, durations)
            choices.append((metrics.uniform_information_bits, feature, candidate, metrics))
        _, feature, candidate, metrics = max(choices, key=lambda item: (item[0], item[1]))
        steps.append(
            SurveyV2TargetStep(
                feature_id=feature,
                incremental_uniform_bits=max(
                    0.0,
                    metrics.uniform_information_bits - current_metrics.uniform_information_bits,
                ),
                cumulative_uniform_bits=metrics.uniform_information_bits,
                unique_fingerprints=metrics.unique_fingerprints,
                uniform_top1_ceiling=metrics.uniform_top1_ceiling,
                reference_1985_tie_size=_tie_size(candidate, ref_index),
            )
        )
        selected.append(feature)
        remaining.remove(feature)
        current = candidate
        current_metrics = metrics

    return SurveyV2CapacityAudit(
        candidate_count=len(states),
        baseline=baseline,
        joint_target=joint_metrics,
        incremental_uniform_bits=max(
            0.0, joint_metrics.uniform_information_bits - baseline.uniform_information_bits
        ),
        remaining_identity_gap_bits=max(
            0.0, maximum_identity_bits - joint_metrics.uniform_information_bits
        ),
        reference_1985_baseline_tie_size=base_ref_tie,
        reference_1985_joint_tie_size=joint_ref_tie,
        greedy_target_sequence=tuple(steps),
    )


def _clean_observable_patterns(
    structural: Sequence[StructuralChartFeatures], model: Mapping[str, Any]
) -> tuple[tuple[int, ...], ...]:
    mappings = tuple(mapping for mapping in model["mappings"] if not bool(mapping.get("post_selection", False)))
    contradictions = tuple(model.get("contradictions", ()))
    ids = tuple(
        sorted(
            {observable_id(mapping) for mapping in mappings}
            | {f"CONTRADICTION:{item['cluster']}" for item in contradictions}
        )
    )
    by_observable: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for mapping in mappings:
        by_observable[observable_id(mapping)].append(mapping)
    rows = []
    for features in structural:
        row = []
        for item_id in ids:
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
            row.append(1 if matched else 0)
        rows.append(tuple(row))
    return tuple(rows)


def _feature_values(
    structural: Sequence[StructuralChartFeatures], feature: str
) -> tuple[Hashable, ...]:
    if feature == "channels":
        return tuple(tuple(sorted(item.channels)) for item in structural)
    return tuple(item.activation_gates.get(feature) for item in structural)


def _require_structural(state: CandidateState) -> StructuralChartFeatures:
    if not isinstance(state.chart_features, StructuralChartFeatures):
        raise ValueError("survey-v2 capacity audit requires structural chart features")
    return state.chart_features


def _reference_index(states: Sequence[CandidateState], timestamp: datetime) -> int:
    for index, state in enumerate(states):
        if state.start_utc <= timestamp < state.end_utc:
            return index
    raise ValueError("reference timestamp not present in candidate universe")


def _tie_size(fingerprints: Sequence[Hashable], index: int) -> int:
    target = fingerprints[index]
    return sum(1 for fingerprint in fingerprints if fingerprint == target)
