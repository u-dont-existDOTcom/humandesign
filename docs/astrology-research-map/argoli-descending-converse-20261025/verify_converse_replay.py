#!/usr/bin/env python3
"""Byte-for-byte reproducibility of original source and two geometry panels.

Synthetic coordinates only; this audit does not ingest natal or human outcomes.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module() -> Any:
    source = HERE / "build_converse_comparison.py"
    specification = importlib.util.spec_from_file_location("argoli_fixed_replay", source)
    if specification is None or specification.loader is None:
        raise RuntimeError("unable to load fixed source-converse generator")
    obj = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(obj)
    return obj


def replay() -> dict[str, Any]:
    engine = module()
    computed, rows = engine.build()
    expected_report = engine.canonical(computed).encode("utf-8")
    report_path = HERE / "CONVERSE_SOURCE_AND_GEOMETRY_REPORT.json"
    if report_path.read_bytes() != expected_report:
        raise AssertionError("source/converse report is not byte-for-byte reproducible")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    csv_path = HERE / "CONVERSE_SYNTHETIC_COORDINATE_CASES.csv"
    if csv_path.read_bytes() != buffer.getvalue().encode("utf-8"):
        raise AssertionError("900-case source geometry CSV differs from independent replay")
    initial = computed["development"]
    held = computed["mathematical_holdout"]
    if initial["n"] != 500 or held["n"] != 400:
        raise ValueError("synthetic development/holdout allocation changed")
    if held["n_disagree_over_one_degree"] != 277:
        raise ValueError("400-case post-commit geometry result differs")
    if held["n_disagree_over_five_degrees"] != 148:
        raise ValueError("400-case five-degree disagreement count differs")
    return {
        "schema": "ARGOLI_1610_CONVERSE_REPLAY_V1",
        "status": "TWO_OF_TWO_OUTPUT_FILES_BITWISE_IDENTICAL",
        "fixed_source_and_math_precommit": "b7eb138099aba840edd4dc748241ad41a5d8dec8",
        "development_cases": initial["n"],
        "subsequent_mathematical_holdout_cases": held["n"],
        "holdout_over_one_degree": held["n_disagree_over_one_degree"],
        "holdout_over_five_degrees": held["n_disagree_over_five_degrees"],
        "holdout_median_degree_difference": held["median_absolute_difference_deg"],
        "holdout_maximum_degree_difference": held["maximum_absolute_difference_deg"],
        "contract_sha256": sha(HERE / "SOURCE_METHOD_ALIGNMENT.json"),
        "generator_sha256": sha(HERE / "build_converse_comparison.py"),
        "output_sha256": {
            report_path.name: sha(report_path),
            csv_path.name: sha(csv_path),
        },
        "human_predictive_accuracy": "UNTESTED",
        "full_historical_argoli_converse_authenticated": False,
    }


if __name__ == "__main__":
    result = replay()
    dest = HERE / "REPLAY_VERIFICATION.json"
    text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if dest.exists() and dest.read_text() != text:
        raise FileExistsError("old independent replay record differs")
    if not dest.exists():
        dest.write_text(text)
    print(result["status"], "500 development + 400 post-commit holdout")
