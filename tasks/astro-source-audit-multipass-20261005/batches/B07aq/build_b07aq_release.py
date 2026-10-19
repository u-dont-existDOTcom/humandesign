#!/usr/bin/env python3
"""Portable original 1647/1659 CLXIX source with the omitted eleventh house.

CRC and exact-byte/SHA verification, then 35 tests in an independent ZIP
extraction. A checked historical book witness is not a validated prediction.
"""

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
REL = T + "/batches/B07aq/"
INDEX = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-CLXIX-Missing-11th-House-B07aq-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    q = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    p = Path(q.stdout.strip()) if q.returncode == 0 and q.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


original = j(B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json")
proof = j(B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
west = j(ROOT / INDEX)
china = j(ROOT / CHINA)
assert west["records_count"] == 12704
assert west["batches"][-1]["id"] == "B07ap"
assert china["sum_source_annotations"] == 355
assert original["source_original_1647_and_1659_both_contain_11th"]
assert original["secondary_modern_html_transcription_omits_house11"]
assert original["new_documentary_source_notes"] == 21
assert original["first_CLXIX_physical_text_span_covered"]
assert not original["full_independent_expert_critical_edition_verified"]
assert len(proof["source_row_proofs"]) == 21
assert rules["record_count"] == 21
assert accept["source_notes_sha256"] == sha(
    B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json"
)
assert accept["source_witness_sha256"] == sha(B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json")
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert accept["next_R"] == "R12726"
assert original["actual_human_predictive_validations"] == original["runtime_promotions"] == 0

names = [
    "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json",
    "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json",
    "SECONDARY_CLXIX_NAVIGATOR_OMITS_ELEVENTH.txt",
    ".gitattributes",
    "RULES.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_original_clxix_house_sources.py",
    "test_b07aq_original_clxix_houses.py",
    "build_b07aq_release.py",
    "prepare_b07aq_canonical.py",
]
files = {REL + n: B / n for n in names}
for entry in original["source_six_original_primary_images"].values():
    relative = entry["relative_file"]
    files[relative] = ROOT / relative
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values()), [
    name for name, file in files.items() if not file.is_file()
]
for row in original["source_six_original_primary_images"].values():
    path = ROOT / row["relative_file"]
    assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"]

manifest = {
    "batch": "B07aq",
    "source": "Original William Lilly first 1647 vs separately typeset 1659 CLXIX printed729–730",
    "first_1647_original_full_book_pdf_sha256": original["original_1647_full_pdf_SHA256"],
    "original_independent_edition_page_photo_count": 6,
    "original_twelve_house_source_positions_documented": True,
    "original_first_and_second_editions_contain_eleventh": True,
    "modern_secondary_omits_eleventh": True,
    "source_navigator_excerpt_SHA256": original["searchable_derivative_excerpt_sha256"],
    "new_historical_documentary_annotations": 21,
    "Lilly_if_accepted": 12725,
    "next_original_R": "R12726",
    "next_original_PDF": 765,
    "parallel_Chinese_V7_source_notes": 355,
    "full_classical_photo_critical_edition_confirmed": False,
    "historic_birth_chart_calculation_and_human_event_predictive_validity": False,
    "real_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
destination = folder / NAME
temp = folder / (NAME + ".building")
assert not temp.exists()
with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07aq-root/" + name)
    z.writestr(
        "B07aq-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07aq-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, data in manifest["members"].items():
        p = root / name
        assert p.stat().st_size == data["bytes"], name
        assert sha(p) == data["sha256"], name
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07aq_original_clxix_houses.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    m = re.search(r"Ran (\d+) tests", proc.stderr)
    assert m and int(m.group(1)) == 35, proc.stderr
    assert "skipped" not in proc.stderr
os.replace(temp, destination)
receipt = {
    "batch": "B07aq",
    "status": "CLXIX_11TH_HOUSE_RESTORED_TWO_ORIGINAL_PRINTS_35_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(destination),
    "archive_bytes": destination.stat().st_size,
    "archive_members": len(files),
    "CRC_passed": True,
    "all_members_SHA256_and_exact_bytes_passed": True,
    "independent_archive_test_replay_passed": True,
    "source_tests_replayed": 35,
    "source_notes_sha256": sha(B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json"),
    "source_photo_witness_sha256": sha(B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "prior_Western_index_SHA256": sha(ROOT / INDEX),
    "prior_Chinese_V7_index_SHA256": sha(ROOT / CHINA),
    "new_historical_notes_if_accepted": 21,
    "original_1647_both_printings_eleventh_source_verified_by_one_reader": True,
    "real_human_prediction_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
