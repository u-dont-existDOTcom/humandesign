#!/usr/bin/env python3
# ruff: noqa: E501  # Historical source locator strings retained.
"""First and SECOND original printed CLXVI are distinct source units.

Document original 1647 annual-profection source p715-718 (PDF749-752).
Source table's 72 historical rows are physically evidenced, but eight zodiac
data columns not exhaustively transcribed, and are NOT retrospectively
generated from cyclic formulas and asserted as original handwriting.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
SOURCE_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
PHOTOS = {
    749: BASE / "B07x/evidence/pdf_1647-749.jpg",
    750: BASE / "B07x/evidence/pdf_1647-750.jpg",
    751: B / "evidence/1647_original_pdf-751.jpg",
    752: B / "evidence/1647_original_pdf-752.jpg",
}
SHA = {
    749: "6b1537073a6747916cf615d5aecf4d3a3fc22f8cd6125a8c103ad92f6a8faff8",
    750: "e8a52bf9b5e5d1391203b9bf2a0e50360bf5e11d78bb66502d41f530eee95eb9",
    751: "36a85230348860504366dae169e0cd50bdcacfbf7f138235eae18456e1b30aef",
    752: "27f15b011b86d789e7686368e3529f8dbc24448dddc975e123eb9932bb28abe7",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


idx = j(INDEX)
ch = j(CHINA)
assert idx["records_count"] == 12581
assert idx["read_numbered_chapters"] == list(range(1, 166))
assert idx["next"]["chapter"] == "CLXVI"
assert idx["next"]["editorial_source_sequence_ordinal"] == 166
assert idx["next"]["pdf_page"] == 749
assert idx["next"]["include_opening_paragraph"] is True
assert ch["sum_source_annotations"] == 262
for page, file in PHOTOS.items():
    assert file.is_file() and sha(file) == SHA[page], (page, file)

notes = [
    (
        749,
        "profection_progression_synonym",
        "Profection and Progression are all one",
        "Lilly treats profection and progression as names for an orderly change of significators through signs.",
    ),
    (
        749,
        "regular_successions",
        "regular or orderly change of the Significators",
        "The method shifts source significators through successive zodiac signs.",
    ),
    (
        749,
        "threefold_profection",
        "Profection is threefold",
        "He divides profection into annual, monthly and daily forms.",
    ),
    (
        749,
        "annual_30_degrees_one_sign",
        "thirty degrees, or one whole Signe to a solar yeer",
        "Annual profections move 30 ecliptic degrees, one whole sign, per solar year.",
    ),
    (
        749,
        "generic_6_Gemini_to_6_Cancer",
        "the sixt degree of ♊ ... the sixt degree of ♋",
        "An illustrative generic ascendant at 6° Gemini shifts to 6° Cancer in the next sign.",
    ),
    (
        750,
        "second_year_Cancer_to_Leo",
        "second yeer ... ♋ ... ♌",
        "The generic example proceeds Cancer to Leo in the second year.",
    ),
    (
        750,
        "third_year_Leo_to_Virgo",
        "third yeer ... ♌ ... ♍",
        "The generic example proceeds Leo to Virgo in the third year.",
    ),
    (
        750,
        "twelve_year_repeat",
        "every twelft yeer the annuall Profections are the same",
        "Annual source profections return to their zodiac state every twelve completed years.",
    ),
    (
        750,
        "solar_return_annual_clock",
        "☉ returnes to the degree and minute ... Radix",
        "Lilly starts the solar profection year at the Sun's return to natal degree/minute, not simply Gregorian Jan1.",
    ),
    (
        750,
        "cusp_degree_fixed_sign_shifts",
        "same degree and minute ... Signe onely varied",
        "For house cusps, natal degree/minute stay fixed while the zodiac sign shifts.",
    ),
    (
        750,
        "monthly_one_sign_period",
        "unto every moneth one Signe",
        "Monthly profection advances one sign for each original profection month.",
    ),
    (
        750,
        "monthly_thirteen_equal_parts",
        "divide the solar yeer into thirteen equall parts",
        "The text says to divide the solar year into THIRTEEN equal parts, even though annual sign cycle has twelve.",
    ),
    (
        750,
        "diurnal_sign_period",
        "two dayes three hours and fifty four minutes",
        "Printed diurnal profection assigns one sign to 2 days 3 hours 54 minutes; keep source literal.",
    ),
    (
        750,
        "author_chooses_annual_only",
        "I will onely proceed to annuall Profections",
        "Lilly chooses to treat annual profections for practicality.",
    ),
    (
        750,
        "separate_table_per_nat",
        "a particular Table for every Nativity",
        "Author prefers making a table for each natal case rather than a universal lookup.",
    ),
    (
        751,
        "example_merchant_birth",
        "A MERCHANT Borne ... 19. of Septemb. Anno 1616",
        "The historical illustrative merchant was born September19, 1616, per original heading.",
    ),
    (
        751,
        "merchant_72_year_labels",
        "0 12 24 36 48 60",
        "The original table spans six columns of twelve indexed years, 0–71, calendar labels 1616–1687.",
    ),
    (
        751,
        "merchant_original_8_position_streams",
        "A Table of Profections",
        "A printed merchant chart table includes multiple sign tracks; not all individual glyph cells are critically transcribed.",
    ),
    (
        751,
        "merchant_selected_year24_1640",
        "24 ... 1640",
        "One visibly printed row pairs 24 completed years and historical year 1640.",
    ),
    (
        751,
        "cyclic_annual_profections_table",
        "12 ... 1628",
        "Table returns 12 years later to source sign pattern; this is historical printed example, not a human outcome.",
    ),
    (
        752,
        "completed_years_not_current_year",
        "yeers ... compleat, not currant",
        "Use years completed for lookup, not ordinal year currently underway.",
    ),
    (
        752,
        "example_25th_year_use_completed24",
        "25. yeer ... 24. yeers compleat",
        "The twenty-fifth year of life is entered with 24 completed years.",
    ),
    (
        752,
        "example_1640_to_1641",
        "nineteenth of September, 1640 ... 1641",
        "Example year25 is from September19,1640 to September19,1641.",
    ),
    (
        752,
        "profected_1640_ascendant_Capricorn",
        "over against 1640 ... ♑ ... ascendant and 6.37",
        "For year1640 example, profected Ascendant is Capricorn 6°37′.",
    ),
    (
        752,
        "year26_ascendant_Aquarius",
        "26. yeer ... 6. degr. 37. min. ♒",
        "Next year moves profected Ascendant to Aquarius 6°37′.",
    ),
    (
        752,
        "retain_degrees_minutes_change_sign",
        "retaining the same degrees and minutes",
        "Original chart positions preserve degrees/minutes but move to succeeding signs.",
    ),
    (
        752,
        "five_hylegical_places_direct",
        "direct the five Hylegiacall places",
        "Lilly says to direct five Hylegial points after building the profectional figure.",
    ),
    (
        752,
        "nominal_degree_time_12d4h12m",
        "twelve dayes foure houres, and twelve minutes",
        "One degree is assigned 12 days 4 hours 12 minutes in this profectional direction explanation.",
    ),
    (
        752,
        "next_distinct_print_CLXVII",
        "Chap. CLXVII.",
        "A physical divider introduces new printed CHAP CLXVII on this very original folio718.",
    ),
    (
        752,
        "next_use_profections_heading",
        "Of the Use of Profections, and their Effects",
        "Next distinct chapter addresses combining profections and directions to assess claimed event timing.",
    ),
]
assert len(notes) == 30
events = []
for i, (page, kind, anchor, meaning) in enumerate(notes):
    events.append(
        {
            "id": f"R{12582 + i}",
            "record_number": 12582 + i,
            "batch": "B07al",
            "original_pdf_frame": page,
            "original_printed_folio": page - 34,
            "physical_section": "SECOND_PRINTED_CLXVI_ANNUAL_PROFECTIONS",
            "role": kind,
            "short_original_photo_source_anchor_or_locator": anchor,
            "historical_source_interpretation": meaning,
            "first_edition_original_photo_sha256": SHA[page],
            "source_evidence_provisional_one_reader": True,
            "merchant_table_full_8_stream_cell_collation": False,
            "historical_solar_return_hour_calendar_parity": False,
            "independently_blinded_real_person_event_validation": False,
            "runtime_model_promoted": False,
        }
    )
source = {
    "schema": "LILLY_1647_DUPLICATED_PRINT_CLXVI_ANNUAL_PROFECTIONS_P715_718_V1",
    "batch": "B07al",
    "original_Wellcome_first_edition_full_PDF_SHA256": SOURCE_SHA,
    "original_first_edition_photo_witnesses": {
        str(page): {
            "printed_folio": page - 34,
            "PDF_frame": page,
            "file": str(file.relative_to(ROOT)),
            "sha256": sha(file),
            "bytes": file.stat().st_size,
        }
        for page, file in PHOTOS.items()
    },
    "second_distinct_PRINTED_CLXVI_source_unit": True,
    "first_PRINTED_CLXVI_directions_time_not_reopened": True,
    "next_PRINTED_CLXVII_starts_on_same_original_PDF752": True,
    "author_solar_return_tied_to_natal_Sun_degree_minute": True,
    "annual_profection_one_sign_per_completed_year": True,
    "annual_sign_cycle_length_years": 12,
    "printed_monthly_profection_parts": 13,
    "printed_diurnal_sign_days_hours_minutes": [2, 3, 54],
    "printed_one_degree_nominal_days_hours_minutes": [12, 4, 12],
    "historic_merchant_natal_date_as_printed": "1616-09-19",
    "historic_merchant_table_years_inclusive": [1616, 1687],
    "historic_merchant_example_25th_year_calendar_1640_1641": [1640, 1641],
    "historic_merchant_example_year_25_profected_ascendant": "Capricorn 6deg37min",
    "original_merchant_table_physical_source_rows": 72,
    "all_merchant_table_zodiac_cells_expert_collated": False,
    "modern_Chinese_or_Western_natal_calculation_parity_verified": False,
    "real_person_outcome_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "record_count": 30,
    "records": events,
}
f = B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json"
save(f, source)
rules = {
    "batch": "B07al",
    "status": "DUPLICATED_PRINTED_CLXVI_ANNUAL_PROFECTIONS_PHYSICAL_SOURCE_COVERED",
    "record_count": 30,
    "first_record": "R12582",
    "last_record": "R12611",
    "source_groups": 4,
    "body_pdf_frames": [749, 750, 751, 752],
    "source_next_distinct_CLXVII_same_PDF752": True,
    "author_original_merchant_example_not_independent_human_test": True,
    "complete_merchant_profection_table_digit_collation": False,
    "empirical_real_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "rules": [
        {
            "id": r["id"],
            "record_number": r["record_number"],
            "batch": "B07al",
            "source_span": f"B07al-S{r['original_pdf_frame'] - 748:03d}",
            "original_pdf_frames": [r["original_pdf_frame"]],
            "source_anchor_not_diplomatic": r["short_original_photo_source_anchor_or_locator"],
            "role": r["role"],
            "historical_meaning_only": r["historical_source_interpretation"],
            "historical_source_documented": True,
            "independent_real_event_timing_accuracy_validated": False,
            "real_person_health_safety_social_status_advice_authorized": False,
            "runtime_model_promoted": False,
        }
        for r in events
    ],
}
save(B / "RULES.json", rules)
accept = {
    "batch": "B07al",
    "prior_Lilly": 12581,
    "Ptolemy_retained": 1066,
    "Chinese_V5_retained": 262,
    "new_documentary_source_records": 30,
    "Lilly_if_accepted": 12611,
    "Western_if_accepted": 13677,
    "editorial_new_completed_source_sequence_ordinal": 166,
    "original_printed_numeral_for_current": "CLXVI",
    "next_editorial_source_ordinal": 167,
    "next_printed_numeral": "CLXVII",
    "next_source_R": "R12612",
    "next_original_pdf_frame": 752,
    "next_original_printed_folio": 718,
    "next_original_heading": "Of the Use of Profections, and their Effects",
    "all_four_physical_pages_checked": True,
    "all_merchant_table_cells_expert_collated": False,
    "real_people_predictions_validated": 0,
    "runtime_promotions": 0,
    "source_SHA256": sha(f),
    "rules_SHA256": sha(B / "RULES.json"),
}
save(B / "ACCEPTANCE.json", accept)
print(
    json.dumps(
        {
            "source_annotated_claims": 30,
            "printed_monthly_divisor_original": 13,
            "literal_daily_sign_rate": [2, 3, 54],
            "merchant_example_year25": 1640,
            "physical_next_CHAP_CLXVII_starts_same_page": True,
            "source_rules_SHA256": sha(B / "RULES.json"),
            "next": "R12612",
        },
        indent=2,
    )
)
