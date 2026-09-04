"""Theory-neutral calibration sampling for Life Patterns automated coding.

Representative units are selected deterministically before automated labels exist. A separate
boundary stratum may be supplied from a frozen theory-neutral selector specification and is
reported separately so enriched difficult cases are not mistaken for natural prevalence.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, load_json_bytes, sha256_json, write_new_bytes

from .structured_annotation_v2 import StructuredAnnotationTaskV2

_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class CalibrationSamplingModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class CalibrationUnit(CalibrationSamplingModel):
    episode_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)


class CalibrationSamplingManifestPayload(CalibrationSamplingModel):
    schema_version: Literal["life-patterns-calibration-sampling-manifest-v1"] = (
        "life-patterns-calibration-sampling-manifest-v1"
    )
    parent_corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    codebook_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    representative_sampling_seed_sha256: str = Field(pattern=_SHA256_PATTERN)
    representative_units: tuple[CalibrationUnit, ...]
    boundary_units: tuple[CalibrationUnit, ...] = ()
    boundary_selector_spec_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    selected_before_automated_labels: Literal[True] = True
    target_model_information_used_for_selection: Literal[False] = False
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("calibration sampling timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def sampling_sets_are_coherent(self) -> CalibrationSamplingManifestPayload:
        for label, units in (
            ("representative", self.representative_units),
            ("boundary", self.boundary_units),
        ):
            keys = [(row.episode_id, row.observable_id) for row in units]
            if len(keys) != len(set(keys)):
                raise ValueError(f"{label} calibration stratum contains duplicate units")
        if self.boundary_units and self.boundary_selector_spec_sha256 is None:
            raise ValueError("boundary calibration units require a frozen selector specification")
        if not self.boundary_units and self.boundary_selector_spec_sha256 is not None:
            raise ValueError("boundary selector specification requires boundary units")
        return self


class CalibrationSamplingManifestArtifact(CalibrationSamplingModel):
    schema_version: Literal["life-patterns-calibration-sampling-manifest-artifact-v1"] = (
        "life-patterns-calibration-sampling-manifest-artifact-v1"
    )
    manifest_id: str = Field(pattern=r"^LPCS-[0-9A-F]{20}$")
    manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: CalibrationSamplingManifestPayload


def annotation_unit_universe(tasks: tuple[StructuredAnnotationTaskV2, ...]) -> tuple[CalibrationUnit, ...]:
    units = {
        (task.episode_id, observable_id)
        for task in tasks
        for observable_id in task.observable_ids
    }
    return tuple(
        CalibrationUnit(episode_id=episode_id, observable_id=observable_id)
        for episode_id, observable_id in sorted(units)
    )


def _unit_rank(seed_sha256: str, unit: CalibrationUnit) -> str:
    material = f"{seed_sha256}\0{unit.episode_id}\0{unit.observable_id}".encode()
    return hashlib.sha256(material).hexdigest()


def deterministic_representative_sample(
    tasks: tuple[StructuredAnnotationTaskV2, ...],
    *,
    sample_size: int,
    seed_sha256: str,
) -> tuple[CalibrationUnit, ...]:
    if len(seed_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in seed_sha256):
        raise ValueError("representative sampling seed must be a lowercase SHA-256 digest")
    universe = annotation_unit_universe(tasks)
    if sample_size < 1:
        raise ValueError("representative sample size must be positive")
    if sample_size > len(universe):
        raise ValueError("representative sample size exceeds eligible unit universe")
    ranked = sorted(universe, key=lambda unit: (_unit_rank(seed_sha256, unit), unit.episode_id, unit.observable_id))
    return tuple(ranked[:sample_size])


def build_calibration_sampling_manifest(
    payload: CalibrationSamplingManifestPayload,
    *,
    tasks: tuple[StructuredAnnotationTaskV2, ...],
) -> CalibrationSamplingManifestArtifact:
    universe = {(row.episode_id, row.observable_id) for row in annotation_unit_universe(tasks)}
    selected = {
        (row.episode_id, row.observable_id)
        for row in (*payload.representative_units, *payload.boundary_units)
    }
    outside = sorted(selected - universe)
    if outside:
        raise ValueError(f"calibration manifest contains units outside frozen task universe: {outside}")
    expected_task_hash = sha256_json(tasks)
    if payload.task_set_sha256 != expected_task_hash:
        raise ValueError("calibration manifest does not bind exact structured task set")
    digest = sha256_json(payload)
    return CalibrationSamplingManifestArtifact(
        manifest_id=f"LPCS-{digest[:20].upper()}",
        manifest_sha256=digest,
        payload=payload,
    )


def calibration_manifest_integrity_errors(
    artifact: CalibrationSamplingManifestArtifact,
) -> tuple[str, ...]:
    digest = sha256_json(artifact.payload)
    if artifact.manifest_sha256 != digest or artifact.manifest_id != f"LPCS-{digest[:20].upper()}":
        return ("calibration sampling manifest failed content-address verification",)
    return ()


def human_calibration_tasks(
    tasks: tuple[StructuredAnnotationTaskV2, ...],
    manifest: CalibrationSamplingManifestArtifact,
) -> tuple[StructuredAnnotationTaskV2, ...]:
    errors = calibration_manifest_integrity_errors(manifest)
    if errors:
        raise ValueError("invalid calibration sampling manifest: " + "; ".join(errors))
    if manifest.payload.task_set_sha256 != sha256_json(tasks):
        raise ValueError("calibration sampling manifest does not bind supplied task set")

    selected_by_episode: dict[str, set[str]] = defaultdict(set)
    for unit in (*manifest.payload.representative_units, *manifest.payload.boundary_units):
        selected_by_episode[unit.episode_id].add(unit.observable_id)

    output: list[StructuredAnnotationTaskV2] = []
    for task in tasks:
        selected = selected_by_episode.get(task.episode_id)
        if not selected:
            continue
        observable_ids = tuple(row for row in task.observable_ids if row in selected)
        if not observable_ids:
            continue
        output.append(task.model_copy(update={"observable_ids": observable_ids}))
    return tuple(output)


def write_calibration_sampling_manifest(
    path: str | Path,
    artifact: CalibrationSamplingManifestArtifact,
) -> Path:
    errors = calibration_manifest_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid calibration sampling manifest: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_calibration_sampling_manifest(path: str | Path) -> CalibrationSamplingManifestArtifact:
    raw = load_json_bytes(path, require_canonical=True)
    artifact = CalibrationSamplingManifestArtifact.model_validate(raw)
    errors = calibration_manifest_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid calibration sampling manifest: " + "; ".join(errors))
    return artifact
