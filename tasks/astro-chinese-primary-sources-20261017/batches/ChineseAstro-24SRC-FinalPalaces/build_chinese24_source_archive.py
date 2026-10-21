#!/usr/bin/env python3
"""Reproducible cold extractable historical Zi Wei V24 source package."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = Path("tasks/astro-chinese-primary-sources-20261017")
REL = TASK / "batches/ChineseAstro-24SRC-FinalPalaces"
DEST = Path("/home/joel/Téléchargements/Astrology-ZiWei-Final-Four-123-Original-Sources-V24-20261021.zip")
FILES = [
    TASK / "CHINESE_SOURCE_AUDIT_INDEX_V23.json",
    TASK / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
    TASK / "batches/ChineseAstro-23SRC-Servants/ZIWEI_SERVANTS_26_SOURCE_NOTES_V1.json",
    Path("tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"),
] + [REL / name for name in (
    "WRITER_LEASE.json",
    "WORKING_CHECKPOINT_20261021.md",
    "SOURCE_1963110_FINAL_FOUR_EXACT_EXCERPT.txt",
    "ZIWEI_FINAL_FOUR_123_SOURCE_NOTES_V1.json",
    "SOURCE_FINAL_FOUR_123_EXACT_OFFSET_WITNESS_V1.json",
    "ACCEPTANCE.json",
    "ORIGINAL_SOURCE_REVIEW_20261021.md",
    "UNRESOLVED_SOURCE_LIMITS.json",
    "freeze_final_four_palaces.py",
    "test_chinese24_original_final_four.py",
    "build_chinese24_source_archive.py",
)]

def sha(raw: bytes) -> str:
    return sha256(raw).hexdigest()

def main() -> None:
    if DEST.exists():
        raise ValueError("Existing original source archive: inspect prior receipt before re-writing")
    if not DEST.parent.is_dir():
        raise ValueError("Owner Downloads folder missing")
    witnesses: dict[str,dict] = {}
    for rel in FILES:
        path = ROOT / rel
        if not path.is_file():
            raise ValueError(f"Expected source package member absent: {rel}")
        data = path.read_bytes()
        witnesses[rel.as_posix()] = {"sha256": sha(data), "bytes": len(data)}
    manifest = {
        "schema": "ZIWEI_V24_FINAL_FOUR_COLD_SOURCE_PACKAGE",
        "original_online_source_oldid": 1963110,
        "original_online_full_source_sha256": "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72",
        "last_four_palaces": ["Career","Estate","Fortune","Parents"],
        "historic_quoted_lines_only": 123,
        "original_site_footer_metadata_only": 2,
        "original_ancient_Ming_printing_independently_authenticated": False,
        "real_human_blind_forecasts_validated": 0,
        "runtime_astrology_promotions": 0,
        "file_checks": witnesses,
    }
    readme = (
        "# Zi Wei original online Volume II end-of-section reading, V24\n\n"
        "Read the source-critical review first: "
        "tasks/astro-chinese-primary-sources-20261017/batches/"
        "ChineseAstro-24SRC-FinalPalaces/ORIGINAL_SOURCE_REVIEW_20261021.md\n"
        "Run after extraction at archive root:\n"
        "python3 -m unittest discover -s tasks/astro-chinese-primary-sources-20261017/"
        "batches/ChineseAstro-24SRC-FinalPalaces -p test_chinese24_original_final_four.py -v\n\n"
        "Source is an unverified modern transmitted edition, not validated people, "
        "medical/legal/property/career decisions, or complete natal chart calculations.\n"
    )
    with ZipFile(DEST, "w", compression=ZIP_DEFLATED, compresslevel=9) as z:
        for rel in FILES:
            z.write(ROOT / rel, arcname=rel.as_posix())
        z.writestr("SOURCE_ARCHIVE_MANIFEST.json", json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        z.writestr("README_READ_ME_FIRST.md", readme)
    with ZipFile(DEST) as z:
        if z.testzip() is not None or len(z.namelist()) != len(FILES)+2:
            raise ValueError("Invalid original source package ZIP CRC or member count")
        for name,expected in witnesses.items():
            original = z.read(name)
            if (sha(original),len(original)) != (expected["sha256"],expected["bytes"]):
                raise ValueError("Archive member hash or size altered: "+name)
    with tempfile.TemporaryDirectory(prefix="ziwei-v24-four-final-palaces-") as scratch:
        output = Path(scratch) / "unpacked"
        output.mkdir()
        with ZipFile(DEST) as z:
            z.extractall(output)
        for name,expected in witnesses.items():
            original = (output/name).read_bytes()
            if (sha(original),len(original)) != (expected["sha256"],expected["bytes"]):
                raise ValueError("Independent cold-extracted source SHA mismatch: "+name)
        cmd = [
            sys.executable, "-m", "unittest", "discover",
            "-s", REL.as_posix(), "-p", "test_chinese24_original_final_four.py", "-v"
        ]
        result = subprocess.run(cmd, cwd=output, capture_output=True, text=True)
        log = result.stdout+result.stderr
        (B/"COLD_ARCHIVE_TEST_LOG_20261021.txt").write_text(log,encoding="utf-8")
        if result.returncode or result.stderr.count(" ... ok") != 14 or "Ran 14 tests" not in result.stderr:
            raise ValueError("Freshly extracted original source tests failed: "+log[-2400:])
    receipt = {
        "batch": "ChineseAstro-24SRC-FinalPalaces",
        "status": "COLD_ORIGINAL_SOURCE_ZIP_CRC_SHA_AND_14_TESTS_PASSED",
        "archive_path_on_owner_computer": str(DEST),
        "archive_filename": DEST.name,
        "archive_SHA256": sha(DEST.read_bytes()),
        "archive_bytes": DEST.stat().st_size,
        "archive_members": len(FILES)+2,
        "ZIP_CRC_verified": True,
        "all_members_sha256_and_bytes_verified": True,
        "all_cold_extracted_members_sha256_verified": True,
        "independent_cold_source_tests_green": 14,
        "source_online_Volume_II_end_reached": True,
        "original_ancient_Ming_book_authenticated": False,
        "independent_human_blind_predictions": 0,
        "runtime_astrology_promotions": 0,
    }
    (B/"SOURCE_RELEASE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
