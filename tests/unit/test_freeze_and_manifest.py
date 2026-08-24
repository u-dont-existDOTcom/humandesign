from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.leakage import LeakageDetectedError
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.experiments.freeze import (
    ArtifactBindings,
    FreezeVerificationError,
    freeze_predictions,
    verify_frozen_predictions,
)
from hdmatch.experiments.manifest import (
    create_run_manifest,
    load_run_manifest,
    verify_run_manifest_resume,
    write_run_manifest,
)


def _digest(label: str) -> str:
    return sha256_bytes(label.encode())


def _bindings() -> ArtifactBindings:
    return ArtifactBindings(
        blind_input_sha256=_digest("blind"),
        model_sha256=_digest("model"),
        question_bank_sha256=_digest("questions"),
        mapping_sha256=_digest("mapping"),
    )


def test_canonical_json_and_exact_file_hash_are_distinct_contracts(tmp_path: Path) -> None:
    first = {"z": [2, 1], "a": "é"}
    second = {"a": "é", "z": [2, 1]}
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert sha256_json(first) == sha256_json(second)

    pretty = tmp_path / "pretty.json"
    pretty.write_text(json.dumps(first, indent=2), encoding="utf-8")
    canonical = tmp_path / "canonical.json"
    write_new_canonical_json(canonical, first)
    assert sha256_file(pretty) != sha256_file(canonical)
    with pytest.raises(FileExistsError):
        write_new_canonical_json(canonical, first)
    with pytest.raises(ValueError, match="non-finite"):
        canonical_json_bytes({"score": float("nan")})


def test_manifest_records_hashes_commit_environment_and_is_immutable(tmp_path: Path) -> None:
    manifest = create_run_manifest(
        experiment_id="EXP-1",
        seed=42,
        repository_root=Path(__file__).parents[2],
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_mean",
        model_id="symbolic-v1",
        input_hashes={"blind_input": _digest("blind")},
        config={"seed": 42},
        declared_outputs=("predictions.json",),
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )
    destination = tmp_path / "manifest.json"
    write_run_manifest(manifest, destination)
    stored = json.loads(destination.read_bytes())
    assert stored["software_commit"]
    assert stored["reveal_status"] == "blind"
    assert stored["config_payload"] == {"seed": 42}
    assert stored["config_sha256"] == sha256_json({"seed": 42})
    assert "python_version" in stored["software_environment"]
    assert load_run_manifest(destination) == manifest
    with pytest.raises(FileExistsError):
        write_run_manifest(manifest, destination)


def test_manifest_resume_requires_exact_recovery_configuration() -> None:
    config = {
        "aggregation": "duration_weighted_evidence",
        "threshold_rubric_bits": 0.0,
        "workers": 2,
        "cache_policy": "hash-bound exact month universes",
    }
    manifest = create_run_manifest(
        experiment_id="EXP-RESUME",
        seed=42,
        repository_root=Path(__file__).parents[2],
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id="MODEL-A-CORE-V1",
        input_hashes={"blind_cases.json": _digest("blind")},
        config=config,
    )
    verify_run_manifest_resume(
        manifest,
        experiment_id="EXP-RESUME",
        seed=42,
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id="MODEL-A-CORE-V1",
        input_hashes={"blind_cases.json": _digest("blind")},
        config=config,
    )

    with pytest.raises(ValueError, match="config_payload"):
        verify_run_manifest_resume(
            manifest,
            experiment_id="EXP-RESUME",
            seed=42,
            candidate_universe="known_month",
            aggregation_rule="duration_weighted_evidence",
            model_id="MODEL-A-CORE-V1",
            input_hashes={"blind_cases.json": _digest("blind")},
            config={**config, "workers": 3},
        )
    with pytest.raises(ValueError, match="aggregation_rule"):
        verify_run_manifest_resume(
            manifest,
            experiment_id="EXP-RESUME",
            seed=42,
            candidate_universe="known_month",
            aggregation_rule="best_state",
            model_id="MODEL-A-CORE-V1",
            input_hashes={"blind_cases.json": _digest("blind")},
            config=config,
        )


def test_freeze_binds_exact_prediction_bytes_and_all_inputs(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    predictions = run_dir / "predictions.json"
    predictions.write_bytes(b'{"predictions":[]}')
    record = freeze_predictions(
        run_dir,
        experiment_id="EXP-1",
        bindings=_bindings(),
        repository_root=Path(__file__).parents[2],
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )
    assert record.prediction_sha256 == sha256_file(predictions)
    assert record.prediction_size_bytes == predictions.stat().st_size
    assert verify_frozen_predictions(run_dir, expected_bindings=_bindings()) == record
    with pytest.raises(FileExistsError):
        freeze_predictions(
            run_dir,
            experiment_id="EXP-1",
            bindings=_bindings(),
            repository_root=Path(__file__).parents[2],
        )

    predictions.write_bytes(b'{"predictions":[]}\n')
    with pytest.raises(FreezeVerificationError, match="length changed"):
        verify_frozen_predictions(run_dir)


def test_strict_freeze_verification_checks_exact_run_manifest_bytes(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "predictions.json").write_bytes(b'{"predictions":[]}')
    manifest_path = run_dir / "run.manifest.json"
    manifest = create_run_manifest(
        experiment_id="EXP-1",
        seed=42,
        repository_root=Path(__file__).parents[2],
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id="MODEL-A-CORE-V1",
        input_hashes={"blind_cases.json": _bindings().blind_input_sha256},
        config={
            "aggregation": "duration_weighted_evidence",
            "threshold_rubric_bits": 0.0,
            "workers": 1,
            "cache_policy": "hash-bound exact month universes",
        },
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )
    write_run_manifest(manifest, manifest_path)
    record = freeze_predictions(
        run_dir,
        experiment_id="EXP-1",
        bindings=_bindings(),
        repository_root=Path(__file__).parents[2],
        run_manifest_path=manifest_path,
        created_at_utc=datetime(2026, 8, 21, 0, 1, tzinfo=UTC),
    )

    assert verify_frozen_predictions(run_dir, require_run_manifest=True) == record
    manifest_path.write_bytes(manifest_path.read_bytes() + b"\n")
    assert verify_frozen_predictions(run_dir) == record
    with pytest.raises(FreezeVerificationError, match="run-manifest bytes changed"):
        verify_frozen_predictions(run_dir, require_run_manifest=True)

    manifest_path.unlink()
    with pytest.raises(FreezeVerificationError, match="path escapes or is absent"):
        verify_frozen_predictions(run_dir, require_run_manifest=True)


def test_freeze_refuses_manifest_timestamp_after_prediction_freeze(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "predictions.json").write_bytes(b'{"predictions":[]}')
    manifest = create_run_manifest(
        experiment_id="EXP-1",
        seed=42,
        repository_root=Path(__file__).parents[2],
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id="MODEL-A-CORE-V1",
        input_hashes={"blind_cases.json": _bindings().blind_input_sha256},
        config={"aggregation": "duration_weighted_evidence"},
        created_at_utc=datetime(2026, 8, 21, 0, 2, tzinfo=UTC),
    )
    manifest_path = run_dir / "run.manifest.json"
    write_run_manifest(manifest, manifest_path)

    with pytest.raises(FreezeVerificationError, match="predates its run manifest"):
        freeze_predictions(
            run_dir,
            experiment_id="EXP-1",
            bindings=_bindings(),
            repository_root=Path(__file__).parents[2],
            run_manifest_path=manifest_path,
            created_at_utc=datetime(2026, 8, 21, 0, 1, tzinfo=UTC),
        )


def test_manifest_rejects_config_payload_hash_mismatch(tmp_path: Path) -> None:
    manifest = create_run_manifest(
        experiment_id="EXP-1",
        seed=42,
        repository_root=Path(__file__).parents[2],
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id="MODEL-A-CORE-V1",
        input_hashes={"blind_cases.json": _digest("blind")},
        config={"workers": 1},
    )
    raw = manifest.model_dump(mode="json")
    raw["config_payload"] = {"workers": 2}
    path = tmp_path / "run.manifest.json"
    write_new_canonical_json(path, raw)

    with pytest.raises(ValueError, match="invalid or non-canonical run manifest"):
        load_run_manifest(path)


def test_strict_freeze_verification_rejects_legacy_unbound_manifest(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "predictions.json").write_bytes(b'{"predictions":[]}')
    record = freeze_predictions(
        run_dir,
        experiment_id="EXP-1",
        bindings=_bindings(),
        repository_root=Path(__file__).parents[2],
    )

    assert verify_frozen_predictions(run_dir) == record
    with pytest.raises(FreezeVerificationError, match="lacks a run-manifest binding"):
        verify_frozen_predictions(run_dir, require_run_manifest=True)


def test_freeze_refuses_predictions_outside_run(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    outside = tmp_path / "predictions.json"
    outside.write_bytes(b"{}")
    with pytest.raises(ValueError, match="inside the run"):
        freeze_predictions(
            run_dir,
            experiment_id="EXP",
            bindings=_bindings(),
            repository_root=Path(__file__).parents[2],
            prediction_path=outside,
        )


def test_freeze_refuses_truth_derived_fields_in_blind_predictions(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    write_new_canonical_json(
        run_dir / "predictions.json",
        {
            "schema_version": "predictions-v1",
            "predictions": [
                {
                    "case_id": "C1",
                    "zero_cluster_rank": 31,
                    "true_date_rank": 1,
                    "true_local_date": "2000-01-02",
                    "hidden_utc": "2000-01-02T00:00:00Z",
                }
            ],
        },
    )
    with pytest.raises(LeakageDetectedError):
        freeze_predictions(
            run_dir,
            experiment_id="EXP",
            bindings=_bindings(),
            repository_root=Path(__file__).parents[2],
        )
    assert not (run_dir / "prediction.freeze.json").exists()
