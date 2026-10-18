#!/usr/bin/env python3
"""Freeze and mechanically replay a portable Lilly CLXIIII original-source ZIP."""

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
REL = TASK + "/batches/B07u/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
FILENAME = "Astrology-Lilly-Printed-CLXIIII-Moon-Promittors-1647-20261018.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    proc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        proc.stdout.strip()
        if proc.returncode == 0 and proc.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


window = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
rules = load(B / "RULES.json")
accepted = load(B / "ACCEPTANCE.json")
previous = B / "recovery" / "INDEX_BEFORE_B07u.json"
old = previous if previous.exists() else ROOT / INDEX
assert sha(old) == window["previous_index_sha256"]
assert load(old)["records_count"] == accepted["prior_lilly"] == 11825
assert load(ROOT / CHINA)["sum_source_annotations"] == 97
assert rules["record_count"] == accepted["new_historical_annotations"] == 343
assert rules["substantive"] == accepted["substantive"] == 341
assert rules["following_navigation"] == accepted["following_navigation"] == 2
assert sha(B / "RULES.json") == accepted["rules_sha256"]
assert rules["independent_human_outcomes_validated"] == rules["runtime_promotions"] == 0

names = [
    "ORIGINAL_SOURCE_WINDOW_V1.json",
    "PLAN_AND_CONTINUATION_PROVISIONAL_20261018.md",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "SOURCE_PART_01_SATURN_JUPITER_20261018.json",
    "SOURCE_PART_02_MARS_SUN_20261018.json",
    "SOURCE_PART_03_VENUS_MERCURY_20261018.json",
    "SOURCE_PART_04_NODES_HOUSES_SEAM_20261018.json",
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "HISTORICAL_NONPROMOTION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "prepare_original_b07u_source_window.py",
    "freeze_b07u_documentary.py",
    "test_b07u_documentary.py",
    "test_b07u_source_window.py",
    "prepare_canonical_b07u.py",
    "build_b07u_release.py",
] + [f"evidence/pdf_1647-{i}.jpg" for i in range(725, 737)]
files = {REL + name: B / name for name in names}
files[INDEX] = old
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [n for n, f in files.items() if not f.is_file()]
manifest = {
    "schema": "LILLY_ORIGINAL_1647_CLXIIII_DOCUMENTARY_SOURCE_ZIP_V1",
    "batch": "B07u",
    "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
    "original_894_frame_pdf_sha256": window["full_source_pdf_sha256"],
    "historical_source_notes": 343,
    "substantive": 341,
    "next_heading_navigation": 2,
    "reversible_source_groups": 41,
    "body_pdf_frames": list(range(725, 736)),
    "photo_witness_frame_count": 12,
    "next_heading_is_UNNUMBERED": True,
    "following_source_heading_pdf": 735,
    "parent_lilly_record_count": 11825,
    "ptolemy_retained": 1066,
    "chinese_source_count": 97,
    "owner_public_domain_full_pdf_not_in_zip": True,
    "empirical_human_predictions_validated": 0,
    "runtime_models_promoted": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / FILENAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
    for name, path in files.items():
        zipped.write(path, "B07u-root/" + name)
    zipped.writestr(
        "B07u-root/RELEASE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
counts = []
with zipfile.ZipFile(archive) as zipped, tempfile.TemporaryDirectory() as tmp:
    assert zipped.testzip() is None
    zipped.extractall(tmp)
    root = Path(tmp) / "B07u-root"
    assert load(root / "RELEASE_MANIFEST.json") == manifest
    for name, info in manifest["members"].items():
        f = root / name
        assert f.stat().st_size == info["bytes"]
        assert sha(f) == info["sha256"]
    for test_name, expected in (
        ("test_b07u_documentary.py", 80),
        ("test_b07u_source_window.py", 28),
    ):
        cmd = [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            test_name,
            "-q",
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=50)
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
        match = re.search(r"Ran (\d+) tests", proc.stderr)
        assert match and int(match.group(1)) == expected, proc.stderr
        assert "skipped" not in proc.stderr, proc.stderr
        counts.append(expected)
assert counts == [80, 28]
receipt = {
    "batch": "B07u",
    "status": "ORIGINAL_CLXIIII_PHOTO_ZIP_CRC_SHA_108_TESTS_REPLAYED",
    "filename": FILENAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "sha256_and_bytes_passed": True,
    "independent_extraction_passed": True,
    "replayed_documentary_tests": 80,
    "replayed_source_window_tests": 28,
    "total_replayed_tests": 108,
    "rules_sha256": sha(B / "RULES.json"),
    "prior_index_sha256": sha(old),
    "new_source_notes_if_admitted": 343,
    "empirical_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
