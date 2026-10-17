#!/usr/bin/env python3
"""Portable, SHA-verified original 1647 sixth-house documentary source packet."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = json.loads((B / "ACCEPTANCE.json").read_text())
assert a["new_historical_source_annotations"] == 112
assert a["normalized_source_items"] == 150
assert a["empirical_validations"] == a["runtime_promotions"] == 0

query = subprocess.run(
    ["xdg-user-dir", "DOWNLOAD"],
    capture_output=True,
    text=True,
)
downloads = (
    Path(query.stdout.strip())
    if query.returncode == 0 and query.stdout.strip()
    else Path.home() / "Téléchargements"
)
downloads.mkdir(parents=True, exist_ok=True)
out = downloads / ("Astrology-Lilly-Sixth-House-Planet-Zodiac-Medical-Sources-1647-20261017.zip")
names = [
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b06d_documentary.py",
    "test_b06d_documentary.py",
    "build_b06d_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(610, 617)]
assert all((B / name).is_file() for name in names)
manifest = {
    "batch": "B06d",
    "original_source": "William Lilly Christian Astrology 1647 Wellcome b30338724",
    "historical_records": 112,
    "substantive_prose_records": 84,
    "planetary_body_and_ailment_cells": 14,
    "zodiac_sign_body_region_cells": 12,
    "following_chapter_navigation": 2,
    "normalized_historical_table_items": 150,
    "actual_human_medical_validations": 0,
    "runtime_promotions": 0,
    "complete_diplomatic_transcription": False,
    "members": {
        name: {"sha256": sha(B / name), "bytes": (B / name).stat().st_size} for name in names
    },
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in names:
        z.write(B / name, "B06d/" + name)
    z.writestr(
        "B06d/RELEASE_MANIFEST_SHA256.json",
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    )

with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    p = Path(tmp) / "B06d"
    recovered = json.loads((p / "RELEASE_MANIFEST_SHA256.json").read_text(encoding="utf-8"))
    assert recovered == manifest
    for file, values in manifest["members"].items():
        assert sha(p / file) == values["sha256"], file
        assert (p / file).stat().st_size == values["bytes"], file
    test = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(p),
            "-p",
            "test_b06d_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert test.returncode == 0 and "Ran 29 tests" in test.stderr, test.stderr

receipt = {
    "batch": "B06d",
    "status": "ORIGINAL_ZIP_CRC_SHA256_EXTRACT_REPLAY_29_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(names),
    "crc_passed": True,
    "full_extraction_passed": True,
    "all_member_sha256_and_byte_sizes_passed": True,
    "independent_extracted_documentary_tests_replayed": 29,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "matrix_sha256": sha(B / "ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json"),
    "historical_source_records": 112,
    "normalized_source_list_items": 150,
    "actual_patient_diagnoses_or_outcomes_validated": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
