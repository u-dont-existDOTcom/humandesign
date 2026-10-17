#!/usr/bin/env python3
"""Portable first-edition historical stature packet; verifiable outside repo."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


q = json.loads((B / "ACCEPTANCE.json").read_text())
assert q["empirical_validations"] == q["runtime_promotions"] == 0
p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
DL = (
    Path(p.stdout.strip())
    if p.returncode == 0 and p.stdout.strip()
    else Path.home() / "Téléchargements"
)
DL.mkdir(parents=True, exist_ok=True)
OUT = DL / "Astrology-Lilly-Chapter-CXI-Stature-1647-Documentary-20261017.zip"
files = [
    "SOURCE_FIRST_AUTHORING.json",
    "ORIGINAL_IMAGE_MANIFEST.json",
    "SOURCE_TO_RECORD_MAP.json",
    "RULES.json",
    "UNRESOLVED.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "freeze_b05i.py",
    "test_b05i.py",
    "release_b05i.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in (580, 581, 582)]
manifest = {
    "batch": "B05i",
    "primary_source": "1647 William Lilly Christian Astrology / Wellcome b30338724",
    "historical_records": 27,
    "empirically_validated_height_predictions": 0,
    "runtime_promotions": 0,
    "files": {f: {"sha256": sha(B / f), "bytes": (B / f).stat().st_size} for f in files},
}
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=7) as z:
    for f in files:
        z.write(B / f, "B05i/" + f)
    z.writestr("B05i/RELEASE_MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
with zipfile.ZipFile(OUT) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    p = Path(tmp) / "B05i"
    assert json.loads((p / "RELEASE_MANIFEST.json").read_text()) == manifest
    for f, check in manifest["files"].items():
        assert sha(p / f) == check["sha256"] and (p / f).stat().st_size == check["bytes"]
    done = subprocess.run(
        ["python3", "-m", "unittest", "discover", "-s", str(p), "-p", "test_b05i.py", "-v"],
        text=True,
        capture_output=True,
    )
    assert done.returncode == 0 and "Ran 12 tests" in done.stderr, done.stderr
receipt = {
    "batch": "B05i",
    "status": "ZIP_CRC_SHA256_FULL_REPLAY_PASS",
    "archive_path": str(OUT),
    "archive_sha256": sha(OUT),
    "archive_bytes": OUT.stat().st_size,
    "crc_passed": True,
    "all_hashes_passed": True,
    "extraction_passed": True,
    "replayed_tests_passed": 12,
    "rules_sha256": sha(B / "RULES.json"),
    "new_source_records": 27,
    "new_height_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
