#!/usr/bin/env python3
"""Literal first-edition Lilly printed711 annual-rate table: source-only bridge.

Do not reread/reextract accepted B07y–B07ad single-reader original photo
evidence or misrepresent 1659 hints as 1647 readings. Preserve all 372
historical source rows with seven UNKNOWN original glyphs, fourteen literal
differences from the modern searchable derivative. No prediction engine.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07ad"
ORIGINAL = B.parent / "B07y"
COMPARE = B.parent / "B07af"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
SIGNS = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)
ABBREVIATIONS = (
    "ARI",
    "TAU",
    "GEM",
    "CAN",
    "LEO",
    "VIR",
    "LIB",
    "SCO",
    "SAG",
    "CAP",
    "AQU",
    "PIS",
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


source = load(PARENT / "ANNUAL_RATE_PHOTO_OVERLAY_V6.json")
hints = load(COMPARE / "SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json")
western = load(WEST)
chinese = load(CHINESE)
assert western["records_count"] == 12501
assert western["batches"][-1]["id"] == "B07ag"
assert western["next"]["pdf_page"] == 745
assert western["next"]["chapter"] == "CLXVI"
assert chinese["sum_source_annotations"] == 262
assert source["original_table_total_positions"] == 372
assert source["cumulative_one_reader_legible_original_1647"] == 365
assert source["cumulative_original_print_unresolved_positions"] == 7
assert source["cumulative_positions_without_any_original_photo_attempt"] == 0
assert hints["source_first_edition_unresolved_after"] == 7
assert (
    sha(ORIGINAL / "evidence/original_1647_annual_measure_pdf745_3500.jpg")
    == (source["historical_original_pdf745_photo_sha256"])
)
assert len(source["rows"]) == 372
before = source["rows"]
mapping = {(r["sign"], r["degree"]): r for r in before}
assert len(mapping) == 372
assert set(r["sign"] for r in before) == set(SIGNS)
assert all((s, degree) in mapping for s in SIGNS for degree in range(31))
assert all(not r["runtime_promoted"] for r in before)

errors = []
gaps = []
rows = []
sign_sources = []
for sign, abbreviated in zip(SIGNS, ABBREVIATIONS, strict=True):
    readings = []
    for degree in range(31):
        original = mapping[sign, degree]
        val = original["first_edition_1647_one_reader_photo_rate"]
        options = original["unresolved_original_source_glyph_options"]
        derivative = original["frozen_B07x_derivative_candidate"]
        assert options is None if val is not None else bool(options)
        if val is None:
            gaps.append((sign, degree))
        if val is not None and val != derivative:
            errors.append((sign, degree, derivative, val))
        reading = {
            "printed_sign_column": abbreviated,
            "sign": sign,
            "original_zodiac_degree_row": degree,
            "literal_original_1647_single_reader_rate_arcminutes_arcseconds": val,
            "original_1647_unresolved_print_glyph_options": options,
            "modern_derivative_candidate_not_authoritative": derivative,
            "first_edition_original_source_photo_pdf_frame": 745,
            "first_edition_original_source_printed_folio": 711,
            "actual_first_edition_photo_read_batch": original["source_read_batch"],
            "source_satisfies_single_reader_legible_only": val is not None,
            "source_critical_second_reader_verified": False,
            "year_arc_time_calculation_engine_verified": False,
            "human_natal_prediction_validated": False,
            "runtime_promoted": False,
        }
        rows.append(reading)
        readings.append(reading)
    encoded = json.dumps(
        readings, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    sign_sources.append(
        {
            "sign": sign,
            "source_abbreviation_1647": abbreviated,
            "original_degree_count": len(readings),
            "one_reader_legible": sum(
                r["literal_original_1647_single_reader_rate_arcminutes_arcseconds"] is not None
                for r in readings
            ),
            "original_glyph_unresolved": sum(
                r["literal_original_1647_single_reader_rate_arcminutes_arcseconds"] is None
                for r in readings
            ),
            "data_rows_SHA256_ordered": hashlib.sha256(encoded).hexdigest(),
        }
    )
assert len(rows) == 372
assert len(gaps) == 7
assert len(errors) == 14
assert sum(item["one_reader_legible"] for item in sign_sources) == 365
assert sum(item["original_glyph_unresolved"] for item in sign_sources) == 7
assert gaps == [
    ("Virgo", 1),
    ("Virgo", 18),
    ("Capricorn", 9),
    ("Capricorn", 15),
    ("Aquarius", 5),
    ("Aquarius", 6),
    ("Pisces", 24),
]
assert errors[0] == ("Taurus", 28, [59, 56], [59, 36])

data = {
    "schema": "LILLY_1647_FIRST_EDITION_ANNUAL_372_RATE_SOURCE_BOUNDARY_V1",
    "batch": "B07ah",
    "source_original_1647_book": (
        "William Lilly, Christian Astrology 1647 first edition, Wellcome b30338724"
    ),
    "source_original_1647_full_pdf_sha256": source["historical_full_pdf_sha256"],
    "source_first_edition_original_photo_pdf745_SHA256": source[
        "historical_original_pdf745_photo_sha256"
    ],
    "origin_original_365plus7_first_reader_archive": (
        "batches/B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
    ),
    "origin_source_overlay_sha256": sha(PARENT / "ANNUAL_RATE_PHOTO_OVERLAY_V6.json"),
    "source_independent_1659_djvu_image_not_critical_read": (
        "batches/B07y/evidence/1659_annual_measure_table_page740.jpg"
    ),
    "original_second_edition_1659_ambiguous_hints_not_substituted": True,
    "original_rate_printed_folio": 711,
    "original_pdf_frame": 745,
    "original_rate_table_sign_count": 12,
    "original_rate_degrees_per_sign": 31,
    "original_rate_total_physical_positions": 372,
    "original_1647_one_reader_legible": 365,
    "original_1647_unresolved": 7,
    "original_glyphs_without_any_photographic_attempt": 0,
    "original_vs_derived_searchable_text_disagreements": len(errors),
    "discrepancy_rows": [
        {"sign": s, "degree": d, "derivative": v, "one_reader_original": actual}
        for s, d, v, actual in errors
    ],
    "unresolved_source_rows": [{"sign": s, "degree": d} for s, d in gaps],
    "source_photo_claim_made_by_one_unblinded_reader_only": True,
    "historical_annual_measure_arithmetic_validated": False,
    "original_1647_first_and_second_print_source_expert_collation_done": False,
    "model_use_as_accurate_astro_calendar_or_event_prediction_authorized": False,
    "empirical_real_human_validations": 0,
    "runtime_promotions": 0,
    "sign_source_groups": sign_sources,
    "rows": rows,
}
target = B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"
save(target, data)

roles = [
    ("printed_annual_table_heading", "A Table of the annuall measure in Directions."),
    ("zodiac_degree_0_through_30", "Original table row labels zero through thirty"),
]
for item in sign_sources:
    roles.append(
        (
            "original_" + item["sign"].lower() + "_source_column",
            "Original printed sign column " + item["source_abbreviation_1647"],
        )
    )
assert len(roles) == 14
rules = []
for i, (role, label) in enumerate(roles):
    rec = {
        "id": f"R{12502 + i}",
        "record_number": 12502 + i,
        "batch": "B07ah",
        "source_span": "B07ah-ANN-P745",
        "original_pdf_frames": [745],
        "source_original_folio": 711,
        "role": role,
        "source_anchor_not_diplomatic": label,
        "historical_meaning_only": (
            "Original 1647 annual-equatorial-rate table for the Sun's zodiac degree; "
            "source photo has 12 sign columns with 31 degrees each, total 372 literal "
            "printed rate positions, 365 one-reader legible and 7 unresolved."
            if i == 0
            else "Degree row index for every historical zodiac column, 0–30 inclusive."
            if i == 1
            else f"One original {SIGNS[i - 2]} "
            "sign's annual-rate column, 31 printed degree positions. See exact "
            "source crosswalk, preserving all unverified and unresolved glyphs."
        ),
        "source_rate_table_file": "batches/B07ah/ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json",
        "historical_photo_corroboration_level": "ONE_UNBLINDED_READER",
        "historical_source_documented": True,
        "all_original_1647_rate_cells_independently_collated": False,
        "original_1647_natal_year_direction_engine_validated": False,
        "real_people_predictive_accuracy_validated": False,
        "human_mortality_health_financial_safety_inference_permitted": False,
        "runtime_model_promoted": False,
    }
    rules.append(rec)
assert [r["record_number"] for r in rules] == list(range(12502, 12516))
output = {
    "batch": "B07ah",
    "status": "ORIGINAL_1647_ANNUAL_RATE_TABLE_SOURCE_ONLY_14_HEADED_RECORDS",
    "printed_chapter": "CLXVI_first_original_directions_time_chapter",
    "record_count": 14,
    "first_record": "R12502",
    "last_record": "R12515",
    "source_groups": 1,
    "body_pdf_frames": [745],
    "original_printed_folio": 711,
    "original_372_rate_cells_are_separate_reversible_source_data": True,
    "first_edition_365_legible_7_unresolved": True,
    "source_source_table_SHA256": sha(target),
    "first_edition_photo_sha256": source["historical_original_pdf745_photo_sha256"],
    "full_CLXVI_historical_source_chapter_complete": False,
    "verified_true_historical_annual_direction_time_engine": False,
    "independent_human_predictive_validations": 0,
    "runtime_promotions": 0,
    "rules": rules,
}
rulefile = B / "RULES.json"
save(rulefile, output)
accept = {
    "batch": "B07ah",
    "prior_Lilly": 12501,
    "prior_Ptolemy": 1066,
    "Chinese_V5_parallel": 262,
    "new_historical_source_note_records": 14,
    "Lilly_if_accepted": 12515,
    "Western_with_Ptolemy_if_accepted": 13581,
    "next_original_R": "R12516",
    "next_original_PDF": 746,
    "next_original_printed_folio": 712,
    "next_original_source_scope": "1647 printed712 annual table use and time examples, then Naibod",
    "source_1647_365_legible_7_unknown": True,
    "original_1647_complete_critical_print_collation": False,
    "complete_CLXVI_chapter": False,
    "source_b07ad_overlay_sha256": sha(PARENT / "ANNUAL_RATE_PHOTO_OVERLAY_V6.json"),
    "source_rate_crosswalk_SHA256": sha(target),
    "rules_SHA256": sha(rulefile),
    "human_predictions_validated": 0,
    "runtime_promotions": 0,
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "source_physical_rows": 372,
            "one_reader_legible": 365,
            "unresolved": 7,
            "source_vs_derivative_differences": 14,
            "partial_historical_rules": 14,
            "first": "R12502",
            "last": "R12515",
            "next": "R12516",
            "source_crosswalk_sha256": sha(target),
            "historical_rules_sha256": sha(rulefile),
        },
        indent=2,
    )
)
