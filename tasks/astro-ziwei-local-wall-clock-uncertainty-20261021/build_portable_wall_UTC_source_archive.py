#!/usr/bin/env python3
"""Cold original-source hash verification and Zi Wei synthetic wall-clock replay.

The owner must already have pinned lunar_python and sxtwl packages with
source/binary SHA from accepted parent; no outside package binaries are copied.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import run_source_pinned_local_wall_UTC_union as run

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAME = "Astrology-ZiWei-Synthetic-Local-Wall-UTC-DST-Fold-20261021.zip"


def h(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def build() -> dict:
    run.verify_parent()
    # Reconstruct original accepted source 22-member engine from its own
    # immutable commit or already SHA-verified files without editing any
    # previously accepted research worktree.
    import sys

    sys.path.insert(0, str(run.PARENT))
    try:
        import run_source_pinned_utc_intervals as previous
    finally:
        sys.path.pop(0)
    original, source = previous.get_original_source()
    parents = [
        run.PARENT_RUNNER,
        run.PARENT_WORKER,
        run.PARENT_REPORT,
        previous.PARENT_RUNNER,
        previous.PARENT_MANIFEST,
        previous.PARENT_REPORT,
    ]
    local = [
        f
        for f in HERE.rglob("*")
        if f.is_file()
        and f.suffix in (".json", ".md", ".py")
        and "__pycache__" not in str(f)
        and f.name
        not in (
            "PORTABLE_WALL_UTC_ORIGINAL_SOURCE_RECEIPT_20261021.json",
            "CONTINUATION_HANDOFF_ACCEPTED_20261021.md",
        )
    ]
    files = {str(p.relative_to(ROOT)): p.read_bytes() for p in set(parents + local)}
    files.update(source)
    member = {name: {"sha256": h(raw), "bytes": len(raw)} for name, raw in sorted(files.items())}
    directory = Path.home() / "Téléchargements"
    directory.mkdir(parents=True, exist_ok=True)
    out = directory / NAME
    with ZipFile(out, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for name, raw in sorted(files.items()):
            z.writestr(name, raw)
    with ZipFile(out) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(files):
            raise ValueError("Archive member list/CRC unexpectedly changed")
        for name, item in member.items():
            raw = z.read(name)
            if len(raw) != item["bytes"] or h(raw) != item["sha256"]:
                raise ValueError("Original source cold archive exact SHA/byte mismatch " + name)
    with tempfile.TemporaryDirectory(prefix="ZiWei_Wall_UTC_PEP495_COLD_") as d:
        root = Path(d)
        with ZipFile(out) as z:
            z.extractall(root)
        folder = root / "tasks/astro-ziwei-local-wall-clock-uncertainty-20261021"
        env = os.environ.copy()
        env["ZIWEI_PINNED_CALENDAR_SITE"] = str(run.LIBRARY_SITE)
        exe = "/home/joel/humandesign/.venv/bin/python"
        test = subprocess.run(
            [
                exe,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(folder),
                "-p",
                "test_synthetic_wall_clock_UTC_union.py",
                "-q",
            ],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
        )
        log = test.stdout + test.stderr
        if test.returncode or "Ran 20 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-2000:])
            raise ValueError("Cold original wall-clock source tests not 20/20 green")
        previous = (
            folder / "PINNED_SOURCE_SYNTHETIC_WALL_CLOCK_UTC_FOLD_UNION_V1.json"
        ).read_bytes()
        run_result = subprocess.run(
            [exe, str(folder / "run_source_pinned_local_wall_UTC_union.py")],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=110,
        )
        if run_result.returncode:
            print(run_result.stderr[-2000:])
            raise ValueError("Cold original local-wall-to-UTC source fold replay failed")
        after = (folder / "PINNED_SOURCE_SYNTHETIC_WALL_CLOCK_UTC_FOLD_UNION_V1.json").read_bytes()
        if previous != after:
            raise ValueError("Original source UTC union output changed after cold replay")
    receipt = {
        "schema": "HUMANDESIGN_ZIWEI_SYNTHETIC_WALL_UTC_PEP495_COLD_SOURCE_ARCHIVE_V1",
        "status": "HASHED_SOURCE_AND_REAL_DST_FOLD_MECHANICS_COLD_REPLAYED_ONLY_NOT_HUMAN_STUDY",
        "original_ZiWei_natal_source_engine_commit": run.ORIGINAL_COMMIT,
        "accepted_prior_UTC_second_checker_commit": run.PARENT_COMMIT,
        "source_ZiWei_original_code_22_file_sha_member_count": len(source),
        "archive_owner_local_file": str(out),
        "archive_filename": NAME,
        "archive_SHA256": h(out.read_bytes()),
        "archive_bytes": out.stat().st_size,
        "member_count": len(files),
        "all_member_original_SHA256_bytes": member,
        "zip_original_CRC_passed": True,
        "all_member_hash_and_size_verified": True,
        "independent_cold_source_tests_green": 20,
        "independent_cold_full_PEP495_UTC_union_replay_identical": True,
        "external_optional_calendar_libraries_are_not_copied_or_redistributed": True,
        "original_optional_library_binary_tree_sha256": original.EXPECTED_LIBRARY_TREE_SHA.copy(),
        "actual_human_birth_or_survey_records": 0,
        "genuine_human_predictive_validations": 0,
        "production_astro_runtime_rules": 0,
    }
    (HERE / "PORTABLE_WALL_UTC_ORIGINAL_SOURCE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return receipt


if __name__ == "__main__":
    data = build()
    print(
        json.dumps(
            {
                "archive": data["archive_owner_local_file"],
                "size_bytes": data["archive_bytes"],
                "SHA256": data["archive_SHA256"],
                "members": data["member_count"],
                "cold_source_tests": data["independent_cold_source_tests_green"],
                "cold_replay_bytewise_identical": data[
                    "independent_cold_full_PEP495_UTC_union_replay_identical"
                ],
                "real_human_predictions": 0,
            },
            indent=2,
        )
    )
