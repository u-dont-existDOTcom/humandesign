#!/usr/bin/env python3
"""Portable original Lilly 1647/1659 seven-uncertain-glyph documentary ZIP."""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
REL = TASK + "/batches/B07af/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
NAME = "Astrology-Lilly-1647-1659-Seven-Unresolved-Rate-Glyphs-B07af-20261019.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    proc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        proc.stdout.strip()
        if proc.returncode == 0 and proc.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


source = j(B / "SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json")
assert len(source["entries"]) == 7
assert source["source_first_edition_unresolved_after"] == 7
assert source["source_second_edition_tentative_glyph_matches"] == 2
assert source["source_second_edition_indeterminate_positions"] == 5
assert source["model_runtime_promotions"] == 0
assert j(ROOT / WEST)["records_count"] == 12472
assert j(ROOT / CHINA)["sum_source_annotations"] == 142

names = [
    "SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json",
    "ORIGINAL_1647_1659_SEVEN_GLYPHS_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "build_b07af_seven_glyph_comparison.py",
    "test_b07af_seven_source_glyphs.py",
    "build_b07af_release.py",
    "evidence/original_1647_annual_table_pdf745_3500.jpg",
    "evidence/second_edition_1659_annual_table_page740.jpg",
    "evidence/2nd1659_header_coordinate_grid.png",
] + [
    "evidence/1659_cell_" + sign + "_" + f"{degree:02d}" + ".png"
    for sign, degree in (
        ("Virgo", 1),
        ("Virgo", 18),
        ("Capricorn", 9),
        ("Capricorn", 15),
        ("Aquarius", 5),
        ("Aquarius", 6),
        ("Pisces", 24),
    )
]
files = {REL + name: B / name for name in names}
files[TASK + "/batches/B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"] = (
    B.parent / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
)
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values()), [
    name for name, file in files.items() if not file.is_file()
]
assert (
    sha(B / "evidence/original_1647_annual_table_pdf745_3500.jpg")
    == (source["source_first_edition_photo_sha256"])
)
assert (
    sha(B / "evidence/second_edition_1659_annual_table_page740.jpg")
    == (source["source_second_edition_original_image_sha256"])
)
manifest = {
    "batch": "B07af",
    "research_status": "SOURCE_COMPARISON_ONLY_1647_UNKNOWNS_RETAINED",
    "1647_original_pdf_sha256": source["source_first_edition_full_pdf_sha256"],
    "1647_original_pdf745_source_sha256": source["source_first_edition_photo_sha256"],
    "1659_original_djvu740_source_sha256": source["source_second_edition_original_image_sha256"],
    "total_first_edition_zodiac_sign_degree_cells": 372,
    "original_first_edition_1647_legible_one_reader": 365,
    "original_first_edition_1647_glyphs_remaining_unresolved": 7,
    "second_edition_1659_one_reader_tentative": 2,
    "second_edition_1659_scan_not_readable": 5,
    "independent_human_historian_review_completed": False,
    "no_original_1647_glyph_replaced": True,
    "Lilly_historical_source_registry_unchanged": 12472,
    "Chinese_V3_historical_source_registry_unchanged": 142,
    "original_1647_time_engine_verified": False,
    "real_human_prediction_validations": 0,
    "runtime_promotions": 0,
    "full_original_1647_pdf_not_embedded": True,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07af-root/" + name)
    z.writestr(
        "B07af-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    out = Path(td) / "B07af-root"
    assert j(out / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        f = out / name
        assert sha(f) == meta["sha256"]
        assert f.stat().st_size == meta["bytes"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(out / REL),
            "-p",
            "test_b07af_seven_source_glyphs.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    m = re.search(r"Ran (\d+) tests", p.stderr)
    assert m and int(m.group(1)) == 18, p.stderr
    assert "skipped" not in p.stderr
receipt = {
    "batch": "B07af",
    "status": "SEVEN_SECOND_EDITION_SOURCE_GLYPHS_18_ARCHIVE_TESTS_PASS",
    "archive_filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "CRC_passed": True,
    "member_SHA256_and_exact_bytes_passed": True,
    "independent_archive_extraction_replayed_tests": 18,
    "source_record_sha256": sha(
        B / "SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json"
    ),
    "prior_original_1647_372_source_sha256": sha(
        files[TASK + "/batches/B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"]
    ),
    "Lilly_history_source_records_retained": 12472,
    "Chinese_V3_historical_source_records_retained": 142,
    "real_human_prediction_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
