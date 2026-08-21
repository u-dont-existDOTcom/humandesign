from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from hdmatch.model_b.mapping_library import FrozenModelB
from hdmatch.runtime.symbolic_adapter import FrozenSymbolicModel

ROOT = Path(__file__).parents[2]
AUDIT_PATH = ROOT / "mappings/model_b_detailed_v2_source_recovery_audit_v1.json"


def _load_object(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data, usedforsecurity=False).hexdigest()


def _load_acceptance_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "hdmatch_task_acceptance",
        ROOT / "scripts/task_acceptance.py",
    )
    if spec is None or spec.loader is None:
        raise AssertionError("task acceptance module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _successful_run(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    del kwargs
    return subprocess.CompletedProcess(args=args[0], returncode=0)


def test_surviving_source_provenance_matches_repository_files() -> None:
    audit = _load_object(AUDIT_PATH)
    provenance = cast(list[dict[str, Any]], audit["exact_surviving_provenance"])
    expected_paths = {
        "reference/core/behavioral_target_combined(5).md",
        "reference/core/human_design_search_instructions_fixed_candidate_blind(6).md",
        "reference/legacy_runs/hd_global_search_results.json",
        "reference/legacy_runs/hd_mapping_sensitivity.json",
    }

    assert {item["artifact"] for item in provenance} == expected_paths
    for item in provenance:
        data = (ROOT / cast(str, item["artifact"])).read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        assert _git_blob_sha1(data) == item["git_blob"]

    legacy_result = _load_object(ROOT / "reference/legacy_runs/hd_global_search_results.json")
    freeze = cast(dict[str, Any], legacy_result["freeze"])
    frozen_entries = {
        cast(str, item["legacy_freeze_field"]): item["sha256"]
        for item in provenance
        if item["legacy_freeze_field"] is not None
    }
    assert freeze["target_sha256"] == frozen_entries["target_sha256"]
    assert freeze["rubric_sha256"] == frozen_entries["rubric_sha256"]


def test_model_b_v2_is_uncompiled_and_behavioral_comparison_is_locked() -> None:
    audit = _load_object(AUDIT_PATH)
    conclusion = cast(dict[str, Any], audit["conclusion"])
    gate = cast(dict[str, Any], audit["model_and_benchmark_gate"])

    assert conclusion["model_b_detailed_v2_compiled"] is False
    assert conclusion["pre_search_mapping_definitions_recovered"] is False
    assert gate["model_b_detailed_v2"].startswith("not created")
    assert gate["behavioral_ab_benchmark_allowed"] is False

    compiled_model_ids = {
        payload["model_id"]
        for path in (ROOT / "mappings").glob("*.json")
        if "model_id" in (payload := _load_object(path))
    }
    assert "MODEL-B-DETAILED-V2" not in compiled_model_ids

    model_a = FrozenSymbolicModel(ROOT / "mappings/mapping_library_v1.json")
    model_b = FrozenModelB(
        ROOT / "mappings/model_b_mapping_library_v1.json",
        project_root=ROOT,
    )
    assert model_b.capability_metadata == {
        "behavioral_scoring": "model-a-base-only",
        "detailed_behavioral_mappings": "unresolved",
        "unresolved_detailed_mapping_count": 8,
    }
    assert model_b.library.sha256() == model_a.library.sha256()
    assert model_b.answer_spaces() == model_a.answer_spaces()


def test_structural_v1_is_not_accepted_as_full_model_b(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    audit = _load_object(AUDIT_PATH)
    gate = cast(dict[str, Any], audit["model_and_benchmark_gate"])
    structural = _load_object(ROOT / "reports/model_b_structural_audit_2000/summary.json")

    assert "not completion" in gate["model_b_structural_intermediate"]
    assert structural["comparison_kind"] == (
        "structural_resolution_upper_bound_not_behavioral_recovery"
    )
    assert structural["behavioral_recovery_performed"] is False
    assert structural["model_b"]["detailed_behavioral_mapping_status"] == "unresolved"

    task_acceptance = _load_acceptance_module()
    subprocess_module = cast(ModuleType, task_acceptance.subprocess)
    main = cast(Callable[[], int], task_acceptance.main)
    monkeypatch.setattr(subprocess_module, "run", _successful_run)
    assert main() == 0
    output = capsys.readouterr().out
    assert "MODEL_B_BEHAVIORAL_STATUS: structural-only-source-recovery-required" in output
    assert "FULL_MODEL_OBJECTIVE: NOT_EVALUATED_BY_THIS_GATE" in output
    assert "TASK_STATUS: INITIAL_ENGINEERING_MILESTONE_READY" in output
