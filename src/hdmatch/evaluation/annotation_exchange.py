"""Tool-neutral annotation exchange for the Life Patterns measurement framework."""

from __future__ import annotations

import json
from typing import Any, cast

from pydantic import ConfigDict, BaseModel, Field

from hdmatch.experiments.canonical import canonical_json_bytes

from .neutral_measurement import (
    AnnotationTask,
    CodeState,
    CodedEpisodeRecord,
    FreezeEvidenceIndex,
    ScalarValue,
    TheoryExposureState,
)


class AnnotationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    schema_version: str = Field(default="life-patterns-annotation-response-v1")
    task_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    episode_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    state: CodeState
    coded_value: ScalarValue | None = None
    mixed_values: tuple[ScalarValue, ...] = ()
    coder_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    supporting_source_turn_ids: tuple[str, ...] = ()
    counterevidence_source_turn_ids: tuple[str, ...] = ()
    context_qualifiers: tuple[str, ...] = ()
    life_phase_qualifier: str | None = None
    language: str | None = None
    theory_exposure: TheoryExposureState = "unknown"
    annotation_note: str | None = None


def annotation_tasks_jsonl(tasks: tuple[AnnotationTask, ...]) -> bytes:
    return b"\n".join(canonical_json_bytes(task) for task in tasks) + (b"\n" if tasks else b"")


def annotation_responses_jsonl(responses: tuple[AnnotationResponse, ...]) -> bytes:
    return b"\n".join(canonical_json_bytes(response) for response in responses) + (
        b"\n" if responses else b""
    )


def load_annotation_responses_jsonl(data: bytes) -> tuple[AnnotationResponse, ...]:
    responses: list[AnnotationResponse] = []
    for line_number, raw_line in enumerate(data.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            value: Any = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"annotation response line {line_number} is invalid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"annotation response line {line_number} is not a JSON object")
        response = AnnotationResponse.model_validate(cast(dict[str, Any], value))
        if canonical_json_bytes(response) != raw_line:
            raise ValueError(f"annotation response line {line_number} is not canonical JSON")
        responses.append(response)
    return tuple(responses)


def coded_record_from_annotation_response(
    response: AnnotationResponse,
    *,
    task: AnnotationTask,
    evidence: FreezeEvidenceIndex,
) -> CodedEpisodeRecord:
    if response.task_id != task.task_id:
        raise ValueError("annotation response does not bind the supplied task")
    if (
        response.freeze_id != task.freeze_id
        or response.freeze_sha256 != task.freeze_sha256
        or response.freeze_id != evidence.freeze_id
        or response.freeze_sha256 != evidence.freeze_sha256
    ):
        raise ValueError("annotation response does not bind the supplied behavioral freeze")
    if (
        response.ontology_artifact_id != task.ontology_artifact_id
        or response.ontology_sha256 != task.ontology_sha256
    ):
        raise ValueError("annotation response does not bind the task ontology")
    if response.episode_id != task.episode_id or response.episode_id not in evidence.episode_sha256:
        raise ValueError("annotation response does not bind the task episode")
    if response.observable_id not in task.observable_ids:
        raise ValueError("annotation response references an observable outside the task")
    task_turn_ids = {
        str(row["turn_id"])
        for row in task.source_turns
        if isinstance(row.get("turn_id"), str)
    }
    cited = set(response.supporting_source_turn_ids) | set(response.counterevidence_source_turn_ids)
    if not cited.issubset(task_turn_ids):
        raise ValueError("annotation response cites source turns outside the annotation task")
    return CodedEpisodeRecord(
        episode_id=response.episode_id,
        observable_id=response.observable_id,
        state=response.state,
        coded_value=response.coded_value,
        mixed_values=response.mixed_values,
        coder_confidence=response.coder_confidence,
        supporting_source_turn_ids=response.supporting_source_turn_ids,
        counterevidence_source_turn_ids=response.counterevidence_source_turn_ids,
        context_qualifiers=response.context_qualifiers,
        life_phase_qualifier=response.life_phase_qualifier,
        language=response.language,
        input_modality=evidence.episode_input_modality[response.episode_id],
        theory_exposure=response.theory_exposure,
        source_episode_participant_revised=evidence.participant_revised_episode[response.episode_id],
        annotation_note=response.annotation_note,
    )
