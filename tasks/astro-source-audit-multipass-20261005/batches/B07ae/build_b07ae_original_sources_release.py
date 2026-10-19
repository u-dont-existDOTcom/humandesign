#!/usr/bin/env python3
"""Independently replay original-printed 1647/1659 Maginus source arithmetic ZIP."""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
REL = TASK + "/batches/B07ae/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
NAME = "Astrology-Lilly-Original-1647-1659-Maginus-Timing-Source-B07ae-20261019.zip"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


source = load(B / "MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json")
assert len(source["worked_cases"]) == 2
assert [x["computed_remaining_arcminutes"] for x in source["worked_cases"]] == [13, 4]
assert [x["source_printed_fraction_used_in_partial_year"] for x in source["worked_cases"]] == [
    42,
    48,
]
assert not source["original_method_a_natal_chart_era_engine_verified"]
assert source["independent_real_human_prediction_validations"] == source["runtime_promotions"] == 0
assert load(ROOT / INDEX)["records_count"] == 12472
assert load(ROOT / CHINA)["sum_source_annotations"] == 142
files = {
    REL + f.name: f
    for f in B.glob("*")
    if f.is_file()
    and f.suffix in (".json", ".md", ".py")
    and not f.name.startswith("SOURCE_RELEASE_RECEIPT")
}
for f in (B / "evidence").glob("*.jpg"):
    files[REL + "evidence/" + f.name] = f
files[TASK + "/batches/B07x/WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json"] = (
    B.parent / "B07x/WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json"
)
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(path.is_file() for path in files.values())
manifest = {
    "batch": "B07ae",
    "source": "William Lilly original 1647 and actual typeset 1659 second edition",
    "1647_full_original_pdf_sha256": source["Wellcome_1647_full_original_pdf_sha256"],
    "original_source_photo_hashes": {k: v["sha256"] for k, v in source["source_photos"].items()},
    "printed_Maginus_worked_cases": 2,
    "source_calculations_fractional_minutes": [42, 48],
    "correct_residuals_from_printed_targets": [13, 4],
    "independent_second_typeset_edition_present": True,
    "independent_second_human_reader_done": False,
    "source_arithmetic_exposed_as_historical_ambiguity": True,
    "Western_Lilly_historical_canonical_unchanged": 12472,
    "Chinese_V3_historical_canonical_unchanged": 142,
    "empirical_human_predictions_validated": 0,
    "runtime_astro_rules_promoted": 0,
    "full_original_1647_PDF_not_included": True,
    "members": {k: {"sha256": sha(v), "bytes": v.stat().st_size} for k, v in files.items()},
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipfile_out:
    for key, path in files.items():
        zipfile_out.write(path, "B07ae-root/" + key)
    zipfile_out.writestr(
        "B07ae-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    extraction = Path(td) / "B07ae-root"
    assert load(extraction / "RELEASE_MANIFEST.json") == manifest
    for path, expected in manifest["members"].items():
        f = extraction / path
        assert sha(f) == expected["sha256"]
        assert f.stat().st_size == expected["bytes"]
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(extraction / REL),
            "-p",
            "test_b07ae_maginus_editions.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=80,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    count = re.search(r"Ran (\d+) tests", proc.stderr)
    assert count and int(count.group(1)) == 26, proc.stderr
    assert "skipped" not in proc.stderr
receipt = {
    "batch": "B07ae",
    "status": "ORIGINAL_FIRST_SECOND_EDITION_SOURCE_MAGINUS_26_ARCHIVE_TESTS_PASS",
    "archive_filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "member_sha256_and_bytes_passed": True,
    "independent_zip_extraction_passed": True,
    "historical_arithmetic_tests_replayed": 26,
    "original_second_edition_photo_sha256s": {
        name: entry["sha256"] for name, entry in source["source_photos"].items()
    },
    "record_sha256": sha(B / "MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json"),
    "Lilly_historical_index_unchanged": 12472,
    "Chinese_V3_history_unchanged": 142,
    "new_canonically_accepted_lilly_record_count": 0,
    "independent_human_predicted_successes": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
