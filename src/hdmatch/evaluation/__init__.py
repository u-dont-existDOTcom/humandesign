"""Tie-aware evaluation, robustness curves, leakage audit, and null tests."""

from .behavioral_difference import (
    BehavioralDifferenceAudit,
    BehavioralDifferenceMonthRequest,
    PairwiseTieSplit,
    VerifiedBehavioralDifferenceBinding,
    audit_behavioral_difference,
    load_behavioral_difference_audit,
    require_behavioral_difference,
    verify_behavioral_difference_audit,
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
    "BehavioralDifferenceMonthRequest",
    "CaseRankMetrics",
    "FailureClassification",
    "FailureRecord",
    "PairwiseTieSplit",
    "TieAwareRank",
    "VerifiedBehavioralDifferenceBinding",
    "aggregate_rank_metrics",
    "audit_behavioral_difference",
    "classify_oracle_failure",
    "evaluate_ranked_case",
    "load_behavioral_difference_audit",
    "require_behavioral_difference",
    "tie_aware_rank",
    "verify_behavioral_difference_audit",
]
