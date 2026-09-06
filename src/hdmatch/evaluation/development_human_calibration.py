"""Blind human first-pass calibration for development transfer coding.

The human coder sees only the preselected calibration units and frozen theory-neutral measurement
materials. This module validates that a first-pass output covers exactly those units, records a
public-safe hash receipt, and later compares the frozen human coding with automated consensus.
It never rewrites either side and defines no pass/fail threshold.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

from .development_annotation_pipeline import (
    DevelopmentConsensusArtifact,
    development_consensus_integrity_errors,
    load_development_episode_responses_jsonl,
    load_development_series_responses_jsonl,
    normalize_development_episode_responses_jsonl,
    normalize_development_series_responses_jsonl,
)
from .development_calibration_sampling import (
    DevelopmentCalibrationSamplingArtifact,
    development_calibration_integrity_errors,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from .development_episode_evidence import (
    DevelopmentEpisodeAnnotationResponse,
    development_episode_response_errors,
)
from .development_series_evidence import (
    DevelopmentSeriesAnnotationResponse,
    DevelopmentSeriesCodingTask,
    development_series_response_errors,
)
from .development_transfer_corpus import DevelopmentEpisodeCodingTask
from .neutral_measurement import OntologyReleaseArtifact
from .structured_annotation_v2 import StructuredCodingProcedureArtifactV2

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
HumanCalibrationEvidenceKind = Literal["episode", "series"]
HumanResponse = DevelopmentEpisodeAnnotationResponse | DevelopmentSeriesAnnotationResponse


class HumanCalibrationModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class DevelopmentHumanFirstPassPayload(HumanCalibrationModel):
    schema_version: Literal["life-patterns-development-human-first-pass-v1"] = (
        "life-patterns-development-human-first-pass-v1"
    )
    evidence_kind: HumanCalibrationEvidenceKind
    auditor_id: str = Field(min_length=1)
    calibration_manifest_id: str = Field(pattern=r"^LPCA-[0-9A-F]{20}$")
    calibration_manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    codebook_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_manual_sha256: str = Field(pattern=_SHA256_PATTERN)
    human_prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    selected_task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    raw_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    normalized_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    expected_unit_count: int = Field(ge=1)
    validated_unit_count: int = Field(ge=1)
    complete_selected_unit_coverage: Literal[True] = True
    independent_first_pass: Literal[True] = True
    llm_outputs_available_before_first_pass: Literal[False] = False
    automated_consensus_available_before_first_pass: Literal[False] = False
    target_theory_blind: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("human first-pass timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def counts_match(self) -> DevelopmentHumanFirstPassPayload:
        if self.expected_unit_count != self.validated_unit_count:
            raise ValueError("human first-pass validated unit count must equal expected count")
        return self


class DevelopmentHumanFirstPassArtifact(HumanCalibrationModel):
    schema_version: Literal["life-patterns-development-human-first-pass-artifact-v1"] = (
        "life-patterns-development-human-first-pass-artifact-v1"
    )
    artifact_id: str = Field(pattern=r"^LPHF-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentHumanFirstPassPayload


def _selected_episode_tasks(
    calibration: DevelopmentCalibrationSamplingArtifact,
    *,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
) -> tuple[DevelopmentEpisodeCodingTask, ...]:
    errors = development_calibration_integrity_errors(
        calibration,
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
    )
    if errors:
        raise ValueError("invalid development calibration manifest: " + "; ".join(errors))
    return human_episode_calibration_tasks(episode_tasks, calibration)


def _selected_series_tasks(
    calibration: DevelopmentCalibrationSamplingArtifact,
    *,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
) -> tuple[DevelopmentSeriesCodingTask, ...]:
    errors = development_calibration_integrity_errors(
        calibration,
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
    )
    if errors:
        raise ValueError("invalid development calibration manifest: " + "; ".join(errors))
    return human_series_calibration_tasks(episode_tasks, series_tasks, calibration)


def build_development_human_episode_first_pass(
    *,
    auditor_id: str,
    raw_output: bytes,
    normalized_output: bytes,
    calibration: DevelopmentCalibrationSamplingArtifact,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
    coding_manual_sha256: str,
    human_prompt_sha256: str,
    created_at_utc: datetime,
) -> DevelopmentHumanFirstPassArtifact:
    selected = _selected_episode_tasks(
        calibration,
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
    )
    if not selected:
        raise ValueError("human episode calibration selection is empty")
    recomputed = normalize_development_episode_responses_jsonl(raw_output)
    if recomputed != normalized_output:
        raise ValueError("human episode output is not deterministic normalization of raw output")
    responses = load_development_episode_responses_jsonl(normalized_output)
    task_by_id = {task.task_id: task for task in selected}
    expected = {
        (task.task_id, task.episode_id, observable_id)
        for task in selected
        for observable_id in task.observable_ids
    }
    actual = {(row.task_id, row.episode_id, row.observable_id) for row in responses}
    if len(actual) != len(responses):
        raise ValueError("human episode first pass repeats calibration units")
    if expected != actual:
        raise ValueError(
            f"human episode first pass does not exactly cover selected units; "
            f"missing={sorted(expected - actual)} extra={sorted(actual - expected)}"
        )
    for response in responses:
        task = task_by_id[response.task_id]
        errors = development_episode_response_errors(
            response,
            task=task,
            ontology=ontology,
            procedure=procedure,
        )
        if errors:
            raise ValueError(
                f"invalid human episode response {response.task_id}/{response.observable_id}: "
                + "; ".join(errors)
            )
    payload = DevelopmentHumanFirstPassPayload(
        evidence_kind="episode",
        auditor_id=auditor_id,
        calibration_manifest_id=calibration.manifest_id,
        calibration_manifest_sha256=calibration.manifest_sha256,
        corpus_id=selected[0].corpus_id,
        corpus_sha256=selected[0].corpus_sha256,
        codebook_sha256=procedure.payload.reconciled_codebook_sha256,
        coding_procedure_sha256=procedure.procedure_sha256,
        coding_manual_sha256=coding_manual_sha256,
        human_prompt_sha256=human_prompt_sha256,
        selected_task_set_sha256=sha256_json(selected),
        raw_output_sha256=_sha256_bytes(raw_output),
        normalized_output_sha256=_sha256_bytes(normalized_output),
        expected_unit_count=len(expected),
        validated_unit_count=len(responses),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentHumanFirstPassArtifact(
        artifact_id=f"LPHF-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def build_development_human_series_first_pass(
    *,
    auditor_id: str,
    raw_output: bytes,
    normalized_output: bytes,
    calibration: DevelopmentCalibrationSamplingArtifact,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
    coding_manual_sha256: str,
    human_prompt_sha256: str,
    created_at_utc: datetime,
) -> DevelopmentHumanFirstPassArtifact:
    selected = _selected_series_tasks(
        calibration,
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
    )
    if not selected:
        raise ValueError("human series calibration selection is empty")
    recomputed = normalize_development_series_responses_jsonl(raw_output)
    if recomputed != normalized_output:
        raise ValueError("human series output is not deterministic normalization of raw output")
    responses = load_development_series_responses_jsonl(normalized_output)
    task_by_id = {task.task_id: task for task in selected}
    expected = {
        (task.task_id, task.series_id, observable_id)
        for task in selected
        for observable_id in task.observable_ids
    }
    actual = {(row.task_id, row.series_id, row.observable_id) for row in responses}
    if len(actual) != len(responses):
        raise ValueError("human series first pass repeats calibration units")
    if expected != actual:
        raise ValueError(
            f"human series first pass does not exactly cover selected units; "
            f"missing={sorted(expected - actual)} extra={sorted(actual - expected)}"
        )
    for response in responses:
        task = task_by_id[response.task_id]
        errors = development_series_response_errors(
            response,
            task=task,
            ontology=ontology,
            procedure=procedure,
        )
        if errors:
            raise ValueError(
                f"invalid human series response {response.task_id}/{response.observable_id}: "
                + "; ".join(errors)
            )
    payload = DevelopmentHumanFirstPassPayload(
        evidence_kind="series",
        auditor_id=auditor_id,
        calibration_manifest_id=calibration.manifest_id,
        calibration_manifest_sha256=calibration.manifest_sha256,
        corpus_id=selected[0].corpus_id,
        corpus_sha256=selected[0].corpus_sha256,
        codebook_sha256=procedure.payload.reconciled_codebook_sha256,
        coding_procedure_sha256=procedure.procedure_sha256,
        coding_manual_sha256=coding_manual_sha256,
        human_prompt_sha256=human_prompt_sha256,
        selected_task_set_sha256=sha256_json(selected),
        raw_output_sha256=_sha256_bytes(raw_output),
        normalized_output_sha256=_sha256_bytes(normalized_output),
        expected_unit_count=len(expected),
        validated_unit_count=len(responses),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentHumanFirstPassArtifact(
        artifact_id=f"LPHF-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def development_human_first_pass_integrity_errors(
    artifact: DevelopmentHumanFirstPassArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPHF-{digest[:20].upper()}":
        return ("development human first-pass artifact failed content-address verification",)
    return ()


class DevelopmentHumanConsensusComparisonUnit(HumanCalibrationModel):
    task_id: str = Field(min_length=1)
    evidence_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    consensus_status: Literal["unanimous", "majority", "unresolved"]
    state_agreement: bool | None
    value_agreement_when_both_observed: bool | None


class DevelopmentHumanConsensusComparisonPayload(HumanCalibrationModel):
    schema_version: Literal["life-patterns-development-human-consensus-comparison-v1"] = (
        "life-patterns-development-human-consensus-comparison-v1"
    )
    evidence_kind: HumanCalibrationEvidenceKind
    human_first_pass_artifact_id: str = Field(pattern=r"^LPHF-[0-9A-F]{20}$")
    human_first_pass_artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    consensus_artifact_id: str = Field(pattern=r"^LPDCN-[0-9A-F]{20}$")
    consensus_artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    sampled_units: int = Field(ge=1)
    consensus_resolved_sample_units: int = Field(ge=0)
    unresolved_consensus_sample_units: int = Field(ge=0)
    state_agreement_units: int = Field(ge=0)
    both_observed_units: int = Field(ge=0)
    value_agreement_units: int = Field(ge=0)
    state_agreement_rate_on_resolved_consensus: float | None = Field(default=None, ge=0.0, le=1.0)
    value_agreement_rate_when_both_observed: float | None = Field(default=None, ge=0.0, le=1.0)
    units: tuple[DevelopmentHumanConsensusComparisonUnit, ...] = Field(min_length=1)
    no_pass_fail_threshold_applied: Literal[True] = True
    human_and_automated_outputs_preserved_separately: Literal[True] = True
    calibration_does_not_establish_construct_validity: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def comparison_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("human-consensus comparison timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def counts_are_coherent(self) -> DevelopmentHumanConsensusComparisonPayload:
        if self.sampled_units != len(self.units):
            raise ValueError("human-consensus comparison sampled unit count disagrees with rows")
        if (
            self.consensus_resolved_sample_units + self.unresolved_consensus_sample_units
            != self.sampled_units
        ):
            raise ValueError("human-consensus resolved/unresolved counts must sum to sampled units")
        if self.state_agreement_units > self.consensus_resolved_sample_units:
            raise ValueError("state agreement cannot exceed resolved consensus sample")
        if self.value_agreement_units > self.both_observed_units:
            raise ValueError("value agreement cannot exceed both-observed units")
        return self


class DevelopmentHumanConsensusComparisonArtifact(HumanCalibrationModel):
    schema_version: Literal[
        "life-patterns-development-human-consensus-comparison-artifact-v1"
    ] = "life-patterns-development-human-consensus-comparison-artifact-v1"
    artifact_id: str = Field(pattern=r"^LPHC-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentHumanConsensusComparisonPayload


def _response_unit_key(
    response: HumanResponse,
) -> tuple[str, str, str]:
    if isinstance(response, DevelopmentEpisodeAnnotationResponse):
        return response.task_id, response.episode_id, response.observable_id
    return response.task_id, response.series_id, response.observable_id


def _ordered_value_signature(response: HumanResponse) -> tuple[str, tuple[object, ...]] | None:
    if response.state != "observed" or response.value_relation is None:
        return None
    values: tuple[object, ...] = cast(tuple[object, ...], response.coded_values)
    if response.value_relation == "unordered_multiple":
        values = tuple(sorted(values, key=canonical_json_bytes))
    return response.value_relation, values


def build_development_human_consensus_comparison(
    *,
    human_first_pass: DevelopmentHumanFirstPassArtifact,
    human_normalized_output: bytes,
    consensus: DevelopmentConsensusArtifact,
    created_at_utc: datetime,
) -> DevelopmentHumanConsensusComparisonArtifact:
    errors = development_human_first_pass_integrity_errors(human_first_pass)
    if errors:
        raise ValueError("invalid human first-pass artifact: " + "; ".join(errors))
    consensus_errors = development_consensus_integrity_errors(consensus)
    if consensus_errors:
        raise ValueError("invalid development consensus artifact: " + "; ".join(consensus_errors))
    if _sha256_bytes(human_normalized_output) != human_first_pass.payload.normalized_output_sha256:
        raise ValueError("human comparison bytes do not bind first-pass artifact")
    if consensus.payload.evidence_kind != human_first_pass.payload.evidence_kind:
        raise ValueError("human first pass and automated consensus use different evidence kinds")
    if consensus.payload.corpus_sha256 != human_first_pass.payload.corpus_sha256:
        raise ValueError("human first pass and automated consensus do not bind same corpus")
    if consensus.payload.codebook_sha256 != human_first_pass.payload.codebook_sha256:
        raise ValueError("human first pass and automated consensus do not bind same codebook")
    if (
        consensus.payload.coding_procedure_sha256
        != human_first_pass.payload.coding_procedure_sha256
    ):
        raise ValueError("human first pass and automated consensus do not bind same procedure")

    if human_first_pass.payload.evidence_kind == "episode":
        responses: tuple[HumanResponse, ...] = load_development_episode_responses_jsonl(
            human_normalized_output
        )
    else:
        responses = load_development_series_responses_jsonl(human_normalized_output)
    human_by_unit = {_response_unit_key(response): response for response in responses}
    consensus_by_unit = {
        (unit.task_id, unit.evidence_id, unit.observable_id): unit for unit in consensus.payload.units
    }
    if not set(human_by_unit).issubset(consensus_by_unit):
        raise ValueError("automated consensus does not cover every sampled human unit")

    rows: list[DevelopmentHumanConsensusComparisonUnit] = []
    resolved = 0
    unresolved = 0
    state_agree = 0
    both_observed = 0
    value_agree = 0
    for key in sorted(human_by_unit):
        human = human_by_unit[key]
        auto_unit = consensus_by_unit[key]
        state_match: bool | None
        value_match: bool | None = None
        if auto_unit.status == "unresolved" or auto_unit.consensus_response is None:
            unresolved += 1
            state_match = None
        else:
            resolved += 1
            automated = auto_unit.consensus_response
            state_match = human.state == automated.state
            if state_match:
                state_agree += 1
            if human.state == "observed" and automated.state == "observed":
                both_observed += 1
                value_match = _ordered_value_signature(human) == _ordered_value_signature(automated)
                if value_match:
                    value_agree += 1
        rows.append(
            DevelopmentHumanConsensusComparisonUnit(
                task_id=key[0],
                evidence_id=key[1],
                observable_id=key[2],
                consensus_status=auto_unit.status,
                state_agreement=state_match,
                value_agreement_when_both_observed=value_match,
            )
        )
    payload = DevelopmentHumanConsensusComparisonPayload(
        evidence_kind=human_first_pass.payload.evidence_kind,
        human_first_pass_artifact_id=human_first_pass.artifact_id,
        human_first_pass_artifact_sha256=human_first_pass.artifact_sha256,
        consensus_artifact_id=consensus.artifact_id,
        consensus_artifact_sha256=consensus.artifact_sha256,
        sampled_units=len(rows),
        consensus_resolved_sample_units=resolved,
        unresolved_consensus_sample_units=unresolved,
        state_agreement_units=state_agree,
        both_observed_units=both_observed,
        value_agreement_units=value_agree,
        state_agreement_rate_on_resolved_consensus=(state_agree / resolved if resolved else None),
        value_agreement_rate_when_both_observed=(
            value_agree / both_observed if both_observed else None
        ),
        units=tuple(rows),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentHumanConsensusComparisonArtifact(
        artifact_id=f"LPHC-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )
