"""Immutable receipt contracts for the Life Patterns blind human reliability pilot.

These objects record corpus selection, coder training, independent first-pass freezing, and
post-freeze adjudication. They contain no substantive behavioral constructs and do not
calculate or claim reliability, construct validity, or model validity.
"""

from __future__ import annotations

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

_SHA256_PATTERN = r"^[0-9a-f]{64}$"

PilotItemRole = Literal["training", "reliability"]
SelectionReason = Literal[
    "ordinary_development_episode",
    "boundary_case",
    "sparse_prerequisite_extension",
    "modality_or_context_coverage",
]


class PilotModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class PilotCorpusItem(PilotModel):
    pilot_item_id: str = Field(min_length=1)
    role: PilotItemRole
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_id: str = Field(min_length=1)
    episode_sha256: str = Field(pattern=_SHA256_PATTERN)
    selection_reason: SelectionReason
    boundary_case_tags: tuple[str, ...] = ()
    target_model_information_used_for_selection: Literal[False] = False

    @model_validator(mode="after")
    def boundary_reason_requires_tags(self) -> PilotCorpusItem:
        if self.selection_reason == "boundary_case" and not self.boundary_case_tags:
            raise ValueError("boundary-case pilot items require at least one theory-neutral boundary tag")
        return self


class PilotCorpusManifestPayload(PilotModel):
    schema_version: Literal["life-patterns-blind-pilot-corpus-manifest-v1"] = (
        "life-patterns-blind-pilot-corpus-manifest-v1"
    )
    codebook_content_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    training_protocol_sha256: str = Field(pattern=_SHA256_PATTERN)
    items: tuple[PilotCorpusItem, ...] = Field(min_length=1)
    created_at_utc: datetime
    reliability_items_locked_before_first_pass: Literal[True] = True
    birth_chart_model_information_available_to_selector: Literal[False] = False
    target_model_outputs_available_to_selector: Literal[False] = False
    selection_uses_only_theory_neutral_criteria: Literal[True] = True
    sparse_extension_reported_separately: Literal[True] = True

    @field_validator("created_at_utc")
    @classmethod
    def manifest_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("pilot-manifest timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("items")
    @classmethod
    def pilot_item_ids_are_unique(cls, value: tuple[PilotCorpusItem, ...]) -> tuple[PilotCorpusItem, ...]:
        ids = [row.pilot_item_id for row in value]
        if len(ids) != len(set(ids)):
            raise ValueError("pilot corpus contains duplicate pilot_item_id values")
        keys = [(row.freeze_id, row.episode_id, row.role) for row in value]
        if len(keys) != len(set(keys)):
            raise ValueError("pilot corpus repeats an episode within the same pilot role")
        return value


class PilotCorpusManifestArtifact(PilotModel):
    schema_version: Literal["life-patterns-blind-pilot-corpus-artifact-v1"] = (
        "life-patterns-blind-pilot-corpus-artifact-v1"
    )
    manifest_id: str = Field(pattern=r"^LPPM-[0-9A-F]{20}$")
    manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: PilotCorpusManifestPayload


class PilotCoderTrainingReceipt(PilotModel):
    schema_version: Literal["life-patterns-blind-pilot-coder-training-v1"] = (
        "life-patterns-blind-pilot-coder-training-v1"
    )
    coder_id: str = Field(min_length=1)
    codebook_content_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    training_protocol_sha256: str = Field(pattern=_SHA256_PATTERN)
    training_material_sha256: str = Field(pattern=_SHA256_PATTERN)
    training_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    completed_at_utc: datetime
    birth_chart_model_blind: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    no_other_coder_reliability_labels_available_during_training_assessment: Literal[True] = True
    training_completion_does_not_claim_coder_reliability: Literal[True] = True

    @field_validator("completed_at_utc")
    @classmethod
    def training_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("coder-training timestamp must be timezone-aware")
        return value.astimezone(UTC)


class PilotCoderOutputReference(PilotModel):
    coder_id: str = Field(min_length=1)
    training_receipt_sha256: str = Field(pattern=_SHA256_PATTERN)
    annotation_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_started_at_utc: datetime
    coding_frozen_at_utc: datetime

    @field_validator("coding_started_at_utc", "coding_frozen_at_utc")
    @classmethod
    def coding_times_are_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("pilot-coding timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def coding_window_is_ordered(self) -> PilotCoderOutputReference:
        if self.coding_frozen_at_utc < self.coding_started_at_utc:
            raise ValueError("coder output cannot freeze before coding starts")
        return self


class PilotFirstPassPayload(PilotModel):
    schema_version: Literal["life-patterns-blind-pilot-first-pass-v1"] = (
        "life-patterns-blind-pilot-first-pass-v1"
    )
    corpus_manifest_id: str = Field(pattern=r"^LPPM-[0-9A-F]{20}$")
    corpus_manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    codebook_content_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    coder_outputs: tuple[PilotCoderOutputReference, ...] = Field(min_length=2)
    frozen_at_utc: datetime
    coders_worked_independently_until_outputs_frozen: Literal[True] = True
    coders_could_not_view_each_others_labels_or_notes: Literal[True] = True
    reliability_must_be_computed_from_pre_adjudication_outputs: Literal[True] = True
    birth_chart_model_blind: Literal[True] = True
    target_model_outputs_available: Literal[False] = False

    @field_validator("frozen_at_utc")
    @classmethod
    def first_pass_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("first-pass timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("coder_outputs")
    @classmethod
    def coder_ids_are_unique(
        cls,
        value: tuple[PilotCoderOutputReference, ...],
    ) -> tuple[PilotCoderOutputReference, ...]:
        ids = [row.coder_id for row in value]
        if len(ids) != len(set(ids)):
            raise ValueError("blind first pass requires distinct coder identities")
        return value

    @model_validator(mode="after")
    def first_pass_follows_all_coder_freezes(self) -> PilotFirstPassPayload:
        if self.frozen_at_utc < max(row.coding_frozen_at_utc for row in self.coder_outputs):
            raise ValueError("first-pass receipt cannot precede a coder-output freeze")
        return self


class PilotFirstPassArtifact(PilotModel):
    schema_version: Literal["life-patterns-blind-pilot-first-pass-artifact-v1"] = (
        "life-patterns-blind-pilot-first-pass-artifact-v1"
    )
    first_pass_id: str = Field(pattern=r"^LPPF-[0-9A-F]{20}$")
    first_pass_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: PilotFirstPassPayload


class PilotAdjudicationPayload(PilotModel):
    schema_version: Literal["life-patterns-blind-pilot-adjudication-v1"] = (
        "life-patterns-blind-pilot-adjudication-v1"
    )
    first_pass_id: str = Field(pattern=r"^LPPF-[0-9A-F]{20}$")
    first_pass_sha256: str = Field(pattern=_SHA256_PATTERN)
    adjudication_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    adjudicator_ids: tuple[str, ...] = Field(min_length=1)
    adjudicated_at_utc: datetime
    original_independent_outputs_preserved: Literal[True] = True
    reliability_computed_from_pre_adjudication_outputs: Literal[True] = True
    target_model_outputs_available: Literal[False] = False
    birth_chart_model_blind: Literal[True] = True

    @field_validator("adjudicated_at_utc")
    @classmethod
    def adjudication_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("adjudication timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("adjudicator_ids")
    @classmethod
    def adjudicators_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("adjudication receipt contains duplicate adjudicator IDs")
        return value


class PilotAdjudicationArtifact(PilotModel):
    schema_version: Literal["life-patterns-blind-pilot-adjudication-artifact-v1"] = (
        "life-patterns-blind-pilot-adjudication-artifact-v1"
    )
    adjudication_id: str = Field(pattern=r"^LPPA-[0-9A-F]{20}$")
    adjudication_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: PilotAdjudicationPayload


def _content_address(prefix: str, payload: PilotModel) -> tuple[str, str]:
    digest = sha256_json(payload)
    return f"{prefix}-{digest[:20].upper()}", digest


def build_pilot_corpus_manifest(payload: PilotCorpusManifestPayload) -> PilotCorpusManifestArtifact:
    artifact_id, digest = _content_address("LPPM", payload)
    return PilotCorpusManifestArtifact(
        manifest_id=artifact_id,
        manifest_sha256=digest,
        payload=payload,
    )


def build_pilot_first_pass(payload: PilotFirstPassPayload) -> PilotFirstPassArtifact:
    artifact_id, digest = _content_address("LPPF", payload)
    return PilotFirstPassArtifact(
        first_pass_id=artifact_id,
        first_pass_sha256=digest,
        payload=payload,
    )


def build_pilot_adjudication(payload: PilotAdjudicationPayload) -> PilotAdjudicationArtifact:
    artifact_id, digest = _content_address("LPPA", payload)
    return PilotAdjudicationArtifact(
        adjudication_id=artifact_id,
        adjudication_sha256=digest,
        payload=payload,
    )


def pilot_corpus_manifest_integrity_errors(artifact: PilotCorpusManifestArtifact) -> tuple[str, ...]:
    expected_id, digest = _content_address("LPPM", artifact.payload)
    if artifact.manifest_id != expected_id or artifact.manifest_sha256 != digest:
        return ("pilot corpus manifest failed content-address verification",)
    return ()


def pilot_first_pass_integrity_errors(artifact: PilotFirstPassArtifact) -> tuple[str, ...]:
    expected_id, digest = _content_address("LPPF", artifact.payload)
    if artifact.first_pass_id != expected_id or artifact.first_pass_sha256 != digest:
        return ("pilot first-pass artifact failed content-address verification",)
    return ()


def pilot_adjudication_integrity_errors(
    artifact: PilotAdjudicationArtifact,
    first_pass: PilotFirstPassArtifact,
) -> tuple[str, ...]:
    errors: list[str] = []
    expected_id, digest = _content_address("LPPA", artifact.payload)
    if artifact.adjudication_id != expected_id or artifact.adjudication_sha256 != digest:
        errors.append("pilot adjudication artifact failed content-address verification")
    if artifact.payload.first_pass_id != first_pass.first_pass_id or (
        artifact.payload.first_pass_sha256 != first_pass.first_pass_sha256
    ):
        errors.append("pilot adjudication does not bind the supplied first-pass artifact")
    if artifact.payload.adjudicated_at_utc < first_pass.payload.frozen_at_utc:
        errors.append("pilot adjudication cannot precede first-pass freeze")
    return tuple(dict.fromkeys(errors))


def write_pilot_artifact(
    path: str | Path,
    artifact: PilotCorpusManifestArtifact | PilotFirstPassArtifact | PilotAdjudicationArtifact,
) -> Path:
    if isinstance(artifact, PilotCorpusManifestArtifact):
        errors = pilot_corpus_manifest_integrity_errors(artifact)
    elif isinstance(artifact, PilotFirstPassArtifact):
        errors = pilot_first_pass_integrity_errors(artifact)
    else:
        expected_id, digest = _content_address("LPPA", artifact.payload)
        errors = (
            ("pilot adjudication artifact failed content-address verification",)
            if artifact.adjudication_id != expected_id or artifact.adjudication_sha256 != digest
            else ()
        )
    if errors:
        raise ValueError("invalid pilot artifact: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_pilot_corpus_manifest(path: str | Path) -> PilotCorpusManifestArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = PilotCorpusManifestArtifact.model_validate(cast(dict[str, Any], raw))
    errors = pilot_corpus_manifest_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid pilot corpus manifest: " + "; ".join(errors))
    return artifact
