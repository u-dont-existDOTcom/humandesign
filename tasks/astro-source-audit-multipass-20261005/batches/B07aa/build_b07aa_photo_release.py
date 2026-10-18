#!/usr/bin/env python3
"""Portable one-reader 1647 Leo/Virgo photographic source ZIP and 79-test replay."""

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
REL = TASK + "/batches/B07aa/"
INDEX = TASK + "/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
NAME = "Astrology-Lilly-1647-Annual-Rate-Leo-Virgo-Photo-Source-B07aa-20261018.zip"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def downloads():
    p = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True)
    return Path(
        p.stdout.strip()
        if p.returncode == 0 and p.stdout.strip()
        else str(Path.home() / "Téléchargements")
    )


source = j(B / "PHOTO_SOURCE_COLUMNS_LEO_VIRGO_1647_V1.json")
overlay = j(B / "ANNUAL_RATE_PHOTO_OVERLAY_V3.json")
assert len(source["entries"]) == 62
assert overlay["B07aa_new_legible_one_reader_positions"] == 59
assert overlay["B07aa_new_ambiguous_glyphs"] == 2
assert overlay["B07aa_prior_B07y_reused_source_positions_not_recounted"] == 1
assert overlay["cumulative_photo_one_reader_legible"] == 205
assert overlay["cumulative_photo_glyphs_unresolved"] == 4
assert overlay["cumulative_unexamined_original_positions"] == 163
assert len(overlay["B07aa_new_derivative_conflicts"]) == 1
assert j(ROOT / INDEX)["records_count"] == 12472
assert j(ROOT / CHINA)["sum_source_annotations"] == 142
assert (
    overlay["runtime_model_promotions"]
    == overlay["real_people_independent_predictions_validated"]
    == 0
)

names = [
    "PHOTO_SOURCE_COLUMNS_LEO_VIRGO_1647_V1.json",
    "ANNUAL_RATE_PHOTO_OVERLAY_V3.json",
    "ORIGINAL_SOURCE_REVIEW_20261018.md",
    "CONTINUATION_HANDOFF_PROVISIONAL_20261018.md",
    "build_b07aa_source_overlay.py",
    "test_b07aa_photo_source.py",
    "build_b07aa_photo_release.py",
] + [
    "evidence/" + f
    for f in (
        "Leo_first_half.png",
        "Leo_second_half.png",
        "Virgo_first_half.png",
        "Virgo_second_half.png",
        "virgo_rows0_5.png",
        "virgo_rows15_22.png",
        "virgo_rows18_25.png",
        "leo_rows0_6.png",
    )
]
files = {REL + name: B / name for name in names}
files[TASK + "/batches/B07z/ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json"] = (
    B.parent / "B07z/ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json"
)
files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"] = (
    B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
)
files[INDEX] = ROOT / INDEX
files[CHINA] = ROOT / CHINA
assert all(file.is_file() for file in files.values())
assert (
    sha(files[TASK + "/batches/B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"])
    == (source["original_photo_sha256"])
)

manifest = {
    "batch": "B07aa",
    "source": "William Lilly Christian Astrology first-edition 1647 original Wellcome b30338724",
    "original_full_pdf_sha256": source["source_original_894frame_pdf_sha256"],
    "original_pdf745_photo_sha256": source["original_photo_sha256"],
    "source_specific_signs": ["Leo", "Virgo"],
    "one_reader_positions_examined_this_batch": 62,
    "old_position_previously_counted_and_preserved": 1,
    "new_one_reader_legible_source_positions": 59,
    "new_one_reader_glyph_uncertainties": 2,
    "new_derivative_disagreements": 1,
    "cumulative_one_reader_legible_photo_positions": 205,
    "cumulative_glyph_uncertainties": 4,
    "not_original_photo_read_yet": 163,
    "annual_source_positions_total": 372,
    "historic_western_Lilly_index_stays": 12472,
    "historic_chinese_V3_index_stays": 142,
    "all_original_1647_rate_cells_photo_verified": False,
    "astrological_engine_date_math_parity_verified": False,
    "human_prediction_validations": 0,
    "runtime_promotions": 0,
    "member_records": {
        name: {"sha256": sha(file), "bytes": file.stat().st_size} for name, file in files.items()
    },
}
folder = downloads()
folder.mkdir(parents=True, exist_ok=True)
archive = folder / NAME
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, file in files.items():
        z.write(file, "B07aa-root/" + name)
    z.writestr(
        "B07aa-root/RELEASE_MANIFEST.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    dest = Path(td) / "B07aa-root"
    assert j(dest / "RELEASE_MANIFEST.json") == manifest
    for name, meta in manifest["member_records"].items():
        file = dest / name
        assert sha(file) == meta["sha256"]
        assert file.stat().st_size == meta["bytes"]
    proc = subprocess.run(
        [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(dest / REL),
            "-p",
            "test_b07aa_photo_source.py",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=80,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    m = re.search(r"Ran (\d+) tests", proc.stderr)
    assert m and int(m.group(1)) == 79, proc.stderr
    assert "skipped" not in proc.stderr

receipt = {
    "batch": "B07aa",
    "status": "ORIGINAL_1647_LEO_VIRGO_SOURCE_ONLY_79_PORTABLE_TESTS_PASS",
    "filename": NAME,
    "archive_sha256": sha(archive),
    "archive_bytes": archive.stat().st_size,
    "archive_member_count": len(files),
    "crc_passed": True,
    "member_hashes_bytes_passed": True,
    "independent_archive_extract_replay": True,
    "focused_source_tests_replayed": 79,
    "parent_B07z_overlay_sha256": sha(B.parent / "B07z/ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json"),
    "new_one_reader_source_sha256": sha(B / "PHOTO_SOURCE_COLUMNS_LEO_VIRGO_1647_V1.json"),
    "new_372_overlay_sha256": sha(B / "ANNUAL_RATE_PHOTO_OVERLAY_V3.json"),
    "canonical_Western_index_sha256_unchanged": sha(ROOT / INDEX),
    "Chinese_V3_sha256_unchanged": sha(ROOT / CHINA),
    "new_historical_Lilly_notes_accepted": 0,
    "original_1647_source_table_full_photo_admission": False,
    "independent_human_outcome_predictions_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
(B / "SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261018.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
