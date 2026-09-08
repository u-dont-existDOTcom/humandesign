"""Prepare recurrence-corrected v2 development artifacts without running any coder.

V2 deliberately reconstructs and reuses the exact deterministic pre-label calibration selection
from the historical v1 preparation instead of drawing a new sample after the method correction.
The private corpus/task universe is unchanged; only the versioned measurement stack, recurrence
semantics, response contract, and transport prompts change.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from hdmatch.experiments.canonical import canonical_json_bytes, write_new_bytes

from .development_calibration_sampling import DevelopmentCalibrationSamplingArtifact
from .development_coding_package_v2 import (
    DevelopmentCodingPackageArtifactV2,
    build_development_coding_package_v2,
)
from .development_private_preparation import (
    DEFAULT_EPISODE_CALIBRATION_UNITS,
    DEFAULT_EPISODE_PER_OBSERVABLE_FLOOR,
    DEFAULT_SERIES_CALIBRATION_UNITS,
    DEFAULT_SERIES_PER_OBSERVABLE_FLOOR,
    EPISODE_TRANSPORT_PROMPT_REL,
    prepare_v8_private_development_package,
)
from .development_series_evidence import (
    DevelopmentSeriesCodingManifestArtifact,
    DevelopmentSeriesTaskBuildReport,
)
from .development_transfer_corpus import (
    DevelopmentEpisodeCodingTask,
    DevelopmentTaskSetManifestArtifact,
    DevelopmentTransferCorpusArtifact,
)
from .resolved_development_stack import file_sha256
from .resolved_development_stack_v2 import (
    ResolvedDevelopmentStackV2,
    build_repository_resolved_development_stack_v2,
)

SERIES_TRANSPORT_PROMPT_V2_REL = Path(
    "state/LIFE-PATTERNS-DEVELOPMENT-SERIES-CODING-PROMPT-v2-2026-09-08.txt"
)
HUMAN_CALIBRATION_PROMPT_V2_REL = Path(
    "state/LIFE-PATTERNS-DEVELOPMENT-HUMAN-CALIBRATION-PROMPT-v2-2026-09-08.txt"
)


@dataclass(frozen=True)
class PrivateDevelopmentPreparationV2:
    stack: ResolvedDevelopmentStackV2
    corpus: DevelopmentTransferCorpusArtifact
    episode_tasks: tuple[DevelopmentEpisodeCodingTask, ...]
    episode_manifest: DevelopmentTaskSetManifestArtifact
    series_report: DevelopmentSeriesTaskBuildReport
    series_manifest: DevelopmentSeriesCodingManifestArtifact | None
    calibration: DevelopmentCalibrationSamplingArtifact
    package: DevelopmentCodingPackageArtifactV2
    episode_transport_prompt_sha256: str
    series_transport_prompt_sha256: str | None
    human_calibration_prompt_sha256: str
    calibration_selection_reused_without_resampling: bool = True


def _prompt_hash(path: Path, *, label: str) -> str:
    if not path.is_file():
        raise ValueError(f"v2 development package is missing {label}: {path}")
    return file_sha256(path)


def prepare_v8_private_development_package_v2(
    *,
    original: dict[str, Any],
    supplement: dict[str, Any],
    repo_root: str | Path,
    historical_source_commit: str,
    historical_created_at_utc: datetime,
    v2_source_commit: str,
    v2_created_at_utc: datetime,
    episode_calibration_units: int = DEFAULT_EPISODE_CALIBRATION_UNITS,
    series_calibration_units: int = DEFAULT_SERIES_CALIBRATION_UNITS,
    episode_per_observable_floor: int = DEFAULT_EPISODE_PER_OBSERVABLE_FLOOR,
    series_per_observable_floor: int = DEFAULT_SERIES_PER_OBSERVABLE_FLOOR,
) -> PrivateDevelopmentPreparationV2:
    """Rebuild the exact pre-label selection, then bind it to v2 semantics without resampling."""

    root = Path(repo_root)
    historical = prepare_v8_private_development_package(
        original=original,
        supplement=supplement,
        repo_root=root,
        source_commit=historical_source_commit,
        created_at_utc=historical_created_at_utc,
        episode_calibration_units=episode_calibration_units,
        series_calibration_units=series_calibration_units,
        episode_per_observable_floor=episode_per_observable_floor,
        series_per_observable_floor=series_per_observable_floor,
    )
    stack = build_repository_resolved_development_stack_v2(
        root,
        source_commit=v2_source_commit,
        released_at_utc=v2_created_at_utc,
    )
    if historical.stack.observable_ids != stack.observable_ids:
        raise ValueError("v2 recurrence revision changed the frozen observable universe")

    episode_prompt_sha256 = _prompt_hash(
        root / EPISODE_TRANSPORT_PROMPT_REL,
        label="episode transport prompt",
    )
    series_prompt_sha256 = (
        _prompt_hash(
            root / SERIES_TRANSPORT_PROMPT_V2_REL,
            label="series transport prompt v2",
        )
        if historical.series_report.tasks
        else None
    )
    human_prompt_sha256 = _prompt_hash(
        root / HUMAN_CALIBRATION_PROMPT_V2_REL,
        label="human calibration prompt v2",
    )
    package = build_development_coding_package_v2(
        corpus=historical.corpus,
        stack=stack,
        episode_tasks=historical.episode_tasks,
        episode_manifest=historical.episode_manifest,
        episode_transport_prompt_sha256=episode_prompt_sha256,
        series_tasks=historical.series_report.tasks,
        series_manifest=historical.series_manifest,
        series_transport_prompt_sha256=series_prompt_sha256,
        human_calibration_prompt_sha256=human_prompt_sha256,
        blocked_summary_only_series_ids=historical.series_report.blocked_summary_only_series_ids,
        calibration=historical.calibration,
        created_at_utc=v2_created_at_utc,
    )
    return PrivateDevelopmentPreparationV2(
        stack=stack,
        corpus=historical.corpus,
        episode_tasks=historical.episode_tasks,
        episode_manifest=historical.episode_manifest,
        series_report=historical.series_report,
        series_manifest=historical.series_manifest,
        calibration=historical.calibration,
        package=package,
        episode_transport_prompt_sha256=episode_prompt_sha256,
        series_transport_prompt_sha256=series_prompt_sha256,
        human_calibration_prompt_sha256=human_prompt_sha256,
    )


def private_preparation_v2_safe_summary(
    preparation: PrivateDevelopmentPreparationV2,
) -> dict[str, Any]:
    package = preparation.package.payload
    return {
        "schema_version": "life-patterns-private-development-preparation-summary-v2",
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
        "coding_manual_sha256": package.coding_manual_sha256,
        "recurrence_policy_sha256": package.recurrence_policy_sha256,
        "episode_transport_prompt_sha256": package.episode_transport_prompt_sha256,
        "series_transport_prompt_sha256": package.series_transport_prompt_sha256,
        "human_calibration_prompt_sha256": package.human_calibration_prompt_sha256,
        "episode_task_count": package.episode_task_count,
        "episode_observable_unit_count": package.episode_observable_unit_count,
        "series_task_count": package.series_task_count,
        "series_observable_unit_count": package.series_observable_unit_count,
        "blocked_summary_only_series_count": len(package.blocked_summary_only_series_ids),
        "calibration_manifest_id": package.calibration_manifest_id,
        "calibration_manifest_sha256": package.calibration_manifest_sha256,
        "calibration_episode_unit_count": package.calibration_episode_unit_count,
        "calibration_series_unit_count": package.calibration_series_unit_count,
        "calibration_selection_reused_without_resampling": True,
        "calibration_resampled_after_method_revision": False,
        "series_response_schema_version": package.series_response_schema_version,
        "confirming_episodes_are_not_frequency_counts": True,
        "required_isolated_automated_passes": package.required_isolated_automated_passes,
        "source_transcript_completeness": package.source_transcript_completeness,
        "canonical_behavioral_freeze_eligible": package.canonical_behavioral_freeze_eligible,
        "validation_use_forbidden": package.validation_use_forbidden,
        "target_model_scoring_authorized": package.target_model_scoring_authorized,
        "target_model_information_used_for_revision": False,
        "contains_private_participant_text": False,
    }


def write_private_development_preparation_v2(
    output_dir: str | Path,
    preparation: PrivateDevelopmentPreparationV2,
) -> dict[str, Path]:
    """Write immutable private v2 preparation plus public-safe package/summary."""

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    private_payloads: dict[str, Any] = {
        "development_transfer_corpus.json": preparation.corpus,
        "development_episode_tasks.json": preparation.episode_tasks,
        "development_episode_task_manifest.json": preparation.episode_manifest,
        "development_series_task_report.json": preparation.series_report,
        "development_series_tasks.json": preparation.series_report.tasks,
        "development_calibration_manifest.json": preparation.calibration,
        "resolved_source_artifact.json": preparation.stack.source,
        "resolved_ambiguity_resolution_artifact.json": preparation.stack.resolution,
        "resolved_codebook_view.json": preparation.stack.resolved,
        "resolved_development_ontology_v2.json": preparation.stack.ontology,
        "resolved_structured_procedure_v2.json": preparation.stack.procedure,
    }
    if preparation.series_manifest is not None:
        private_payloads["development_series_task_manifest.json"] = preparation.series_manifest

    paths: dict[str, Path] = {}
    for filename, payload in private_payloads.items():
        path = write_new_bytes(root / filename, canonical_json_bytes(payload), mode=0o400)
        paths[filename] = path

    package_path = write_new_bytes(
        root / "development_coding_package_v2_public_safe.json",
        canonical_json_bytes(preparation.package),
        mode=0o400,
    )
    paths[package_path.name] = package_path
    summary_path = write_new_bytes(
        root / "development_preparation_v2_public_safe_summary.json",
        canonical_json_bytes(private_preparation_v2_safe_summary(preparation)),
        mode=0o400,
    )
    paths[summary_path.name] = summary_path
    return paths
