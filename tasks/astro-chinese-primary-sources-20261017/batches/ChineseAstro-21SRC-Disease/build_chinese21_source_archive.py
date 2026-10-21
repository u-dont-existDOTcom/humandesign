#!/usr/bin/env python3
"""Cold-extracted historical Zi Wei V21 archive with per-member SHA/CRC tests."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = Path("tasks/astro-chinese-primary-sources-20261017")
REL = T / "batches/ChineseAstro-21SRC-Disease"
DEST = Path("/home/joel/Téléchargements/Astrology-ZiWei-Disease-25-Original-Sources-V21-20261021.zip")
INPUTS = [
    T / "CHINESE_SOURCE_AUDIT_INDEX_V20.json",
    T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
    T / "batches/ChineseAstro-20SRC-Wealth/ZIWEI_WEALTH_31_SOURCE_NOTES_V1.json",
    Path("tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"),
] + [REL / name for name in (
    "WRITER_LEASE.json",
    "WORKING_CHECKPOINT_20261021.md",
    "SOURCE_1963110_DISEASE_EXACT_EXCERPT.txt",
    "ZIWEI_DISEASE_25_SOURCE_NOTES_V1.json",
    "SOURCE_DISEASE_25_EXACT_OFFSET_WITNESS_V1.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "freeze_ziwei_disease_original.py",
    "test_chinese21_original_disease.py",
    "build_chinese21_source_archive.py",
)]


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def main() -> None:
    if DEST.exists():
        raise ValueError("Source archive exists; inspect prior receipt before writing")
    if not DEST.parent.is_dir():
        raise ValueError("Owner's Downloads directory not available")
    members = {}
    for rel in INPUTS:
        p = ROOT / rel
        if not p.is_file():
            raise ValueError("Source-package member missing: " + str(rel))
        blob = p.read_bytes()
        members[rel.as_posix()] = {"sha256": digest(blob), "bytes": len(blob)}
    manifest = {
        "schema": "ZIWEI_V21_ORIGINAL_WIKITEXT_SOURCE_COLD_ARCHIVE_V1",
        "historical_source_original_online_oldid": 1963110,
        "historical_source_full_SHA256": "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72",
        "source_only": True,
        "original_Ming_woodblock_authenticated": False,
        "medical_or_person_outcome_validated": False,
        "independently_blinded_real_human_forecasts": 0,
        "runtime_astrology_promotions": 0,
        "members": members,
    }
    readme = (
        "# Zi Wei V21 original source-only Disease section\n\n"
        "Read tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-21SRC-Disease/ORIGINAL_SOURCE_REVIEW_20261021.md.\n"
        "From the cold-extracted archive root, replay:\n"
        "python3 -m unittest discover -s tasks/astro-chinese-primary-sources-20261017/"
        "batches/ChineseAstro-21SRC-Disease -p test_chinese21_original_disease.py -v\n\n"
        "The text includes historical illness assertions, not medical advice or "
        "clinically validated predictions. The online Chinese text is not an "
        "authenticated early printing.\n"
    )
    with ZipFile(DEST, "w", compression=ZIP_DEFLATED, compresslevel=9) as zipf:
        for rel in INPUTS:
            zipf.write(ROOT / rel, arcname=rel.as_posix())
        zipf.writestr("SOURCE_ARCHIVE_MANIFEST.json",
                      json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        zipf.writestr("README_READ_ME_FIRST.md", readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist()) != len(INPUTS) + 2:
            raise ValueError("ZIP CRC/member list validation failed")
        for name, meta in members.items():
            blob = z.read(name)
            if (digest(blob), len(blob)) != (meta["sha256"], meta["bytes"]):
                raise ValueError("ZIP member bytes/hash mismatch: " + name)
    with tempfile.TemporaryDirectory(prefix="ziwei-v21-cold-source-") as scratch:
        extracted = Path(scratch) / "archive_root"
        extracted.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(extracted)
        for name, meta in members.items():
            blob = (extracted / name).read_bytes()
            if (digest(blob), len(blob)) != (meta["sha256"], meta["bytes"]):
                raise ValueError("Cold-extracted source file changed: " + name)
        tests = subprocess.run(
            [sys.executable, "-m", "unittest", "discover",
             "-s", REL.as_posix(),
             "-p", "test_chinese21_original_disease.py", "-v"],
            cwd=extracted, capture_output=True, text=True
        )
        log = tests.stdout + tests.stderr
        (B / "COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log, encoding="utf-8")
        if tests.returncode or tests.stderr.count(" ... ok") != 12 or "Ran 12 tests" not in tests.stderr:
            raise ValueError("Cold source unit replay failed: " + log[-2200:])
    receipt = {
        "batch": "ChineseAstro-21SRC-Disease",
        "status": "COLD_SOURCE_ZIP_CRC_SHA_BYTES_AND_12_TESTS_PASSED",
        "archive_path_on_owner_computer": str(DEST),
        "archive_filename": DEST.name,
        "archive_sha256": digest(DEST.read_bytes()),
        "archive_bytes": DEST.stat().st_size,
        "archive_members": len(INPUTS) + 2,
        "all_member_SHA256_and_bytes_verified": True,
        "ZIP_CRC_verified": True,
        "cold_extracted_members_SHA256_verified": True,
        "independent_cold_original_source_tests_green": 12,
        "original_historic_woodblock_imprint_authenticated": False,
        "human_blind_forecast_successes": 0,
        "runtime_astrological_promotions": 0,
    }
    (B / "SOURCE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
