"""High-fidelity theory-blind annotation exchange for Life Patterns.

V1 annotation artifacts are intentionally left unchanged because adding default fields to the
existing Pydantic models would alter canonical serialization and content hashes. V2 adds the
measurement details required by the reconciled codebook: ordered within-episode sequences,
explicit non-action prerequisites, and narrator-influence versus temporal-precedence fields.

This module is still content-neutral. Substantive observable definitions and the designation of
which categorical values represent non-action come from separately frozen ontology/procedure
artifacts.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

from .neutral_measurement import (
    FreezeEvidenceIndex,
    OntologyReleaseArtifact,
    ScalarValue,
    TheoryExposureState,
    build_annotation_tasks,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"

PrimaryEpisodeState = Literal["observed", "insufficient", "not_applicable"]
ValueRelation = Literal["single", "ordered_sequence", "unordered_multiple"]
GateStatus = Literal["established", "not_established", "unclear"]
InfluenceRelation = Literal[
    "none_reported",
    "narrator_explicit_influence",
    "temporal_precedence_only",
]


class StructuredAnnotationModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class NonActionGateAssessmentV2(StructuredAnnotationModel):
    """Four prerequisites required before a substantive non-action may be asserted."""

    awareness: GateStatus
    opportunity: GateStatus
    feasibility: GateStatus
    established_non_action: GateStatus

    @property
    def all_established(self) -> bool:
        return all(
            value == "established"
            for value in (
                self.awareness,
                self.opportunity,
                self.feasibility,
                self.established_non_action,
            )
        )


class ObservableProcedureExtensionV2(StructuredAnnotationModel):
    observable_id: str = Field(min_length=1)
    non_action_values: tuple[str, ...] = ()

    @field_validator("non_action_values")
    @classmethod
    def non_action_values_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("observable procedure contains duplicate non-action values")
        return value


class StructuredCodingProcedurePayloadV2(StructuredAnnotationModel):
    schema_version: Literal["life-patterns-structured-coding-procedure-v2"] = (
        "life-patterns-structured-coding-procedure-v2"
    )
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    reconciled_codebook_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_manual_sha256: str = Field(pattern=_SHA256_PATTERN)
    observable_extensions: tuple[ObservableProcedureExtensionV2, ...]
    episode_boundaries_frozen_upstream: Literal[True] = True
    primary_episode_states_exclude_person_level_contradiction_and_mixed: Literal[True] = True
    target_model_information_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("structured coding procedure timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("observable_extensions")
    @classmethod
    def observable_extensions_are_unique(
        cls,
        value: tuple[ObservableProcedureExtensionV2, ...],
    ) -> tuple[ObservableProcedureExtensionV2, ...]:
        ids = [row.observable_id for row in value]
        if len(ids) != len(set(ids)):
            raise ValueError("structured coding procedure repeats an observable identity")
        return value


class StructuredCodingProcedureArtifactV2(StructuredAnnotationModel):
    schema_version: Literal["life-patterns-structured-coding-procedure-artifact-v2"] = (
        "life-patterns-structured-coding-procedure-artifact-v2"
    )
    procedure_id: str = Field(pattern=r"^LPSP-[0-9A-F]{20}$")
    procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: StructuredCodingProcedurePayloadV2


class StructuredAnnotationTaskV2(StructuredAnnotationModel):
    schema_version: Literal["life-patterns-structured-annotation-task-v2"] = (
        "life-patterns-structured-annotation-task-v2"
    )
    task_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    procedure_id: str = Field(pattern=r"^LPSP-[0-9A-F]{20}$")
    procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_id: str = Field(min_length=1)
    episode_title: str = Field(min_length=1)
    episode_narrative: str = Field(min_length=1)
    source_turns: tuple[dict[str, Any], ...]
    observable_ids: tuple[str, ...] = Field(min_length=1)
    episode_boundary_frozen_upstream: Literal[True] = True
    birth_chart_model_blind: Literal[True] = True


class StructuredAnnotationResponseV2(StructuredAnnotationModel):
    schema_version: Literal["life-patterns-structured-annotation-response-v2"] = (
        "life-patterns-structured-annotation-response-v2"
    )
    task_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    procedure_id: str = Field(pattern=r"^LPSP-[0-9A-F]{20}$")
    procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    state: PrimaryEpisodeState
    coded_values: tuple[ScalarValue, ...] = ()
    value_relation: ValueRelation | None = None
    asserts_non_action: bool = False
    non_action_gate: NonActionGateAssessmentV2 | None = None
    supporting_source_turn_ids: tuple[str, ...] = ()
    counterevidence_source_turn_ids: tuple[str, ...] = ()
    context_qualifiers: tuple[str, ...] = ()
    life_phase_qualifier: str | None = None
    language: str | None = None
    influence_relation: InfluenceRelation = "none_reported"
    influence_source_turn_ids: tuple[str, ...] = ()
    theory_exposure: TheoryExposureState = "unknown"
    annotation_note: str | None = None
    person_level_contradiction_or_mixed_not_encoded_here: Literal[True] = True

    @model_validator(mode="after")
    def state_and_values_are_coherent(self) -> StructuredAnnotationResponseV2:
        if self.state == "observed":
            if not self.coded_values or self.value_relation is None:
                raise ValueError("observed structured annotations require coded values and relation")
            if self.value_relation == "single" and len(self.coded_values) != 1:
                raise ValueError("single value relation requires exactly one coded value")
            if self.value_relation in {"ordered_sequence", "unordered_multiple"} and len(
                self.coded_values
            ) < 2:
                raise ValueError("multi-value relation requires at least two coded values")
            if not self.supporting_source_turn_ids:
                raise ValueError("observed structured annotations require supporting source turns")
        elif self.coded_values or self.value_relation is not None or self.asserts_non_action:
            raise ValueError(
                "insufficient/not-applicable structured annotations cannot assert substantive values"
            )

        if self.asserts_non_action:
            if self.non_action_gate is None or not self.non_action_gate.all_established:
                raise ValueError("substantive non-action requires all four gate elements established")

        if self.influence_relation == "none_reported" and self.influence_source_turn_ids:
            raise ValueError("no reported influence cannot cite influence source turns")
        if self.influence_relation != "none_reported" and not self.influence_source_turn_ids:
            raise ValueError("reported/temporal influence relation requires source-turn provenance")
        return self


def structured_procedure_errors(
    artifact: StructuredCodingProcedureArtifactV2,
    ontology: OntologyReleaseArtifact,
) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(artifact.payload)
    if artifact.procedure_sha256 != digest or artifact.procedure_id != f"LPSP-{digest[:20].upper()}":
        errors.append("structured coding procedure failed content-address verification")
    if (
        artifact.payload.ontology_artifact_id != ontology.artifact_id
        or artifact.payload.ontology_sha256 != ontology.ontology_sha256
    ):
        errors.append("structured coding procedure does not bind supplied ontology")

    definitions = {row.observable_id: row for row in ontology.payload.observables}
    extensions = {row.observable_id: row for row in artifact.payload.observable_extensions}
    unknown = sorted(set(extensions) - set(definitions))
    if unknown:
        errors.append("structured coding procedure references unknown observables: " + ", ".join(unknown))

    for observable_id, extension in extensions.items():
        definition = definitions.get(observable_id)
        if definition is None:
            continue
        if extension.non_action_values and definition.value_type not in {"nominal", "ordinal"}:
            errors.append(f"non-action registry for {observable_id} requires a categorical observable")
            continue
        unknown_values = sorted(set(extension.non_action_values) - set(definition.allowed_values))
        if unknown_values:
            errors.append(
                f"non-action registry for {observable_id} contains values outside its codebook: "
                + ", ".join(unknown_values)
            )
    return tuple(dict.fromkeys(errors))


def build_structured_coding_procedure_v2(
    payload: StructuredCodingProcedurePayloadV2,
    ontology: OntologyReleaseArtifact,
) -> StructuredCodingProcedureArtifactV2:
    digest = sha256_json(payload)
    artifact = StructuredCodingProcedureArtifactV2(
        procedure_id=f"LPSP-{digest[:20].upper()}",
        procedure_sha256=digest,
        payload=payload,
    )
    errors = structured_procedure_errors(artifact, ontology)
    if errors:
        raise ValueError("invalid structured coding procedure: " + "; ".join(errors))
    return artifact


def _validate_scalar_value(value: ScalarValue, definition: Any) -> bool:
    if definition.value_type in {"nominal", "ordinal"}:
        return isinstance(value, str) and value in definition.allowed_values
    if definition.value_type == "boolean":
        return isinstance(value, bool)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    numeric = float(value)
    if definition.numeric_min is not None and numeric < definition.numeric_min:
        return False
    if definition.numeric_max is not None and numeric > definition.numeric_max:
        return False
    return True


def structured_annotation_response_errors(
    response: StructuredAnnotationResponseV2,
    *,
    task: StructuredAnnotationTaskV2,
    evidence: FreezeEvidenceIndex,
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
) -> tuple[str, ...]:
    errors = list(structured_procedure_errors(procedure, ontology))
    if response.task_id != task.task_id:
        errors.append("structured annotation response does not bind supplied task")
    if (
        response.freeze_id != task.freeze_id
        or response.freeze_sha256 != task.freeze_sha256
        or response.freeze_id != evidence.freeze_id
        or response.freeze_sha256 != evidence.freeze_sha256
    ):
        errors.append("structured annotation response does not bind supplied behavioral freeze")
    if (
        response.ontology_artifact_id != task.ontology_artifact_id
        or response.ontology_sha256 != task.ontology_sha256
        or response.ontology_artifact_id != ontology.artifact_id
        or response.ontology_sha256 != ontology.ontology_sha256
    ):
        errors.append("structured annotation response does not bind supplied ontology")
    if (
        response.procedure_id != task.procedure_id
        or response.procedure_sha256 != task.procedure_sha256
        or response.procedure_id != procedure.procedure_id
        or response.procedure_sha256 != procedure.procedure_sha256
    ):
        errors.append("structured annotation response does not bind structured coding procedure")
    if response.episode_id != task.episode_id or response.episode_id not in evidence.episode_sha256:
        errors.append("structured annotation response does not bind supplied episode")
    if response.observable_id not in task.observable_ids:
        errors.append("structured annotation response references observable outside task")

    definitions = {row.observable_id: row for row in ontology.payload.observables}
    definition = definitions.get(response.observable_id)
    if definition is None:
        errors.append("structured annotation response references unknown ontology observable")
    else:
        for value in response.coded_values:
            if not _validate_scalar_value(value, definition):
                errors.append(
                    f"structured annotation for {response.observable_id} contains value outside codebook"
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
        errors.append("structured annotation non-action flag disagrees with frozen procedure registry")
    if expected_non_action and (
        response.non_action_gate is None or not response.non_action_gate.all_established
    ):
        errors.append("structured annotation non-action value lacks fully established gate")

    task_turn_ids = {
        str(row["turn_id"])
        for row in task.source_turns
        if isinstance(row.get("turn_id"), str)
    }
    cited = (
        set(response.supporting_source_turn_ids)
        | set(response.counterevidence_source_turn_ids)
        | set(response.influence_source_turn_ids)
    )
    if not cited.issubset(task_turn_ids):
        errors.append("structured annotation cites source turns outside supplied task")
    return tuple(dict.fromkeys(errors))


def build_structured_annotation_tasks_v2(
    freeze_artifact: dict[str, Any],
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
) -> tuple[StructuredAnnotationTaskV2, ...]:
    errors = structured_procedure_errors(procedure, ontology)
    if errors:
        raise ValueError("invalid structured coding procedure: " + "; ".join(errors))
    v1_tasks = build_annotation_tasks(freeze_artifact, ontology)
    return tuple(
        StructuredAnnotationTaskV2(
            task_id=f"{task.task_id}:V2",
            freeze_id=task.freeze_id,
            freeze_sha256=task.freeze_sha256,
            ontology_artifact_id=task.ontology_artifact_id,
            ontology_sha256=task.ontology_sha256,
            procedure_id=procedure.procedure_id,
            procedure_sha256=procedure.procedure_sha256,
            episode_id=task.episode_id,
            episode_title=task.episode_title,
            episode_narrative=task.episode_narrative,
            source_turns=task.source_turns,
            observable_ids=task.observable_ids,
        )
        for task in v1_tasks
    )


def structured_annotation_tasks_jsonl_v2(tasks: tuple[StructuredAnnotationTaskV2, ...]) -> bytes:
    return b"\n".join(canonical_json_bytes(task) for task in tasks) + (b"\n" if tasks else b"")


def structured_annotation_responses_jsonl_v2(
    responses: tuple[StructuredAnnotationResponseV2, ...],
) -> bytes:
    return b"\n".join(canonical_json_bytes(response) for response in responses) + (
        b"\n" if responses else b""
    )


def load_structured_annotation_responses_jsonl_v2(
    data: bytes,
) -> tuple[StructuredAnnotationResponseV2, ...]:
    responses: list[StructuredAnnotationResponseV2] = []
    for line_number, raw_line in enumerate(data.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            value: Any = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"structured annotation line {line_number} is invalid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"structured annotation line {line_number} is not a JSON object")
        response = StructuredAnnotationResponseV2.model_validate(cast(dict[str, Any], value))
        if canonical_json_bytes(response) != raw_line:
            raise ValueError(f"structured annotation line {line_number} is not canonical JSON")
        responses.append(response)
    return tuple(responses)


def write_structured_coding_procedure_v2(
    path: str | Path,
    artifact: StructuredCodingProcedureArtifactV2,
    ontology: OntologyReleaseArtifact,
) -> Path:
    errors = structured_procedure_errors(artifact, ontology)
    if errors:
        raise ValueError("invalid structured coding procedure: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_structured_coding_procedure_v2(
    path: str | Path,
    ontology: OntologyReleaseArtifact,
) -> StructuredCodingProcedureArtifactV2:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = StructuredCodingProcedureArtifactV2.model_validate(cast(dict[str, Any], raw))
    errors = structured_procedure_errors(artifact, ontology)
    if errors:
        raise ValueError("invalid structured coding procedure: " + "; ".join(errors))
    return artifact
