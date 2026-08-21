#!/usr/bin/env python3
"""Artifact-based completion gate for the known-month initial milestone."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    findings: list[str] = []
    required = [
        ROOT / "pyproject.toml",
        ROOT / "src" / "hdmatch" / "cli.py",
        ROOT / "mappings" / "mapping_library_v1.json",
        ROOT / "reports" / "known_month_oracle_1000" / "report.json",
        ROOT / "reports" / "known_month_oracle_1000" / "failure_report.json",
        ROOT / "reports" / "known_month_oracle_1000" / "leakage_audit.json",
        ROOT / "reports" / "known_month_oracle_1000" / "freeze_record.json",
        ROOT / "reports" / "known_month_oracle_1000" / "evaluation.json",
    ]
    for path in required:
        if not path.exists():
            findings.append(f"REQUIRED_ARTIFACT_MISSING:{path.relative_to(ROOT)}")
    report_path = ROOT / "reports" / "known_month_oracle_1000" / "report.json"
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("case_count") != 1000:
            findings.append("ORACLE_CASE_COUNT_INVALID")
        for metric in ("top_1", "top_3", "top_5", "mrr"):
            if metric not in report.get("metrics", {}):
                findings.append(f"ORACLE_METRIC_MISSING:{metric}")
        if "ablation" not in report or "restoration" not in report:
            findings.append("ABLATION_RESTORATION_MISSING")
    tests = (
        subprocess.run(
            [str(ROOT / ".venv" / "bin" / "python"), "-m", "pytest"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if (ROOT / ".venv" / "bin" / "python").exists()
        else None
    )
    if tests is None:
        findings.append("PROJECT_VENV_MISSING")
    elif tests.returncode != 0:
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
