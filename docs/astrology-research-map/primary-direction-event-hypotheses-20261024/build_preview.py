#!/usr/bin/env python3
"""Deterministic, synthetic-only candidate contact coverage diagnostic.

It MUST NOT read any real person's natal chart, outcomes or responses.
"""

from __future__ import annotations

import json
from pathlib import Path

from hdmatch.astrology.event_hypothesis_windows import project_unfrozen_candidate_windows

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SYNTHETIC = (
    ROOT
    / "docs/astrology-research-map/gansten-primary-timeline-20261024/examples"
    / "synthetic_2000_timeline.json"
)
CANDIDATES = HERE / "LILLY_1647_EVENT_CANDIDATES.json"
OUTPUT = HERE / "PRE_FREEZE_SYNTHETIC_EXPOSURE_DIAGNOSTIC.json"


def build() -> dict[str, object]:
    timeline = json.loads(SYNTHETIC.read_text(encoding="utf-8"))
    rules = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    output = project_unfrozen_candidate_windows(timeline, rules)
    output["input_fixture"] = "synthetic_2000_timeline.json, no human answers/events"
    output["candidate_registry"] = CANDIDATES.name
    output["no_optimization_undertaken"] = True
    return output


if __name__ == "__main__":
    outcome = build()
    OUTPUT.write_text(json.dumps(outcome, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("synthetic-only contact exposure groups:", outcome["unique_contact_exposure_groups"])
