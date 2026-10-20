#!/usr/bin/env python3
"""Cold extraction of exact pinned source/chart engine, HKO bytes and tests.

External lunar_python/sxtwl compiled files are *not* bundled. Test/replay
requires both already-installed source- and binary-SHA verified versions.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import run_pinned_natal_policy_sensitivity as main

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
NAME = "Astrology-ZiWei-Pinned-Natal-Calendar-Policy-Synthetic-20261020.zip"


def h(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def build():
    source = main.verified_sources()
    earlier = [
        main.PREVIOUS,
    ]
    local = [
        p
        for p in B.rglob("*")
        if p.is_file()
        and p.suffix in (".json", ".md", ".py")
        and "__pycache__" not in str(p)
        and p.name
        not in (
            "PORTABLE_ORIGINAL_NATAL_SOURCE_RECEIPT_20261020.json",
            "CONTINUATION_HANDOFF_ACCEPTED_20261020.md",
        )
    ]
    other = sorted(set(local + earlier), key=lambda p: str(p.relative_to(ROOT)))
    files = {str(p.relative_to(ROOT)): p.read_bytes() for p in other}
    files.update(source)
    members = {name: {"sha256": h(raw), "bytes": len(raw)} for name, raw in sorted(files.items())}
    dest = Path.home() / "Téléchargements"
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / NAME
    with ZipFile(out, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for name, raw in sorted(files.items()):
            z.writestr(name, raw)
    with ZipFile(out) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(files):
            raise ValueError("Pinned original source ZIP member set or CRC changed")
        for name, entry in members.items():
            b = z.read(name)
            if h(b) != entry["sha256"] or len(b) != entry["bytes"]:
                raise ValueError("Cold original source SHA/member bytes mismatch " + name)
    with tempfile.TemporaryDirectory(prefix="Chinese_Natal_Policy_COLD_") as d:
        tmp = Path(d)
        with ZipFile(out) as z:
            z.extractall(tmp)
        suite = tmp / "tasks/astro-ziwei-natal-policy-sensitivity-20261020"
        if len(main.verified_sources.__code__.co_varnames) < 1:
            raise ValueError("Source engine hash verifier unavailable")
        env = os.environ.copy()
        env["ZIWEI_PINNED_CALENDAR_SITE"] = str(main.DEFAULT_CALENDAR_PACKAGE_SITE)
        exe = "/home/joel/humandesign/.venv/bin/python"
        test = subprocess.run(
            [
                exe,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(suite),
                "-p",
                "test_pinned_synthetic_natal_policy.py",
                "-q",
            ],
            cwd=tmp,
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
        )
        logs = test.stdout + test.stderr
        if test.returncode != 0 or "Ran 18 tests" not in logs or not logs.rstrip().endswith("OK"):
            print(logs[-1700:])
            raise ValueError("Independent cold source+policy tests not 18/18")
        source_before = (
            suite / "PINNED_ENGINE_SYNTHETIC_NATAL_POLICY_SENSITIVITY_V1.json"
        ).read_bytes()
        rerun = subprocess.run(
            [exe, str(suite / "run_pinned_natal_policy_sensitivity.py")],
            cwd=tmp,
            env=env,
            capture_output=True,
            text=True,
            timeout=100,
        )
        if rerun.returncode != 0:
            print(rerun.stderr[-1800:])
            raise ValueError("Cold extracted source engine full 48-policy replay failed")
        actual = (suite / "PINNED_ENGINE_SYNTHETIC_NATAL_POLICY_SENSITIVITY_V1.json").read_bytes()
        if actual != source_before:
            raise ValueError("Independent source engine cold policy results differ bytewise")
    receipt = {
        "schema": "HUMANDESIGN_PINNED_ZIWEI_NATAL_POLICY_PORTABLE_SOURCE_AND_COLD_TESTS_V1",
        "status": "SOURCE_ORACLE_AND_SYNTHETIC_NATAL_POLICIES_COLD_REPLAYED_NOT_PERSONAL_ASTROLOGY",
        "source_engine_versioned_git_commit": main.ENGINE_COMMIT,
        "source_file_sha_manifest": h(main.MANIFEST.read_bytes()),
        "archive_local_owner_path": str(out),
        "archive_filename": NAME,
        "archive_sha256": h(out.read_bytes()),
        "archive_bytes": out.stat().st_size,
        "original_source_and_test_member_count": len(files),
        "original_all_member_source_sha256_bytes": members,
        "zip_crc_passed": True,
        "source_member_exact_SHA_bytes_verified": True,
        "independent_cold_extracted_focused_tests_green": 18,
        "independent_cold_full_48_policy_replay_bytewise_identical": True,
        "optional_pinned_external_calendar_packages_required": (
            main.EXPECTED_LIBRARY_TREE_SHA.copy()
        ),
        "optional_calendar_package_binaries_copied_into_repo_or_zip": False,
        "real_human_birth_dates_or_questionnaire_responses": 0,
        "validated_astrology_human_predictions": 0,
        "production_astro_rules_promoted": 0,
    }
    (B / "PORTABLE_ORIGINAL_NATAL_SOURCE_RECEIPT_20261020.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return receipt


if __name__ == "__main__":
    data = build()
    print(
        json.dumps(
            {
                "filename": data["archive_filename"],
                "bytes": data["archive_bytes"],
                "sha256": data["archive_sha256"],
                "members": data["original_source_and_test_member_count"],
                "independent_cold_tests": data["independent_cold_extracted_focused_tests_green"],
                "replay_48_policy_rows_bytewise": data[
                    "independent_cold_full_48_policy_replay_bytewise_identical"
                ],
                "actual_human_predictions": 0,
            },
            indent=2,
        )
    )
