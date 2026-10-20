#!/usr/bin/env python3
"""Portable historic 1647/1659 Brethren source and 34-test extracted replay."""

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
REL = T + "/batches/B07ba/"
WEST = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-Brethren-1647-1659-22-Historical-Sources-B07ba-20261020.zip"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def downloads():
    x = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(x.stdout.strip()) if x.returncode == 0 and x.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


source = j(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
old = j(ROOT / WEST)
chinese = j(ROOT / CHINA)
assert old["records_count"] == accept["prior_Lilly"] == 12969
assert old["batches"][-1]["id"] == "B07az"
assert chinese["sum_source_annotations"] == 355
assert source["record_count"] == len(rules["rules"]) == 22
assert source["source_author_reports_sibling_count_brothers"] == 7
assert source["source_author_reports_sibling_count_sisters"] == 1
assert source["reported_sibling_count_independent_validation_count"] == 0
assert rules["real_human_blind_prediction_successes"] == 0
assert accept["next_R"] == "R12992"
assert (
    sha(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json")
    == (accept["source_notes_sha256"])
)
assert sha(B / "RULES.json") == accept["rules_sha256"]

names = [
    "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "TASK_SCOPE.json",
    "RECOVERY_CHECKPOINT_20261020.md",
    "build_b07ba_original_brethren.py",
    "test_b07ba_brethren_original.py",
    "build_b07ba_release.py",
    "prepare_b07ba_canonical.py",
]
files = {REL + n: B / n for n in names}
for parts in source["original_two_editions_four_source_page_images"].values():
    for item in parts.values():
        name = item["relative_original_source_image"]
        f = ROOT / name
        assert sha(f) == item["sha256"]
        assert f.stat().st_size == item["bytes"]
        files[name] = f
files[T + "/batches/B07az/ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json"] = (
    B.parent / "B07az/ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json"
)
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values())
manifest = {
    "batch": "B07ba",
    "first_original_1647_Wellcome_full_book_sha256": source[
        "full_original_1647_Wellcome_pdf_SHA256"
    ],
    "source_original_1647_and_1659_photographic_pages": 4,
    "original_brethren_chapter_printed_folios": [751, 752],
    "new_historical_annotations": 22,
    "original_source_author_reported_siblings": [7, 1],
    "original_author_prior_Ptolemy_rule_suggests_few": True,
    "ex_post_reconciliation_not_blind_prediction": True,
    "source_historic_sibling_reports_independently_verified": False,
    "Lilly_if_admitted": 12991,
    "next_original_chapter": "CLXXIX Of Parents",
    "Chinese_V7_retained": 355,
    "human_predicted_outcomes_validated": 0,
    "runtime_promotions": 0,
    "members": {k: {"sha256": sha(v), "bytes": v.stat().st_size} for k, v in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
temp = folder / (NAME + ".building")
assert not temp.exists()
with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for key, file in files.items():
        z.write(file, "B07ba-root/" + key)
    z.writestr(
        "B07ba-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07ba-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, item in manifest["members"].items():
        f = root / name
        assert sha(f) == item["sha256"] and f.stat().st_size == item["bytes"], name
    r = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07ba_brethren_original.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=75,
    )
    assert r.returncode == 0, r.stdout + "\n" + r.stderr
    count = re.search(r"Ran (\d+) tests", r.stderr)
    assert count and int(count.group(1)) == 34, r.stderr
    assert "skipped" not in r.stderr
os.replace(temp, archive)
receipt = {
    "batch": "B07ba",
    "status": "ORIGINAL_BRETHREN_22_SOURCE_NOTES_34_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_SHA256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_members": len(files),
    "CRC_passed": True,
    "member_SHA256_and_exact_bytes_passed": True,
    "independent_archive_extraction_34_tests_passed": True,
    "source_SHA256": sha(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "old_Western_index_SHA256": sha(ROOT / WEST),
    "Chinese_V7_index_SHA256": sha(ROOT / CHINA),
    "new_source_only_annotations": 22,
    "human_predictive_validations": 0,
    "runtime_promotions": 0,
    "remotely_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
