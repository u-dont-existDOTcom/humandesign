"""Fail-closed validation wrapper for complete automated StructuredAnnotation V2 passes."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from hdmatch.experiments.canonical import canonical_json_bytes, load_json_bytes, sha256_json, write_new_bytes

from .automated_annotation_calibration import AutomatedCodingPassReceipt
from .neutral_measurement import FreezeEvidenceIndex, OntologyReleaseArtifact
from .structured_annotation_normalization import (
    normalize_structured_annotation_responses_jsonl_v2,
)
from .structured_annotation_v2 import (
    StructuredAnnotationTaskV2,
    StructuredCodingProcedureArtifactV2,
    load_structured_annotation_responses_jsonl_v2,
    structured_annotation_response_errors,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class ValidatedPassModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class ValidatedStructuredAutomatedPassPayloadV2(ValidatedPassModel):
    schema_version: Literal["life-patterns-validated-structured-automated-pass-v2"] = (
        "life-patterns-validated-structured-automated-pass-v2"
    )
    automated_pass: AutomatedCodingPassReceipt
    task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    raw_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    normalized_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    normalization_implementation_sha256: str = Field(pattern=_SHA256_PATTERN)
    expected_unit_count: int = Field(ge=1)
    validated_unit_count: int = Field(ge=1)
    complete_unit_coverage: Literal[True] = True
    all_responses_structurally_valid: Literal[True] = True
    normalization_is_format_only: Literal[True] = True
    target_model_information_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("validated automated pass timestamp must be timezone-aware")
        return value.astimezone(UTC)


class ValidatedStructuredAutomatedPassArtifactV2(ValidatedPassModel):
    schema_version: Literal["life-patterns-validated-structured-automated-pass-artifact-v2"] = (
        "life-patterns-validated-structured-automated-pass-artifact-v2"
    )
    artifact_id: str = Field(pattern=r"^LPVP-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: ValidatedStructuredAutomatedPassPayloadV2


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _expected_units(
    tasks: tuple[StructuredAnnotationTaskV2, ...],
) -> set[tuple[str, str, str]]:
    return {
        (task.task_id, task.episode_id, observable_id)
        for task in tasks
        for observable_id in task.observable_ids
    }


def build_validated_structured_automated_pass_v2(
    *,
    raw_output: bytes,
    normalized_output: bytes,
    automated_pass: AutomatedCodingPassReceipt,
    tasks: tuple[StructuredAnnotationTaskV2, ...],
    evidence: FreezeEvidenceIndex,
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
    expected_corpus_sha256: str,
    normalization_implementation_sha256: str,
    created_at_utc: datetime,
) -> ValidatedStructuredAutomatedPassArtifactV2:
    if automated_pass.corpus_sha256 != expected_corpus_sha256:
        raise ValueError("automated pass does not bind expected development corpus")
    if automated_pass.codebook_sha256 != procedure.payload.reconciled_codebook_sha256:
        raise ValueError("automated pass does not bind structured procedure codebook")
    if automated_pass.coding_procedure_sha256 != procedure.procedure_sha256:
        raise ValueError("automated pass does not bind structured coding procedure")

    recomputed_normalized = normalize_structured_annotation_responses_jsonl_v2(raw_output)
    if recomputed_normalized != normalized_output:
        raise ValueError("normalized output is not deterministic normalization of preserved raw output")
    normalized_sha256 = _sha256_bytes(normalized_output)
    if automated_pass.output_sha256 != normalized_sha256:
        raise ValueError("automated pass output hash does not bind canonical normalized output")

    task_set_sha256 = sha256_json(tasks)
    task_by_id = {task.task_id: task for task in tasks}
    if len(task_by_id) != len(tasks):
        raise ValueError("structured task set contains duplicate task identities")

    responses = load_structured_annotation_responses_jsonl_v2(normalized_output)
    expected_units = _expected_units(tasks)
    actual_units = {
        (response.task_id, response.episode_id, response.observable_id)
        for response in responses
    }
    if len(actual_units) != len(responses):
        raise ValueError("normalized automated pass repeats structured annotation units")
    missing = sorted(expected_units - actual_units)
    extra = sorted(actual_units - expected_units)
    if missing:
        raise ValueError(f"automated pass is missing frozen annotation units: {missing}")
    if extra:
        raise ValueError(f"automated pass contains units outside frozen task set: {extra}")

    for response in responses:
        task = task_by_id[response.task_id]
        errors = structured_annotation_response_errors(
            response,
            task=task,
            evidence=evidence,
            ontology=ontology,
            procedure=procedure,
        )
        if errors:
            raise ValueError(
                f"invalid structured automated response {response.task_id}/{response.observable_id}: "
                + "; ".join(errors)
            )

    payload = ValidatedStructuredAutomatedPassPayloadV2(
        automated_pass=automated_pass,
        task_set_sha256=task_set_sha256,
        raw_output_sha256=_sha256_bytes(raw_output),
        normalized_output_sha256=normalized_sha256,
        normalization_implementation_sha256=normalization_implementation_sha256,
        expected_unit_count=len(expected_units),
        validated_unit_count=len(responses),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return ValidatedStructuredAutomatedPassArtifactV2(
        artifact_id=f"LPVP-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def validated_structured_automated_pass_integrity_errors(
    artifact: ValidatedStructuredAutomatedPassArtifactV2,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPVP-{digest[:20].upper()}":
        return ("validated structured automated pass failed content-address verification",)
    if artifact.payload.expected_unit_count != artifact.payload.validated_unit_count:
        return ("validated structured automated pass stored inconsistent unit counts",)
    return ()


def write_validated_structured_automated_pass_v2(
    path: str | Path,
    artifact: ValidatedStructuredAutomatedPassArtifactV2,
) -> Path:
    errors = validated_structured_automated_pass_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid validated structured automated pass: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_validated_structured_automated_pass_v2(
    path: str | Path,
) -> ValidatedStructuredAutomatedPassArtifactV2:
    raw = load_json_bytes(path, require_canonical=True)
    artifact = ValidatedStructuredAutomatedPassArtifactV2.model_validate(raw)
    errors = validated_structured_automated_pass_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid validated structured automated pass: " + "; ".join(errors))
    return artifact
