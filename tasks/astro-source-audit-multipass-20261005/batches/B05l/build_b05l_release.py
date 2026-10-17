#!/usr/bin/env python3
"""Portable source-faithful fortune chapter archive; NOT predictive verification."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = json.loads((B / "ACCEPTANCE.json").read_text())
assert a["historical_records_added"] == 44
assert a["empirical_validations"] == a["runtime_promotions"] == 0
loc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
downloads = (
    Path(loc.stdout.strip())
    if loc.returncode == 0 and loc.stdout.strip()
    else Path.home() / "Téléchargements"
)
downloads.mkdir(parents=True, exist_ok=True)
out = downloads / "Astrology-Lilly-Chapter-CXIV-General-Fortune-1647-20261017.zip"
files = [
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b05l_documentary.py",
    "test_b05l_original.py",
    "build_b05l_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(585, 589)]
manifest = {
    "batch": "B05l",
    "source": "Lilly Christian Astrology original edition 1647 / Wellcome b30338724",
    "historical_source_annotations": 44,
    "source_passages": 10,
    "substantive_original_annotations": 41,
    "navigation_witnesses": 3,
    "independently_validated_outcomes": 0,
    "runtime_promotions": 0,
    "members": {f: {"bytes": (B / f).stat().st_size, "sha256": h(B / f)} for f in files},
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for file in files:
        z.write(B / file, "B05l/" + file)
    z.writestr("B05l/RELEASE_MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
with zipfile.ZipFile(out) as archive, tempfile.TemporaryDirectory() as temp:
    assert archive.testzip() is None
    archive.extractall(temp)
    p = Path(temp) / "B05l"
    assert json.loads((p / "RELEASE_MANIFEST.json").read_text()) == manifest
    for file, check in manifest["members"].items():
        assert h(p / file) == check["sha256"]
        assert (p / file).stat().st_size == check["bytes"]
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(p),
            "-p",
            "test_b05l_original.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "Ran 18 tests" in result.stderr, result.stderr
receipt = {
    "batch": "B05l",
    "status": "ZIP_CRC_SHA256_FULL_EXTRACTED_18_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": h(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "per_member_sha256_passed": True,
    "full_extraction_passed": True,
    "extracted_tests_passed": 18,
    "accepted_rules_sha256": h(B / "RULES.json"),
    "historical_source_records_added": 44,
    "independent_outcomes_validated": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
