"""Frozen chart-blind relationship phenotype records and validation."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

AxisDirection = Literal["a_to_b", "b_to_a", "dyadic", "person_a", "person_b"]
AxisScope = Literal["directional", "dyadic", "person"]
AxisStatus = Literal[
    "classified",
    "mixed",
    "other",
    "insufficient_evidence",
    "unclassifiable",
    "not_applicable",
]
OrdinalValue = Literal["very_low", "low", "moderate", "high", "very_high"]
Trajectory = Literal[
    "stable",
    "gradual_increase",
    "gradual_decrease",
    "rapid_increase",
    "rapid_decrease",
    "cyclical",
    "novelty_reset",
    "state_conditional",
    "unknown",
]
VALIDATION_CONTRACT_VERSION: Literal["relationship-phenotype-validation-contract-v2"] = (
    "relationship-phenotype-validation-contract-v2"
)
_VALIDATION_CONTRACT = {
    "version": VALIDATION_CONTRACT_VERSION,
    "rules": [
        "exact_submitted_question_coverage",
        "question_target_axis_enforcement",
        "rubric_scope_direction_enforcement",
        "unique_axis_direction_within_question",
        "classified_requires_ordinal_confidence_and_literal_evidence",
        "nonclassified_forbids_ordinal",
        "unresolved_axes_must_be_unique_known_question_targets",
        "all_evidence_spans_are_nonblank_verbatim_question_scoped_source_substrings",
    ],
}
VALIDATION_CONTRACT_SHA256 = hashlib.sha256(
    json.dumps(
        _VALIDATION_CONTRACT,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
).hexdigest()


class PhenotypeModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class AxisPhenotype(PhenotypeModel):
    axis_id: str = Field(min_length=1)
    direction: AxisDirection
    status: AxisStatus
    ordinal_value: OrdinalValue | None = None
    trajectory: Trajectory | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_spans: tuple[str, ...] = ()
    counterevidence_spans: tuple[str, ...] = ()
    context_conditions: tuple[str, ...] = ()
    observability_limits: tuple[str, ...] = ()
    forced_choice: Literal[False] = False

    @field_validator("ordinal_value")
    @classmethod
    def ordinal_requires_classified_status(
        cls,
        value: OrdinalValue | None,
        info: Any,
    ) -> OrdinalValue | None:
        # Cross-field validity is rechecked by ``validate_phenotype_output`` after parsing.
        return value


class QuestionPhenotype(PhenotypeModel):
    question_id: str = Field(min_length=1)
    axis_results: tuple[AxisPhenotype, ...]
    applicability_flags: tuple[str, ...] = ()
    unresolved_axis_ids: tuple[str, ...] = ()
    verbatim_preserved: Literal[True] = True


class RelationshipPhenotypeOutput(PhenotypeModel):
    question_results: tuple[QuestionPhenotype, ...]


class PhenotypeProviderReceipt(PhenotypeModel):
    provider: Literal["OpenAI"] = "OpenAI"
    model: str = Field(min_length=1)
    endpoint: str = Field(min_length=1)
    raw_response_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class RelationshipPhenotypeFreeze(PhenotypeModel):
    schema_version: Literal[
        "relationship-phenotype-freeze-v1", "relationship-phenotype-freeze-v2"
    ] = "relationship-phenotype-freeze-v2"
    validation_contract_version: Literal["relationship-phenotype-validation-contract-v2"] | None = (
        None
    )
    validation_contract_sha256: str | None = Field(
        default=None,
        pattern=r"^[a-f0-9]{64}$",
    )
    session_id: str = Field(min_length=1)
    created_at_utc: datetime
    response_record_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    questionnaire_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    rubric_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    classifier_protocol_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    classifier_model: str = Field(min_length=1)
    minimum_confidence: float = Field(ge=0.0, le=1.0)
    provider_receipt: PhenotypeProviderReceipt
    output: RelationshipPhenotypeOutput

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at_utc must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_contract_receipt(self) -> RelationshipPhenotypeFreeze:
        if self.schema_version == "relationship-phenotype-freeze-v1":
            if self.validation_contract_version is not None or self.validation_contract_sha256:
                raise ValueError("legacy phenotype freeze cannot claim a v2 validation receipt")
            return self
        if self.validation_contract_version != VALIDATION_CONTRACT_VERSION:
            raise ValueError("phenotype freeze v2 requires the current validation contract")
        if self.validation_contract_sha256 != VALIDATION_CONTRACT_SHA256:
            raise ValueError("phenotype freeze v2 validation contract hash does not match")
        return self

    @property
    def freeze_sha256(self) -> str:
        if self.schema_version == "relationship-phenotype-freeze-v1":
            return canonical_sha256(
                self.model_dump(
                    mode="json",
                    exclude={
                        "validation_contract_version",
                        "validation_contract_sha256",
                    },
                )
            )
        return canonical_sha256(self.model_dump(mode="json"))


class CalibrationPhenotypeObservation(PhenotypeModel):
    """One unique classified criterion row suitable for a later private ledger."""

    schema_version: Literal["relationship-calibration-phenotype-observation-v1"] = (
        "relationship-calibration-phenotype-observation-v1"
    )
    phenotype_freeze_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    question_id: str = Field(min_length=1)
    axis_id: str = Field(min_length=1)
    direction: AxisDirection
    ordinal_value: OrdinalValue
    trajectory: Trajectory | None = None
    classifier_confidence: float = Field(ge=0.0, le=1.0)
    context_conditions: tuple[str, ...] = ()
    observability_limits: tuple[str, ...] = ()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def response_record_sha256(
    answers: list[dict[str, Any]],
    semantic_audit: dict[str, Any],
) -> str:
    return canonical_sha256(
        {
            "answers": answers,
            "semantic_audit": {
                "audit_version": semantic_audit.get("audit_version"),
                "queue": semantic_audit.get("queue", []),
                "answers": semantic_audit.get("answers", []),
            },
        }
    )


def source_text_corpus(
    answers: list[dict[str, Any]],
    semantic_audit: dict[str, Any],
) -> dict[str, tuple[str, ...]]:
    by_question: dict[str, list[str]] = {}
    for record in answers:
        question_id = record.get("question_id")
        if not isinstance(question_id, str) or not question_id:
            continue
        texts = by_question.setdefault(question_id, [])
        for field in record.get("fields", []):
            if not isinstance(field, dict):
                continue
            for key in ("answer", "clarification"):
                text = field.get(key)
                if isinstance(text, str) and text.strip():
                    texts.append(text.strip())
        broad = record.get("answer")
        if isinstance(broad, str) and broad.strip():
            texts.append(broad.strip())
    for row in semantic_audit.get("answers", []):
        if isinstance(row, dict):
            question_id = row.get("source_question_id")
            text = row.get("answer")
            if (
                isinstance(question_id, str)
                and question_id
                and isinstance(text, str)
                and text.strip()
            ):
                by_question.setdefault(question_id, []).append(text.strip())
    return {question_id: tuple(texts) for question_id, texts in by_question.items()}


def validate_phenotype_output(
    output: RelationshipPhenotypeOutput,
    *,
    submitted_question_ids: set[str],
    allowed_axis_ids: set[str],
    question_target_axis_ids: Mapping[str, set[str]],
    axis_scopes: Mapping[str, AxisScope],
    source_texts_by_question: Mapping[str, tuple[str, ...]],
    minimum_confidence: float,
) -> RelationshipPhenotypeOutput:
    """Enforce frozen protocol identities and literal-evidence provenance."""

    returned_questions = [row.question_id for row in output.question_results]
    if len(returned_questions) != len(set(returned_questions)):
        raise ValueError("phenotype output contains duplicate question ids")
    if set(returned_questions) != submitted_question_ids:
        raise ValueError("phenotype output must cover exactly the submitted question ids")

    for question in output.question_results:
        target_axis_ids = question_target_axis_ids.get(question.question_id)
        if target_axis_ids is None:
            raise ValueError(f"questionnaire target registry is missing {question.question_id}")
        source_texts = source_texts_by_question.get(question.question_id, ())
        seen_axis_directions: set[tuple[str, AxisDirection]] = set()
        for axis in question.axis_results:
            if axis.axis_id not in allowed_axis_ids:
                raise ValueError(f"classifier returned unknown axis: {axis.axis_id}")
            if axis.axis_id not in target_axis_ids:
                raise ValueError(
                    f"classifier returned axis {axis.axis_id} outside question "
                    f"{question.question_id} targets"
                )
            scope = axis_scopes.get(axis.axis_id)
            if scope is None:
                raise ValueError(f"rubric scope is missing for axis: {axis.axis_id}")
            if axis.direction not in _directions_for_scope(scope):
                raise ValueError(
                    f"classifier direction {axis.direction} is invalid for {scope} "
                    f"axis {axis.axis_id}"
                )
            identity = (axis.axis_id, axis.direction)
            if identity in seen_axis_directions:
                raise ValueError(
                    "classifier returned a duplicate axis/direction within one question"
                )
            seen_axis_directions.add(identity)
            if axis.status == "classified" and axis.ordinal_value is None:
                raise ValueError("classified phenotype axis requires ordinal_value")
            if axis.status != "classified" and axis.ordinal_value is not None:
                raise ValueError("non-classified phenotype axis must not force ordinal_value")
            if axis.status == "classified" and axis.confidence < minimum_confidence:
                raise ValueError("classified phenotype axis is below the frozen confidence gate")
            if axis.status == "classified" and not axis.evidence_spans:
                raise ValueError("classified phenotype axis requires verbatim evidence")
            for span in (*axis.evidence_spans, *axis.counterevidence_spans):
                if not span.strip():
                    raise ValueError("evidence spans cannot be blank")
                if not any(span in source for source in source_texts):
                    raise ValueError("classifier cited evidence not present verbatim in responses")
        if len(question.unresolved_axis_ids) != len(set(question.unresolved_axis_ids)):
            raise ValueError("classifier returned duplicate unresolved axis ids")
        for axis_id in question.unresolved_axis_ids:
            if axis_id not in allowed_axis_ids:
                raise ValueError(f"classifier returned unknown unresolved axis: {axis_id}")
            if axis_id not in target_axis_ids:
                raise ValueError(
                    f"classifier returned unresolved axis {axis_id} outside question "
                    f"{question.question_id} targets"
                )
    return output


def calibration_phenotype_observations(
    phenotype: RelationshipPhenotypeFreeze,
) -> tuple[CalibrationPhenotypeObservation, ...]:
    """Extract classified rows while refusing cross-question duplicate weighting.

    The questionnaire deliberately revisits some constructs. A later calibration
    job must use an explicitly frozen consolidation rule; silently averaging or
    counting repeated axis/direction rows would manufacture extra evidence.
    """

    if (
        phenotype.schema_version != "relationship-phenotype-freeze-v2"
        or phenotype.validation_contract_version != VALIDATION_CONTRACT_VERSION
        or phenotype.validation_contract_sha256 != VALIDATION_CONTRACT_SHA256
    ):
        raise ValueError("calibration extraction requires a current validated phenotype freeze")

    unresolved_axis_ids = {
        axis_id
        for question in phenotype.output.question_results
        for axis_id in question.unresolved_axis_ids
    }
    observations: list[CalibrationPhenotypeObservation] = []
    seen: dict[tuple[str, AxisDirection], str] = {}
    for question in phenotype.output.question_results:
        for axis in question.axis_results:
            identity = (axis.axis_id, axis.direction)
            previous_question = seen.get(identity)
            if previous_question is not None:
                raise ValueError(
                    f"duplicate axis/direction across questions: "
                    f"{previous_question} and {question.question_id}"
                )
            seen[identity] = question.question_id
            if axis.status != "classified":
                continue
            if axis.axis_id in unresolved_axis_ids:
                raise ValueError(
                    f"axis {axis.axis_id} is calibration-ineligible because a repeated "
                    "probe remains unresolved"
                )
            if (
                axis.ordinal_value is None
                or not axis.evidence_spans
                or axis.confidence < phenotype.minimum_confidence
            ):
                raise ValueError("classified calibration row is incomplete")
            observations.append(
                CalibrationPhenotypeObservation(
                    phenotype_freeze_sha256=phenotype.freeze_sha256,
                    question_id=question.question_id,
                    axis_id=axis.axis_id,
                    direction=axis.direction,
                    ordinal_value=axis.ordinal_value,
                    trajectory=axis.trajectory,
                    classifier_confidence=axis.confidence,
                    context_conditions=axis.context_conditions,
                    observability_limits=axis.observability_limits,
                )
            )
    return tuple(observations)


def _directions_for_scope(scope: AxisScope) -> frozenset[AxisDirection]:
    if scope == "directional":
        return frozenset(("a_to_b", "b_to_a"))
    if scope == "dyadic":
        return frozenset(("dyadic",))
    return frozenset(("person_a", "person_b"))
