#!/usr/bin/env python3
"""Preserve cumulative original 1647 yearly-equatorial-rate source photo evidence."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parent / "B07ac"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


source = j(B / "PHOTO_SOURCE_AQUARIUS_PISCES_1647_V1.json")
before = j(P / "ANNUAL_RATE_PHOTO_OVERLAY_V5.json")
assert j(WEST)["records_count"] == 12472
assert j(CHINESE)["sum_source_annotations"] == 142
assert before["cumulative_one_reader_legible_original"] == 320
assert before["cumulative_original_source_glyph_ambiguities"] == 5
assert before["cumulative_positions_original_unread"] == 47
assert source["positions_inspected"] == 62
assert source["prior_reviewed_B07y_overlap"] == 15
assert source["additionally_legible_original_photo"] == 45
assert source["additional_ambiguous_print_glyphs"] == 2
assert (
    sha(B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg")
    == (source["original_first_edition_table_photo_sha256"])
)
before_by = {(r["sign"], r["degree"]): r for r in before["rows"]}
new = {(r["sign"], r["degree"]): r for r in source["records"]}
assert len(before_by) == 372 and len(new) == 62
assert all((s, i) in new for s in ("Aquarius", "Pisces") for i in range(31))
overlap = {k for k, r in new.items() if r["prior_B07y_original_photo_status"]}
assert overlap == {
    ("Aquarius", 0),
    ("Aquarius", 1),
    ("Aquarius", 2),
    ("Aquarius", 3),
    ("Aquarius", 4),
    ("Pisces", 0),
    ("Pisces", 4),
    ("Pisces", 5),
    ("Pisces", 6),
    ("Pisces", 7),
    ("Pisces", 21),
    ("Pisces", 22),
    ("Pisces", 23),
    ("Pisces", 24),
    ("Pisces", 25),
}
assert all(before_by[k]["source_read_batch"] == "B07y" for k in overlap)
assert all(before_by[k]["source_read_batch"] is None for k in new if k not in overlap)
assert len(list((B / "evidence").glob("*_half.png"))) == 4

rows = []
differences = []
for old in before["rows"]:
    k = (old["sign"], old["degree"])
    s = new.get(k)
    result = dict(old)
    if s:
        val = s["first_edition_1647_printed_rate"]
        opts = s["unresolved_source_photo_alternatives"]
        if k in overlap:
            assert old["first_edition_1647_one_reader_photo_rate"] == val
            assert old["unresolved_original_source_glyph_options"] == opts
        else:
            assert old["first_edition_1647_one_reader_photo_rate"] is None
            assert old["unresolved_original_source_glyph_options"] is None
            result["first_edition_1647_one_reader_photo_rate"] = val
            result["unresolved_original_source_glyph_options"] = opts
            result["source_read_batch"] = "B07ad"
            result["first_edition_source_photo_verified_by_one_reader"] = val is not None
            if val is not None and val != old["frozen_B07x_derivative_candidate"]:
                differences.append(
                    {
                        "sign": k[0],
                        "degree": k[1],
                        "original_1647_photo_reading": val,
                        "previous_derivative_searchable_text": old[
                            "frozen_B07x_derivative_candidate"
                        ],
                        "one_reader_source_not_critical_edition": True,
                    }
                )
    assert result["runtime_promoted"] is False
    rows.append(result)

assert differences == [
    {
        "sign": "Aquarius",
        "degree": 13,
        "original_1647_photo_reading": [60, 56],
        "previous_derivative_searchable_text": [60, 50],
        "one_reader_source_not_critical_edition": True,
    },
    {
        "sign": "Aquarius",
        "degree": 15,
        "original_1647_photo_reading": [60, 31],
        "previous_derivative_searchable_text": [60, 21],
        "one_reader_source_not_critical_edition": True,
    },
    {
        "sign": "Pisces",
        "degree": 30,
        "original_1647_photo_reading": [54, 26],
        "previous_derivative_searchable_text": [54, 16],
        "one_reader_source_not_critical_edition": True,
    },
]
assert len(rows) == 372
assert sum(r["first_edition_1647_one_reader_photo_rate"] is not None for r in rows) == 365
assert sum(bool(r["unresolved_original_source_glyph_options"]) for r in rows) == 7
assert all(
    r["first_edition_1647_one_reader_photo_rate"] is not None
    or r["unresolved_original_source_glyph_options"]
    for r in rows
)
assert sum(r["source_read_batch"] is None for r in rows) == 0

data = {
    "schema": "LILLY_1647_372_ALL_PHOTO_POSITIONS_ATTEMPTED_B07ad_V6",
    "batch": "B07ad",
    "historical_full_pdf_sha256": source["original_full_1647_scan_sha256"],
    "historical_original_pdf745_photo_sha256": source["original_first_edition_table_photo_sha256"],
    "parent_B07ac_overlay_sha256": sha(P / "ANNUAL_RATE_PHOTO_OVERLAY_V5.json"),
    "new_original_aquarius_pisces_source_sha256": sha(
        B / "PHOTO_SOURCE_AQUARIUS_PISCES_1647_V1.json"
    ),
    "original_table_total_positions": 372,
    "new_B07ad_one_reader_legible_original": 45,
    "new_B07ad_unresolved_original_glyphs": 2,
    "previous_original_B07y_overlap_not_counted": 15,
    "new_1647_print_vs_derivative_conflicts": differences,
    "cumulative_one_reader_legible_original_1647": 365,
    "cumulative_original_print_unresolved_positions": 7,
    "cumulative_positions_without_any_original_photo_attempt": 0,
    "all_372_original_positions_at_least_source_photo_attempted": True,
    "source_critical_second_reader_verified_for_all_positions": False,
    "scientific_1647_ra_year_method_ascendant_calculations_validated": False,
    "modern_ephemeris_and_birth_datetime_parity_validated": False,
    "Western_Lilly_accepted_history_unchanged": 12472,
    "Chinese_V3_accepted_history_unchanged": 142,
    "individual_human_outcome_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "rows": rows,
}
p = B / "ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "historical_source_positions": 372,
            "current_source_legible": 365,
            "source_glyph_unresolved": 7,
            "not_attempted": 0,
            "new_photo_corrections": differences,
            "overlay_sha256": sha(p),
        },
        indent=2,
    )
)
