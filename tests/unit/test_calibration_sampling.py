from __future__ import annotations

import stat
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.calibration_sampling import (
    CalibrationSamplingManifestPayload,
    CalibrationUnit,
    annotation_unit_universe,
    build_calibration_sampling_manifest,
    deterministic_representative_sample,
    human_calibration_tasks,
    load_calibration_sampling_manifest,
    write_calibration_sampling_manifest,
)
from hdmatch.evaluation.structured_annotation_v2 import StructuredAnnotationTaskV2
from hdmatch.experiments.canonical import sha256_json

NOW = datetime(2026, 9, 4, 2, 0, tzinfo=UTC)


def _task(episode_id: str, observables: tuple[str, ...]) -> StructuredAnnotationTaskV2:
    return StructuredAnnotationTaskV2(
        task_id=f"TASK-{episode_id}",
        freeze_id="BPF-0123456789ABCDEF0123",
        freeze_sha256="0" * 64,
        ontology_artifact_id="LPO-0123456789ABCDEF0123",
        ontology_sha256="1" * 64,
        procedure_id="LPSP-0123456789ABCDEF0123",
        procedure_sha256="2" * 64,
        episode_id=episode_id,
        episode_title=f"Episode {episode_id}",
        episode_narrative="STRUCTURAL CALIBRATION TEST",
        source_turns=({"turn_id": f"TURN-{episode_id}", "text": "STRUCTURAL"},),
        observable_ids=observables,
    )


def _tasks() -> tuple[StructuredAnnotationTaskV2, ...]:
    return (
        _task("EP-A", ("OBS-A", "OBS-B", "OBS-C")),
        _task("EP-B", ("OBS-A", "OBS-B", "OBS-C")),
    )


def test_representative_sample_is_deterministic_and_from_full_unit_universe() -> None:
    tasks = _tasks()
    universe = annotation_unit_universe(tasks)
    assert len(universe) == 6
    seed = "a" * 64
    first = deterministic_representative_sample(tasks, sample_size=3, seed_sha256=seed)
    second = deterministic_representative_sample(tasks, sample_size=3, seed_sha256=seed)
    assert first == second
    assert len(set((row.episode_id, row.observable_id) for row in first)) == 3
    assert set(first).issubset(set(universe))

    with pytest.raises(ValueError, match="exceeds eligible unit universe"):
        deterministic_representative_sample(tasks, sample_size=7, seed_sha256=seed)


def test_manifest_binds_exact_task_set_and_boundary_selector() -> None:
    tasks = _tasks()
    representative = deterministic_representative_sample(
        tasks,
        sample_size=2,
        seed_sha256="a" * 64,
    )
    boundary = (CalibrationUnit(episode_id="EP-A", observable_id="OBS-C"),)
    payload = CalibrationSamplingManifestPayload(
        parent_corpus_sha256="3" * 64,
        codebook_sha256="4" * 64,
        coding_procedure_sha256="5" * 64,
        task_set_sha256=sha256_json(tasks),
        representative_sampling_seed_sha256="a" * 64,
        representative_units=representative,
        boundary_units=boundary,
        boundary_selector_spec_sha256="6" * 64,
        created_at_utc=NOW,
    )
    artifact = build_calibration_sampling_manifest(payload, tasks=tasks)
    assert artifact.manifest_id == f"LPCS-{artifact.manifest_sha256[:20].upper()}"

    changed_tasks = (tasks[0].model_copy(update={"episode_title": "CHANGED"}), tasks[1])
    with pytest.raises(ValueError, match="does not bind exact structured task set"):
        build_calibration_sampling_manifest(payload, tasks=changed_tasks)

    with pytest.raises(ValueError, match="frozen selector specification"):
        CalibrationSamplingManifestPayload(
            **{
                **payload.model_dump(),
                "boundary_selector_spec_sha256": None,
            }
        )


def test_human_calibration_tasks_expose_only_selected_observables() -> None:
    tasks = _tasks()
    payload = CalibrationSamplingManifestPayload(
        parent_corpus_sha256="3" * 64,
        codebook_sha256="4" * 64,
        coding_procedure_sha256="5" * 64,
        task_set_sha256=sha256_json(tasks),
        representative_sampling_seed_sha256="a" * 64,
        representative_units=(
            CalibrationUnit(episode_id="EP-A", observable_id="OBS-B"),
            CalibrationUnit(episode_id="EP-B", observable_id="OBS-C"),
        ),
        created_at_utc=NOW,
    )
    manifest = build_calibration_sampling_manifest(payload, tasks=tasks)
    selected = human_calibration_tasks(tasks, manifest)
    assert [(row.episode_id, row.observable_ids) for row in selected] == [
        ("EP-A", ("OBS-B",)),
        ("EP-B", ("OBS-C",)),
    ]


def test_calibration_manifest_is_immutable(tmp_path: Path) -> None:
    tasks = _tasks()
    payload = CalibrationSamplingManifestPayload(
        parent_corpus_sha256="3" * 64,
        codebook_sha256="4" * 64,
        coding_procedure_sha256="5" * 64,
        task_set_sha256=sha256_json(tasks),
        representative_sampling_seed_sha256="a" * 64,
        representative_units=deterministic_representative_sample(
            tasks,
            sample_size=2,
            seed_sha256="a" * 64,
        ),
        created_at_utc=NOW,
    )
    artifact = build_calibration_sampling_manifest(payload, tasks=tasks)
    path = tmp_path / "calibration-sampling.json"
    write_calibration_sampling_manifest(path, artifact)
    assert stat.S_IMODE(path.stat().st_mode) == 0o400
    assert load_calibration_sampling_manifest(path) == artifact
    with pytest.raises(FileExistsError):
        write_calibration_sampling_manifest(path, artifact)
