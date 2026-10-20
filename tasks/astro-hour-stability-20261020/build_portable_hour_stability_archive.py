#!/usr/bin/env python3
"""Cold verified source-locked previous audit + original synthetic oracle package."""

from __future__ import annotations

import json
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UP = ROOT / "tasks/astro-chart-eligibility-20261020"
ORIG = ROOT / "tasks/astro-chinese-primary-sources-20261017"
SOURCE_PATH = UP / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json"
NAME = "Astrology-ZiWei-Four-Anchors-Hour-Stability-20261020.zip"


def sha(blob: bytes) -> str:
    return sha256(blob).hexdigest()


def archive():
    from audit_conservative_feature_states import oracle

    command = ["git", "show", f"{oracle.PARITY_COMMIT}:{oracle.PARITY_PATH}"]
    raw = subprocess.run(command, cwd=ROOT, check=True, capture_output=True).stdout
    if sha(raw) != oracle.PARITY_SHA or len(raw) != 899155:
        raise ValueError("Accepted original 312 synthetic oracle bytes/SHA changed")
    parents = [
        UP / "audit_synthetic_natal_feature_coverage.py",
        UP / "SYNTHETIC_CHART_FOUR_ANCHOR_ELIGIBILITY_AUDIT_V1.json",
        ROOT
        / "tasks/astro-source-four-anchor-synthetic-20261020/SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json",
        ORIG / "CHINESE_SOURCE_AUDIT_INDEX_V14.json",
        ORIG / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
    ]
    local = [
        x
        for x in HERE.rglob("*")
        if x.is_file()
        and x.suffix in (".json", ".py", ".md")
        and "__pycache__" not in str(x)
        and x.name
        not in (
            "PORTABLE_HOUR_STABILITY_RECEIPT_20261020.json",
            "CONTINUATION_HANDOFF_ACCEPTED_20261020.md",
        )
    ]
    sources = sorted(set(parents + local), key=lambda x: str(x.relative_to(ROOT)))
    files = {str(p.relative_to(ROOT)): p.read_bytes() for p in sources}
    files[str(SOURCE_PATH.relative_to(ROOT))] = raw
    members = {
        path: {"bytes": len(content), "sha256": sha(content)}
        for path, content in sorted(files.items())
    }
    output_dir = Path.home() / "Téléchargements"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / NAME
    with ZipFile(output, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for path, blob in sorted(files.items()):
            z.writestr(path, blob)
    with ZipFile(output) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(files):
            raise ValueError("Cold source package CRC/list invalid")
        for filename, expected in members.items():
            value = z.read(filename)
            if len(value) != expected["bytes"] or sha(value) != expected["sha256"]:
                raise ValueError("Source package exact member hash mismatch " + filename)
    with tempfile.TemporaryDirectory(prefix="ziwei_hour_stability_cold_") as dirname:
        root = Path(dirname)
        with ZipFile(output) as z:
            z.extractall(root)
        suite = root / "tasks/astro-hour-stability-20261020"
        command = [
            "/usr/bin/python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(suite),
            "-p",
            "test_source_hour_stability.py",
            "-q",
        ]
        test = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=60)
        out = test.stdout + test.stderr
        if test.returncode != 0 or "Ran 18 tests" not in out or not out.rstrip().endswith("OK"):
            print(out[-1900:])
            raise ValueError("Independent cold source/hour tests did not pass18/18")
        if (root / SOURCE_PATH.relative_to(ROOT)).read_bytes() != raw:
            raise ValueError("Original 312 case source bytes drift after cold extraction")
    receipt = {
        "schema": "HUMANDESIGN_FOUR_ANCHOR_HOUR_STABILITY_PORTABLE_ORIGINAL_SOURCE_V1",
        "status": "COLD_SOURCE_AND_SYNTHETIC_TESTS_PASSED_NOT_HUMAN_ASTROLOGY",
        "archive_name": NAME,
        "archive_on_owner_computer": str(output),
        "archive_sha256": sha(output.read_bytes()),
        "archive_bytes": output.stat().st_size,
        "member_count": len(files),
        "all_member_exact_source_bytes_SHA256": members,
        "independent_ZIP_CRC_verified": True,
        "all_member_sha_verified": True,
        "original_312_synthetic_oracle_sha256": oracle.PARITY_SHA,
        "independent_cold_source_hour_tests_passed": 18,
        "real_birth_records": 0,
        "real_human_scored_predictions": 0,
        "production_astrological_rules": 0,
    }
    (HERE / "PORTABLE_HOUR_STABILITY_RECEIPT_20261020.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return receipt


if __name__ == "__main__":
    r = archive()
    print(
        json.dumps(
            {
                "path": r["archive_on_owner_computer"],
                "SHA256": r["archive_sha256"],
                "bytes": r["archive_bytes"],
                "members": r["member_count"],
                "cold_source_tests": r["independent_cold_source_hour_tests_passed"],
                "human_predictions": 0,
            },
            indent=2,
        )
    )
