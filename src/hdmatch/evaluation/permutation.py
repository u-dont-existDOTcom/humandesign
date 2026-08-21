"""Seeded, person-level, stratum-preserving permutation/null utilities."""

from __future__ import annotations

import math
import random
import statistics
from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class NullDistributionSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    permutations: int = Field(ge=1)
    observed_statistic: float
    null_mean: float
    null_standard_deviation: float = Field(ge=0.0)
    null_q025: float
    null_median: float
    null_q975: float
    p_value: float = Field(gt=0.0, le=1.0)
    alternative: Literal["greater", "less", "two-sided"]
    seed: int
    fixed_singleton_strata: tuple[str, ...]


def _validate_people(participant_ids: Sequence[str]) -> None:
    if not participant_ids:
        raise ValueError("at least one participant is required")
    if len(set(participant_ids)) != len(participant_ids):
        raise ValueError("participant identifiers must be unique for person-level permutation")


def stratified_permutation(
    participant_ids: Sequence[str],
    *,
    strata: Mapping[str, str] | None = None,
    seed: int,
) -> dict[str, str]:
    """Map each person to a chart donor shuffled only within the same declared stratum."""

    _validate_people(participant_ids)
    unknown = set(strata or {}) - set(participant_ids)
    if unknown:
        raise ValueError(f"strata contain unknown participants: {sorted(unknown)}")
    missing = set(participant_ids) - set(strata or {}) if strata is not None else set()
    if missing:
        raise ValueError(f"strata missing participants: {sorted(missing)}")
    groups: dict[str, list[str]] = defaultdict(list)
    for participant in participant_ids:
        groups[(strata or {}).get(participant, "__all__")].append(participant)
    rng = random.Random(seed)
    assignment: dict[str, str] = {}
    for group in sorted(groups):
        people = sorted(groups[group])
        donors = people.copy()
        rng.shuffle(donors)
        assignment.update(zip(people, donors, strict=True))
    return assignment


def generate_null_assignments(
    participant_ids: Sequence[str],
    *,
    strata: Mapping[str, str] | None = None,
    permutations: int,
    seed: int,
) -> tuple[dict[str, str], ...]:
    if permutations < 1:
        raise ValueError("permutations must be positive")
    rng = random.Random(seed)
    child_seeds = [rng.getrandbits(64) for _ in range(permutations)]
    return tuple(
        stratified_permutation(participant_ids, strata=strata, seed=child_seed)
        for child_seed in child_seeds
    )


def _quantile(values: Sequence[float], proportion: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * proportion
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def empirical_p_value(
    observed: float,
    null_values: Sequence[float],
    *,
    alternative: Literal["greater", "less", "two-sided"] = "greater",
) -> float:
    """Phipson-Smyth plus-one p-value, so Monte Carlo p is never zero."""

    if not null_values:
        raise ValueError("null distribution cannot be empty")
    if not math.isfinite(observed) or not all(math.isfinite(item) for item in null_values):
        raise ValueError("permutation statistics must be finite")
    if alternative == "greater":
        extreme = sum(item >= observed for item in null_values)
    elif alternative == "less":
        extreme = sum(item <= observed for item in null_values)
    elif alternative == "two-sided":
        center = statistics.fmean(null_values)
        distance = abs(observed - center)
        extreme = sum(abs(item - center) >= distance for item in null_values)
    else:
        raise ValueError(f"unknown alternative: {alternative}")
    return (extreme + 1.0) / (len(null_values) + 1.0)


def permutation_test(
    participant_ids: Sequence[str],
    *,
    observed_statistic: float,
    statistic_for_assignment: Callable[[Mapping[str, str]], float],
    strata: Mapping[str, str] | None = None,
    permutations: int = 1000,
    seed: int = 0,
    alternative: Literal["greater", "less", "two-sided"] = "greater",
) -> NullDistributionSummary:
    assignments = generate_null_assignments(
        participant_ids,
        strata=strata,
        permutations=permutations,
        seed=seed,
    )
    null_values = [float(statistic_for_assignment(assignment)) for assignment in assignments]
    if not all(math.isfinite(item) for item in null_values):
        raise ValueError("permutation statistic returned a non-finite value")
    singleton_strata: tuple[str, ...] = ()
    if strata is not None:
        counts: dict[str, int] = defaultdict(int)
        for value in strata.values():
            counts[value] += 1
        singleton_strata = tuple(sorted(key for key, count in counts.items() if count == 1))
    return NullDistributionSummary(
        permutations=permutations,
        observed_statistic=observed_statistic,
        null_mean=statistics.fmean(null_values),
        null_standard_deviation=(statistics.stdev(null_values) if len(null_values) > 1 else 0.0),
        null_q025=_quantile(null_values, 0.025),
        null_median=_quantile(null_values, 0.5),
        null_q975=_quantile(null_values, 0.975),
        p_value=empirical_p_value(observed_statistic, null_values, alternative=alternative),
        alternative=alternative,
        seed=seed,
        fixed_singleton_strata=singleton_strata,
    )
