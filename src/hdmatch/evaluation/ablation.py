"""Aggregate random-restoration, active-restoration, and ablation rank curves."""

from __future__ import annotations

import statistics
from collections import defaultdict
from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CurveObservation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    method: Literal["random", "active", "leave_one_out"]
    cluster_count: int = Field(ge=0)
    midrank: float | None = Field(default=None, ge=1.0)
    candidate_count: int = Field(ge=1)
    tie_size: int = Field(default=1, ge=1)


class CurvePoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    method: Literal["random", "active", "leave_one_out"]
    cluster_count: int = Field(ge=0)
    case_count: int = Field(ge=1)
    evaluated_case_count: int = Field(ge=0)
    unevaluable_case_count: int = Field(ge=0)
    mean_midrank: float | None = Field(default=None, ge=1.0)
    median_midrank: float | None = Field(default=None, ge=1.0)
    mean_reciprocal_rank: float = Field(ge=0.0, le=1.0)
    top_1: float = Field(ge=0.0, le=1.0)
    top_3: float = Field(ge=0.0, le=1.0)
    top_5: float = Field(ge=0.0, le=1.0)
    tie_rate: float | None = Field(default=None, ge=0.0, le=1.0)


def _top_k_credit(midrank: float, tie_size: int, k: int) -> float:
    best = int(midrank - (tie_size - 1) / 2)
    worst = best + tie_size - 1
    occupied = max(0, min(worst, k) - best + 1)
    return occupied / tie_size


def aggregate_restoration_curves(
    observations: Sequence[CurveObservation],
) -> tuple[CurvePoint, ...]:
    groups: dict[tuple[str, int], list[CurveObservation]] = defaultdict(list)
    for observation in observations:
        groups[(observation.method, observation.cluster_count)].append(observation)
    output: list[CurvePoint] = []
    for (method, count), values in sorted(groups.items()):
        evaluated = [
            (item, item.midrank) for item in values if item.midrank is not None
        ]
        ranks = [rank for _, rank in evaluated]
        denominator = float(len(values))
        output.append(
            CurvePoint(
                method=method,  # type: ignore[arg-type]
                cluster_count=count,
                case_count=len(values),
                evaluated_case_count=len(evaluated),
                unevaluable_case_count=len(values) - len(evaluated),
                mean_midrank=statistics.fmean(ranks) if ranks else None,
                median_midrank=statistics.median(ranks) if ranks else None,
                mean_reciprocal_rank=sum(1.0 / rank for rank in ranks) / denominator,
                top_1=(
                    sum(_top_k_credit(rank, item.tie_size, 1) for item, rank in evaluated)
                    / denominator
                ),
                top_3=(
                    sum(_top_k_credit(rank, item.tie_size, 3) for item, rank in evaluated)
                    / denominator
                ),
                top_5=(
                    sum(_top_k_credit(rank, item.tie_size, 5) for item, rank in evaluated)
                    / denominator
                ),
                tie_rate=(
                    statistics.fmean(float(item.tie_size > 1) for item, _ in evaluated)
                    if evaluated
                    else None
                ),
            )
        )
    return tuple(output)


class LeaveOneClusterOutObservation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    cluster_id: str
    full_midrank: float | None = Field(default=None, ge=1.0)
    ablated_midrank: float | None = Field(default=None, ge=1.0)


class ClusterAblationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cluster_id: str
    case_count: int = Field(ge=1)
    evaluated_case_count: int = Field(ge=0)
    unevaluable_case_count: int = Field(ge=0)
    mean_rank_change: float | None
    median_rank_change: float | None
    worsened_fraction: float | None = Field(default=None, ge=0.0, le=1.0)


def aggregate_leave_one_cluster_out(
    observations: Sequence[LeaveOneClusterOutObservation],
) -> tuple[ClusterAblationSummary, ...]:
    grouped: dict[str, list[float | None]] = defaultdict(list)
    for observation in observations:
        change = (
            None
            if observation.ablated_midrank is None or observation.full_midrank is None
            else observation.ablated_midrank - observation.full_midrank
        )
        grouped[observation.cluster_id].append(change)
    return tuple(
        ClusterAblationSummary(
            cluster_id=cluster,
            case_count=len(changes),
            evaluated_case_count=len([change for change in changes if change is not None]),
            unevaluable_case_count=len([change for change in changes if change is None]),
            mean_rank_change=(
                statistics.fmean(change for change in changes if change is not None)
                if any(change is not None for change in changes)
                else None
            ),
            median_rank_change=(
                statistics.median(change for change in changes if change is not None)
                if any(change is not None for change in changes)
                else None
            ),
            worsened_fraction=(
                statistics.fmean(
                    float(change > 0) for change in changes if change is not None
                )
                if any(change is not None for change in changes)
                else None
            ),
        )
        for cluster, changes in sorted(grouped.items())
    )
