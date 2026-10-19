#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve exact archival file hashes and full source glosses.
"""Independent arithmetic diagnostic of Lilly's seven printed antiscions.

Source readings are manually transcribed separately from computed reflection.
Exactly six of seven match 180-degree solar-axis reflection; both editions
print Mercury natal Libra 3°34 and antiscion Pisces 26°06, whereas reflection
predicts Pisces 26°26. Never silently edit historical first printing.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARENT = B.parent / "B07aw"
ROOT = B.parents[3]
IMAGES = B / "evidence"
SOURCE = B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json"
OUTPUT = B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json"

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
ONE_READER_SOURCE = [
    ("Saturn", ("Taurus", 9, 2), ("Leo", 20, 58), ("Aquarius", 20, 58)),
    ("Jupiter", ("Sagittarius", 21, 55), ("Capricorn", 8, 5), ("Cancer", 8, 5)),
    ("Mars", ("Leo", 0, 54), ("Taurus", 29, 6), ("Scorpio", 29, 6)),
    ("Sun", ("Libra", 6, 37), ("Pisces", 23, 23), ("Virgo", 23, 23)),
    ("Venus", ("Libra", 6, 54), ("Pisces", 23, 6), ("Virgo", 23, 6)),
    ("Mercury", ("Libra", 3, 34), ("Pisces", 26, 6), ("Virgo", 26, 6)),
    ("Moon", ("Gemini", 1, 44), ("Cancer", 28, 16), ("Capricorn", 28, 16)),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def total(x):
    sign, degree, minute = x
    assert sign in SIGNS and type(degree) is int and 0 <= degree < 30
    assert type(minute) is int and 0 <= minute < 60
    return SIGNS.index(sign) * 1800 + degree * 60 + minute


def zodiac(mm):
    x = mm % (360 * 60)
    s, r = divmod(x, 1800)
    d, m = divmod(r, 60)
    return [SIGNS[s], d, m]


def freeze():
    meta = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert meta["status"] == "PHOTO_CHECKPOINT_NOT_YET_CANONICAL_RULES"
    assert meta["next_unaccepted_Lilly_R"] == "R12871"
    expected = {
        "derived_1647_p743_antiscions.png": "60192a1e0345d72a25a2c7c28a35101096375c914ae223ec15da8b7afacda8c1",
        "derived_1659_p743_antiscions.png": "5fcb10b83267feb6d6f5727a6b21fc5020001d853a74acf966693f15a6ab1dbc",
        "derived_1647_p745_mercury_natal.png": "62f4fc8ff262c6ed0a818da54f390c9ec344256de78f86e77b285215ad4aa4cd",
        "derived_1659_p745_mercury_natal.png": "0d1b5e3628f7e39779b7f51d10119079f257ee479e7ca78c39bdbee59b47a0d1",
    }
    for p, v in expected.items():
        assert sha(IMAGES / p) == v, p
    original_binaries = meta["original_source_photographic_witnesses"]
    for s in (1647, 1659):
        for printed in (743, 745):
            key = f"{s}_printed_{printed}"
            row = original_binaries[key]
            assert sha(ROOT / row["file"]) == row["sha256"]
    records = []
    for body, natal, printed, contra in ONE_READER_SOURCE:
        n = total(natal)
        a = (180 * 60 - n) % (360 * 60)
        computed = zodiac(a)
        computed_contra = zodiac(a + 180 * 60)
        delta = total(printed) - a
        if delta > 180 * 60:
            delta -= 360 * 60
        elif delta < -180 * 60:
            delta += 360 * 60
        record = {
            "source_body": body,
            "original_first_1647_and_second_1659_printed_natal_longitude": list(natal),
            "original_first_1647_and_second_1659_printed_antiscion": list(printed),
            "original_first_1647_and_second_1659_printed_contra_antiscion": list(contra),
            "analytic_solar_axis_reflection_antiscion": computed,
            "analytic_solar_axis_reflection_contra_antiscion": computed_contra,
            "printed_antiscion_minus_computed_arcminutes": delta,
            "printed_contra_minus_computed_arcminutes": (
                total(contra) - (a + 180 * 60) % (360 * 60)
            ),
            "source_physical_edition_single_reader_verified": True,
            "transmitted_numerical_error_cause_editorial_proven": False,
            "underlying_real_natal_chart_position_independently_verified": False,
            "may_replace_literal_old_print_in_canonical_original": False,
            "actual_human_mood_fortune_health_predictions_validated": False,
        }
        records.append(record)
    assert len(records) == 7
    assert sum(x["printed_antiscion_minus_computed_arcminutes"] == 0 for x in records) == 6
    merc = next(x for x in records if x["source_body"] == "Mercury")
    assert merc["printed_antiscion_minus_computed_arcminutes"] == -20
    assert merc["analytic_solar_axis_reflection_antiscion"] == ["Pisces", 26, 26]
    assert merc["analytic_solar_axis_reflection_contra_antiscion"] == ["Virgo", 26, 26]
    assert merc["original_first_1647_and_second_1659_printed_antiscion"] == ["Pisces", 26, 6]
    result = {
        "schema": "LILLY_1647_1659_MERCHANT_MERCURY_ANTISCION_20MIN_SOURCE_CONFLICT_V1",
        "batch": "B07ax",
        "status": "SOURCE_CRITICAL_ARITHMETIC_DIAGNOSTIC_NOT_CORRECTED_CHART_ENGINE",
        "original_1647_printed_source_folio_natal_longitude": 745,
        "original_1647_printed_source_folio_antiscion": 743,
        "independently_typeset_1659_same_printed_folios": [743, 745],
        "1647_Wellcome_full_pdf_sha256": meta["original_1647_Wellcome_full_scan_sha256"],
        "source_1647_antiscion_photo_sha256": original_binaries["1647_printed_743"]["sha256"],
        "source_1659_antiscion_photo_sha256": original_binaries["1659_printed_743"]["sha256"],
        "source_1647_natal_Mercury_photo_sha256": original_binaries["1647_printed_745"]["sha256"],
        "source_1659_natal_Mercury_photo_sha256": original_binaries["1659_printed_745"]["sha256"],
        "derived_reading_aid_crop_sha256": expected,
        "historical_source_natal_longitude_chart_recomputed": False,
        "standard_reflection_formula": "(180 degrees minus tropical natal longitude) modulo 360 degrees",
        "analytic_7_body_reflection_matches": 6,
        "analytic_7_body_reflection_mismatches": 1,
        "mismatch_original_body": "Mercury",
        "original_Mercury_natal_longitude": ["Libra", 3, 34],
        "both_printed_editions_Mercury_antiscion": ["Pisces", 26, 6],
        "analytic_expected_Mercury_antiscion": ["Pisces", 26, 26],
        "original_minus_formula_arcminutes": -20,
        "both_printed_editions_Mercury_contra_antiscion": ["Virgo", 26, 6],
        "analytic_expected_Mercury_contra_antiscion": ["Virgo", 26, 26],
        "historical_author_or_compositor_causation_established": False,
        "all_other_6_antiscions_arithmetically_match": True,
        "source_original_tables_preserved_without_interpolation": True,
        "source_not_prospective_independent_birth_chart_validation": True,
        "actual_person_outcomes_predicted_and_verified": 0,
        "astrology_runtime_promotions": 0,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "source_planets": len(records),
                "matched_reflections": 6,
                "Mercury_print": merc["original_first_1647_and_second_1659_printed_antiscion"],
                "Mercury_formula": merc["analytic_solar_axis_reflection_antiscion"],
                "printed_minus_formula_arcminutes": merc[
                    "printed_antiscion_minus_computed_arcminutes"
                ],
                "source_critical_note_SHA256": sha(OUTPUT),
                "human_predictions_validated": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
