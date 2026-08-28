from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

from hdmatch.evaluation.survey_v2_noise import DEFAULT_NOISE_SCENARIOS
from hdmatch.util.canonical import sha256_json


def _runner() -> ModuleType:
    path = Path(__file__).parents[2] / "scripts" / "audit_survey_v2_noise.py"
    spec = importlib.util.spec_from_file_location("audit_survey_v2_noise", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checkpoint_round_trip_and_identity_guard(tmp_path: Path) -> None:
    runner = _runner()
    scenario = DEFAULT_NOISE_SCENARIOS[0].model_dump(mode="json")
    checkpoint = {
        "schema_version": "survey-v2-noise-scenario-checkpoint-v1",
        "run_identity_sha256": "run-a",
        "scenario": scenario,
        "summary": {"scenario_id": "perfect_answers"},
        "diagnostics": {},
    }
    checkpoint["checkpoint_content_sha256"] = sha256_json(checkpoint)
    path = tmp_path / "perfect_answers.json"

    runner._write_json_atomic(path, checkpoint)

    assert runner._load_checkpoint(
        path, run_identity_sha256="run-a", scenario=scenario
    ) == checkpoint
    with pytest.raises(ValueError, match="run identity mismatch"):
        runner._load_checkpoint(path, run_identity_sha256="run-b", scenario=scenario)


def test_tampered_checkpoint_is_rejected(tmp_path: Path) -> None:
    runner = _runner()
    scenario = DEFAULT_NOISE_SCENARIOS[0].model_dump(mode="json")
    checkpoint = {
        "run_identity_sha256": "run-a",
        "scenario": scenario,
        "summary": {},
        "diagnostics": {},
        "checkpoint_content_sha256": "not-the-content-hash",
    }
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(checkpoint), encoding="utf-8")

    with pytest.raises(ValueError, match="content hash mismatch"):
        runner._load_checkpoint(path, run_identity_sha256="run-a", scenario=scenario)


def test_status_and_partial_report_are_machine_readable(tmp_path: Path) -> None:
    runner = _runner()
    status_path = tmp_path / "status.json"
    partial_path = tmp_path / "partial-report.json"

    runner._write_status(
        status_path,
        state="running",
        scenario_id="wrong_05pct",
        completed_scenarios=["perfect_answers"],
        selected_scenario_count=2,
        completed_cases=10_000,
        total_cases=288_938,
        elapsed_seconds=12.5,
        estimated_remaining_seconds=348.6,
    )
    runner._write_partial_report(
        partial_path,
        run_identity={"git_commit_sha": "abc"},
        run_identity_sha256="run-a",
        completed_scenarios=["perfect_answers"],
        selected_scenario_count=2,
        summaries=[{"scenario_id": "perfect_answers"}],
        diagnostics={"perfect_answers": {}},
    )

    status = json.loads(status_path.read_text(encoding="utf-8"))
    partial = json.loads(partial_path.read_text(encoding="utf-8"))
    assert status["completed_cases"] == 10_000
    assert status["state"] == "running"
    assert partial["is_complete"] is False
    stored_hash = partial.pop("report_content_sha256")
    assert stored_hash == sha256_json(partial)
