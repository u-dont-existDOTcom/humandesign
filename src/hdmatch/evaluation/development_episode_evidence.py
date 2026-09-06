"""Development-only episode annotation responses for partial-source v8/v8.1 transfer tasks.

This mirrors the substantive Structured Annotation V2 semantics without pretending the source is
a canonical BPF freeze. Evidence citations use exact participant source-segment IDs supplied by
the development task. Transfer summaries may orient the coder but cannot substitute for exact
source text when asserting an observed value.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .development_transfer_corpus import DevelopmentEpisodeCodingTask
from .neutral_measurement import (
    ObservableDefinition,
    OntologyReleaseArtifact,
    ScalarValue,
    TheoryExposureState,
)
from .structured_annotation_v2 import (
    InfluenceRelation,
    MissingnessFlag,
    NonActionGateAssessmentV2,
    PrimaryEpisodeState,
    StructuredCodingProcedureArtifactV2,
    ValueRelation,
    structured_procedure_errors,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class DevelopmentEpisodeModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentEpisodeAnnotationResponse(DevelopmentEpisodeModel):
    schema_version: Literal["life-patterns-development-episode-annotation-response-v1"] = (
        "life-patterns-development-episode-annotation-response-v1"
    )
    task_id: str = Field(pattern=r"^LPDT-[0-9A-F]{20}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    state: PrimaryEpisodeState
    coded_values: tuple[ScalarValue, ...] = ()
    value_relation: ValueRelation | None = None
    asserts_non_action: bool = False
    non_action_gate: NonActionGateAssessmentV2 | None = None
    other_specified_description: str | None = None
    supporting_source_segment_ids: tuple[str, ...] = ()
    counterevidence_source_segment_ids: tuple[str, ...] = ()
    context_qualifiers: tuple[str, ...] = ()
    missingness_flags: tuple[MissingnessFlag, ...] = ()
    life_phase_qualifier: str | None = None
    language: str | None = None
    influence_relation: InfluenceRelation = "none_reported"
    influence_source_segment_ids: tuple[str, ...] = ()
    theory_exposure: TheoryExposureState = "unknown"
    annotation_note: str | None = None
    transfer_summary_is_not_primary_source: Literal[True] = True
    person_level_contradiction_or_mixed_not_encoded_here: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @field_validator("missingness_flags")
    @classmethod
    def missingness_flags_are_unique(
        cls,
        value: tuple[MissingnessFlag, ...],
    ) -> tuple[MissingnessFlag, ...]:
        if len(value) != len(set(value)):
            raise ValueError("development episode annotation repeats a missingness flag")
        return value

    @model_validator(mode="after")
    def state_contract_is_coherent(self) -> DevelopmentEpisodeAnnotationResponse:
        if self.state == "observed":
            if not self.coded_values or self.value_relation is None:
                raise ValueError("observed development episode requires coded values and relation")
            if not self.supporting_source_segment_ids:
                raise ValueError("observed development episode requires exact source-segment support")
            if self.value_relation == "single" and len(self.coded_values) != 1:
                raise ValueError("single episode value relation requires exactly one coded value")
            if self.value_relation in {"ordered_sequence", "unordered_multiple"} and len(
                self.coded_values
            ) < 2:
                raise ValueError("multi-value episode relation requires at least two coded values")
        elif (
            self.coded_values
            or self.value_relation is not None
            or self.asserts_non_action
            or self.other_specified_description is not None
        ):
            raise ValueError(
                "insufficient/not-applicable development episode cannot assert substantive values"
            )

        if self.asserts_non_action and (
            self.non_action_gate is None or not self.non_action_gate.all_established
        ):
            raise ValueError("development episode non-action requires the full four-part gate")
        if self.influence_relation == "none_reported" and self.influence_source_segment_ids:
            raise ValueError("no reported influence cannot cite influence source segments")
        if self.influence_relation != "none_reported" and not self.influence_source_segment_ids:
            raise ValueError("reported influence relation requires exact source-segment provenance")
        return self


def _value_allowed(value: ScalarValue, definition: ObservableDefinition) -> bool:
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


def development_episode_response_errors(
    response: DevelopmentEpisodeAnnotationResponse,
    *,
    task: DevelopmentEpisodeCodingTask,
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
) -> tuple[str, ...]:
    errors = list(structured_procedure_errors(procedure, ontology))
    if response.task_id != task.task_id:
        errors.append("development episode response does not bind supplied task")
    if response.corpus_id != task.corpus_id or response.corpus_sha256 != task.corpus_sha256:
        errors.append("development episode response does not bind development corpus")
    if response.episode_id != task.episode_id:
        errors.append("development episode response does not bind supplied episode")
    if response.observable_id not in task.observable_ids:
        errors.append("development episode response references observable outside task")

    source_ids = {segment.segment_id for segment in task.exact_source_segments}
    if not set(response.supporting_source_segment_ids).issubset(source_ids):
        errors.append("development episode response cites supporting source outside supplied task")
    if not set(response.counterevidence_source_segment_ids).issubset(source_ids):
        errors.append("development episode response cites counterevidence outside supplied task")
    if not set(response.influence_source_segment_ids).issubset(source_ids):
        errors.append("development episode response cites influence source outside supplied task")

    definitions = {row.observable_id: row for row in ontology.payload.observables}
    definition = definitions.get(response.observable_id)
    if definition is None:
        errors.append("development episode response references unknown ontology observable")
    else:
        for value in response.coded_values:
            if not _value_allowed(value, definition):
                errors.append(
                    f"development episode annotation for {response.observable_id} contains value outside codebook"
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
        errors.append("development episode non-action flag disagrees with frozen registry")
    if expected_non_action and (
        response.non_action_gate is None or not response.non_action_gate.all_established
    ):
        errors.append("development episode non-action value lacks fully established gate")

    expected_other_specified = bool(
        extension
        and extension.other_specified_value is not None
        and any(
            isinstance(value, str) and value == extension.other_specified_value
            for value in response.coded_values
        )
    )
    if expected_other_specified != (response.other_specified_description is not None):
        errors.append(
            "development episode Other Specified description disagrees with frozen registry"
        )
    return tuple(dict.fromkeys(errors))
