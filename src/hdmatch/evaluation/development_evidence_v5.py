"""Development-only episode and repeated-series responses using the reviewed v5 graph.

The historical v1/v2 response contracts remain immutable. New development calibration and
subsequent automated development coding use the facet/stage/provenance graph accepted by the
independent v5 review while retaining the recurrence-v2 evidence firewall for repeated series.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .development_series_evidence import DevelopmentSeriesCodingTask
from .development_series_evidence_v2 import (
    ExceptionFrequencyClass,
    FrequencyEvidenceBasis,
    RecurrenceExceptionStatus,
    ReportedRecurrenceStrength,
)
from .development_transfer_corpus import DevelopmentEpisodeCodingTask
from .facet_relation_v5 import ObservableResponseV5, observable_response_v5_errors
from .neutral_measurement import OntologyReleaseArtifact

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
_V5_REVIEW_COMMIT = "ce04642146c41a7d5d94f85360572c78de887682"


class DevelopmentV5Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentEpisodeAnnotationResponseV5(DevelopmentV5Model):
    schema_version: Literal["life-patterns-development-episode-annotation-response-v5"] = (
        "life-patterns-development-episode-annotation-response-v5"
    )
    task_id: str = Field(pattern=r"^LPDT-[0-9A-F]{20}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_id: str = Field(min_length=1)
    observable_id: str = Field(pattern=r"^NBM-R\d{2}$")
    response_graph: ObservableResponseV5
    accepted_contract_review_commit: Literal[
        "ce04642146c41a7d5d94f85360572c78de887682"
    ] = _V5_REVIEW_COMMIT
    transfer_summary_is_not_primary_source: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @model_validator(mode="after")
    def graph_identity_is_coherent(self) -> DevelopmentEpisodeAnnotationResponseV5:
        if self.response_graph.observable_id != self.observable_id:
            raise ValueError("episode v5 graph observable does not match response observable")
        if self.response_graph.response_scope_id != self.episode_id:
            raise ValueError("episode v5 graph scope does not match episode identity")
        return self


class DevelopmentSeriesAnnotationResponseV5(DevelopmentV5Model):
    schema_version: Literal["life-patterns-development-series-annotation-response-v5"] = (
        "life-patterns-development-series-annotation-response-v5"
    )
    task_id: str = Field(pattern=r"^LPST-[0-9A-F]{20}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    series_id: str = Field(min_length=1)
    observable_id: str = Field(pattern=r"^NBM-R\d{2}$")
    response_graph: ObservableResponseV5

    reported_recurrence_strength: ReportedRecurrenceStrength | None = None
    exception_status: RecurrenceExceptionStatus | None = None
    exception_frequency: ExceptionFrequencyClass | None = None
    frequency_evidence_basis: FrequencyEvidenceBasis | None = None
    minimum_reported_occurrences: int | None = Field(default=None, ge=2)
    bounded_rate_or_count_description: str | None = None
    recurrence_scope_description: str | None = None

    confirming_episode_counted_as_independent_frequency_evidence: Literal[False] = False
    series_is_recurrence_support_not_primary_episode: Literal[True] = True
    reported_recurrence_is_not_verified_true_frequency: Literal[True] = True
    summary_fields_are_not_primary_source: Literal[True] = True
    accepted_contract_review_commit: Literal[
        "ce04642146c41a7d5d94f85360572c78de887682"
    ] = _V5_REVIEW_COMMIT
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @model_validator(mode="after")
    def graph_and_recurrence_are_coherent(self) -> DevelopmentSeriesAnnotationResponseV5:
        if self.response_graph.observable_id != self.observable_id:
            raise ValueError("series v5 graph observable does not match response observable")
        if self.response_graph.response_scope_id != self.series_id:
            raise ValueError("series v5 graph scope does not match series identity")

        recurrence_fields = (
            self.reported_recurrence_strength,
            self.exception_status,
            self.exception_frequency,
            self.frequency_evidence_basis,
            self.minimum_reported_occurrences,
            self.bounded_rate_or_count_description,
            self.recurrence_scope_description,
        )
        if self.response_graph.state == "observed":
            if self.reported_recurrence_strength is None:
                raise ValueError("observed series v5 response requires reported recurrence strength")
            if self.exception_status is None:
                raise ValueError("observed series v5 response requires exception status")
            if self.frequency_evidence_basis is None:
                raise ValueError("observed series v5 response requires frequency evidence basis")
        elif any(value is not None for value in recurrence_fields):
            raise ValueError(
                "insufficient/not-applicable series v5 response cannot assert recurrence fields"
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
        return self


def _ontology_value_ids(ontology: OntologyReleaseArtifact, observable_id: str) -> set[str]:
    for definition in ontology.payload.observables:
        if definition.observable_id == observable_id:
            if definition.value_type not in {"nominal", "ordinal"}:
                return set()
            return set(definition.allowed_values)
    return set()


def _graph_value_errors(
    response_graph: ObservableResponseV5,
    *,
    ontology: OntologyReleaseArtifact,
) -> tuple[str, ...]:
    allowed = _ontology_value_ids(ontology, response_graph.observable_id)
    if not allowed:
        return ("v5 response references an unknown or non-categorical observable",)
    errors = [
        f"v5 assertion {row.assertion_id} uses value outside ontology"
        for row in response_graph.value_assertions
        if row.value_id not in allowed
    ]
    return tuple(errors)


def development_episode_response_errors_v5(
    response: DevelopmentEpisodeAnnotationResponseV5,
    *,
    task: DevelopmentEpisodeCodingTask,
    ontology: OntologyReleaseArtifact,
    contract: dict[str, object],
) -> tuple[str, ...]:
    errors: list[str] = []
    if response.task_id != task.task_id:
        errors.append("episode v5 response does not bind supplied task")
    if response.corpus_id != task.corpus_id or response.corpus_sha256 != task.corpus_sha256:
        errors.append("episode v5 response does not bind development corpus")
    if response.episode_id != task.episode_id:
        errors.append("episode v5 response does not bind supplied episode")
    if response.observable_id not in task.observable_ids:
        errors.append("episode v5 response references observable outside task")
    source_ids = {segment.segment_id for segment in task.exact_source_segments}
    errors.extend(
        observable_response_v5_errors(
            response.response_graph,
            contract=contract,
            valid_source_record_ids=source_ids,
        )
    )
    errors.extend(_graph_value_errors(response.response_graph, ontology=ontology))
    return tuple(dict.fromkeys(errors))


def development_series_response_errors_v5(
    response: DevelopmentSeriesAnnotationResponseV5,
    *,
    task: DevelopmentSeriesCodingTask,
    ontology: OntologyReleaseArtifact,
    contract: dict[str, object],
) -> tuple[str, ...]:
    errors: list[str] = []
    if response.task_id != task.task_id:
        errors.append("series v5 response does not bind supplied task")
    if response.corpus_id != task.corpus_id or response.corpus_sha256 != task.corpus_sha256:
        errors.append("series v5 response does not bind development corpus")
    if response.series_id != task.series_id:
        errors.append("series v5 response does not bind supplied series report")
    if response.observable_id not in task.observable_ids:
        errors.append("series v5 response references observable outside task")
    source_ids = {segment.segment_id for segment in task.exact_source_segments}
    errors.extend(
        observable_response_v5_errors(
            response.response_graph,
            contract=contract,
            valid_source_record_ids=source_ids,
        )
    )
    errors.extend(_graph_value_errors(response.response_graph, ontology=ontology))
    return tuple(dict.fromkeys(errors))


def series_supports_opportunity_level_frequency_inference_v5(
    response: DevelopmentSeriesAnnotationResponseV5,
) -> bool:
    return response.response_graph.state == "observed" and response.frequency_evidence_basis in {
        "sampled_opportunities",
        "external_record_or_observation",
        "mixed_basis",
    }
