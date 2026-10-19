#!/usr/bin/env python3
# ruff: noqa: E501  # Long historical source explanations remain intact.
"""Carry already scrutinized original Naibod first and second printing tables.

The source has 90 degree rows and 59 visibly numbered minute rows; one
printed label (27) is missing and the first-minute 1647 glyph is uncertain.
Do not normalize degree69 rollover, 24h, printed minute60, or source errors.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
OLD = B.parent / "B07x"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
SIG = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, x):
    Path(path).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


raw = load(OLD / "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json")
compare = load(OLD / "NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json")
index = load(INDEX)
china = load(CHINA)
assert index["records_count"] == 12546
assert index["batches"][-1]["id"] == "B07ai"
assert index["next"]["pdf_page"] == 747
assert china["sum_source_annotations"] == 262
assert raw["first_edition_pdf_sha256"] == SIG
assert len(raw["degree_rows"]) == 90
assert len(raw["minute_rows"]) == 59
assert raw["missing_source_minute_labels"] == [27]
assert compare["full_1647_source_table_digit_corpus_checked"] is False
assert compare["full_1659_source_table_digit_corpus_checked"] is False
assert compare["independent_real_human_predictions_validated"] == 0
degree = {r["equatorial_degrees"]: r for r in raw["degree_rows"]}
minute = {r["equatorial_arcminutes_as_printed"]: r for r in raw["minute_rows"]}
assert set(degree) == set(range(1, 91))
assert set(minute) == set(range(1, 61)) - {27}
assert degree[11]["printed_1647_days"] == 58 and degree[11]["printed_1647_hours"] == 21
assert degree[69]["printed_1647_years"] == 70
assert degree[80]["printed_1647_hours"] == 24
assert degree[90]["printed_1647_years"] == 91
assert minute[8]["secondary_days"] == 44
assert minute[44]["secondary_hours"] == 8
assert minute[55]["secondary_days"] == 339 and minute[55]["secondary_hours"] == 17
assert minute[60]["secondary_days"] == 374
assert minute[1]["original_photo_day_ambiguity"] == [5, 6]
assert len(compare["comparisons"]) == 12

images = {}
for kind, page, _key in (
    ("original_1647_degree", 747, "degree_table"),
    ("original_1647_minute", 748, "minute_table"),
):
    src = OLD / "evidence" / f"pdf_1647-{page}.jpg"
    assert src.is_file()
    expected = (
        raw["first_edition_degree_photo_sha256"]
        if page == 747
        else raw["first_edition_minute_photo_sha256"]
    )
    assert sha(src) == expected
    images[kind] = {
        "physical_source_year": 1647,
        "original_pdf_frame": page,
        "printed_folio": page - 34,
        "path": str(src.relative_to(ROOT)),
        "sha256": sha(src),
        "bytes": src.stat().st_size,
    }
for kind, key in (
    ("separate_1659_degree", "degree_table"),
    ("separate_1659_minute", "minute_table"),
):
    entry = compare["second_edition"][key]
    src = OLD / entry["file"]
    assert src.is_file()
    assert sha(src) == entry["sha256"]
    images[kind] = {
        "physical_source_year": 1659,
        "original_djvu_page": entry["djvu_scan_page"],
        "printed_folio": entry["printed_folio"],
        "path": str(src.relative_to(ROOT)),
        "sha256": entry["sha256"],
        "bytes": src.stat().st_size,
    }

source_rows = []
for degree_number in range(1, 91):
    r = degree[degree_number]
    source_rows.append(
        {
            "kind": "degree",
            "source_equatorial_degrees": degree_number,
            "literal_1647_one_reader_years": r["printed_1647_years"],
            "literal_1647_one_reader_days": r["printed_1647_days"],
            "literal_1647_one_reader_hours": r["printed_1647_hours"],
            "modern_flat_text_year_candidate": r["secondary_transcript_years"],
            "source_year_1647_print_edition": True,
            "source_pdf_frame": 747,
            "original_1647_source_photo_SHA256": images["original_1647_degree"]["sha256"],
            "cross_edition_1659_complete_expert_verified": False,
            "historical_astrology_time_engine_validated": False,
            "human_prediction_validated": False,
            "runtime_promoted": False,
        }
    )
for key in sorted(minute):
    r = minute[key]
    source_rows.append(
        {
            "kind": "minute",
            "source_equatorial_arcminutes_printed_label": key,
            "literal_1647_one_reader_days": (None if key == 1 else r["secondary_days"]),
            "literal_1647_one_reader_hours": r["secondary_hours"],
            "secondary_searchable_days_not_authoritative": r["secondary_days"],
            "1647_first_minute_day_glyph_options": r["original_photo_day_ambiguity"],
            "source_anomaly_notes": r["source_anomaly_notes"],
            "source_year_1647_print_edition": True,
            "source_pdf_frame": 748,
            "original_1647_source_photo_SHA256": images["original_1647_minute"]["sha256"],
            "cross_edition_1659_complete_expert_verified": False,
            "historical_astrology_time_engine_validated": False,
            "human_prediction_validated": False,
            "runtime_promoted": False,
        }
    )
assert len(source_rows) == 149
orig = {
    "schema": "LILLY_1647_NAIBOD_DEGREE90_MINUTE59_LITERAL_TABLE_CROSSWALK_V1",
    "batch": "B07aj",
    "original_first_edition_full_pdf_SHA256": SIG,
    "source_image_witnesses_first_and_second_editions": images,
    "previous_1647_source_table_SHA256": sha(OLD / "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json"),
    "previous_1647_1659_comparison_SHA256": sha(
        OLD / "NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json"
    ),
    "degree_source_printed_folio": 713,
    "minute_source_printed_folio": 714,
    "source_degree_rows": 90,
    "source_minute_rows_visible": 59,
    "missing_original_1647_printed_minute_labels": [27],
    "source_first_minute_day_glyph_1647_unresolved": [5, 6],
    "source_degree69_printed_1647_years_70": True,
    "source_degree80_prints_24_hours": True,
    "source_minute8_prints_44days10h": True,
    "source_minute44_1647_8h_vs_1659_18h": True,
    "source_minute60_prints_374days14h": True,
    "source_numeric_anomalies_retained_as_printed": True,
    "second_edition_all_149_source_cells_expert_collated": False,
    "original_natal_time_calculator_approved": False,
    "human_prediction_validations": 0,
    "runtime_promotions": 0,
    "selected_original_1647_vs_1659_comparison_records": compare["comparisons"],
    "rows": source_rows,
}
file = B / "ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"
save(file, orig)

topics = [
    (
        "degree_table_original_heading",
        "Naibod exact conversion of equatorial degrees, historical heading; not independently validated accuracy.",
        747,
    ),
    (
        "degree_rows_1_30",
        "Original first block equatorial degrees1–30 yields printed years/days/hours.",
        747,
    ),
    (
        "degree_rows_31_60",
        "Original second block equatorial degrees31–60 yields printed years/days/hours.",
        747,
    ),
    (
        "degree_rows_61_90",
        "Original third block equatorial degrees61–90 yields printed years/days/hours.",
        747,
    ),
    (
        "degree69_printed_year70",
        "Original degree69 explicitly has printed year70 and four days three hours, differing from modern flattened text.",
        747,
    ),
    (
        "degree80_printed_hour24",
        "Original degree80 prints 81 years, 62 days, 24 hours; do not normalize 24h.",
        747,
    ),
    (
        "degree90_printed_year91",
        "Original degree90 prints year91, 116 days, 13 hours in both editions.",
        747,
    ),
    (
        "minute_table_original_heading",
        "Original 1647 folio714 converts equatorial minutes into days and hours.",
        748,
    ),
    (
        "minute_rows_1_26",
        "Minute first block source labels1–26; original minute1 day glyph uncertain five/six.",
        748,
    ),
    (
        "missing_minute27",
        "After printed minute26 the original source jumps directly to minute28.",
        748,
    ),
    (
        "minute28_30_printed_values",
        "Original labels minute28–30 are retained literally, not shifted into fabricated minute27.",
        748,
    ),
    (
        "minute_second_block31_60",
        "Second block minute31–60 literal days/hours retained separately.",
        748,
    ),
    (
        "minute8_44days",
        "Original minute8 prints 44 days 10 hours despite progression suggesting different value.",
        748,
    ),
    (
        "minute44_two_editions_disagree",
        "1647 minute44 reads 271days8hours; 1659 copy reads 271days18hours.",
        748,
    ),
    (
        "minute55_worked_339days17h",
        "Printed minute55 gives 339 days 17 hours, used by worked terms example.",
        748,
    ),
    (
        "minute60_374days14h",
        "Printed 60-minute value is 374days14h, inconsistent with degree-one row.",
        748,
    ),
    (
        "two_tables_explicitly_distinguished",
        "Lilly's prose states first table converts degrees; second table converts minutes.",
        748,
    ),
    (
        "mars_terms_historical_target",
        "Worked ascendant to Mars terms has 11 degrees 55 minutes of equatorial arc.",
        748,
    ),
    ("naibod_degree11_11y58d21h", "Original degree11 row is 11 years 58 days 21 hours.", 748),
    ("naibod_minute55_339d17h", "Original minute55 row adds 339 days 17 hours.", 748),
    (
        "naibod_partial_sum_before_carry",
        "Source prints 11 years, 397 days and 38 hours before carrying excess days/hours.",
        748,
    ),
]
assert len(topics) == 21
rule_rows = []
for i, (kind, meaning, frame) in enumerate(topics):
    rule_rows.append(
        {
            "id": f"R{12547 + i}",
            "record_number": 12547 + i,
            "batch": "B07aj",
            "source_span": "B07aj-S001" if frame == 747 else "B07aj-S002",
            "original_pdf_frames": [frame],
            "original_printed_folio": frame - 34,
            "role": kind,
            "source_anchor_not_diplomatic": kind.replace("_", " "),
            "historical_meaning_only": meaning,
            "historical_source_documented_by_one_reader": True,
            "source_original_table_crosswalk": "batches/B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json",
            "source_critical_second_reader_149_cells_verified": False,
            "original_natal_epoch_direction_math_validated": False,
            "independent_human_predictive_event_validation": False,
            "runtime_model_promoted": False,
        }
    )
rules = {
    "batch": "B07aj",
    "status": "PARTIAL_ORIGINAL_1647_NAIBOD_DEGREE_AND_MINUTE_TABLES_SOURCE",
    "record_count": 21,
    "first_record": "R12547",
    "last_record": "R12567",
    "source_groups": 2,
    "body_pdf_frames": [747, 748],
    "original_naibod_first_print_degrees90_minutes59_not60": True,
    "original_minute27_missing_and_one_day_glyph_unresolved": True,
    "full_first_CLXVI_source_chapter_complete": False,
    "source_crosswalk_SHA256": sha(file),
    "human_prediction_validations": 0,
    "runtime_promotions": 0,
    "rules": rule_rows,
}
rulepath = B / "RULES.json"
save(rulepath, rules)
accept = {
    "batch": "B07aj",
    "Lilly_before": 12546,
    "Ptolemy_retained": 1066,
    "Chinese_V5_retained": 262,
    "source_note_count": 21,
    "Lilly_after_if_accepted": 12567,
    "Western_after_if_accepted": 13633,
    "next_record_id": "R12568",
    "next_original_pdf_frame": 749,
    "next_original_printed_folio": 715,
    "next_source": "Naibod 365day carry and Mars opposition worked example, duplicate printed CLXVI next unit",
    "full_first_CLXVI_source_chapter_complete": False,
    "149_table_rows_source_only": True,
    "source_crosswalk_SHA256": sha(file),
    "rules_SHA256": sha(rulepath),
    "original_first_edition_1647_full_pdf_SHA256": SIG,
    "independent_human_predictions_validated": 0,
    "runtime_model_promotions": 0,
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "source_degree_rows": 90,
            "source_minute_rows_visible": 59,
            "missing_label": 27,
            "source_uncertain_minute_one": True,
            "degree69_years": 70,
            "minute60_days": 374,
            "literal_page_source_records": 21,
            "next": "R12568",
            "source_sha256": sha(file),
            "rules_sha256": sha(rulepath),
        },
        indent=2,
    )
)
