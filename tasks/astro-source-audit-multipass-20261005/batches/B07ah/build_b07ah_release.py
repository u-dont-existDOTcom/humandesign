#!/usr/bin/env python3
"""Atomic owner archive for Lilly original annual 1647 table, 386 tests replay."""

import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
REL = TASK + "/batches/B07ah/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NAME = "Astrology-Lilly-1647-Annual-Rate-372-Original-Source-B07ah-20261019.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    if french.is_dir():
        return french
    return Path.home()


cross = j(B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
old = j(ROOT / WEST)
china = j(ROOT / CHINESE)
assert old["records_count"] == accept["prior_Lilly"] == 12501
assert old["batches"][-1]["id"] == "B07ag"
assert china["sum_source_annotations"] == accept["Chinese_V5_parallel"] == 262
assert cross["original_rate_total_physical_positions"] == 372
assert cross["original_1647_one_reader_legible"] == 365
assert cross["original_1647_unresolved"] == 7
assert cross["original_vs_derived_searchable_text_disagreements"] == 14
assert rules["record_count"] == 14
assert len(rules["rules"]) == 14
assert all(not r["runtime_model_promoted"] for r in rules["rules"])
assert rules["source_source_table_SHA256"] == sha(
    B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"
)
assert not cross["historical_annual_measure_arithmetic_validated"]
assert (
    cross["empirical_real_human_validations"]
    == rules["independent_human_predictive_validations"]
    == 0
)

names = [
    "ACCEPTANCE.json",
    "RULES.json",
    "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_1647_annual_rate_table_bridge.py",
    "test_b07ah_rate_table_source.py",
    "build_b07ah_release.py",
    "prepare_b07ah_partial_canonical.py",
]
files = {REL + n: B / n for n in names}
files[TASK + "/batches/B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"] = (
    B.parent / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
)
files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"] = (
    B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
)
files[TASK + "/batches/B07y/evidence/1659_annual_measure_table_page740.jpg"] = (
    B.parent / "B07y/evidence/1659_annual_measure_table_page740.jpg"
)
files[TASK + "/batches/B07af/SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json"] = (
    B.parent / "B07af/SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json"
)
files[TASK + "/batches/B07ag/RULES.json"] = B.parent / "B07ag/RULES.json"
files[WEST] = ROOT / WEST
files[CHINESE] = ROOT / CHINESE
assert all(v.is_file() for v in files.values()), [k for k, v in files.items() if not v.is_file()]
assert (
    sha(files[TASK + "/batches/B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"])
    == (cross["origin_source_overlay_sha256"])
)
assert (
    sha(files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"])
    == (cross["source_first_edition_original_photo_pdf745_SHA256"])
)
manifest = {
    "batch": "B07ah",
    "source": "William Lilly 1647 original first edition printed711 PDF745",
    "primary_1647_photo_SHA256": cross["source_first_edition_original_photo_pdf745_SHA256"],
    "historical_1647_original_full_pdf_SHA256": cross["source_original_1647_full_pdf_sha256"],
    "historical_source_table_physical_rate_rows": 372,
    "source_read_by_one_reader": 365,
    "source_1647_glyphs_unresolved": 7,
    "derivative_discrepancy_rows": 14,
    "new_source_history_annotation_records": 14,
    "new_R_first": "R12502",
    "new_R_last": "R12515",
    "Lilly_historical_registry_if_accepted": 12515,
    "Ptolemy_retained": 1066,
    "Chinese_V5_retained": 262,
    "full_Lilly_CLXVI_source_chapter_accepted": False,
    "source_year_time_ephemeris_engine_validated": False,
    "predictive_human_validation": 0,
    "runtime_promotions": 0,
    "members": {name: {"sha256": sha(v), "bytes": v.stat().st_size} for name, v in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
temp_path = folder / (NAME + ".building")
assert not temp_path.exists()
with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07ah-root/" + name)
    z.writestr(
        "B07ah-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temp_path) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    restored = Path(td) / "B07ah-root"
    assert j(restored / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        f = restored / name
        assert f.stat().st_size == meta["bytes"]
        assert sha(f) == meta["sha256"]
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(restored / REL),
            "-p",
            "test_b07ah_rate_table_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=75,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    m = re.search(r"Ran (\d+) tests", result.stderr)
    assert m and int(m.group(1)) == 386, result.stderr
    assert "skipped" not in result.stderr
os.replace(temp_path, archive)
receipt = {
    "batch": "B07ah",
    "status": "LILLY_1647_ANNUAL_TABLE_372_CELLS_386_PORTABLE_TEST_REPLAYS_PASS",
    "archive_filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "crc_passed": True,
    "member_SHA256_and_sizes_passed": True,
    "independent_archive_extracted_test_replay_passed": True,
    "portable_test_count": 386,
    "source_rate_crosswalk_SHA256": sha(B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "parent_B07ad_source_SHA256": sha(B.parent / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"),
    "prior_Lilly_index_SHA256": sha(ROOT / WEST),
    "Chinese_V5_index_SHA256": sha(ROOT / CHINESE),
    "new_canonical_historical_annotations_if_accepted": 14,
    "CLXVI_complete": False,
    "real_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
