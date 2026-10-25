#!/usr/bin/env python3
"""Integrity manifest for source-visible 1647 dignity research, not human validity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OMIT = {"VERIFICATION.json"}


def make_manifest() -> dict[str, Any]:
    summary = json.loads((HERE / "PARTIAL_DIGNITIES_SUMMARY.json").read_text())
    replay = json.loads((HERE / "DIGNITY_REPLAY_VERIFICATION.json").read_text())
    if summary["n_synthetic_charts"] != 96 or summary["n_planet_rows"] != 672:
        raise ValueError("synthetic chart counts changed")
    if summary["n_source_rule_contact_rows"] != 216:
        raise ValueError("historical rule contact crosswalk changed")
    if replay["status"] != "3_OF_3_OUTPUT_FILES_BITWISE_IDENTICAL":
        raise ValueError("full replay was not verified")
    if summary["full_radix_strength_verdicts"] != 0:
        raise ValueError("unsupported historical strong/not-strong claim introduced")
    files = [
        p
        for p in HERE.rglob("*")
        if p.is_file()
        and p.name not in OMIT
        and p.suffix != ".pyc"
        and "__pycache__" not in p.parts
    ]
    files.extend(
        [
            ROOT / "src/hdmatch/astrology/lilly_essential_dignity.py",
            ROOT / "tests/unit/test_lilly_essential_dignity.py",
        ]
    )
    digest = {
        str(p.relative_to(ROOT)): {
            "bytes": len(p.read_bytes()),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        }
        for p in sorted(files)
    }
    if sum("/original_1647_pages/" in name for name in digest) != 6:
        raise ValueError("missing 1647 first edition source images")
    return {
        "schema": "LILLY_1647_SOURCE_VISIBLE_DIGNITY_VERIFICATION_V1",
        "date": "2026-10-25",
        "source_precommit": "e5106235f787eb7150df425b4c1a5611c672da92",
        "parent_96_chart_commit": "97104a3513eb278e50ea05a22626b00b6f83d1d2",
        "n_synthetic_charts": 96,
        "n_planet_rows": 672,
        "n_contact_rows": 216,
        "human_predictive_accuracy": "UNTESTED",
        "full_historical_natal_strength": "UNRESOLVED",
        "replay": replay["status"],
        "files": digest,
    }


if __name__ == "__main__":
    path = HERE / "VERIFICATION.json"
    obj = make_manifest()
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + "\n")
    print("Verified source/provenance manifest files:", len(obj["files"]))
