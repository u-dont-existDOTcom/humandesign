#!/usr/bin/env python3
"""Cold-replayable, source SHA-verified synthetic-only chart eligibility archive.

Includes the EXACT 899155 byte original accepted synthetic parity JSON from
a pinned distinct Git commit without tracking a second redundant copy in this
research branch. The copy exists only INSIDE the portable verification archive.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import audit_synthetic_natal_feature_coverage as audit

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
FILENAME = "Astrology-Four-Star-Life-Palace-Synthetic-Coverage-20261020.zip"


def h(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def build() -> dict:
    p = subprocess.run(
        ["git", "show", f"{audit.PARITY_COMMIT}:{audit.PARITY_PATH}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    fixture = p.stdout
    if len(fixture) != 899155 or h(fixture) != audit.PARITY_SHA:
        raise ValueError("Accepted 312 synthetic vendor case source SHA differs")
    others = [
        B / "audit_synthetic_natal_feature_coverage.py",
        B / "test_synthetic_natal_feature_coverage.py",
        B / "SYNTHETIC_CHART_FOUR_ANCHOR_ELIGIBILITY_AUDIT_V1.json",
        B / "SYNTHETIC_CHART_ELIGIBILITY_FINDINGS_20261020.md",
        B / "WORKING_CHECKPOINT_20261020.md",
        B / "build_portable_chart_eligibility_archive.py",
        ROOT
        / "tasks/astro-source-four-anchor-synthetic-20261020/SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json",
    ]
    blobs = {str(path.relative_to(ROOT)): path.read_bytes() for path in others}
    fixture_name = str((B / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json").relative_to(ROOT))
    blobs[fixture_name] = fixture
    manifest = {name: {"sha256": h(data), "bytes": len(data)} for name, data in blobs.items()}
    downloads = Path.home() / "Téléchargements"
    downloads.mkdir(parents=True, exist_ok=True)
    path = downloads / FILENAME
    with ZipFile(path, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for name, data in sorted(blobs.items()):
            z.writestr(name, data)
    with ZipFile(path) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(blobs):
            raise ValueError("Portable historical synthetic source archive CRC/member mismatch")
        for name, expect in manifest.items():
            raw = z.read(name)
            if h(raw) != expect["sha256"] or len(raw) != expect["bytes"]:
                raise ValueError("Cold source archive exact SHA/byte check failed " + name)
    with tempfile.TemporaryDirectory(prefix="Chinese_4_star_eligibility_cold_") as directory:
        output = Path(directory)
        with ZipFile(path) as z:
            z.extractall(output)
        testdir = output / "tasks/astro-chart-eligibility-20261020"
        command = [
            "/usr/bin/python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(testdir),
            "-p",
            "test_synthetic_natal_feature_coverage.py",
            "-q",
        ]
        cp = subprocess.run(command, cwd=output, text=True, capture_output=True, timeout=60)
        logs = cp.stdout + cp.stderr
        if cp.returncode != 0 or "Ran 20 tests" not in logs or not logs.rstrip().endswith("OK"):
            print(logs[-1600:])
            raise ValueError("Independent cold source chart eligibility fixture tests failed")
        if (testdir / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json").read_bytes() != fixture:
            raise ValueError("Independent cold fixture original source bytes not identical")
    result = {
        "schema": "HUMANDESIGN_SYNTHETIC_FOUR_STAR_CHART_ELIGIBILITY_PORTABLE_V1",
        "status": "VERIFIED_PORTABLE_EXACT_SOURCE_AND_20_COLD_TOY_TESTS_NOT_HUMAN_ASTROLOGY",
        "owner_local_zip_path": str(path),
        "zip_filename": FILENAME,
        "zip_SHA256": h(path.read_bytes()),
        "zip_size_bytes": path.stat().st_size,
        "member_count": len(blobs),
        "original_member_SHA256_and_bytes": manifest,
        "zip_CRC_verified": True,
        "member_exact_SHA_and_bytes_verified": True,
        "source_original_fixture_sha256": audit.PARITY_SHA,
        "source_original_fixture_commit": audit.PARITY_COMMIT,
        "independent_cold_test_suite_executed": 20,
        "independent_cold_test_suite_green": 20,
        "actual_real_person_birth_records": 0,
        "actual_scored_human_responses": 0,
        "actual_validated_human_predictions": 0,
        "production_astrology_rules_promoted": 0,
    }
    (B / "PORTABLE_SOURCE_ORACLE_RECEIPT_20261020.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    doc = build()
    print(
        json.dumps(
            {
                "archive": doc["owner_local_zip_path"],
                "size": doc["zip_size_bytes"],
                "sha256": doc["zip_SHA256"],
                "members": doc["member_count"],
                "independent_cold_tests": doc["independent_cold_test_suite_green"],
                "human_predictive_validations": 0,
            },
            indent=2,
        )
    )
