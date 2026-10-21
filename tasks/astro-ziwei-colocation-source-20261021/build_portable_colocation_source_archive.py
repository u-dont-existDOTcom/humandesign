#!/usr/bin/env python3
"""Independently cold-check a source-only Zi Wei pair/condition audit package.

ZIP includes exact transmitted original Chinese text and accepted source note
records, 312 previously accepted SYNTHETIC oracle-comparison rows and code.
No real person birth records or psychological outcomes. No user secrets.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import audit_original_four_star_colocations as audit

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
NAME = "Astrology-ZiWei-Original-Four-Trait-CoStar-Clauses-20261021.zip"
FIXTURE = B / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json"


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def build():
    audit.accepted_text()
    old = audit.source_notes()
    assert len(audit.original_grade_witnesses(old)) == 15
    assert len(audit.narrative_clusters(old)) == 7
    parent = subprocess.run(
        ["git", "show", f"{audit.ORACLE_COMMIT}:{audit.ORACLE_FILE}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    oracle = parent.stdout
    if len(oracle) != audit.ORACLE_BYTES or digest(oracle) != audit.ORACLE_SHA:
        raise ValueError("Previously accepted synthetic original source oracle changed")
    required = [
        audit.RAW,
        audit.INDEX,
        audit.MAP,
    ] + [audit.CHINA / "batches" / rel for rel in audit.ORIGINAL_SOURCE_FILES.values()]
    local = [
        file
        for file in B.rglob("*")
        if file.is_file()
        and file.suffix in (".json", ".md", ".py")
        and "__pycache__" not in str(file)
        and file.name
        not in (
            "PORTABLE_COLOCATION_SOURCE_RECEIPT_20261021.json",
            "CONTINUATION_HANDOFF_ACCEPTED_20261021.md",
            "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json",
        )
    ]
    blobs = {str(p.relative_to(ROOT)): p.read_bytes() for p in sorted(set(required + local))}
    blobs[str(FIXTURE.relative_to(ROOT))] = oracle
    members = {
        rel: {"bytes": len(blob), "sha256": digest(blob)} for rel, blob in sorted(blobs.items())
    }
    outdir = Path.home() / "Téléchargements"
    outdir.mkdir(parents=True, exist_ok=True)
    archive = outdir / NAME
    with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for name, raw in sorted(blobs.items()):
            z.writestr(name, raw)
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(blobs):
            raise ValueError("Cold source ZIP member list or CRC mismatch")
        for name, check in members.items():
            content = z.read(name)
            if len(content) != check["bytes"] or digest(content) != check["sha256"]:
                raise ValueError("Exact source ZIP hash/bytes mismatch " + name)
    with tempfile.TemporaryDirectory(prefix="ZiWei_Four_Star_CoStar_Source_COLD_") as d:
        root = Path(d)
        with ZipFile(archive) as z:
            z.extractall(root)
        directory = root / "tasks/astro-ziwei-colocation-source-20261021"
        cmd = [
            "/usr/bin/python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(directory),
            "-p",
            "test_original_four_star_colocations.py",
            "-q",
        ]
        cp = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=60)
        log = cp.stdout + cp.stderr
        if cp.returncode or "Ran 23 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-2400:])
            raise ValueError("Independently cold Zi Wei source 23 tests not green")
        source_before = (
            directory / "ORIGINAL_FOUR_BEHAVIOR_STAR_COLOCATION_SOURCE_AUDIT_V1.json"
        ).read_bytes()
        replay = subprocess.run(
            ["/usr/bin/python3", str(directory / "audit_original_four_star_colocations.py")],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if replay.returncode:
            print(replay.stderr[-1500:])
            raise ValueError("Independent original-text exact SHA co-star audit replay failed")
        replay_result = directory / "ORIGINAL_FOUR_BEHAVIOR_STAR_COLOCATION_SOURCE_AUDIT_V1.json"
        if replay_result.read_bytes() != source_before:
            raise ValueError("Independently replayed original source audit differs bytewise")
    receipt = {
        "schema": "HUMANDESIGN_ZIWEI_ORIGINAL_FOUR_STAR_PAIR_CONDITIONAL_SOURCE_COLD_V1",
        "status": "EXACT_QUOTE_SOURCE_SHA_AND_SYNTHETIC_PAIR_COMPARISON_ONLY_NOT_HUMAN_PREDICTION",
        "owner_local_archive_path": str(archive),
        "archive_filename": NAME,
        "archive_sha256": digest(archive.read_bytes()),
        "archive_bytes": archive.stat().st_size,
        "original_exact_member_count": len(blobs),
        "original_member_sha256_and_bytes": members,
        "zip_crc_verified": True,
        "all_original_file_member_sha_and_bytes_verified": True,
        "accepted_original_Chinese_raw_wikitext_sha256": audit.SOURCE_SHA,
        "original_312_synthetic_vendor_dataset_sha256": audit.ORACLE_SHA,
        "source_15_pair_grade_rules_literal_not_behavioural_modifiers": True,
        "cold_extracted_focused_unit_tests_green": 23,
        "cold_replay_full_original_source_and_120_synthetic_result_byte_identical": True,
        "scored_actual_human_birth_and_questionnaire_records": 0,
        "human_predictive_validations": 0,
        "runtime_astrology_rule_promotions": 0,
    }
    (B / "PORTABLE_COLOCATION_SOURCE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return receipt


if __name__ == "__main__":
    r = build()
    print(
        json.dumps(
            {
                "archive": r["owner_local_archive_path"],
                "size": r["archive_bytes"],
                "sha256": r["archive_sha256"],
                "member_count": r["original_exact_member_count"],
                "cold_unit_tests_green": r["cold_extracted_focused_unit_tests_green"],
                "independent_source_replay_bytewise": r[
                    "cold_replay_full_original_source_and_120_synthetic_result_byte_identical"
                ],
                "verified_human_predictions": 0,
            },
            indent=2,
        )
    )
