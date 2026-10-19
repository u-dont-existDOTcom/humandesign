#!/usr/bin/env python3
"""Portable original first-edition source-only B07ac research evidence archive."""

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
REL = TASK + "/batches/B07ac/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
NAME = "Astrology-Lilly-1647-Sagittarius-Capricorn-Rate-Photos-B07ac-20261019.zip"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


src = j(B / "PHOTO_SOURCE_SAGITTARIUS_CAPRICORN_V1.json")
overlay = j(B / "ANNUAL_RATE_PHOTO_OVERLAY_V5.json")
assert overlay["B07ac_new_one_reader_legible"] == 57
assert overlay["B07ac_new_ambiguous_source_glyphs"] == 1
assert overlay["cumulative_one_reader_legible_original"] == 320
assert overlay["cumulative_original_source_glyph_ambiguities"] == 5
assert overlay["cumulative_positions_original_unread"] == 47
assert j(ROOT / INDEX)["records_count"] == 12472
assert j(ROOT / CHINA)["sum_source_annotations"] == 142

names = [
    "PHOTO_SOURCE_SAGITTARIUS_CAPRICORN_V1.json",
    "ANNUAL_RATE_PHOTO_OVERLAY_V5.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "build_b07ac_overlay.py",
    "test_b07ac_photos.py",
    "build_b07ac_release.py",
]
names += sorted(str(f.relative_to(B)) for f in (B / "evidence").glob("*.png"))
files = {REL + n: B / n for n in names}
files[TASK + "/batches/B07ab/ANNUAL_RATE_PHOTO_OVERLAY_V4.json"] = (
    B.parent / "B07ab/ANNUAL_RATE_PHOTO_OVERLAY_V4.json"
)
files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"] = (
    B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
)
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values())
assert (
    sha(files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"])
    == (src["original_1647_image_pdf745_sha256"])
)

manifest = {
    "batch": "B07ac",
    "source": "Lilly 1647 Wellcome b30338724 first-edition printed711 PDF745",
    "full_original_pdf_sha256": src["full_1647_pdf_sha256"],
    "original_photo_source_SHA256": src["original_1647_image_pdf745_sha256"],
    "new_original_source_cells_legible": 57,
    "new_original_source_cell_glyph_unclear": 1,
    "four_prior_Capricorn_B07y_overlaps_unduplicated": True,
    "new_source_derivative_disagreements": 2,
    "source_table_total_cells": 372,
    "cumulative_original_one_reader_legible": 320,
    "cumulative_glyph_ambiguities": 5,
    "unread_original_source_cells": 47,
    "source_is_not_validated_human_chart_scoring": True,
    "accepted_Lilly_source_count_unchanged": 12472,
    "accepted_Chinese_V3_source_count_unchanged": 142,
    "independent_human_validations": 0,
    "runtime_promotions": 0,
    "members": {
        name: {"sha256": sha(path), "bytes": path.stat().st_size} for name, path in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, f in files.items():
        z.write(f, "B07ac-root/" + name)
    z.writestr(
        "B07ac-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )

with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07ac-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        f = root / name
        assert sha(f) == meta["sha256"]
        assert f.stat().st_size == meta["bytes"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07ac_photos.py",
            "-q",
        ],
        text=True,
        capture_output=True,
        timeout=85,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    m = re.search(r"Ran (\d+) tests", p.stderr)
    assert m and int(m.group(1)) == 78, p.stderr
    assert "skipped" not in p.stderr
receipt = {
    "batch": "B07ac",
    "status": "SOURCE_PHOTO_SAG_CAP_78_PORTABLE_TESTS_CRC_SHA_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "sha256_and_exact_bytes_passed": True,
    "independent_extraction_replayed_tests": 78,
    "source_sha256": sha(B / "PHOTO_SOURCE_SAGITTARIUS_CAPRICORN_V1.json"),
    "overlay_sha256": sha(B / "ANNUAL_RATE_PHOTO_OVERLAY_V5.json"),
    "Lilly_index_sha256_unchanged": sha(ROOT / INDEX),
    "Chinese_V3_sha256_unchanged": sha(ROOT / CHINA),
    "historical_source_records_accepted_new": 0,
    "all_372_first_edition_cells_collated": False,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
