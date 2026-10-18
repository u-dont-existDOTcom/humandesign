#!/usr/bin/env python3
"""Portable Lilly original 1647 CLVI historical mortality source only."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


accept = json.loads((B / "ACCEPTANCE.json").read_text())
assert accept["new_historical_annotations"] == 222
assert accept["empirical_validations"] == accept["runtime_promotions"] == 0
r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
dl = (
    Path(r.stdout.strip())
    if r.returncode == 0 and r.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
output = dl / "Astrology-Lilly-Printed-CLVI-Death-Historical-Source-1647-20261018.zip"
names = [
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json",
    "MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b07l_documentary.py",
    "test_b07l_documentary.py",
    "build_b07l_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(678, 686)]
manifest = {
    "batch": "B07l",
    "source": "William Lilly 1647 first edition / Wellcome b30338724",
    "historical_annotations": 222,
    "substantive": 220,
    "following_unnumbered_directions_navigation": 2,
    "independent_real_person_mortality_validated": 0,
    "runtime_promotions": 0,
    "complete_diplomatic_transcription": False,
    "next_unnumbered_directions_heading_verified": True,
    "members": {
        name: {"sha256": sha(B / name), "bytes": (B / name).stat().st_size} for name in names
    },
}
assert all((B / name).is_file() for name in names)
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in names:
        z.write(B / name, "B07l/" + name)
    z.writestr(
        "B07l/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(output) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B07l"
    assert json.loads((root / "RELEASE_MANIFEST.json").read_text()) == manifest
    for name, details in manifest["members"].items():
        assert sha(root / name) == details["sha256"]
        assert (root / name).stat().st_size == details["bytes"]
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root),
            "-p",
            "test_b07l_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0 and "Ran 36 tests" in proc.stderr, proc.stderr
receipt = {
    "batch": "B07l",
    "status": "ORIGINAL_SOURCE_ZIP_SHA256_CRC_EXTRACTED_36_TESTS_PASS",
    "archive_path": str(output),
    "archive_sha256": sha(output),
    "archive_bytes": output.stat().st_size,
    "members": len(names),
    "crc_passed": True,
    "sha256_passed": True,
    "extraction_passed": True,
    "replayed_tests": 36,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "historical_records_added": 222,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
