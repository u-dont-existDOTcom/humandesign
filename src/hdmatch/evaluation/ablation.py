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
    midrank: float = Field(ge=1.0)
    candidate_count: int = Field(ge=1)
    tie_size: int = Field(default=1, ge=1)


class CurvePoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    method: Literal["random", "active", "leave_one_out"]
    cluster_count: int = Field(ge=0)
    case_count: int = Field(ge=1)
    mean_midrank: float = Field(ge=1.0)
    median_midrank: float = Field(ge=1.0)
    mean_reciprocal_rank: float = Field(gt=0.0, le=1.0)
    top_1: float = Field(ge=0.0, le=1.0)
    top_3: float = Field(ge=0.0, le=1.0)
    top_5: float = Field(ge=0.0, le=1.0)
    tie_rate: float = Field(ge=0.0, le=1.0)


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
        output.append(
            CurvePoint(
                method=method,  # type: ignore[arg-type]
                cluster_count=count,
                case_count=len(values),
                mean_midrank=statistics.fmean(item.midrank for item in values),
                median_midrank=statistics.median(item.midrank for item in values),
                mean_reciprocal_rank=statistics.fmean(1.0 / item.midrank for item in values),
                top_1=statistics.fmean(
                    _top_k_credit(item.midrank, item.tie_size, 1) for item in values
                ),
                top_3=statistics.fmean(
                    _top_k_credit(item.midrank, item.tie_size, 3) for item in values
                ),
                top_5=statistics.fmean(
                    _top_k_credit(item.midrank, item.tie_size, 5) for item in values
                ),
                tie_rate=statistics.fmean(float(item.tie_size > 1) for item in values),
            )
        )
    return tuple(output)


class LeaveOneClusterOutObservation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    cluster_id: str
    full_midrank: float = Field(ge=1.0)
    ablated_midrank: float = Field(ge=1.0)


class ClusterAblationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cluster_id: str
    case_count: int = Field(ge=1)
    mean_rank_change: float
    median_rank_change: float
    worsened_fraction: float = Field(ge=0.0, le=1.0)


def aggregate_leave_one_cluster_out(
    observations: Sequence[LeaveOneClusterOutObservation],
) -> tuple[ClusterAblationSummary, ...]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for observation in observations:
        grouped[observation.cluster_id].append(
            observation.ablated_midrank - observation.full_midrank
        )
    return tuple(
        ClusterAblationSummary(
            cluster_id=cluster,
            case_count=len(changes),
            mean_rank_change=statistics.fmean(changes),
            median_rank_change=statistics.median(changes),
            worsened_fraction=statistics.fmean(float(change > 0) for change in changes),
        )
        for cluster, changes in sorted(grouped.items())
    )
