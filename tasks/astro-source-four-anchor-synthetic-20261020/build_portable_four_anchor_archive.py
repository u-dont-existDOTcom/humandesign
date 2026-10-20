#!/usr/bin/env python3
"""Portable source-anchored toy-only scorer with independently extracted tests.

Original Chinese source bytes + versioned source lines + reused HD metric
modules and mocked charts/respondents are included. Installed Python package
runtime (pydantic) is external and NOT falsely described as fully standalone.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017"
NAME = "Astrology-ZiWei-Four-Anchors-Synthetic-Blind-Scoring-20261020.zip"


def hash_data(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def package() -> dict:
    prior = [
        CHINA / "CHINESE_SOURCE_AUDIT_INDEX_V14.json",
        CHINA / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt",
        CHINA
        / "batches/ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",
        CHINA
        / "batches/ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json",
        CHINA
        / "batches/ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json",
        CHINA
        / "batches/ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json",
        ROOT / "tasks/astro-blind-readiness-20261020/READINESS_GATES_V1.json",
        ROOT / "src/hdmatch/__init__.py",
        ROOT / "src/hdmatch/evaluation/__init__.py",
        ROOT / "src/hdmatch/evaluation/failures.py",
        ROOT / "src/hdmatch/evaluation/metrics.py",
        ROOT / "src/hdmatch/evaluation/permutation.py",
    ]
    excluded = {
        "PORTABLE_ARCHIVE_RECEIPT_20261020.json",
        "PROTOTYPE_VERIFICATION_RECEIPT_20261020.json",
        "ACCEPTED_CONTINUATION_HANDOFF_20261020.md",
    }
    current = [
        p
        for p in B.rglob("*")
        if p.is_file()
        and p.suffix in (".py", ".json", ".md")
        and p.name not in excluded
        and "__pycache__" not in str(p)
        and "recovery" not in str(p)
    ]
    files = sorted(set(prior + current), key=lambda x: str(x.relative_to(ROOT)))
    checked = {}
    for p in files:
        blob = p.read_bytes()
        checked[str(p.relative_to(ROOT))] = {"sha256": hash_data(blob), "bytes": len(blob)}
    downloads = Path.home() / "Téléchargements"
    downloads.mkdir(parents=True, exist_ok=True)
    archive = downloads / NAME
    with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for p in files:
            z.write(p, arcname=str(p.relative_to(ROOT)))
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(checked):
            raise ValueError("Portable archive corrupt CRC or mismatched member paths")
        for name, item in checked.items():
            data = z.read(name)
            if hash_data(data) != item["sha256"] or len(data) != item["bytes"]:
                raise ValueError("Portable member original bytes/hash changed " + name)
    with tempfile.TemporaryDirectory(prefix="astrology_four_anchors_cold_") as d:
        extracted = Path(d)
        with ZipFile(archive) as z:
            z.extractall(extracted)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(extracted / "src")
        suite = extracted / "tasks/astro-source-four-anchor-synthetic-20261020"
        command = [
            "/home/joel/humandesign/.venv/bin/python",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(suite),
            "-p",
            "test_four_anchor_synthetic.py",
            "-q",
        ]
        result = subprocess.run(
            command, cwd=extracted, env=env, capture_output=True, text=True, timeout=50
        )
        logs = result.stdout + result.stderr
        if result.returncode or "Ran 20 tests" not in logs or not logs.rstrip().endswith("OK"):
            print(logs[-1900:])
            raise ValueError("Cold extracted synthetic source and scorer tests not 20/20 green")
        source_passes = 20
        seal_path = (
            extracted
            / "tasks"
            / "astro-source-four-anchor-synthetic-20261020"
            / "SYNTHETIC_PRE_RESPONSE_SEAL_V1.json"
        )
        if not seal_path.is_file():
            raise ValueError("Synthetic sealed prediction package absent in cold archive")
    manifest = {
        "schema": "HUMANDESIGN_ASTROLOGY_SYNTHETIC_SOURCE_TO_QUESTION_PORTABLE_RECEIPT_V1",
        "status": "EXACT_SOURCE_BYTES_AND_COLD_TOY_TESTS_VERIFIED_NOT_HUMAN_STUDY",
        "zip_filename": NAME,
        "owner_local_archive_path": str(archive),
        "zip_sha256": hash_data(archive.read_bytes()),
        "zip_size_bytes": archive.stat().st_size,
        "member_count": len(checked),
        "original_source_member_SHA_and_bytes": checked,
        "zip_CRC_verified": True,
        "all_member_exact_SHA_and_size_verified": True,
        "independent_cold_extracted_toy_source_tests_green": source_passes,
        "cold_test_interpreter": "/home/joel/humandesign/.venv/bin/python",
        "runtime_requires_external_installed_pydantic": True,
        "actual_human_participant_records": 0,
        "validated_real_human_predictions": 0,
        "scored_actual_birth_charts": 0,
        "model_ready_for_human_recruitment": False,
        "source_all_aux_stars_interpreted": False,
    }
    (B / "PORTABLE_ARCHIVE_RECEIPT_20261020.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    obj = package()
    print(
        json.dumps(
            {
                "zip": obj["owner_local_archive_path"],
                "bytes": obj["zip_size_bytes"],
                "SHA256": obj["zip_sha256"],
                "members": obj["member_count"],
                "cold_source_and_toy_tests_green": obj[
                    "independent_cold_extracted_toy_source_tests_green"
                ],
                "actual_human_predictions": 0,
            },
            indent=2,
        )
    )
