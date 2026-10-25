#!/usr/bin/env python3
"""Source-image, method-registry and synthetic replay SHA-256 verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest() -> dict[str, Any]:
    registry = json.loads((HERE / "SOURCE_METHOD_ALIGNMENT.json").read_text())
    if registry["human_predictive_accuracy"] != "UNTESTED":
        raise ValueError("historical source audit cannot claim predictive accuracy")
    witnesses = registry["original_source_files"]
    if len(witnesses) != 11:
        raise ValueError("original print page witness count changed")
    for entry in witnesses:
        path = HERE / entry["path"]
        if path.stat().st_size != entry["bytes"] or sha(path) != entry["sha256"]:
            raise ValueError("source photograph/crop changed: " + entry["path"])
    replay = json.loads((HERE / "REPLAY_VERIFICATION.json").read_text())
    if replay["status"] != "TWO_OF_TWO_OUTPUT_FILES_BITWISE_IDENTICAL":
        raise ValueError("full deterministic replay not verified")
    if replay["fixed_source_and_math_precommit"] != ("b7eb138099aba840edd4dc748241ad41a5d8dec8"):
        raise ValueError("precommit bound to different historical method")
    parent_manifest = ROOT / registry["first_editions"]["1610"]["institutional_manifest"]
    if sha(parent_manifest) != registry["first_editions"]["1610"]["manifest_sha256"]:
        raise ValueError("original 1610 institutional manifest changed")
    parent_pdf = ROOT / registry["first_editions"]["1667"]["original_pdf"]
    if sha(parent_pdf) != registry["first_editions"]["1667"]["original_pdf_sha256"]:
        raise ValueError("original 1667 Michigan volume/excerpt changed")

    paths = sorted(
        [
            p
            for p in HERE.rglob("*")
            if p.is_file()
            and p.name != "VERIFICATION.json"
            and p.suffix != ".pyc"
            and "__pycache__" not in p.parts
        ]
        + [
            ROOT / "src/hdmatch/astrology/argoli_1610_direction_conventions.py",
            ROOT / "tests/unit/test_argoli_descending_converse.py",
        ]
    )
    hashes = {
        str(path.relative_to(ROOT)): {
            "sha256": sha(path),
            "bytes": path.stat().st_size,
        }
        for path in paths
    }
    return {
        "schema": "ARGOLI_1610_1667_DESCENDING_CONVERSE_FILE_AUDIT_V1",
        "source_method_before_holdout_commit": replay["fixed_source_and_math_precommit"],
        "source_witness_images": 10,
        "derived_detail_crops_not_independent_evidence": 1,
        "original_1610_printed_pages": [43, 44, 45, 46, 47, 48],
        "original_1667_printed_pages": [31, 32, 33, 34],
        "original_1644_printing_compared": False,
        "new_400_case_holdout_over_one_degree": replay["holdout_over_one_degree"],
        "new_400_case_holdout_over_five_degrees": replay["holdout_over_five_degrees"],
        "replay_status": replay["status"],
        "all_human_predictive_accuracy": "UNTESTED",
        "root_owner_goal_state": "OPEN",
        "file_sha256": hashes,
    }


if __name__ == "__main__":
    path = HERE / "VERIFICATION.json"
    data = manifest()
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print("verified source and computed artifacts:", len(data["file_sha256"]))
