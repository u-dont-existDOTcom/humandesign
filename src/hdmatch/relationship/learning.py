"""Structured learning ledger for relationship-model development.

This module deliberately does not mutate questionnaire/model definitions. It
summarizes immutable case evaluations so a later development process can detect
recurrent failure structure and propose a *new* version. Promotion thresholds
remain caller-supplied while the upstream Survey-v2 noise audit is incomplete.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


EvaluationOutcome = Literal["hit", "miss", "partial", "unresolved", "not_predicted"]
Direction = Literal["a_to_b", "b_to_a", "dyadic", "person_a", "person_b"]


class RelationshipAxisEvaluation(_FrozenModel):
    """One immutable model-vs-phenotype comparison for one axis/direction."""

    case_id: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    axis_id: str = Field(min_length=1)
    direction: Direction
    outcome: EvaluationOutcome
    classifier_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    predicted_ordinal: int | None = Field(default=None, ge=0, le=4)
    observed_ordinal: int | None = Field(default=None, ge=0, le=4)
    context_tags: tuple[str, ...] = ()
    observability_limits: tuple[str, ...] = ()
    question_ids: tuple[str, ...] = ()


class AxisLearningSummary(_FrozenModel):
    model_id: str
    axis_id: str
    direction: Direction
    total_records: int = Field(ge=1)
    scored_records: int = Field(ge=0)
    hit_count: int = Field(ge=0)
    miss_count: int = Field(ge=0)
    partial_count: int = Field(ge=0)
    unresolved_count: int = Field(ge=0)
    not_predicted_count: int = Field(ge=0)
    hit_rate_scored: float | None = Field(default=None, ge=0.0, le=1.0)
    miss_rate_scored: float | None = Field(default=None, ge=0.0, le=1.0)
    mean_classifier_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    mean_absolute_ordinal_error: float | None = Field(default=None, ge=0.0)
    context_counts: dict[str, int]
    observability_limit_counts: dict[str, int]
    question_counts: dict[str, int]


class RelationshipLearningSummary(_FrozenModel):
    schema_version: str = "relationship-learning-summary-v1"
    case_count: int = Field(ge=0)
    evaluation_count: int = Field(ge=0)
    axis_summaries: tuple[AxisLearningSummary, ...]


class RevisionSignal(_FrozenModel):
    """A deterministic flag for review, never an automatic model edit."""

    model_id: str
    axis_id: str
    direction: Direction
    signal_type: Literal[
        "high_miss_rate",
        "high_unresolved_rate",
        "context_concentrated_misses",
        "directional_asymmetry",
    ]
    value: float = Field(ge=0.0)
    supporting_case_count: int = Field(ge=0)
    notes: str


def summarize_relationship_learning(
    evaluations: Iterable[RelationshipAxisEvaluation],
) -> RelationshipLearningSummary:
    """Aggregate immutable relationship evaluations by model/axis/direction."""
    rows = tuple(evaluations)
    groups: dict[tuple[str, str, Direction], list[RelationshipAxisEvaluation]] = defaultdict(list)
    for row in rows:
        groups[(row.model_id, row.axis_id, row.direction)].append(row)

    summaries = tuple(
        _summarize_group(model_id, axis_id, direction, tuple(group))
        for (model_id, axis_id, direction), group in sorted(groups.items())
    )
    return RelationshipLearningSummary(
        case_count=len({row.case_id for row in rows}),
        evaluation_count=len(rows),
        axis_summaries=summaries,
    )


def detect_revision_signals(
    summary: RelationshipLearningSummary,
    *,
    min_scored_cases: int,
    miss_rate_threshold: float,
    unresolved_rate_threshold: float,
    context_miss_share_threshold: float,
    directional_hit_rate_gap_threshold: float,
) -> tuple[RevisionSignal, ...]:
    """Flag recurrent development failures using caller-frozen thresholds.

    Thresholds are intentionally mandatory arguments. The relationship module
    must not silently freeze its own noise/retry policy before the upstream
    Survey-v2 noise audit and relationship-specific reliability work are done.
    """
    if min_scored_cases < 1:
        raise ValueError("min_scored_cases must be positive")
    for value in (
        miss_rate_threshold,
        unresolved_rate_threshold,
        context_miss_share_threshold,
        directional_hit_rate_gap_threshold,
    ):
        if not 0.0 <= value <= 1.0:
            raise ValueError("revision signal thresholds must be within [0, 1]")

    signals: list[RevisionSignal] = []
    by_model_axis: dict[tuple[str, str], list[AxisLearningSummary]] = defaultdict(list)
    for item in summary.axis_summaries:
        by_model_axis[(item.model_id, item.axis_id)].append(item)
        if (
            item.scored_records >= min_scored_cases
            and item.miss_rate_scored is not None
            and item.miss_rate_scored >= miss_rate_threshold
        ):
            signals.append(
                RevisionSignal(
                    model_id=item.model_id,
                    axis_id=item.axis_id,
                    direction=item.direction,
                    signal_type="high_miss_rate",
                    value=item.miss_rate_scored,
                    supporting_case_count=item.scored_records,
                    notes="Frozen model repeatedly misses this axis/direction in development data.",
                )
            )
        unresolved_rate = item.unresolved_count / item.total_records
        if item.total_records >= min_scored_cases and unresolved_rate >= unresolved_rate_threshold:
            signals.append(
                RevisionSignal(
                    model_id=item.model_id,
                    axis_id=item.axis_id,
                    direction=item.direction,
                    signal_type="high_unresolved_rate",
                    value=unresolved_rate,
                    supporting_case_count=item.total_records,
                    notes="Current questionnaire/rubric frequently cannot resolve this axis.",
                )
            )

    # Context concentration requires the individual miss rows, which the compact
    # summary intentionally does not retain. Reserve the signal type for a future
    # ledger-level function rather than manufacturing it from aggregate counts.

    for (model_id, axis_id), directions in sorted(by_model_axis.items()):
        lookup = {item.direction: item for item in directions}
        left = lookup.get("a_to_b")
        right = lookup.get("b_to_a")
        if left is None or right is None:
            continue
        if (
            left.scored_records < min_scored_cases
            or right.scored_records < min_scored_cases
            or left.hit_rate_scored is None
            or right.hit_rate_scored is None
        ):
            continue
        gap = abs(left.hit_rate_scored - right.hit_rate_scored)
        if gap >= directional_hit_rate_gap_threshold:
            signals.append(
                RevisionSignal(
                    model_id=model_id,
                    axis_id=axis_id,
                    direction="dyadic",
                    signal_type="directional_asymmetry",
                    value=gap,
                    supporting_case_count=min(left.scored_records, right.scored_records),
                    notes="Predictive performance differs materially by actor direction; pooled treatment may be hiding a failure.",
                )
            )

    return tuple(signals)


def _summarize_group(
    model_id: str,
    axis_id: str,
    direction: Direction,
    rows: tuple[RelationshipAxisEvaluation, ...],
) -> AxisLearningSummary:
    outcomes = Counter(row.outcome for row in rows)
    scored = outcomes["hit"] + outcomes["miss"] + outcomes["partial"]
    hit_rate = outcomes["hit"] / scored if scored else None
    miss_rate = outcomes["miss"] / scored if scored else None

    confidences = [
        row.classifier_confidence for row in rows if row.classifier_confidence is not None
    ]
    ordinal_errors = [
        abs(row.predicted_ordinal - row.observed_ordinal)
        for row in rows
        if row.predicted_ordinal is not None and row.observed_ordinal is not None
    ]
    contexts = Counter(tag for row in rows for tag in row.context_tags)
    limits = Counter(tag for row in rows for tag in row.observability_limits)
    questions = Counter(question for row in rows for question in row.question_ids)

    return AxisLearningSummary(
        model_id=model_id,
        axis_id=axis_id,
        direction=direction,
        total_records=len(rows),
        scored_records=scored,
        hit_count=outcomes["hit"],
        miss_count=outcomes["miss"],
        partial_count=outcomes["partial"],
        unresolved_count=outcomes["unresolved"],
        not_predicted_count=outcomes["not_predicted"],
        hit_rate_scored=hit_rate,
        miss_rate_scored=miss_rate,
        mean_classifier_confidence=(sum(confidences) / len(confidences) if confidences else None),
        mean_absolute_ordinal_error=(sum(ordinal_errors) / len(ordinal_errors) if ordinal_errors else None),
        context_counts=dict(sorted(contexts.items())),
        observability_limit_counts=dict(sorted(limits.items())),
        question_counts=dict(sorted(questions.items())),
    )
