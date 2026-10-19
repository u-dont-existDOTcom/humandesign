#!/usr/bin/env python3
"""Portable original 1647/1659 Maginus source: CRC/hash/70 focused test replay."""

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
REL = TASK + "/batches/B07ai/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NAME = "Astrology-Lilly-1647-1659-Maginus-31-Historical-Sources-B07ai-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


source = j(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
assert source["new_historical_annotation_count"] == rules["record_count"] == 31
assert source["Lilly_before"] == j(ROOT / WEST)["records_count"] == 12515
assert source["Chinese_V5_retained"] == j(ROOT / CHINESE)["sum_source_annotations"] == 262
assert len(source["original_24_years_source_table"]) == 24
assert source["actual_real_person_predictions_validated"] == source["runtime_promotions"] == 0
assert not source["full_original_CLXVI_chapter_complete"]
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["original_source_records_SHA256"] == sha(
    B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json"
)

names = [
    "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "SECONDARY_NAVIGATOR_WINDOW.txt",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_table_use_maginus_p746.py",
    "test_b07ai_printed_maginus.py",
    "build_b07ai_release.py",
    "prepare_b07ai_partial_canonical.py",
]
files = {REL + x: B / x for x in names}
files[TASK + "/batches/B07ah/ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"] = (
    B.parent / "B07ah/ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"
)
files[TASK + "/batches/B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json"] = (
    B.parent / "B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json"
)
for meta in source["original_source_photo_four_print_witnesses"].values():
    file = ROOT / meta["file"]
    files[meta["file"]] = file
    assert sha(file) == meta["sha256"]
    assert file.stat().st_size == meta["bytes"]
files[WEST] = ROOT / WEST
files[CHINESE] = ROOT / CHINESE
assert all(f.is_file() for f in files.values())
manifest = {
    "batch": "B07ai",
    "physical_sources": (
        "Original 1647 and independently typeset second edition 1659 "
        "Christian Astrology printed711–712"
    ),
    "original_full_pdf_sha256": source["source_original_1647_full_PDF_sha256"],
    "original_photo_binary_sha256s": {
        key: photo["sha256"]
        for key, photo in source["original_source_photo_four_print_witnesses"].items()
    },
    "new_historical_source_notes": 31,
    "original_24_year_annual_source_table_rows": 24,
    "first_printed_simplified_rate_arcminutes_per_nominal_year": 54,
    "original_one_arcminute_printed_6days18hours": True,
    "printed_case_fraction_minutes": [42, 48],
    "actual_subtracted_arcminute_residuals": [13, 4],
    "original_literary_year_at_54_times_6d18h_nominal_days": "729/2",
    "full_CLXVI_source_chapter_complete": False,
    "Western_Lilly_source_if_accepted": 12546,
    "Ptolemy_retained": 1066,
    "Chinese_history_V5_retained": 262,
    "accurate_original_1647_birth_chart_engine_verified": False,
    "real_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "members": {name: {"sha256": sha(f), "bytes": f.stat().st_size} for name, f in files.items()},
}
out = downloads()
out.mkdir(parents=True, exist_ok=True)
archive = out / NAME
temporary = out / (NAME + ".building")
assert not temporary.exists()
with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
    for name, f in files.items():
        zipped.write(f, "B07ai-root/" + name)
    zipped.writestr(
        "B07ai-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temporary) as zipped, tempfile.TemporaryDirectory() as td:
    assert zipped.testzip() is None
    zipped.extractall(td)
    dest = Path(td) / "B07ai-root"
    assert j(dest / "RELEASE_MANIFEST.json") == manifest
    for name, info in manifest["members"].items():
        file = dest / name
        assert file.stat().st_size == info["bytes"]
        assert sha(file) == info["sha256"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(dest / REL),
            "-p",
            "test_b07ai_printed_maginus.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=80,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    m = re.search(r"Ran (\d+) tests", p.stderr)
    assert m and int(m.group(1)) == 70, p.stderr
    assert "skipped" not in p.stderr
os.replace(temporary, archive)
receipt = {
    "batch": "B07ai",
    "status": "1647_1659_SOURCE_MAGINUS_24_YEAR_TABLE_70_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_SHA256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "CRC_passed": True,
    "member_hashes_and_byte_sizes_passed": True,
    "independent_archive_extracted_test_replay_passed": True,
    "source_tests_replayed": 70,
    "records_SHA256": sha(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "prior_Western_index_SHA256": sha(ROOT / WEST),
    "Chinese_V5_SHA256": sha(ROOT / CHINESE),
    "original_source_printed_minutes": [42, 48],
    "actual_arithmetic_minutes_remaining": [13, 4],
    "historical_full_CLXVI_completed": False,
    "new_source_only_notes_if_admitted": 31,
    "real_people_predictive_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
