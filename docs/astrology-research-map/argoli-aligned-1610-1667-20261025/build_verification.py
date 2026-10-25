#!/usr/bin/env python3
"""Integrity/provenance manifest of aligned Argoli 1610 and 1667 source evidence.

Original visual readings were made from displayed physical page images.
Mechanical checks verify image bytes, IIIF labels, old original PDF and exact
sexagesimal examples; no OCR or human outcome data enters the result.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hdmatch.astrology.argoli_printed_arithmetic import (
    printed_arc_discrepancy_minutes,
    subtract_degree_minute_seconds,
    subtract_degree_minutes,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict[str, Any]:
    evidence = json.loads((HERE / "ARGOLI_ALIGNED_EXAMPLES.json").read_text())
    if evidence["schema"] != "ARGOLI_1610_1667_ALIGNED_DIRECTION_EXAMPLES_V1":
        raise ValueError("unexpected original-source alignment schema")
    bsb = evidence["source_hierarchy"]["edition_1610"]
    manifest_path = HERE / "BSB_1610_1760_leaf_IIIF_manifest.json"
    if sha(manifest_path) != bsb["full_iiif_manifest_sha256"]:
        raise ValueError("1610 institutional IIIF provenance changed")
    iiif = json.loads(manifest_path.read_text())
    if len(iiif["sequences"][0]["canvases"]) != 1760:
        raise ValueError("1610 original canvas count changed")
    for page in bsb["pages"]:
        if sha(HERE / page["file"]) != page["sha256"]:
            raise ValueError("1610 original primary image changed")
        canvas = iiif["sequences"][0]["canvases"][page["iiif_leaf"] - 1]
        if not canvas["label"].startswith(str(page["printed"]) + " "):
            raise ValueError("1610 canvas original printed-page label changed")

    original_1667 = evidence["source_hierarchy"]["edition_1667"]
    if (
        sha(ROOT / original_1667["parent_original_pdf"])
        != (original_1667["parent_original_pdf_sha256"])
    ):
        raise ValueError("parent original 1667 prose/excerpt PDF changed")
    for page in original_1667["pages"]:
        if sha(HERE / page["file"]) != page["sha256"]:
            raise ValueError("1667 original primary image changed")
    for x in evidence["worked_examples"]:
        if x["id"] == "SATURN_POSITION_POLE":
            actual = subtract_degree_minute_seconds(
                x["first_operand_deg_min_sec"], x["subtrahend_deg_min_sec"]
            )
            expected = x["arithmetically_computed_deg_min_sec"]
            if list(actual) != expected:
                raise ValueError("pole interpolation historical arithmetic changed")
            if x["printed_1610_deg_min_sec"] != expected:
                raise ValueError("1610 printed pole interpolation differs")
            if x["printed_1667_deg_min_sec"] != expected:
                raise ValueError("1667 printed pole interpolation differs")
        else:
            actual_minutes = subtract_degree_minutes(
                x["first_operand_deg_min"], x["second_operand_deg_min"]
            )
            if list(actual_minutes) != x["arithmetically_computed_deg_min"]:
                raise ValueError("historical direction operands changed")
            if x["printed_1610_deg_min"] != list(actual_minutes):
                raise ValueError("1610 printed angular result differs from arithmetic")
            if x["id"] == "SATURN_TO_OPPOSITION_SUN":
                if (
                    printed_arc_discrepancy_minutes(actual_minutes, x["printed_1667_deg_min"])
                    != 120
                ):
                    raise ValueError("original 1667 2-degree discrepancy changed")
            elif x["printed_1667_deg_min"] != list(actual_minutes):
                raise ValueError("1667 original printed identical example changed")
    if evidence["empirical_human_predictive_accuracy"] != "UNTESTED":
        raise ValueError("this source packet must not claim human validation")

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
            ROOT / "src/hdmatch/astrology/argoli_printed_arithmetic.py",
            ROOT / "tests/unit/test_argoli_aligned_1610_1667.py",
        ]
    )
    hashes = {
        str(path.relative_to(ROOT)): {
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        }
        for path in paths
    }
    return {
        "schema": "ARGOLI_1610_1667_ALIGNED_PRIMARY_SOURCE_INTEGRITY_V1",
        "original_1610_BSB_canvases": 1760,
        "original_1610_primary_pages_checked": [39, 40, 41],
        "original_1667_primary_pages_checked": [29, 30],
        "identical_printed_arcs_checked": 2,
        "inspected_1667_original_arithmetic_discrepancy_arc_minutes": 120,
        "source_1644_homologous_passages": "UNRESOLVED",
        "source_1667_second_prose_witness": "NOT_FOUND",
        "human_predictive_accuracy": "UNTESTED",
        "owner_combined_astrology_outcome": "OPEN",
        "hashed_files": hashes,
        "separately_located_1667_table_PDF_sha256": evidence["source_hierarchy"][
            "additional_1667_table_volume"
        ]["pdf_sha256"],
        "separately_located_1667_table_PDF_in_Git": False,
    }


if __name__ == "__main__":
    dest = HERE / "VERIFICATION.json"
    record = build()
    dest.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n")
    print("Source witness hashes verified:", len(record["hashed_files"]))
