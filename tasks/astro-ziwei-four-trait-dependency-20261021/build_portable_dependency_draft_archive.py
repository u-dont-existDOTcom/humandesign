#!/usr/bin/env python3
"""Cold portable original source→behavior dependency and chart coverage audit.

Includes raw original Chinese and referenced accepted source files for expert
review, previously accepted 312-row vendor comparison for synthetic cases.
No private personal birth records or actual human predictive responses.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import build_original_source_dependency_draft as check

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
NAME = "Astrology-ZiWei-Four-Construct-Source-Dependency-Draft-20261021.zip"


def sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def build() -> dict:
    check.get_data()
    sources = [check.L, check.C, check.READY]
    original = ROOT / "tasks/astro-chinese-primary-sources-20261017"
    sources += [
        original / "CHINESE_SOURCE_AUDIT_INDEX_V14.json",
        original / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
    ]
    for b, file in (
        ("ChineseAstro-10SRC-Life", "ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json"),
        ("ChineseAstro-11SRC-Life", "ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"),
        ("ChineseAstro-12SRC-Life", "ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json"),
        ("ChineseAstro-13SRC-Life", "ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"),
        ("ChineseAstro-14SRC-Life", "ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"),
    ):
        sources.append(original / "batches" / b / file)
    local = [
        p
        for p in B.rglob("*")
        if p.is_file()
        and p.suffix in (".py", ".json", ".md")
        and "__pycache__" not in str(p)
        and p.name
        not in (
            "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json",
            "PORTABLE_DEPENDENCY_DRAFT_SOURCE_RECEIPT_20261021.json",
            "CONTINUATION_HANDOFF_ACCEPTED_20261021.md",
        )
    ]
    blob = {
        str(path.relative_to(ROOT)): path.read_bytes()
        for path in sorted(set(local + sources), key=lambda p: str(p.relative_to(ROOT)))
    }
    oracle = subprocess.run(
        ["git", "show", f"{check.ORACLE_COMMIT}:{check.ORACLE_FILE}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    if len(oracle) != 899155 or sha(oracle) != check.ORACLE_SHA:
        raise ValueError("Pinned source comparison original SHA moved")
    blob[str(check.COLD_ORACLE.relative_to(ROOT))] = oracle
    docs = {path: {"bytes": len(data), "sha256": sha(data)} for path, data in sorted(blob.items())}
    directory = Path.home() / "Téléchargements"
    directory.mkdir(parents=True, exist_ok=True)
    archive = directory / NAME
    with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for path, raw in sorted(blob.items()):
            z.writestr(path, raw)
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(blob):
            raise ValueError("Source dependency ZIP CRC/member mismatch")
        for path, receipt in docs.items():
            raw = z.read(path)
            if sha(raw) != receipt["sha256"] or len(raw) != receipt["bytes"]:
                raise ValueError("Independent original source SHA or bytes changed " + path)
    with tempfile.TemporaryDirectory(prefix="ZiWei_Four_Behavior_Dependency_COLD_") as name:
        root = Path(name)
        with ZipFile(archive) as z:
            z.extractall(root)
        suite = root / "tasks/astro-ziwei-four-trait-dependency-20261021"
        run = subprocess.run(
            [
                "/usr/bin/python3",
                "-m",
                "unittest",
                "discover",
                "-s",
                str(suite),
                "-p",
                "test_original_source_dependency_draft.py",
                "-q",
            ],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
        )
        logs = run.stdout + run.stderr
        if run.returncode or "Ran 24 tests" not in logs or not logs.rstrip().endswith("OK"):
            print(logs[-1700:])
            raise ValueError("Independent source dependency archive 24 source tests not green")
        p = suite / "FOUR_ZIWEI_SOURCE_CONSTRUCT_DEPENDENCY_DRAFT_V1.json"
        before = p.read_bytes()
        replay = subprocess.run(
            ["/usr/bin/python3", str(suite / "build_original_source_dependency_draft.py")],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if replay.returncode:
            print(replay.stderr[-1600:])
            raise ValueError("Cold archive source-rule dependency and 120 toy chart replay failed")
        if p.read_bytes() != before:
            raise ValueError("Cold source dependency simulation differs bytewise")
    receipt = {
        "schema": "HUMANDESIGN_ZIWEI_FOUR_CONSTRUCT_ORIGINAL_SOURCE_DEPENDENCY_ARCHIVE_V1",
        "status": "SOURCE_HISTORICAL_PHRASES_AND_SYNTHETIC_COVERAGE_ONLY_NOT_HUMAN_PREDICTIONS",
        "owner_local_archive_path": str(archive),
        "archive_filename": NAME,
        "archive_SHA256": sha(archive.read_bytes()),
        "archive_bytes": archive.stat().st_size,
        "member_count": len(blob),
        "original_source_sha256_and_byte_records": docs,
        "zip_CRC_passed": True,
        "all_source_file_sha_and_sizes_verified": True,
        "independent_cold_original_source_dependency_tests_green": 24,
        "independent_cold_120_synthetic_chart_coverage_recomputed_exactly": True,
        "original_Chinese_transmitted_source_SHA256": (
            "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
        ),
        "real_human_birth_or_survey_records": 0,
        "real_human_chart_to_behavior_predictions_validated": 0,
        "astrology_production_rules_promoted": 0,
    }
    (B / "PORTABLE_DEPENDENCY_DRAFT_SOURCE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return receipt


if __name__ == "__main__":
    result = build()
    print(
        json.dumps(
            {
                "filename": result["owner_local_archive_path"],
                "bytes": result["archive_bytes"],
                "sha256": result["archive_SHA256"],
                "members": result["member_count"],
                "cold_source_tests": result[
                    "independent_cold_original_source_dependency_tests_green"
                ],
                "cold_original_synthetic_120_chart_replay": result[
                    "independent_cold_120_synthetic_chart_coverage_recomputed_exactly"
                ],
                "independent_real_human_validations": 0,
            },
            indent=2,
        )
    )
