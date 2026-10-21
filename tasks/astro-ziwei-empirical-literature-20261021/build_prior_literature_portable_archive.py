#!/usr/bin/env python3
"""Cold replay of original-source abstract-only astrology prior evidence.

Does not download paywalled/full theses or assert their contents were read.
Stores reviewed research metadata and independent negative/evidence tests.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import audit_external_prior_studies as audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAME = "HumanDesign-Astrology-External-ZiWei-Studies-Evidence-20261021.zip"


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def build() -> dict:
    audit.emit_receipt()
    selected = [
        audit.REG,
        audit.QUEUE,
        audit.REVIEW,
        audit.RECEIPT,
        HERE / "audit_external_prior_studies.py",
        HERE / "test_external_prior_studies.py",
        HERE / "WORKING_CHECKPOINT_20261021.md",
    ]
    content = {str(path.relative_to(ROOT)): path.read_bytes() for path in selected}
    manifest = {
        name: {"sha256": digest(raw), "bytes": len(raw)} for name, raw in sorted(content.items())
    }
    outdir = Path.home() / "Téléchargements"
    outdir.mkdir(parents=True, exist_ok=True)
    dest = outdir / NAME
    with ZipFile(dest, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for name, raw in sorted(content.items()):
            z.writestr(name, raw)
    with ZipFile(dest) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(content):
            raise ValueError("Original source metadata archive CRC/member set failed")
        for name, item in manifest.items():
            raw = z.read(name)
            if len(raw) != item["bytes"] or digest(raw) != item["sha256"]:
                raise ValueError("Exact source metadata archive hash/bytes failed " + name)
    with tempfile.TemporaryDirectory(prefix="ZiWei_empirical_prior_COLD_") as name:
        temp = Path(name)
        with ZipFile(dest) as z:
            z.extractall(temp)
        suite = temp / "tasks/astro-ziwei-empirical-literature-20261021"
        exe = "/home/joel/humandesign/.venv/bin/python"
        tests = subprocess.run(
            [
                exe,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(suite),
                "-p",
                "test_external_prior_studies.py",
                "-q",
            ],
            cwd=temp,
            capture_output=True,
            text=True,
            timeout=50,
        )
        log = tests.stdout + tests.stderr
        if tests.returncode or "Ran 18 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-1800:])
            raise ValueError("Independent cold source-metadata evidence tests not 18/18")
        outfile = suite / audit.RECEIPT.name
        expected = outfile.read_bytes()
        replay = subprocess.run(
            [exe, str(suite / "audit_external_prior_studies.py")],
            cwd=temp,
            capture_output=True,
            text=True,
            timeout=40,
        )
        if replay.returncode:
            print(replay.stderr[-1400:])
            raise ValueError("Cold source-registry metadata verification script failed")
        if outfile.read_bytes() != expected:
            raise ValueError("Cold replay changed original study provenance evidence")
    result = {
        "schema": "HUMANDESIGN_ZIWEI_PRIOR_HUMAN_STUDY_ABSTRACT_COLD_SOURCE_ARCHIVE_V1",
        "status": "COLD_VERIFIED_AUTHOR_ABSTRACT_METADATA_ONLY_FULL_THESIS_BLOCKED",
        "archive_owner_local_path": str(dest),
        "archive_filename": NAME,
        "archive_sha256": digest(dest.read_bytes()),
        "archive_bytes": dest.stat().st_size,
        "member_count": len(manifest),
        "exact_file_source_sha256_and_bytes": manifest,
        "zip_crc_verified": True,
        "all_member_hashes_and_lengths_verified": True,
        "independent_cold_unit_tests_green": 18,
        "independent_cold_metadata_review_replay_identical": True,
        "direct_ZiWei_studies_reviewed": 2,
        "full_original_Taiwan_theses_downloaded": 0,
        "external_Western_studies_methods_comparator_only": 5,
        "real_HumanDesign_astrology_predictive_trials": 0,
    }
    (HERE / "PORTABLE_EMPIRICAL_PRIOR_EVIDENCE_RECEIPT_20261021.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    result = build()
    print(
        json.dumps(
            {
                "archive": result["archive_owner_local_path"],
                "bytes": result["archive_bytes"],
                "sha256": result["archive_sha256"],
                "members": result["member_count"],
                "cold_tests": result["independent_cold_unit_tests_green"],
                "cold_metadata_source_replay": result[
                    "independent_cold_metadata_review_replay_identical"
                ],
                "full_Chinese_theses_available": result["full_original_Taiwan_theses_downloaded"],
                "project_predictive_validations": 0,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
