#!/usr/bin/env python3
"""Portable 1647/1659 profection source samples, 40 tests after ZIP extraction."""

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
T = "tasks/astro-source-audit-multipass-20261005"
REL = T + "/batches/B07an/"
INDEX = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-Profection-Timing-Source-B07an-20261019.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    dir = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if dir is not None and dir.is_dir() and dir.resolve() != Path.home().resolve():
        return dir
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


doc = j(B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json")
proof = j(B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
old = j(ROOT / INDEX)
chinese = j(ROOT / CHINA)
assert old["records_count"] == accept["prior_Lilly"] == 12625
assert old["batches"][-1]["id"] == "B07am"
assert chinese["sum_source_annotations"] == 355
assert len(doc["source_notes"]) == len(rules["rules"]) == 24
assert len(doc["source_images"]) == len(proof["primary_photographic_binary_witnesses"]) == 8
assert len(doc["source_sample_one_reader_table_rows"]) == 9
assert accept["next_R"] == "R12650"
assert doc["independent_real_person_predictions_validated"] == 0
assert not doc["source_full_30_and_60_digit_columns_critically_collated"]
assert sha(B / "RULES.json") == accept["rules_SHA256"]
assert (
    sha(B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json")
    == (accept["historical_photographic_data_SHA256"])
)
assert (
    sha(B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json")
    == (accept["source_photo_and_arithmetic_witness_SHA256"])
)
names = [
    "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json",
    "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_original_profection_time_table_source.py",
    "test_b07an_original_profection_tables.py",
    "build_b07an_release.py",
    "prepare_b07an_partial_canonical.py",
]
names += [
    str(f.relative_to(B))
    for f in sorted((B / "evidence").glob("*.jpg"))
    if not f.name.startswith("reading_")
]
files = {REL + name: B / name for name in names}
files[T + "/batches/B07am/RULES.json"] = B.parent / "B07am/RULES.json"
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [k for k, f in files.items() if not f.is_file()]
for key, row in doc["source_images"].items():
    file = B / row["file"]
    assert sha(file) == row["source_image_SHA256"], key
    assert file.stat().st_size == row["source_image_exact_bytes"], key
manifest = {
    "batch": "B07an",
    "source": (
        "Lilly Christian Astrology 1647 first edition and separately "
        "typeset 1659 original printed pages721–724"
    ),
    "original_1647_Wellcome_full_pdf_sha256": doc["original_full_1647_PDF_sha256"],
    "original_1647_and_1659_full_page_image_count": 8,
    "source_original_sample_table_rows": 9,
    "source_full_original_30_degree_and_60_minute_rows_expert_verified": False,
    "source_full_calendar_day_grid_expert_verified": False,
    "third_source_6degree23_uses_minute37_not23": True,
    "original_printed_third_case_total_dhm": [80, 13, 21],
    "source_recomputed_using_actual_target_residual_dhm": [77, 17, 11],
    "source_historical_record_count": 24,
    "Lilly_after_if_accepted": 12649,
    "Chinese_V7_retained": 355,
    "next_record": "R12650",
    "actual_birth_calendar_and_person_prediction_validated": False,
    "human_predictive_validations": 0,
    "runtime_model_promotions": 0,
    "members": {k: {"sha256": sha(v), "bytes": v.stat().st_size} for k, v in files.items()},
}
dir = downloads()
dir.mkdir(parents=True, exist_ok=True)
archive = dir / NAME
tmp = dir / (NAME + ".building")
assert not tmp.exists(), tmp
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07an-root/" + name)
    z.writestr(
        "B07an-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(tmp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07an-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for k, r in manifest["members"].items():
        f = root / k
        assert sha(f) == r["sha256"], k
        assert f.stat().st_size == r["bytes"], k
    test = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07an_original_profection_tables.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert test.returncode == 0, test.stdout + "\n" + test.stderr
    count = re.search(r"Ran (\d+) tests", test.stderr)
    assert count and int(count.group(1)) == 40, test.stderr
    assert "skipped" not in test.stderr
os.replace(tmp, archive)
receipt = {
    "batch": "B07an",
    "status": "ORIGINAL_1647_1659_PROFECTION_TABLES_THREE_CASES_40_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_members": len(files),
    "CRC_passed": True,
    "member_SHA256_bytes_passed": True,
    "independent_ZIP_extraction_test_replay_passed": True,
    "source_tests_replayed": 40,
    "source_SHA256": sha(B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json"),
    "witness_SHA256": sha(B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "old_Western_index_SHA256": sha(ROOT / INDEX),
    "Chinese_V7_source_index_SHA256": sha(ROOT / CHINA),
    "new_source_documentary_notes": 24,
    "original_degree_minute_calendar_tables_fully_collated": False,
    "real_human_outcome_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
