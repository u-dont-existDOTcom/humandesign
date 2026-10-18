#!/usr/bin/env python3
"""Independently extract and replay expanded CLXVI numerical SOURCE-only packet.

This is a PROVISIONAL document engineering archive, not canonical acceptance
of CLXVI calculations or a real-person event forecast engine.
"""

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
REL = TASK + "/batches/B07x/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
FILENAME = "Astrology-Lilly-1647-CLXVI-Numerical-Timing-Expanded-Provisional-20261018.zip"


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


win = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
cases = j(B / "WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json")
naibod = j(B / "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json")
annual = j(B / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json")
cross = j(B / "NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json")
assert win["accepted_lilly_before"] == 12472
assert win["next_historical_record"] == "R12473"
assert win["following_heading_is_duplicate_printed_numeral"]
assert naibod["degree_rows_count"] == 90
assert naibod["minute_rows_currently_visible_count"] == 59
assert naibod["missing_source_minute_labels"] == [27]
assert annual["source_cells_expected"] == 372
assert annual["direct_original_photo_confirmed"] == 12
assert annual["cells_without_direct_photo_check"] == 360
assert cross["first_edition_documentary_values_never_overwritten_from_later_edition"]
assert not cross["historical_algorithm_martial_natal_accuracy_validated"]
assert not cases["all_original_numerical_table_cells_collated"]
assert naibod["runtime_promotions"] == annual["runtime_promotions"] == 0
assert j(ROOT / INDEX)["records_count"] == 12472
assert sha(ROOT / INDEX) == win["source_index_parent_sha256"]
assert j(ROOT / CHINA)["sum_source_annotations"] == 97

names = (
    [
        "ORIGINAL_SOURCE_WINDOW_V1.json",
        "WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json",
        "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json",
        "NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json",
        "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json",
        "ORIGINAL_NUMERICAL_SOURCE_REVIEW_20261018.md",
        "NUMERIC_1659_COMPARISON_AND_ANNUAL_RECONSTRUCTION_20261018.md",
        "CONTINUATION_HANDOFF_PROVISIONAL_20261018.md",
        "CONTINUATION_HANDOFF_EXPANDED_PROVISIONAL_20261018.md",
        "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261018.json",
        "prepare_original_b07x_source_window.py",
        "lilly_1647_direction_time_mechanics.py",
        "save_b07x_numeric_source_cases.py",
        "build_naibod_original_tables_provisional.py",
        "build_annual_measure_372_provisional.py",
        "test_b07x_numerical_source.py",
        "test_b07x_naibod_table.py",
        "test_b07x_cross_edition.py",
        "test_b07x_annual_measure.py",
        "build_b07x_numeric_release.py",
        "build_b07x_expanded_release.py",
    ]
    + [f"evidence/pdf_1647-{n}.jpg" for n in range(742, 751)]
    + [
        "evidence/second_edition_1659/1659_djvu_scan_742.jpg",
        "evidence/second_edition_1659/1659_djvu_scan_743.jpg",
    ]
)
files = {REL + name: B / name for name in names}
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(p.is_file() for p in files.values()), [
    name for name, p in files.items() if not p.is_file()
]
for name in ("degrees", "minutes"):
    row = cross["first_edition"][name]
    assert sha(B / row["file"]) == row["sha256"]
for name in ("degree_table", "minute_table"):
    row = cross["second_edition"][name]
    assert sha(B / row["file"]) == row["sha256"]

manifest = {
    "batch": "B07x",
    "status": "PROVISIONAL_NUMERICAL_SOURCE_NOT_CANONICAL_ACCEPTANCE",
    "1647_full_original_pdf_sha256": win["full_source_pdf_sha256"],
    "historical_printed_chapter_label": "CLXVI_time_measure",
    "next_printed_chapter_label": "CLXVI_annual_profections_DUPLICATED_NUMBER",
    "Lilly_canonical_accepted_stays_at": 12472,
    "proposed_next_Lilly_history_id": "R12473",
    "Ptolemy_retained": 1066,
    "chinese_v2_retained": 97,
    "degree_source_candidates": 90,
    "printed_minute_source_labels": 59,
    "minute_27_missing_in_both_printings": True,
    "second_edition_1659_original_photo_comparison": True,
    "annual_zodiac_candidate_cell_count": 372,
    "annual_cells_photo_confirmed": 12,
    "annual_cells_unverified_derivative": 360,
    "source_only_not_verified_natal_engine": True,
    "independent_real_person_forecasts_validated": 0,
    "runtime_promotions": 0,
    "members": {rel: {"sha256": sha(p), "bytes": p.stat().st_size} for rel, p in files.items()},
}
root = downloads()
root.mkdir(parents=True, exist_ok=True)
archive = root / FILENAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for rel, path in files.items():
        z.write(path, "B07x-expanded-root/" + rel)
    z.writestr(
        "B07x-expanded-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    extraction = Path(tmp) / "B07x-expanded-root"
    assert j(extraction / "RELEASE_MANIFEST.json") == manifest
    for rel, desc in manifest["members"].items():
        file = extraction / rel
        assert file.stat().st_size == desc["bytes"]
        assert sha(file) == desc["sha256"]
    cmd = [
        "python3",
        "-m",
        "unittest",
        "discover",
        "-s",
        str(extraction / REL),
        "-p",
        "test_b07x_*.py",
        "-q",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    count = re.search(r"Ran (\d+) tests", p.stderr)
    assert count and int(count.group(1)) == 110, p.stderr
    assert "skipped" not in p.stderr, p.stderr
receipt = {
    "batch": "B07x",
    "status": "EXPANDED_PROVISIONAL_SOURCE_110_PORTABLE_TESTS_PASS",
    "filename": FILENAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_members": len(files),
    "crc_passed": True,
    "member_sha256_and_bytes_passed": True,
    "independent_extraction_passed": True,
    "all_tests_replayed": 110,
    "original_canonical_index_sha256": sha(ROOT / INDEX),
    "naibod_table_sha256": sha(B / "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json"),
    "annual_candidates_sha256": sha(B / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"),
    "cross_edition_comparison_sha256": sha(B / "NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json"),
    "new_canonical_source_notes_accepted": 0,
    "source_table_critical_collation_completed": False,
    "human_predictive_accuracy_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_EXPANDED_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
