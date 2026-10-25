#!/usr/bin/env python3
"""Replay all frozen reception/chart arithmetic without human outcomes."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_module() -> Any:
    script = HERE / "build_reception_inventory.py"
    spec = importlib.util.spec_from_file_location("lilly_fixed_receptions", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("can't load first-edition reception generator")
    program = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(program)
    return program


def replay() -> dict[str, Any]:
    program = source_module()
    new = program.build()
    hashes = {}
    for key, filename in sorted(program.OUTPUTS.items()):
        path = HERE / filename
        recalculated = program.canonical(new[key]).encode("utf-8")
        if path.read_bytes() != recalculated:
            raise AssertionError("fixed 96-chart output mismatch: " + filename)
        hashes[filename] = digest(path)
    summary = new["summary"]
    assert summary["n_synthetic_charts"] == 96
    assert summary["n_prior_planet_rows"] == 672
    assert summary["n_prior_source_rule_contacts"] == 216
    assert summary["n_unordered_reception_pairs"] == 462
    assert summary["n_same_mode_reception_pairs"] == 172
    assert summary["mc_jupiter_contacts_with_any_same_mode"] == 19
    assert summary["mc_jupiter_contacts_with_dom_or_exaltation_reception"] == 8
    assert summary["full_lilly_radix_strength_verdicts"] == 0
    return {
        "schema": "LILLY_1647_RECEPTION_SYNTHETIC_FULL_REPLAY_V1",
        "status": "FOUR_OF_FOUR_COMPLETE_SOURCE_DATA_OUTPUTS_BYTE_IDENTICAL",
        "source_precommit": "286bbc5",
        "program_sha256": digest(HERE / "build_reception_inventory.py"),
        "frozen_contract_sha256": digest(HERE / "RECEPTION_ORIENTATION_PRECOMMIT.json"),
        "n_original_synthetic_charts": 96,
        "n_original_event_candidate_contacts": 216,
        "historically_scoreable_jupiter_predictions": 0,
        "human_predictive_accuracy": "UNTESTED",
        "file_sha256": hashes,
    }


if __name__ == "__main__":
    result = replay()
    output = HERE / "RECEPTION_REPLAY_VERIFICATION.json"
    content = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output.exists() and output.read_text() != content:
        raise ValueError("prior replay receipt does not agree")
    if not output.exists():
        output.write_text(content, encoding="utf-8")
    print(result["status"], result["n_original_synthetic_charts"], "charts")
