#!/usr/bin/env python3
"""Portable original printed Naibod source photo archive, 160-test replay."""

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
REL = TASK + "/batches/B07aj/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NAME = "Astrology-Lilly-1647-1659-Naibod-149-Original-Table-Rows-B07aj-20261019.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


data = j(B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
assert j(ROOT / WEST)["records_count"] == accept["Lilly_before"] == 12546
assert j(ROOT / CHINESE)["sum_source_annotations"] == 262
assert len(data["rows"]) == 149
assert len(rules["rules"]) == 21
assert data["source_minute_rows_visible"] == 59
assert data["missing_original_1647_printed_minute_labels"] == [27]
assert rules["human_prediction_validations"] == data["human_prediction_validations"] == 0
assert (
    sha(B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json")
    == (accept["source_crosswalk_SHA256"])
)
assert sha(B / "RULES.json") == accept["rules_SHA256"]

names = [
    "ACCEPTANCE.json",
    "RULES.json",
    "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_naibod_original_tables.py",
    "test_b07aj_naibod_table_source.py",
    "build_b07aj_release.py",
    "prepare_b07aj_partial_canonical.py",
]
files = {REL + n: B / n for n in names}
files[TASK + "/batches/B07x/NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json"] = (
    B.parent / "B07x/NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json"
)
files[TASK + "/batches/B07x/NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json"] = (
    B.parent / "B07x/NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json"
)
for key, record in data["source_image_witnesses_first_and_second_editions"].items():
    original_name = record["path"]
    file = ROOT / original_name
    assert sha(file) == record["sha256"], key
    files[original_name] = file
files[WEST] = ROOT / WEST
files[CHINESE] = ROOT / CHINESE
assert all(file.is_file() for file in files.values())
manifest = {
    "batch": "B07aj",
    "source": (
        "Lilly Christian Astrology 1647 first and independently typeset "
        "1659 editions, printed713–714"
    ),
    "original_1647_full_pdf_sha256": data["original_first_edition_full_pdf_SHA256"],
    "degree_source_rows": 90,
    "visible_source_minute_rows": 59,
    "original_minute27_unprinted": True,
    "original_minute1_uncertain_day_glyph": True,
    "source_historical_notes": 21,
    "Lilly_if_source_admitted": 12567,
    "Chinese_V5_retained": 262,
    "source_critical_all_rows_verified_by_separate_second_reader": False,
    "full_CLXVI_source_chapter_done": False,
    "human_predictive_successes": 0,
    "runtime_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
target = folder / NAME
tmp = folder / (NAME + ".building")
assert not tmp.exists()
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07aj-root/" + name)
    z.writestr(
        "B07aj-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(tmp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07aj-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        file = root / name
        assert file.stat().st_size == meta["bytes"]
        assert sha(file) == meta["sha256"]
    test = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07aj_naibod_table_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=75,
    )
    assert test.returncode == 0, test.stdout + "\n" + test.stderr
    m = re.search(r"Ran (\d+) tests", test.stderr)
    assert m and int(m.group(1)) == 160, test.stderr
    assert "skipped" not in test.stderr
os.replace(tmp, target)
receipt = {
    "batch": "B07aj",
    "status": "ORIGINAL_1647_1659_NAIBOD_149_SOURCE_ROWS_160_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(target),
    "archive_bytes": target.stat().st_size,
    "member_count": len(files),
    "archive_crc_passed": True,
    "archive_members_sha_bytes_verified": True,
    "extracted_test_replay_passed": True,
    "test_count": 160,
    "source_crosswalk_sha256": sha(B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "old_Western_source_SHA256": sha(ROOT / WEST),
    "Chinese_V5_SHA256": sha(ROOT / CHINESE),
    "new_source_records_if_admitted": 21,
    "complete_original_first_CLXVI": False,
    "empirical_human_predictions": 0,
    "runtime_model_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
