#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve complete original-source annotations.
"""Close physical source span of FIRST 1647 printed CLXVI at page715.

Covers original Naibod worked carry and original duplicated chapter divider.
Source *documentary coverage* may be complete with unresolved old print glyphs;
old timing/math engine, independent research, and human results remain OPEN.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parent
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
FIRST = P / "B07x/evidence/pdf_1647-749.jpg"
SECOND = B / "evidence/1659_independent_printed715_djvu744.jpg"
SOURCE_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
FIRST_SHA = "6b1537073a6747916cf615d5aecf4d3a3fc22f8cd6125a8c103ad92f6a8faff8"
SECOND_SHA = "b220aa040522df63c24d79d2cfed6d5591d0b3d1b3b9b9c47eb81fd3f9d95409"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(p, v):
    Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


base = j(WEST)
china = j(CHINA)
tables = j(P / "B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json")
assert base["records_count"] == 12567
assert base["batches"][-1]["id"] == "B07aj"
assert base["next"]["pdf_page"] == 749
assert base["partial_numbered_chapters"][0]["complete"] is False
assert china["sum_source_annotations"] == 262
assert sha(FIRST) == FIRST_SHA and sha(SECOND) == SECOND_SHA
degree = {r["source_equatorial_degrees"]: r for r in tables["rows"] if r["kind"] == "degree"}
minute = {
    r["source_equatorial_arcminutes_printed_label"]: r
    for r in tables["rows"]
    if r["kind"] == "minute"
}
assert [
    degree[11]["literal_1647_one_reader_years"],
    degree[11]["literal_1647_one_reader_days"],
    degree[11]["literal_1647_one_reader_hours"],
] == [11, 58, 21]
assert [
    minute[55]["literal_1647_one_reader_days"],
    minute[55]["literal_1647_one_reader_hours"],
] == [339, 17]
assert [
    degree[19]["literal_1647_one_reader_years"],
    degree[19]["literal_1647_one_reader_days"],
    degree[19]["literal_1647_one_reader_hours"],
] == [19, 101, 17]
assert [
    minute[52]["literal_1647_one_reader_days"],
    minute[52]["literal_1647_one_reader_hours"],
] == [321, 4]

terms_before = [11, 58 + 339, 21 + 17]
terms_after_hours = [11, terms_before[1] + terms_before[2] // 24, terms_before[2] % 24]
terms_after_years = [
    terms_after_hours[0] + terms_after_hours[1] // 365,
    terms_after_hours[1] % 365,
    terms_after_hours[2],
]
opposition_before = [19, 101 + 321, 17 + 4]
opposition_after = [
    opposition_before[0] + opposition_before[1] // 365,
    opposition_before[1] % 365,
    opposition_before[2],
]
assert terms_before == [11, 397, 38]
assert terms_after_hours == [11, 398, 14]
assert terms_after_years == [12, 33, 14]
assert opposition_before == [19, 422, 21]
assert opposition_after == [20, 57, 21]
assert not base["partial_numbered_chapters"][0]["naibod_full_critical_edition_finished"]

source_photos = {
    "original_1647": {
        "original_full_1647_pdf_sha256": SOURCE_SHA,
        "source_pdf_frame": 749,
        "source_printed_folio": 715,
        "relative_source": str(FIRST.relative_to(ROOT)),
        "photo_sha256": FIRST_SHA,
        "bytes": FIRST.stat().st_size,
    },
    "separately_typeset_1659": {
        "source_djvu_frame": 744,
        "source_printed_folio": 715,
        "relative_source": str(SECOND.relative_to(ROOT)),
        "photo_sha256": SECOND_SHA,
        "bytes": SECOND.stat().st_size,
    },
}
cases = [
    {
        "case": "Mars_terms",
        "arc_target_degrees_minutes": [11, 55],
        "degree_lookup": [11, 58, 21],
        "minute_lookup": [339, 17],
        "before_hours_carry": terms_before,
        "after_hours_carry": terms_after_hours,
        "after_365day_year_carry": terms_after_years,
        "literal_1647_1659_witness_agreement": True,
    },
    {
        "case": "Mars_opposition",
        "arc_target_degrees_minutes": [19, 52],
        "degree_lookup": [19, 101, 17],
        "minute_lookup": [321, 4],
        "before_hours_carry": opposition_before,
        "after_hours_carry": opposition_after,
        "after_365day_year_carry": opposition_after,
        "literal_1647_1659_witness_agreement": True,
    },
]
notes = [
    (
        "terms_hour_sum",
        "11 years 397 days 38 hours",
        "The original terms example starts with 11y397d38h before carrying.",
    ),
    (
        "terms_24hour_carry",
        "make one day to be added to 397",
        "Convert 38 hours to one whole day plus fourteen hours.",
    ),
    (
        "terms_398_days",
        "11 398 14",
        "The source intermediate result is 11 years 398 days fourteen hours.",
    ),
    (
        "terms_365day_year",
        "subtract three hundred and sixty five dayes",
        "Lilly carries 365 nominal days into one full year.",
    ),
    (
        "terms_final_time",
        "twelve yeeres ... thirty three dayes ... fourteen houres",
        "The terms example concludes 12y33d14h.",
    ),
    (
        "mars_opposition_arc",
        "nineteen degrees and fifty two minutes",
        "Mars-opposition directed arc target is 19°52′.",
    ),
    (
        "opposition_degree_lookup",
        "nineteen yeers ... hundred and one days ... seventeen hours",
        "The degree19 table lookup contributes 19y101d17h.",
    ),
    (
        "opposition_minute_lookup",
        "fifty two min. ... three hundred twenty one dayes ... four hours",
        "Minute52 contributes 321d4h.",
    ),
    (
        "opposition_first_sum",
        "nineteen yeers ... four hundred twenty two dayes ... twenty one hours",
        "Lilly adds to 19y422d21h.",
    ),
    (
        "opposition_365day_carry",
        "three hundred sixty five dayes",
        "The second example subtracts a 365-day nominal year.",
    ),
    (
        "opposition_final_time",
        "aged twenty yeers ... fifty seven dayes ... twenty one hours",
        "The printed conclusion is 20y57d21h.",
    ),
    (
        "original_first_CLXVI_ends",
        "horizontal divider",
        "A physical rule after the Naibod example terminates the first printed CLXVI directions-time source unit.",
    ),
    (
        "duplicated_next_CLXVI_heading",
        "CHAP. CLXVI.",
        "A separate chapter begins on the same page with the identical printed numeral, not the same discussion.",
    ),
    (
        "next_annual_profections_heading",
        "Of annual Profections",
        "The next distinct source unit concerns annual profections and the profectional sign of each year.",
    ),
]
assert len(notes) == 14
rules = []
for i, (role, anchor, meaning) in enumerate(notes):
    rules.append(
        {
            "id": f"R{12568 + i}",
            "record_number": 12568 + i,
            "batch": "B07ak",
            "source_span": "B07ak-S001",
            "original_pdf_frames": [749],
            "original_printed_folio": 715,
            "role": role,
            "source_anchor_label_not_diplomatic_quote": anchor,
            "source_historical_meaning_only": meaning,
            "original_first_ed_photo_SHA256": FIRST_SHA,
            "original_second_ed_photo_SHA256": SECOND_SHA,
            "source_one_reader_physical_print_witnessed": True,
            "original_1647_time_engine_verified": False,
            "human_event_prediction_validated": False,
            "runtime_model_promoted": False,
        }
    )
data = {
    "schema": "LILLY_1647_FIRST_CLXVI_NAIBOD_WORKED_CARRY_AND_DUPLICATED_HEADING_V1",
    "batch": "B07ak",
    "source_photographic_first_and_second_edition_witnesses": source_photos,
    "source_first_printed_CLXVI_directions_time_text_physically_ends_PDF749": True,
    "second_distinct_original_PRINTED_CLXVI_starts_same_PDF749": True,
    "source_verified_by_one_reader_not_critical_expert_editions": True,
    "prior_b07aj_149_table_rows_SHA256": sha(
        P / "B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"
    ),
    "source_1647_original_rate_table_seven_unresolved_glyphs_remain": True,
    "source_Naibod_original_minute27_label_missing": True,
    "source_all_1647_numbered_chapter_physical_pages_attempted": True,
    "source_first_CLXVI_full_expert_diplomatic_critical_edition_complete": False,
    "source_old_astrological_chart_time_engine_mathematically_verified": False,
    "independently_blinded_actual_person_predictions": 0,
    "runtime_promotions": 0,
    "cases": cases,
    "note_count": len(rules),
    "records": rules,
}
path = B / "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json"
save(path, data)
reg = {
    "batch": "B07ak",
    "status": "FIRST_1647_PRINTED_CLXVI_PHYSICAL_SOURCE_CHAPTER_COVERED_WITH_UNRESOLVED_GLYPHS",
    "record_count": len(rules),
    "first_record": "R12568",
    "last_record": "R12581",
    "source_groups": 1,
    "body_pdf_frames": [749],
    "physical_first_CLXVI_source_full_span_pdf_frames_742_to_749": True,
    "textual_source_first_CLXVI_closed_at_physical_divider": True,
    "independent_expert_edition_collation_finished": False,
    "historical_natal_direction_age_engine_verified": False,
    "empirical_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "rules": [
        {
            "id": r["id"],
            "record_number": r["record_number"],
            "batch": "B07ak",
            "source_span": "B07ak-S001",
            "original_pdf_frames": [749],
            "role": r["role"],
            "source_anchor_not_diplomatic": r["source_anchor_label_not_diplomatic_quote"],
            "historical_meaning_only": r["source_historical_meaning_only"],
            "historical_source_documented": True,
            "independent_real_event_timing_accuracy_validated": False,
            "independent_health_or_death_prediction_validated": False,
            "original_directions_angle_date_conversion_verified": False,
            "runtime_model_promoted": False,
        }
        for r in rules
    ],
}
save(B / "RULES.json", reg)
accept = {
    "batch": "B07ak",
    "Lilly_before": 12567,
    "Ptolemy_retained": 1066,
    "Chinese_V5_retained": 262,
    "new_historical_source_records": 14,
    "Lilly_after_if_accepted": 12581,
    "Western_after_if_accepted": 13647,
    "physical_first_CLXVI_source_heading_covered": True,
    "source_full_critical_edition_expert_collation": False,
    "source_true_astro_calendar_engine_verified": False,
    "next_original_R": "R12582",
    "next_original_pdf_frame": 749,
    "next_original_printed_folio": 715,
    "next_printed_chapter_label": "CLXVI",
    "next_editorial_distinct_chapter_ordinal": 166,
    "next_chapter_heading": "Of annual Profections, and by what means to find out the Profectionall Signe of every yeer",
    "original_Naibod_terms_result": terms_after_years,
    "original_Naibod_opposition_result": opposition_after,
    "source_record_SHA256": sha(path),
    "rules_SHA256": sha(B / "RULES.json"),
    "human_predictive_validations": 0,
    "runtime_promotions": 0,
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "source_cases": 2,
            "source_1647_1659_Mars_terms": terms_after_years,
            "source_1647_1659_Mars_opposition": opposition_after,
            "first_printed_CLXVI_source_physically_covered": True,
            "next_distinct_heading_same_printed_numeral": True,
            "records": len(rules),
            "first": reg["first_record"],
            "last": reg["last_record"],
            "next": accept["next_original_R"],
            "new_doc_SHA256": sha(path),
        },
        indent=2,
    )
)
