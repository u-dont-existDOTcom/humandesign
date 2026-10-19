#!/usr/bin/env python3
"""Portable original Lilly CLXVII final-source photograph and test proof."""

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
REL = T + "/batches/B07ao/"
WEST = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-CLXVII-End-Profections-B07ao-20261019.zip"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def downloads():
    a = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(a.stdout.strip()) if a.returncode == 0 and a.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    fr = Path.home() / "Téléchargements"
    return fr if fr.is_dir() else Path.home()


doc = j(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
assert j(ROOT / WEST)["records_count"] == 12649
assert j(ROOT / CHINA)["sum_source_annotations"] == 355
assert doc["historical_claims_source_count"] == rules["record_count"] == 22
assert accept["Lilly_if_accepted"] == 12671
assert accept["next_R"] == "R12672"
assert doc["verified_life_event_predictions"] == doc["runtime_promotions"] == 0
assert sha(B / "RULES.json") == accept["rules_sha256"]
assert sha(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json") == accept["records_sha256"]
names = [
    "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_clxvii_final_boundary.py",
    "test_b07ao_source_and_boundary.py",
    "build_b07ao_release.py",
    "prepare_b07ao_canonical.py",
]
names += [str(f.relative_to(B)) for f in sorted((B / "evidence").glob("*.jpg"))]
files = {REL + name: B / name for name in names}
files[T + "/batches/B07an/ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json"] = (
    B.parent / "B07an/ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json"
)
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [k for k, f in files.items() if not f.is_file()]
for name, entry in doc["source_photo_images"].items():
    file = B / entry["path"]
    assert sha(file) == entry["sha256"], name
    assert file.stat().st_size == entry["byte_length"], name
manifest = {
    "batch": "B07ao",
    "source": "Lilly original 1647 and separately typeset 1659 printed725–726",
    "original_full_Wellcome_1647_PDF_SHA256": doc["source_full_first_1647_Wellcome_PDF_SHA256"],
    "source_original_two_edition_four_photo_witnesses": True,
    "prefetched_1647_printed727_729_not_source_critically_read": True,
    "historical_source_annotations": 22,
    "Lilly_after_if_accepted": 12671,
    "Western_Ptolemy_retained": 1066,
    "Chinese_V7_retained": 355,
    "next_historical_source": "R12672",
    "next_original_1647_printed_chapter": "CLXVIII",
    "physical_CLXVII_source_coverage_complete": True,
    "original_table_all_values_expert_critically_collated": False,
    "original_human_prediction_validations": 0,
    "astrology_runtime_promotions": 0,
    "members": {k: {"sha256": sha(f), "bytes": f.stat().st_size} for k, f in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
out = folder / NAME
tmp = folder / (NAME + ".building")
assert not tmp.exists()
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07ao-root/" + name)
    z.writestr(
        "B07ao-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(tmp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07ao-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        file = root / name
        assert file.stat().st_size == meta["bytes"], name
        assert sha(file) == meta["sha256"], name
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07ao_source_and_boundary.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    k = re.search(r"Ran (\d+) tests", p.stderr)
    assert k and int(k.group(1)) == 33, p.stderr
    assert "skipped" not in p.stderr
os.replace(tmp, out)
receipt = {
    "batch": "B07ao",
    "status": "FIRST_ORIGINAL_CLXVII_SOURCE_END_22_HISTORY_RECORDS_33_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "archive_members": len(files),
    "CRC_passed": True,
    "all_member_SHA256_sizes_passed": True,
    "extracted_test_replay_passed": True,
    "portable_source_tests": 33,
    "source_SHA256": sha(B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "old_Western_SHA256": sha(ROOT / WEST),
    "old_Chinese_V7_SHA256": sha(ROOT / CHINA),
    "new_historical_source_notes": 22,
    "full_critical_original_tables_verified": False,
    "actual_real_human_predictions": 0,
    "astrology_runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
