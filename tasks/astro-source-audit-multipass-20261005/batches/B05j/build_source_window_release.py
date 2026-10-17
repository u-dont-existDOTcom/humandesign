#!/usr/bin/env python3
"""Portable archive of next first-edition source witness, pending claim extraction."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
dl = (
    Path(p.stdout.strip())
    if p.returncode == 0 and p.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
out = dl / "Astrology-Lilly-Chapter-CXII-Face-Hair-Original-Source-Window-20261017.zip"
names = [
    "SOURCE_WINDOW_20261017.json",
    "CONTINUATION_HANDOFF_20261017.md",
    "make_window.py",
    "test_b05j_window.py",
    "build_source_window_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(581, 587)]
manifest = {
    "batch": "B05j",
    "status": "UNEXTRACTED_ORIGINAL_SOURCE_WINDOW",
    "original_documents": "Lilly first edition 1647 / Wellcome b30338724",
    "new_source_records": 0,
    "independent_validation_count": 0,
    "files": {f: {"sha256": sha(B / f), "bytes": (B / f).stat().st_size} for f in names},
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    for f in names:
        zipf.write(B / f, "B05j/" + f)
    zipf.writestr("B05j/RELEASE_MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory() as temp:
    assert z.testzip() is None
    z.extractall(temp)
    extracted = Path(temp) / "B05j"
    for f, q in manifest["files"].items():
        assert sha(extracted / f) == q["sha256"]
        assert (extracted / f).stat().st_size == q["bytes"]
    run = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(extracted),
            "-p",
            "test_b05j_window.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0 and "Ran 5 tests" in run.stderr, run.stderr

receipt = {
    "batch": "B05j",
    "status": "ORIGINAL_WITNESS_ARCHIVED_SHA256_CRC_5_TESTS",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_size": out.stat().st_size,
    "test_count": 5,
    "baseline_canonical_source_records": 7737,
    "new_historical_records": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_WINDOW_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
