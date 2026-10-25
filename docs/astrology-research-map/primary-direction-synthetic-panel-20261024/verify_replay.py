#!/usr/bin/env python3
"""Independently replay frozen synthetic inputs and compare full output bytes."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(ephemeris_dir: Path) -> None:
    script = HERE / "build_synthetic_panel.py"
    spec = importlib.util.spec_from_file_location("panel_reproduction", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen runner")
    build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build)
    plan = build.load_plan()
    frozen_inputs = build.verified_inputs(plan)
    result = build.run_panel(plan, frozen_inputs, ephemeris_dir)
    expected = {
        "SYNTHETIC_PANEL_COVERAGE.json": build.canonical(result["analysis"]),
        "SYNTHETIC_PANEL_EXPOSURES.json": build.canonical(result["exposures"]),
        "BIRTH_TIME_PERTURBATION.json": build.canonical(result["stability"]),
    }
    csv_output = io.StringIO(newline="")
    writer = csv.DictWriter(csv_output, fieldnames=list(result["chart_rows"][0]))
    writer.writeheader()
    writer.writerows(result["chart_rows"])
    expected["SYNTHETIC_PANEL_CHART_ROWS.csv"] = csv_output.getvalue()
    for name, content in expected.items():
        if (HERE / name).read_bytes() != content.encode("utf-8"):
            raise AssertionError("bitwise synthetic replay mismatch: " + name)
    evidence = {
        "schema": "PRIMARY_DIRECTION_SYNTHETIC_REPLAY_RECEIPT_V1",
        "source": "Strict local verified Swiss Ephemeris, no human outcomes",
        "frozen_plan_sha256": build.PLAN_SHA256,
        "code_sha256": digest(script),
        "frozen_inputs_sha256": digest(HERE / "SYNTHETIC_PANEL_INPUTS.json"),
        "replayed_case_count": len(frozen_inputs["synthetic_cases"]),
        "status": "4_OF_4_OUTPUTS_BIT_FOR_BIT_REPRODUCED",
        "files": {name: digest(HERE / name) for name in sorted(expected)},
        "human_predictive_validity": "UNTESTED",
    }
    dest = HERE / "REPLAY_VERIFICATION.json"
    if dest.exists():
        if json.loads(dest.read_text()) != evidence:
            raise FileExistsError("old replay receipt differs")
    else:
        dest.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print("Verified 4/4 complete outputs identical; 96 charts, 24 time-uncertainty cases")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris-dir", type=Path, required=True)
    main(parser.parse_args().ephemeris_dir)
