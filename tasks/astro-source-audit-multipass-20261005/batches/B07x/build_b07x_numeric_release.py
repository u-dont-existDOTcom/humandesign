#!/usr/bin/env python3
"""Portable original CLXVI numerical-method research checkpoint, not canonical acceptance."""

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
FILENAME = "Astrology-Lilly-1647-CLXVI-Numerical-Timing-Provisional-20261018.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
cases = load(B / "WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json")
assert window["accepted_lilly_before"] == 12472
assert window["next_historical_record"] == "R12473"
assert window["following_heading_is_duplicate_printed_numeral"]
assert window["body_original_pdf_frames"] == list(range(742, 750))
assert cases["independent_human_life_event_predictions_validated"] == 0
assert cases["runtime_promotions"] == 0
assert cases["all_original_numerical_table_cells_collated"] is False
assert cases["first_edition_annual_measure_table_cells_expected"] == 372
assert cases["annual_measure_cells_visually_verified"] == 1
assert sha(ROOT / INDEX) == window["source_index_parent_sha256"]
assert load(ROOT / INDEX)["records_count"] == 12472
assert load(ROOT / CHINA)["sum_source_annotations"] == 97

names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json",
    "ORIGINAL_NUMERICAL_SOURCE_REVIEW_20261018.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261018.md",
    "prepare_original_b07x_source_window.py",
    "lilly_1647_direction_time_mechanics.py",
    "save_b07x_numeric_source_cases.py",
    "test_b07x_numerical_source.py",
    "build_b07x_numeric_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(742, 751)]
files = {REL + name: B / name for name in names}
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values())
manifest = {
    "batch": "B07x",
    "source": "Original William Lilly Christian Astrology 1647 b30338724",
    "documentary_stage": "NUMERICAL_METHOD_PROVISIONAL_UNACCEPTED",
    "printed_original_time_measure_heading": "CLXVI",
    "following_original_annual_profection_heading": "CLXVI",
    "same_heading_numeral_repeated": True,
    "proposed_next_Lilly_R": "R12473",
    "accepted_Lilly_count_unmodified": 12472,
    "ancient_ptolemy_registry_unchanged": 1066,
    "chinese_historic_registry_unchanged": 97,
    "anchored_original_method_propositions": 12,
    "bounded_historical_arithmetic_method_count": 3,
    "original_historical_worked_examples_with_internal_discrepancies": 2,
    "full_zodiac_annual_measure_table_cells": 372,
    "original_annual_table_cells_checked": 1,
    "Naibod_degree_table_rows_expected": 90,
    "Naibod_minute_table_rows_expected": 60,
    "full_printed_numerical_table_reconciliation_done": False,
    "astrological_accurate_birth_chart_engine_verified": False,
    "real_human_event_prediction_validated": 0,
    "runtime_model_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / FILENAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07x-root/" + name)
    z.writestr(
        "B07x-root/RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B07x-root"
    assert load(root / "RELEASE_MANIFEST.json") == manifest
    for name, spec in manifest["members"].items():
        file = root / name
        assert file.stat().st_size == spec["bytes"]
        assert sha(file) == spec["sha256"]
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07x_numerical_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    m = re.search(r"Ran (\d+) tests", proc.stderr)
    assert m and int(m.group(1)) == 40, proc.stderr
    assert "skipped" not in proc.stderr
receipt = {
    "batch": "B07x",
    "status": "PROVISIONAL_ORIGINAL_NUMERICAL_METHODS_40_ARCHIVE_TESTS_PASS",
    "filename": FILENAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "sha256_and_bytes_passed": True,
    "independent_extraction_passed": True,
    "total_replayed_tests": 40,
    "original_index_sha256_unchanged": sha(ROOT / INDEX),
    "original_worked_source_sha256": sha(B / "WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json"),
    "proposed_new_canonical_source_records_accepted": 0,
    "annual_measure_cells_fully_verified": False,
    "independent_real_human_event_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
