"""Development-only coding layer for repeated-series reports.

The reconciled Life Patterns codebook allows a detailed episode plus an anchored repeated-series
report to support provisional recurrence.  Structured Annotation V2 is intentionally episode
level, so treating a series report as a pseudo-episode would blur the primary unit and could
inflate evidence counts.  This module keeps series evidence separate while allowing a blind
coder to classify the behavior described by a genuinely repeated report.

Only series reports with some exact participant text are eligible for this development coding
layer.  Summary-only series reports remain preserved in the transfer corpus but are blocked from
automated series coding until source text is available.  This is development evidence only and
cannot be used as a validation substitute for a canonical behavioral freeze.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import sha256_json

from .development_transfer_corpus import (
    DevelopmentSourceSegment,
    DevelopmentTransferCorpusArtifact,
)
from .neutral_measurement import OntologyReleaseArtifact, ScalarValue, TheoryExposureState
from .structured_annotation_v2 import (
    MissingnessFlag,
    NonActionGateAssessmentV2,
    StructuredCodingProcedureArtifactV2,
    ValueRelation,
    structured_procedure_errors,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"

SeriesEvidenceState = Literal["observed", "insufficient", "not_applicable"]
SeriesAnchorRelation = Literal[
    "no_anchor_identified",
    "includes_anchor_episode",
    "excludes_anchor_episode",
    "anchor_relation_unknown",
]


class DevelopmentSeriesModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentSeriesCodingTask(DevelopmentSeriesModel):
    schema_version: Literal["life-patterns-development-series-coding-task-v1"] = (
        "life-patterns-development-series-coding-task-v1"
    )
    task_id: str = Field(pattern=r"^LPST-[0-9A-F]{20}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    series_id: str = Field(min_length=1)
    domain_id: str | None = None
    bounded_period_context: str = Field(min_length=1)
    approximate_age_life_phase: str = Field(min_length=1)
    recurrence_language: str = Field(min_length=1)
    rough_opportunity_count: str | None = None
    behavior_reportedly_recurred: str = Field(min_length=1)
    explicit_exceptions_or_limits: str | None = None
    memory_source_uncertainty: str | None = None
    exact_source_segments: tuple[DevelopmentSourceSegment, ...] = Field(min_length=1)
    observable_ids: tuple[str, ...] = Field(min_length=1)
    participant_theory_exposure: TheoryExposureState
    summary_fields_are_secondary_to_exact_source_text: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    birth_chart_model_blind: Literal[True] = True

    @field_validator("observable_ids")
    @classmethod
    def observable_ids_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("development series task repeats an observable identity")
        return value


class DevelopmentSeriesTaskBuildReport(DevelopmentSeriesModel):
    schema_version: Literal["life-patterns-development-series-task-build-report-v1"] = (
        "life-patterns-development-series-task-build-report-v1"
    )
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    tasks: tuple[DevelopmentSeriesCodingTask, ...]
    blocked_summary_only_series_ids: tuple[str, ...]
    eligible_series_count: int = Field(ge=0)
    blocked_series_count: int = Field(ge=0)
    source_complete_series_required_for_validation: Literal[True] = True

    @model_validator(mode="after")
    def counts_match_rows(self) -> DevelopmentSeriesTaskBuildReport:
        if self.eligible_series_count != len(self.tasks):
            raise ValueError("eligible series count disagrees with task count")
        if self.blocked_series_count != len(self.blocked_summary_only_series_ids):
            raise ValueError("blocked series count disagrees with blocked identity count")
        return self


class DevelopmentSeriesAnnotationResponse(DevelopmentSeriesModel):
    schema_version: Literal["life-patterns-development-series-annotation-response-v1"] = (
        "life-patterns-development-series-annotation-response-v1"
    )
    task_id: str = Field(pattern=r"^LPST-[0-9A-F]{20}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    series_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    state: SeriesEvidenceState
    coded_values: tuple[ScalarValue, ...] = ()
    value_relation: ValueRelation | None = None
    minimum_reported_occurrences: int | None = Field(default=None, ge=2)
    anchor_episode_id: str | None = None
    anchor_relation: SeriesAnchorRelation = "no_anchor_identified"
    asserts_non_action: bool = False
    non_action_gate: NonActionGateAssessmentV2 | None = None
    other_specified_description: str | None = None
    supporting_source_segment_ids: tuple[str, ...] = ()
    context_qualifiers: tuple[str, ...] = ()
    missingness_flags: tuple[MissingnessFlag, ...] = ()
    life_phase_qualifier: str | None = None
    theory_exposure: TheoryExposureState = "unknown"
    annotation_note: str | None = None
    series_is_recurrence_support_not_primary_episode: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @field_validator("missingness_flags")
    @classmethod
    def missingness_flags_are_unique(
        cls,
        value: tuple[MissingnessFlag, ...],
    ) -> tuple[MissingnessFlag, ...]:
        if len(value) != len(set(value)):
            raise ValueError("development series annotation repeats a missingness flag")
        return value

    @model_validator(mode="after")
    def state_contract_is_coherent(self) -> DevelopmentSeriesAnnotationResponse:
        if self.state == "observed":
            if not self.coded_values or self.value_relation is None:
                raise ValueError("observed series evidence requires coded values and value relation")
            if self.minimum_reported_occurrences is None:
                raise ValueError("observed series evidence requires a reported recurrence floor")
            if not self.supporting_source_segment_ids:
                raise ValueError("observed series evidence requires exact source-segment support")
            if self.value_relation == "single" and len(self.coded_values) != 1:
                raise ValueError("single series value relation requires exactly one coded value")
            if self.value_relation in {"ordered_sequence", "unordered_multiple"} and len(
                self.coded_values
            ) < 2:
                raise ValueError("multi-value series relation requires at least two coded values")
        elif (
            self.coded_values
            or self.value_relation is not None
            or self.minimum_reported_occurrences is not None
            or self.asserts_non_action
            or self.other_specified_description is not None
        ):
            raise ValueError(
                "insufficient/not-applicable series evidence cannot assert substantive recurrence"
            )

        if self.asserts_non_action and (
            self.non_action_gate is None or not self.non_action_gate.all_established
        ):
            raise ValueError("series-level substantive non-action requires the full four-part gate")

        if self.anchor_episode_id is None:
            if self.anchor_relation != "no_anchor_identified":
                raise ValueError("series anchor relation requires an anchor episode identity")
        elif self.anchor_relation == "no_anchor_identified":
            raise ValueError("identified anchor episode requires an explicit anchor relation")
        return self


class DevelopmentSeriesCodingManifestPayload(DevelopmentSeriesModel):
    schema_version: Literal["life-patterns-development-series-coding-manifest-v1"] = (
        "life-patterns-development-series-coding-manifest-v1"
    )
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    task_count: int = Field(ge=1)
    expected_series_observable_unit_count: int = Field(ge=1)
    blocked_summary_only_series_ids: tuple[str, ...]
    series_reports_are_not_episode_counts: Literal[True] = True
    target_model_information_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("series coding manifest timestamp must be timezone-aware")
        return value.astimezone(UTC)


class DevelopmentSeriesCodingManifestArtifact(DevelopmentSeriesModel):
    schema_version: Literal["life-patterns-development-series-coding-manifest-artifact-v1"] = (
        "life-patterns-development-series-coding-manifest-artifact-v1"
    )
    manifest_id: str = Field(pattern=r"^LPSM-[0-9A-F]{20}$")
    manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentSeriesCodingManifestPayload


def build_development_series_tasks(
    corpus: DevelopmentTransferCorpusArtifact,
    *,
    observable_ids: tuple[str, ...],
) -> DevelopmentSeriesTaskBuildReport:
    if not observable_ids or len(observable_ids) != len(set(observable_ids)):
        raise ValueError("series task observable IDs must be nonempty and unique")

    tasks: list[DevelopmentSeriesCodingTask] = []
    blocked: list[str] = []
    for series in corpus.payload.series_reports:
        if not series.exact_source_segments:
            blocked.append(series.series_id)
            continue
        payload = {
            "corpus_id": corpus.corpus_id,
            "corpus_sha256": corpus.corpus_sha256,
            "series_id": series.series_id,
            "domain_id": series.domain_id,
            "bounded_period_context": series.bounded_period_context,
            "approximate_age_life_phase": series.approximate_age_life_phase,
            "recurrence_language": series.recurrence_language,
            "rough_opportunity_count": series.rough_opportunity_count,
            "behavior_reportedly_recurred": series.behavior_reportedly_recurred,
            "explicit_exceptions_or_limits": series.explicit_exceptions_or_limits,
            "memory_source_uncertainty": series.memory_source_uncertainty,
            "exact_source_segments": series.exact_source_segments,
            "observable_ids": observable_ids,
            "participant_theory_exposure": corpus.payload.participant_theory_exposure,
        }
        digest = sha256_json(payload)
        tasks.append(
            DevelopmentSeriesCodingTask(
                task_id=f"LPST-{digest[:20].upper()}",
                **payload,
            )
        )
    return DevelopmentSeriesTaskBuildReport(
        corpus_id=corpus.corpus_id,
        corpus_sha256=corpus.corpus_sha256,
        tasks=tuple(tasks),
        blocked_summary_only_series_ids=tuple(sorted(blocked)),
        eligible_series_count=len(tasks),
        blocked_series_count=len(blocked),
    )


def build_development_series_manifest(
    report: DevelopmentSeriesTaskBuildReport,
    *,
    created_at_utc: datetime,
) -> DevelopmentSeriesCodingManifestArtifact:
    if not report.tasks:
        raise ValueError("no exact-source repeated-series reports are eligible for coding")
    observable_ids = report.tasks[0].observable_ids
    if any(task.observable_ids != observable_ids for task in report.tasks):
        raise ValueError("series task set has inconsistent observable universes")
    task_set_sha256 = sha256_json(report.tasks)
    payload = DevelopmentSeriesCodingManifestPayload(
        corpus_id=report.corpus_id,
        corpus_sha256=report.corpus_sha256,
        task_set_sha256=task_set_sha256,
        task_count=len(report.tasks),
        expected_series_observable_unit_count=len(report.tasks) * len(observable_ids),
        blocked_summary_only_series_ids=report.blocked_summary_only_series_ids,
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentSeriesCodingManifestArtifact(
        manifest_id=f"LPSM-{digest[:20].upper()}",
        manifest_sha256=digest,
        payload=payload,
    )


def _value_allowed(value: ScalarValue, definition: Any) -> bool:
    if definition.value_type in {"nominal", "ordinal"}:
        return isinstance(value, str) and value in definition.allowed_values
    if definition.value_type == "boolean":
        return isinstance(value, bool)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    numeric = float(value)
    if definition.numeric_min is not None and numeric < definition.numeric_min:
        return False
    return definition.numeric_max is None or numeric <= definition.numeric_max


def development_series_response_errors(
    response: DevelopmentSeriesAnnotationResponse,
    *,
    task: DevelopmentSeriesCodingTask,
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
) -> tuple[str, ...]:
    errors = list(structured_procedure_errors(procedure, ontology))
    if response.task_id != task.task_id:
        errors.append("series response does not bind supplied task")
    if response.corpus_id != task.corpus_id or response.corpus_sha256 != task.corpus_sha256:
        errors.append("series response does not bind development corpus")
    if response.series_id != task.series_id:
        errors.append("series response does not bind supplied series report")
    if response.observable_id not in task.observable_ids:
        errors.append("series response references observable outside task")

    source_ids = {segment.segment_id for segment in task.exact_source_segments}
    if not set(response.supporting_source_segment_ids).issubset(source_ids):
        errors.append("series response cites source segments outside supplied task")

    definitions = {row.observable_id: row for row in ontology.payload.observables}
    definition = definitions.get(response.observable_id)
    if definition is None:
        errors.append("series response references unknown ontology observable")
    else:
        for value in response.coded_values:
            if not _value_allowed(value, definition):
                errors.append(
                    f"series annotation for {response.observable_id} contains value outside codebook"
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
        errors.append("series non-action flag disagrees with frozen procedure registry")
    if expected_non_action and (
        response.non_action_gate is None or not response.non_action_gate.all_established
    ):
        errors.append("series non-action value lacks fully established gate")

    expected_other_specified = bool(
        extension
        and extension.other_specified_value is not None
        and any(
            isinstance(value, str) and value == extension.other_specified_value
            for value in response.coded_values
        )
    )
    if expected_other_specified != (response.other_specified_description is not None):
        errors.append("series Other Specified description disagrees with frozen procedure registry")
    return tuple(dict.fromkeys(errors))


def series_supports_additional_occurrence_for_anchor(
    response: DevelopmentSeriesAnnotationResponse,
    *,
    anchor_episode_id: str,
    substantive_value: ScalarValue,
) -> bool:
    """Whether a coded series proves >=1 occurrence independent of a detailed anchor episode."""

    if response.state != "observed" or substantive_value not in response.coded_values:
        return False
    if response.minimum_reported_occurrences is None:
        return False
    if response.anchor_episode_id != anchor_episode_id:
        return False
    if response.anchor_relation == "excludes_anchor_episode":
        return response.minimum_reported_occurrences >= 2
    if response.anchor_relation == "includes_anchor_episode":
        return response.minimum_reported_occurrences >= 2
    return False


def series_supports_stronger_repeated_condition(
    response: DevelopmentSeriesAnnotationResponse,
) -> bool:
    """Codebook stronger repeated-condition floor: at least three reported opportunities."""

    return (
        response.state == "observed"
        and response.minimum_reported_occurrences is not None
        and response.minimum_reported_occurrences >= 3
    )
