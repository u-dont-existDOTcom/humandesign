#!/usr/bin/env python3
"""Freeze original source, numerical worked cases and explicitly unresolved cells."""

import hashlib
import json
from pathlib import Path

from lilly_1647_direction_time_mechanics import source_demo_cases

B = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    (B / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


window = json.loads((B / "ORIGINAL_SOURCE_WINDOW_V1.json").read_text())
assert window["source_index_parent_sha256"]
assert window["body_original_pdf_frames"] == list(range(742, 750))
assert window["following_heading_is_duplicate_printed_numeral"]
assert window["next_historical_record"] == "R12473"
for photo in window["photos"].values():
    original = B / photo["file"]
    assert sha(original) == photo["sha256"]
    assert original.stat().st_size == photo["bytes"]

cases = source_demo_cases()
assert cases["terms_arc"] == {"degree": 11, "minute": 55, "second": 0}
assert cases["opposition_arc"] == {"degree": 19, "minute": 52, "second": 0}
assert cases["naibod_original_result_terms"] == {"years": 12, "days": 33, "hours": 14}
assert cases["naibod_original_result_opposition"] == {
    "years": 20,
    "days": 57,
    "hours": 21,
}

source_statements = [
    {
        "method": "PTOLEMY_PRIMARY_DIRECTION_DEGREE_PER_YEAR",
        "photo": 743,
        "anchor": "oblique ascension of the ascendant 312.10",
        "original_numeric": {"ascendant": [312, 10]},
        "status": "visual_source_witness",
    },
    {
        "method": "PTOLEMY_PRIMARY_DIRECTION_DEGREE_PER_YEAR",
        "photo": 743,
        "anchor": "oblique ascension of the Termes of Mars 324.5",
        "original_numeric": {"mars_terms": [324, 5], "printed_diff": [11, 55]},
        "status": "visual_source_witness",
    },
    {
        "method": "PTOLEMY_PRIMARY_DIRECTION_DEGREE_PER_YEAR",
        "photo": 743,
        "anchor": "opposition of Mars 332.2",
        "original_numeric": {"mars_opposition": [332, 2], "printed_diff": [19, 52]},
        "status": "visual_source_witness",
    },
    {
        "method": "PTOLEMY_PRIMARY_DIRECTION_DEGREE_PER_YEAR",
        "photo": 743,
        "anchor": "for every degree ... one yeere ... for every minute ... six dayes",
        "original_numeric": {"one_arc_degree_years": 1, "one_arc_minute_days": 6},
        "status": "visual_source_witness",
    },
    {
        "method": "MAGINUS_APPARENT_SUN_MOTION_RATE",
        "photo": 744,
        "anchor": "right ascension 186.58 ... 186.4 ... 54 minutes",
        "original_numeric": {
            "sun_right_ascension_day1": [186, 4],
            "sun_right_ascension_day2": [186, 58],
            "derived_rate_arcminutes": 54,
        },
        "status": "visual_source_witness",
    },
    {
        "method": "MAGINUS_APPARENT_SUN_MOTION_RATE",
        "photo": 745,
        "anchor": "table entry 7 degrees Libra 54 min 25 seconds",
        "original_numeric": {
            "sun_natal_zodiac": "6 degrees 37 minutes Libra",
            "rounded_lookup_degree": 7,
            "minutes": 54,
            "seconds": 25,
        },
        "status": "visual_single_cell_checked",
    },
    {
        "method": "MAGINUS_ANNUAL_RATE_54_MIN",
        "photo": 746,
        "anchor": "degree table 13 years: 11 degrees 42 minutes",
        "original_numeric": {
            "whole_years": 13,
            "achieved_arc": [11, 42],
            "target_arc": [11, 55],
            "printed_partial_minutes_used": 42,
            "reconstructed_remaining_minutes": 13,
        },
        "status": "visual_checked_internal_arithmetic_discrepancy",
    },
    {
        "method": "MAGINUS_ANNUAL_RATE_54_MIN",
        "photo": 746,
        "anchor": "19 degrees 48 minutes for 22 years",
        "original_numeric": {
            "whole_years": 22,
            "achieved_arc": [19, 48],
            "target_arc": [19, 52],
            "printed_partial_minutes_used": 48,
            "reconstructed_remaining_minutes": 4,
        },
        "status": "visual_checked_internal_arithmetic_discrepancy",
    },
    {
        "method": "NAIBOD_TABULAR_DIRECTION_TIME",
        "photo": 747,
        "anchor": "A most exact Table ... Naibod ... degrees of AEquator",
        "original_numeric": {
            "11_degrees_year_day_hour": [11, 58, 21],
            "19_degrees_year_day_hour": [19, 101, 17],
            "one_degree_year_day_hour": [1, 5, 8],
        },
        "status": "visual_selected_source_cells_checked",
    },
    {
        "method": "NAIBOD_TABULAR_DIRECTION_TIME",
        "photo": 748,
        "anchor": "minutes table 55 gives 339 days 17 hours; 52 gives 321 days 4 hours",
        "original_numeric": {"55_minutes_days_hours": [339, 17], "52_minutes_days_hours": [321, 4]},
        "status": "visual_selected_source_cells_checked",
    },
    {
        "method": "NAIBOD_TABULAR_DIRECTION_TIME",
        "photo": 749,
        "anchor": (
            "subtract three hundred sixty five days ... twelve years "
            "thirty three days fourteen hours"
        ),
        "original_numeric": {
            "year_length_for_carry_days": 365,
            "terms_age": [12, 33, 14],
            "opposition_age": [20, 57, 21],
        },
        "status": "visual_worked_example_reproduced",
    },
    {
        "method": "PRINTED_CHAPTER_NUMBERING",
        "photo": 749,
        "anchor": "CHAP CLXVI Of annual Profections",
        "original_numeric": {
            "same_printed_numeral_as_previous_chapter": True,
            "new_distinct_numbered_heading_on_same_original_page": True,
        },
        "status": "physical_section_divider_verified",
    },
]
known = {
    "schema": "LILLY_1647_CLXVI_TIMING_WORKED_EXAMPLES_SOURCE_FIRST_V1",
    "batch": "B07x",
    "status": "NUMERICAL_METHOD_PROVISIONAL_NOT_CANONICALLY_ACCEPTED",
    "source": window["source"],
    "original_source_pdf_sha256": window["full_source_pdf_sha256"],
    "source_original_pdf_frames": list(range(742, 750)),
    "next_original_printed_chapter": "CLXVI_REPEATED_ANNUAL_PROFECTIONS",
    "original_printed_numeral_is_duplicated": True,
    "source_statements": source_statements,
    "derived_computation": cases,
    "internal_arithmetic_discrepancy": (
        "Maginus worked examples use printed year-table fractional minute "
        "cells (42' and 48') as if they were the remaining angular arc, "
        "whereas subtracting completed-year arcs from stated targets "
        "leaves 13' and 4'. The birth-chart and annual rate choices are "
        "not independently historically reconciled."
    ),
    "first_edition_annual_measure_table_cells_expected": 372,
    "first_edition_annual_measure_table_scalar_numbers_expected": 744,
    "annual_measure_cells_visually_verified": 1,
    "annual_measure_degree_rows_inclusive": [0, 30],
    "naibod_degree_table_rows_expected": 90,
    "naibod_minute_table_rows_expected": 60,
    "all_original_numerical_table_cells_collated": False,
    "anomalous_first_edition_examples_need_secondary_edition_comparison": True,
    "original_1647_source_technical_epoch_chart_input_validated": False,
    "historical_math_mechanics_reproduced_on_selected_cases_only": True,
    "independent_human_life_event_predictions_validated": 0,
    "runtime_promotions": 0,
}
save("WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json", known)
print(
    "Saved original numerical-method witness: 12 anchored source statements, "
    "3 historical timing methods, 2 source arithmetic discrepancies."
)
