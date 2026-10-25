#!/usr/bin/env python3
"""Checksum-backed extent audit of 1610 and partial 1667 Argoli scan witnesses.

Visual printed-page numbers are source-inspection assertions; this tool verifies
the underlying original bytes, source IDs, and PDF physical leaf count.
It does not OCR, compare unaligned chapters, or score any human astrology.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREVIOUS_SOURCE = ROOT / "docs/astrology-research-map/argoli-independent-regio-pole-20261025"


def sha(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def build() -> dict[str, Any]:
    record: dict[str, Any] = json.loads((HERE / "ARGOLI_EDITION_AUDIT.json").read_text())
    section = record["edition_1610"]
    for witness in section["distinct_digital_volumes"]:
        if sha(HERE / witness["relative_path"]) != witness["sha256"]:
            raise ValueError("1610 original image changed: " + witness["volume_id"])
    ext = record["edition_1667"]
    original = ROOT / ext["parent_pdf_relative_path"]
    if sha(original) != ext["parent_pdf_sha256"]:
        raise ValueError("existing partial 1667 original PDF changed")
    for leaf in ext["terminal_leaves"]:
        if sha(HERE / leaf["relative_path"]) != leaf["sha256"]:
            raise ValueError("1667 terminal leaf image changed")
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        raise RuntimeError("pdfinfo required for PDF physical page-count verification")
    result = subprocess.run(
        [pdfinfo, str(original)], capture_output=True, text=True, timeout=20, check=True
    )
    found = re.search(r"^Pages:\s*(\d+)\s*$", result.stdout, re.MULTILINE)
    if found is None or int(found.group(1)) != 107:
        raise ValueError("1667 excerpt's PDF leaf count changed")
    names = sorted(
        [
            p
            for p in HERE.rglob("*")
            if p.is_file()
            and p.name != "VERIFICATION.json"
            and p.suffix != ".pyc"
            and "__pycache__" not in p.parts
        ]
        + [
            ROOT / "tests/unit/test_argoli_edition_extent.py",
            PREVIOUS_SOURCE / "VERIFICATION.json",
            PREVIOUS_SOURCE / "README.md",
            PREVIOUS_SOURCE / "PRIMARY_SOURCE_SCOPE.md",
            PREVIOUS_SOURCE / "CONTINUATION_CHECKPOINT.md",
        ]
    )
    files = {
        str(path.relative_to(ROOT)): {
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        }
        for path in names
    }
    return {
        "schema": "ARGOLI_1610_1644_1667_EXTENT_VERIFICATION_V1",
        "root_astrology_human_validation": "OPEN",
        "human_predictive_accuracy": "UNTESTED",
        "complete_1667_volume_available": False,
        "verified_1667_pdf_leaves": 107,
        "verified_1667_last_printed_page": 95,
        "n_independent_1610_printed_p3_images": 3,
        "edition_1644_primary_page_collation": "UNAVAILABLE_HTTP_403",
        "1610_method_chapter_alignment": "UNRESOLVED",
        "original_parent_source_sha256": sha(original),
        "files": files,
    }


if __name__ == "__main__":
    target = HERE / "VERIFICATION.json"
    receipt = build()
    target.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(
        "Original source extent verified:", len(receipt["files"]), "files; 1667 excerpt: 107 leaves"
    )
