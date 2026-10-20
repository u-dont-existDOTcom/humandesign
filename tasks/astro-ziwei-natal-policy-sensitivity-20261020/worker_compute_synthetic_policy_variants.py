#!/usr/bin/env python3
"""Four explicitly fictional civil clocks through pinned original engine.

This worker is called only by the versioned source-checking parent driver.
No freeform input, real persons, interpretations or astrology predictions.
"""

from __future__ import annotations

import json

import dual_witness_civil_lunar as lunar
import explicit_natal_time as natal

CALENDARS = natal.CALENDAR_DATE_POLICIES
HOURS = natal.HOUR_POLICIES
LEAPS = natal.LEAP_MONTH_POLICIES
FICTITIOUS = (
    ("SYNTH_WEST_AFRICA_LUNAR_NEW_YEAR", "2026-02-16T21:30:00", "Africa/Dakar", "-17.4"),
    ("SYNTH_HONG_KONG_LEAP_FIRST_DAY", "2023-03-22T12:00:00", "Asia/Hong_Kong", "114.17"),
    ("SYNTH_NEW_YORK_DATE_CROSSING", "2026-10-20T13:30:00", "America/New_York", "-74"),
    ("SYNTH_HONG_KONG_HISTORICAL_DST", "1965-07-01T00:30:00", "Asia/Hong_Kong", "114.17"),
)
STARS = {"WuQu", "LianZhen", "TianLiang", "PoJun"}
HKO = {
    "2023-03-21",
    "2023-03-22",
    "2023-04-19",
    "2023-04-20",
    "2025-07-25",
    "2026-02-16",
    "2026-02-17",
    "2026-10-20",
    "2027-02-06",
    "2028-01-01",
}
SOURCE_LEAP = "transmitted_quan_shu_as_next"


def exact_chart(clock, zone, longitude, calendar, hour, leap):
    return natal.fourteen_stars_from_explicit_civil_birth(
        clock,
        zone,
        fold=None,
        calendar_day_policy=calendar,
        hour_time_policy=hour,
        longitude_east_degrees=longitude,
        late_zi_day_policy="midnight_day_boundary",
        recorded_clock_uncertainty_seconds=0,
        lunar_year_boundary_policy=natal.BIRTH_CALENDAR_BOUNDARY,
        leap_month_policy=leap,
        documented_nayin_emendations=True,
        documented_diagram_corrections=True,
    )


def lunar_tuple(src):
    return (src.year, src.month, src.day, src.is_leap_month)


def record(q, calendar, hour, leap):
    c = q.clock
    source = q.official_chinese_lunar_date
    original = q.principal_stars
    if original.stars is None or len(original.stars) != 14:
        raise ValueError("Bounded full 14 major-star mechanical placements unavailable")
    life = original.partial_natal.life_palace
    body = original.partial_natal.body_palace
    major = tuple(sorted(original.placements_by_palace[life]))
    anchor = tuple(sorted(set(major) & STARS))
    if not anchor:
        status = "ABSTAIN_NO_SELECTED_SOURCE_STAR"
    elif len(anchor) > 1:
        status = "ABSTAIN_TWO_SOURCE_ANCHOR_STARS"
    elif len(major) > 1:
        status = "ABSTAIN_OTHER_SOURCE_MAJOR_STAR_PRESENT"
    else:
        status = "SOURCE_STAR_ALONE_NO_FULL_BIRTH_ENGINE_EXTERNAL_PARITY"
    if c.selected_chinese_calendar_day in HKO:
        H = lunar.frozen_hko_example(c.selected_chinese_calendar_day)
        if lunar_tuple(H) != lunar_tuple(source):
            raise ValueError("Pinned original HKO lunar date differs from two software clocks")
        witness = "INDEPENDENT_HKO_SOURCE_JSON_SHA_PLUS_TWO_SOFTWARE_CALENDARS"
    else:
        witness = "DUAL_SOFTWARE_CALENDARS_ONLY_NO_PINNED_HKO_SOURCE"
    return {
        "calendar_reference_policy": calendar,
        "birth_hour_policy": hour,
        "leap_month_school_policy": leap,
        "actual_real_birth_data": False,
        "fictitious_local_clock_historic_format": c.birth_local_clock,
        "fictitious_birth_zone": c.birth_iana_timezone,
        "birthplace_longitude_east_degrees_for_hour_sensitivity_only": c.longitude_east_degrees,
        "UTC_instant": c.birth_utc_instant,
        "zoneinfo_TZif_SHA256": c.tzif_sha256,
        "selected_chinese_calendar_day": c.selected_chinese_calendar_day,
        "selected_hour_Earthly_Branch": c.selected_hour_branch,
        "birth_site_civil_day": c.birthplace_civil_calendar_day,
        "same_instant_fixed_UTC8_day": c.same_instant_fixed_utc_plus_8_calendar_day,
        "original_lunar_year": source.year,
        "original_lunar_month": source.month,
        "original_lunar_day": source.day,
        "original_is_leap_month": source.is_leap_month,
        "calendar_witness_quality": witness,
        "source_14_major_stars_status": original.status,
        "source_principal_life_palace": life,
        "source_principal_body_palace": body,
        "life_palace_major_stars": list(major),
        "selected_four_source_anchor_stars_in_life": list(anchor),
        "conservative_behavioral_trait_applicability_status": status,
        "complete_14_main_star_placement_sha256_NOT_behaviour_proof": None,
        "all_14_principal_star_locations": dict(original.stars),
        "is_complete_Zi_Wei_chart": False,
        "is_actual_ordinary_human_behavioral_prediction": False,
    }


def one_policy_grid(name, clock, zone, lon):
    rows = []
    for day in CALENDARS:
        for hour in HOURS:
            for leap in LEAPS:
                q = exact_chart(clock, zone, lon, day, hour, leap)
                rows.append(record(q, day, hour, leap))
    source_rows = [r for r in rows if r["leap_month_school_policy"] == SOURCE_LEAP]
    if len(rows) != 12 or len(source_rows) != 4:
        raise ValueError("Explicit day/hour/leap policy grid size changed")
    distinct_full = {
        (
            r["original_lunar_year"],
            r["original_lunar_month"],
            r["original_lunar_day"],
            r["selected_hour_Earthly_Branch"],
            r["source_principal_life_palace"],
            tuple(sorted(r["all_14_principal_star_locations"].items())),
        )
        for r in rows
    }
    original_four = {
        (
            r["selected_chinese_calendar_day"],
            r["selected_hour_Earthly_Branch"],
            r["source_principal_life_palace"],
            tuple(r["life_palace_major_stars"]),
        )
        for r in source_rows
    }
    original_anchor = {tuple(r["selected_four_source_anchor_stars_in_life"]) for r in source_rows}
    return {
        "case_id": name,
        "source_clock_is_entirely_fictitious": True,
        "case_fixture_local_clock": clock,
        "case_fixture_zone": zone,
        "case_fixture_longitude": lon,
        "sensitivity_only_not_selected_traditional_school_for_real_people": True,
        "policy_cases": rows,
        "policy_count": len(rows),
        "source_original_leap_grid_distinct_life_plus_clock_configurations": len(original_four),
        "all_twelve_policy_variants_distinct_major_star_charts": len(distinct_full),
        "source_original_leap_grid_distinct_selected_anchor_sets": len(original_anchor),
        "source_original_calendar_hour_policy_invariant_full_configuration": len(original_four)
        == 1,
        "source_original_calendar_hour_policy_invariant_selected_anchor_set": len(original_anchor)
        == 1,
        "complete_real_person_astro_predictions": 0,
    }


def failures():
    base = dict(
        birth_local_clock="2026-02-16T21:30:00",
        birth_iana_timezone="Africa/Dakar",
        fold=None,
        calendar_day_policy=CALENDARS[0],
        hour_time_policy=HOURS[0],
        longitude_east_degrees="-17.4",
        late_zi_day_policy="midnight_day_boundary",
        recorded_clock_uncertainty_seconds=0,
        lunar_year_boundary_policy=natal.BIRTH_CALENDAR_BOUNDARY,
        leap_month_policy=SOURCE_LEAP,
        documented_nayin_emendations=True,
        documented_diagram_corrections=True,
    )
    cases = {
        "2057_calendar_conflict": {
            "birth_local_clock": "2057-09-28T12:00:00",
            "birth_iana_timezone": "Asia/Hong_Kong",
        },
        "new_york_dst_spring_gap": {
            "birth_local_clock": "2026-03-08T02:30:00",
            "birth_iana_timezone": "America/New_York",
        },
        "new_york_dst_fall_fold_missing": {
            "birth_local_clock": "2026-11-01T01:30:00",
            "birth_iana_timezone": "America/New_York",
        },
        "birth_time_uncertainty_unresolved": {"recorded_clock_uncertainty_seconds": 60},
        "unsupported_23h_Zi_day": {"late_zi_day_policy": "Zi-day-starts-23"},
        "unsupported_apparent_solar": {"hour_time_policy": "apparent_solar"},
        "unsupported_LiChun_year": {"lunar_year_boundary_policy": "LiChun"},
    }
    result = []
    for name, changes in cases.items():
        kw = {**base, **changes}
        try:
            natal.fourteen_stars_from_explicit_civil_birth(**kw)
        except (natal.NatalTimeResolutionError, lunar.CalendarParityError) as exc:
            result.append(
                {
                    "case_id": name,
                    "expected_fail_closed": True,
                    "actual_failed_closed": True,
                    "failure_class": type(exc).__name__,
                    "failure_message": str(exc),
                    "real_human_chart_resolved": False,
                }
            )
        else:
            raise ValueError("Unsafe unsupported input silently produced a natal chart: " + name)
    return result


def main():
    results = [one_policy_grid(*c) for c in FICTITIOUS]
    errors = failures()
    return {
        "schema": "ZI_WEI_PINNED_EXPLICIT_CIVIL_BIRTH_TIME_POLICY_SYNTHETIC_V1",
        "status": "SOURCE_PINNED_MECHANICAL_CLOCK_CALENDAR_SENSITIVITY_NOT_HUMAN_PREDICTIONS",
        "original_transmitted_Source_imprint_critically_authenticated": False,
        "fourteen_principal_star_engine_complete_natal_horoscope": False,
        "sampled_times_are_actual_birth_records": False,
        "fictitious_independent_test_clocks": len(results),
        "calendar_policy_variants": list(CALENDARS),
        "hour_policy_variants": list(HOURS),
        "lunar_leap_school_variants": list(LEAPS),
        "distinct_test_policy_variants_per_clock": 12,
        "source_as_next_always_used_for_primary_mechanical_comparison": True,
        "lunar_year_boundary": "Chinese Lunar New Year, NOT BaZi Li Chun",
        "original_11pm_Zi_day_start_supported": False,
        "true_apparent_solar_time_supported": False,
        "nonzero_clock_uncertainty_supported": False,
        "actual_human_natal_test_count": 0,
        "empirically_validated_astrology_traits": 0,
        "astrological_runtime_promotions": 0,
        "cases": results,
        "unsupported_conditions_fail_closed": errors,
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
