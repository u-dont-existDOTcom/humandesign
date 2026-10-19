#!/usr/bin/env python3
"""Compare two independently printed Lilly editions and exact Maginus residuals.

Source examples are 17th-century historical text, not an astronomical model
or validation of actual events. Preserve literal printed figures separately
from any diagnostic arithmetic. Source photos are inspected by one reader.
"""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PHOTO = {
    "first_edition_1647_printed712_pdf746": {
        "file": "evidence/first_edition_1647_printed712_pdf746.jpg",
        "printed": 712,
        "original_pdf_frame": 746,
        "sha256": "a3a4955f3fa0ff446d95a730857f4add250ca876604289985fbaa9d30d813986",
    },
    "second_edition_1659_printed709_djvu738": {
        "file": "evidence/second_edition_1659_djvu_page_738.jpg",
        "printed": 709,
        "djvu_page": 738,
        "sha256": "55509e5690b849096d2a87bad2b79c30997ee5ce5c386b6e71aa05ea7e251918",
    },
    "second_edition_1659_printed710_djvu739": {
        "file": "evidence/second_edition_1659_djvu_page_739.jpg",
        "printed": 710,
        "djvu_page": 739,
        "sha256": "6d10cc1de22a6e05f1dd43fee2f5db4bd6463e7d0be1de146a23418bf114a0d5",
    },
    "second_edition_1659_printed712_djvu741": {
        "file": "evidence/second_edition_1659_djvu_page_741.jpg",
        "printed": 712,
        "djvu_page": 741,
        "sha256": "ee4fbe098258b57439cae727e2ac34eea9b703addb6d75a24d8494c2fffe2579",
    },
}


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def days_per_fractional_arc(arc_minutes: int, rate_minutes_per_year: int = 54) -> Fraction:
    if type(arc_minutes) is not int or type(rate_minutes_per_year) is not int:
        raise ValueError("Inputs must be exact integer historical arcminutes")
    if not 0 <= arc_minutes <= 360 * 60 or rate_minutes_per_year <= 0:
        raise ValueError("Invalid bounded historical arithmetic inputs")
    return Fraction(arc_minutes * 365, rate_minutes_per_year)


def reconstruct():
    for item in PHOTO.values():
        assert sha(B / item["file"]) == item["sha256"]
    index = j(
        ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
    )
    china = j(
        ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
    )
    assert index["records_count"] == 12472
    assert china["sum_source_annotations"] == 142
    parent = j(B.parent / "B07x/WORKED_DIRECTION_TIME_SOURCE_CASES_V1.json")
    assert parent["independent_human_life_event_predictions_validated"] == 0
    assert parent["runtime_promotions"] == 0

    cases = []
    for label, goal, whole_years, attained, printed_fraction, printed_days in (
        ("Mars_terms", (11, 55), 13, (11, 42), 42, 284),
        ("Mars_opposition", (19, 52), 22, (19, 48), 48, 324),
    ):
        target_arc = goal[0] * 60 + goal[1]
        prior_arc = attained[0] * 60 + attained[1]
        assert prior_arc == whole_years * 54
        true_remaining = target_arc - prior_arc
        assert true_remaining > 0
        printed_ratio = days_per_fractional_arc(printed_fraction)
        mathematical_ratio = days_per_fractional_arc(true_remaining)
        cases.append(
            {
                "historical_example": label,
                "source_page_printed": 712,
                "1647_and_1659_original_printed_targets": list(goal),
                "1647_and_1659_printed_completed_years": whole_years,
                "1647_and_1659_printed_attained_arc": list(attained),
                "source_annual_rate_arcminutes": 54,
                "source_printed_fraction_used_in_partial_year": printed_fraction,
                "source_printed_partial_year_days": printed_days,
                "computed_target_arcminutes": target_arc,
                "computed_attained_arcminutes": prior_arc,
                "computed_remaining_arcminutes": true_remaining,
                "printed_fraction_is_attained_minutes_not_residual": (
                    printed_fraction == attained[1] and printed_fraction != true_remaining
                ),
                "printed_fraction_year_days_exact": str(printed_ratio),
                "correct_residual_year_days_exact_under_same_365_day_rule": str(mathematical_ratio),
                "difference_in_365_day_nominal_days": str(printed_ratio - mathematical_ratio),
                "printed_days_consistent_with_printed_fraction_if_nearest_day": (
                    abs(printed_ratio - printed_days) <= Fraction(1, 2)
                ),
                "first_edition_source_photo": "first_edition_1647_printed712_pdf746",
                "second_edition_source_photo": "second_edition_1659_printed712_djvu741",
                "source_only_no_human_events": True,
            }
        )
    assert [a["computed_remaining_arcminutes"] for a in cases] == [13, 4]
    assert [a["printed_fraction_is_attained_minutes_not_residual"] for a in cases] == [True, True]
    assert [a["printed_days_consistent_with_printed_fraction_if_nearest_day"] for a in cases] == [
        True,
        True,
    ]

    original = {
        "schema": "LILLY_1647_AND_1659_MAGINUS_RESIDUAL_CROSS_EDITION_V1",
        "batch": "B07ae",
        "source": (
            "William Lilly Christian Astrology original 1647 first edition "
            "and separately typeset 1659 second edition"
        ),
        "Wellcome_1647_full_original_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "1659_original_printed_djvu_commons_file": "Christian Astrology (Lilly, 1659).djvu",
        "source_comparison_method": (
            "Direct one-reader visual comparison of original 1647 photographed p712 "
            "and separate 1659 typeset p712, with original Ptolemy/Maginus context "
            "on 1659 pp709–710. Mathematical analysis kept distinct."
        ),
        "source_years": [1647, 1659],
        "source_year_roughly_365_day_historical_example": 365,
        "annual_method_54_arcminutes_per_year": (
            "Maginus simple worked rate (different from separate 7 Libra "
            "54min25sec annual lookup table)"
        ),
        "two_photographic_1659_worked_paragraphs_still_contain_source_numbers_42_and_48": True,
        "neither_edition_corrects_remaining_arc_from_13_or_4_in_the_worked_examples": True,
        "source_printed_glyphs_verified_against_historical_editions_by_one_reader": True,
        "independently_blinded_second_human_reader": False,
        "original_method_a_natal_chart_era_engine_verified": False,
        "historic_source_format_not_independent_human_forecast_validation": True,
        "source_photos": PHOTO,
        "worked_cases": cases,
        "distinct_period_methods": [
            "Ptolemy 360day approximate arc-to-age",
            "Maginus daily solar right-ascension proportional annual arc",
            "Naibod degrees/minutes lookup and365day carry",
        ],
        "dependent_original_1647_note": (
            "B07x source time mechanics remains provisional; B07y–B07ad table "
            "is first-edition source-only. Do not treat two editions of the "
            "same text as independent predictive replication."
        ),
        "canonical_Lilly_historical_count_retained": 12472,
        "Chinese_V3_historical_count_retained": 142,
        "independent_real_human_prediction_validations": 0,
        "runtime_promotions": 0,
    }
    file = B / "MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json"
    file.write_text(json.dumps(original, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "cases": len(cases),
                "fractional_mismatch": [
                    (
                        x["computed_remaining_arcminutes"],
                        x["source_printed_fraction_used_in_partial_year"],
                    )
                    for x in cases
                ],
                "days_offsets": [x["difference_in_365_day_nominal_days"] for x in cases],
                "source_photo_hashes": [e["sha256"] for e in PHOTO.values()],
                "document_sha256": sha(file),
                "independent_person_validations": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    reconstruct()
