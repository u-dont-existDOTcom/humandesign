#!/usr/bin/env python3
"""Portable first-edition 1647 mature-body-bulk source packet; not predictive validation."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


q = json.loads((B / "ACCEPTANCE.json").read_text())
assert q["new_records"] == 31
assert q["empirical_validations"] == q["runtime_promotions"] == 0
config = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
dl = (
    Path(config.stdout.strip())
    if config.returncode == 0 and config.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
out = dl / "Astrology-Lilly-Chapter-CXIII-Mature-Body-1647-20261017.zip"
files = [
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b05k_documentary.py",
    "test_b05k_original.py",
    "build_b05k_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(583, 587)]
manifest = {
    "batch": "B05k",
    "source": "Lilly Christian Astrology original edition 1647, Wellcome b30338724",
    "documentary_historical_annotations": 31,
    "substantive_source_records": 29,
    "following_chapter_navigation": 2,
    "independent_human_size_validations": 0,
    "clinical_validations": 0,
    "runtime_promotions": 0,
    "files": {f: {"sha256": h(B / f), "bytes": (B / f).stat().st_size} for f in files},
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for f in files:
        z.write(B / f, "B05k/" + f)
    z.writestr(
        "B05k/RELEASE_MANIFEST_SHA256.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory() as temp:
    assert z.testzip() is None
    z.extractall(temp)
    x = Path(temp) / "B05k"
    assert json.loads((x / "RELEASE_MANIFEST_SHA256.json").read_text()) == manifest
    for f, check in manifest["files"].items():
        assert h(x / f) == check["sha256"]
        assert (x / f).stat().st_size == check["bytes"]
    run = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(x),
            "-p",
            "test_b05k_original.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0 and "Ran 17 tests" in run.stderr, run.stderr
receipt = {
    "batch": "B05k",
    "status": "ZIP_CRC_SHA256_FULL_EXTRACTED_17_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": h(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "sha256_passed": True,
    "extraction_passed": True,
    "tests_replayed": 17,
    "rules_sha256": h(B / "RULES.json"),
    "source_historical_records": 31,
    "human_size_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
