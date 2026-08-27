"""Find the smallest cached structural fields that close survey-v2 residual ties.

This is a target-selection diagnostic only. Structural discrimination is not
behavioral validity; every selected field still requires a pre-existing HD claim
and a blind participant-observable operationalization before confirmatory use.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Hashable, Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.discrimination import FingerprintMetrics, summarize_fingerprints
from hdmatch.evaluation.survey_v2_capacity import TARGET_FEATURES, _clean_observable_patterns
from hdmatch.schemas import CandidateState, StructuralChartFeatures


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class CompletionStep(_FrozenModel):
    feature_id: str
    incremental_uniform_bits: float = Field(ge=0.0)
    cumulative_uniform_bits: float = Field(ge=0.0)
    unique_fingerprints: int = Field(ge=1)
    uniform_top1_ceiling: float = Field(ge=0.0, le=1.0)
    tie_size_max: int = Field(ge=1)


class SurveyV2CompletionAudit(_FrozenModel):
    schema_version: str = "survey-v2-completion-audit-v1"
    candidate_count: int = Field(ge=1)
    survey_v2_baseline: FingerprintMetrics
    full_cached_structure: FingerprintMetrics
    cached_structure_can_uniquely_identify_all_states: bool
    greedy_completion: tuple[CompletionStep, ...]


def audit_survey_v2_completion(
    states: Sequence[CandidateState], model: Mapping[str, Any]
) -> SurveyV2CompletionAudit:
    if not states:
        raise ValueError("survey-v2 completion audit requires candidate states")
    structural = tuple(_require_structural(state) for state in states)
    durations = tuple((state.end_utc - state.start_utc).total_seconds() for state in states)
    base = _clean_observable_patterns(structural, model)
    target_values = {
        feature: _value_vector(structural, feature) for feature in TARGET_FEATURES
    }
    survey_v2: tuple[Hashable, ...] = tuple(
        (base[index],) + tuple(target_values[feature][index] for feature in TARGET_FEATURES)
        for index in range(len(states))
    )
    baseline = summarize_fingerprints(survey_v2, durations)

    full = tuple(_full_structural_key(features) for features in structural)
    full_metrics = summarize_fingerprints(full, durations)

    activation_keys = tuple(
        sorted({key for features in structural for key in features.activation_gates})
    )
    already_targeted = {feature for feature in TARGET_FEATURES if feature != "channels"}
    feature_vectors: dict[str, tuple[Hashable, ...]] = {
        "profile": tuple(features.profile for features in structural),
        "definition": tuple(features.definition for features in structural),
        "defined_centers": tuple(tuple(sorted(features.defined_centers)) for features in structural),
        "type": tuple(features.type for features in structural),
        "authority": tuple(features.authority for features in structural),
    }
    for key in activation_keys:
        if key not in already_targeted:
            feature_vectors[f"activation:{key}"] = tuple(
                features.activation_gates.get(key) for features in structural
            )

    # Collapse the already-rich survey fingerprint to compact integer group ids.
    # Candidate fields only need to split the residual tie groups, so repeated
    # hashing of the full nested V3.6+v2 fingerprint is unnecessary.
    current_labels = _labels_for(survey_v2)
    current_metrics = summarize_fingerprints(current_labels, durations)
    remaining = set(feature_vectors)
    steps: list[CompletionStep] = []
    while remaining and current_metrics.unique_fingerprints < len(states):
        choices: list[tuple[float, str]] = []
        for feature in sorted(remaining):
            values = feature_vectors[feature]
            counts = Counter(zip(current_labels, values, strict=True))
            choices.append((_entropy_from_counts(counts.values(), len(states)), feature))

        best_bits, feature = max(choices, key=lambda item: (item[0], item[1]))
        values = feature_vectors[feature]
        next_labels = _labels_for(tuple(zip(current_labels, values, strict=True)))
        metrics = summarize_fingerprints(next_labels, durations)
        gain = max(0.0, best_bits - current_metrics.uniform_information_bits)
        steps.append(
            CompletionStep(
                feature_id=feature,
                incremental_uniform_bits=gain,
                cumulative_uniform_bits=metrics.uniform_information_bits,
                unique_fingerprints=metrics.unique_fingerprints,
                uniform_top1_ceiling=metrics.uniform_top1_ceiling,
                tie_size_max=metrics.tie_size_max,
            )
        )
        remaining.remove(feature)
        current_labels = next_labels
        current_metrics = metrics
        if gain <= 1e-15:
            break

    return SurveyV2CompletionAudit(
        candidate_count=len(states),
        survey_v2_baseline=baseline,
        full_cached_structure=full_metrics,
        cached_structure_can_uniquely_identify_all_states=(
            full_metrics.unique_fingerprints == len(states)
        ),
        greedy_completion=tuple(steps),
    )


def _labels_for(fingerprints: Sequence[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for fingerprint in fingerprints:
        label = labels.get(fingerprint)
        if label is None:
            label = len(labels) + 1
            labels[fingerprint] = label
        result.append(label)
    return tuple(result)


def _entropy_from_counts(counts: Sequence[int], total: int) -> float:
    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts
        if count > 0
    )


def _value_vector(
    structural: Sequence[StructuralChartFeatures], feature: str
) -> tuple[Hashable, ...]:
    if feature == "channels":
        return tuple(tuple(sorted(item.channels)) for item in structural)
    return tuple(item.activation_gates.get(feature) for item in structural)


def _full_structural_key(features: StructuralChartFeatures) -> Hashable:
    return (
        features.type,
        features.strategy,
        features.authority,
        features.profile,
        features.definition,
        tuple(sorted(features.defined_centers)),
        tuple(sorted(features.channels)),
        tuple(sorted(features.activation_gates.items())),
    )


def _require_structural(state: CandidateState) -> StructuralChartFeatures:
    if not isinstance(state.chart_features, StructuralChartFeatures):
        raise ValueError("survey-v2 completion audit requires structural chart features")
    return state.chart_features
