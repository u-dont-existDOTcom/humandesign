#!/usr/bin/env python3
"""Portable historical source-only original CLXVII opening; 24 extracted tests."""

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
REL = T + "/batches/B07am/"
INDEX = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NAME = "Astrology-Lilly-1647-CLXVII-Effects-Opening-14-Source-B07am-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    dest = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if dest is not None and dest.is_dir() and dest.resolve() != Path.home().resolve():
        return dest
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


doc = j(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
assert j(ROOT / INDEX)["records_count"] == 12611
assert j(ROOT / CHINA)["sum_source_annotations"] == 262
assert len(doc["records"]) == len(rules["rules"]) == 14
assert rules["record_count"] == 14
assert accept["next_R"] == "R12626"
assert sha(B / "RULES.json") == accept["rules_SHA256"]
assert sha(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json") == accept["notes_SHA256"]
assert rules["runtime_promotions"] == 0
files = {
    REL + n: B / n
    for n in (
        "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json",
        "RULES.json",
        "ACCEPTANCE.json",
        "build_b07am_opening_rules.py",
        "test_b07am_profections_effects_opening.py",
        "build_b07am_release.py",
        "prepare_b07am_canonical.py",
        "ORIGINAL_SOURCE_REVIEW_20261019.md",
        "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
        "evidence/original_1647_pdf-753.jpg",
        "evidence/original_1647_pdf-754.jpg",
    )
}
files[T + "/batches/B07al/evidence/1647_original_pdf-752.jpg"] = (
    B.parent / "B07al/evidence/1647_original_pdf-752.jpg"
)
files[T + "/batches/B07al/RULES.json"] = B.parent / "B07al/RULES.json"
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [n for n, f in files.items() if not f.is_file()]
for frame, hash_expected in doc["original_source_photo_shas"].items():
    image = (
        B.parent / "B07al/evidence/1647_original_pdf-752.jpg"
        if frame == "752"
        else B / "evidence" / f"original_1647_pdf-{frame}.jpg"
    )
    assert sha(image) == hash_expected
manifest = {
    "batch": "B07am",
    "original_source_pdf_sha256": doc["original_1647_pdf_SHA256"],
    "original_source_first_edition_pdf_frames": [752, 753, 754],
    "source_only_historical_annotations": 14,
    "Lilly_source_count_before": 12611,
    "Lilly_source_count_if_accepted": 12625,
    "parallel_Chinese_source_count_unchanged": 262,
    "chapter_CLXVII_complete": False,
    "original_source_p721_conversion_table_admitted": False,
    "empirical_human_prediction_successes": 0,
    "runtime_promotions": 0,
    "members": {n: {"sha256": sha(f), "bytes": f.stat().st_size} for n, f in files.items()},
}
out = downloads()
out.mkdir(exist_ok=True, parents=True)
archive = out / NAME
tmp = out / (NAME + ".building")
assert not tmp.exists()
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07am-root/" + name)
    z.writestr(
        "B07am-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(tmp) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07am-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, v in manifest["members"].items():
        f = root / name
        assert f.stat().st_size == v["bytes"]
        assert sha(f) == v["sha256"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07am_profections_effects_opening.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=80,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    m = re.search(r"Ran (\d+) tests", p.stderr)
    assert m and int(m.group(1)) == 24, p.stderr
os.replace(tmp, archive)
receipt = {
    "batch": "B07am",
    "status": "ORIGINAL_1647_CLXVII_14_OPENING_SOURCE_24_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "CRC_passed": True,
    "member_shas_and_sizes_passed": True,
    "independent_archive_replayed_24_tests": True,
    "source_sha256": sha(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "original_index_sha256": sha(ROOT / INDEX),
    "Chinese_V5_sha256": sha(ROOT / CHINA),
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
