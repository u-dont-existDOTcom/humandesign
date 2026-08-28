"""Dynamic relationship questionnaire routing.

The relationship questionnaire reuses the repository's answer-blind expected-
information-gain selector. Development capture remains chart-blind and asks the
broad core anchors first; validation mode may adapt among anonymous frozen
prediction likelihoods without exposing birth metadata or chart labels here.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.search.adaptive import QuestionUtility, select_next_question


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class RelationshipQuestion(_FrozenModel):
    id: str = Field(min_length=1)
    stage: Literal["core", "adaptive_followup"]
    priority: int = Field(ge=1)
    burden: float = Field(ge=0.0)
    expected_reliability: float = Field(ge=0.0, le=1.0)
    target_axes: tuple[str, ...]
    prompt: str = Field(min_length=1)
    probes: tuple[str, ...]
    response_format: str = Field(min_length=1)
    minimum_evidence: str = Field(min_length=1)
    scoring_policy: str = Field(min_length=1)
    applicability_flags: tuple[str, ...] = ()


class RelationshipQuestionnaireSpec(_FrozenModel):
    schema_version: str = Field(min_length=1)
    status: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    rubric_registry: str = Field(min_length=1)
    adaptive_engine: str = Field(min_length=1)
    global_rules: tuple[str, ...]
    modes: Mapping[str, Any]
    core_question_ids: tuple[str, ...]
    questions: tuple[RelationshipQuestion, ...]


def load_relationship_questionnaire(path: Path) -> RelationshipQuestionnaireSpec:
    """Load and structurally validate a relationship questionnaire JSON file."""
    payload: Any = json.loads(path.read_text(encoding="utf-8"))
    spec = RelationshipQuestionnaireSpec.model_validate(payload)
    _validate_questionnaire(spec)
    return spec


def question_by_id(
    spec: RelationshipQuestionnaireSpec, question_id: str
) -> RelationshipQuestion:
    for question in spec.questions:
        if question.id == question_id:
            return question
    raise KeyError(f"unknown relationship question id: {question_id}")


def select_next_capture_question(
    spec: RelationshipQuestionnaireSpec,
    *,
    answered_question_ids: Sequence[str] = (),
    unresolved_axis_ids: Sequence[str] = (),
    applicability_flags: Sequence[str] = (),
) -> RelationshipQuestion | None:
    """Choose the next chart-blind development-capture question.

    All core anchors are asked first in their frozen order. Once the core is
    complete, only follow-ups touching an unresolved axis or a fixed
    applicability flag are eligible. No chart prediction is accepted by this
    function.
    """
    answered = _validated_id_set(spec, answered_question_ids)
    for question_id in spec.core_question_ids:
        if question_id not in answered:
            return question_by_id(spec, question_id)

    unresolved = set(unresolved_axis_ids)
    flags = set(applicability_flags)
    eligible = [
        question
        for question in spec.questions
        if question.stage == "adaptive_followup"
        and question.id not in answered
        and (
            bool(unresolved.intersection(question.target_axes))
            or bool(flags.intersection(question.applicability_flags))
        )
    ]
    if not eligible:
        return None
    return min(eligible, key=lambda item: (item.priority, item.id))


def select_next_validation_question(
    spec: RelationshipQuestionnaireSpec,
    *,
    candidate_weights: Sequence[float],
    likelihoods_by_question: Mapping[str, Sequence[Mapping[str, float]]],
    answered_question_ids: Sequence[str] = (),
    applicability_flags: Sequence[str] = (),
    expected_reliability_override: Mapping[str, float] | None = None,
    burden_override: Mapping[str, float] | None = None,
) -> QuestionUtility | None:
    """Select the next candidate-blind validation question by adjusted EIG.

    This wrapper filters the frozen question bank and delegates the actual
    utility calculation to :func:`hdmatch.search.adaptive.select_next_question`.
    It intentionally accepts no birth metadata, chart object, true-candidate id,
    participant prose, or classifier rationale.
    """
    answered = _validated_id_set(spec, answered_question_ids)
    flags = set(applicability_flags)
    question_map = {question.id: question for question in spec.questions}

    eligible_likelihoods: dict[str, Sequence[Mapping[str, float]]] = {}
    for question_id, likelihoods in likelihoods_by_question.items():
        question = question_map.get(question_id)
        if question is None:
            raise KeyError(f"likelihoods supplied for unknown question id: {question_id}")
        if question_id in answered:
            continue
        if (
            question.stage == "adaptive_followup"
            and question.applicability_flags
            and not flags.intersection(question.applicability_flags)
        ):
            continue
        eligible_likelihoods[question_id] = likelihoods

    if not eligible_likelihoods:
        return None

    reliability_override = expected_reliability_override or {}
    burden_cost_override = burden_override or {}
    reliability: dict[str, float] = {}
    burden: dict[str, float] = {}
    for question_id in eligible_likelihoods:
        question = question_map[question_id]
        reliability[question_id] = reliability_override.get(
            question_id, question.expected_reliability
        )
        burden[question_id] = burden_cost_override.get(question_id, question.burden)

    return select_next_question(
        candidate_weights,
        eligible_likelihoods,
        expected_reliability=reliability,
        burden=burden,
    )


def _validate_questionnaire(spec: RelationshipQuestionnaireSpec) -> None:
    question_ids = [question.id for question in spec.questions]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("relationship question ids must be unique")
    if len(spec.core_question_ids) != len(set(spec.core_question_ids)):
        raise ValueError("core relationship question ids must be unique")
    question_map = {question.id: question for question in spec.questions}
    for question_id in spec.core_question_ids:
        question = question_map.get(question_id)
        if question is None:
            raise ValueError(f"core question id is missing from question bank: {question_id}")
        if question.stage != "core":
            raise ValueError(f"core question must have stage=core: {question_id}")
    declared_core = {question.id for question in spec.questions if question.stage == "core"}
    if declared_core != set(spec.core_question_ids):
        raise ValueError("core_question_ids must contain every and only stage=core question")


def _validated_id_set(
    spec: RelationshipQuestionnaireSpec, question_ids: Sequence[str]
) -> set[str]:
    known = {question.id for question in spec.questions}
    supplied = set(question_ids)
    unknown = supplied - known
    if unknown:
        raise KeyError(f"unknown relationship question ids: {sorted(unknown)}")
    return supplied
