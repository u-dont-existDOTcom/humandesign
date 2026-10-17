#!/usr/bin/env python3
"""Portable, independently replayed first-edition wealth-durability source packet."""

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
assert accepted["new_records"] == 75
assert accepted["empirical_validations"] == accepted["runtime_promotions"] == 0
folder = subprocess.run(
    ["xdg-user-dir", "DOWNLOAD"],
    capture_output=True,
    text=True,
)
downloads = (
    Path(folder.stdout.strip())
    if folder.returncode == 0 and folder.stdout.strip()
    else Path.home() / "Téléchargements"
)
downloads.mkdir(parents=True, exist_ok=True)
out = downloads / "Astrology-Lilly-Chapter-CXVIII-Estate-Durability-1647-20261017.zip"
members = [
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b05q_documentary.py",
    "test_b05q_documentary.py",
    "build_b05q_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(596, 601)]
manifest = {
    "batch": "B05q",
    "original_source": "William Lilly 1647 first edition / Wellcome b30338724",
    "historical_documentary_records": 75,
    "substantive_source_claims": 72,
    "following_third_house_navigation": 3,
    "actual_human_financial_accuracy_validated": 0,
    "runtime_promotions": 0,
    "source_interpretation_diplomatic": False,
    "members": {f: {"sha256": sha(B / f), "bytes": (B / f).stat().st_size} for f in members},
}
assert all((B / f).exists() for f in members)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for f in members:
        z.write(B / f, "B05q/" + f)
    z.writestr(
        "B05q/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    root = Path(tmp) / "B05q"
    assert json.loads((root / "RELEASE_MANIFEST.json").read_text()) == manifest
    for f, check in manifest["members"].items():
        assert sha(root / f) == check["sha256"], f
        assert (root / f).stat().st_size == check["bytes"], f
    result = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(root),
            "-p",
            "test_b05q_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "Ran 26 tests" in result.stderr, result.stderr
rec = {
    "batch": "B05q",
    "status": "ZIP_CRC_SHA256_FULL_EXTRACTED_26_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(members),
    "crc_passed": True,
    "per_member_sha256_passed": True,
    "full_extraction_passed": True,
    "replayed_source_tests": 26,
    "source_rules_sha256": sha(B / "RULES.json"),
    "historical_documentary_records": 75,
    "human_wealth_timing_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))
