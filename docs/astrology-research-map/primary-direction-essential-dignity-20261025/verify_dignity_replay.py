#!/usr/bin/env python3
"""Full independent 96-chart recomputation against the source-visible output bytes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "build_source_visible_dignities.py"


def source_module() -> Any:
    spec = importlib.util.spec_from_file_location("fixed_dignity_research", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import the frozen source reconstruction")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(ephemeris_dir: Path) -> dict[str, Any]:
    mod = source_module()
    result = mod.compute(ephemeris_dir)
    csv_text = io.StringIO(newline="")
    headers = [
        "chart_id",
        "planet",
        "chart_sect",
        "sign",
        "term_ruler",
        "face_ruler",
        "dignities",
        "debilities",
        "positive_points",
        "negative_points",
        "partial_net_points",
        "placidus_house",
        "fractional_house",
        "isolated_house_points",
        "house_angular",
        "full_natal_strength",
    ]
    writer = csv.DictWriter(csv_text, fieldnames=headers)
    writer.writeheader()
    for record in result["planet_rows"]:
        row = dict(record)
        for key in ("dignities", "debilities"):
            row[key] = "|".join(row[key])
        writer.writerow(row)
    payloads = {
        "PARTIAL_DIGNITIES_SUMMARY.json": mod.canonical(result["summary"]),
        "PARTIAL_DIGNITIES_PLANET_ROWS.csv": csv_text.getvalue(),
        "PARTIAL_DIGNITIES_CONTACT_CROSSWALK.json": mod.canonical(result["contact_rows"]),
    }
    for name, content in payloads.items():
        if (HERE / name).read_bytes() != content.encode("utf-8"):
            raise AssertionError("synthetic dignity byte-for-byte mismatch: " + name)
    return {
        "schema": "LILLY_1647_PARTIAL_DIGNITY_INDEPENDENT_REPLAY_V1",
        "status": "3_OF_3_OUTPUT_FILES_BITWISE_IDENTICAL",
        "source_code_sha256": digest(SOURCE),
        "precommitted_contract_sha256": digest(HERE / "DIGNITY_PRE_FREEZE_CONTRACT.json"),
        "n_synthetic_charts": 96,
        "n_partial_planet_records": 672,
        "n_source_rule_contact_joins": 216,
        "human_outcomes_used": False,
        "full_natal_strength_verified": False,
        "files": {k: digest(HERE / k) for k in sorted(payloads)},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris-dir", type=Path, required=True)
    receipt = replay(parser.parse_args().ephemeris_dir)
    file = HERE / "DIGNITY_REPLAY_VERIFICATION.json"
    if file.exists():
        if json.loads(file.read_text()) != receipt:
            raise ValueError("existing replay provenance differs")
    else:
        file.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("3 of 3 source-visible files reproduced exactly, 96 charts")
