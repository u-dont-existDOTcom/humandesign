#!/usr/bin/env python3
"""Artifact-based completion gate for the bounded known-month/Model B milestone."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    findings: list[str] = []
    required = [
        ROOT / "pyproject.toml",
        ROOT / "src" / "hdmatch" / "cli.py",
        ROOT / "mappings" / "mapping_library_v1.json",
        ROOT / "mappings" / "model_a_manifest_v1.json",
        ROOT / "mappings" / "model_b_mapping_library_v1.json",
        ROOT / "mappings" / "model_b_unresolved_mapping_report_v1.json",
        ROOT / "reports" / "model_a_smoke_75" / "summary.json",
        ROOT / "reports" / "model_a_smoke_75" / "README.md",
        ROOT / "reports" / "model_b_structural_audit_2000" / "summary.json",
    ]
    for path in required:
        if not path.exists():
            findings.append(f"REQUIRED_ARTIFACT_MISSING:{path.relative_to(ROOT)}")
    smoke_path = ROOT / "reports" / "model_a_smoke_75" / "summary.json"
    if smoke_path.exists():
        smoke = json.loads(smoke_path.read_text(encoding="utf-8"))
        if smoke.get("model_id") != "MODEL-A-CORE-V1" or smoke.get("case_count") != 75:
            findings.append("MODEL_A_SMOKE_ID_OR_CASE_COUNT_INVALID")
        if smoke.get("pipeline_status") != "complete":
            findings.append("MODEL_A_SMOKE_NOT_COMPLETE")
        for metric in ("top_1", "top_3", "top_5", "mean_reciprocal_rank"):
            if metric not in smoke.get("metrics", {}):
                findings.append(f"MODEL_A_SMOKE_METRIC_MISSING:{metric}")
        for artifact in (
            "blind_cases.json",
            "leakage_audit.json",
            "run.manifest.json",
            "predictions.json",
            "prediction.freeze.json",
            "answer-key.reveal.json",
            "evaluation.json",
        ):
            if artifact not in smoke.get("artifact_sha256", {}):
                findings.append(f"MODEL_A_ARTIFACT_HASH_MISSING:{artifact}")

    model_b_path = ROOT / "mappings" / "model_b_mapping_library_v1.json"
    if model_b_path.exists():
        model_b = json.loads(model_b_path.read_text(encoding="utf-8"))
        if model_b.get("model_id") != "MODEL-B-DETAILED-V1":
            findings.append("MODEL_B_ID_INVALID")
        if model_b.get("base_model_id") != "MODEL-A-CORE-V1":
            findings.append("MODEL_B_BASE_ID_INVALID")
        if len(model_b.get("channel_catalog", ())) != 36:
            findings.append("MODEL_B_CHANNEL_CATALOG_INCOMPLETE")
        if len(model_b.get("structural_families", ())) != 7:
            findings.append("MODEL_B_STRUCTURAL_FAMILIES_INCOMPLETE")
        mappings = model_b.get("behavioral_mappings", ())
        if len(mappings) != 8 or any(item.get("status") != "unresolved" for item in mappings):
            findings.append("MODEL_B_UNRESOLVED_MAPPING_INVENTORY_INVALID")

    comparison_path = ROOT / "reports" / "model_b_structural_audit_2000" / "summary.json"
    if comparison_path.exists():
        comparison = json.loads(comparison_path.read_text(encoding="utf-8"))
        if comparison.get("answer_keys_used") is not False:
            findings.append("STRUCTURAL_AUDIT_ANSWER_KEY_BOUNDARY_INVALID")
        if comparison.get("behavioral_recovery_performed") is not False:
            findings.append("STRUCTURAL_AUDIT_CLAIM_BOUNDARY_INVALID")
        model_a_unique = comparison.get("model_a", {}).get("unique_structural_signatures", 0)
        model_b_unique = comparison.get("model_b", {}).get("unique_structural_signatures", 0)
        if model_b_unique < model_a_unique or model_a_unique <= 0:
            findings.append("STRUCTURAL_AUDIT_PARTITION_INVALID")

    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if tests.returncode != 0:
        findings.append("PYTEST_FAILED")
    if findings:
        for item in findings:
            print(item)
        print("TASK_STATUS: INCOMPLETE")
        return 1
    print("TASK_STATUS: READY_FOR_LOCAL_MERGE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
