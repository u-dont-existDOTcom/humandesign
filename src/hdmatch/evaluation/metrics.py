"""Rank metrics with explicit fractional treatment of score ties."""

from __future__ import annotations

import math
import statistics
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class TieAwareRank(BaseModel):
    """The positions occupied by a candidate's exact score-tie group."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_count: int = Field(ge=1)
    best_rank: int = Field(ge=1)
    worst_rank: int = Field(ge=1)
    midrank: float = Field(ge=1.0)
    tie_size: int = Field(ge=1)
    true_score: float
    margin_to_best_other: float | None

    def top_k_credit(self, k: int) -> float:
        """Expected top-k inclusion under random ordering inside the tie group."""

        if k < 1:
            raise ValueError("k must be positive")
        occupied = max(0, min(self.worst_rank, k) - self.best_rank + 1)
        return occupied / self.tie_size

    def top_k_possible(self, k: int) -> bool:
        return self.best_rank <= k

    def top_k_guaranteed(self, k: int) -> bool:
        return self.worst_rank <= k


class CaseRankMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    true_candidate_id: str
    candidate_count: int = Field(ge=1)
    best_rank: int = Field(ge=1)
    worst_rank: int = Field(ge=1)
    midrank: float = Field(ge=1.0)
    tie_size: int = Field(ge=1)
    reciprocal_rank: float = Field(gt=0.0, le=1.0)
    percentile: float = Field(ge=0.0, le=1.0)
    margin_to_best_other: float | None
    top_1_credit: float = Field(ge=0.0, le=1.0)
    top_3_credit: float = Field(ge=0.0, le=1.0)
    top_5_credit: float = Field(ge=0.0, le=1.0)
    tied: bool


class AggregateRankMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    case_count: int = Field(ge=0)
    evaluated_case_count: int = Field(ge=0)
    unevaluable_case_count: int = Field(ge=0)
    top_1: float | None = Field(default=None, ge=0.0, le=1.0)
    top_3: float | None = Field(default=None, ge=0.0, le=1.0)
    top_5: float | None = Field(default=None, ge=0.0, le=1.0)
    mean_reciprocal_rank: float | None = Field(default=None, ge=0.0, le=1.0)
    mean_percentile: float | None = Field(default=None, ge=0.0, le=1.0)
    mean_midrank: float | None = Field(default=None, ge=1.0)
    median_midrank: float | None = Field(default=None, ge=1.0)
    tie_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    tie_policy: Literal["fractional-credit-random-within-tie"] = (
        "fractional-credit-random-within-tie"
    )


def tie_aware_rank(
    scores: Sequence[float],
    true_index: int,
    *,
    tie_tolerance: float = 0.0,
) -> TieAwareRank:
    """Rank a true score descending while preserving its entire tie interval."""

    if not scores:
        raise ValueError("at least one candidate score is required")
    if true_index < 0 or true_index >= len(scores):
        raise IndexError("true_index is outside the score sequence")
    if tie_tolerance < 0 or not math.isfinite(tie_tolerance):
        raise ValueError("tie_tolerance must be finite and nonnegative")
    converted = [float(item) for item in scores]
    if not all(math.isfinite(item) for item in converted):
        raise ValueError("candidate scores must be finite")
    true_score = converted[true_index]
    higher = sum(score > true_score + tie_tolerance for score in converted)
    tied = sum(abs(score - true_score) <= tie_tolerance for score in converted)
    best = higher + 1
    worst = higher + tied
    others = converted[:true_index] + converted[true_index + 1 :]
    margin = true_score - max(others) if others else None
    return TieAwareRank(
        candidate_count=len(converted),
        best_rank=best,
        worst_rank=worst,
        midrank=(best + worst) / 2.0,
        tie_size=tied,
        true_score=true_score,
        margin_to_best_other=margin,
    )


def evaluate_ranked_case(
    *,
    case_id: str,
    candidates: Sequence[Mapping[str, Any]],
    true_candidate_id: str,
    id_field: str = "local_date",
    score_field: str = "date_score",
    tie_tolerance: float = 0.0,
) -> CaseRankMetrics:
    """Evaluate one ranking and reject missing or duplicated candidate identities."""

    identities = [str(candidate[id_field]) for candidate in candidates]
    if len(set(identities)) != len(identities):
        raise ValueError(f"case {case_id}: duplicate candidate identities")
    true_identity = str(true_candidate_id)
    if true_identity not in identities:
        raise ValueError(f"case {case_id}: true candidate is absent from ranking")
    scores = [float(candidate[score_field]) for candidate in candidates]
    rank = tie_aware_rank(scores, identities.index(true_identity), tie_tolerance=tie_tolerance)
    if rank.candidate_count == 1:
        percentile = 1.0
    else:
        percentile = 1.0 - ((rank.midrank - 1.0) / (rank.candidate_count - 1.0))
    return CaseRankMetrics(
        case_id=case_id,
        true_candidate_id=true_identity,
        candidate_count=rank.candidate_count,
        best_rank=rank.best_rank,
        worst_rank=rank.worst_rank,
        midrank=rank.midrank,
        tie_size=rank.tie_size,
        reciprocal_rank=1.0 / rank.midrank,
        percentile=percentile,
        margin_to_best_other=rank.margin_to_best_other,
        top_1_credit=rank.top_k_credit(1),
        top_3_credit=rank.top_k_credit(3),
        top_5_credit=rank.top_k_credit(5),
        tied=rank.tie_size > 1,
    )


def aggregate_rank_metrics(
    cases: Sequence[CaseRankMetrics], *, total_case_count: int | None = None
) -> AggregateRankMetrics:
    total = len(cases) if total_case_count is None else total_case_count
    if total < len(cases):
        raise ValueError("total_case_count cannot be smaller than evaluated cases")
    if total == 0:
        return AggregateRankMetrics(
            case_count=0, evaluated_case_count=0, unevaluable_case_count=0
        )
    denominator = float(total)
    if not cases:
        return AggregateRankMetrics(
            case_count=total,
            evaluated_case_count=0,
            unevaluable_case_count=total,
            top_1=0.0,
            top_3=0.0,
            top_5=0.0,
            mean_reciprocal_rank=0.0,
            mean_percentile=0.0,
        )
    return AggregateRankMetrics(
        case_count=total,
        evaluated_case_count=len(cases),
        unevaluable_case_count=total - len(cases),
        top_1=sum(case.top_1_credit for case in cases) / denominator,
        top_3=sum(case.top_3_credit for case in cases) / denominator,
        top_5=sum(case.top_5_credit for case in cases) / denominator,
        mean_reciprocal_rank=sum(case.reciprocal_rank for case in cases) / denominator,
        mean_percentile=sum(case.percentile for case in cases) / denominator,
        mean_midrank=statistics.fmean(case.midrank for case in cases),
        median_midrank=statistics.median(case.midrank for case in cases),
        tie_rate=statistics.fmean(float(case.tied) for case in cases),
    )
