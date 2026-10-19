#!/usr/bin/env python3
"""Hermetic ZIP of CLXXII original 1647/1659 two-page source and 38 tests."""

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
REL = TASK + "/batches/B07at/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-CLXXII-1646-Solar-Return-Opening-B07at-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    d = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if d is not None and d.is_dir() and d.resolve() != Path.home().resolve():
        return d
    fr = Path.home() / "Téléchargements"
    return fr if fr.is_dir() else Path.home()


source = load(B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json")
rules = load(B / "RULES.json")
accepted = load(B / "ACCEPTANCE.json")
assert load(ROOT / WEST)["records_count"] == 12764
assert load(ROOT / CHINA)["sum_source_annotations"] == 355
assert len(source["records"]) == rules["record_count"] == 24
assert source["independent_real_life_predictions_validated"] == 0
assert source["original_CLXXII_full_source_physical_span_read"] is False
assert (
    sha(B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json")
    == (accepted["source_photo_and_arithmetic_SHA256"])
)
assert sha(B / "RULES.json") == accepted["rules_SHA256"]

names = [
    "CONTINUATION_CHECKPOINT_PROVISIONAL_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "build_clxxii_solar_return_opening.py",
    "test_b07at_solar_return.py",
    "build_b07at_release.py",
    "prepare_b07at_canonical.py",
]
files = {REL + n: B / n for n in names}
for _, entry in source["documentary_witness_photos"].items():
    p = ROOT / entry["repository_path"]
    files[entry["repository_path"]] = p
    assert sha(p) == entry["raw_image_SHA256"]
    assert p.stat().st_size == entry["raw_image_bytes"]
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(p.is_file() for p in files.values()), [x for x, p in files.items() if not p.is_file()]
manifest = {
    "batch": "B07at",
    "source": "Lilly original 1647 and separately printed 1659 solar revolution p734–735",
    "original_wellcome_full_PDF_sha256": source["original_full_1647_book_PDF_SHA256"],
    "source_photographic_pages": 4,
    "source_historical_notes": 24,
    "Lilly_if_accepted": 12788,
    "Chinese_V7_unchanged": 355,
    "next_R": "R12789",
    "CLXXII_full_source_complete": False,
    "original_1646_true_solar_hour_birth_calendar_parity_verified": False,
    "independent_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "members": {n: {"sha256": sha(p), "bytes": p.stat().st_size} for n, p in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
target = folder / NAME
building = folder / (NAME + ".building")
assert not building.exists(), building
with zipfile.ZipFile(building, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, path in files.items():
        z.write(path, "B07at-root/" + name)
    z.writestr(
        "B07at-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(building) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B07at-root"
    assert load(root / "RELEASE_MANIFEST.json") == manifest
    for name, record in manifest["members"].items():
        f = root / name
        assert f.stat().st_size == record["bytes"]
        assert sha(f) == record["sha256"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root / REL),
            "-p",
            "test_b07at_solar_return.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=70,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    match = re.search(r"Ran (\d+) tests", p.stderr)
    assert match and int(match.group(1)) == 38, p.stderr
    assert "skipped" not in p.stderr
os.replace(building, target)
receipt = {
    "batch": "B07at",
    "status": "CLXXII_ORIGINAL_SOLAR_RETURN_24_NOTES_38_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(target),
    "archive_bytes": target.stat().st_size,
    "members": len(files),
    "CRC_passed": True,
    "member_SHA256_exact_bytes_passed": True,
    "independent_extraction_source_tests_passed": True,
    "portable_test_replays": 38,
    "source_sha256": sha(B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json"),
    "rules_sha256": sha(B / "RULES.json"),
    "old_Western_index_SHA256": sha(ROOT / WEST),
    "Chinese_V7_index_SHA256": sha(ROOT / CHINA),
    "new_historical_notes": 24,
    "actual_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
