#!/usr/bin/env python3
"""Cold-replayable original source Zi Wei finite synthetic UTC interval archive.

The optional lunar software packages and native binaries are NOT bundled.
Only the owner's existing independently SHA-pinned runtime can replay charts.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import run_source_pinned_utc_intervals as run

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
NAME = "Astrology-ZiWei-Original-Finite-UTC-Interval-Source-20261021.zip"


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def build() -> dict:
    original, source = run.get_original_source()
    parents = [
        run.PARENT_RUNNER,
        run.PARENT_MANIFEST,
        run.PARENT_REPORT,
    ]
    locals = [
        x
        for x in B.rglob("*")
        if x.is_file()
        and x.suffix in (".json", ".py", ".md")
        and "__pycache__" not in str(x)
        and x.name
        not in (
            "PORTABLE_FINITE_SOURCE_INTERVAL_RECEIPT_20261021.json",
            "CONTINUATION_HANDOFF_ACCEPTED_20261021.md",
        )
    ]
    files = {str(f.relative_to(ROOT)): f.read_bytes() for f in set(parents + locals)}
    files.update(source)
    members = {
        name: {"sha256": digest(content), "bytes": len(content)}
        for name, content in sorted(files.items())
    }
    directory = Path.home() / "Téléchargements"
    directory.mkdir(parents=True, exist_ok=True)
    archive = directory / NAME
    with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for name, data in sorted(files.items()):
            z.writestr(name, data)
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(files):
            raise ValueError("Original source package CRC or member count wrong")
        for name, meta in members.items():
            data = z.read(name)
            if len(data) != meta["bytes"] or digest(data) != meta["sha256"]:
                raise ValueError("Original source ZIP exact byte/SHA mismatch " + name)
    with tempfile.TemporaryDirectory(prefix="ZiWei_Finite_UTC_Source_COLD_") as d:
        root = Path(d)
        with ZipFile(archive) as z:
            z.extractall(root)
        suite = root / "tasks/astro-ziwei-finite-utc-uncertainty-20261020"
        environment = os.environ.copy()
        environment["ZIWEI_PINNED_CALENDAR_SITE"] = str(run.CALENDAR_RUNTIME_DEFAULT)
        py = "/home/joel/humandesign/.venv/bin/python"
        cmd = [
            py,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(suite),
            "-p",
            "test_finite_utc_source_intervals.py",
            "-q",
        ]
        proc = subprocess.run(
            cmd, cwd=root, env=environment, capture_output=True, text=True, timeout=90
        )
        logs = proc.stdout + proc.stderr
        if proc.returncode or "Ran 20 tests" not in logs or not logs.rstrip().endswith("OK"):
            print(logs[-2500:])
            raise ValueError("Cold extracted 20 original source finite UTC tests failed")
        expected = (
            suite / "FINITE_UTC_SECOND_SYNTHETIC_ORIGINAL_SOURCE_CHART_SETS_V1.json"
        ).read_bytes()
        proc = subprocess.run(
            [py, str(suite / "run_source_pinned_utc_intervals.py")],
            cwd=root,
            env=environment,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode:
            print(proc.stderr[-1800:])
            raise ValueError("Cold extracted full 1206-second original chart replay failed")
        got = (
            suite / "FINITE_UTC_SECOND_SYNTHETIC_ORIGINAL_SOURCE_CHART_SETS_V1.json"
        ).read_bytes()
        if got != expected:
            raise ValueError(
                "Original finite UTC synthetic chart result differs bytewise on cold replay"
            )
    receipt = {
        "schema": "HUMANDESIGN_ZIWEI_FINITE_UTC_ORIGINAL_SOURCE_COLD_ARCHIVE_V1",
        "status": "EXACT_SOURCE_HASH_COLD_INTERVAL_REPLAY_NO_HUMAN_ASTROLOGY",
        "source_engine_original_parent_commit": run.ENGINE_COMMIT,
        "accepted_parent_original_source_sha256": run.PARENT_MANIFEST_SHA,
        "archive_owner_computer_path": str(archive),
        "archive_file_name": NAME,
        "archive_sha256": digest(archive.read_bytes()),
        "archive_bytes": archive.stat().st_size,
        "archive_member_count": len(files),
        "original_source_members_SHA256_and_bytes": members,
        "zip_original_CRC_verified": True,
        "all_source_members_SHA256_and_bytes_verified": True,
        "independent_cold_extract_unit_tests_green": 20,
        "independent_cold_extracted_full_4824_policy_tick_replay_identical": True,
        "optional_calendar_libraries_source_binary_sha_pinned_but_not_bundled": (
            original.EXPECTED_LIBRARY_TREE_SHA.copy()
        ),
        "external_calendar_binaries_in_archive": False,
        "actual_human_birth_records": 0,
        "real_human_predictive_validations": 0,
        "runtime_astrology_rule_promotions": 0,
    }
    (B / "PORTABLE_FINITE_SOURCE_INTERVAL_RECEIPT_20261021.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return receipt


if __name__ == "__main__":
    info = build()
    print(
        json.dumps(
            {
                "archive": info["archive_owner_computer_path"],
                "bytes": info["archive_bytes"],
                "sha256": info["archive_sha256"],
                "members": info["archive_member_count"],
                "independent_tests": info["independent_cold_extract_unit_tests_green"],
                "full_source_replay_same_bytes": info[
                    "independent_cold_extracted_full_4824_policy_tick_replay_identical"
                ],
                "actual_human_predictions": 0,
            },
            indent=2,
        )
    )
