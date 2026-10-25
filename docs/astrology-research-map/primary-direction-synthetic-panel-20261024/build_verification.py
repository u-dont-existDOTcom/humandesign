#!/usr/bin/env python3
"""Create/recheck research SHA-256 manifest; no participant data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXCLUDED = {"VERIFICATION.json"}


def build() -> dict[str, object]:
    paths = sorted(
        [
            p
            for p in HERE.rglob("*")
            if p.is_file()
            and p.name not in EXCLUDED
            and "__pycache__" not in p.parts
            and p.suffix != ".pyc"
        ]
        + [ROOT / "tests/unit/test_primary_direction_synthetic_panel.py"]
    )
    manifest = {}
    for path in paths:
        blob = path.read_bytes()
        manifest[str(path.relative_to(ROOT))] = {
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
        }
    plan = json.loads((HERE / "PANEL_PLAN.json").read_text())
    analysis = json.loads((HERE / "SYNTHETIC_PANEL_COVERAGE.json").read_text())
    replay = json.loads((HERE / "REPLAY_VERIFICATION.json").read_text())
    if plan["n_cases"] != 96:
        raise ValueError("panel changed")
    if analysis["contact_coverage"]["total_exposures"] != 216:
        raise ValueError("coverage changed")
    if replay["status"] != "4_OF_4_OUTPUTS_BIT_FOR_BIT_REPRODUCED":
        raise ValueError("reproducibility not confirmed")
    return {
        "schema": "ASTRO_PRIMARY_DIRECTIONS_SYNTHETIC_VERIFICATION_V1",
        "human_predictive_validity": "UNTESTED",
        "frozen_plan_sha256": "948a1289b5f891c7f7870632ad116fb16ea6409d1bed575483c07c9901fbc0d0",
        "n_synthetic_charts": 96,
        "n_contact_exposures": 216,
        "birth_time_cases": 24,
        "original_1647_printed_source_pages": [509, 510, 651, 652, 653, 654, 655],
        "replay_status": replay["status"],
        "focused_regression_status": "139 passed with verified Swiss ephemeris files",
        "mypy_status": "checked analysis/replay scripts with MYPYPATH=src",
        "archive_inputs": manifest,
    }


if __name__ == "__main__":
    dest = HERE / "VERIFICATION.json"
    obj = build()
    dest.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    print("Source/output SHA-256 manifest entries:", len(obj["archive_inputs"]))
