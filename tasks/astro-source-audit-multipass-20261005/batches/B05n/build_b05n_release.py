#!/usr/bin/env python3
"""Portable source-only archive, originally scanned first-edition Lilly CHAP CXIIII."""

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
assert accepted["new_source_annotations"] == 57
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
out = dl / "Astrology-Lilly-Chapter-CXV-Whether-Rich-1647-20261017.zip"
files = [
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b05n_documentary.py",
    "test_b05n_documentary.py",
    "build_b05n_release.py",
] + [f"evidence/pdf_1647-{i}.jpg" for i in range(587, 592)]
assert all((B / name).is_file() for name in files)
manifest = {
    "batch": "B05n",
    "source": (
        "William Lilly Christian Astrology original 1647 edition, Wellcome Collection b30338724"
    ),
    "historical_annotations": 57,
    "substantive_source_claims": 55,
    "next_chapter_navigation": 2,
    "independent_wealth_validation": 0,
    "confirmed_inheritance_predictions": 0,
    "runtime_rule_promotions": 0,
    "fully_diplomatic_transcription": False,
    "files": {
        name: {"sha256": sha(B / name), "bytes": (B / name).stat().st_size} for name in files
    },
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in files:
        z.write(B / name, "B05n/" + name)
    z.writestr(
        "B05n/RELEASE_SHA256_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root = Path(td) / "B05n"
    assert json.loads((root / "RELEASE_SHA256_MANIFEST.json").read_text()) == manifest
    for name, record in manifest["files"].items():
        assert sha(root / name) == record["sha256"], name
        assert (root / name).stat().st_size == record["bytes"], name
    run = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root),
            "-p",
            "test_b05n_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0 and "Ran 24 tests" in run.stderr, run.stderr
receipt = {
    "batch": "B05n",
    "status": "ZIP_CRC_SHA256_FULL_EXTRACT_24_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_size": out.stat().st_size,
    "member_count": len(files),
    "crc_pass": True,
    "per_member_hashes_pass": True,
    "full_extraction_pass": True,
    "replayed_source_tests": 24,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "new_historical_records": 57,
    "independent_economic_outcomes": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
