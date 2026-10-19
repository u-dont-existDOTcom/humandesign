#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve whole source-location and analytical gloss sentences.
"""Lilly CLXVI table-use and Maginus printed712 source-first, both editions.

Reference actual first edition p711 lower/p712 whole, plus separate 1659
printed edition; derivative text is only a navigational phrase locator.
Historical printed 42/48 minutes and exact remaining 13/4 minutes are
separate fields, not silently corrected. No human prediction.
"""

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parent
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
CROSS = P / "B07ah/ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"
ORIGINAL_BOOK_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
PHOTO = {
    "1647_original_printed711": P / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg",
    "1647_original_printed712": P / "B07ae/evidence/first_edition_1647_printed712_pdf746.jpg",
    "1659_original_printed711": P / "B07y/evidence/1659_annual_measure_table_page740.jpg",
    "1659_original_printed712": P / "B07ae/evidence/second_edition_1659_djvu_page_741.jpg",
}
CLAIMS = [
    (
        745,
        "table_use_heading",
        "The use of the Table.",
        "Introduces instructions for choosing annual equatorial rate from solar zodiac degree.",
    ),
    (
        745,
        "enter_sun_zodiac_degree",
        "Enter with the degrees adhering to the Sun in your Nativity",
        "Select the Sun's source-defined zodiac degree, not modern sun sign only.",
    ),
    (
        745,
        "round_up_strict_over_30",
        "more then 30 min. take the next greater degree",
        "Advance to the next greater source table degree strictly when appended minutes exceed 30.",
    ),
    (
        745,
        "worked_sun_6_libra_37",
        "the Sun is in 6.37. Libra",
        "Worked Sun is at 6 degrees 37 arcminutes of Libra.",
    ),
    (
        745,
        "worked_select_7_libra",
        "I enter with 7. degrees under Libra",
        "Because 37 exceeds 30, the author chooses printed row Libra degree7.",
    ),
    (
        745,
        "worked_7_libra_source_54_25",
        "I find 54 min. 25. sec.",
        "Original table's Libra7 row is 54 arcminutes 25 arcseconds per nominal year.",
    ),
    (
        745,
        "drop_seconds_permitted",
        "you may omit the seconds",
        "Lilly explicitly permits omitting 25 arcseconds and using whole 54 arcminutes.",
    ),
    (
        745,
        "cumulative_minutes_to_degrees",
        "by a continuall addition of minutes",
        "A simplified annual table is obtained by repeated addition then 60-minute carries.",
    ),
    (
        746,
        "table_24_years_header",
        "YR. 1 2 3 4 5 6 7 8 9 10",
        "The left table lists twenty-four numbered whole years.",
    ),
    (
        746,
        "annual_degree_table",
        "DEG 0 1 2 3 4 5 6",
        "The annual table records accumulated whole equatorial degrees.",
    ),
    (
        746,
        "annual_minute_table",
        "MIN 54 48 42 36 30",
        "The adjacent annual row tracks remainder arcminutes.",
    ),
    (
        746,
        "mars_terms_target_11_55",
        "the termes of Mars is 11. deg. 55.",
        "The worked terms target is 11 degrees 55 arcminutes in oblique ascension.",
    ),
    (
        746,
        "terms_table_13_years",
        "on the left hand 13. yeers",
        "Source uses 13 completed 54-arcminute years for its 11-degree-plus target.",
    ),
    (
        746,
        "terms_table_11_42_accumulated",
        "42. min adhering to 11. deg.",
        "At 13 years, table accumulation is 11 degrees 42 arcminutes.",
    ),
    (
        746,
        "term_printed_fraction_42",
        "42. min. give 284. dayes",
        "Source uses 42 arcminutes for fractional contribution, though 11:55 minus 11:42 is 13 arcminutes.",
    ),
    (
        746,
        "one_minute_equals_6days18hours",
        "one min. shall signifie 6 dayes 18. hours",
        "Lilly specifies six days and eighteen hours for each of the simplified 54 annual arcminutes.",
    ),
    (
        746,
        "terms_284_days",
        "284. dayes",
        "Source prints 284 days for the 42-minute fraction, rounded from 283.5 days at stated daily rate.",
    ),
    (
        746,
        "terms_age_13_and_three_quarters",
        "13. yeers compleat and three quarters currant",
        "Author describes a little more than 13 and three quarters years, referring to his rounded printed fraction.",
    ),
    (
        746,
        "mars_opposition_target_19_52",
        "19. deg. 52. min.",
        "The second worked arc target is 19 degrees 52 arcminutes.",
    ),
    (
        746,
        "mars_opp_22_years",
        "In this Table 19. degr. give 22. yeers.",
        "The source takes 22 whole 54-arcminute years to reach 19 degrees 48 arcminutes.",
    ),
    (
        746,
        "mars_opp_19_48_accumulated",
        "19. degr. give 22. yeers.",
        "At year22, accumulated arc is 19 degrees 48 arcminutes.",
    ),
    (
        746,
        "mars_opp_printed_fraction_48",
        "And 48. min. give 324. dayes",
        "The source uses 48 instead of the actual 4-minute difference from 19:48 to 19:52.",
    ),
    (
        746,
        "mars_opp_324_days",
        "324. dayes",
        "At six days eighteen hours each, 48 minutes gives exactly 324 nominal days.",
    ),
    (
        746,
        "mars_opp_23rd_year",
        "23. yeer current",
        "Author attributes this example to time during the 23rd year.",
    ),
    (
        746,
        "naibod_third_method",
        "The third and last Measure of time",
        "The text introduces a third, separate Naibod timing measure.",
    ),
    (
        746,
        "naibod_commentary",
        "Valentine Naibods in his Coment of Ptolomey",
        "Lilly attributes the Naibod measure to a commentary on Ptolemy.",
    ),
    (
        746,
        "maginus_de_diebus_citation",
        "de Diebus Criticis",
        "Lilly cites Maginus as publishing/commending Naibod's method.",
    ),
    (
        746,
        "published_1619_historical_claim",
        "new Tables published in 1619",
        "Lilly attributes an edition year to Maginus's new tables; bibliographic provenance not independently confirmed.",
    ),
    (
        746,
        "naibod_when_sufficient_time",
        "where I take or have sufficient time allowed me",
        "He says he personally chooses Naibod's method when sufficient time is available.",
    ),
    (
        746,
        "ptolemy_shortcut_when_little_time",
        "otherwise, I use Ptolomies way",
        "For lower-effort natal readings he reports using Ptolemy instead.",
    ),
    (
        746,
        "naibod_claim_most_exact",
        "the most exactest measure",
        "Lilly expresses an opinion that Naibod's method is most precise; this is not verification.",
    ),
]
assert len(CLAIMS) == 31


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(p, a):
    Path(p).write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compute_year_table(rate=54):
    assert rate == 54
    return [
        {
            "printed_whole_year": y,
            "one_reader_original_1647_printed_accumulated_degree": (y * rate) // 60,
            "one_reader_original_1647_printed_remaining_arcminute": (y * rate) % 60,
            "analytical_54_times_years_arcminutes": y * rate,
            "first_edition_printed712_photo_verified_by_one_reader_only": True,
            "source_readings_are_not_independent_annual_ephemeris_validations": True,
        }
        for y in range(1, 25)
    ]


def freeze(text_path):
    index = load(INDEX)
    china = load(CHINESE)
    table = load(CROSS)
    prev = load(P / "B07ae/MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json")
    assert index["records_count"] == 12515 and index["batches"][-1]["id"] == "B07ah"
    assert index["next"]["pdf_page"] == 746 and index["next"]["chapter"] == "CLXVI"
    assert china["sum_source_annotations"] == 262
    assert table["original_rate_total_physical_positions"] == 372
    assert table["original_1647_one_reader_legible"] == 365
    assert prev["independent_real_human_prediction_validations"] == 0
    for name, file in PHOTO.items():
        assert file.is_file(), name
        assert len(sha(file)) == 64
    witness = {
        key: {
            "file": str(file.relative_to(ROOT)),
            "sha256": sha(file),
            "bytes": file.stat().st_size,
        }
        for key, file in PHOTO.items()
    }
    t = text_path.read_text(encoding="utf-8")
    start = t.index("The use of the Table.")
    end = t.find("A most exact Table according", start)
    text = t[start:end] if end >= 0 else t[start:]
    entries = []
    for i, (frame, role, anchor, meaning) in enumerate(CLAIMS):
        k = text.find(anchor)
        assert k >= 0, (role, anchor)
        entries.append(
            {
                "id": f"R{12516 + i}",
                "record_number": 12516 + i,
                "source_pdf_frame_first_1647": frame,
                "source_printed_folio_first_1647": frame - 34,
                "source_group": "B07ai-S001" if frame == 745 else "B07ai-S002",
                "role": role,
                "modern_flattened_source_navigator_anchor_not_diplomatic": anchor,
                "modern_flattened_navigator_char_offset": k,
                "historical_source_meaning_only": meaning,
                "qualification": (
                    "One source reader of original 1647 and independently typeset 1659; "
                    "historical numerical claims are not validated original astronomy "
                    "or verified predictions about actual people."
                ),
                "source_first_edition_image_sha256": witness[
                    "1647_original_printed711" if frame == 745 else "1647_original_printed712"
                ]["sha256"],
                "source_documentary_attested": True,
                "human_event_time_predictive_accuracy_validated": False,
                "original_solar_epoch_natal_calculation_validated": False,
                "high_stakes_prediction_or_personality_advice_permitted": False,
                "runtime_model_promoted": False,
            }
        )
    assert len(entries) == 31
    assert [r["record_number"] for r in entries] == list(range(12516, 12547))
    lookup = {(r["sign"], r["original_zodiac_degree_row"]): r for r in table["rows"]}
    libra7 = lookup["Libra", 7]["literal_original_1647_single_reader_rate_arcminutes_arcseconds"]
    assert libra7 == [54, 25]
    table24 = compute_year_table()
    assert table24[12]["printed_whole_year"] == 13
    assert (
        table24[12]["one_reader_original_1647_printed_accumulated_degree"],
        table24[12]["one_reader_original_1647_printed_remaining_arcminute"],
    ) == (11, 42)
    assert (
        table24[21]["one_reader_original_1647_printed_accumulated_degree"],
        table24[21]["one_reader_original_1647_printed_remaining_arcminute"],
    ) == (19, 48)
    assert table24[-1]["analytical_54_times_years_arcminutes"] == 1296
    day_per_min = Fraction(27, 4)  # exactly 6 days and 18 hours
    examples = []
    for name, target, years, source_print_min, source_print_days in (
        ("Mars_terms", [11, 55], 13, 42, 284),
        ("Mars_opposition", [19, 52], 22, 48, 324),
    ):
        tot = target[0] * 60 + target[1]
        obtained = years * 54
        resid = tot - obtained
        actual_fraction = day_per_min * resid
        alleged_fraction = day_per_min * source_print_min
        examples.append(
            {
                "worked_example": name,
                "target_arc_degrees_minutes": target,
                "whole_years_completed": years,
                "attained_source_table_degrees_minutes": [obtained // 60, obtained % 60],
                "true_arithmetic_remaining_arcminutes": resid,
                "original_printed_fraction_arcminutes": source_print_min,
                "original_printed_fractional_days_rounded": source_print_days,
                "original_statement_one_minute_six_days_eighteen_hours": True,
                "exact_days_per_arcminute": str(day_per_min),
                "source_printed_fraction_exact_days": str(alleged_fraction),
                "mathematical_target_residual_exact_days": str(actual_fraction),
                "difference_exact_nominal_days": str(alleged_fraction - actual_fraction),
                "never_silently_repair_original_printed_source": True,
                "empirically_predicted_life_event": False,
            }
        )
    assert [e["true_arithmetic_remaining_arcminutes"] for e in examples] == [13, 4]
    assert [e["original_printed_fraction_arcminutes"] for e in examples] == [42, 48]
    assert [e["difference_exact_nominal_days"] for e in examples] == [
        str(Fraction(783, 4)),
        str(Fraction(297, 1)),
    ]
    assert Fraction(54) * day_per_min == Fraction(729, 2)  # 364.5 days
    data = {
        "schema": "LILLY_CLXVI_1647_TABLE_USE_PRINT712_MAGINUS_31_SOURCE_RECORDS_V1",
        "batch": "B07ai",
        "source_original_1647_full_PDF_sha256": ORIGINAL_BOOK_SHA,
        "original_source_photo_four_print_witnesses": witness,
        "source_navigator_modern_nonauthoritative_text_SHA256": hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest(),
        "original_source_partial_folios": [711, 712],
        "original_source_pdf_frames": [745, 746],
        "original_24_year_table_source_one_reader_only": True,
        "1647_vs_1659_print_42_48_and_284_324_correspond": True,
        "original_54_arcminutes_per_year_worked_simplification": 54,
        "original_7_libra_annual_table_rate_arcminutes_arcseconds": libra7,
        "original_24_years_source_table": table24,
        "historical_arithmetic_cases": examples,
        "original_one_arcminute_expressly_6d18h": True,
        "exact_54_arcminutes_times_6d18h_is_364_point_5_days": True,
        "original_printed_source_error_unresolved": True,
        "full_original_CLXVI_chapter_complete": False,
        "naibod_actual_degree_minute_tables_source_verified": False,
        "natal_1647_ascendant_and_true_solar_time_engine_validated": False,
        "source_first_second_printing_not_independent_human_test": True,
        "new_historical_annotation_count": len(entries),
        "Lilly_before": 12515,
        "Lilly_if_accepted": 12546,
        "Ptolemy_retained": 1066,
        "Chinese_V5_retained": 262,
        "next_original_R": "R12547",
        "next_original_PDF": 747,
        "actual_real_person_predictions_validated": 0,
        "runtime_promotions": 0,
        "records": entries,
    }
    save(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json", data)
    rules = {
        "batch": "B07ai",
        "status": "FIRST_CLXVI_1647_PRINTED711_TABLE_USE_AND_PRINTED712_MAGINUS_SOURCE",
        "record_count": 31,
        "first_record": "R12516",
        "last_record": "R12546",
        "source_groups": 2,
        "body_pdf_frames": [745, 746],
        "original_table_24_years_54_arcminutes_per_year": True,
        "original_source_42_48_min_not_exact_target_residuals": True,
        "true_arithmetic_remaining_min": [13, 4],
        "original_annual_rate_of_54_min_6d18h_matches_364_point_5_days": True,
        "next_1647_Naibod_table_pdf": 747,
        "original_CLXVI_complete": False,
        "empirical_real_person_validations": 0,
        "runtime_promotions": 0,
        "rules": [
            {
                "id": r["id"],
                "record_number": r["record_number"],
                "batch": "B07ai",
                "source_span": r["source_group"],
                "original_pdf_frames": [r["source_pdf_frame_first_1647"]],
                "role": r["role"],
                "source_anchor_not_diplomatic": r[
                    "modern_flattened_source_navigator_anchor_not_diplomatic"
                ],
                "historical_meaning_only": r["historical_source_meaning_only"],
                "qualification": r["qualification"],
                "historical_source_documented": True,
                "independent_real_event_timing_accuracy_validated": False,
                "independent_health_or_death_prediction_validated": False,
                "independent_relationship_or_financial_prediction_validated": False,
                "independent_faith_personality_or_crime_label_validated": False,
                "original_directions_angle_date_conversion_verified": False,
                "real_person_health_safety_social_status_advice_authorized": False,
                "runtime_model_promoted": False,
            }
            for r in entries
        ],
    }
    save(B / "RULES.json", rules)
    accept = {
        "batch": "B07ai",
        "prior_Lilly": 12515,
        "prior_Ptolemy": 1066,
        "Chinese_V5_retained": 262,
        "new_historical_source_notes": 31,
        "Lilly_if_accepted": 12546,
        "Western_if_accepted": 13612,
        "next_R": "R12547",
        "next_PDF": 747,
        "next_printed_folio": 713,
        "next_source_scope": "Naibod first-edition degree/years/days/hours table printed713–714",
        "original_CLXVI_still_partial": True,
        "original_text_sources_1647_1659_witnessed": True,
        "real_life_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules_SHA256": sha(B / "RULES.json"),
        "original_source_records_SHA256": sha(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json"),
    }
    save(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "records": 31,
                "source_photo_witnesses": 4,
                "years": 24,
                "original_fraction_minutes": [42, 48],
                "true_residual_minutes": [13, 4],
                "literal_minutes_equal_days": "27/4",
                "54_minutes_year_nominal_days": "729/2",
                "next": "R12547",
                "rules_sha256": sha(B / "RULES.json"),
                "records_sha256": sha(B / "TABLE_USE_MAGINUS_SOURCE_RECORDS_V1.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument(
        "--modern-text",
        type=Path,
        default=B / "SECONDARY_NAVIGATOR_WINDOW.txt",
    )
    freeze(cli.parse_args().modern_text)
