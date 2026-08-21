"""Tie-aware evaluation, robustness curves, leakage audit, and null tests."""

from .behavioral_difference import (
    BehavioralDifferenceAudit,
    PairwiseTieSplit,
    audit_behavioral_difference,
    require_behavioral_difference,
)
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
    "BehavioralDifferenceAudit",
    "CaseRankMetrics",
    "FailureClassification",
    "FailureRecord",
    "PairwiseTieSplit",
    "TieAwareRank",
    "aggregate_rank_metrics",
    "audit_behavioral_difference",
    "classify_oracle_failure",
    "evaluate_ranked_case",
    "require_behavioral_difference",
    "tie_aware_rank",
]
