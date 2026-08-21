"""Tie-aware evaluation, robustness curves, leakage audit, and null tests."""

from .failures import FailureClassification, FailureRecord, classify_oracle_failure
from .metrics import (
    AggregateRankMetrics,
    CaseRankMetrics,
    TieAwareRank,
    aggregate_rank_metrics,
    evaluate_ranked_case,
    tie_aware_rank,
)

__all__ = [
    "AggregateRankMetrics",
    "CaseRankMetrics",
    "FailureClassification",
    "FailureRecord",
    "TieAwareRank",
    "aggregate_rank_metrics",
    "classify_oracle_failure",
    "evaluate_ranked_case",
    "tie_aware_rank",
]
