#!/usr/bin/env python3
"""Lilly 1646 historic CLXXII Sun return source vs verified modern Swiss Sun.

Lilly knew the native; this is source astronomy/interpolation diagnostics only.
Clock, longitude and historical Frankfurt meridian time are unresolved.
Nominal 12:00 UT for written 1646 September 19 is illustrative, never the
claim that Origanus's noon was UT. Old 21:43 is HOUSE-TABLE quantity, NOT UT.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import swisseph as swe

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from compute_1616_merchant_swe_parity import (  # noqa: E402
    REFERENCE_CLOCK_UT_HOURS_ASSUMED,
    signed_arcminutes,
    validate_ephe_dir,
)
from compute_1616_merchant_swe_parity import (  # noqa: E402
    SOURCE_PATH as OLD_NATAL_WITNESS,
)

SOLAR_SOURCE = (
    ROOT
    / "tasks/astro-source-audit-multipass-20261005/batches/"
    "B07at/ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json"
)
NOMINAL_RETURN_DATE = (1646, 9, 19)
NATAL_DATE = (1616, 9, 19)
FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
BRACKET_HOURS_AFTER_NOON = (-12, 24)
MAX_ROOT_ITERATIONS = 65
ROOT_TOLERANCE_SECONDS = 0.002
EXPECTED_SOURCE_KEYS = ("original_1647_printed735", "independent_1659_printed735")


def source_witness() -> tuple[dict[str, object], dict[str, object], str]:
    blob = SOLAR_SOURCE.read_bytes()
    data = json.loads(blob)
    literal = data["original_1646_literal_versus_computed_arithmetic"]
    if [data["original_full_1647_book_PDF_SHA256"],
        literal["original_natal_longitude_sign"],
        literal["original_natal_longitude_deg_min"],
        literal["original_ephemeris_noon_deg_min"]] != [
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
            "Libra", [6, 37], [6, 12]
    ]:
        raise ValueError("Historical original solar-return source changed")
    witnesses: dict[str, object] = {}
    for key in EXPECTED_SOURCE_KEYS:
        w = data["documentary_witness_photos"][key]
        path = ROOT / w["repository_path"]
        raw = path.read_bytes()
        if sha256(raw).hexdigest() != w["raw_image_SHA256"] or len(raw) != w["raw_image_bytes"]:
            raise ValueError(f"Original 1647/1659 solar return photo SHA/bytes changed: {key}")
        witnesses[key] = {
            "repository_path":w["repository_path"],
            "sha256":w["raw_image_SHA256"],
            "bytes":w["raw_image_bytes"],
            "physical_original_source_perspective":key,
        }
    return literal, witnesses, sha256(blob).hexdigest()


def sun_at_jd(jd_ut: float) -> tuple[float, float, int]:
    result, return_flags = swe.calc_ut(jd_ut, swe.SUN, FLAGS)
    if not return_flags & swe.FLG_SWIEPH or return_flags & swe.FLG_MOSEPH:
        raise ValueError("Swiss ephemeris requested but true return flags show fallback")
    return result[0] % 360, result[3], return_flags


def crossing_of_target(
    noon_jd_ut: float, target_lon_degrees: float
) -> dict[str, object]:
    """Bracket and bisect Sun's tropical ecliptic longitude near solar return.

    No root-search optimization over historical clock/city or life outcomes;
    only an original or modern PREDEFINED solar ecliptic longitude target.
    """
    if not 180 <= target_lon_degrees <= 210:
        raise ValueError("1646 source longitude must be in tropical Libra")
    a = noon_jd_ut + BRACKET_HOURS_AFTER_NOON[0] / 24
    b = noon_jd_ut + BRACKET_HOURS_AFTER_NOON[1] / 24
    lon_a, _, flags_a = sun_at_jd(a)
    lon_b, _, flags_b = sun_at_jd(b)
    if not lon_a < target_lon_degrees < lon_b:
        raise ValueError("Solar target not bracketed around nominal 1646 Julian date")
    for _i in range(MAX_ROOT_ITERATIONS):
        midpoint = (a + b) / 2
        midlon, _, flags = sun_at_jd(midpoint)
        if midlon < target_lon_degrees:
            a = midpoint
        else:
            b = midpoint
        if (b - a) * 86400 < ROOT_TOLERANCE_SECONDS:
            break
    root_jd=(a+b)/2
    longitude, velocity_degday, returned = sun_at_jd(root_jd)
    if abs(longitude - target_lon_degrees) * 60 > 0.0001:
        raise ValueError("Bisection did not solve solar return angular root")
    jdcalendar = swe.revjul(root_jd, swe.JUL_CAL)
    gregcal=swe.revjul(root_jd,swe.GREG_CAL)
    return {
        "crossing_JD_UT":round(root_jd,11),
        "target_original_or_modern_tropical_longitude_degrees":round(target_lon_degrees,9),
        "longitude_at_computed_crossing_degrees":round(longitude,9),
        "sun_daily_speed_arcmin_per_day_at_crossing":round(velocity_degday*60,8),
        "hours_after_1646_09_19_Julian_noon_assumed_UT":round((root_jd-noon_jd_ut)*24,8),
        "source_day_is_Julian_not_modern_Gregorian":True,
        "julian_calendar_root_date_time": {
            "year":int(jdcalendar[0]),"month":int(jdcalendar[1]),
            "day":int(jdcalendar[2]),"hour_decimal_UT_assumed":round(jdcalendar[3],8),
        },
        "gregorian_calendar_root_date_time": {
            "year":int(gregcal[0]),"month":int(gregcal[1]),
            "day":int(gregcal[2]),"hour_decimal_UT_assumed":round(gregcal[3],8),
        },
        "search_iterations_max":MAX_ROOT_ITERATIONS,
        "returned_swieph":bool(returned&swe.FLG_SWIEPH),
        "returned_moshier":bool(returned&swe.FLG_MOSEPH),
        "historical_observed_return_clock_verified":False,
    }


def compute(ephe_dir: Path) -> dict[str, object]:
    literal, photos, source_sha = source_witness()
    natal=json.loads(OLD_NATAL_WITNESS.read_text(encoding="utf-8"))
    if natal["original_Mercury_natal_longitude"] != ["Libra",3,34]:
        raise ValueError("Original 1616 chart witness drift")
    files=validate_ephe_dir(ephe_dir)
    swe.close()
    swe.set_ephe_path(str(ephe_dir))
    jd_noon_jul=swe.julday(*NOMINAL_RETURN_DATE,12,swe.JUL_CAL)
    jd_noon_greg=swe.julday(*NOMINAL_RETURN_DATE,12,swe.GREG_CAL)
    noon_jul_lon,noon_jul_speed,noon_jul_flags=sun_at_jd(jd_noon_jul)
    noon_greg_lon,noon_greg_speed,noon_greg_flags=sun_at_jd(jd_noon_greg)
    jd_natal_jul=swe.julday(*NATAL_DATE,REFERENCE_CLOCK_UT_HOURS_ASSUMED,swe.JUL_CAL)
    modern_natal_sun,modern_natal_speed,natal_retflag=sun_at_jd(jd_natal_jul)
    original_natal_lon=180+literal["original_natal_longitude_deg_min"][0]+literal["original_natal_longitude_deg_min"][1]/60
    original_1646_noon=180+literal["original_ephemeris_noon_deg_min"][0]+literal["original_ephemeris_noon_deg_min"][1]/60
    assert abs(original_natal_lon-(180+6+37/60))<1e-10
    if abs(noon_jul_lon-original_1646_noon)*60<1.0:
        raise ValueError("Expected independent original-vs-modern longitude difference lost")
    source_lookup_seconds=(
        3600*literal["twenty_arcminute_time_hms"][0]
        +60*literal["twenty_arcminute_time_hms"][1]
        +literal["twenty_arcminute_time_hms"][2]
        +3600*literal["five_arcminute_time_hms"][0]
        +60*literal["five_arcminute_time_hms"][1]
        +literal["five_arcminute_time_hms"][2]
    )
    printed_exact_seconds=(
        3600*literal["source_sum_unrounded_time_hms"][0]
        +60*literal["source_sum_unrounded_time_hms"][1]
        +literal["source_sum_unrounded_time_hms"][2]
    )
    if source_lookup_seconds!=printed_exact_seconds:
        raise ValueError("Printed original source 20′+5′ original interpolation sum mismatches")
    source_rounded_minutes=(printed_exact_seconds//60)
    if source_rounded_minutes!=10*60+8:
        raise ValueError("Printed source truncation is not 10h08m")
    old_rate_table=literal["historical_nearby_table_rate_arcminute_arcsecond"]
    source_25_min_arc_fraction=Fraction(25,1)/Fraction(
        60*old_rate_table[0]+old_rate_table[1],60
    )
    source_25min_time_seconds_exact=float(source_25_min_arc_fraction)*86400
    modern_old_source_target=crossing_of_target(jd_noon_jul,original_natal_lon)
    modern_true_natal_target=crossing_of_target(jd_noon_jul,modern_natal_sun)
    original_source_clock_if_UT_root_hour=12+source_lookup_seconds/3600
    modern_noon_rate_arcminsec=(
        int(noon_jul_speed*60),
        (noon_jul_speed*60-int(noon_jul_speed*60))*60
    )
    comparison={
        "original_source_ephemeris_nominal_calendar_date":list(NOMINAL_RETURN_DATE),
        "calendar_independent_year_month_day_old_style_verified":False,
        "source_sun_noon_longitude_deg":round(original_1646_noon,9),
        "source_sun_natal_longitude_deg":round(original_natal_lon,9),
        "source_printed_noon_to_natal_arcmin":literal["remaining_arcminutes"],
        "source_daily_sun_motion_arcmin_arcsec":literal["source_sun_daily_motion_arcminute_arcsecond"],
        "source_Maginus_nearby_rate_arcmin_arcsec":old_rate_table,
        "modern_Julian_date_noon_UT_sun_longitude_deg":round(noon_jul_lon,9),
        "modern_Gregorian_date_noon_UT_sun_longitude_deg":round(noon_greg_lon,9),
        "modern_Julian_noon_sun_degree_in_tropical_Libra":round(noon_jul_lon-180,9),
        "modern_Julian_noon_minus_old_ephemeris_noon_arcmin":round(
            signed_arcminutes(noon_jul_lon, original_1646_noon),8
        ),
        "modern_noon_Julian_daily_rate_arcmin_per_day":round(noon_jul_speed*60,9),
        "modern_noon_Julian_daily_rate_arcmin_arcsecond":[
            modern_noon_rate_arcminsec[0],round(modern_noon_rate_arcminsec[1],7)
        ],
        "source_Maginus_rate_minus_modern_noon_rate_arcsec":round(
            old_rate_table[1] + old_rate_table[0]*60 - noon_jul_speed*3600,
            7
        ),
        "source_daily_motion_minus_modern_noon_rate_arcsec":round(
            literal["source_sun_daily_motion_arcminute_arcsecond"][1]
            + literal["source_sun_daily_motion_arcminute_arcsecond"][0]*60
            - noon_jul_speed*3600,
            7
        ),
        "source_time_20_arcmin_hms":literal["twenty_arcminute_time_hms"],
        "source_time_5_arcmin_hms":literal["five_arcminute_time_hms"],
        "source_time_addition_seconds":source_lookup_seconds,
        "source_time_exact_sum_hms":literal["source_sum_unrounded_time_hms"],
        "source_truncated_clock_hm":literal["printed_later_minute_level_time_hm"],
        "source_time_by_exact_25_over_Maginus_59_08_rate_seconds":round(
            source_25min_time_seconds_exact,4
        ),
        "source_printed_10h08m47_if_UT_interpreted_as_HHMMSS": [
            int(original_source_clock_if_UT_root_hour),
            int((original_source_clock_if_UT_root_hour%1)*60),
            47
        ],
        "source_after_westward_meridian_subtraction_minutes": [
            literal["source_westward_meridian_subtract_hm"][0],
            literal["source_westward_meridian_subtract_hm"][1]
        ],
        "source_house_table_final_hm_NOT_UT":literal["source_house_table_final_hm"],
        "source_house_table_final_is_not_a_direct_astronomical_UT_datetime":True,
        "modern_sun_when_original_source_6deg37_target_crossed":modern_old_source_target,
        "modern_1616_Julian_natal_at_assumed_UT_Sun_longitude_degrees":round(
            modern_natal_sun,9
        ),
        "modern_sun_when_modern_natal_Julian_1616_target_crossed":modern_true_natal_target,
        "modern_crossing_modern_natal_minus_crossing_old_natal_arcminutes":round(
            signed_arcminutes(modern_natal_sun,original_natal_lon),6
        ),
        "nominal_1646_source_clock_UT_equivalence_unverified":True,
        "daily_rate_parity_does_not_prove_noon_original_longitude_or_return_clock":True,
    }
    if not all(
        flag & swe.FLG_SWIEPH
        for flag in (noon_jul_flags, noon_greg_flags, natal_retflag)
    ):
        raise ValueError("Modern source Sun calculation returned bad flags")
    report={
        "title": (
            "Lilly original 1646 September 19 CLXXII Sun return: old source "
            "daily interpolation vs true Swiss DE441 solar longitude and crossing"
        ),
        "status":"SOURCE-ASTRONOMY-AND-TIMING-CALCULATION_ONLY; NO_HUMAN_PREDICTIVE_VALIDATION",
        "source_original_review": (
            "1647 first and 1659 second original printed735; "
            "source anchor images already stored"
        ),
        "source_B07at_index_file":str(SOLAR_SOURCE.relative_to(ROOT)),
        "original_B07at_source_file_SHA256":source_sha,
        "source_original_1647_1659_photo_witnesses":photos,
        "source_original_day_solar_interpolation_values":literal,
        "swisseph_library_version":swe.version,
        "ephe_files_verified_outside_repo":files,
        "solar_calculation_flags_request":FLAGS,
        "solar_calculation_return_flags":[noon_jul_flags,noon_greg_flags,natal_retflag],
        "every_modern_solar_longitude_actual_swieph":True,
        "no_moshier_fallback":True,
        "reference_clock_unverified": (
            "1646-09-19 12h UT is an analytic assumption, "
            "NOT original Frankfurt clock"
        ),
        "original_17th_century_local_UT_and_date_style_resolved":False,
        "source_known_merchant_retrospective_only":True,
        "solar_return_source_modern_comparison":comparison,
        "historic_birth_certificate_and_source_UT_unverified":True,
        "historically_exact_revolution_and_house_timings_authenticated":False,
        "retrospective_merchant_study_not_blind":True,
        "independently_scored_blind_actual_humans":0,
        "runtime_astrology_promotions":0,
        "new_historical_source_annotation_ids":0,
    }
    return report


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--ephe-dir",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    data=compute(args.ephe_dir)
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    c=data["solar_return_source_modern_comparison"]
    print("SOURCE 1646 NOON",c["source_sun_noon_longitude_deg"],
          "MODERN SWISS",c["modern_Julian_date_noon_UT_sun_longitude_deg"],
          "RESIDUAL_ARCMIN",c["modern_Julian_noon_minus_old_ephemeris_noon_arcmin"])
    print("SOURCE 59'08 sec vs modern",c["modern_noon_Julian_daily_rate_arcmin_arcsecond"],
          "DIFF_ARCSEC",c["source_Maginus_rate_minus_modern_noon_rate_arcsec"])
    print("SOURCE TABLE RETURN",c["source_time_exact_sum_hms"])
    for name in (
        "modern_sun_when_original_source_6deg37_target_crossed",
        "modern_sun_when_modern_natal_Julian_1616_target_crossed"
    ):
        print("CROSSING",name,c[name])
    print("SAVED",args.output)


if __name__=="__main__":
    main()
