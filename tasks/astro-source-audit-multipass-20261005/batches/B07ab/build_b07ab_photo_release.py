#!/usr/bin/env python3
"""Portable primary-source 1647 Libra/Scorpio 77-test ZIP/CRC/SHA replay."""

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
REL = TASK + "/batches/B07ab/"
W = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
NAME = "Astrology-Lilly-1647-Libra-Scorpio-Rate-Photos-B07ab-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


source = j(B / "PHOTO_SOURCE_LIBRA_SCORPIO_V1.json")
overlay = j(B / "ANNUAL_RATE_PHOTO_OVERLAY_V4.json")
assert overlay["added_Libra_Scorpio_source_readings"] == 58
assert overlay["cumulative_one_reader_original_photo_legible"] == 263
assert overlay["not_read_original_table_remaining"] == 105
assert overlay["cumulative_original_glyphs_unresolved"] == 4
assert j(ROOT / W)["records_count"] == 12472
assert j(ROOT / CHINA)["sum_source_annotations"] == 142

names = [
    "PHOTO_SOURCE_LIBRA_SCORPIO_V1.json",
    "ANNUAL_RATE_PHOTO_OVERLAY_V4.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "build_b07ab_overlay.py",
    "test_b07ab_libra_scorpio.py",
    "build_b07ab_photo_release.py",
] + [
    "evidence/" + s + "_" + h + ".png"
    for s in ("Libra", "Scorpio")
    for h in ("first_half", "second_half")
]
files = {REL + n: B / n for n in names}
files[TASK + "/batches/B07aa/ANNUAL_RATE_PHOTO_OVERLAY_V3.json"] = (
    B.parent / "B07aa/ANNUAL_RATE_PHOTO_OVERLAY_V3.json"
)
files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"] = (
    B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
)
files[W] = ROOT / W
files[CHINA] = ROOT / CHINA
assert all(p.is_file() for p in files.values())

manifest = {
    "batch": "B07ab",
    "source": "Lilly 1647 Wellcome b30338724 PDF745 printed711",
    "original_full_pdf_sha256": source["full_original_pdf_sha256"],
    "photo_1647_sha256": source["photo_parent_sha256"],
    "physical_positions_looked_at": 62,
    "previous_overlap_not_double_counted": 4,
    "new_single_reader_positions": 58,
    "source_vs_derivative_disagreements": 2,
    "total_literary_table_cells": 372,
    "one_reader_1647_legible_cumulative": 263,
    "glyph_uncertainties_cumulative": 4,
    "still_not_physically_read": 105,
    "Western_canonical_Lilly_count_unchanged": 12472,
    "Chinese_history_index_retained": 142,
    "final_CLXVI_numeric_chapter_accepted": False,
    "real_person_predictions_validated": 0,
    "runtime_rules_promoted": 0,
    "first_edition_source_pdf_not_republished": True,
    "members": {k: {"sha256": sha(v), "bytes": v.stat().st_size} for k, v in files.items()},
}
out = downloads()
out.mkdir(parents=True, exist_ok=True)
archive = out / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, path in files.items():
        z.write(path, "B07ab-root/" + name)
    z.writestr(
        "B07ab-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07ab-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for path, meta in manifest["members"].items():
        f = root / path
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
            "test_b07ab_libra_scorpio.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=80,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    m = re.search(r"Ran (\d+) tests", p.stderr)
    assert m and int(m.group(1)) == 77, p.stderr
    assert "skipped" not in p.stderr
receipt = {
    "batch": "B07ab",
    "status": "PHOTOGRAPHIC_SOURCE_LIBRA_SCORPIO_77_TESTS_ARCHIVE_REPLAY_PASS",
    "archive_filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "CRC_verified": True,
    "all_member_SHA256_and_exact_bytes_verified": True,
    "portable_extracted_test_replay_passed": True,
    "replayed_tests": 77,
    "new_source_sha256": sha(B / "PHOTO_SOURCE_LIBRA_SCORPIO_V1.json"),
    "new_overlay_sha256": sha(B / "ANNUAL_RATE_PHOTO_OVERLAY_V4.json"),
    "Western_Lilly_count_retained": 12472,
    "Chinese_V3_count_retained": 142,
    "new_canonical_historical_source_records": 0,
    "original_372_table_fully_collated": False,
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
