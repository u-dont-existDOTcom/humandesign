#!/usr/bin/env python3
"""Hermetic first-edition 1647 lawful/indirect wealth source; no ethics inference."""

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
assert accepted["new_historical_annotations"] == 57
assert accepted["empirical_validations"] == accepted["runtime_promotions"] == 0
query = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
dl = (
    Path(query.stdout.strip())
    if query.returncode == 0 and query.stdout.strip()
    else Path.home() / "Téléchargements"
)
dl.mkdir(parents=True, exist_ok=True)
out = dl / "Astrology-Lilly-Chapter-CXVII-Lawful-Indirect-1647-20261017.zip"
files = [
    "SOURCE_FIRST_AUTHORING_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b05p_documentary.py",
    "test_b05p_documentary.py",
    "build_b05p_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(594, 599)]
assert all((B / f).is_file() for f in files)
manifest = {
    "batch": "B05p",
    "source": ("Original 1647 William Lilly Christian Astrology, Wellcome b30338724"),
    "historical_source_annotations": 57,
    "substantive_conditions": 55,
    "following_chapter_navigation": 2,
    "person_level_legality_or_criminality_validated": 0,
    "actual_independent_wealth_successes": 0,
    "runtime_promotions": 0,
    "complete_diplomatic_transcription": False,
    "members": {f: {"sha256": sha(B / f), "bytes": (B / f).stat().st_size} for f in files},
}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for f in files:
        archive.write(B / f, "B05p/" + f)
    archive.writestr(
        "B05p/SHA256_RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as archive, tempfile.TemporaryDirectory() as temp:
    assert archive.testzip() is None
    archive.extractall(temp)
    source = Path(temp) / "B05p"
    assert json.loads((source / "SHA256_RELEASE_MANIFEST.json").read_text()) == manifest
    for f, expected in manifest["members"].items():
        assert sha(source / f) == expected["sha256"], f
        assert (source / f).stat().st_size == expected["bytes"], f
    check = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(source),
            "-p",
            "test_b05p_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0 and "Ran 21 tests" in check.stderr, check.stderr
receipt = {
    "batch": "B05p",
    "status": "ORIGINAL_ZIP_CRC_SHA256_REPLAY_21_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "per_member_sha256_passed": True,
    "full_extraction_passed": True,
    "replayed_tests": 21,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "historical_source_records": 57,
    "real_human_ethics_validations": 0,
    "economic_prediction_validations": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
