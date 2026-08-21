"""Transparent aggregation of declared perturbation and noise-tier evaluations."""

from __future__ import annotations

import statistics
from collections import defaultdict
from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict, Field

from .metrics import AggregateRankMetrics, CaseRankMetrics, aggregate_rank_metrics


class RobustnessObservation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    perturbation: str = Field(min_length=1)
    level: str = Field(min_length=1)
    metrics: CaseRankMetrics


class RobustnessPoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    perturbation: str
    level: str
    aggregate: AggregateRankMetrics


def aggregate_robustness(
    observations: Sequence[RobustnessObservation],
) -> tuple[RobustnessPoint, ...]:
    grouped: dict[tuple[str, str], list[CaseRankMetrics]] = defaultdict(list)
    for observation in observations:
        grouped[(observation.perturbation, observation.level)].append(observation.metrics)
    return tuple(
        RobustnessPoint(
            perturbation=perturbation,
            level=level,
            aggregate=aggregate_rank_metrics(metrics),
        )
        for (perturbation, level), metrics in sorted(grouped.items())
    )


class PairedRobustnessChange(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    perturbation: str
    level: str
    paired_case_count: int = Field(ge=1)
    mean_midrank_change: float
    median_midrank_change: float
    worsened_fraction: float = Field(ge=0.0, le=1.0)


def paired_changes_from_baseline(
    observations: Sequence[RobustnessObservation],
    *,
    baseline_level: str = "baseline",
) -> tuple[PairedRobustnessChange, ...]:
    """Compare levels only for cases also observed in the same perturbation baseline."""

    baselines: dict[tuple[str, str], float] = {}
    for item in observations:
        if item.level == baseline_level:
            key = (item.perturbation, item.metrics.case_id)
            if key in baselines:
                raise ValueError(f"duplicate baseline observation for {key}")
            baselines[key] = item.metrics.midrank
    changes: dict[tuple[str, str], list[float]] = defaultdict(list)
    for item in observations:
        if item.level == baseline_level:
            continue
        baseline = baselines.get((item.perturbation, item.metrics.case_id))
        if baseline is not None:
            changes[(item.perturbation, item.level)].append(item.metrics.midrank - baseline)
    return tuple(
        PairedRobustnessChange(
            perturbation=perturbation,
            level=level,
            paired_case_count=len(values),
            mean_midrank_change=statistics.fmean(values),
            median_midrank_change=statistics.median(values),
            worsened_fraction=statistics.fmean(float(value > 0) for value in values),
        )
        for (perturbation, level), values in sorted(changes.items())
        if values
    )
