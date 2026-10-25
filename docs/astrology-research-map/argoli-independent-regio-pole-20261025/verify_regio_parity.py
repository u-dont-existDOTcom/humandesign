#!/usr/bin/env python3
"""Replay both fixed mathematical panels and verify primary witness integrity."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def build_module() -> Any:
    p = HERE / "build_regio_parity.py"
    spec = importlib.util.spec_from_file_location("regio_math_parity_generator", p)
    if spec is None or spec.loader is None:
        raise RuntimeError("mathematical parity module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay() -> dict[str, Any]:
    generator = build_module()
    computed = generator.build()
    output = HERE / "POSITION_CIRCLE_PARITY_REPORT.json"
    if output.read_bytes() != generator.canonical(computed).encode("utf-8"):
        raise AssertionError("full mathematical parity result not bitwise reproducible")
    sample = computed["new_fixed_800_seed20261026"]
    if sample["synthetic_coordinate_cases"] != 800:
        raise AssertionError("holdout size not frozen")
    if sample["cases_exceeding_1e_minus_8_deg"]:
        raise AssertionError("independent mathematical formula failed fixed holdout")
    original = (
        HERE
        / "primary_1667_volume"
        / "Andrea_Argoli_Primi_Mobilis_Tabulae_1667_original_partial_volume.pdf"
    )
    if digest(original) != "b3f93054d64c3ca4318ffaec84e8b7161cdc79d6474bb300efd10787b743df1d":
        raise AssertionError("original Argoli scan changed")
    return {
        "schema": "ARGOLI_REGIO_MATH_INDEPENDENT_REPLAY_V1",
        "status": "TWO_OF_TWO_PANELS_BITWISE_REPRODUCIBLE",
        "initial_source_method_commit": "3e6b17ece6936b5d413787ba8be54414e8fc0145",
        "n_development_geometries": 1200,
        "n_later_precommitted_holdout_geometries": 800,
        "max_angular_error_degrees": sample["max_circular_arc_error_degrees"],
        "source_pdf_sha256": digest(original),
        "contract_sha256": digest(HERE / "REGIO_INDEPENDENT_PARITY_PRECOMMIT.json"),
        "script_sha256": digest(HERE / "build_regio_parity.py"),
        "report_sha256": digest(output),
        "human_prediction_validation": "UNTESTED",
        "exact_1610_Argoli_authentication": False,
    }


def manifest() -> dict[str, Any]:
    receipt = replay()
    extra = [
        ROOT / "src/hdmatch/astrology/regio_pole_independent.py",
        ROOT / "tests/unit/test_regio_pole_independent.py",
    ]
    files = sorted(
        [
            f
            for f in HERE.rglob("*")
            if f.is_file()
            and f.name != "VERIFICATION.json"
            and f.suffix != ".pyc"
            and "__pycache__" not in f.parts
        ]
        + extra
    )
    hashes = {
        str(file.relative_to(ROOT)): {
            "bytes": file.stat().st_size,
            "sha256": digest(file),
        }
        for file in files
    }
    if sum("/primary_1667_pages/" in path for path in hashes) != 3:
        raise ValueError("three source text plate images required")
    if sum("/primary_1667_volume/" in path for path in hashes) != 1:
        raise ValueError("original PDF source missing")
    return {
        "schema": "ARGOLI_INDEPENDENT_MATH_SOURCE_INTEGRITY_V1",
        "replay": receipt,
        "historical_exactness": "PARTIAL_FAMILY_ONLY_1610_NOT_ESTABLISHED",
        "human_predictive_accuracy": "UNTESTED",
        "file_hashes": hashes,
    }


if __name__ == "__main__":
    result = manifest()
    output = HERE / "VERIFICATION.json"
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output.exists() and output.read_text() != text:
        raise ValueError("prior verified file set mutated")
    if not output.exists():
        output.write_text(text, encoding="utf-8")
    print("Full parity replay and source digests verified:", len(result["file_hashes"]), "files")
