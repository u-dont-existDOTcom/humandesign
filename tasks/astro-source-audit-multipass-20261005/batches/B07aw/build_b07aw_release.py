#!/usr/bin/env python3
"""Hermetic 1647/1659 transit-source archive with independent 42-test replay."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
REL = TASK + "/batches/B07aw/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-Transit-Days-vs-Years-B07aw-20261019.zip"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def downloads() -> Path:
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    raw = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    if raw is not None and raw.is_dir() and raw.resolve() != Path.home().resolve():
        return raw
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


def package() -> None:
    notes = read(B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json")
    conflict = read(B / "ORIGINAL_1647_1659_MARS_TRANSIT_DURATION_SOURCE_CONFLICT_V1.json")
    boundary = read(B / "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json")
    candidate = read(B / "ACCEPTANCE.json")
    rules = read(B / "RULES.json")
    old = read(ROOT / INDEX)
    chinese = read(ROOT / CHINESE)
    assert old["records_count"] == 12845
    assert old["batches"][-1]["id"] == "B07av"
    assert chinese["sum_source_annotations"] == 355
    assert rules["record_count"] == notes["new_source_documentary_rule_count"] == 25
    assert candidate["rules_SHA256"] == sha(B / "RULES.json")
    assert candidate["source_full_document_SHA256"] == sha(
        B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json"
    )
    assert conflict["first_edition_implied_duration_unit"] == "days"
    assert conflict["second_edition_implied_duration_unit"] == "years"
    assert boundary["first_edition_original_chapter_numeral"] == "CLXXV"
    assert notes["independent_blinded_real_people_predictions_validated"] == 0
    assert notes["runtime_astrological_rule_promotions"] == 0

    names = [
        "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json",
        "ORIGINAL_1647_1659_MARS_TRANSIT_DURATION_SOURCE_CONFLICT_V1.json",
        "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json",
        "RULES.json",
        "ACCEPTANCE.json",
        "TASK_SCOPE.json",
        "ORIGINAL_TRANSITS_SOURCE_REVIEW_20261019.md",
        "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
        "build_b07aw_transit_source.py",
        "test_b07aw_original_transit.py",
        "build_b07aw_release.py",
        "prepare_b07aw_canonical.py",
        "evidence/1647_original-776.jpg",
        "evidence/1659_original_djvu_771.jpg",
        "evidence/transit_original_1647_mars_duration_crop.png",
        "evidence/transit_original_1659_mars_duration_crop.png",
    ]
    files = {REL + name: B / name for name in names}
    first = TASK + "/batches/B07av/evidence/1647_original-775.jpg"
    second = TASK + "/batches/B07av/evidence/1659_original_djvu_770.jpg"
    files[first] = ROOT / first
    files[second] = ROOT / second
    files[TASK + "/batches/B07av/RULES.json"] = B.parent / "B07av/RULES.json"
    files[INDEX] = ROOT / INDEX
    files[CHINESE] = ROOT / CHINESE
    assert all(f.is_file() for f in files.values()), [
        name for name, f in files.items() if not f.is_file()
    ]
    assert sha(files[first]) == conflict["original_first_edition_full_page_sha256"]
    assert sha(files[second]) == conflict["original_second_edition_full_page_sha256"]
    assert sha(B / "evidence/1647_original-776.jpg") == (boundary["new_first_edition_page_sha256"])
    assert (
        sha(B / "evidence/1659_original_djvu_771.jpg")
        == (boundary["new_second_typeset_edition_page_sha256"])
    )
    assert sha(B / conflict["first_edition_source_crop"]) == conflict["first_crop_sha256"]
    assert sha(B / conflict["second_edition_source_crop"]) == conflict["second_crop_sha256"]

    manifest = {
        "batch": "B07aw",
        "source": "William Lilly original 1647 and original second typeset 1659, printed741-742",
        "original_1647_pdf_full_source_SHA256": old["source_sha256"],
        "source_1647_transits_heading": "CLXXIIII",
        "source_1659_transits_heading": "CLXXIV",
        "first_edition_Mars_duration": "two or three dayes",
        "second_edition_Mars_duration": "two or three years",
        "following_original_new_chapter": "CLXXV Merchant Nativity",
        "historical_source_annotations": 25,
        "historical_Lilly_if_accepted": 12870,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "original_1647_natal_ephemeris_calculation_verified": False,
        "source_edition_critical_expert_corroboration_done": False,
        "human_predictive_validations": 0,
        "runtime_promotions": 0,
        "members": {
            name: {"sha256": sha(f), "bytes": f.stat().st_size} for name, f in files.items()
        },
    }
    folder = downloads()
    folder.mkdir(parents=True, exist_ok=True)
    archive = folder / NAME
    temp = folder / (NAME + ".building")
    assert not temp.exists(), temp
    with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, f in files.items():
            z.write(f, "B07aw-root/" + name)
        z.writestr(
            "B07aw-root/RELEASE_MANIFEST.json",
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        )

    with zipfile.ZipFile(temp) as z, tempfile.TemporaryDirectory() as td:
        assert z.testzip() is None
        z.extractall(td)
        root = Path(td) / "B07aw-root"
        assert read(root / "RELEASE_MANIFEST.json") == manifest
        for name, item in manifest["members"].items():
            f = root / name
            assert sha(f) == item["sha256"], name
            assert f.stat().st_size == item["bytes"], name
        test = subprocess.run(
            [
                "python3",
                "-m",
                "unittest",
                "discover",
                "-s",
                str(root / REL),
                "-p",
                "test_b07aw_original_transit.py",
                "-q",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        assert test.returncode == 0, test.stdout + "\n" + test.stderr
        found = re.search(r"Ran (\d+) tests", test.stderr)
        assert found and int(found.group(1)) == 42, test.stderr
        assert "skipped" not in test.stderr

    os.replace(temp, archive)
    receipt = {
        "batch": "B07aw",
        "status": "ORIGINAL_1647_1659_TRANSIT_DURATION_42_PORTABLE_TESTS_PASS",
        "filename": NAME,
        "archive_sha256": sha(archive),
        "archive_bytes": archive.stat().st_size,
        "member_count": len(files),
        "CRC_passed": True,
        "all_members_SHA256_and_bytes_passed": True,
        "independent_archive_test_replay_passed": True,
        "focused_source_tests_replayed": 42,
        "document_SHA256": sha(B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json"),
        "rules_SHA256": sha(B / "RULES.json"),
        "before_Lilly_index_SHA256": sha(ROOT / INDEX),
        "before_Chinese_index_SHA256": sha(ROOT / CHINESE),
        "source_edition_duration_conflict_days_years": True,
        "new_historical_transit_source_notes_if_admitted": 25,
        "human_prediction_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    }
    (B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    package()
