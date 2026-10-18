#!/usr/bin/env python3
"""Reproducible portable archive, independent CRC, member SHA and 62-test replay."""

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
REL = TASK + "/batches/B07t/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
ARCHIVE_NAME = "Astrology-Lilly-Printed-CLXIII-Sun-Fixed-Stars-1647-20261018.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    proc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    return (
        Path(proc.stdout.strip())
        if proc.returncode == 0 and proc.stdout.strip()
        else Path.home() / "Téléchargements"
    )


window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
accepted = load(B / "ACCEPTANCE.json")
old = B / "recovery" / "INDEX_BEFORE_B07t.json"
index_before = old if old.exists() else ROOT / INDEX
assert window["parent_lilly_index_sha256"] == sha(index_before)
assert load(index_before)["records_count"] == 11721
assert load(ROOT / CHINA)["sum_source_annotations"] == 97
assert rules["record_count"] == accepted["new_historical_annotations"] == 104
assert accepted["rules_sha256"] == sha(B / "RULES.json")
assert accepted["fixed_star_table_sha256"] == sha(
    B / "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json"
)
assert rules["empirical_human_validations"] == rules["runtime_promotions"] == 0

names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "SOURCE_PART_01_RIGEL_TO_LIONS_HEART_20261018.json",
    "SOURCE_PART_02_HERCULES_TO_CRATCH_20261018.json",
    "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json",
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "freeze_b07t_documentary.py",
    "test_b07t_documentary.py",
    "test_b07t_source_window.py",
    "prepare_original_b07t_source_window.py",
    "build_b07t_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in (723, 724, 725)]
files = {REL + name: B / name for name in names}
files[INDEX] = index_before
files[CHINA] = ROOT / CHINA
assert all(p.is_file() for p in files.values())
manifest = {
    "batch": "B07t",
    "source": "William Lilly 1647 Christian Astrology original Wellcome b30338724",
    "full_original_source_sha256": window["full_source_894_frame_pdf_sha256"],
    "historical_source_records": 104,
    "substantive": 102,
    "next_navigation": 2,
    "reversible_groups": 13,
    "stellar_effect_passages": 11,
    "stellar_entries": 13,
    "frozen_parent_index_record_count": 11721,
    "chinese_history_count_unchanged": 97,
    "independent_human_predictions_validated": 0,
    "model_runtime_promotions": 0,
    "source_only_not_complete_diplomatic_transcription": True,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / ARCHIVE_NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07t-root/" + name)
    z.writestr(
        "B07t-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
counts = []
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B07t-root"
    assert load(root / "RELEASE_MANIFEST.json") == manifest
    for name, specification in manifest["members"].items():
        file = root / name
        assert file.stat().st_size == specification["bytes"]
        assert sha(file) == specification["sha256"]
    for name, expected in (
        ("test_b07t_documentary.py", 53),
        ("test_b07t_source_window.py", 9),
    ):
        proc = subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", str(root / REL), "-p", name, "-q"],
            text=True,
            capture_output=True,
            timeout=40,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        result = re.search(r"Ran (\d+) tests", proc.stderr)
        assert result and int(result.group(1)) == expected
        assert "skipped" not in proc.stderr
        counts.append(expected)
assert counts == [53, 9]
receipt = {
    "batch": "B07t",
    "status": "ORIGINAL_SOURCE_PORTABLE_CRC_SHA_62_REPLAY_PASS",
    "owner_archive_filename": ARCHIVE_NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "crc_passed": True,
    "sha256_and_bytes_passed": True,
    "independent_extraction_passed": True,
    "replayed_original_documentary_tests": 53,
    "replayed_original_window_tests": 9,
    "total_replayed": 62,
    "original_record_rule_sha256": sha(B / "RULES.json"),
    "original_stellar_table_sha256": sha(B / "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json"),
    "previous_index_sha256": sha(index_before),
    "new_historical_annotations_if_accepted": 104,
    "empirical_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
