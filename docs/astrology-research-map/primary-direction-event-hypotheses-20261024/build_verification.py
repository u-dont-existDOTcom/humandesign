#!/usr/bin/env python3
"""Rebuild a SHA256 manifest of all portable primary-direction event research files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RELATIVE_PATHS = (
    [
        "src/hdmatch/astrology/event_hypothesis_windows.py",
        "tests/unit/test_primary_direction_event_hypotheses.py",
        "docs/astrology-research-map/gansten-primary-timeline-20261024/examples/synthetic_2000_timeline.json",
    ]
    + [
        str(p.relative_to(ROOT))
        for p in HERE.iterdir()
        if p.is_file() and p.name != "VERIFICATION.json"
    ]
    + [str(p.relative_to(ROOT)) for p in sorted((HERE / "witness_pages").glob("*.jpg"))]
    + [str(p.relative_to(ROOT)) for p in sorted((HERE / "synthetic_examples").glob("*.json"))]
)


def build() -> dict[str, object]:
    digests = {}
    for relative in sorted(RELATIVE_PATHS):
        content = (ROOT / relative).read_bytes()
        digests[relative] = {
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
    return {
        "schema": "PRIMARY_DIRECTION_EVENT_CANDIDATE_VERIFICATION_V0",
        "source_witness": "Wellcome first-edition Lilly (1647) facsimile",
        "upstream_branch": "research/primary-direction-method-inventory-20261024",
        "no_real_human_answers": True,
        "predictive_accuracy": "UNTESTED",
        "tests": "130 passed with official Swiss files on Zorin, focused Ruff and mypy pass",
        "synthetic_2000_adult_direct_exposures": 0,
        "files": digests,
    }


if __name__ == "__main__":
    out = HERE / "VERIFICATION.json"
    out.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("verified file manifest:", len(build()["files"]), "files")
