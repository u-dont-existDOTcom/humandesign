#!/usr/bin/env python3
"""ZIP, CRC, SHA and independently replay original 1647 Part Fortune source tests."""

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
REL = TASK + "/batches/B07w/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
FILENAME = "Astrology-Lilly-Printed-CLXV-Part-Fortune-Directions-1647-20261018.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


win = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
accepted = load(B / "ACCEPTANCE.json")
old = B / "recovery" / "INDEX_BEFORE_B07w.json"
index_before = old if old.exists() else ROOT / INDEX
assert sha(index_before) == win["parent_index_sha256"]
assert load(index_before)["records_count"] == 12268
assert load(ROOT / CHINA)["sum_source_annotations"] == 97
assert rules["record_count"] == accepted["new_historical_annotations"] == 204
assert (rules["substantive"], rules["following_navigation"]) == (201, 3)
assert rules["empirical_human_validations"] == rules["runtime_promotions"] == 0
assert sha(B / "RULES.json") == accepted["rules_sha256"]

names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "CONTINUATION_HANDOFF_ACCEPTED_20261018.md",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "SOURCE_PART_01_FORTUNA_SATURN_SUN_20261018.json",
    "SOURCE_PART_02_FORTUNA_VENUS_NODES_20261018.json",
    "SOURCE_PART_03_FORTUNA_STARS_HOUSES_20261018.json",
    "FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json",
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "prepare_original_b07w_window.py",
    "freeze_b07w_documentary.py",
    "test_b07w_documentary.py",
    "prepare_canonical_b07w.py",
    "build_b07w_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(737, 744)]
files = {REL + name: B / name for name in names}
files[INDEX] = index_before
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values())
manifest = {
    "batch": "B07w",
    "source": "William Lilly original 1647 first-edition Christian Astrology",
    "original_full_source_pdf_sha256": win["full_pdf_original_sha256"],
    "printed_chapter": "CLXV",
    "historical_source_annotations": 204,
    "substantive": 201,
    "following_navigation": 3,
    "reversible_original_photo_groups": 35,
    "body_original_pdf_frames": list(range(737, 743)),
    "source_photos": 7,
    "star_headings_without_numerical_coordinates": 3,
    "next_original_printed_chapter": "CLXVI",
    "retained_previous_lilly_index": 12268,
    "retained_Ptolemy": 1066,
    "retained_chinese_histories": 97,
    "independent_human_predictions_validated": 0,
    "runtime_rules_promoted": 0,
    "full_original_pdf_not_in_archive": True,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / FILENAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07w-root/" + name)
    z.writestr(
        "B07w-root/RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B07w-root"
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
            "test_b07w_documentary.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    match = re.search(r"Ran (\d+) tests", proc.stderr)
    assert match and int(match.group(1)) == 62, proc.stderr
    assert "skipped" not in proc.stderr
receipt = {
    "batch": "B07w",
    "status": "ORIGINAL_1647_CLXV_PORTABLE_ARCHIVE_CRC_SHA_62_TEST_REPLAY_PASS",
    "filename": FILENAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "sha256_and_bytes_passed": True,
    "independent_extraction_passed": True,
    "total_replayed_tests": 62,
    "rules_sha256": sha(B / "RULES.json"),
    "star_table_sha256": sha(B / "FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json"),
    "previous_index_sha256": sha(index_before),
    "new_historical_records_if_accepted": 204,
    "individual_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
