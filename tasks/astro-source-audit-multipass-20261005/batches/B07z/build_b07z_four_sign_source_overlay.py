#!/usr/bin/env python3
"""Append photographed four source columns without altering accepted B07x/B07y notes."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARENT_Y = B.parent / "B07y"
PARENT_X = B.parent / "B07x"
ROOT = B.parents[3]
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


source = j(B / "FULL_COLUMNS_ARIES_TAURUS_GEMINI_CANCER_1647_V1.json")
b07y = j(PARENT_Y / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json")
b07x = j(PARENT_X / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json")
manual_y = j(PARENT_Y / "PHOTO_ADJUDICATION_1647_V1.json")
index = j(WESTERN)
china = j(CHINESE)
assert index["records_count"] == 12472 and index["batches"][-1]["id"] == "B07w"
assert china["sum_source_annotations"] == 142
assert b07x["source_cells_expected"] == len(b07y["rows"]) == 372
assert manual_y["unambiguous_original_photo_readings"] == 22
assert manual_y["unresolved_original_photo_readings"] == 2
assert source["source_signs"] == ["Aries", "Taurus", "Gemini", "Cancer"]
assert source["four_sign_source_rows"] == len(source["records"]) == 124
assert source["original_rows_per_sign"] == 31
assert source["original_source_photo_sha256"] == sha(
    PARENT_Y / "evidence" / "original_1647_annual_measure_pdf745_3500.jpg"
)
assert not source["source_claimed_as_mathematical_corrected_values"]
assert source["runtime_promotions"] == 0

candidates = {(r["sign"], r["zodiac_degree"]): r for r in b07x["tentative_candidate_pairs"]}
previous = {(r["sign"], r["degree"]): r for r in b07y["rows"]}
assert len(candidates) == len(previous) == 372
readings = {}
for r in source["records"]:
    key = (r["sign"], r["degree"])
    assert key in candidates and key not in readings
    assert key not in {(a["sign"], a["degree"]) for a in manual_y["photo_readings"]}
    assert r["original_1647_rate_arcminutes"] >= 0
    assert 0 <= r["original_1647_rate_arcseconds"] < 60
    assert r["source_photo_half"] == ("first_half" if r["degree"] < 16 else "second_half")
    assert r["original_photo_is_source_not_modernautocorrected"]
    assert not r["runtime_promoted"] and not r["human_forecast_validated"]
    readings[key] = r
assert len(readings) == 124
assert all(
    set(k for k in readings if k[0] == sign) == {(sign, i) for i in range(31)}
    for sign in source["source_signs"]
)

new_differences = []
rows = []
for prior in b07y["rows"]:
    key = (prior["sign"], prior["degree"])
    doc = readings.get(key)
    old_derivative = prior["B07x_derivative_candidate_as_originally_retained"]
    if doc is None:
        as_printed = prior["B07y_manual_1647_source_photo_read"]
        alternatives = prior["B07y_manual_original_glyph_alternatives"]
        phase = (
            "B07y" if prior["B07y_review_status"] != "NO_NEW_DIRECT_PHOTO_ADJUDICATION" else None
        )
    else:
        as_printed = [
            doc["original_1647_rate_arcminutes"],
            doc["original_1647_rate_arcseconds"],
        ]
        alternatives = None
        phase = "B07z"
        if as_printed != old_derivative:
            new_differences.append(
                {
                    "sign": key[0],
                    "degree": key[1],
                    "derivative_rate": old_derivative,
                    "1647_first_edition_photo_rate": as_printed,
                    "source_fidelity_status": "UNBLINDED_SINGLE_READER_PHOTOGRAPHIC_REVISION",
                }
            )
    rows.append(
        {
            "sign": key[0],
            "degree": key[1],
            "frozen_B07x_derivative_candidate": old_derivative,
            "first_edition_1647_one_reader_photo_rate": as_printed,
            "unresolved_original_source_glyph_options": alternatives,
            "source_read_batch": phase,
            "first_edition_source_photo_verified_by_one_reader": as_printed is not None,
            "independent_second_reader_verified": False,
            "naibod_maginus_ptolemy_calendar_engine_verified": False,
            "real_life_event_predictive_accuracy_verified": False,
            "runtime_promoted": False,
        }
    )
assert len(rows) == 372
assert len(new_differences) == 1
assert new_differences == [
    {
        "sign": "Taurus",
        "degree": 28,
        "derivative_rate": [59, 56],
        "1647_first_edition_photo_rate": [59, 36],
        "source_fidelity_status": "UNBLINDED_SINGLE_READER_PHOTOGRAPHIC_REVISION",
    }
]
assert sum(r["first_edition_source_photo_verified_by_one_reader"] for r in rows) == 146
assert sum(bool(r["unresolved_original_source_glyph_options"]) for r in rows) == 2
assert (
    sum(
        not r["first_edition_source_photo_verified_by_one_reader"]
        and not r["unresolved_original_source_glyph_options"]
        for r in rows
    )
    == 224
)
assert len({(r["sign"], r["degree"]) for r in rows}) == 372

out = {
    "schema": "LILLY_1647_ANNUAL_RATE_372_PHOTO_EVIDENCE_OVERLAY_V2",
    "batch": "B07z",
    "original_first_edition_1647_full_pdf_sha256": source["source_pdf_full_sha256"],
    "direct_first_edition_photo_sha256": source["original_source_photo_sha256"],
    "parent_B07y_overlay_sha256": sha(
        PARENT_Y / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json"
    ),
    "new_source_first_four_signs_sha256": sha(
        B / "FULL_COLUMNS_ARIES_TAURUS_GEMINI_CANCER_1647_V1.json"
    ),
    "history_source_registry_lilly_retained": 12472,
    "independent_chinese_source_V3_retained": 142,
    "full_annual_table_positions": 372,
    "one_reader_photo_read_positions_cumulative_B07y_B07z": 146,
    "unresolved_original_photo_glyph_positions_cumulative": 2,
    "not_yet_first_edition_photo_read_positions_cumulative": 224,
    "one_full_column_per_verified_sign": 31,
    "new_full_columns": ["Aries", "Taurus", "Gemini", "Cancer"],
    "new_full_column_photo_positions": 124,
    "source_1647_values_differing_from_derivative_in_new_column": 1,
    "new_source_conflicts": new_differences,
    "original_1647_printed_Taurus27_nonmonotonic_rate_not_math_corrected": [59, 48],
    "original_1647_Taurus28_photo_rate": [59, 36],
    "source_complete_original_photo_table": False,
    "independent_photo_reader_reviews": 0,
    "historical_math_or_birth_chart_engine_verified": False,
    "human_predictive_accuracy_validations": 0,
    "runtime_promotions": 0,
    "cells": rows,
}
file = B / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json"
file.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "new_full_photo_columns": source["source_signs"],
            "new_first_edition_photo_rows": 124,
            "new_derivative_conflicts": new_differences,
            "cumulative_photo_read_one_reader": 146,
            "cumulative_ambiguous_source_glyphs": 2,
            "not_yet_photo_read_or_adjudicated": 224,
            "overlay_sha256": sha(file),
            "Western_accepted_Lilly_unchanged": 12472,
            "Chinese_V3_unchanged": 142,
        },
        indent=2,
    )
)
