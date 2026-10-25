#!/usr/bin/env python3
"""Complete immutable file checksum inventory for first-edition reception audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def build() -> dict[str, Any]:
    summary = json.loads((HERE / "RECEPTION_SYNTHETIC_SUMMARY.json").read_text())
    replay = json.loads((HERE / "RECEPTION_REPLAY_VERIFICATION.json").read_text())
    if summary["n_synthetic_charts"] != 96:
        raise ValueError("synthetic sample changed")
    if summary["n_same_mode_reception_pairs"] != 172:
        raise ValueError("source-scoped reception classification changed")
    if summary["mixed_only_pairs_not_history_scored"] != 290:
        raise ValueError("unresolved mixed-only statuses changed")
    if summary["full_lilly_radix_strength_verdicts"] != 0:
        raise ValueError("unlicensed source-strength classification")
    if replay["status"] != "FOUR_OF_FOUR_COMPLETE_SOURCE_DATA_OUTPUTS_BYTE_IDENTICAL":
        raise ValueError("unverified replay")
    files = [
        f
        for f in HERE.rglob("*")
        if f.is_file()
        and f.name != "VERIFICATION.json"
        and f.suffix != ".pyc"
        and "__pycache__" not in f.parts
    ]
    files.extend(
        [
            ROOT / "src/hdmatch/astrology/lilly_reception.py",
            ROOT / "src/hdmatch/astrology/lilly_angle_progression.py",
            ROOT / "tests/unit/test_lilly_reception_orientation_1647.py",
        ]
    )
    hashes = {
        str(path.relative_to(ROOT)): {
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(files)
    }
    original_images = [
        name for name in hashes if "/witness_pages/" in name and name.endswith(".jpg")
    ]
    if len(original_images) != 5:
        raise ValueError("original first-edition witnesses incomplete")
    return {
        "schema": "LILLY_1647_RECEPTION_ORIENTATION_VERIFICATION_V1",
        "date": "2026-10-25",
        "branch": "research/primary-direction-reception-orientation-20261025",
        "source_method_precommit": "286bbc5",
        "n_frozen_synthetic_charts": 96,
        "n_previous_source_direction_contacts": 216,
        "n_mathematical_reciprocal_pairs": 462,
        "n_same_type_reciprocal_pairs": 172,
        "n_mixed_only_unresolved_pairs": 290,
        "new_original_witness_pages": [112, 510, 511, 515, 517],
        "replay": replay["status"],
        "human_predictive_validity": "UNTESTED",
        "full_Argolus_method_authenticated": False,
        "complete_Jupiter_natal_strength_authenticated": False,
        "files": hashes,
    }


if __name__ == "__main__":
    output = HERE / "VERIFICATION.json"
    rec = build()
    output.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n")
    print("Verified", len(rec["files"]), "source/analysis files")
