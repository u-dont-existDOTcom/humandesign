#!/usr/bin/env python3
"""Verify outcome-blind scoring tools without real human data or source files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest() -> dict[str, Any]:
    contract = json.loads((HERE / "BLIND_EVENT_SCORING_CONTRACT.json").read_text())
    if contract["schema"] != "WESTERN_LILLY_MODERN_EVENT_ONLY_BLIND_SCORE_ENGINEERING_V0":
        raise ValueError("frozen study source contract changed")
    source = contract["public_data_source_candidate"]
    if source["binary_acquired"] or source["first_raw_individual_event_read"]:
        raise ValueError("this experiment cannot be represented as event-blind")
    if contract["human_predictive_accuracy"] != "UNTESTED":
        raise ValueError("no actual human validation has been performed")
    expected = [
        HERE / "BLIND_EVENT_SCORING_CONTRACT.json",
        HERE / "README.md",
        HERE / "CONTINUATION_CHECKPOINT.md",
        HERE / "build_verification.py",
        ROOT / "src/hdmatch/astrology/western_event_only_scoring.py",
        ROOT / "src/hdmatch/astrology/western_birth_only_cohort.py",
        ROOT / "tests/unit/test_western_event_only_scoring.py",
        ROOT / "tests/unit/test_western_birth_only_cohort.py",
        ROOT
        / "docs/astrology-research-map/western-private-natal-bridge-20261025/METHOD_SCOPE.json",
        ROOT
        / (
            "docs/astrology-research-map/western-primary-direction-blind-pilot-20261025/"
            "PILOT_V0_METHOD_CONTRACT.json"
        ),
    ]
    if len(set(expected)) != len(expected):
        raise ValueError("duplicate evidence file")
    if not all(p.is_file() for p in expected):
        raise ValueError("source code, requirements or tests missing")
    hashes = {
        str(p.relative_to(ROOT)): {"sha256": sha(p), "bytes": p.stat().st_size}
        for p in sorted(expected)
    }
    return {
        "schema": "WESTERN_EVENT_ONLY_OUTCOME_BLIND_SCORER_VERIFICATION_V0",
        "root_owner_multi_tradition_result": "OPEN",
        "human_predictive_validity": "UNTESTED",
        "astro_databank_free_sample": "DISCOVERED_BINARY_NOT_DOWNLOADED",
        "population_generalizability": "NOT_ESTABLISHED",
        "actual_participants_or_events": 0,
        "read_any_real_event_nodes": False,
        "statistical_result": "SYNTHETIC_UNIT_TESTS_ONLY",
        "file_sha256": hashes,
    }


if __name__ == "__main__":
    output = HERE / "VERIFICATION.json"
    result = manifest()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("SOURCE_AND_SCORER_FILE_SHA256_MANIFEST", len(result["file_sha256"]))
