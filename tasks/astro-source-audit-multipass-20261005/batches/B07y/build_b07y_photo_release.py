#!/usr/bin/env python3
"""Portable limited first-edition photo correction archive; 28-test independent replay."""

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
REL = TASK + "/batches/B07y/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
FILENAME = "Astrology-Lilly-1647-Annual-Rate-Photographic-Corrections-B07y-20261018.zip"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


review = j(B / "PHOTO_ADJUDICATION_1647_V1.json")
overlay = j(B / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json")
western = j(ROOT / INDEX)
china = j(ROOT / CHINA)
assert overlay["total_annual_sign_degree_positions"] == 372
assert overlay["B07y_current_manually_reviewed_positions"] == 24
assert overlay["B07y_confirmed_1647_one_reader_positions"] == 22
assert overlay["B07y_ambiguous_glyph_positions"] == 2
assert overlay["B07y_conflicts_with_derivative_candidates"] == 5
assert overlay["B07y_positions_not_directly_read_in_this_batch"] == 348
assert western["records_count"] == 12472
assert china["sum_source_annotations"] == 142
assert overlay["runtime_promotions"] == 0
assert overlay["actual_human_predictions_validated"] == 0
assert (
    sha(B / review["original_source"]["archived_3500_image"])
    == (review["original_source"]["source_3500_sha256"])
)
assert (
    sha(B / review["comparator_source"]["photo_file"])
    == (review["comparator_source"]["photo_sha256"])
)
assert (
    sha(B.parent / "B07x" / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json")
    == (overlay["inherited_previous_derivative_candidate_sha256"])
)

names = [
    "PHOTO_ADJUDICATION_1647_V1.json",
    "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json",
    "ORIGINAL_1647_ANNUAL_RATE_PHOTO_REVIEW_20261018.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261018.md",
    "build_photo_overlay_b07y.py",
    "test_b07y_photo_overlay.py",
    "build_b07y_photo_release.py",
    "evidence/original_1647_annual_measure_pdf745_3500.jpg",
    "evidence/1659_annual_measure_table_page740.jpg",
]
files = {REL + name: B / name for name in names}
files[TASK + "/batches/B07x/ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"] = (
    B.parent / "B07x" / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"
)
files[TASK + "/batches/B07x/ORIGINAL_SOURCE_WINDOW_V1.json"] = (
    B.parent / "B07x" / "ORIGINAL_SOURCE_WINDOW_V1.json"
)
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values())

manifest = {
    "batch": "B07y",
    "purpose": "1647 original printed annual-rate cell photo adjudication",
    "source_original_pdf_sha256": review["original_source"]["original_894_frame_pdf_sha256"],
    "page_original_1647_photo_sha256": review["original_source"]["source_3500_sha256"],
    "later_1659_typeset_print_photo_sha256": review["comparator_source"]["photo_sha256"],
    "historical_source_only": True,
    "inherited_derivative_372_cells_preserved": True,
    "current_manual_photo_positions": 24,
    "clear_original_one_reader": 22,
    "ambiguous_original_photo_glyphs": 2,
    "corrections_against_derivative": 5,
    "positions_not_photo_reviewed_in_new_pass": 348,
    "Western_Lilly_historic_source_count_unchanged": 12472,
    "Chinese_V3_historic_source_count_unchanged": 142,
    "printed_CLXVI_numerical_source_accepted": False,
    "independent_human_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "original_1647_full_pdf_not_embedded": True,
    "members": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / FILENAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
    for name, file in files.items():
        zipped.write(file, "B07y-root/" + name)
    zipped.writestr(
        "B07y-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as zipped, tempfile.TemporaryDirectory() as tmp:
    assert zipped.testzip() is None
    zipped.extractall(tmp)
    root = Path(tmp) / "B07y-root"
    assert j(root / "RELEASE_MANIFEST.json") == manifest
    for name, info in manifest["members"].items():
        file = root / name
        assert sha(file) == info["sha256"]
        assert file.stat().st_size == info["bytes"]
    cmd = [
        "python3",
        "-m",
        "unittest",
        "discover",
        "-s",
        str(root / REL),
        "-p",
        "test_b07y_photo_overlay.py",
        "-q",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=75)
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    m = re.search(r"Ran (\d+) tests", proc.stderr)
    assert m and int(m.group(1)) == 28, proc.stderr
    assert "skipped" not in proc.stderr
receipt = {
    "batch": "B07y",
    "status": "LIMITED_ORIGINAL_1647_PHOTO_SOURCE_28_ARCHIVE_TESTS_PASS",
    "filename": FILENAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "member_count": len(files),
    "crc_passed": True,
    "member_hashes_and_sizes_passed": True,
    "standalone_extract_test_replay_passed": True,
    "replayed_tests": 28,
    "source_photo_1647_sha256": review["original_source"]["source_3500_sha256"],
    "second_edition_1659_photo_sha256": review["comparator_source"]["photo_sha256"],
    "new_photo_overlay_sha256": sha(B / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json"),
    "Western_index_sha256_unchanged": sha(ROOT / INDEX),
    "Chinese_V3_sha256_unchanged": sha(ROOT / CHINA),
    "new_canonical_Lilly_history_records": 0,
    "all_original_direction_rate_cells_verified": False,
    "independent_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(receipt, indent=2))
