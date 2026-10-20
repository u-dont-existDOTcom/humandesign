#!/usr/bin/env python3
"""Original Lilly merchant (1647/1659) printed HOUSE cusps vs Swiss geometry.

This source-only diagnostic starts from source-written RA Midheaven 222°10′
and latitude 53°. It computes modern houses at that meridian RA without
selecting an unknown historical birthplace, longitude, UT, house-event chart
or real personal outcome. Tests compare 8 named Western house systems.

Manual visual source reading from 1647 p742/PDF776 (SHA locked) and
independent typeset 1659 p742/DjVu771 (SHA locked). This is NOT a historical
birth register, complete horoscope, ancient ephemeris or predictive test.
"""

from __future__ import annotations

import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path

import swisseph as swe

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from compute_1616_merchant_swe_parity import (  # noqa: E402
    REFERENCE_CLOCK_UT_HOURS_ASSUMED,
    SENSITIVITY_OFFSETS_HOURS,
    SOURCE_PATH,
    signed_arcminutes,
    validate_ephe_dir,
)

ZODIAC = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
SOURCE_PHOTOS = {
    "1647_first_printed_742": {
        "path": (
            "tasks/astro-source-audit-multipass-20261005/batches/"
            "B07aw/evidence/1647_original-776.jpg"
        ),
        "sha256": "29d25ae08284733e07dc950f7f5b4762e10f2ada3ec2ab866a75bd442aeae760",
    },
    "1659_second_printed_742": {
        "path": (
            "tasks/astro-source-audit-multipass-20261005/batches/"
            "B07aw/evidence/1659_original_djvu_771.jpg"
        ),
        "sha256": "c545d6ffd3da2d2d7bddd30d3fa65342fbea8ef2f85274da5e8d93c86d1a9008",
    },
}
SOURCE_RA_MC_DEG = 222 + 10 / 60
SOURCE_OBLIQUE_ASC_DEG = 312 + 10 / 60
LATITUDE_DEG = 53.0

# Independently visible both physically printed editions. Original diagrams
# label zodiac signs with symbols; original books are NOT an original birth
# register. The values are exact manually read sexagesimal printed glyphs.
SOURCE_HOUSE_CUSPS = {
    "ASC": {"house": 1, "zodiac": "Capricorn", "deg": 6, "arcmin": 37},
    "HOUSE2": {"house": 2, "zodiac": "Aquarius", "deg": 23, "arcmin": 30},
    "HOUSE3": {"house": 3, "zodiac": "Aries", "deg": 18, "arcmin": 34},
    "MC": {"house": 10, "zodiac": "Scorpio", "deg": 14, "arcmin": 39},
}
HOUSE_SYSTEMS = {
    "Regiomontanus": b"R",
    "Placidus": b"P",
    "Campanus": b"C",
    "Alcabitius": b"B",
    "Porphyry": b"O",
    "Equal": b"E",
    "Koch": b"K",
    "Whole_Sign": b"W",
}


def source_photo_fingerprints() -> dict[str, dict[str, object]]:
    witnesses: dict[str, dict[str, object]] = {}
    for key, meta in SOURCE_PHOTOS.items():
        path = ROOT / meta["path"]
        data = path.read_bytes()
        digest = sha256(data).hexdigest()
        if digest != meta["sha256"]:
            raise ValueError(f"Original {key} image hash does not match pinned source")
        witnesses[key] = {
            "source_path": meta["path"],
            "sha256": digest,
            "byte_length": len(data),
            "historical_source": "original physical scan",
            "human_transcribed_manually": True,
            "independently_expert_critical_editional_reading": False,
        }
    return witnesses


def zodiac_absolute_longitude(sign: str, degree: int, arcmin: int) -> float:
    if sign not in ZODIAC:
        raise ValueError("Source zodiac sign not admitted")
    if any(type(x) is not int for x in (degree, arcmin)):
        raise ValueError("Source historical angle must use whole printed minutes")
    if not 0 <= degree < 30 or not 0 <= arcmin < 60:
        raise ValueError("Bad printed whole-degree/minute glyph")
    return ZODIAC.index(sign) * 30 + degree + arcmin / 60


def _all_source_cusps() -> dict[str, float]:
    return {
        name: zodiac_absolute_longitude(
            row["zodiac"], row["deg"], row["arcmin"]
        )
        for name, row in SOURCE_HOUSE_CUSPS.items()
    }


def _calc_true_obliquity_swieph(jd_ut: float) -> tuple[float, int]:
    obliquities, returned = swe.calc_ut(jd_ut, swe.ECL_NUT, swe.FLG_SWIEPH)
    if not returned & swe.FLG_SWIEPH or returned & swe.FLG_MOSEPH:
        raise ValueError(
            "Must verify actual Swiss Ephemeris obliquity flag, not requested flag"
        )
    if not 23 < obliquities[0] < 24:
        raise ValueError("Unexpected original 1616 true Earth axial obliquity")
    return obliquities[0], returned


def _candidate_houses(armc: float, epsilon: float) -> list[dict[str, object]]:
    source = _all_source_cusps()
    all_candidates: list[dict[str, object]] = []
    for method, code in HOUSE_SYSTEMS.items():
        cusps, angles = swe.houses_armc(armc, LATITUDE_DEG, epsilon, code)
        if len(cusps) != 12:
            raise ValueError(f"Unsupported 12-house formula {method}")
        residuals = {}
        for label, printed in source.items():
            house_number = SOURCE_HOUSE_CUSPS[label]["house"]
            calculated = angles[0] if label == "ASC" else (
                angles[1] if label == "MC" else cusps[house_number - 1]
            )
            residuals[label] = {
                "source_first_and_second_printed_longitude_degrees": round(
                    printed, 8
                ),
                "calculated_ecliptic_tropical_longitude_degrees": round(
                    calculated, 8
                ),
                "signed_computed_minus_printed_arcmin": round(
                    signed_arcminutes(calculated, printed), 6
                ),
                "abs_arcmin": round(
                    abs(signed_arcminutes(calculated, printed)), 6
                ),
            }
        max_err = max(row["abs_arcmin"] for row in residuals.values())
        middle = sorted(row["abs_arcmin"] for row in residuals.values())
        all_candidates.append({
            "method": method,
            "swe_house_system_code": code.decode("ascii"),
            "source_4_house_cusps": residuals,
            "max_abs_residual_arcmin": round(max_err, 6),
            "median_abs_residual_arcmin": round((middle[1] + middle[2]) / 2, 6),
            "all_four_cusps_within_ten_arcmin": max_err < 10,
        })
    return all_candidates


def _implied_longitude_as_time_alternatives(jd_ut: float) -> list[dict[str, object]]:
    # RA-MC constrains the sum of Greenwich sidereal time + eastern longitude.
    # This is a one-equation family of solutions, not an independently
    # authenticated birthplace longitude, geographical claim or clock reading.
    rows: list[dict[str, object]] = []
    for offset in SENSITIVITY_OFFSETS_HOURS:
        hour_jd = jd_ut + offset / 24
        greenwich_sid_deg = swe.sidtime(hour_jd) * 15
        east_deg = (SOURCE_RA_MC_DEG - greenwich_sid_deg + 180) % 360 - 180
        rows.append({
            "assumed_printed_clock_mapped_to_UT_offset_hours": offset,
            "greenwich_sidereal_right_ascension_deg": round(
                greenwich_sid_deg, 8
            ),
            "conditional_longitude_east_deg_to_match_original_RA_MC": round(
                east_deg, 8
            ),
            "longitude_is_independently_real_birthplace_observed": False,
        })
    return rows


def compute(ephe_dir: Path) -> dict[str, object]:
    original_photos = source_photo_fingerprints()
    source_positions = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    if source_positions["original_Mercury_natal_longitude"] != [
        "Libra", 3, 34
    ]:
        raise ValueError("Source native source registry drift")
    if abs(SOURCE_RA_MC_DEG + 90 - SOURCE_OBLIQUE_ASC_DEG) > 1e-9:
        raise ValueError("Original recorded RA MC + 90 versus OA Asc inconsistent")

    pinned_ephe = validate_ephe_dir(ephe_dir)
    swe.close()
    swe.set_ephe_path(str(ephe_dir))
    jd_ut = swe.julday(
        1616, 9, 19, REFERENCE_CLOCK_UT_HOURS_ASSUMED, swe.JUL_CAL
    )
    true_obliquity, eps_flags = _calc_true_obliquity_swieph(jd_ut)
    methods = _candidate_houses(SOURCE_RA_MC_DEG, true_obliquity)
    by_method = {row["method"]: row for row in methods}
    reg = by_method["Regiomontanus"]
    if not reg["all_four_cusps_within_ten_arcmin"]:
        raise ValueError("Regiomontanus failed original four house-cusp witness")
    if any(method != "Regiomontanus"
           and candidate["max_abs_residual_arcmin"] <= reg["max_abs_residual_arcmin"]
           for method, candidate in by_method.items()):
        raise ValueError("Unexpected Regiomontanus comparison ranking changed")

    conditional_time_longitudes = _implied_longitude_as_time_alternatives(jd_ut)
    return {
        "title": (
            "Original Lilly English Merchant RA-MC, latitude and four house cusps "
            "vs eight independent modern house methods"
        ),
        "evidence_status": (
            "SOURCE-READING_AND_GEOMETRY_ONLY_NOT_PERSON_REAL_NATAL_OR_FORECAST_VALIDATION"
        ),
        "original_source_editions": original_photos,
        "original_chart_source_record_reference": str(
            SOURCE_PATH.relative_to(ROOT)
        ),
        "source_original_ra_mc_deg_min": [222, 10],
        "source_original_oblique_asc_deg_min": [312, 10],
        "original_oblique_asc_minus_ra_mc": 90,
        "source_original_latitude_deg": LATITUDE_DEG,
        "source_printed_cusps_glyph_reading": SOURCE_HOUSE_CUSPS,
        "source_printed_four_numeric_cusp_longitudes": {
            k: round(v, 8) for k, v in _all_source_cusps().items()
        },
        "original_glyph_reading_method": (
            "Manually inspected exactly hashed original 1647/1659 original page scans; "
            "expert collation still open"
        ),
        "source_period_julian_date_treated_as_hypothesis": [1616, 9, 19],
        "historical_utc_clock_assumed_for_obliquity_only": "14:24:39 UT",
        "original_printed_clock_was_UT_verified": False,
        "original_merchant_geographical_birth_longitude_known": False,
        "requested_obliquity_swieph": True,
        "returned_obliquity_flags": eps_flags,
        "actual_obliquity_swieph_flag": bool(eps_flags & swe.FLG_SWIEPH),
        "calculated_true_obliquity_at_original_julian_date_deg": round(
            true_obliquity, 11
        ),
        "swisseph_version": swe.version,
        "original_2026_DE441_file_binary_witnesses": pinned_ephe,
        "source_ra_mc_supplied_to_all_methods_without_backfitting": SOURCE_RA_MC_DEG,
        "methods": methods,
        "best_correspondence_on_4_development_source_readings": "Regiomontanus",
        "source_specific_house_system_predeclared_independently_blind": False,
        "hypothetical_RA_MC_derived_longitudes_for_5_UT_clocks": conditional_time_longitudes,
        "longitude_is_actual_birthplace": False,
        "houses_derived_without_UT_or_birthplace_after_source_RA_MC_known": True,
        "independently_verified_early_time_or_actual_birthplace": False,
        "independent_prediction_on_unseen_humans": 0,
        "runtime_forecast_promotions": 0,
        "new_accepted_historical_annotation_records": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephe-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compute(args.ephe_dir)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    for row in result["methods"]:
        print(
            "HOUSE", row["method"],
            "max_abs_arcmin", row["max_abs_residual_arcmin"],
            "median_abs_arcmin", row["median_abs_residual_arcmin"],
            "within10", row["all_four_cusps_within_ten_arcmin"]
        )
        if row["method"] == "Regiomontanus":
            for cusp, obs in row["source_4_house_cusps"].items():
                print("CUSP", cusp, obs)
    print("IMPLIED_LONGITUDE_IF_UT_ASSUMPTIONS")
    for row in result["hypothetical_RA_MC_derived_longitudes_for_5_UT_clocks"]:
        print(row)
    print("OUTPUT", args.output)


if __name__ == "__main__":
    main()
