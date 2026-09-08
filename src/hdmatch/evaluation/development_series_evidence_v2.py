"""Recurrence-corrected development-only repeated-series annotation contract.

V1 remains immutable historical development behavior.  V2 preserves generalized behavioral
recurrence self-report directly, keeps exception status and evidence basis explicit, and forbids
using self-selected confirming episodes as independent frequency evidence.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .development_series_evidence import DevelopmentSeriesCodingTask, SeriesEvidenceState
from .neutral_measurement import OntologyReleaseArtifact, ScalarValue, TheoryExposureState
from .structured_annotation_v2 import (
    MissingnessFlag,
    NonActionGateAssessmentV2,
    StructuredCodingProcedureArtifactV2,
    ValueRelation,
    structured_procedure_errors,
)

ReportedRecurrenceStrength = Literal[
    "universal_language",
    "near_universal",
    "usually",
    "often",
    "sometimes",
    "rarely",
    "repeated_unquantified",
    "bounded_rate_or_count",
    "context_conditional",
    "changed_over_time",
    "unclear",
]
RecurrenceExceptionStatus = Literal[
    "exceptions_explicitly_denied",
    "exceptions_reported",
    "exceptions_not_probed_or_unknown",
]
ExceptionFrequencyClass = Literal[
    "none_reported",
    "almost_never",
    "sometimes",
    "often",
    "context_dependent",
    "rough_rate_or_count",
    "unknown",
]
FrequencyEvidenceBasis = Literal[
    "generalized_self_report",
    "bounded_rate_or_count_self_report",
    "sampled_opportunities",
    "external_record_or_observation",
    "mixed_basis",
]


class DevelopmentSeriesV2Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentSeriesAnnotationResponseV2(DevelopmentSeriesV2Model):
    schema_version: Literal["life-patterns-development-series-annotation-response-v2"] = (
        "life-patterns-development-series-annotation-response-v2"
    )
    task_id: str = Field(pattern=r"^LPST-[0-9A-F]{20}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    series_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    state: SeriesEvidenceState
    coded_values: tuple[ScalarValue, ...] = ()
    value_relation: ValueRelation | None = None

    reported_recurrence_strength: ReportedRecurrenceStrength | None = None
    exception_status: RecurrenceExceptionStatus | None = None
    exception_frequency: ExceptionFrequencyClass | None = None
    frequency_evidence_basis: FrequencyEvidenceBasis | None = None
    minimum_reported_occurrences: int | None = Field(default=None, ge=2)
    bounded_rate_or_count_description: str | None = None
    recurrence_scope_description: str | None = None

    asserts_non_action: bool = False
    non_action_gate: NonActionGateAssessmentV2 | None = None
    other_specified_description: str | None = None
    supporting_source_segment_ids: tuple[str, ...] = ()
    counterevidence_source_segment_ids: tuple[str, ...] = ()
    context_qualifiers: tuple[str, ...] = ()
    missingness_flags: tuple[MissingnessFlag, ...] = ()
    life_phase_qualifier: str | None = None
    theory_exposure: TheoryExposureState = "unknown"
    annotation_note: str | None = None

    confirming_episode_counted_as_independent_frequency_evidence: Literal[False] = False
    series_is_recurrence_support_not_primary_episode: Literal[True] = True
    reported_recurrence_is_not_verified_true_frequency: Literal[True] = True
    summary_fields_are_not_primary_source: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @field_validator("missingness_flags")
    @classmethod
    def missingness_flags_are_unique(
        cls,
        value: tuple[MissingnessFlag, ...],
    ) -> tuple[MissingnessFlag, ...]:
        if len(value) != len(set(value)):
            raise ValueError("development series v2 annotation repeats a missingness flag")
        return value

    @model_validator(mode="after")
    def state_contract_is_coherent(self) -> DevelopmentSeriesAnnotationResponseV2:
        if self.state == "observed":
            if not self.coded_values or self.value_relation is None:
                raise ValueError("observed series v2 evidence requires coded values and relation")
            if not self.supporting_source_segment_ids:
                raise ValueError("observed series v2 evidence requires exact source-segment support")
            if self.reported_recurrence_strength is None:
                raise ValueError("observed series v2 evidence requires reported recurrence strength")
            if self.exception_status is None:
                raise ValueError("observed series v2 evidence requires explicit exception-status coding")
            if self.frequency_evidence_basis is None:
                raise ValueError("observed series v2 evidence requires a frequency evidence basis")
            if self.value_relation == "single" and len(self.coded_values) != 1:
                raise ValueError("single series v2 value relation requires exactly one coded value")
            if self.value_relation in {"ordered_sequence", "unordered_multiple"} and len(
                self.coded_values
            ) < 2:
                raise ValueError("multi-value series v2 relation requires at least two coded values")
        elif any(
            (
                self.coded_values,
                self.value_relation is not None,
                self.reported_recurrence_strength is not None,
                self.exception_status is not None,
                self.exception_frequency is not None,
                self.frequency_evidence_basis is not None,
                self.minimum_reported_occurrences is not None,
                self.bounded_rate_or_count_description is not None,
                self.recurrence_scope_description is not None,
                self.asserts_non_action,
                self.other_specified_description is not None,
            )
        ):
            raise ValueError(
                "insufficient/not-applicable series v2 evidence cannot assert substantive recurrence"
            )

        if self.exception_status == "exceptions_explicitly_denied" and self.exception_frequency != (
            "none_reported"
        ):
            raise ValueError("explicitly denied exceptions require exception_frequency=none_reported")
        if self.exception_status == "exceptions_reported" and self.exception_frequency == "none_reported":
            raise ValueError("reported exceptions cannot have exception_frequency=none_reported")
        if self.exception_status == "exceptions_not_probed_or_unknown" and self.exception_frequency not in {
            None,
            "unknown",
        }:
            raise ValueError("unknown exception status cannot assert a known exception frequency")

        count_bases = {
            "bounded_rate_or_count_self_report",
            "sampled_opportunities",
            "external_record_or_observation",
            "mixed_basis",
        }
        if self.minimum_reported_occurrences is not None and self.frequency_evidence_basis not in count_bases:
            raise ValueError(
                "minimum reported occurrences require bounded/sampled/external/mixed evidence basis"
            )
        if self.reported_recurrence_strength == "bounded_rate_or_count" and (
            self.frequency_evidence_basis not in count_bases
            or (
                self.minimum_reported_occurrences is None
                and not (self.bounded_rate_or_count_description or "").strip()
            )
        ):
            raise ValueError(
                "bounded rate/count recurrence requires bounded evidence and a supported count/rate description"
            )

        if self.asserts_non_action and (
            self.non_action_gate is None or not self.non_action_gate.all_established
        ):
            raise ValueError("series v2 substantive non-action requires the full four-part gate")
        return self


def _value_allowed(value: ScalarValue, definition: object) -> bool:
    value_type = getattr(definition, "value_type")
    if value_type in {"nominal", "ordinal"}:
        return isinstance(value, str) and value in getattr(definition, "allowed_values")
    if value_type == "boolean":
        return isinstance(value, bool)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    numeric = float(value)
    numeric_min = getattr(definition, "numeric_min")
    numeric_max = getattr(definition, "numeric_max")
    if numeric_min is not None and numeric < numeric_min:
        return False
    return numeric_max is None or numeric <= numeric_max


def development_series_response_errors_v2(
    response: DevelopmentSeriesAnnotationResponseV2,
    *,
    task: DevelopmentSeriesCodingTask,
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
) -> tuple[str, ...]:
    errors = list(structured_procedure_errors(procedure, ontology))
    if response.task_id != task.task_id:
        errors.append("series v2 response does not bind supplied task")
    if response.corpus_id != task.corpus_id or response.corpus_sha256 != task.corpus_sha256:
        errors.append("series v2 response does not bind development corpus")
    if response.series_id != task.series_id:
        errors.append("series v2 response does not bind supplied series report")
    if response.observable_id not in task.observable_ids:
        errors.append("series v2 response references observable outside task")

    source_ids = {segment.segment_id for segment in task.exact_source_segments}
    if not set(response.supporting_source_segment_ids).issubset(source_ids):
        errors.append("series v2 response cites supporting source outside supplied task")
    if not set(response.counterevidence_source_segment_ids).issubset(source_ids):
        errors.append("series v2 response cites counterevidence outside supplied task")

    definitions = {row.observable_id: row for row in ontology.payload.observables}
    definition = definitions.get(response.observable_id)
    if definition is None:
        errors.append("series v2 response references unknown ontology observable")
    else:
        for value in response.coded_values:
            if not _value_allowed(value, definition):
                errors.append(
                    f"series v2 annotation for {response.observable_id} contains value outside codebook"
                )

    extensions = {row.observable_id: row for row in procedure.payload.observable_extensions}
    extension = extensions.get(response.observable_id)
    expected_non_action = bool(
        extension
        and any(
            isinstance(value, str) and value in extension.non_action_values
            for value in response.coded_values
        )
    )
    if response.asserts_non_action != expected_non_action:
        errors.append("series v2 non-action flag disagrees with frozen procedure registry")
    if expected_non_action and (
        response.non_action_gate is None or not response.non_action_gate.all_established
    ):
        errors.append("series v2 non-action value lacks fully established gate")

    expected_other_specified = bool(
        extension
        and extension.other_specified_value is not None
        and any(
            isinstance(value, str) and value == extension.other_specified_value
            for value in response.coded_values
        )
    )
    if expected_other_specified != (response.other_specified_description is not None):
        errors.append("series v2 Other Specified description disagrees with frozen procedure registry")
    return tuple(dict.fromkeys(errors))


def series_supports_opportunity_level_frequency_inference_v2(
    response: DevelopmentSeriesAnnotationResponseV2,
) -> bool:
    """Whether the response basis can support more than reported-recurrence semantics."""

    return response.state == "observed" and response.frequency_evidence_basis in {
        "sampled_opportunities",
        "external_record_or_observation",
        "mixed_basis",
    }
