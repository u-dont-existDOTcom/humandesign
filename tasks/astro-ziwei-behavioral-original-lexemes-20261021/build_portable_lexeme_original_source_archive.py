#!/usr/bin/env python3
"""Cold replay of exact original Chinese text and 11 source lexical matches.

Includes accepted original Wikitext, its V14 index/source notes, four
provisional source candidate claims and independent 312 synthetic source
oracle as ZIP-only fixture. No real birth records or human outcome data.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import audit_original_trait_lexical_overlap as audit

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
NAME = "Astrology-ZiWei-Original-Life-Behavior-Lexeme-Overlap-20261021.zip"


def h(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def build():
    audit.accepted_source()
    witnesses = audit.phrase_inventory()
    if len(witnesses) != 11:
        raise ValueError("Expected exact 11 fixed historical lexical source quotes")
    cp = subprocess.run(
        ["git", "show", f"{audit.ORACLE_COMMIT}:{audit.ORACLE_PATH}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    raw = cp.stdout
    if len(raw) != 899155 or h(raw) != audit.ORACLE_SHA:
        raise ValueError("Previously accepted synthetic chart oracle bytes changed")
    selected = [
        audit.RAW,
        audit.INDEX,
        audit.CANDIDATE,
    ] + [
        audit.CHINA / "batches" / source[2]
        for source in audit.SOURCE_GROUPS.values()
        if source[2] is not None
    ]
    local = [
        p
        for p in B.rglob("*")
        if p.is_file()
        and p.suffix in (".py", ".md", ".json")
        and "__pycache__" not in str(p)
        and p.name
        not in (
            "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json",
            "PORTABLE_ORIGINAL_LEXEME_SOURCE_RECEIPT_20261021.json",
            "CONTINUATION_HANDOFF_ACCEPTED_20261021.md",
        )
    ]
    blobs = {
        str(f.relative_to(ROOT)): f.read_bytes()
        for f in sorted(set(selected + local), key=lambda x: str(x.relative_to(ROOT)))
    }
    blobs[str(audit.COLD_ORACLE.relative_to(ROOT))] = raw
    manifest = {
        name: {"sha256": h(content), "bytes": len(content)}
        for name, content in sorted(blobs.items())
    }
    downloads = Path.home() / "Téléchargements"
    downloads.mkdir(parents=True, exist_ok=True)
    archive = downloads / NAME
    with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=3) as z:
        for name, data in sorted(blobs.items()):
            z.writestr(name, data)
    with ZipFile(archive) as z:
        if z.testzip() is not None or sorted(z.namelist()) != sorted(blobs):
            raise ValueError("Source ZIP CRC or member list not original")
        for name, expect in manifest.items():
            data = z.read(name)
            if h(data) != expect["sha256"] or len(data) != expect["bytes"]:
                raise ValueError("Source ZIP exact SHA and size mismatch " + name)
    with tempfile.TemporaryDirectory(prefix="ZiWei_Behavior_Lexeme_Source_COLD_") as d:
        root = Path(d)
        with ZipFile(archive) as z:
            z.extractall(root)
        task = root / "tasks/astro-ziwei-behavioral-original-lexemes-20261021"
        tests = subprocess.run(
            [
                "/usr/bin/python3",
                "-m",
                "unittest",
                "discover",
                "-s",
                str(task),
                "-p",
                "test_original_trait_lexical_overlap.py",
                "-q",
            ],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
        )
        log = tests.stdout + tests.stderr
        if tests.returncode or "Ran 23 tests" not in log or not log.rstrip().endswith("OK"):
            print(log[-1800:])
            raise ValueError("Original lexical source cold tests not 23/23 green")
        resultfile = task / "ZIWEI_LIFE_BEHAVIORAL_LEXEME_OVERLAP_SOURCE_AUDIT_V1.json"
        before = resultfile.read_bytes()
        replay = subprocess.run(
            ["/usr/bin/python3", str(task / "audit_original_trait_lexical_overlap.py")],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if replay.returncode:
            print(replay.stderr[-1900:])
            raise ValueError("Original transmitted Wikitext lexical audit cold replay failed")
        if resultfile.read_bytes() != before:
            raise ValueError("Exact original textual results differ after cold extraction")
    receipt = {
        "schema": "HUMANDESIGN_PINNED_ZIWEI_FOUR_BEHAVIOR_LEXEMES_COLD_SOURCE_V1",
        "status": "ORIGINAL_CHINESE_SOURCE_EXACT_LEXEMES_COLD_VERIFIED_NOT_HUMAN_TEST",
        "original_full_transmitted_raw_source_sha256": audit.RAW_SHA,
        "original_312_synthetic_chart_data_sha256": audit.ORACLE_SHA,
        "owner_local_archive_path": str(archive),
        "archive_filename": NAME,
        "archive_sha256": h(archive.read_bytes()),
        "archive_bytes": archive.stat().st_size,
        "member_count": len(blobs),
        "exact_original_source_member_sha256_and_bytes": manifest,
        "zip_CRC_verified": True,
        "all_members_SHA_and_size_verified": True,
        "independent_cold_source_exact_lexeme_tests_green": 23,
        "independent_cold_recomputed_11_original_lexeme_hits_bytewise_identical": True,
        "literal_scholarly_word_equivalence_independently_verified": False,
        "human_personality_predictive_validations": 0,
        "production_astrology_rule_promotions": 0,
    }
    (B / "PORTABLE_ORIGINAL_LEXEME_SOURCE_RECEIPT_20261021.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return receipt


if __name__ == "__main__":
    result = build()
    print(
        json.dumps(
            {
                "owner_zip": result["owner_local_archive_path"],
                "sha256": result["archive_sha256"],
                "bytes": result["archive_bytes"],
                "members": result["member_count"],
                "cold_source_tests": result["independent_cold_source_exact_lexeme_tests_green"],
                "independent_replay_identical": result[
                    "independent_cold_recomputed_11_original_lexeme_hits_bytewise_identical"
                ],
                "human_predictive_tests": 0,
            },
            indent=2,
        )
    )
