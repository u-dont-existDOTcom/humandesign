#!/usr/bin/env python3
"""Synthetic recorded local clock ± explicit seconds -> all valid UTC instants.

DST fold: include BOTH legal UTC instants. DST gap: record every invalid
local wall-clock second, reject prediction use; never roll a missing clock.
All valid UTC instants are regrouped into exact contiguous UTC ranges and
fed to the PREVIOUS SHA-PINNED original engine's six-interval source checker.

No real participant birth records, no actual astrological personal predictions.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import explicit_natal_time as natal
import worker_synthetic_utc_interval_states as prior

MAX_WALL_CLOCK_SECONDS = 301
MOCK_CASES = (
    {
        "case_id": "SYNTH_NY_FALL_FOLD_LOCAL_0130",
        "local_center": "2026-11-01T01:30:00",
        "uncertainty_seconds": 90,
        "fictional_iana_zone": "America/New_York",
        "fictional_explicit_east_longitude": "-74",
    },
    {
        "case_id": "SYNTH_NY_SPRING_GAP_PARTIAL_LOCAL_0200",
        "local_center": "2026-03-08T02:00:00",
        "uncertainty_seconds": 90,
        "fictional_iana_zone": "America/New_York",
        "fictional_explicit_east_longitude": "-74",
    },
    {
        "case_id": "SYNTH_NY_SPRING_GAP_ALL_LOCAL_0230",
        "local_center": "2026-03-08T02:30:00",
        "uncertainty_seconds": 60,
        "fictional_iana_zone": "America/New_York",
        "fictional_explicit_east_longitude": "-74",
    },
    {
        "case_id": "SYNTH_DAKAR_LUNAR_NEW_YEAR_LOCAL_2100",
        "local_center": "2026-02-16T21:00:00",
        "uncertainty_seconds": 90,
        "fictional_iana_zone": "Africa/Dakar",
        "fictional_explicit_east_longitude": "-17.4",
    },
    {
        "case_id": "SYNTH_HK_HISTORIC_DST_LOCAL_005930",
        "local_center": "1965-07-01T00:59:30",
        "uncertainty_seconds": 90,
        "fictional_iana_zone": "Asia/Hong_Kong",
        "fictional_explicit_east_longitude": "114.17",
    },
    {
        "case_id": "SYNTH_HK_2023_LEAP_LOCAL_125930",
        "local_center": "2023-03-22T12:59:30",
        "uncertainty_seconds": 90,
        "fictional_iana_zone": "Asia/Hong_Kong",
        "fictional_explicit_east_longitude": "114.17",
    },
)


def fail(reason: str):
    raise ValueError("Original-source synthetic wall-clock UTC set rejected: " + reason)


def checked_wall_case(case: dict) -> tuple[datetime, datetime, ZoneInfo]:
    if set(case) != {
        "case_id",
        "local_center",
        "uncertainty_seconds",
        "fictional_iana_zone",
        "fictional_explicit_east_longitude",
    }:
        fail("synthetic-only case requires exact five approved fields, no private birth details")
    if not case["case_id"].startswith("SYNTH_"):
        fail("only explicitly fictional case labels allowed")
    seconds = case["uncertainty_seconds"]
    if type(seconds) is not int or seconds < 0 or 2 * seconds + 1 > MAX_WALL_CLOCK_SECONDS:
        fail("finite synthetic local second margin out of bounds")
    center = natal._parse_birth_clock(case["local_center"])
    zone = natal._get_zone(case["fictional_iana_zone"])
    natal._longitude_to_solar_offset(case["fictional_explicit_east_longitude"])
    return center - timedelta(seconds=seconds), center + timedelta(seconds=seconds), zone


def utc_candidates_for_local_second(naive: datetime, zone: ZoneInfo) -> list[dict]:
    result = []
    seen = set()
    for fold in (0, 1):
        aware = naive.replace(tzinfo=zone, fold=fold)
        utc = aware.astimezone(UTC)
        back = utc.astimezone(zone)
        # The fold check is essential: an ordinary hour must not acquire a
        # duplicate UTC instant solely by trying fold=1.
        if back.replace(tzinfo=None) != naive or back.fold != fold:
            continue
        if utc in seen:
            continue
        checked, original_fold = natal._disambiguate_local_clock(naive, zone, fold)
        if checked.astimezone(UTC) != utc or original_fold != fold:
            fail("Original source PEP-495 clock bridge inconsistent with UTC candidate")
        seen.add(utc)
        result.append(
            {
                "UTC_instant": utc.isoformat(timespec="seconds"),
                "local_wall_second": naive.isoformat(timespec="seconds"),
                "recorded_wall_fold": fold,
                "historical_zone_UTC_offset_seconds": int(aware.utcoffset().total_seconds()),
            }
        )
    return result


def connected_UTC_groups(instants: list[datetime]) -> list[tuple[datetime, datetime]]:
    if not instants:
        return []
    if sorted(set(instants)) != instants:
        fail("UTC instants must be sorted and unique before connected-component analysis")
    result = []
    start = last = instants[0]
    for instant in instants[1:]:
        if (instant - last).total_seconds() == 1:
            last = instant
        else:
            result.append((start, last))
            start = last = instant
    result.append((start, last))
    if sum(int((b - a).total_seconds()) + 1 for a, b in result) != len(instants):
        fail("not all UTC instants are represented in connected components")
    return result


def run_wall_case(case: dict) -> dict:
    start, end, zone = checked_wall_case(case)
    local_count = int((end - start).total_seconds()) + 1
    nonexistent = []
    choices = []
    for offset in range(local_count):
        wall = start + timedelta(seconds=offset)
        possible = utc_candidates_for_local_second(wall, zone)
        if not possible:
            nonexistent.append(wall.isoformat(timespec="seconds"))
        choices.extend(possible)
    utc_to_choice = {}
    for c in choices:
        if c["UTC_instant"] in utc_to_choice:
            fail("duplicate UTC instant from two supposedly different local seconds")
        utc_to_choice[c["UTC_instant"]] = c
    sorted_instants = sorted(datetime.fromisoformat(s) for s in utc_to_choice)
    pieces = connected_UTC_groups(sorted_instants)
    if nonexistent and len(nonexistent) == local_count:
        resolution_status = "REJECT_ALL_LOCAL_WALL_TIMES_NONEXISTENT"
    elif nonexistent:
        resolution_status = "ABSTAIN_PARTIAL_LOCAL_WALL_CLOCK_GAP"
    elif len(sorted_instants) > local_count:
        resolution_status = "ALL_VALID_BOTH_DST_FOLDS_PRESERVED_SOURCE_ONLY"
    else:
        resolution_status = "EXACT_VALID_LOCAL_WALL_SECONDS_SOURCE_ONLY"
    source_groups = []
    for i, (a, b) in enumerate(pieces, 1):
        segment = {
            "case_id": case["case_id"] + f"_UTC_COMPONENT_{i:02d}",
            "start_UTC": a.isoformat(timespec="seconds"),
            "end_UTC": b.isoformat(timespec="seconds"),
            "fictional_iana_zone": case["fictional_iana_zone"],
            "fictional_explicit_east_longitude": case["fictional_explicit_east_longitude"],
        }
        computed = prior.summarize_interval(segment)
        source_groups.append(computed)
    if sum(g["total_original_UTC_integer_second_inclusive_samples"] for g in source_groups) != len(
        sorted_instants
    ):
        fail("source chart policy interval union lost an original UTC instant")
    distinct_stars = {
        state_hash: record
        for group in source_groups
        for state_hash, record in group["all_original_unique_source_state_details"].items()
    }
    distinct_labels = {
        r["strict_methodological_source_trait_status"] for r in distinct_stars.values()
    }
    full_mechanics_same = len(distinct_stars) == 1
    status_same = len(distinct_labels) == 1
    usable_mechanics = not nonexistent and full_mechanics_same
    return {
        **case,
        "artificial_local_wall_window_start": start.isoformat(timespec="seconds"),
        "artificial_local_wall_window_end": end.isoformat(timespec="seconds"),
        "fictitious_ordinary_person_birth_data": False,
        "original_local_clock_interval_length_seconds": local_count,
        "nonexistent_local_clock_second_count": len(nonexistent),
        "nonexistent_local_clock_seconds": nonexistent,
        "valid_local_clock_second_count": local_count - len(nonexistent),
        "ambiguous_local_clock_second_count": sum(
            1
            for o in range(local_count)
            if (len(utc_candidates_for_local_second(start + timedelta(seconds=o), zone)) == 2)
        ),
        "valid_UTC_candidate_instants_including_both_DST_folds": len(sorted_instants),
        "all_valid_local_wall_to_UTC_candidates": choices,
        "disjoint_exact_contiguous_UTC_components": [
            {
                "start_UTC": a.isoformat(timespec="seconds"),
                "end_UTC": b.isoformat(timespec="seconds"),
                "whole_UTC_second_count": int((b - a).total_seconds()) + 1,
            }
            for a, b in pieces
        ],
        "number_of_separate_UTC_components": len(pieces),
        "status": resolution_status,
        "source_chart_results_for_each_UTC_component": source_groups,
        "original_source_unique_chart_states_across_all_UTC_and_calendar_hour_policies": len(
            distinct_stars
        ),
        "all_source_star_status_categories": sorted(distinct_labels),
        "mechanical_full_source_chart_invariant_if_no_clock_gap": usable_mechanics,
        "mechanical_anchor_presence_status_invariant_without_trait_validation": status_same,
        "source_summary_is_a_real_behavioral_prediction": False,
        "actual_personal_birth_instant_recovered": False,
        "incomplete_ancient_source_personality_rule_promoted": False,
        "runtime_chinese_star_calendar_uncertainty_completely_solved": False,
    }


def disputed_2057_source() -> dict:
    case = {
        "case_id": "SYNTH_2057_DISPUTED_CALENDAR_LOCAL_1200",
        "local_center": "2057-09-28T12:00:00",
        "uncertainty_seconds": 1,
        "fictional_iana_zone": "Asia/Hong_Kong",
        "fictional_explicit_east_longitude": "114.17",
    }
    try:
        run_wall_case(case)
    except natal.NatalTimeResolutionError as e:
        # No fallback; still fail closed on unsupported original clock.
        return {
            "synthetic_source_case": case["case_id"],
            "refused": True,
            "failure_class": type(e).__name__,
            "reason": str(e),
        }
    except prior.lunar.CalendarParityError as e:
        return {
            "synthetic_source_case": case["case_id"],
            "refused": True,
            "failure_class": type(e).__name__,
            "reason": str(e),
        }
    raise ValueError(
        "A source-ambiguous 2057 Chinese calendar date produced an unrejected horoscope"
    )


def main() -> dict:
    result = [run_wall_case(case) for case in MOCK_CASES]
    rejected = disputed_2057_source()
    if len(result) != 6 or not rejected["refused"]:
        fail("incorrect number of deliberately synthetic wall clocks")
    return {
        "schema": "HUMANDESIGN_ORIGINAL_ZIWEI_SYNTHETIC_LOCAL_WALL_CLOCK_TO_UTC_UNION_V1",
        "status": "ALL_VALID_FOLDS_INCLUDED_NONEXISTENT_TIMES_FLAGGED_NOT_HUMAN_BIRTH_CHART",
        "same_original_calendar_source_engine_as_prior_acceptance": True,
        "source_fourteen_main_stars_only_not_a_full_birth_horoscope": True,
        "lunar_year_boundary_traditional_new_year_not_LiChun": True,
        "original_lunar_leap_policy_transmitted_always_next": True,
        "UTC_state_evaluator_imported_from_previous_SHA_pinned_research": True,
        "original_true_apparent_solar_time_23h_Zi_day_still_unsupported": True,
        "local_clock_uncertainty_uses_exact_integer_seconds": True,
        "local_UTC_time_zone_and_longitude_fully_explicit_per_case": True,
        "full_real_person_birth_time_or_probability_distribution_inferred": False,
        "number_of_entirely_fictional_wall_clock_cases": len(result),
        "sum_of_independent_artificial_local_wall_seconds_across_cases": sum(
            r["original_local_clock_interval_length_seconds"] for r in result
        ),
        "sum_of_UTC_candidates_including_two_fold_branches": sum(
            r["valid_UTC_candidate_instants_including_both_DST_folds"] for r in result
        ),
        "cases": result,
        "entirely_rejected_2057_source_date": rejected,
        "real_human_chart_outcomes_or_predictions_validated": 0,
        "real_person_birth_records": 0,
        "production_astro_human_traits_promoted": 0,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
