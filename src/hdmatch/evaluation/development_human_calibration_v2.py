"""Validate recurrence-corrected blind human first-pass development coding.

The v2 validator binds the first pass to the recurrence-corrected package/policy while reusing the
pre-label calibration selection. It validates exact coverage and response semantics but does not
by itself prove the human's real-world independence/exposure chronology; the completed auditor
attestation and controlled handoff remain necessary evidence.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

from .development_annotation_pipeline import (
    load_development_episode_responses_jsonl,
    normalize_development_episode_responses_jsonl,
)
from .development_calibration_sampling import (
    DevelopmentCalibrationSamplingArtifact,
    development_calibration_integrity_errors,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
)
from .development_coding_package_v2 import DevelopmentCodingPackageArtifactV2
from .development_episode_evidence import development_episode_response_errors
from .development_series_evidence import DevelopmentSeriesCodingTask
from .development_series_evidence_v2 import (
    DevelopmentSeriesAnnotationResponseV2,
    development_series_response_errors_v2,
)
from .development_transfer_corpus import DevelopmentEpisodeCodingTask

HumanCalibrationEvidenceKindV2 = Literal["episode", "series"]


class HumanCalibrationV2Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _decode_json_object_stream(data: bytes) -> tuple[dict[str, Any], ...]:
    import json

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("raw human series v2 output is not UTF-8") from exc
    decoder = json.JSONDecoder()
    position = 0
    values: list[dict[str, Any]] = []
    while position < len(text):
        while position < len(text) and text[position].isspace():
            position += 1
        if position >= len(text):
            break
        try:
            value, end = decoder.raw_decode(text, position)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"raw human series v2 output contains invalid JSON near character {position}"
            ) from exc
        if not isinstance(value, dict):
            raise ValueError("raw human series v2 entries must be JSON objects")
        values.append(cast(dict[str, Any], value))
        position = end
    return tuple(values)


def normalize_development_series_responses_v2_jsonl(data: bytes) -> bytes:
    rows: list[DevelopmentSeriesAnnotationResponseV2] = []
    units: set[tuple[str, str, str]] = set()
    for object_number, value in enumerate(_decode_json_object_stream(data), start=1):
        response = DevelopmentSeriesAnnotationResponseV2.model_validate(value)
        key = (response.task_id, response.series_id, response.observable_id)
        if key in units:
            raise ValueError(
                "raw human series v2 output repeats task/series/observable unit "
                f"at object {object_number}"
            )
        units.add(key)
        rows.append(response)
    return b"\n".join(canonical_json_bytes(row) for row in rows) + (b"\n" if rows else b"")


def load_development_series_responses_v2_jsonl(
    data: bytes,
) -> tuple[DevelopmentSeriesAnnotationResponseV2, ...]:
    return tuple(
        DevelopmentSeriesAnnotationResponseV2.model_validate(value)
        for value in _decode_json_object_stream(data)
    )


class DevelopmentHumanFirstPassPayloadV2(HumanCalibrationV2Model):
    schema_version: Literal["life-patterns-development-human-first-pass-v2"] = (
        "life-patterns-development-human-first-pass-v2"
    )
    evidence_kind: HumanCalibrationEvidenceKindV2
    auditor_id: str = Field(min_length=1)
    package_id: str = Field(pattern=r"^LPKG2-[0-9A-F]{20}$")
    package_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    calibration_manifest_id: str = Field(pattern=r"^LPCA-[0-9A-F]{20}$")
    calibration_manifest_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    codebook_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coding_procedure_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coding_manual_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    recurrence_policy_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    human_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    selected_task_set_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    raw_output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    normalized_output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    expected_unit_count: int = Field(ge=1)
    validated_unit_count: int = Field(ge=1)
    complete_selected_unit_coverage: Literal[True] = True
    calibration_selection_reused_without_resampling: Literal[True] = True
    confirming_episodes_counted_as_frequency_evidence: Literal[False] = False
    independent_first_pass: Literal[True] = True
    human_facing_offline_ui_used: Literal[True] = True
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
            raise ValueError("human first-pass v2 timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def counts_match(self) -> DevelopmentHumanFirstPassPayloadV2:
        if self.expected_unit_count != self.validated_unit_count:
            raise ValueError("human first-pass v2 validated count must equal expected count")
        return self


class DevelopmentHumanFirstPassArtifactV2(HumanCalibrationV2Model):
    schema_version: Literal["life-patterns-development-human-first-pass-artifact-v2"] = (
        "life-patterns-development-human-first-pass-artifact-v2"
    )
    artifact_id: str = Field(pattern=r"^LPHF2-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    payload: DevelopmentHumanFirstPassPayloadV2


def _check_selection(
    calibration: DevelopmentCalibrationSamplingArtifact,
    *,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
) -> None:
    errors = development_calibration_integrity_errors(
        calibration,
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
    )
    if errors:
        raise ValueError("invalid reused v2 calibration selection: " + "; ".join(errors))


def _base_payload_fields(
    *,
    auditor_id: str,
    package: DevelopmentCodingPackageArtifactV2,
    calibration: DevelopmentCalibrationSamplingArtifact,
    raw_output: bytes,
    normalized_output: bytes,
    selected_task_set_sha256: str,
    expected_unit_count: int,
    validated_unit_count: int,
    created_at_utc: datetime,
) -> dict[str, Any]:
    bound = package.payload
    return {
        "auditor_id": auditor_id,
        "package_id": package.package_id,
        "package_sha256": package.package_sha256,
        "calibration_manifest_id": calibration.manifest_id,
        "calibration_manifest_sha256": calibration.manifest_sha256,
        "corpus_id": bound.corpus_id,
        "corpus_sha256": bound.corpus_sha256,
        "codebook_sha256": bound.resolved_view_sha256,
        "coding_procedure_sha256": bound.procedure_sha256,
        "coding_manual_sha256": bound.coding_manual_sha256,
        "recurrence_policy_sha256": bound.recurrence_policy_sha256,
        "human_prompt_sha256": bound.human_calibration_prompt_sha256,
        "selected_task_set_sha256": selected_task_set_sha256,
        "raw_output_sha256": _sha256_bytes(raw_output),
        "normalized_output_sha256": _sha256_bytes(normalized_output),
        "expected_unit_count": expected_unit_count,
        "validated_unit_count": validated_unit_count,
        "created_at_utc": created_at_utc,
    }


def build_development_human_episode_first_pass_v2(
    *,
    auditor_id: str,
    raw_output: bytes,
    normalized_output: bytes,
    package: DevelopmentCodingPackageArtifactV2,
    calibration: DevelopmentCalibrationSamplingArtifact,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
    ontology,
    procedure,
    created_at_utc: datetime,
) -> DevelopmentHumanFirstPassArtifactV2:
    _check_selection(calibration, episode_tasks=episode_tasks, series_tasks=series_tasks)
    selected = human_episode_calibration_tasks(episode_tasks, calibration)
    if not selected:
        raise ValueError("human episode calibration v2 selection is empty")
    recomputed = normalize_development_episode_responses_jsonl(raw_output)
    if recomputed != normalized_output:
        raise ValueError("human episode v2 output is not deterministic normalization of raw output")
    responses = load_development_episode_responses_jsonl(normalized_output)
    task_by_id = {task.task_id: task for task in selected}
    expected = {
        (task.task_id, task.episode_id, observable_id)
        for task in selected
        for observable_id in task.observable_ids
    }
    actual = {(row.task_id, row.episode_id, row.observable_id) for row in responses}
    if len(actual) != len(responses) or actual != expected:
        raise ValueError("human episode v2 first pass does not exactly cover selected units")
    for response in responses:
        errors = development_episode_response_errors(
            response,
            task=task_by_id[response.task_id],
            ontology=ontology,
            procedure=procedure,
        )
        if errors:
            raise ValueError(
                f"invalid human episode v2 response {response.task_id}/{response.observable_id}: "
                + "; ".join(errors)
            )
    payload = DevelopmentHumanFirstPassPayloadV2(
        evidence_kind="episode",
        **_base_payload_fields(
            auditor_id=auditor_id,
            package=package,
            calibration=calibration,
            raw_output=raw_output,
            normalized_output=normalized_output,
            selected_task_set_sha256=sha256_json(selected),
            expected_unit_count=len(expected),
            validated_unit_count=len(responses),
            created_at_utc=created_at_utc,
        ),
    )
    digest = sha256_json(payload)
    return DevelopmentHumanFirstPassArtifactV2(
        artifact_id=f"LPHF2-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def build_development_human_series_first_pass_v2(
    *,
    auditor_id: str,
    raw_output: bytes,
    normalized_output: bytes,
    package: DevelopmentCodingPackageArtifactV2,
    calibration: DevelopmentCalibrationSamplingArtifact,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
    ontology,
    procedure,
    created_at_utc: datetime,
) -> DevelopmentHumanFirstPassArtifactV2:
    _check_selection(calibration, episode_tasks=episode_tasks, series_tasks=series_tasks)
    selected = human_series_calibration_tasks(episode_tasks, series_tasks, calibration)
    if not selected:
        raise ValueError("human series calibration v2 selection is empty")
    recomputed = normalize_development_series_responses_v2_jsonl(raw_output)
    if recomputed != normalized_output:
        raise ValueError("human series v2 output is not deterministic normalization of raw output")
    responses = load_development_series_responses_v2_jsonl(normalized_output)
    task_by_id = {task.task_id: task for task in selected}
    expected = {
        (task.task_id, task.series_id, observable_id)
        for task in selected
        for observable_id in task.observable_ids
    }
    actual = {(row.task_id, row.series_id, row.observable_id) for row in responses}
    if len(actual) != len(responses) or actual != expected:
        raise ValueError("human series v2 first pass does not exactly cover selected units")
    for response in responses:
        errors = development_series_response_errors_v2(
            response,
            task=task_by_id[response.task_id],
            ontology=ontology,
            procedure=procedure,
        )
        if errors:
            raise ValueError(
                f"invalid human series v2 response {response.task_id}/{response.observable_id}: "
                + "; ".join(errors)
            )
    payload = DevelopmentHumanFirstPassPayloadV2(
        evidence_kind="series",
        **_base_payload_fields(
            auditor_id=auditor_id,
            package=package,
            calibration=calibration,
            raw_output=raw_output,
            normalized_output=normalized_output,
            selected_task_set_sha256=sha256_json(selected),
            expected_unit_count=len(expected),
            validated_unit_count=len(responses),
            created_at_utc=created_at_utc,
        ),
    )
    digest = sha256_json(payload)
    return DevelopmentHumanFirstPassArtifactV2(
        artifact_id=f"LPHF2-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def development_human_first_pass_v2_integrity_errors(
    artifact: DevelopmentHumanFirstPassArtifactV2,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPHF2-{digest[:20].upper()}":
        return ("development human first-pass v2 artifact failed content-address verification",)
    return ()
