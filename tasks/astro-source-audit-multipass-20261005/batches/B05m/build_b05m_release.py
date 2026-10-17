#!/usr/bin/env python3
"""Build portable SHA/CRC-verified unnumbered 1647 wealth source packet."""

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = json.loads((B / "ACCEPTANCE.json").read_text())
assert a["new_historical_records"] == 45
assert a["empirical_validations"] == a["runtime_promotions"] == 0
loc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
dl = (
    Path(loc.stdout.strip())
    if loc.returncode == 0 and loc.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
out = dl / "Astrology-Lilly-Second-House-Riches-Unnumbered-1647-20261017.zip"
files = [
    "SOURCE_WINDOW_20261017.json",
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "make_source_window.py",
    "freeze_b05m_documentary.py",
    "test_b05m_window.py",
    "test_b05m_documentary.py",
    "build_b05m_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in (586, 587, 588)]
assert all((B / f).is_file() for f in files)
manifest = {
    "batch": "B05m",
    "primary_source": "William Lilly 1647 first edition, Wellcome b30338724",
    "historical_source_records": 45,
    "substantive_historical_claims": 43,
    "following_chapter_navigation": 2,
    "direct_ptolemy_original_comparison_verified": False,
    "human_wealth_outcome_accuracy_validated": 0,
    "runtime_promotions": 0,
    "members": {f: {"sha256": sha(B / f), "bytes": (B / f).stat().st_size} for f in files},
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    for f in files:
        zipf.write(B / f, "B05m/" + f)
    zipf.writestr(
        "B05m/RELEASE_SHA256_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as zipf, tempfile.TemporaryDirectory() as temp:
    assert zipf.testzip() is None
    zipf.extractall(temp)
    extract = Path(temp) / "B05m"
    assert json.loads((extract / "RELEASE_SHA256_MANIFEST.json").read_text()) == manifest
    for f, info in manifest["members"].items():
        assert sha(extract / f) == info["sha256"], f
        assert (extract / f).stat().st_size == info["bytes"], f
    check = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(extract),
            "-p",
            "test_b05m_*.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0 and "Ran 20 tests" in check.stderr, check.stderr
receipt = {
    "batch": "B05m",
    "status": "CRC_SHA256_ARCHIVE_EXTRACT_AND_20_TEST_REPLAY_PASS",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(files),
    "crc_pass": True,
    "all_member_hashes_pass": True,
    "full_extraction_pass": True,
    "replayed_tests": 20,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "new_historical_records": 45,
    "independent_human_outcomes_validated": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
