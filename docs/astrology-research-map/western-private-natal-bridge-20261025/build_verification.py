#!/usr/bin/env python3
"""Verify source-file provenance and published research adapter artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest() -> dict[str, Any]:
    contract = json.loads((HERE / "METHOD_SCOPE.json").read_text())
    if contract["stage"] != "ENGINEERING_SYNTHETIC_ONLY_NOT_LIVE_TRIAL_OR_PREDICTION_FREEZE":
        raise ValueError("research stage changed without study governance")
    if contract["human_predictive_accuracy"] != "UNTESTED":
        raise ValueError("synthetic work cannot certify human validity")
    for name, expected in (
        (
            "LILLY_1647_EVENT_CANDIDATES.json",
            "66719c3ba3f8c3877b3684b30fb8c31537d56a33ae95909be348246374d42c87",
        ),
        (
            "ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json",
            "dc219e072bd03835c3e6527a41a70680bd24197d1e0840a6250495f33e4ae11d",
        ),
    ):
        file = (
            ROOT / "docs/astrology-research-map/primary-direction-event-hypotheses-20261024" / name
        )
        if digest(file) != expected:
            raise ValueError("original source anchor changed: " + name)
    required = [
        HERE / "METHOD_SCOPE.json",
        HERE / "README.md",
        HERE / "CONTINUATION_CHECKPOINT.md",
        HERE / "build_verification.py",
        ROOT / "src/hdmatch/astrology/western_private_natal_bridge.py",
        ROOT / "tests/unit/test_western_private_natal_bridge.py",
    ]
    if len(set(required)) != len(required) or not all(path.is_file() for path in required):
        raise ValueError("research packet is missing source or test files")
    return {
        "schema": "WESTERN_PRIVATE_NATAL_BRIDGE_RESEARCH_VERIFICATION_V0",
        "study_status": "SYNTHETIC_ENGINEERING_NO_REAL_PARTICIPANTS",
        "ephemeris_mode_integration": "STRICT_SWIEPH_PINNED_LOCAL_FILES",
        "historical_source_completeness": "NOT_COMPLETE_LILLY_OR_ARGOLUS",
        "private_input_exposure": "NO_REAL_BIRTH_RECORDS_USED",
        "human_predictive_validity": "UNTESTED",
        "owner_multi_tradition_forward_blind_goal": "OPEN",
        "file_sha256": {
            str(path.relative_to(ROOT)): {"sha256": digest(path), "bytes": path.stat().st_size}
            for path in sorted(required)
        },
    }


if __name__ == "__main__":
    receipt = manifest()
    output = HERE / "VERIFICATION.json"
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("VERIFIED_RESEARCH_FILES", len(receipt["file_sha256"]))
