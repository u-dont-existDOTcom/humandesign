#!/usr/bin/env python3
"""Portable source-only original first/second Lilly CLXVIII photography archive."""

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
REL = T + "/batches/B07ap/"
INDEX = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-Profection-Judgment-Source-B07ap-20261019.zip"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


source = j(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
witness = j(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json")
assert j(ROOT / INDEX)["records_count"] == 12671
assert j(ROOT / CHINA)["sum_source_annotations"] == 355
assert len(source["rows"]) == rules["record_count"] == 33
assert accept["Lilly_if_accepted"] == 12704
assert accept["next_R"] == "R12705"
assert len(source["image_sources"]) == 8
assert source["human_predictions_validated"] == source["runtime_promotions"] == 0
assert not source["full_expert_diplomatic_comparison_completed"]
assert accept["records_sha256"] == sha(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json")
assert accept["witness_sha256"] == sha(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json")
assert accept["rules_sha256"] == sha(B / "RULES.json")

names = [
    "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json",
    "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "TASK_SCOPE.json",
    "build_clxviii_source_rules.py",
    "test_b07ap_original_source.py",
    "build_b07ap_release.py",
    "prepare_b07ap_canonical.py",
]
names += [
    str(f.relative_to(B))
    for f in sorted((B / "evidence").glob("*.jpg"))
    if not f.name.startswith("reading-")
]
files = {REL + name: B / name for name in names}
files[T + "/batches/B07ao/ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json"] = (
    B.parent / "B07ao/ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json"
)
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [k for k, f in files.items() if not f.is_file()]
for key, image in witness["full_image_sha_and_exact_bytes"].items():
    file = B / image["relative_file"]
    assert file.is_file() and sha(file) == image["photo_sha256"], key
    assert file.stat().st_size == image["source_exact_bytes"], key
manifest = {
    "batch": "B07ap",
    "source": "Lilly original first 1647 and typeset second 1659 CLXVIII printed726–729",
    "first_original_Wellcome_book_PDF_SHA256": source["original_full_Wellcome_1647_PDF_SHA256"],
    "source_original_image_count": 8,
    "source_historical_document_notes": 33,
    "starting_Lilly_source_notes": 12671,
    "Lilly_if_accepted": 12704,
    "parallel_Chinese_V7_unchanged": 355,
    "next_1647_chapter": "CLXIX",
    "next_original_R": "R12705",
    "case_Pisces6_37_jupiter_until_June29_source": True,
    "historical_1647_annual_lord_sample_time": [284, 16, 28],
    "original_all_historical_judgment_methods_engineered": False,
    "historical_human_predictive_validation": 0,
    "runtime_promotions": 0,
    "members": {k: {"sha256": sha(v), "bytes": v.stat().st_size} for k, v in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
out = folder / NAME
temp = folder / (NAME + ".building")
assert not temp.exists()
with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07ap-root/" + name)
    z.writestr(
        "B07ap-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07ap-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        f = root / name
        assert f.stat().st_size == meta["bytes"], name
        assert sha(f) == meta["sha256"], name
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07ap_original_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    match = re.search(r"Ran (\d+) tests", p.stderr)
    assert match and int(match.group(1)) == 46, p.stderr
    assert "skipped" not in p.stderr
os.replace(temp, out)
receipt = {
    "batch": "B07ap",
    "status": "LILLY_1647_CLXVIII_SOURCE_33_DOCUMENTARY_NOTES_46_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "source_member_count": len(files),
    "CRC_passed": True,
    "SHA_exact_bytes_passed": True,
    "independent_archive_replay_passed": True,
    "tests": 46,
    "source_SHA256": sha(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json"),
    "witness_SHA256": sha(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "old_Western_SHA256": sha(ROOT / INDEX),
    "old_Chinese_V7_SHA256": sha(ROOT / CHINA),
    "source_notes_if_accepted": 33,
    "historical_calendar_engine_validated": False,
    "actual_human_prediction_successes": 0,
    "runtime_model_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
