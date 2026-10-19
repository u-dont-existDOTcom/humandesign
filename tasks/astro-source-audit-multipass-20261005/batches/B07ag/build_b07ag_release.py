#!/usr/bin/env python3
"""Build portable source-only partial CLXVI owner archive and replay 43 tests."""

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
REL = TASK + "/batches/B07ag/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NAME = "Astrology-Lilly-CLXVI-Opening-1647-1659-Partial-29-B07ag-20261019.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def read(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


notes = read(B / "CLXVI_OPENING_SOURCE_PHOTO_29_NOTES_V1.json")
proof = read(B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json")
rules = read(B / "RULES.json")
accept = read(B / "ACCEPTANCE.json")
assert len(notes["records"]) == len(rules["rules"]) == 29
assert len(proof["photographic_source_note_receipts"]) == 29
assert accept["prior_Lilly"] == read(ROOT / INDEX)["records_count"] == 12472
assert accept["parallel_Chinese_V5"] == read(ROOT / CHINESE)["sum_source_annotations"] == 262
assert accept["rules_sha256"] == sha(B / "RULES.json")
assert accept["source_witness_sha256"] == sha(
    B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json"
)
assert accept["lilly_after"] == 12501 and accept["next_original_source_id"] == "R12502"
assert rules["empirical_real_person_predictions_validated"] == rules["runtime_promotions"] == 0
assert proof["original_printing_1647_next_day_sun_longitude"] == [7, 36]
assert proof["second_printing_1659_next_day_sun_longitude"] == [7, 36]
assert proof["modern_derivative_transcription_next_day_sun_longitude"] == [7, 37]

names = [
    "ACCEPTANCE.json",
    "CLXVI_OPENING_SOURCE_PHOTO_29_NOTES_V1.json",
    "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json",
    "RULES.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "audit_b07ag_opening_sources.py",
    "build_partial_clxvi_source_rules.py",
    "test_b07ag_partial_original_source.py",
    "build_b07ag_release.py",
    "prepare_b07ag_partial_canonical.py",
]
files = {REL + name: B / name for name in names}
files[TASK + "/batches/B07x/ORIGINAL_SOURCE_WINDOW_V1.json"] = (
    B.parent / "B07x/ORIGINAL_SOURCE_WINDOW_V1.json"
)
files[TASK + "/batches/B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json"] = (
    B.parent / "B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json"
)
for frame in (742, 743, 744):
    key = TASK + f"/batches/B07x/evidence/pdf_1647-{frame}.jpg"
    files[key] = B.parent / "B07x/evidence" / f"pdf_1647-{frame}.jpg"
files[TASK + "/batches/B07ae/evidence/second_edition_1659_djvu_page_739.jpg"] = (
    B.parent / "B07ae/evidence/second_edition_1659_djvu_page_739.jpg"
)
files[INDEX] = ROOT / INDEX
files[CHINESE] = ROOT / CHINESE
assert all(file.is_file() for file in files.values()), [
    name for name, file in files.items() if not file.is_file()
]
for item in proof["first_edition_source_photographs"].values():
    assert sha(ROOT / item["file"]) == item["sha256"]
assert (
    sha(ROOT / proof["independent_1659_typeset_photo"]["file"])
    == (proof["independent_1659_typeset_photo"]["sha256"])
)
manifest = {
    "batch": "B07ag",
    "scope": "First three source pages of original Lilly CLXVI, not full chapter",
    "source": "William Lilly Christian Astrology 1647 original Wellcome b30338724",
    "original_full_pdf_sha256": proof["full_1647_original_pdf_sha256"],
    "original_first_three_frames": [742, 743, 744],
    "separate_original_typeset_1659_comparator": True,
    "original_print_next_day_sun_longitude_degrees_minutes": [7, 36],
    "searchable_text_mistranscription": [7, 37],
    "partial_source_historical_rule_count": 29,
    "before_Lilly_historical_records": 12472,
    "if_accepted_Lilly_historical_records": 12501,
    "next_unaccepted_Lilly_record": "R12502",
    "full_CLXVI_chapter_accepted": False,
    "original_1647_direction_to_time_engine_complete": False,
    "parallel_Chinese_V5_historical_records_unchanged": 262,
    "real_person_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07ag-root/" + name)
    z.writestr(
        "B07ag-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    restored = Path(td) / "B07ag-root"
    assert read(restored / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        file = restored / name
        assert file.stat().st_size == meta["bytes"]
        assert sha(file) == meta["sha256"]
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(restored / REL),
            "-p",
            "test_b07ag_partial_original_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=80,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    m = re.search(r"Ran (\d+) tests", result.stderr)
    assert m and int(m.group(1)) == 43, result.stderr
    assert "skipped" not in result.stderr
receipt = {
    "batch": "B07ag",
    "status": "1647_1659_CLXVI_PARTIAL_29_SOURCE_43_PORTABLE_TESTS_PASS",
    "archive_filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "crc_passed": True,
    "all_member_SHA256_and_sizes_passed": True,
    "independently_extracted_tests_passed": True,
    "portable_test_replays": 43,
    "rules_sha256": sha(B / "RULES.json"),
    "source_witness_sha256": sha(B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json"),
    "prior_Lilly_source_index_sha256": sha(ROOT / INDEX),
    "parallel_Chinese_V5_source_index_sha256": sha(ROOT / CHINESE),
    "new_history_notes_if_accepted": 29,
    "fully_collated_original_chapter": False,
    "genuine_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
