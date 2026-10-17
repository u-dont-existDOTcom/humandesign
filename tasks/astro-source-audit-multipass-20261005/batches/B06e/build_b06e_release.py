#!/usr/bin/env python3
"""Portable original Lilly CXXVIII source with SHA and hermetic replay."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


accepted = json.loads((B / "ACCEPTANCE.json").read_text())
assert accepted["new_historical_annotations"] == 113
assert accepted["empirical_validations"] == accepted["runtime_promotions"] == 0
query = subprocess.run(
    ["xdg-user-dir", "DOWNLOAD"],
    capture_output=True,
    text=True,
)
dl = (
    Path(query.stdout.strip())
    if query.returncode == 0 and query.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
out = dl / "Astrology-Lilly-Chapter-CXXIX-Eyes-Speech-Medical-History-1647-20261017.zip"
files = [
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b06e_documentary.py",
    "test_b06e_documentary.py",
    "build_b06e_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(615, 628)]
assert all((B / name).is_file() for name in files)

manifest = {
    "batch": "B06e",
    "original_source": "William Lilly 1647 first edition Wellcome b30338724",
    "historical_annotations": 113,
    "substantive_historical_medical_claims": 111,
    "following_numbered_chapter_navigation": 2,
    "named_subsection_topics": 8,
    "independent_clinical_outcomes_validated": 0,
    "runtime_promotions": 0,
    "full_diplomatic_transcription": False,
    "files": {
        name: {"sha256": sha(B / name), "bytes": (B / name).stat().st_size} for name in files
    },
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in files:
        z.write(B / name, "B06e/" + name)
    z.writestr(
        "B06e/RELEASE_SHA256_MANIFEST.json",
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    )

with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    p = Path(tmp) / "B06e"
    assert json.loads((p / "RELEASE_SHA256_MANIFEST.json").read_text()) == manifest
    for name, details in manifest["files"].items():
        assert sha(p / name) == details["sha256"], name
        assert (p / name).stat().st_size == details["bytes"], name
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(p),
            "-p",
            "test_b06e_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "Ran 24 tests" in result.stderr, result.stderr

receipt = {
    "batch": "B06e",
    "status": "ORIGINAL_ZIP_CRC_SHA256_FULL_EXTRACTED_24_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "full_extraction_passed": True,
    "all_member_sha256_and_bytes_verified": True,
    "independent_replayed_tests": 24,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "source_boundary_sha256": sha(B / "ORIGINAL_NUMBERED_CHAPTER_BOUNDARY_20261017.json"),
    "historical_records": 113,
    "independent_human_medical_predictions_validated": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
