"""Candidate-universe construction, interval scoring, and date aggregation."""

from .adaptive import QuestionUtility, expected_information_gain, select_next_question
from .candidate_universe import local_month_utc_bounds, split_interval_by_local_date
from .date_aggregator import AggregationMode, aggregate_dates

__all__ = [
    "AggregationMode",
    "QuestionUtility",
    "aggregate_dates",
    "expected_information_gain",
    "local_month_utc_bounds",
    "select_next_question",
    "split_interval_by_local_date",
]
