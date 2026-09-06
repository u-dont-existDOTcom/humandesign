"""Fail-closed normalization, pass validation, and consensus for development transfer coding.

Episode and repeated-series evidence remain separate unit universes.  Both use the same resolved
Life Patterns ontology/procedure, but each has its own transport prompt and response schema.  Raw
model bytes are preserved and hashed; normalization is format-only; at least three isolated
passes are required for deterministic strict-majority consensus.

This module does not execute a model and does not promote development transfer evidence to a
canonical behavioral freeze or validation instrument.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

from .automated_annotation_calibration import AutomatedCodingPassReceipt
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
DevelopmentEvidenceKind = Literal["episode", "series"]
DevelopmentConsensusStatus = Literal["unanimous", "majority", "unresolved"]
DevelopmentResponse = DevelopmentEpisodeAnnotationResponse | DevelopmentSeriesAnnotationResponse
DevelopmentTask = DevelopmentEpisodeCodingTask | DevelopmentSeriesCodingTask


class DevelopmentPipelineModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _decode_json_object_stream(data: bytes) -> tuple[dict[str, Any], ...]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("raw development annotation output is not UTF-8") from exc
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
                f"raw development annotation contains invalid JSON near character {position}"
            ) from exc
        if not isinstance(value, dict):
            raise ValueError("raw development annotation entries must be JSON objects")
        values.append(cast(dict[str, Any], value))
        position = end
    return tuple(values)


def normalize_development_episode_responses_jsonl(data: bytes) -> bytes:
    rows: list[DevelopmentEpisodeAnnotationResponse] = []
    units: set[tuple[str, str, str]] = set()
    for object_number, value in enumerate(_decode_json_object_stream(data), start=1):
        response = DevelopmentEpisodeAnnotationResponse.model_validate(value)
        key = (response.task_id, response.episode_id, response.observable_id)
        if key in units:
            raise ValueError(
                "raw development episode output repeats task/episode/observable unit "
                f"at object {object_number}"
            )
        units.add(key)
        rows.append(response)
    return b"\n".join(canonical_json_bytes(row) for row in rows) + (b"\n" if rows else b"")


def normalize_development_series_responses_jsonl(data: bytes) -> bytes:
    rows: list[DevelopmentSeriesAnnotationResponse] = []
    units: set[tuple[str, str, str]] = set()
    for object_number, value in enumerate(_decode_json_object_stream(data), start=1):
        response = DevelopmentSeriesAnnotationResponse.model_validate(value)
        key = (response.task_id, response.series_id, response.observable_id)
        if key in units:
            raise ValueError(
                "raw development series output repeats task/series/observable unit "
                f"at object {object_number}"
            )
        units.add(key)
        rows.append(response)
    return b"\n".join(canonical_json_bytes(row) for row in rows) + (b"\n" if rows else b"")


def load_development_episode_responses_jsonl(
    data: bytes,
) -> tuple[DevelopmentEpisodeAnnotationResponse, ...]:
    return tuple(
        DevelopmentEpisodeAnnotationResponse.model_validate(value)
        for value in _decode_json_object_stream(data)
    )


def load_development_series_responses_jsonl(
    data: bytes,
) -> tuple[DevelopmentSeriesAnnotationResponse, ...]:
    return tuple(
        DevelopmentSeriesAnnotationResponse.model_validate(value)
        for value in _decode_json_object_stream(data)
    )


class ValidatedDevelopmentAutomatedPassPayload(DevelopmentPipelineModel):
    schema_version: Literal["life-patterns-validated-development-automated-pass-v1"] = (
        "life-patterns-validated-development-automated-pass-v1"
    )
    evidence_kind: DevelopmentEvidenceKind
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
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    target_model_information_available: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("validated development pass timestamp must be timezone-aware")
        return value.astimezone(UTC)


class ValidatedDevelopmentAutomatedPassArtifact(DevelopmentPipelineModel):
    schema_version: Literal["life-patterns-validated-development-automated-pass-artifact-v1"] = (
        "life-patterns-validated-development-automated-pass-artifact-v1"
    )
    artifact_id: str = Field(pattern=r"^LPDV-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: ValidatedDevelopmentAutomatedPassPayload


def _validate_receipt_binding(
    automated_pass: AutomatedCodingPassReceipt,
    *,
    corpus_sha256: str,
    procedure: StructuredCodingProcedureArtifactV2,
    expected_prompt_sha256: str,
    normalized_output: bytes,
) -> None:
    if automated_pass.corpus_sha256 != corpus_sha256:
        raise ValueError("development automated pass does not bind expected corpus")
    if automated_pass.codebook_sha256 != procedure.payload.reconciled_codebook_sha256:
        raise ValueError("development automated pass does not bind resolved codebook")
    if automated_pass.coding_procedure_sha256 != procedure.procedure_sha256:
        raise ValueError("development automated pass does not bind structured procedure")
    if automated_pass.prompt_sha256 != expected_prompt_sha256:
        raise ValueError("development automated pass does not bind expected transport prompt")
    if automated_pass.output_sha256 != _sha256_bytes(normalized_output):
        raise ValueError("development automated pass output hash does not bind normalized output")


def _expected_episode_units(
    tasks: tuple[DevelopmentEpisodeCodingTask, ...],
) -> set[tuple[str, str, str]]:
    return {
        (task.task_id, task.episode_id, observable_id)
        for task in tasks
        for observable_id in task.observable_ids
    }


def _expected_series_units(
    tasks: tuple[DevelopmentSeriesCodingTask, ...],
) -> set[tuple[str, str, str]]:
    return {
        (task.task_id, task.series_id, observable_id)
        for task in tasks
        for observable_id in task.observable_ids
    }


def build_validated_development_episode_pass(
    *,
    raw_output: bytes,
    normalized_output: bytes,
    automated_pass: AutomatedCodingPassReceipt,
    tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
    expected_prompt_sha256: str,
    normalization_implementation_sha256: str,
    created_at_utc: datetime,
) -> ValidatedDevelopmentAutomatedPassArtifact:
    if not tasks:
        raise ValueError("development episode pass requires nonempty task set")
    corpus_ids = {task.corpus_id for task in tasks}
    corpus_hashes = {task.corpus_sha256 for task in tasks}
    if len(corpus_ids) != 1 or len(corpus_hashes) != 1:
        raise ValueError("development episode tasks do not bind one exact corpus")
    recomputed = normalize_development_episode_responses_jsonl(raw_output)
    if recomputed != normalized_output:
        raise ValueError("episode normalized output is not deterministic normalization of raw output")
    corpus_sha256 = next(iter(corpus_hashes))
    _validate_receipt_binding(
        automated_pass,
        corpus_sha256=corpus_sha256,
        procedure=procedure,
        expected_prompt_sha256=expected_prompt_sha256,
        normalized_output=normalized_output,
    )
    task_by_id = {task.task_id: task for task in tasks}
    if len(task_by_id) != len(tasks):
        raise ValueError("development episode task set repeats task identity")
    responses = load_development_episode_responses_jsonl(normalized_output)
    expected = _expected_episode_units(tasks)
    actual = {(row.task_id, row.episode_id, row.observable_id) for row in responses}
    if len(actual) != len(responses):
        raise ValueError("normalized development episode pass repeats annotation units")
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise ValueError(f"development episode pass is missing units: {missing}")
    if extra:
        raise ValueError(f"development episode pass contains extra units: {extra}")
    for response in responses:
        task = task_by_id.get(response.task_id)
        if task is None:
            raise ValueError("development episode response references unknown task")
        errors = development_episode_response_errors(
            response,
            task=task,
            ontology=ontology,
            procedure=procedure,
        )
        if errors:
            raise ValueError(
                f"invalid development episode response {response.task_id}/{response.observable_id}: "
                + "; ".join(errors)
            )
    payload = ValidatedDevelopmentAutomatedPassPayload(
        evidence_kind="episode",
        automated_pass=automated_pass,
        task_set_sha256=sha256_json(tasks),
        raw_output_sha256=_sha256_bytes(raw_output),
        normalized_output_sha256=_sha256_bytes(normalized_output),
        normalization_implementation_sha256=normalization_implementation_sha256,
        expected_unit_count=len(expected),
        validated_unit_count=len(responses),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return ValidatedDevelopmentAutomatedPassArtifact(
        artifact_id=f"LPDV-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def build_validated_development_series_pass(
    *,
    raw_output: bytes,
    normalized_output: bytes,
    automated_pass: AutomatedCodingPassReceipt,
    tasks: tuple[DevelopmentSeriesCodingTask, ...],
    ontology: OntologyReleaseArtifact,
    procedure: StructuredCodingProcedureArtifactV2,
    expected_prompt_sha256: str,
    normalization_implementation_sha256: str,
    created_at_utc: datetime,
) -> ValidatedDevelopmentAutomatedPassArtifact:
    if not tasks:
        raise ValueError("development series pass requires nonempty task set")
    corpus_ids = {task.corpus_id for task in tasks}
    corpus_hashes = {task.corpus_sha256 for task in tasks}
    if len(corpus_ids) != 1 or len(corpus_hashes) != 1:
        raise ValueError("development series tasks do not bind one exact corpus")
    recomputed = normalize_development_series_responses_jsonl(raw_output)
    if recomputed != normalized_output:
        raise ValueError("series normalized output is not deterministic normalization of raw output")
    corpus_sha256 = next(iter(corpus_hashes))
    _validate_receipt_binding(
        automated_pass,
        corpus_sha256=corpus_sha256,
        procedure=procedure,
        expected_prompt_sha256=expected_prompt_sha256,
        normalized_output=normalized_output,
    )
    task_by_id = {task.task_id: task for task in tasks}
    if len(task_by_id) != len(tasks):
        raise ValueError("development series task set repeats task identity")
    responses = load_development_series_responses_jsonl(normalized_output)
    expected = _expected_series_units(tasks)
    actual = {(row.task_id, row.series_id, row.observable_id) for row in responses}
    if len(actual) != len(responses):
        raise ValueError("normalized development series pass repeats annotation units")
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise ValueError(f"development series pass is missing units: {missing}")
    if extra:
        raise ValueError(f"development series pass contains extra units: {extra}")
    for response in responses:
        task = task_by_id.get(response.task_id)
        if task is None:
            raise ValueError("development series response references unknown task")
        errors = development_series_response_errors(
            response,
            task=task,
            ontology=ontology,
            procedure=procedure,
        )
        if errors:
            raise ValueError(
                f"invalid development series response {response.task_id}/{response.observable_id}: "
                + "; ".join(errors)
            )
    payload = ValidatedDevelopmentAutomatedPassPayload(
        evidence_kind="series",
        automated_pass=automated_pass,
        task_set_sha256=sha256_json(tasks),
        raw_output_sha256=_sha256_bytes(raw_output),
        normalized_output_sha256=_sha256_bytes(normalized_output),
        normalization_implementation_sha256=normalization_implementation_sha256,
        expected_unit_count=len(expected),
        validated_unit_count=len(responses),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return ValidatedDevelopmentAutomatedPassArtifact(
        artifact_id=f"LPDV-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def validated_development_pass_integrity_errors(
    artifact: ValidatedDevelopmentAutomatedPassArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    errors: list[str] = []
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPDV-{digest[:20].upper()}":
        errors.append("validated development pass failed content-address verification")
    if artifact.payload.expected_unit_count != artifact.payload.validated_unit_count:
        errors.append("validated development pass stores inconsistent unit counts")
    return tuple(errors)


class DevelopmentPassUnitConsensusTrace(DevelopmentPipelineModel):
    pass_id: str = Field(min_length=1)
    response_sha256: str = Field(pattern=_SHA256_PATTERN)
    semantic_sha256: str = Field(pattern=_SHA256_PATTERN)


class DevelopmentConsensusUnit(DevelopmentPipelineModel):
    evidence_kind: DevelopmentEvidenceKind
    task_id: str = Field(min_length=1)
    evidence_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    status: DevelopmentConsensusStatus
    agreeing_pass_ids: tuple[str, ...]
    dissenting_pass_ids: tuple[str, ...]
    consensus_response: DevelopmentResponse | None = None
    pass_trace: tuple[DevelopmentPassUnitConsensusTrace, ...] = Field(min_length=3)

    @model_validator(mode="after")
    def resolution_matches_status(self) -> DevelopmentConsensusUnit:
        if self.status == "unresolved" and self.consensus_response is not None:
            raise ValueError("unresolved development consensus cannot carry a response")
        if self.status != "unresolved" and self.consensus_response is None:
            raise ValueError("resolved development consensus requires a response")
        return self


class DevelopmentConsensusPayload(DevelopmentPipelineModel):
    schema_version: Literal["life-patterns-development-consensus-v1"] = (
        "life-patterns-development-consensus-v1"
    )
    evidence_kind: DevelopmentEvidenceKind
    validated_pass_artifact_sha256: tuple[str, ...] = Field(min_length=3)
    pass_ids: tuple[str, ...] = Field(min_length=3)
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    codebook_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    consensus_rule_id: Literal["development-semantic-strict-majority-v1"] = (
        "development-semantic-strict-majority-v1"
    )
    units: tuple[DevelopmentConsensusUnit, ...] = Field(min_length=1)
    total_units: int = Field(ge=1)
    unanimous_units: int = Field(ge=0)
    majority_units: int = Field(ge=0)
    unresolved_units: int = Field(ge=0)
    episode_and_series_consensus_are_never_pooled: Literal[True] = True
    self_consistency_does_not_establish_correctness: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @field_validator("pass_ids")
    @classmethod
    def pass_ids_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("development consensus contains duplicate pass IDs")
        return value

    @model_validator(mode="after")
    def counts_are_coherent(self) -> DevelopmentConsensusPayload:
        if self.total_units != len(self.units):
            raise ValueError("development consensus total disagrees with unit rows")
        if self.unanimous_units + self.majority_units + self.unresolved_units != self.total_units:
            raise ValueError("development consensus status counts must sum to total")
        if any(row.evidence_kind != self.evidence_kind for row in self.units):
            raise ValueError("development consensus pooled incompatible evidence kinds")
        return self


class DevelopmentConsensusArtifact(DevelopmentPipelineModel):
    schema_version: Literal["life-patterns-development-consensus-artifact-v1"] = (
        "life-patterns-development-consensus-artifact-v1"
    )
    artifact_id: str = Field(pattern=r"^LPDCN-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentConsensusPayload


def _sorted_scalar_values(values: tuple[object, ...]) -> tuple[object, ...]:
    return tuple(sorted(values, key=lambda value: canonical_json_bytes(value)))


def semantic_development_response(response: DevelopmentResponse) -> DevelopmentResponse:
    coded_values = response.coded_values
    if response.value_relation == "unordered_multiple":
        coded_values = cast(Any, _sorted_scalar_values(coded_values))
    if isinstance(response, DevelopmentEpisodeAnnotationResponse):
        return response.model_copy(
            update={
                "coded_values": coded_values,
                "supporting_source_segment_ids": tuple(
                    sorted(set(response.supporting_source_segment_ids))
                ),
                "counterevidence_source_segment_ids": tuple(
                    sorted(set(response.counterevidence_source_segment_ids))
                ),
                "context_qualifiers": tuple(sorted(set(response.context_qualifiers))),
                "missingness_flags": tuple(sorted(set(response.missingness_flags))),
                "influence_source_segment_ids": tuple(
                    sorted(set(response.influence_source_segment_ids))
                ),
                "annotation_note": None,
            }
        )
    return response.model_copy(
        update={
            "coded_values": coded_values,
            "supporting_source_segment_ids": tuple(
                sorted(set(response.supporting_source_segment_ids))
            ),
            "context_qualifiers": tuple(sorted(set(response.context_qualifiers))),
            "missingness_flags": tuple(sorted(set(response.missingness_flags))),
            "annotation_note": None,
        }
    )


def _responses_by_unit(
    evidence_kind: DevelopmentEvidenceKind,
    data: bytes,
) -> dict[tuple[str, str, str], DevelopmentResponse]:
    if evidence_kind == "episode":
        rows: tuple[DevelopmentResponse, ...] = load_development_episode_responses_jsonl(data)
        output = {
            (row.task_id, cast(DevelopmentEpisodeAnnotationResponse, row).episode_id, row.observable_id): row
            for row in rows
        }
    else:
        rows = load_development_series_responses_jsonl(data)
        output = {
            (row.task_id, cast(DevelopmentSeriesAnnotationResponse, row).series_id, row.observable_id): row
            for row in rows
        }
    if len(output) != len(rows):
        raise ValueError("development consensus input repeats annotation units")
    return output


def build_development_consensus(
    passes: tuple[tuple[ValidatedDevelopmentAutomatedPassArtifact, bytes], ...],
) -> DevelopmentConsensusArtifact:
    if len(passes) < 3:
        raise ValueError("development consensus requires at least three validated passes")
    evidence_kinds = {artifact.payload.evidence_kind for artifact, _ in passes}
    if len(evidence_kinds) != 1:
        raise ValueError("episode and series passes cannot be pooled into one consensus")
    evidence_kind = next(iter(evidence_kinds))

    validated: list[
        tuple[
            ValidatedDevelopmentAutomatedPassArtifact,
            dict[tuple[str, str, str], DevelopmentResponse],
        ]
    ] = []
    for artifact, normalized_output in passes:
        errors = validated_development_pass_integrity_errors(artifact)
        if errors:
            raise ValueError("invalid development pass: " + "; ".join(errors))
        if _sha256_bytes(normalized_output) != artifact.payload.normalized_output_sha256:
            raise ValueError("development consensus bytes do not bind validated pass")
        validated.append((artifact, _responses_by_unit(evidence_kind, normalized_output)))

    first_artifact, first_rows = validated[0]
    first_pass = first_artifact.payload.automated_pass
    expected_units = set(first_rows)
    for artifact, rows in validated[1:]:
        current_pass = artifact.payload.automated_pass
        if set(rows) != expected_units:
            raise ValueError("development consensus passes do not contain the same units")
        if artifact.payload.task_set_sha256 != first_artifact.payload.task_set_sha256:
            raise ValueError("development consensus passes do not bind the same task set")
        if current_pass.corpus_sha256 != first_pass.corpus_sha256:
            raise ValueError("development consensus passes do not bind the same corpus")
        if current_pass.codebook_sha256 != first_pass.codebook_sha256:
            raise ValueError("development consensus passes do not bind the same codebook")
        if current_pass.coding_procedure_sha256 != first_pass.coding_procedure_sha256:
            raise ValueError("development consensus passes do not bind the same procedure")
        if current_pass.prompt_sha256 != first_pass.prompt_sha256:
            raise ValueError("development consensus passes do not bind the same transport prompt")

    unit_rows: list[DevelopmentConsensusUnit] = []
    all_pass_ids = {artifact.payload.automated_pass.pass_id for artifact, _ in validated}
    for unit in sorted(expected_units):
        groups: dict[str, list[tuple[str, DevelopmentResponse, str]]] = defaultdict(list)
        trace: list[DevelopmentPassUnitConsensusTrace] = []
        for artifact, rows in validated:
            response = rows[unit]
            semantic = semantic_development_response(response)
            response_sha = _sha256_bytes(canonical_json_bytes(response))
            semantic_sha = _sha256_bytes(canonical_json_bytes(semantic))
            pass_id = artifact.payload.automated_pass.pass_id
            groups[semantic_sha].append((pass_id, semantic, response_sha))
            trace.append(
                DevelopmentPassUnitConsensusTrace(
                    pass_id=pass_id,
                    response_sha256=response_sha,
                    semantic_sha256=semantic_sha,
                )
            )
        _, winner_rows = max(groups.items(), key=lambda item: (len(item[1]), item[0]))
        winner_count = len(winner_rows)
        pass_count = len(validated)
        if winner_count == pass_count:
            status: DevelopmentConsensusStatus = "unanimous"
        elif winner_count > pass_count / 2:
            status = "majority"
        else:
            status = "unresolved"
        agreeing = tuple(sorted(row[0] for row in winner_rows)) if status != "unresolved" else ()
        dissenting = (
            tuple(sorted(all_pass_ids - set(agreeing)))
            if status != "unresolved"
            else tuple(sorted(all_pass_ids))
        )
        consensus_response = (
            min(winner_rows, key=lambda row: row[0])[1] if status != "unresolved" else None
        )
        unit_rows.append(
            DevelopmentConsensusUnit(
                evidence_kind=evidence_kind,
                task_id=unit[0],
                evidence_id=unit[1],
                observable_id=unit[2],
                status=status,
                agreeing_pass_ids=agreeing,
                dissenting_pass_ids=dissenting,
                consensus_response=consensus_response,
                pass_trace=tuple(sorted(trace, key=lambda row: row.pass_id)),
            )
        )

    payload = DevelopmentConsensusPayload(
        evidence_kind=evidence_kind,
        validated_pass_artifact_sha256=tuple(
            artifact.artifact_sha256 for artifact, _ in validated
        ),
        pass_ids=tuple(artifact.payload.automated_pass.pass_id for artifact, _ in validated),
        corpus_sha256=first_pass.corpus_sha256,
        codebook_sha256=first_pass.codebook_sha256,
        coding_procedure_sha256=first_pass.coding_procedure_sha256,
        prompt_sha256=first_pass.prompt_sha256,
        task_set_sha256=first_artifact.payload.task_set_sha256,
        units=tuple(unit_rows),
        total_units=len(unit_rows),
        unanimous_units=sum(row.status == "unanimous" for row in unit_rows),
        majority_units=sum(row.status == "majority" for row in unit_rows),
        unresolved_units=sum(row.status == "unresolved" for row in unit_rows),
    )
    digest = sha256_json(payload)
    return DevelopmentConsensusArtifact(
        artifact_id=f"LPDCN-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def development_consensus_integrity_errors(
    artifact: DevelopmentConsensusArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPDCN-{digest[:20].upper()}":
        return ("development consensus failed content-address verification",)
    return ()
