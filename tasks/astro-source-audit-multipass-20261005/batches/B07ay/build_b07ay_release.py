#!/usr/bin/env python3
"""Portable original CLXXVI source archive, 52 independent extracted test replays."""

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
REL = T + "/batches/B07ay/"
WEST = T + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-Manners-1647-1659-40-Historical-Sources-B07ay-20261020.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    p = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    if p is not None and p.is_dir() and p.resolve() != Path.home().resolve():
        return p
    f = Path.home() / "Téléchargements"
    return f if f.is_dir() else Path.home()


photos = load(B / "ORIGINAL_PHOTO_WITNESS_V1.json")
notes = load(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json")
rules = load(B / "RULES.json")
accept = load(B / "ACCEPTANCE.json")
old = load(ROOT / WEST)
chi = load(ROOT / CHINA)
assert old["records_count"] == 12900 and old["batches"][-1]["id"] == "B07ax"
assert chi["sum_source_annotations"] == 355
assert notes["historical_annotations_added_if_accepted"] == 40
assert len(rules["rules"]) == 40
assert notes["source_negative_throat_mark_observation_count"] == 1
assert notes["independent_actual_human_forecast_validations"] == 0
assert accept["next_original_R"] == "R12941"
assert photos["source_next_printed_CLXXVII_Riches_starts_same_pdf783"]
assert sha(B / "ORIGINAL_PHOTO_WITNESS_V1.json") == accept["photo_witness_SHA256"]
assert sha(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json") == accept["source_data_SHA256"]
assert sha(B / "RULES.json") == accept["rules_SHA256"]

names = [
    "ACCEPTANCE.json",
    "MANNERS_SOURCE_CANDIDATES_V1.json",
    "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json",
    "ORIGINAL_PHOTO_WITNESS_V1.json",
    "CORRECTED_PHYSICAL_CHAPTER_BOUNDARY_V1.json",
    "RULES.json",
    "RECOVERY_CHECKPOINT_20261019_LATEST.md",
    "FOCUSED_SOURCE_TEST_RECEIPT_PROVISIONAL_20261019.json",
    "test_b07ay_manners_original_source.py",
    "build_b07ay_manners_source.py",
    "build_b07ay_release.py",
    "prepare_b07ay_canonical.py",
]
files = {REL + name: B / name for name in names}
for label, photo in photos["source_1647_1659_page_photos"].items():
    name = photo["image_path"]
    p = ROOT / name
    assert p.is_file(), label
    assert sha(p) == photo["sha256"], label
    assert p.stat().st_size == photo["bytes"], label
    files[name] = p
files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values()), [k for k, f in files.items() if not f.is_file()]
manifest = {
    "batch": "B07ay",
    "source": (
        "Lilly Christian Astrology original 1647 and separately typeset "
        "1659, Manners printed745–749"
    ),
    "full_original_1647_PDF_SHA256": photos["source_full_Wellcome_1647_original_PDF_SHA256"],
    "first_second_original_editions_photo_count": 10,
    "historical_author_knew_merchant": True,
    "source_historical_throat_mark_negative_count": 1,
    "negative_lilly_quote": "I can find none.",
    "new_historical_documentary_annotations": 40,
    "Lilly_history_after_if_accepted": 12940,
    "next_original_CLXXVII_Riches": "R12941",
    "first_CLXXVI_physical_boundary_printed749": True,
    "original_epoch_merchant_natal_chart_independently_verified": False,
    "historical_astrology_human_accuracy_validated": 0,
    "runtime_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
dest = downloads()
dest.mkdir(parents=True, exist_ok=True)
archive = dest / NAME
staging = dest / (NAME + ".building")
assert not staging.exists(), staging
with zipfile.ZipFile(staging, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07ay-root/" + name)
    z.writestr(
        "B07ay-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(staging) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    base = Path(td) / "B07ay-root"
    assert load(base / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        p = base / name
        assert p.stat().st_size == meta["bytes"], name
        assert sha(p) == meta["sha256"], name
    test = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(base / REL),
            "-p",
            "test_b07ay_manners_original_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert test.returncode == 0, test.stdout + "\n" + test.stderr
    m = re.search(r"Ran (\d+) tests", test.stderr)
    assert m and int(m.group(1)) == 52, test.stderr
    assert "skipped" not in test.stderr
os.replace(staging, archive)
receipt = {
    "batch": "B07ay",
    "status": "MANNERS_1647_1659_40_SOURCE_NOTES_52_PORTABLE_TESTS_PASS",
    "archive_filename": NAME,
    "archive_SHA256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "archive_CRC_passed": True,
    "archive_exact_SHA256_and_byte_size_passed": True,
    "independent_extracted_source_tests_passed": 52,
    "photo_witness_SHA256": sha(B / "ORIGINAL_PHOTO_WITNESS_V1.json"),
    "original_notes_SHA256": sha(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "old_Western_SHA256": sha(ROOT / WEST),
    "Chinese_V7_SHA256": sha(ROOT / CHINA),
    "new_documentary_notes_if_accepted": 40,
    "real_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remotely_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
