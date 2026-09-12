"""Public-safe binding manifest for a private Life Patterns development coding package.

The private package may contain autobiographical text. This artifact contains identifiers,
hashes, counts, provenance limits, and chronology gates only. It binds the v8/v8.1 transfer
corpus to the exact resolved development measurement stack, explicit transport prompts, and a
pre-label human calibration selection without making the transfer corpus a canonical behavioral
freeze.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import sha256_json

from .development_calibration_sampling import DevelopmentCalibrationSamplingArtifact
from .development_series_evidence import (
    DevelopmentSeriesCodingManifestArtifact,
    DevelopmentSeriesCodingTask,
)
from .development_transfer_corpus import (
    DevelopmentEpisodeCodingTask,
    DevelopmentTaskSetManifestArtifact,
    DevelopmentTransferCorpusArtifact,
)
from .resolved_development_stack import ResolvedDevelopmentStack

_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class DevelopmentCodingPackageModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentCodingPackagePayload(DevelopmentCodingPackageModel):
    schema_version: Literal["life-patterns-development-coding-package-v1"] = (
        "life-patterns-development-coding-package-v1"
    )
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    source_record_sha256: str = Field(pattern=_SHA256_PATTERN)
    supplement_sha256: str = Field(pattern=_SHA256_PATTERN)
    source_transcript_completeness: Literal["partial_exact_segments_only"]
    participant_theory_exposure: Literal["prior_exposure_possible", "unknown"]

    reconciled_source_artifact_id: str = Field(pattern=r"^LPCB-[0-9A-F]{20}$")
    reconciled_source_sha256: str = Field(pattern=_SHA256_PATTERN)
    ambiguity_resolution_id: str = Field(pattern=r"^LPAR-[0-9A-F]{20}$")
    ambiguity_resolution_sha256: str = Field(pattern=_SHA256_PATTERN)
    resolved_view_id: str = Field(pattern=r"^LPRV-[0-9A-F]{20}$")
    resolved_view_sha256: str = Field(pattern=_SHA256_PATTERN)
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    procedure_id: str = Field(pattern=r"^LPSP-[0-9A-F]{20}$")
    procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_manual_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_transport_prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    series_transport_prompt_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    observable_count: Literal[22] = 22
    resolved_subcode_count: Literal[208] = 208
    resolved_non_action_count: Literal[28] = 28

    episode_task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_task_count: int = Field(ge=1)
    episode_observable_unit_count: int = Field(ge=1)
    series_task_set_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    series_task_count: int = Field(ge=0)
    series_observable_unit_count: int = Field(ge=0)
    # These identifiers are copied from private records into a public receipt.
    # Keep arbitrary source text out without rewriting the private source IDs.
    blocked_summary_only_series_ids: tuple[
        Annotated[str, Field(pattern=r"^(?:SER|ADD-EV)-[0-9]{3}$")], ...
    ]
    series_reports_are_not_pseudo_episodes: Literal[True] = True

    calibration_manifest_id: str = Field(pattern=r"^LPCA-[0-9A-F]{20}$")
    calibration_manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    calibration_episode_unit_count: int = Field(ge=1)
    calibration_series_unit_count: int = Field(ge=0)
    calibration_selected_before_automated_labels: Literal[True] = True

    required_isolated_automated_passes: Literal[3] = 3
    raw_automated_outputs_must_be_preserved: Literal[True] = True
    human_first_pass_must_precede_llm_label_exposure: Literal[True] = True
    target_model_information_available: Literal[False] = False
    canonical_behavioral_freeze_eligible: Literal[False] = False
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    target_model_scoring_authorized: Literal[False] = False
    contains_private_participant_text: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("development coding package timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def series_bindings_are_coherent(self) -> DevelopmentCodingPackagePayload:
        if self.series_task_count:
            if (
                self.series_task_set_sha256 is None
                or self.series_transport_prompt_sha256 is None
                or self.series_observable_unit_count < 1
            ):
                raise ValueError(
                    "series task count requires bound nonempty tasks and series transport prompt"
                )
        elif (
            self.series_task_set_sha256 is not None
            or self.series_transport_prompt_sha256 is not None
            or self.series_observable_unit_count
        ):
            raise ValueError("empty series task set cannot carry series task/prompt bindings")
        return self


class DevelopmentCodingPackageArtifact(DevelopmentCodingPackageModel):
    schema_version: Literal["life-patterns-development-coding-package-artifact-v1"] = (
        "life-patterns-development-coding-package-artifact-v1"
    )
    package_id: str = Field(pattern=r"^LPKG-[0-9A-F]{20}$")
    package_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentCodingPackagePayload


def build_development_coding_package(
    *,
    corpus: DevelopmentTransferCorpusArtifact,
    stack: ResolvedDevelopmentStack,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    episode_manifest: DevelopmentTaskSetManifestArtifact,
    episode_transport_prompt_sha256: str,
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
    series_manifest: DevelopmentSeriesCodingManifestArtifact | None,
    series_transport_prompt_sha256: str | None,
    blocked_summary_only_series_ids: tuple[str, ...],
    calibration: DevelopmentCalibrationSamplingArtifact,
    created_at_utc: datetime,
) -> DevelopmentCodingPackageArtifact:
    if corpus.payload.canonical_behavioral_freeze_eligible:
        raise ValueError(
            "development package refuses a transfer corpus claiming canonical freeze eligibility"
        )
    if not corpus.payload.validation_use_forbidden:
        raise ValueError("development package requires validation use to remain forbidden")
    if episode_manifest.payload.corpus_id != corpus.corpus_id:
        raise ValueError("episode task manifest does not bind development corpus")
    if episode_manifest.payload.corpus_sha256 != corpus.corpus_sha256:
        raise ValueError("episode task manifest does not bind exact corpus hash")
    if episode_manifest.payload.task_set_sha256 != sha256_json(episode_tasks):
        raise ValueError("episode task manifest does not bind supplied episode task set")
    if any(task.observable_ids != stack.observable_ids for task in episode_tasks):
        raise ValueError("episode tasks do not use exact resolved observable universe")

    if series_tasks:
        if series_manifest is None:
            raise ValueError("series tasks require a series task manifest")
        if series_transport_prompt_sha256 is None:
            raise ValueError("series tasks require a series transport prompt hash")
        if series_manifest.payload.corpus_id != corpus.corpus_id:
            raise ValueError("series task manifest does not bind development corpus")
        if series_manifest.payload.corpus_sha256 != corpus.corpus_sha256:
            raise ValueError("series task manifest does not bind exact corpus hash")
        if series_manifest.payload.task_set_sha256 != sha256_json(series_tasks):
            raise ValueError("series task manifest does not bind supplied series task set")
        if any(task.observable_ids != stack.observable_ids for task in series_tasks):
            raise ValueError("series tasks do not use exact resolved observable universe")
    elif series_manifest is not None or series_transport_prompt_sha256 is not None:
        raise ValueError("series task/prompt binding supplied without series tasks")

    if (
        calibration.payload.corpus_id != corpus.corpus_id
        or calibration.payload.corpus_sha256 != corpus.corpus_sha256
    ):
        raise ValueError("calibration manifest does not bind exact development corpus")
    if calibration.payload.episode_task_set_sha256 != sha256_json(episode_tasks):
        raise ValueError("calibration manifest does not bind episode task set")
    expected_series_hash = sha256_json(series_tasks) if series_tasks else None
    if calibration.payload.series_task_set_sha256 != expected_series_hash:
        raise ValueError("calibration manifest does not bind series task set")

    participant_exposure = corpus.payload.participant_theory_exposure
    if participant_exposure not in {"prior_exposure_possible", "unknown"}:
        raise ValueError(
            "development package requires participant theory exposure to remain explicit"
        )

    payload = DevelopmentCodingPackagePayload(
        corpus_id=corpus.corpus_id,
        corpus_sha256=corpus.corpus_sha256,
        source_record_sha256=corpus.payload.source_record_sha256,
        supplement_sha256=corpus.payload.supplement_sha256,
        source_transcript_completeness=corpus.payload.source_transcript_completeness,
        participant_theory_exposure=participant_exposure,
        reconciled_source_artifact_id=stack.source.artifact_id,
        reconciled_source_sha256=stack.source.artifact_sha256,
        ambiguity_resolution_id=stack.resolution.resolution_id,
        ambiguity_resolution_sha256=stack.resolution.resolution_sha256,
        resolved_view_id=stack.resolved.view_id,
        resolved_view_sha256=stack.resolved.view_sha256,
        ontology_artifact_id=stack.ontology.artifact_id,
        ontology_sha256=stack.ontology.ontology_sha256,
        procedure_id=stack.procedure.procedure_id,
        procedure_sha256=stack.procedure.procedure_sha256,
        coding_manual_sha256=stack.coding_manual_sha256,
        episode_transport_prompt_sha256=episode_transport_prompt_sha256,
        series_transport_prompt_sha256=series_transport_prompt_sha256,
        episode_task_set_sha256=sha256_json(episode_tasks),
        episode_task_count=len(episode_tasks),
        episode_observable_unit_count=sum(len(task.observable_ids) for task in episode_tasks),
        series_task_set_sha256=expected_series_hash,
        series_task_count=len(series_tasks),
        series_observable_unit_count=sum(len(task.observable_ids) for task in series_tasks),
        blocked_summary_only_series_ids=blocked_summary_only_series_ids,
        calibration_manifest_id=calibration.manifest_id,
        calibration_manifest_sha256=calibration.manifest_sha256,
        calibration_episode_unit_count=len(calibration.payload.representative_episode_units),
        calibration_series_unit_count=len(calibration.payload.representative_series_units),
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentCodingPackageArtifact(
        package_id=f"LPKG-{digest[:20].upper()}",
        package_sha256=digest,
        payload=payload,
    )


def development_coding_package_integrity_errors(
    artifact: DevelopmentCodingPackageArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.package_sha256 != digest or artifact.package_id != f"LPKG-{digest[:20].upper()}":
        return ("development coding package failed content-address verification",)
    return ()
