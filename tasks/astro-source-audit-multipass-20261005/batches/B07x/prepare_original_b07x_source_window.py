#!/usr/bin/env python3
"""Witness source-original printed CLXVI TIME MEASURE and repeated printed numeral."""

import hashlib
import json
import os
import shutil
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07w"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
SOURCE = Path(os.environ["LILLY_1647_SOURCE_PDF"])
RENDER_1600 = Path(os.environ["LILLY_1647_1600_RENDER_DIR"])
RENDER_1800 = Path(os.environ["LILLY_1647_1800_RENDER_DIR"])


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


assert not (B / "ORIGINAL_SOURCE_WINDOW_V1.json").exists()
before = j(INDEX)
parent = j(PARENT / "ORIGINAL_SOURCE_WINDOW_V1.json")
assert before["records_count"] == 12472
assert before["batches"][-1]["id"] == "B07w"
assert before["next"]["chapter"] == "CLXVI"
assert before["next"]["pdf_page"] == 742
assert parent["following_heading_pdf"] == 742
assert j(CHINA)["sum_source_annotations"] == 97
assert SOURCE.stat().st_size == 141842963
assert sha(SOURCE) == before["source_sha256"] == parent["full_pdf_original_sha256"]
(B / "evidence").mkdir(exist_ok=True)
photos = {}
for n in range(742, 751):
    if n in (742, 743):
        image = PARENT / "evidence" / f"pdf_1647-{n}.jpg"
        prior = parent["photos"][str(n)]
        assert sha(image) == prior["sha256"] and image.stat().st_size == prior["bytes"]
        origin = "EXACT_PREVIOUS_B07w_ORIGINAL_PDF_RASTER"
    elif n == 744:
        image = RENDER_1600 / "page-744.jpg"
        origin = "ORIGINAL_SOURCE_PDF_POPPLER_JPEG_1600_Q93"
    else:
        image = RENDER_1800 / f"page-{n}.jpg"
        origin = "ORIGINAL_SOURCE_PDF_POPPLER_JPEG_1800_Q93"
    assert image.is_file()
    dest = B / "evidence" / f"pdf_1647-{n}.jpg"
    if not dest.exists():
        shutil.copyfile(image, dest)
    assert dest.read_bytes() == image.read_bytes()
    photos[str(n)] = {
        "file": str(dest.relative_to(B)),
        "original_pdf_frame": n,
        "printed_page": n - 34,
        "bytes": dest.stat().st_size,
        "sha256": sha(dest),
        "raster_method": origin,
        "scope": (
            "CLXVI_TIME_MEASURE_AFTER_CLXV_DIVIDER"
            if n == 742
            else "CLXVI_TIME_MEASURE_BEFORE_REPEAT_CLXVI_HEADING"
            if n == 749
            else "NEXT_SEPARATE_PRINTED_CLXVI_ANNUAL_PROFECTION_CONTEXT"
            if n == 750
            else "CLXVI_NUMERICAL_METHOD_BODY"
        ),
    }
window = {
    "schema": "LILLY_1647_PRINTED_TIME_MEASURE_CHAPTER_WINDOW_V1",
    "batch": "B07x",
    "source": "William Lilly Christian Astrology original first edition 1647 Wellcome b30338724",
    "full_source_pdf_sha256": sha(SOURCE),
    "source_pdf_frames_total": 894,
    "accepted_lilly_before": 12472,
    "ptolemy_records_unchanged": 1066,
    "Chinese_v2_records_unchanged": 97,
    "source_index_parent_sha256": sha(INDEX),
    "next_historical_record": "R12473",
    "printed_numbered_heading": "CHAP CLXVI Of the measure of time in DIRECTIONS",
    "printed_heading_numeral": "CLXVI",
    "starts_pdf": 742,
    "starts_printed_folio": 708,
    "body_original_pdf_frames": list(range(742, 750)),
    "ends_pdf": 749,
    "ends_printed_folio": 715,
    "following_heading_printed_numeral": "CLXVI",
    "following_heading_text": (
        "Of annual Profections, and by what meanes to find out "
        "the Profectionall Signe of every yeer"
    ),
    "following_heading_starts_pdf": 749,
    "following_heading_starts_printed": 715,
    "following_heading_is_duplicate_printed_numeral": True,
    "following_distinct_next_numbered_heading": (
        "CHAP CLXVII Of the Use of Profections and their Effects"
    ),
    "following_CLXVII_starts_pdf": 752,
    "note": (
        "FIRST EDITION REPEATS THE PRINTED NUMERAL CHAP CLXVI: "
        "the current directions-time chapter ends above divider PDF749, "
        "then annual Profections opens below a second CHAP CLXVI; "
        "distinct CHAP CLXVII begins lower PDF752. "
        "Never silently renumber headings or merge the two CLXVI sources."
    ),
    "original_arctoage_and_ephemeris_computations_fully_verified": False,
    "human_event_timing_predictive_accuracy_verified": False,
    "original_full_annual_measure_table_collated": False,
    "source_only": True,
    "photos": photos,
}
(B / "ORIGINAL_SOURCE_WINDOW_V1.json").write_text(
    json.dumps(window, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("Time-measure original source window: PDF742–749; next duplicate printed CLXVI on PDF749")
