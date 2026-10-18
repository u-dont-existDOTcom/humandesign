#!/usr/bin/env python3
"""Portable photographic first-edition four-sign audit ZIP with 148-test replay."""

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
REL = TASK + "/batches/B07z/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
NAME = "Astrology-Lilly-1647-Four-Full-Annual-Rate-Columns-B07z-20261018.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


source = j(B / "FULL_COLUMNS_ARIES_TAURUS_GEMINI_CANCER_1647_V1.json")
overlay = j(B / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json")
assert source["four_sign_source_rows"] == 124
assert overlay["new_full_column_photo_positions"] == 124
assert overlay["one_reader_photo_read_positions_cumulative_B07y_B07z"] == 146
assert overlay["unresolved_original_photo_glyph_positions_cumulative"] == 2
assert overlay["not_yet_first_edition_photo_read_positions_cumulative"] == 224
assert overlay["source_1647_values_differing_from_derivative_in_new_column"] == 1
assert j(ROOT / INDEX)["records_count"] == 12472
assert j(ROOT / CHINESE)["sum_source_annotations"] == 142

names = [
    "FULL_COLUMNS_ARIES_TAURUS_GEMINI_CANCER_1647_V1.json",
    "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261018.md",
    "build_b07z_four_sign_source_overlay.py",
    "test_b07z_four_signs.py",
    "build_b07z_photo_release.py",
] + [
    "evidence/contrast_crops/" + n + "_" + part + ".png"
    for n, parts in (
        ("Aries", ("first_half", "second_half")),
        ("Taurus", ("first_half", "second_half")),
        ("Gemini_correct", ("first", "second")),
        ("Cancer", ("first_half", "second_half")),
    )
    for part in parts
]
files = {REL + name: B / name for name in names}
files[TASK + "/batches/B07x/ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"] = (
    B.parent / "B07x" / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"
)
files[TASK + "/batches/B07y/ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json"] = (
    B.parent / "B07y" / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json"
)
files[TASK + "/batches/B07y/PHOTO_ADJUDICATION_1647_V1.json"] = (
    B.parent / "B07y" / "PHOTO_ADJUDICATION_1647_V1.json"
)
files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"] = (
    B.parent / "B07y" / "evidence/original_1647_annual_measure_pdf745_3500.jpg"
)
files[INDEX] = ROOT / INDEX
files[CHINESE] = ROOT / CHINESE
assert all(p.is_file() for p in files.values()), [
    name for name, p in files.items() if not p.is_file()
]
assert (
    sha(files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"])
    == source["original_source_photo_sha256"]
)

manifest = {
    "batch": "B07z",
    "status": "FIRST_EDITION_PHOTOGRAPHIC_SINGLE_READER_COLLATON_NOT_PREDICTION",
    "original_full_pdf_sha256": source["source_pdf_full_sha256"],
    "original_page_render_sha256": source["original_source_photo_sha256"],
    "new_complete_original_signs": source["source_signs"],
    "complete_source_degrees_per_sign": 31,
    "new_source_photo_rows": 124,
    "new_derivative_discrepancies": 1,
    "source_photo_legible_cumulative": 146,
    "original_glyphs_unresolved_cumulative": 2,
    "source_locations_unread_cumulative": 224,
    "historical_source_total_positions": 372,
    "Western_Lilly_accepted_stays": 12472,
    "Chinese_V3_stays": 142,
    "medical_legal_death_personality_or_other_real_human_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "full_original_pdf_not_embedded": True,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(exist_ok=True, parents=True)
archive = folder / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, path in files.items():
        z.write(path, "B07z-root/" + name)
    z.writestr(
        "B07z-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    restored = Path(tmp) / "B07z-root"
    assert j(restored / "RELEASE_MANIFEST.json") == manifest
    for name, record in manifest["members"].items():
        file = restored / name
        assert file.stat().st_size == record["bytes"]
        assert sha(file) == record["sha256"]
    cmd = [
        "python3",
        "-m",
        "unittest",
        "discover",
        "-s",
        str(restored / REL),
        "-p",
        "test_b07z_four_signs.py",
        "-q",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    result = re.search(r"Ran (\d+) tests", proc.stderr)
    assert result and int(result.group(1)) == 148, proc.stderr
    assert "skipped" not in proc.stderr
receipt = {
    "batch": "B07z",
    "status": "FIRST_EDITION_124_NEW_PHOTO_ROWS_148_ARCHIVE_REPLAY_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "all_sha256_and_byte_lengths_passed": True,
    "independently_extracted": True,
    "replayed_original_source_tests": 148,
    "original_first_edition_photo_sha256": source["original_source_photo_sha256"],
    "source_rows_sha256": sha(B / "FULL_COLUMNS_ARIES_TAURUS_GEMINI_CANCER_1647_V1.json"),
    "derived_372_overlay_sha256": sha(B / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json"),
    "Lilly_index_retained_sha256": sha(ROOT / INDEX),
    "Chinese_V3_retained_sha256": sha(ROOT / CHINESE),
    "human_predictive_accuracy_validations": 0,
    "runtime_promotions": 0,
    "new_canonical_Lilly_records": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
