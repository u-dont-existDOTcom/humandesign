"""Perfect-match recoverability audit for the frozen survey-v2 architecture.

This module tests an engineering property, not a claim about people: when the
answer oracle returns exactly the chart-predicted labels, a candidate-blind,
predeclared adaptive policy must reduce every candidate's tie set to one.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Hashable, Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.evaluation.survey_v2_capacity import TARGET_FEATURES, _clean_observable_patterns
from hdmatch.schemas import CandidateState, StructuralChartFeatures


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class PerfectMatchRecoverabilityAudit(_FrozenModel):
    schema_version: str = "survey-v2-perfect-match-recoverability-v1"
    candidate_count: int = Field(ge=1)
    recovered_rank1_count: int = Field(ge=0)
    recovered_rank1_fraction: float = Field(ge=0.0, le=1.0)
    all_candidates_recover_rank1: bool
    all_candidates_uniquely_recovered: bool
    unresolved_candidate_count: int = Field(ge=0)
    maximum_questions_asked: int = Field(ge=0)
    mean_questions_asked: float = Field(ge=0.0)
    question_count_p50: int = Field(ge=0)
    question_count_p90: int = Field(ge=0)
    allowed_tie_breakers: tuple[str, ...]
    selection_uses_birth_metadata: bool = False
    selection_uses_candidate_rank: bool = False
    claim_scope: str = "structural_recoverability_only_not_empirical_human_accuracy"


# Frozen before human evaluation. Profile is asked first because it has by far
# the largest residual global gain. Remaining fields are eligible only as blind,
# conditional tie-breakers. Values are gate archetypes, not birth metadata.
DEFAULT_TIE_BREAKERS = (
    "profile",
    "activation:personality:mars",
    "activation:design:mars",
    "activation:design:jupiter",
    "activation:personality:jupiter",
    "activation:design:saturn",
    "activation:personality:saturn",
    "activation:design:uranus",
    "activation:personality:uranus",
    "activation:personality:south_node",
    "activation:design:south_node",
    "activation:design:pluto",
    "activation:personality:neptune",
    "activation:design:neptune",
    "activation:personality:pluto",
)


def audit_perfect_match_recoverability(
    states: Sequence[CandidateState],
    model: Mapping[str, Any],
    *,
    allowed_tie_breakers: Sequence[str] = DEFAULT_TIE_BREAKERS,
) -> PerfectMatchRecoverabilityAudit:
    """Simulate perfect answers through a candidate-blind adaptive decision tree."""
    if not states:
        raise ValueError("perfect-match recoverability audit requires candidate states")
    if len(set(allowed_tie_breakers)) != len(allowed_tie_breakers):
        raise ValueError("tie-breakers must be unique")

    structural = tuple(_require_structural(state) for state in states)
    base = _clean_observable_patterns(structural, model)
    target_values = {
        feature: _value_vector(structural, feature) for feature in TARGET_FEATURES
    }
    baseline: tuple[Hashable, ...] = tuple(
        (base[index],) + tuple(target_values[feature][index] for feature in TARGET_FEATURES)
        for index in range(len(states))
    )
    vectors = {
        feature: _tie_breaker_vector(structural, feature)
        for feature in allowed_tie_breakers
    }

    question_counts = [0] * len(states)
    unresolved: set[int] = set()
    initial_groups: dict[Hashable, list[int]] = {}
    for index, fingerprint in enumerate(baseline):
        initial_groups.setdefault(fingerprint, []).append(index)
    for indices in initial_groups.values():
        _resolve_group(
            tuple(indices),
            tuple(allowed_tie_breakers),
            vectors,
            question_counts,
            unresolved,
        )

    recovered = len(states) - len(unresolved)
    ordered_counts = sorted(question_counts)
    return PerfectMatchRecoverabilityAudit(
        candidate_count=len(states),
        recovered_rank1_count=recovered,
        recovered_rank1_fraction=recovered / len(states),
        all_candidates_recover_rank1=recovered == len(states),
        all_candidates_uniquely_recovered=recovered == len(states),
        unresolved_candidate_count=len(unresolved),
        maximum_questions_asked=max(question_counts),
        mean_questions_asked=sum(question_counts) / len(states),
        question_count_p50=_percentile(ordered_counts, 0.50),
        question_count_p90=_percentile(ordered_counts, 0.90),
        allowed_tie_breakers=tuple(allowed_tie_breakers),
    )


def _resolve_group(
    indices: tuple[int, ...],
    remaining: tuple[str, ...],
    vectors: Mapping[str, tuple[Hashable, ...]],
    question_counts: list[int],
    unresolved: set[int],
) -> None:
    if len(indices) == 1:
        return
    choices: list[tuple[float, int, str]] = []
    for order, feature in enumerate(remaining):
        counts = Counter(vectors[feature][index] for index in indices)
        entropy = -sum(
            (count / len(indices)) * math.log2(count / len(indices))
            for count in counts.values()
        )
        choices.append((entropy, -order, feature))
    if not choices:
        unresolved.update(indices)
        return
    entropy, _, feature = max(choices)
    if entropy <= 0.0:
        unresolved.update(indices)
        return
    next_remaining = tuple(item for item in remaining if item != feature)
    children: dict[Hashable, list[int]] = {}
    for index in indices:
        question_counts[index] += 1
        children.setdefault(vectors[feature][index], []).append(index)
    for child in children.values():
        _resolve_group(
            tuple(child), next_remaining, vectors, question_counts, unresolved
        )


def _tie_breaker_vector(
    structural: Sequence[StructuralChartFeatures], feature: str
) -> tuple[Hashable, ...]:
    if feature == "profile":
        return tuple(item.profile for item in structural)
    if feature.startswith("activation:"):
        key = feature.removeprefix("activation:")
        return tuple(item.activation_gates.get(key) for item in structural)
    raise ValueError(f"unsupported tie-breaker: {feature}")


def _value_vector(
    structural: Sequence[StructuralChartFeatures], feature: str
) -> tuple[Hashable, ...]:
    if feature == "channels":
        return tuple(tuple(sorted(item.channels)) for item in structural)
    return tuple(item.activation_gates.get(feature) for item in structural)


def _percentile(ordered: Sequence[int], fraction: float) -> int:
    return ordered[max(0, math.ceil(len(ordered) * fraction) - 1)]


def _require_structural(state: CandidateState) -> StructuralChartFeatures:
    if not isinstance(state.chart_features, StructuralChartFeatures):
        raise ValueError("recoverability audit requires structural chart features")
    return state.chart_features
