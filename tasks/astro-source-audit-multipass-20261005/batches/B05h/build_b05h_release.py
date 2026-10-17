#!/usr/bin/env python3
"""Portable hermetic archive of first-edition intellect chapter source witnesses."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def H(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


a = json.loads((B / "ACCEPTANCE.json").read_text())
assert a["historical_source_annotations_added"] == 53 and a["empirical_validations"] == 0
p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], text=True, capture_output=True)
dl = (
    Path(p.stdout.strip())
    if p.returncode == 0 and p.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
out = dl / "Astrology-Lilly-Chapter-CX-Wit-Understanding-1647-20261017.zip"
names = [
    "SOURCE_FIRST_CLAIMS_AUTHORING.json",
    "SOURCE_IMAGE_WITNESSES.json",
    "SOURCE_TO_RECORD_REVERSE_MAP.json",
    "RULES.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_FIRST_REVIEW_20261017.md",
    "freeze_b05h_documentary.py",
    "test_b05h_documentary.py",
    "build_b05h_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(577, 582)]
manifest = {
    "batch": "B05h",
    "source": "William Lilly, Christian Astrology (1647), Wellcome b30338724",
    "historical_only": True,
    "documentary_records": 53,
    "substantive_historical_annotations": 50,
    "following_chapter_navigation": 3,
    "human_intellect_validation": 0,
    "clinical_validation": 0,
    "runtime_promotions": 0,
    "members": {f: {"sha256": H(B / f), "bytes": (B / f).stat().st_size} for f in names},
}
with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for f in names:
        z.write(B / f, "B05h/" + f)
    z.writestr("B05h/RELEASE_MANIFEST_SHA256.json", json.dumps(manifest, indent=2) + "\n")
with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory(prefix="B05h-source-") as temp:
    assert z.testzip() is None
    z.extractall(temp)
    root = Path(temp) / "B05h"
    assert json.loads((root / "RELEASE_MANIFEST_SHA256.json").read_text()) == manifest
    for f, record in manifest["members"].items():
        assert H(root / f) == record["sha256"] and (root / f).stat().st_size == record["bytes"], f
    t = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root),
            "-p",
            "test_b05h_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert t.returncode == 0 and "Ran 18 tests" in t.stderr, t.stderr
receipt = {
    "batch": "B05h",
    "status": "PORTABLE_ZIP_CRC_SHA256_FULL_EXTRACTION_18_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": H(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(names),
    "crc_ok": True,
    "per_member_sha256_ok": True,
    "full_extraction_ok": True,
    "extracted_tests_passed": 18,
    "accepted_rules_sha256": H(B / "RULES.json"),
    "historical_source_records": 53,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
