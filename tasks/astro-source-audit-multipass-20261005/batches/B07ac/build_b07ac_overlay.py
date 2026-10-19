#!/usr/bin/env python3
"""Source-first Sagittarius/Capricorn annual-motion 1647, append-only V5."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parent / "B07ab"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


a = j(B / "PHOTO_SOURCE_SAGITTARIUS_CAPRICORN_V1.json")
p = j(P / "ANNUAL_RATE_PHOTO_OVERLAY_V4.json")
assert j(WEST)["records_count"] == 12472
assert j(CHINA)["sum_source_annotations"] == 142
assert p["cumulative_one_reader_original_photo_legible"] == 263
assert p["cumulative_original_glyphs_unresolved"] == 4
assert p["not_read_original_table_remaining"] == 105
assert a["source_positions"] == 62
assert a["old_B07y_Capricorn_overlap"] == 4
assert a["new_1647_photo_legible_positions"] == 57
assert a["new_photo_unresolved_positions"] == 1
assert (
    sha(B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg")
    == (a["original_1647_image_pdf745_sha256"])
)
old = {(r["sign"], r["degree"]): r for r in p["rows"]}
new = {(r["sign"], r["degree"]): r for r in a["records"]}
assert len(old) == 372 and len(new) == 62
assert set(key for key, r in new.items() if r["previous_source_photo_review"]) == {
    ("Capricorn", 12),
    ("Capricorn", 13),
    ("Capricorn", 14),
    ("Capricorn", 15),
}
assert all(
    old[key]["source_read_batch"] == "B07y"
    for key, r in new.items()
    if r["previous_source_photo_review"]
)
assert all(
    old[key]["source_read_batch"] is None
    for key, r in new.items()
    if not r["previous_source_photo_review"]
)
assert len(list((B / "evidence").glob("*_half.png"))) == 4

rows = []
diff = []
for prev in p["rows"]:
    key = (prev["sign"], prev["degree"])
    src = new.get(key)
    result = dict(prev)
    if src:
        curr = src["first_edition_1647_printed_rate"]
        choices = src["unresolved_print_glyph_alternatives"]
        if src["previous_source_photo_review"]:
            assert prev["first_edition_1647_one_reader_photo_rate"] == curr
            assert prev["unresolved_original_source_glyph_options"] == choices
        else:
            assert prev["first_edition_1647_one_reader_photo_rate"] is None
            assert not prev["unresolved_original_source_glyph_options"]
            result["source_read_batch"] = "B07ac"
            result["first_edition_1647_one_reader_photo_rate"] = curr
            result["unresolved_original_source_glyph_options"] = choices
            result["first_edition_source_photo_verified_by_one_reader"] = curr is not None
            if curr is not None and curr != prev["frozen_B07x_derivative_candidate"]:
                diff.append(
                    {
                        "sign": key[0],
                        "degree": key[1],
                        "printed_1647": curr,
                        "derivative_originally_frozen": prev["frozen_B07x_derivative_candidate"],
                        "source_proof": "ONE_READER_UNBLINDED_ORIGINAL_PHOTO_PDF745",
                    }
                )
    assert not result["runtime_promoted"]
    rows.append(result)
assert diff == [
    {
        "sign": "Sagittarius",
        "degree": 6,
        "printed_1647": [64, 37],
        "derivative_originally_frozen": [64, 27],
        "source_proof": "ONE_READER_UNBLINDED_ORIGINAL_PHOTO_PDF745",
    },
    {
        "sign": "Sagittarius",
        "degree": 22,
        "printed_1647": [66, 30],
        "derivative_originally_frozen": [66, 31],
        "source_proof": "ONE_READER_UNBLINDED_ORIGINAL_PHOTO_PDF745",
    },
]
assert len(rows) == 372
assert sum(r["first_edition_1647_one_reader_photo_rate"] is not None for r in rows) == 320
assert sum(bool(r["unresolved_original_source_glyph_options"]) for r in rows) == 5
assert (
    sum(
        r["first_edition_1647_one_reader_photo_rate"] is None
        and not r["unresolved_original_source_glyph_options"]
        for r in rows
    )
    == 47
)
data = {
    "schema": "LILLY_1647_ANNUAL_RATE_PHOTO_APPEND_B07ac_V5",
    "batch": "B07ac",
    "original_photo_pdf745_sha256": a["original_1647_image_pdf745_sha256"],
    "original_full_1647_source_pdf_sha256": a["full_1647_pdf_sha256"],
    "preserved_parent_B07ab_overlay_sha256": sha(P / "ANNUAL_RATE_PHOTO_OVERLAY_V4.json"),
    "added_original_sagittarius_capricorn_source_sha256": sha(
        B / "PHOTO_SOURCE_SAGITTARIUS_CAPRICORN_V1.json"
    ),
    "historical_original_rate_cells": 372,
    "B07ac_new_one_reader_legible": 57,
    "B07ac_new_ambiguous_source_glyphs": 1,
    "B07ac_old_Capricorn_B07y_overlaps": 4,
    "B07ac_printed_vs_derivative": diff,
    "cumulative_one_reader_legible_original": 320,
    "cumulative_original_source_glyph_ambiguities": 5,
    "cumulative_positions_original_unread": 47,
    "all_original_source_rate_cells_collated": False,
    "independent_second_source_reader_review_complete": False,
    "historical_angular_year_math_or_natal_engine_verified": False,
    "Lilly_accepted_canonical_source_registry_unchanged": 12472,
    "Chinese_V3_registry_unchanged": 142,
    "real_people_predictive_validations": 0,
    "runtime_model_promotions": 0,
    "rows": rows,
}
file = B / "ANNUAL_RATE_PHOTO_OVERLAY_V5.json"
file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "new_source_legible": 57,
            "new_source_ambiguous": 1,
            "cumulative_legible": 320,
            "cumulative_ambiguous": 5,
            "unexamined": 47,
            "new_derivative_differences": diff,
            "overlay_sha256": sha(file),
        },
        indent=2,
    )
)
