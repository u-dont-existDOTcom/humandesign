"""Argoli 1610 witness hashes and 1667 107-leaf scan-extent verification.

Manual visual collation labels are provenance statements, NOT inferred by
OCR or by an image hash. Tests mechanically verify exact audited bytes and
prevent old incomplete-scan assertions from being promoted to source truth.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/astrology-research-map/argoli-edition-witness-audit-20261025"


def data() -> dict:
    return json.loads((DOC / "ARGOLI_EDITION_AUDIT.json").read_text(encoding="utf-8"))


def test_exact_1610_original_printed_p3_three_digital_witnesses() -> None:
    source = data()["edition_1610"]
    assert source["print_page_checked"] == 3
    assert source["status"] == "ONE_PAGE_THREE_WITNESSES_VISUALLY_COMPARED"
    assert source["whole_book_original_scanned"] is False
    scans = source["distinct_digital_volumes"]
    assert {s["volume_id"] for s in scans} == {"R92lDeOw8X0C", "7utl-3EFz1UC", "-zhmAAAAcAAJ"}
    assert len({s["sha256"] for s in scans}) == 3
    for entry in scans:
        file = DOC / entry["relative_path"]
        assert file.is_file()
        assert hashlib.sha256(file.read_bytes()).hexdigest() == entry["sha256"]
        assert file.read_bytes().startswith(b"\xff\xd8\xff")
    assert "all three" in source["verified_visual_statement"].lower()


def test_1667_pdf_has_only_107_leaves_and_ends_at_printed_p95() -> None:
    info = data()["edition_1667"]
    pdf = ROOT / info["parent_pdf_relative_path"]
    assert pdf.is_file()
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == info["parent_pdf_sha256"]
    command = shutil.which("pdfinfo")
    if command is None:
        pytest.skip("pdfinfo unavailable; PDF hash and images still checked")
    result = subprocess.run(
        [command, str(pdf)], capture_output=True, text=True, timeout=15, check=True
    )
    match = re.search(r"^Pages:\s*(\d+)\s*$", result.stdout, flags=re.MULTILINE)
    assert match is not None
    assert int(match.group(1)) == info["pdf_physical_pages"] == 107
    assert "95" in info["partial_extent"]
    assert info["status"] == "FIRST_95_PRINTED_PAGES_AND_COVERS_VERIFIED_SCAN_PARTIAL"


def test_final_pages_images_match_verified_original_leaf_labels() -> None:
    pages = data()["edition_1667"]["terminal_leaves"]
    assert [(p["pdf_page"], p["printed_page"]) for p in pages] == [
        (105, 94),
        (106, 95),
        (107, None),
    ]
    for leaf in pages:
        source = DOC / leaf["relative_path"]
        assert source.is_file()
        assert source.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        assert hashlib.sha256(source.read_bytes()).hexdigest() == leaf["sha256"]


def test_no_anachronistic_full_edition_or_empirical_validity_claims() -> None:
    audit = data()
    assert audit["human_outcomes_seen"] is False
    assert audit["human_predictive_validity"] == "UNTESTED"
    assert audit["edition_1644"]["full_edition_verified"] is False
    assert "NOT_ALIGNED" in audit["unaligned_same_page_comparison"]["status"]
    assert "not prove" in audit["unaligned_same_page_comparison"]["statement"].lower()
    assert len(audit["negative_results"]) >= 3
    assert audit["owner_root_goal"]["state"] == "OPEN"
    checkpoint = (
        ROOT
        / "docs/astrology-research-map/argoli-independent-regio-pole-20261025"
        / "CONTINUATION_CHECKPOINT.md"
    ).read_text()
    assert "complete **107-image excerpt**" in checkpoint
    assert "not the full printed volume" in checkpoint


def test_source_file_manifest_and_correction_are_reproducible() -> None:
    import importlib.util

    generator = DOC / "build_verification.py"
    module_spec = importlib.util.spec_from_file_location(
        "argoli_source_extent_verification", generator
    )
    assert module_spec is not None and module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    old = json.loads((DOC / "VERIFICATION.json").read_text())
    assert module.build() == old
    assert old["human_predictive_accuracy"] == "UNTESTED"
    assert old["verified_1667_pdf_leaves"] == 107
    assert old["verified_1667_last_printed_page"] == 95
    assert old["complete_1667_volume_available"] is False
    assert old["n_independent_1610_printed_p3_images"] == 3
    assert old["1610_method_chapter_alignment"] == "UNRESOLVED"
    for relative, proof in old["files"].items():
        f = ROOT / relative
        assert f.stat().st_size == proof["bytes"]
        assert hashlib.sha256(f.read_bytes()).hexdigest() == proof["sha256"]
