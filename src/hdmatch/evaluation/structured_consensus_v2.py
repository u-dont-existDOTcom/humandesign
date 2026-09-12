"""Deterministic semantic consensus across validated StructuredAnnotation V2 passes."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

from .structured_annotation_v2 import (
    StructuredAnnotationResponseV2,
    load_structured_annotation_responses_jsonl_v2,
)
from .validated_automated_pass_v2 import (
    ValidatedStructuredAutomatedPassArtifactV2,
    validated_structured_automated_pass_integrity_errors,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
ConsensusStatus = Literal["unanimous", "majority", "unresolved"]


class ConsensusModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class PassUnitConsensusTrace(ConsensusModel):
    pass_id: str = Field(min_length=1)
    response_sha256: str = Field(pattern=_SHA256_PATTERN)
    semantic_sha256: str = Field(pattern=_SHA256_PATTERN)


class StructuredConsensusUnitV2(ConsensusModel):
    task_id: str = Field(min_length=1)
    episode_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    status: ConsensusStatus
    agreeing_pass_ids: tuple[str, ...]
    dissenting_pass_ids: tuple[str, ...]
    consensus_response: StructuredAnnotationResponseV2 | None = None
    pass_trace: tuple[PassUnitConsensusTrace, ...] = Field(min_length=3)

    @model_validator(mode="after")
    def resolution_matches_status(self) -> StructuredConsensusUnitV2:
        if self.status == "unresolved" and self.consensus_response is not None:
            raise ValueError("unresolved consensus unit cannot carry a consensus response")
        if self.status != "unresolved" and self.consensus_response is None:
            raise ValueError("resolved consensus unit requires a consensus response")
        return self


class StructuredConsensusPayloadV2(ConsensusModel):
    schema_version: Literal["life-patterns-structured-consensus-v2"] = (
        "life-patterns-structured-consensus-v2"
    )
    validated_pass_artifact_sha256: tuple[str, ...] = Field(min_length=3)
    pass_ids: tuple[str, ...] = Field(min_length=3)
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    codebook_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    consensus_rule_id: Literal["structured-semantic-strict-majority-v1"] = (
        "structured-semantic-strict-majority-v1"
    )
    units: tuple[StructuredConsensusUnitV2, ...] = Field(min_length=1)
    total_units: int = Field(ge=1)
    unanimous_units: int = Field(ge=0)
    majority_units: int = Field(ge=0)
    unresolved_units: int = Field(ge=0)
    self_consistency_does_not_establish_correctness: Literal[True] = True

    @field_validator("pass_ids")
    @classmethod
    def pass_ids_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("structured consensus contains duplicate pass IDs")
        return value

    @model_validator(mode="after")
    def counts_are_coherent(self) -> StructuredConsensusPayloadV2:
        if self.total_units != len(self.units):
            raise ValueError("structured consensus total_units disagrees with unit rows")
        if self.unanimous_units + self.majority_units + self.unresolved_units != self.total_units:
            raise ValueError("structured consensus status counts must sum to total_units")
        return self


class StructuredConsensusArtifactV2(ConsensusModel):
    schema_version: Literal["life-patterns-structured-consensus-artifact-v2"] = (
        "life-patterns-structured-consensus-artifact-v2"
    )
    artifact_id: str = Field(pattern=r"^LPSC-[0-9A-F]{20}$")
    artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: StructuredConsensusPayloadV2


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sorted_scalar_values(values: tuple[object, ...]) -> tuple[object, ...]:
    return tuple(sorted(values, key=lambda value: canonical_json_bytes(value)))


def semantic_response(response: StructuredAnnotationResponseV2) -> StructuredAnnotationResponseV2:
    coded_values = response.coded_values
    if response.value_relation == "unordered_multiple":
        coded_values = _sorted_scalar_values(coded_values)  # type: ignore[assignment]
    return response.model_copy(
        update={
            "coded_values": coded_values,
            "supporting_source_turn_ids": tuple(sorted(set(response.supporting_source_turn_ids))),
            "counterevidence_source_turn_ids": tuple(
                sorted(set(response.counterevidence_source_turn_ids))
            ),
            "context_qualifiers": tuple(sorted(set(response.context_qualifiers))),
            "missingness_flags": tuple(sorted(set(response.missingness_flags))),
            "influence_source_turn_ids": tuple(sorted(set(response.influence_source_turn_ids))),
            "annotation_note": None,
        }
    )


def _responses_by_unit(
    data: bytes,
) -> dict[tuple[str, str, str], StructuredAnnotationResponseV2]:
    rows = load_structured_annotation_responses_jsonl_v2(data)
    output = {
        (row.task_id, row.episode_id, row.observable_id): row
        for row in rows
    }
    if len(output) != len(rows):
        raise ValueError("structured consensus input repeats annotation units")
    return output


def build_structured_consensus_v2(
    passes: tuple[tuple[ValidatedStructuredAutomatedPassArtifactV2, bytes], ...],
) -> StructuredConsensusArtifactV2:
    if len(passes) < 3:
        raise ValueError("structured consensus requires at least three validated passes")

    validated: list[tuple[ValidatedStructuredAutomatedPassArtifactV2, dict[tuple[str, str, str], StructuredAnnotationResponseV2]]] = []
    for artifact, normalized_output in passes:
        errors = validated_structured_automated_pass_integrity_errors(artifact)
        if errors:
            raise ValueError("invalid validated pass: " + "; ".join(errors))
        if _sha256_bytes(normalized_output) != artifact.payload.normalized_output_sha256:
            raise ValueError("structured consensus output bytes do not bind validated pass")
        validated.append((artifact, _responses_by_unit(normalized_output)))

    first_artifact, first_rows = validated[0]
    first_pass = first_artifact.payload.automated_pass
    expected_units = set(first_rows)
    for artifact, rows in validated[1:]:
        current_pass = artifact.payload.automated_pass
        if set(rows) != expected_units:
            raise ValueError("structured consensus passes do not contain the same annotation units")
        if artifact.payload.task_set_sha256 != first_artifact.payload.task_set_sha256:
            raise ValueError("structured consensus passes do not bind the same task set")
        if current_pass.corpus_sha256 != first_pass.corpus_sha256:
            raise ValueError("structured consensus passes do not bind the same corpus")
        if current_pass.codebook_sha256 != first_pass.codebook_sha256:
            raise ValueError("structured consensus passes do not bind the same codebook")
        if current_pass.coding_procedure_sha256 != first_pass.coding_procedure_sha256:
            raise ValueError("structured consensus passes do not bind the same coding procedure")
        if current_pass.prompt_sha256 != first_pass.prompt_sha256:
            raise ValueError("structured consensus passes do not bind the same prompt")

    unit_rows: list[StructuredConsensusUnitV2] = []
    for unit in sorted(expected_units):
        groups: dict[str, list[tuple[str, StructuredAnnotationResponseV2, str]]] = defaultdict(list)
        trace: list[PassUnitConsensusTrace] = []
        for artifact, rows in validated:
            response = rows[unit]
            semantic = semantic_response(response)
            response_sha = _sha256_bytes(canonical_json_bytes(response))
            semantic_sha = _sha256_bytes(canonical_json_bytes(semantic))
            pass_id = artifact.payload.automated_pass.pass_id
            groups[semantic_sha].append((pass_id, semantic, response_sha))
            trace.append(
                PassUnitConsensusTrace(
                    pass_id=pass_id,
                    response_sha256=response_sha,
                    semantic_sha256=semantic_sha,
                )
            )

        winner_sha, winner_rows = max(
            groups.items(),
            key=lambda item: (len(item[1]), item[0]),
        )
        winner_count = len(winner_rows)
        pass_count = len(validated)
        if winner_count == pass_count:
            status: ConsensusStatus = "unanimous"
        elif winner_count > pass_count / 2:
            status = "majority"
        else:
            status = "unresolved"

        agreeing = tuple(sorted(row[0] for row in winner_rows)) if status != "unresolved" else ()
        all_pass_ids = {artifact.payload.automated_pass.pass_id for artifact, _ in validated}
        dissenting = tuple(sorted(all_pass_ids - set(agreeing))) if status != "unresolved" else tuple(
            sorted(all_pass_ids)
        )
        consensus_response = (
            min(winner_rows, key=lambda row: row[0])[1]
            if status != "unresolved"
            else None
        )
        unit_rows.append(
            StructuredConsensusUnitV2(
                task_id=unit[0],
                episode_id=unit[1],
                observable_id=unit[2],
                status=status,
                agreeing_pass_ids=agreeing,
                dissenting_pass_ids=dissenting,
                consensus_response=consensus_response,
                pass_trace=tuple(sorted(trace, key=lambda row: row.pass_id)),
            )
        )

    unanimous = sum(row.status == "unanimous" for row in unit_rows)
    majority = sum(row.status == "majority" for row in unit_rows)
    unresolved = sum(row.status == "unresolved" for row in unit_rows)
    payload = StructuredConsensusPayloadV2(
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
        unanimous_units=unanimous,
        majority_units=majority,
        unresolved_units=unresolved,
    )
    digest = sha256_json(payload)
    return StructuredConsensusArtifactV2(
        artifact_id=f"LPSC-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def structured_consensus_integrity_errors(
    artifact: StructuredConsensusArtifactV2,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.artifact_sha256 != digest or artifact.artifact_id != f"LPSC-{digest[:20].upper()}":
        return ("structured consensus artifact failed content-address verification",)
    return ()
