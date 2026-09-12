"""Deterministic pre-label calibration sampling for development transfer evidence.

This sampler is deliberately separate from ``calibration_sampling.py`` because v8/v8.1 transfer
material is not a canonical behavioral freeze and must never inherit validation semantics by
accident.  It samples episode-observable and repeated-series-observable units as distinct strata,
with optional per-observable representation floors, before any automated labels exist.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import sha256_json

from .development_series_evidence import DevelopmentSeriesCodingTask
from .development_transfer_corpus import DevelopmentEpisodeCodingTask

_SHA256_PATTERN = r"^[0-9a-f]{64}$"

DevelopmentEvidenceKind = Literal["episode", "series"]


class DevelopmentCalibrationModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class DevelopmentCalibrationUnit(DevelopmentCalibrationModel):
    evidence_kind: DevelopmentEvidenceKind
    evidence_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)


class DevelopmentCalibrationSamplingPayload(DevelopmentCalibrationModel):
    schema_version: Literal["life-patterns-development-calibration-sampling-v1"] = (
        "life-patterns-development-calibration-sampling-v1"
    )
    corpus_id: str = Field(pattern=r"^LPDC-[0-9A-F]{20}$")
    corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_task_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    series_task_set_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    sampling_seed_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_per_observable_floor: int = Field(ge=0)
    series_per_observable_floor: int = Field(ge=0)
    representative_episode_units: tuple[DevelopmentCalibrationUnit, ...]
    representative_series_units: tuple[DevelopmentCalibrationUnit, ...]
    selected_before_automated_labels: Literal[True] = True
    no_automated_labels_used_for_selection: Literal[True] = True
    target_model_information_used_for_selection: Literal[False] = False
    separate_episode_and_series_strata: Literal[True] = True
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("development calibration timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def units_are_separate_unique_strata(self) -> DevelopmentCalibrationSamplingPayload:
        for expected_kind, units in (
            ("episode", self.representative_episode_units),
            ("series", self.representative_series_units),
        ):
            if any(row.evidence_kind != expected_kind for row in units):
                raise ValueError(f"{expected_kind} calibration stratum contains wrong evidence kind")
            keys = [(row.evidence_id, row.observable_id) for row in units]
            if len(keys) != len(set(keys)):
                raise ValueError(f"{expected_kind} calibration stratum repeats a unit")
        if self.representative_series_units and self.series_task_set_sha256 is None:
            raise ValueError("series calibration units require a bound series task set")
        if not self.representative_series_units and self.series_task_set_sha256 is not None:
            raise ValueError("bound series task set requires at least one selected series unit")
        return self


class DevelopmentCalibrationSamplingArtifact(DevelopmentCalibrationModel):
    schema_version: Literal["life-patterns-development-calibration-sampling-artifact-v1"] = (
        "life-patterns-development-calibration-sampling-artifact-v1"
    )
    manifest_id: str = Field(pattern=r"^LPCA-[0-9A-F]{20}$")
    manifest_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: DevelopmentCalibrationSamplingPayload


def _validate_seed(seed_sha256: str) -> None:
    if len(seed_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in seed_sha256):
        raise ValueError("development calibration seed must be a lowercase SHA-256 digest")


def _rank(seed_sha256: str, unit: DevelopmentCalibrationUnit) -> str:
    material = (
        f"{seed_sha256}\0{unit.evidence_kind}\0{unit.evidence_id}\0{unit.observable_id}"
    ).encode()
    return hashlib.sha256(material).hexdigest()


def episode_unit_universe(
    tasks: tuple[DevelopmentEpisodeCodingTask, ...],
) -> tuple[DevelopmentCalibrationUnit, ...]:
    units = {
        (task.episode_id, observable_id)
        for task in tasks
        for observable_id in task.observable_ids
    }
    return tuple(
        DevelopmentCalibrationUnit(
            evidence_kind="episode",
            evidence_id=evidence_id,
            observable_id=observable_id,
        )
        for evidence_id, observable_id in sorted(units)
    )


def series_unit_universe(
    tasks: tuple[DevelopmentSeriesCodingTask, ...],
) -> tuple[DevelopmentCalibrationUnit, ...]:
    units = {
        (task.series_id, observable_id)
        for task in tasks
        for observable_id in task.observable_ids
    }
    return tuple(
        DevelopmentCalibrationUnit(
            evidence_kind="series",
            evidence_id=evidence_id,
            observable_id=observable_id,
        )
        for evidence_id, observable_id in sorted(units)
    )


def _balanced_sample(
    universe: tuple[DevelopmentCalibrationUnit, ...],
    *,
    sample_size: int,
    per_observable_floor: int,
    seed_sha256: str,
) -> tuple[DevelopmentCalibrationUnit, ...]:
    if sample_size < 0:
        raise ValueError("development calibration sample size cannot be negative")
    if sample_size > len(universe):
        raise ValueError("development calibration sample size exceeds eligible universe")
    if not universe:
        if sample_size or per_observable_floor:
            raise ValueError("cannot sample from an empty calibration universe")
        return ()

    by_observable: dict[str, list[DevelopmentCalibrationUnit]] = defaultdict(list)
    for unit in universe:
        by_observable[unit.observable_id].append(unit)
    observable_ids = sorted(by_observable)
    minimum_required = sum(
        min(per_observable_floor, len(by_observable[observable_id]))
        for observable_id in observable_ids
    )
    if sample_size < minimum_required:
        raise ValueError(
            "development calibration sample size is too small for the requested observable floor"
        )

    chosen: dict[tuple[str, str, str], DevelopmentCalibrationUnit] = {}
    for observable_id in observable_ids:
        ranked = sorted(
            by_observable[observable_id],
            key=lambda unit: (_rank(seed_sha256, unit), unit.evidence_id),
        )
        for unit in ranked[:per_observable_floor]:
            chosen[(unit.evidence_kind, unit.evidence_id, unit.observable_id)] = unit

    remaining = sorted(
        (
            unit
            for unit in universe
            if (unit.evidence_kind, unit.evidence_id, unit.observable_id) not in chosen
        ),
        key=lambda unit: (
            _rank(seed_sha256, unit),
            unit.observable_id,
            unit.evidence_id,
        ),
    )
    for unit in remaining[: sample_size - len(chosen)]:
        chosen[(unit.evidence_kind, unit.evidence_id, unit.observable_id)] = unit

    return tuple(
        sorted(
            chosen.values(),
            key=lambda unit: (unit.observable_id, unit.evidence_id, unit.evidence_kind),
        )
    )


def build_development_calibration_sample(
    *,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...] = (),
    episode_sample_size: int,
    series_sample_size: int = 0,
    episode_per_observable_floor: int = 0,
    series_per_observable_floor: int = 0,
    seed_sha256: str,
    created_at_utc: datetime,
) -> DevelopmentCalibrationSamplingArtifact:
    """Freeze deterministic human-calibration units before automated labels exist."""

    _validate_seed(seed_sha256)
    if not episode_tasks:
        raise ValueError("development calibration requires episode tasks")
    corpus_ids = {task.corpus_id for task in (*episode_tasks, *series_tasks)}
    corpus_hashes = {task.corpus_sha256 for task in (*episode_tasks, *series_tasks)}
    if len(corpus_ids) != 1 or len(corpus_hashes) != 1:
        raise ValueError("development calibration tasks must bind one exact corpus")
    if series_sample_size and not series_tasks:
        raise ValueError("series calibration sample requested without series tasks")
    if series_tasks and series_sample_size == 0:
        raise ValueError("supplied series tasks require a nonzero series calibration sample")

    episode_universe = episode_unit_universe(episode_tasks)
    series_universe = series_unit_universe(series_tasks)
    episode_units = _balanced_sample(
        episode_universe,
        sample_size=episode_sample_size,
        per_observable_floor=episode_per_observable_floor,
        seed_sha256=seed_sha256,
    )
    series_units = _balanced_sample(
        series_universe,
        sample_size=series_sample_size,
        per_observable_floor=series_per_observable_floor,
        seed_sha256=seed_sha256,
    )
    payload = DevelopmentCalibrationSamplingPayload(
        corpus_id=next(iter(corpus_ids)),
        corpus_sha256=next(iter(corpus_hashes)),
        episode_task_set_sha256=sha256_json(episode_tasks),
        series_task_set_sha256=sha256_json(series_tasks) if series_tasks else None,
        sampling_seed_sha256=seed_sha256,
        episode_per_observable_floor=episode_per_observable_floor,
        series_per_observable_floor=series_per_observable_floor,
        representative_episode_units=episode_units,
        representative_series_units=series_units,
        created_at_utc=created_at_utc,
    )
    digest = sha256_json(payload)
    return DevelopmentCalibrationSamplingArtifact(
        manifest_id=f"LPCA-{digest[:20].upper()}",
        manifest_sha256=digest,
        payload=payload,
    )


def development_calibration_integrity_errors(
    artifact: DevelopmentCalibrationSamplingArtifact,
    *,
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...] = (),
) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(artifact.payload)
    if artifact.manifest_sha256 != digest or artifact.manifest_id != f"LPCA-{digest[:20].upper()}":
        errors.append("development calibration manifest failed content-address verification")
    if artifact.payload.episode_task_set_sha256 != sha256_json(episode_tasks):
        errors.append("development calibration manifest does not bind episode task set")
    expected_series_hash = sha256_json(series_tasks) if series_tasks else None
    if artifact.payload.series_task_set_sha256 != expected_series_hash:
        errors.append("development calibration manifest does not bind series task set")

    episode_universe = {
        (unit.evidence_id, unit.observable_id) for unit in episode_unit_universe(episode_tasks)
    }
    series_universe = {
        (unit.evidence_id, unit.observable_id) for unit in series_unit_universe(series_tasks)
    }
    for unit in artifact.payload.representative_episode_units:
        if (unit.evidence_id, unit.observable_id) not in episode_universe:
            errors.append("development calibration contains episode unit outside task universe")
    for unit in artifact.payload.representative_series_units:
        if (unit.evidence_id, unit.observable_id) not in series_universe:
            errors.append("development calibration contains series unit outside task universe")
    return tuple(dict.fromkeys(errors))


def _selected_by_evidence(
    units: tuple[DevelopmentCalibrationUnit, ...],
) -> dict[str, set[str]]:
    selected: dict[str, set[str]] = defaultdict(set)
    for unit in units:
        selected[unit.evidence_id].add(unit.observable_id)
    return selected


def human_episode_calibration_tasks(
    tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    manifest: DevelopmentCalibrationSamplingArtifact,
) -> tuple[DevelopmentEpisodeCodingTask, ...]:
    errors = development_calibration_integrity_errors(manifest, episode_tasks=tasks)
    if errors and any("episode" in error for error in errors):
        raise ValueError("invalid development calibration manifest: " + "; ".join(errors))
    selected = _selected_by_evidence(manifest.payload.representative_episode_units)
    output: list[DevelopmentEpisodeCodingTask] = []
    for task in tasks:
        observable_ids = tuple(
            observable_id
            for observable_id in task.observable_ids
            if observable_id in selected.get(task.episode_id, set())
        )
        if observable_ids:
            output.append(task.model_copy(update={"observable_ids": observable_ids}))
    return tuple(output)


def human_series_calibration_tasks(
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...],
    series_tasks: tuple[DevelopmentSeriesCodingTask, ...],
    manifest: DevelopmentCalibrationSamplingArtifact,
) -> tuple[DevelopmentSeriesCodingTask, ...]:
    errors = development_calibration_integrity_errors(
        manifest,
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
    )
    if errors:
        raise ValueError("invalid development calibration manifest: " + "; ".join(errors))
    selected = _selected_by_evidence(manifest.payload.representative_series_units)
    output: list[DevelopmentSeriesCodingTask] = []
    for task in series_tasks:
        observable_ids = tuple(
            observable_id
            for observable_id in task.observable_ids
            if observable_id in selected.get(task.series_id, set())
        )
        if observable_ids:
            output.append(task.model_copy(update={"observable_ids": observable_ids}))
    return tuple(output)
