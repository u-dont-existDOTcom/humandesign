#!/usr/bin/env python3
"""Hermetic Merchant Nativity original-source archive: 47 tests after extraction.

Capture two physical editions' page images, SHA/byte witnesses, historical
source annotations and arithmetic discrepancies; keep full original 1647
894-page PDF referenced by hash but not embedded. Never claim actual
human-event predictive replication.
"""

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
REL = TASK + "/batches/B07ax/"
WEST = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAME = "Astrology-Lilly-1647-1659-Merchant-Nativity-30-Sources-B07ax-20261019.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    result = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    directory = (
        Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
    )
    if (
        directory is not None
        and directory.is_dir()
        and directory.resolve() != Path.home().resolve()
    ):
        return directory
    french = Path.home() / "Téléchargements"
    return french if french.is_dir() else Path.home()


photos = j(B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json")
math = j(B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json")
notes = j(B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json")
rules = j(B / "RULES.json")
accept = j(B / "ACCEPTANCE.json")
old = j(ROOT / WEST)
chinese = j(ROOT / CHINA)
assert old["records_count"] == accept["prior_Lilly"] == 12870
assert old["batches"][-1]["id"] == "B07aw"
assert chinese["sum_source_annotations"] == 355
assert len(photos["original_source_photographic_witnesses"]) == 10
assert len(notes["source_records"]) == len(rules["rules"]) == 30
assert rules["first_record"] == "R12871" and rules["last_record"] == "R12900"
assert accept["next_historical_R"] == "R12901"
assert math["original_minus_formula_arcminutes"] == -20
assert math["actual_person_outcomes_predicted_and_verified"] == 0
assert notes["source_human_outcomes_validated"] == 0
assert rules["independent_actual_person_outcome_validations"] == 0
assert accept["rules_SHA256"] == sha(B / "RULES.json")
assert accept["source_notes_SHA256"] == sha(
    B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json"
)

files = {}
names = [
    "MERCHANT_NATIVITY_SOURCE_CANDIDATES_V1.json",
    "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json",
    "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json",
    "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json",
    "RULES.json",
    "ACCEPTANCE.json",
    "RECOVERY_CHECKPOINT_20261019_LATEST.md",
    "ORIGINAL_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261019.md",
    "FOCUSED_TEST_RECEIPT_PROVISIONAL_20261019.json",
    "build_b07ax_source_rules.py",
    "test_b07ax_merchant_source.py",
    "build_b07ax_release.py",
    "prepare_b07ax_canonical.py",
]
for name in names:
    files[REL + name] = B / name

for original in photos["original_source_photographic_witnesses"].values():
    path = original["file"]
    file = ROOT / path
    assert file.is_file(), path
    assert sha(file) == original["sha256"], path
    assert file.stat().st_size == original["bytes"], path
    files[path] = file

files[WEST] = ROOT / WEST
files[CHINA] = ROOT / CHINA
files[TASK + "/batches/B07aw/RULES.json"] = B.parent / "B07aw/RULES.json"
assert all(file.is_file() for file in files.values()), [
    name for name, file in files.items() if not file.is_file()
]
manifest = {
    "batch": "B07ax",
    "source": (
        "William Lilly Christian Astrology original first printed 1647 "
        "and independently typeset original second printed 1659, "
        "CLXXV English Merchant Nativity folios742–745"
    ),
    "source_1647_original_full_Wellcome_pdf_sha256": (
        photos["original_1647_Wellcome_full_scan_sha256"]
    ),
    "original_full_1647_pdf_embedded": False,
    "original_two_edition_source_photo_count": 10,
    "first_printed_historical_birthday_text": (
        photos["original_1647_chart_center_source_folio742"]
    ),
    "original_humor_count": (
        photos["temperament_source_table_and_author_qualifications"][
            "literal_first_edition_1647_folio743_counts"
        ]
    ),
    "first_and_second_print_Mercury_antiscion": ["Pisces", 26, 6],
    "analytic_expected_Mercury_reflection": ["Pisces", 26, 26],
    "historical_1647_print_arithmetic_discrepancy_minutes": -20,
    "source_merchant_known_to_historical_author_unblinded": True,
    "proposed_historical_source_notes": 30,
    "canonical_prior_Lilly_source_count": 12870,
    "if_accepted_Lilly_source_count": 12900,
    "parallel_Chinese_V7_source_count": 355,
    "proposed_next_source_R": "R12901",
    "next_original_printed_heading": "CLXXVI Of the Manners of the Native",
    "independent_natal_era_ephemeris_engine_verified": False,
    "independent_human_predictive_event_tests_completed": 0,
    "runtime_astrological_model_promotions": 0,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}

folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
temporary = folder / (NAME + ".building")
assert not temporary.exists(), temporary
with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as out:
    for name, file in files.items():
        out.write(file, "B07ax-root/" + name)
    out.writestr(
        "B07ax-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )

with zipfile.ZipFile(temporary) as source_archive, tempfile.TemporaryDirectory() as td:
    assert source_archive.testzip() is None
    source_archive.extractall(td)
    restored = Path(td) / "B07ax-root"
    assert j(restored / "RELEASE_MANIFEST.json") == manifest
    for name, record in manifest["members"].items():
        recovered = restored / name
        assert recovered.stat().st_size == record["bytes"], name
        assert sha(recovered) == record["sha256"], name
    replay = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(restored / REL),
            "-p",
            "test_b07ax_merchant_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert replay.returncode == 0, replay.stdout + "\n" + replay.stderr
    count = re.search(r"Ran (\d+) tests", replay.stderr)
    assert count and int(count.group(1)) == 47, replay.stderr
    assert "skipped" not in replay.stderr
os.replace(temporary, archive)

receipt = {
    "batch": "B07ax",
    "status": "1647_1659_MERCHANT_NATIVITY_30_SOURCE_47_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_members": len(files),
    "CRC_passed": True,
    "member_SHA256_and_exact_bytes_passed": True,
    "independent_ZIP_extraction_test_replay_passed": True,
    "source_tests_replayed": 47,
    "source_notes_SHA256": sha(B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json"),
    "rules_SHA256": sha(B / "RULES.json"),
    "mercury_diagnostic_SHA256": sha(
        B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json"
    ),
    "old_Lilly_index_SHA256": sha(ROOT / WEST),
    "Chinese_V7_index_SHA256": sha(ROOT / CHINA),
    "new_canonical_original_historical_annotations_if_admitted": 30,
    "source_known_person_not_independent_blind_case": True,
    "real_person_event_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
