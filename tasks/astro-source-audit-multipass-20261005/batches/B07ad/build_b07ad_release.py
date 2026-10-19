#!/usr/bin/env python3
"""Final sign-column first-edition annual source photo portable evidence ZIP."""

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
REL = TASK + "/batches/B07ad/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
NAME = "Astrology-Lilly-1647-Full-372-Annual-Rate-Photo-Inventory-B07ad-20261019.zip"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


a = read(B / "PHOTO_SOURCE_AQUARIUS_PISCES_1647_V1.json")
o = read(B / "ANNUAL_RATE_PHOTO_OVERLAY_V6.json")
assert o["original_table_total_positions"] == 372
assert o["cumulative_one_reader_legible_original_1647"] == 365
assert o["cumulative_original_print_unresolved_positions"] == 7
assert o["cumulative_positions_without_any_original_photo_attempt"] == 0
assert a["additionally_legible_original_photo"] == 45
assert a["additional_ambiguous_print_glyphs"] == 2
assert not o["source_critical_second_reader_verified_for_all_positions"]
assert not o["modern_ephemeris_and_birth_datetime_parity_validated"]
assert read(ROOT / INDEX)["records_count"] == 12472
assert read(ROOT / CHINA)["sum_source_annotations"] == 142

files = {
    REL + f.name: f
    for f in B.glob("*")
    if f.is_file()
    and (f.suffix in (".py", ".json", ".md") and not f.name.startswith("SOURCE_RELEASE_RECEIPT"))
}
files.update({REL + str(f.relative_to(B)): f for f in (B / "evidence").glob("*.png")})
files[TASK + "/batches/B07ac/ANNUAL_RATE_PHOTO_OVERLAY_V5.json"] = (
    B.parent / "B07ac/ANNUAL_RATE_PHOTO_OVERLAY_V5.json"
)
files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"] = (
    B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
)
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(f.is_file() for f in files.values())
assert (
    sha(files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"])
    == (a["original_first_edition_table_photo_sha256"])
)
manifest = {
    "batch": "B07ad",
    "status": "ALL_372_POSITIONS_ORIGINAL_PHOTO_ATTEMPTED_ONE_READER_ONLY",
    "original_source_full_pdf_sha256": a["original_full_1647_scan_sha256"],
    "first_edition_original_pdf745_photo_sha256": a["original_first_edition_table_photo_sha256"],
    "twelve_signs_original_rate_cell_positions": 372,
    "legible_one_reader_original_source_values": 365,
    "ambiguous_original_source_glyphs": 7,
    "positions_unread": 0,
    "historical_source_photo_review_not_calculation_truth": True,
    "true_independent_editorial_second_reader_done": False,
    "original_CLXVI_numerical_chapter_accepted": False,
    "canonical_Western_Lilly_accepted_unchanged": 12472,
    "Chinese_V3_accepted_unchanged": 142,
    "human_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "source_original_complete_pdf_not_embedded": True,
    "members": {
        name: {"sha256": sha(path), "bytes": path.stat().st_size} for name, path in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, f in files.items():
        z.write(f, "B07ad-root/" + name)
    z.writestr(
        "B07ad-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )

with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    dest = Path(td) / "B07ad-root"
    assert read(dest / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["members"].items():
        f = dest / name
        assert sha(f) == meta["sha256"]
        assert f.stat().st_size == meta["bytes"]
    p = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(dest / REL),
            "-p",
            "test_b07ad_all_372.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert p.returncode == 0, p.stdout + "\n" + p.stderr
    m = re.search(r"Ran (\d+) tests", p.stderr)
    assert m and int(m.group(1)) == 79, p.stderr
    assert "skipped" not in p.stderr
receipt = {
    "batch": "B07ad",
    "status": "1647_ALL_372_PHOTO_POSITIONS_ATTEMPTED_79_ARCHIVE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "CRC_passed": True,
    "member_sha256_and_exact_size_passed": True,
    "independent_extraction_replayed_tests": 79,
    "source_sha256": sha(B / "PHOTO_SOURCE_AQUARIUS_PISCES_1647_V1.json"),
    "final_source_inventory_SHA256": sha(B / "ANNUAL_RATE_PHOTO_OVERLAY_V6.json"),
    "previous_1647_source_inventory_SHA256": sha(
        B.parent / "B07ac/ANNUAL_RATE_PHOTO_OVERLAY_V5.json"
    ),
    "Western_Lilly_history_count_unchanged": 12472,
    "Chinese_V3_history_count_unchanged": 142,
    "full_critical_edition_editorial_collation_completed": False,
    "annual_time_direction_engine_verified": False,
    "human_predictive_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261019.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
