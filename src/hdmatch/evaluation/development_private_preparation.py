"""Prepare a private v8/v8.1 development coding package without running any coder.

This is the final deterministic preparation stage before isolated theory-blind coding.  It reads
the two participant transfer JSON objects, builds the development-only corpus, binds the exact
resolved measurement stack, generates episode and exact-source repeated-series task sets, and
freezes a human calibration subset before automated labels exist.

No model is called here.  No target-model information is accepted.  Private text remains only in
the returned private artifacts; the package receipt is public-safe by construction.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from hdmatch.experiments.canonical import canonical_json_bytes, write_new_bytes

from .development_calibration_sampling import (
    DevelopmentCalibrationSamplingArtifact,
    build_development_calibration_sample,
)
from .development_coding_package import (
    DevelopmentCodingPackageArtifact,
    build_development_coding_package,
)
from .development_series_evidence import (
    DevelopmentSeriesCodingManifestArtifact,
    DevelopmentSeriesTaskBuildReport,
    build_development_series_manifest,
    build_development_series_tasks,
)
from .development_transfer_corpus import (
    DevelopmentEpisodeCodingTask,
    DevelopmentTaskSetManifestArtifact,
    DevelopmentTransferCorpusArtifact,
    build_development_episode_tasks,
    build_development_task_manifest,
    build_v8_v8_1_development_corpus,
)
from .resolved_development_stack import (
    ResolvedDevelopmentStack,
    build_repository_resolved_development_stack,
)

CALIBRATION_SEED_POLICY = "life-patterns-v8-v8.1-development-calibration-seed-v1"
DEFAULT_EPISODE_CALIBRATION_UNITS = 44
DEFAULT_SERIES_CALIBRATION_UNITS = 22
DEFAULT_EPISODE_PER_OBSERVABLE_FLOOR = 2
DEFAULT_SERIES_PER_OBSERVABLE_FLOOR = 1


@dataclass(frozen=True)
class PrivateDevelopmentPreparation:
    stack: ResolvedDevelopmentStack
    corpus: DevelopmentTransferCorpusArtifact
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...]
    episode_manifest: DevelopmentTaskSetManifestArtifact
    series_report: DevelopmentSeriesTaskBuildReport
    series_manifest: DevelopmentSeriesCodingManifestArtifact | None
    calibration: DevelopmentCalibrationSamplingArtifact
    package: DevelopmentCodingPackageArtifact
    calibration_seed_sha256: str


def deterministic_calibration_seed(
    *,
    source_record_sha256: str,
    supplement_sha256: str,
) -> str:
    material = (
        CALIBRATION_SEED_POLICY
        + "\0"
        + source_record_sha256
        + "\0"
        + supplement_sha256
    ).encode()
    return hashlib.sha256(material).hexdigest()


def prepare_v8_private_development_package(
    *,
    original: dict[str, Any],
    supplement: dict[str, Any],
    repo_root: str | Path,
    source_commit: str,
    created_at_utc: datetime,
    episode_calibration_units: int = DEFAULT_EPISODE_CALIBRATION_UNITS,
    series_calibration_units: int = DEFAULT_SERIES_CALIBRATION_UNITS,
    episode_per_observable_floor: int = DEFAULT_EPISODE_PER_OBSERVABLE_FLOOR,
    series_per_observable_floor: int = DEFAULT_SERIES_PER_OBSERVABLE_FLOOR,
) -> PrivateDevelopmentPreparation:
    stack = build_repository_resolved_development_stack(
        repo_root,
        source_commit=source_commit,
        released_at_utc=created_at_utc,
    )
    corpus = build_v8_v8_1_development_corpus(
        original,
        supplement,
        participant_theory_exposure="prior_exposure_possible",
        created_at_utc=created_at_utc,
    )
    episode_tasks = build_development_episode_tasks(
        corpus,
        observable_ids=stack.observable_ids,
    )
    episode_manifest = build_development_task_manifest(
        corpus,
        tasks=episode_tasks,
        created_at_utc=created_at_utc,
    )
    series_report = build_development_series_tasks(
        corpus,
        observable_ids=stack.observable_ids,
    )
    series_tasks = series_report.tasks
    series_manifest = (
        build_development_series_manifest(series_report, created_at_utc=created_at_utc)
        if series_tasks
        else None
    )

    if episode_calibration_units > len(episode_tasks) * len(stack.observable_ids):
        raise ValueError("episode calibration sample exceeds private episode task universe")
    if series_tasks:
        if series_calibration_units < 1:
            raise ValueError("exact-source series tasks require nonzero human calibration sampling")
        if series_calibration_units > len(series_tasks) * len(stack.observable_ids):
            raise ValueError("series calibration sample exceeds private series task universe")
    elif series_calibration_units:
        raise ValueError("series calibration units requested but no exact-source series are available")

    seed = deterministic_calibration_seed(
        source_record_sha256=corpus.payload.source_record_sha256,
        supplement_sha256=corpus.payload.supplement_sha256,
    )
    calibration = build_development_calibration_sample(
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
        episode_sample_size=episode_calibration_units,
        series_sample_size=series_calibration_units if series_tasks else 0,
        episode_per_observable_floor=episode_per_observable_floor,
        series_per_observable_floor=series_per_observable_floor if series_tasks else 0,
        seed_sha256=seed,
        created_at_utc=created_at_utc,
    )
    package = build_development_coding_package(
        corpus=corpus,
        stack=stack,
        episode_tasks=episode_tasks,
        episode_manifest=episode_manifest,
        series_tasks=series_tasks,
        series_manifest=series_manifest,
        blocked_summary_only_series_ids=series_report.blocked_summary_only_series_ids,
        calibration=calibration,
        created_at_utc=created_at_utc,
    )
    return PrivateDevelopmentPreparation(
        stack=stack,
        corpus=corpus,
        episode_tasks=episode_tasks,
        episode_manifest=episode_manifest,
        series_report=series_report,
        series_manifest=series_manifest,
        calibration=calibration,
        package=package,
        calibration_seed_sha256=seed,
    )


def private_preparation_safe_summary(
    preparation: PrivateDevelopmentPreparation,
) -> dict[str, Any]:
    package = preparation.package.payload
    return {
        "schema_version": "life-patterns-private-development-preparation-summary-v1",
        "package_id": preparation.package.package_id,
        "package_sha256": preparation.package.package_sha256,
        "corpus_id": package.corpus_id,
        "corpus_sha256": package.corpus_sha256,
        "source_record_sha256": package.source_record_sha256,
        "supplement_sha256": package.supplement_sha256,
        "resolved_view_id": package.resolved_view_id,
        "resolved_view_sha256": package.resolved_view_sha256,
        "ontology_artifact_id": package.ontology_artifact_id,
        "ontology_sha256": package.ontology_sha256,
        "procedure_id": package.procedure_id,
        "procedure_sha256": package.procedure_sha256,
        "coder_prompt_sha256": package.coder_prompt_sha256,
        "episode_task_count": package.episode_task_count,
        "episode_observable_unit_count": package.episode_observable_unit_count,
        "series_task_count": package.series_task_count,
        "series_observable_unit_count": package.series_observable_unit_count,
        "blocked_summary_only_series_count": len(package.blocked_summary_only_series_ids),
        "calibration_manifest_id": package.calibration_manifest_id,
        "calibration_manifest_sha256": package.calibration_manifest_sha256,
        "calibration_episode_unit_count": package.calibration_episode_unit_count,
        "calibration_series_unit_count": package.calibration_series_unit_count,
        "calibration_seed_sha256": preparation.calibration_seed_sha256,
        "required_isolated_automated_passes": package.required_isolated_automated_passes,
        "source_transcript_completeness": package.source_transcript_completeness,
        "canonical_behavioral_freeze_eligible": package.canonical_behavioral_freeze_eligible,
        "validation_use_forbidden": package.validation_use_forbidden,
        "target_model_scoring_authorized": package.target_model_scoring_authorized,
        "contains_private_participant_text": False,
    }


def write_private_development_preparation(
    output_dir: str | Path,
    preparation: PrivateDevelopmentPreparation,
) -> dict[str, Path]:
    """Write private artifacts read-only; only the package/safe summary are safe for public Git."""

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    private_payloads: dict[str, Any] = {
        "development_transfer_corpus.json": preparation.corpus,
        "development_episode_tasks.json": preparation.episode_tasks,
        "development_episode_task_manifest.json": preparation.episode_manifest,
        "development_series_task_report.json": preparation.series_report,
        "development_calibration_manifest.json": preparation.calibration,
        "resolved_source_artifact.json": preparation.stack.source,
        "resolved_ambiguity_resolution_artifact.json": preparation.stack.resolution,
        "resolved_codebook_view.json": preparation.stack.resolved,
        "resolved_development_ontology.json": preparation.stack.ontology,
        "resolved_structured_procedure.json": preparation.stack.procedure,
    }
    if preparation.series_manifest is not None:
        private_payloads["development_series_task_manifest.json"] = preparation.series_manifest
    private_payloads["development_series_tasks.json"] = preparation.series_report.tasks

    paths: dict[str, Path] = {}
    for filename, payload in private_payloads.items():
        path = write_new_bytes(root / filename, canonical_json_bytes(payload), mode=0o400)
        paths[filename] = path

    package_path = write_new_bytes(
        root / "development_coding_package_public_safe.json",
        canonical_json_bytes(preparation.package),
        mode=0o400,
    )
    paths[package_path.name] = package_path
    summary_path = write_new_bytes(
        root / "development_preparation_public_safe_summary.json",
        canonical_json_bytes(private_preparation_safe_summary(preparation)),
        mode=0o400,
    )
    paths[summary_path.name] = summary_path
    return paths
