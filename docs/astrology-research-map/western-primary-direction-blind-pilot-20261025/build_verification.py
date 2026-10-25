#!/usr/bin/env python3
"""Reverify prior synthetic inputs, modern diagnostic feasibility and code hashes."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict[str, Any]:
    manifest = json.loads((HERE / "PILOT_V0_METHOD_CONTRACT.json").read_text())
    if manifest["schema"] != "WESTERN_MODERN_PRIMARY_DIRECTION_BLIND_PILOT_DESIGN_V0":
        raise ValueError("pilot method contract was replaced")
    if manifest["human_predictive_accuracy"] != "UNTESTED":
        raise ValueError("human predictive status must remain untested")
    script = HERE / "build_synthetic_pilot_feasibility.py"
    spec = importlib.util.spec_from_file_location("frozen_synthetic_pilot_check", script)
    if spec is None or spec.loader is None:
        raise ValueError("pilot feasibility generator unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    actual = module.canonical(module.build())
    saved = HERE / "SYNTHETIC_PILOT_FEASIBILITY.json"
    if saved.read_bytes() != actual:
        raise ValueError("known synthetic feasibility cannot be reproduced")
    result = json.loads(actual)
    if result["existing_frozen_96_synthetic_charts"] != 96:
        raise ValueError("unexpected synthetic natal cohort size")
    if sum(result["tentative_two_occupational_contact_counts"].values()) != 20:
        raise ValueError("source selection or original contacts changed")
    if result["status"] != "PRIOR_96_CHART_DEVELOPMENT_ONLY_NOT_PROSPECTIVE_VALIDATION":
        raise ValueError("invalid predictive validity status")

    files = [
        p for p in HERE.rglob("*")
        if p.is_file() and p.name != "VERIFICATION.json"
        and "__pycache__" not in p.parts and p.suffix != ".pyc"
    ]
    files.extend([
        ROOT / "src/hdmatch/astrology/western_forward_blind.py",
        ROOT / "tests/unit/test_western_direction_forward_blind.py",
    ])
    hashes = {
        str(path.relative_to(ROOT)): {"sha256":sha(path),"bytes":path.stat().st_size}
        for path in sorted(files)
    }
    return {
        "schema":"WESTERN_DIRECTION_MODERN_DIAGNOSTIC_ENGINEERING_VERIFICATION_V0",
        "source_candidate_count":8,
        "tentative_modern_occupational_domains":2,
        "prior_synthetic_charts":96,
        "prior_all_source_contacts":216,
        "prior_tentative_occupational_contacts":20,
        "hypothetical_adult_age_occupancy_fraction":
            result["fraction_of_unconditional_age_interval_exposed"],
        "compatibility_source_age_windows_reproduced":True,
        "real_participants_or_events_used":False,
        "empirical_predictive_validity":"UNTESTED",
        "historically_complete_lilly_or_argoli":"UNRESOLVED",
        "actual_trial_ready":False,
        "file_hashes":hashes,
    }


if __name__ == "__main__":
    target=HERE/"VERIFICATION.json"
    result=build()
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("Verified fixed 96-chart source feasibility and",len(result["file_hashes"]),"files")
