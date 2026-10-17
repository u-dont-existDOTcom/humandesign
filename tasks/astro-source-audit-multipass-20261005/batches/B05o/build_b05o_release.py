#!/usr/bin/env python3
"""Hermetic first-edition Lilly wealth-origin source release; not economic validation."""

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
assert accepted["new_source_annotations"] == 84
assert accepted["normalized_cell_items"] == 316
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
out = dl / "Astrology-Lilly-Chapter-CXVI-Origins-of-Estate-1647-20261017.zip"
files = [
    "SOURCE_FIRST_LOGIC_AUTHORING_20261017.json",
    "SOURCE_FIRST_CLASSIFICATION_MATRIX_20261017.json",
    "ORIGINAL_SOURCE_WITNESS.json",
    "SOURCE_TO_RECORD_MAP.json",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "ORIGINAL_SOURCE_REVIEW_20261017.md",
    "RULES.json",
    "ACCEPTANCE.json",
    "freeze_b05o_documentary.py",
    "test_b05o_documentary.py",
    "build_b05o_release.py",
] + [f"evidence/pdf_1647-{n}.jpg" for n in range(588, 597)]
manifest = {
    "batch": "B05o",
    "original_source": (
        "William Lilly Christian Astrology original edition 1647, Wellcome Collection b30338724"
    ),
    "historic_documentary_records": 84,
    "planet_matter_person_cells": 14,
    "sign_element_cells": 4,
    "planetary_sign_nature_cells": 6,
    "house_cells": 12,
    "normalized_table_source_items": 316,
    "prose_claims_and_navigation": 48,
    "proven_real_person_wealth_predictions": 0,
    "runtime_rule_promotions": 0,
    "full_diplomatic_transcription": False,
    "files": {f: {"sha256": sha(B / f), "bytes": (B / f).stat().st_size} for f in files},
}
assert all((B / f).is_file() for f in files)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipfile_out:
    for f in files:
        zipfile_out.write(B / f, "B05o/" + f)
    zipfile_out.writestr(
        "B05o/RELEASE_MANIFEST_SHA256.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(out) as archive, tempfile.TemporaryDirectory() as td:
    assert archive.testzip() is None
    archive.extractall(td)
    p = Path(td) / "B05o"
    assert json.loads((p / "RELEASE_MANIFEST_SHA256.json").read_text()) == manifest
    for f, info in manifest["files"].items():
        assert sha(p / f) == info["sha256"], f
        assert (p / f).stat().st_size == info["bytes"], f
    run = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(p),
            "-p",
            "test_b05o_documentary.py",
            "-v",
        ],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0 and "Ran 28 tests" in run.stderr, run.stderr
rec = {
    "batch": "B05o",
    "status": "FIRST_EDITION_ZIP_CRC_SHA256_28_REPLAYED_TESTS_PASSED",
    "archive_path": str(out),
    "archive_sha256": sha(out),
    "archive_bytes": out.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "per_member_hash_passed": True,
    "full_extraction_passed": True,
    "replayed_source_tests": 28,
    "accepted_rules_sha256": sha(B / "RULES.json"),
    "historical_annotations": 84,
    "normalized_source_cell_items": 316,
    "independently_validated_financial_results": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))
