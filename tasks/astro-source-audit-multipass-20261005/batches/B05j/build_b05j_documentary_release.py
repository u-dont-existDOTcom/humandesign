#!/usr/bin/env python3
"""Self-verifying portable first-edition CHAP CXI historical-source packet."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


accept = json.loads((BASE / "ACCEPTANCE.json").read_text())
assert accept["new_historical_records"] == 62
assert accept["empirical_validations"] == accept["runtime_promotions"] == 0
loc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
dl = (
    Path(loc.stdout.strip())
    if loc.returncode == 0 and loc.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
out = dl / "Astrology-Lilly-Chapter-CXII-Signs-Face-Hair-1647-20261017.zip"
files = [
    "SOURCE_WINDOW_20261017.json",
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "SOURCE_FIRST_REVERSE_MAP.json",
    "ORIGINAL_SOURCE_INTEGRITY.json",
    "UNRESOLVED_SOURCE_QUALIFICATIONS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b05j_documentary.py",
    "test_b05j_documentary.py",
    "test_b05j_window.py",
    "build_b05j_documentary_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(581, 587)]
assert all((BASE / f).is_file() for f in files)
members = {f: {"sha256": sha(BASE / f), "bytes": (BASE / f).stat().st_size} for f in files}
manifest = {
    "batch": "B05j",
    "source": "Original William Lilly 1647, Wellcome b30338724",
    "historical_source_records": 62,
    "substantive_historical_annotations": 60,
    "next_chapter_navigation_units": 2,
    "human_biometric_validations": 0,
    "ancestry_or_medical_validations": 0,
    "runtime_promotions": 0,
    "original_full_diplomatic_transcription": False,
    "members": members,
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for f in files:
        archive.write(BASE / f, "B05j/" + f)
    archive.writestr(
        "B05j/RELEASE_SHA256_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as archive, tempfile.TemporaryDirectory() as temp:
    assert archive.testzip() is None
    archive.extractall(temp)
    p = Path(temp) / "B05j"
    assert json.loads((p / "RELEASE_SHA256_MANIFEST.json").read_text()) == manifest
    for f, expected in members.items():
        assert (p / f).stat().st_size == expected["bytes"], f
        assert sha(p / f) == expected["sha256"], f
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(p),
            "-p",
            "test_b05j*.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    print(result.stderr[-650:])
    assert result.returncode == 0 and "Ran 23 tests" in result.stderr, result.stderr
receipt = {
    "batch": "B05j",
    "status": "PORTABLE_ZIP_CRC_SHA256_EXTRACTED_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "per_member_sha256_passed": True,
    "full_extraction_passed": True,
    "replayed_tests": 23,
    "accepted_rules_sha256": sha(BASE / "RULES.json"),
    "historical_source_records_if_published": 62,
    "independent_human_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(BASE / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
