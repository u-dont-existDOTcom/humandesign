#!/usr/bin/env python3
"""Portable Lilly CLIX Ascendant directions and original fixed-stars source."""

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
assert accept["new_historical_annotations"] == 335
assert accept["empirical_validations"] == accept["runtime_promotions"] == 0
r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
dl = (
    Path(r.stdout.strip())
    if r.returncode == 0 and r.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
output = dl / "Astrology-Lilly-Printed-CLIX-Ascendant-Directions-1647-20261018.zip"
names = [
    "SOURCE_FIRST_AUTHORING_20261018.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json",
    "SOURCE_PART_01_JUPITER_MARS_BODY_20261018.json",
    "SOURCE_PART_02_MARS_SUN_VENUS_20261018.json",
    "SOURCE_PART_03_MERCURY_MOON_NODES_20261018.json",
    "SOURCE_PART_04_FIXED_STARS_HOUSE_CUSPS_20261018.json",
    "PLAN_20261018.md",
    "CLIX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b07p_documentary.py",
    "test_b07p_documentary.py",
    "build_b07p_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(691, 704)]
manifest = {
    "batch": "B07p",
    "source": "William Lilly 1647 first edition / Wellcome b30338724",
    "historical_annotations": 335,
    "substantive": 332,
    "following_printed_CLX_navigation": 3,
    "independent_real_human_directions_events_validated": 0,
    "runtime_promotions": 0,
    "complete_diplomatic_transcription": False,
    "next_printed_CLX_heading_verified": True,
    "members": {
        name: {"sha256": sha(B / name), "bytes": (B / name).stat().st_size} for name in names
    },
}
assert all((B / name).is_file() for name in names)
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in names:
        z.write(B / name, "B07p/" + name)
    z.writestr(
        "B07p/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(output) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B07p"
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
            "test_b07p_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0 and "Ran 38 tests" in proc.stderr, proc.stderr
receipt = {
    "batch": "B07p",
    "status": "ORIGINAL_SOURCE_ZIP_SHA256_CRC_EXTRACTED_38_TESTS_PASS",
    "archive_path": str(output),
    "archive_sha256": sha(output),
    "archive_bytes": output.stat().st_size,
    "members": len(names),
    "crc_passed": True,
    "sha256_passed": True,
    "extraction_passed": True,
    "replayed_tests": 38,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "historical_records_added": 335,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261018.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
