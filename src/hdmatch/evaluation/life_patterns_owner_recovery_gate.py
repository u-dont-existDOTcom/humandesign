"""Executable regression gate for the Life Patterns owner AstroHD recovery benchmark.

The gate compares *post-freeze* recovery metrics with the already-recorded historical
owner benchmark. It never receives raw birth data and is not used by the participant
interviewer. Passing this gate is a development regression result, not untouched human
validation of astrology or Human Design.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OwnerRecoverySignature(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    search_procedure_id: str = Field(min_length=1)
    exact_recorded_rank_hourly: int = Field(ge=1)
    correct_date_top_distinct_refined_neighborhood: bool
    refined_peak_offset_minutes: float


class OwnerRecoveryGateResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    passed: bool
    same_search_procedure: bool
    correct_date_recovered: bool
    exact_rank_not_worse: bool
    refined_time_not_worse: bool
    reasons: tuple[str, ...]


def evaluate_owner_recovery_regression(
    *,
    candidate: OwnerRecoverySignature,
    baseline: OwnerRecoverySignature,
) -> OwnerRecoveryGateResult:
    """Require a fresh post-freeze run to reproduce or improve the historical signature."""

    same_procedure = candidate.search_procedure_id == baseline.search_procedure_id
    correct_date = candidate.correct_date_top_distinct_refined_neighborhood
    rank_ok = candidate.exact_recorded_rank_hourly <= baseline.exact_recorded_rank_hourly
    time_ok = abs(candidate.refined_peak_offset_minutes) <= abs(
        baseline.refined_peak_offset_minutes
    )

    reasons: list[str] = []
    if not same_procedure:
        reasons.append("search procedure differs from the historical benchmark")
    if not correct_date:
        reasons.append("recorded date is not the top distinct refined neighborhood")
    if not rank_ok:
        reasons.append("exact recorded moment ranks worse than the historical benchmark")
    if not time_ok:
        reasons.append("refined peak is farther from the recorded time than the historical benchmark")

    return OwnerRecoveryGateResult(
        passed=same_procedure and correct_date and rank_ok and time_ok,
        same_search_procedure=same_procedure,
        correct_date_recovered=correct_date,
        exact_rank_not_worse=rank_ok,
        refined_time_not_worse=time_ok,
        reasons=tuple(reasons),
    )
