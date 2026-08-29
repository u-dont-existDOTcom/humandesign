"""Frozen chart-blind relationship phenotype records and validation."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

AxisDirection = Literal["a_to_b", "b_to_a", "dyadic", "person_a", "person_b"]
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
    schema_version: Literal["relationship-phenotype-freeze-v1"] = (
        "relationship-phenotype-freeze-v1"
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

    @property
    def freeze_sha256(self) -> str:
        return canonical_sha256(self.model_dump(mode="json"))


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
) -> tuple[str, ...]:
    texts: list[str] = []
    for record in answers:
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
            text = row.get("answer")
            if isinstance(text, str) and text.strip():
                texts.append(text.strip())
    return tuple(texts)


def validate_phenotype_output(
    output: RelationshipPhenotypeOutput,
    *,
    submitted_question_ids: set[str],
    allowed_axis_ids: set[str],
    source_texts: tuple[str, ...],
    minimum_confidence: float,
) -> RelationshipPhenotypeOutput:
    """Enforce frozen protocol identities and literal-evidence provenance."""

    returned_questions = [row.question_id for row in output.question_results]
    if len(returned_questions) != len(set(returned_questions)):
        raise ValueError("phenotype output contains duplicate question ids")
    if set(returned_questions) != submitted_question_ids:
        raise ValueError("phenotype output must cover exactly the submitted question ids")

    for question in output.question_results:
        for axis in question.axis_results:
            if axis.axis_id not in allowed_axis_ids:
                raise ValueError(f"classifier returned unknown axis: {axis.axis_id}")
            if axis.status == "classified" and axis.ordinal_value is None:
                raise ValueError("classified phenotype axis requires ordinal_value")
            if axis.status != "classified" and axis.ordinal_value is not None:
                raise ValueError("non-classified phenotype axis must not force ordinal_value")
            if axis.status == "classified" and axis.confidence < minimum_confidence:
                raise ValueError("classified phenotype axis is below the frozen confidence gate")
            for span in (*axis.evidence_spans, *axis.counterevidence_spans):
                if not span.strip():
                    raise ValueError("evidence spans cannot be blank")
                if not any(span in source for source in source_texts):
                    raise ValueError("classifier cited evidence not present verbatim in responses")
        for axis_id in question.unresolved_axis_ids:
            if axis_id not in allowed_axis_ids:
                raise ValueError(f"classifier returned unknown unresolved axis: {axis_id}")
    return output
