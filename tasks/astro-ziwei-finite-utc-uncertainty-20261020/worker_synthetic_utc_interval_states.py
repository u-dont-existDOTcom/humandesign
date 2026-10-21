#!/usr/bin/env python3
"""Finite explicit UTC integer-second synthetic uncertainty-set enumeration.

This is NOT a traditional natal chart of any living human and not an
astrological rule likelihood or empirical personality prediction. Interval
coverage is complete only for the DECLARED finite integer seconds and source
date/hour policies. The source engine's own human-facing function still
fails closed for nonzero birth-clock uncertainty and alternate true-solar/
23h Zi-day conventions.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from hashlib import sha256
from zoneinfo import ZoneInfo

import dual_witness_civil_lunar as lunar
import explicit_natal_time as natal
from quan_shu_fourteen_stars import fourteen_from_lunar_inputs

CASES = (
    {
        "case_id": "SYNTH_DAKAR_CIVIL_HOUR_BOUNDARY",
        "start_UTC": "2026-02-16T20:59:00+00:00",
        "end_UTC": "2026-02-16T21:01:00+00:00",
        "fictional_iana_zone": "Africa/Dakar",
        "fictional_explicit_east_longitude": "-17.4",
    },
    {
        "case_id": "SYNTH_DAKAR_LUNAR_NEW_YEAR_UTC8_MIDNIGHT",
        "start_UTC": "2026-02-16T15:59:00+00:00",
        "end_UTC": "2026-02-16T16:01:00+00:00",
        "fictional_iana_zone": "Africa/Dakar",
        "fictional_explicit_east_longitude": "-17.4",
    },
    {
        "case_id": "SYNTH_NY_LOCAL_MEAN_SOLAR_HOUR_BOUNDARY",
        "start_UTC": "2026-07-01T17:55:00+00:00",
        "end_UTC": "2026-07-01T18:05:00+00:00",
        "fictional_iana_zone": "America/New_York",
        "fictional_explicit_east_longitude": "-74",
    },
    {
        "case_id": "SYNTH_HK_1965_DST_UTC8_MIDNIGHT",
        "start_UTC": "1965-06-30T15:59:00+00:00",
        "end_UTC": "1965-06-30T16:01:00+00:00",
        "fictional_iana_zone": "Asia/Hong_Kong",
        "fictional_explicit_east_longitude": "114.17",
    },
    {
        "case_id": "SYNTH_NY_2026_DST_FOLD_UTC_INSTANT",
        "start_UTC": "2026-11-01T05:59:00+00:00",
        "end_UTC": "2026-11-01T06:01:00+00:00",
        "fictional_iana_zone": "America/New_York",
        "fictional_explicit_east_longitude": "-74",
    },
    {
        "case_id": "SYNTH_HK_2023_LEAP_HOUR_BOUNDARY",
        "start_UTC": "2023-03-22T04:59:00+00:00",
        "end_UTC": "2023-03-22T05:01:00+00:00",
        "fictional_iana_zone": "Asia/Hong_Kong",
        "fictional_explicit_east_longitude": "114.17",
    },
)
CALENDAR_POLICIES = natal.CALENDAR_DATE_POLICIES
HOUR_POLICIES = natal.HOUR_POLICIES
SOURCE_LEAP_POLICY = "transmitted_quan_shu_as_next"
FOUR_STARS = {"WuQu", "LianZhen", "TianLiang", "PoJun"}
HKO_DATES = {
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
PER_CASE_MAX_INTEGER_SECOND_STATES = 1000


def canon(obj) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


@lru_cache(maxsize=100)
def source_chart(calendar_day: str, hour_branch: str) -> dict:
    "Source-only Chinese lunar year/day and original 14-star chart with HKO checks."
    official = lunar.dual_library_reference_date(calendar_day)
    witness = "TWO_PINNED_SOFTWARE_CALENDARS_ONLY"
    if calendar_day in HKO_DATES:
        original = lunar.frozen_hko_example(calendar_day)
        if (official.year, official.month, official.day, official.is_leap_month) != (
            original.year,
            original.month,
            original.day,
            original.is_leap_month,
        ):
            raise ValueError("Official original HKO date and external calendar software disagree")
        witness = "ORIGINAL_HKO_SOURCE_SHA_PLUS_TWO_PINNED_SOFTWARE_CALENDARS"
    stars = fourteen_from_lunar_inputs(
        official.year_heavenly_stem,
        official.month,
        hour_branch,
        official.day,
        is_leap_month=official.is_leap_month,  # original always NEXT, no modern split
        documented_nayin_emendations=True,
        documented_diagram_corrections=True,
    )
    if stars.stars is None or len(stars.stars) != 14:
        raise ValueError("Original bounded 14 principal-star source layout unresolved")
    life = stars.partial_natal.life_palace
    major = tuple(sorted(stars.placements_by_palace[life]))
    selected = tuple(sorted(set(major) & FOUR_STARS))
    if len(selected) == 0:
        category = "ABSTAIN_NO_SELECTED_STAR_NOT_TRAIT_ABSENCE"
    elif len(selected) > 1:
        category = "ABSTAIN_MULTIPLE_SELECTED_STARS_COMBINATION_UNRESOLVED"
    elif len(major) > 1:
        category = "ABSTAIN_OTHER_MAJOR_STAR_CONJUNCTION_UNRESOLVED"
    else:
        category = "SOURCE_ONLY_SINGLE_STAR_LAYOUT_NOT_PREDICTIVE_VALIDITY"
    return {
        "reference_calendar_day": calendar_day,
        "source_hour_Earthly_Branch": hour_branch,
        "original_HKO_source_quality": witness,
        "lunar_year": official.year,
        "lunar_month": official.month,
        "lunar_day": official.day,
        "source_is_leap_month": official.is_leap_month,
        "life_palace": life,
        "body_palace": stars.partial_natal.body_palace,
        "original_source_status": stars.status,
        "life_palace_major_stars": list(major),
        "selected_four_provisional_behavior_anchor_stars": list(selected),
        "strict_methodological_source_trait_status": category,
        "full_14_major_star_layout_sha256": sha256(canon(stars.stars)).hexdigest(),
        "is_independent_birth_chart_empirical_truth": False,
        "human_behavior_p_value_or_probability_available": False,
    }


def resolve_one_tick(utc: datetime, case: dict, cal_policy: str, hour_policy: str) -> dict:
    zone = ZoneInfo(case["fictional_iana_zone"])
    local = utc.astimezone(zone)
    naive = local.replace(tzinfo=None).isoformat(timespec="seconds")
    clock = natal.resolve_explicit_local_birth_clock(
        naive,
        case["fictional_iana_zone"],
        fold=local.fold,
        calendar_day_policy=cal_policy,
        hour_time_policy=hour_policy,
        longitude_east_degrees=case["fictional_explicit_east_longitude"],
        late_zi_day_policy="midnight_day_boundary",
        recorded_clock_uncertainty_seconds=0,
    )
    if clock.birth_utc_instant != utc.isoformat(timespec="seconds"):
        raise ValueError("Reverse-constructed local wall clock lost its source UTC instant")
    st = source_chart(clock.selected_chinese_calendar_day, clock.selected_hour_branch)
    return {
        "source_calendrical_and_star_state": st,
        "source_fictional_local_clock": naive,
        "zone_offset_seconds": clock.utc_offset_seconds,
        "zone_fold": clock.fold,
        "zoneinfo_TZif_SHA256": clock.tzif_sha256,
    }


def datetime_from_UTC(s):
    d = datetime.fromisoformat(s)
    if d.utcoffset() != timedelta(0) or d.tzinfo is None:
        raise ValueError("Synthetic interval endpoints require explicit UTC+00:00 offsets")
    if d.microsecond != 0:
        raise ValueError("Synthetic source interval must use exact integer UTC seconds")
    return d.astimezone(UTC)


def summarize_interval(case: dict) -> dict:
    start = datetime_from_UTC(case["start_UTC"])
    end = datetime_from_UTC(case["end_UTC"])
    total = int((end - start).total_seconds()) + 1
    if end < start or total > PER_CASE_MAX_INTEGER_SECOND_STATES or total < 1:
        raise ValueError("Bounced UTC interval outside bounded synthetic second resolution")
    runs = []
    allstates = {}
    total_ticks = 0
    for calendar in CALENDAR_POLICIES:
        for hour in HOUR_POLICIES:
            policy = (calendar, hour)
            segments = []
            current = None
            for offset in range(total):
                utc = start + timedelta(seconds=offset)
                sampled = resolve_one_tick(utc, case, *policy)
                st = sampled["source_calendrical_and_star_state"]
                state_hash = sha256(canon(st)).hexdigest()
                allstates[state_hash] = st
                if current is None or state_hash != current["source_chart_state_SHA256"]:
                    if current is not None:
                        segments.append(current)
                    current = {
                        "start_UTC_inclusive": utc.isoformat(timespec="seconds"),
                        "end_UTC_inclusive": utc.isoformat(timespec="seconds"),
                        "integer_second_samples": 1,
                        "first_local_wall_clock": sampled["source_fictional_local_clock"],
                        "last_local_wall_clock": sampled["source_fictional_local_clock"],
                        "zone_UTC_offset_seconds_values": [sampled["zone_offset_seconds"]],
                        "zone_fold_values": [sampled["zone_fold"]],
                        "time_zone_TZif_SHA256": sampled["zoneinfo_TZif_SHA256"],
                        "source_chart_state_SHA256": state_hash,
                        "source_calendar_day": st["reference_calendar_day"],
                        "selected_hour_branch": st["source_hour_Earthly_Branch"],
                        "selected_source_trait_status": st[
                            "strict_methodological_source_trait_status"
                        ],
                        "life_palace": st["life_palace"],
                        "life_palace_major_stars": st["life_palace_major_stars"],
                        "selected_anchor_stars": st[
                            "selected_four_provisional_behavior_anchor_stars"
                        ],
                    }
                else:
                    current["end_UTC_inclusive"] = utc.isoformat(timespec="seconds")
                    current["integer_second_samples"] += 1
                    current["last_local_wall_clock"] = sampled["source_fictional_local_clock"]
                    if (
                        sampled["zone_offset_seconds"]
                        not in current["zone_UTC_offset_seconds_values"]
                    ):
                        current["zone_UTC_offset_seconds_values"].append(
                            sampled["zone_offset_seconds"]
                        )
                    if sampled["zone_fold"] not in current["zone_fold_values"]:
                        current["zone_fold_values"].append(sampled["zone_fold"])
                total_ticks += 1
            if current is not None:
                segments.append(current)
            if sum(x["integer_second_samples"] for x in segments) != total:
                raise ValueError("Missing synthetic uncertainty interval UTC seconds")
            runs.append(
                {
                    "calendar_reference_day_policy": calendar,
                    "hour_Earthly_branch_policy": hour,
                    "source_lunar_leap_policy": SOURCE_LEAP_POLICY,
                    "interval_integer_second_samples": total,
                    "distinct_natal_source_states": len(segments),
                    "source_chart_segment_states": segments,
                    "policy_invariant_source_chart_sha256": (
                        segments[0]["source_chart_state_SHA256"] if len(segments) == 1 else None
                    ),
                }
            )
    signatures = {
        segment["source_chart_state_SHA256"]
        for p in runs
        for segment in p["source_chart_segment_states"]
    }
    labels = {
        segment["selected_source_trait_status"]
        for p in runs
        for segment in p["source_chart_segment_states"]
    }
    source_anchors = {
        tuple(segment["selected_anchor_stars"])
        for p in runs
        for segment in p["source_chart_segment_states"]
    }
    complete_invariant = len(signatures) == 1
    policy_invariant = len(labels) == 1
    return {
        **case,
        "all_birth_instants_fictitious": True,
        "interval_exact_only_at_declared_integer_second_resolution": True,
        "total_original_UTC_integer_second_inclusive_samples": total,
        "all_four_reference_day_hour_policies_enumerated": True,
        "source_lunar_leap_school_predeclared": SOURCE_LEAP_POLICY,
        "source_failing_2057_date_not_replaced_by_another_calendar_school": True,
        "original_HKO_source_sample_dates_not_human_predictions": True,
        "four_calendar_hour_policy_runs": runs,
        "distinct_source_calendar_hour_life_full14_states_across_all_seconds_policies": len(
            signatures
        ),
        "distinct_four_candidate_anchor_sets_across_all_seconds_policies": len(source_anchors),
        "source_all_policy_invariant_14star_state": complete_invariant,
        "source_all_policy_invariant_four_anchor_status_only": policy_invariant,
        "robust_behavioral_prediction_from_source": False,
        "any_real_person_birth_record": False,
        "all_original_unique_source_state_details": allstates,
        "engine_footgun_note": (
            "UTC instant is pre-known in this toy; an uncertain real wall "
            "clock may include multiple possible instants/DST folds not solved here."
        ),
    }


def reject_2057_calendar_disagreement() -> dict:
    test = {
        "case_id": "SYNTH_2057_DISPUTED_DUAL_LUNAR_CALENDAR",
        "start_UTC": "2057-09-28T03:59:59+00:00",
        "end_UTC": "2057-09-28T04:00:01+00:00",
        "fictional_iana_zone": "Asia/Hong_Kong",
        "fictional_explicit_east_longitude": "114.17",
    }
    try:
        summarize_interval(test)
    except lunar.CalendarParityError as e:
        return {
            "case_id": test["case_id"],
            "entire_uncertain_interval_rejected": True,
            "reason_class": type(e).__name__,
            "reason": str(e),
            "rejected_instead_of_voting_on_calendar_school": True,
        }
    raise ValueError("Disputed 2057 calendar silently interpreted as reliable natal interval")


def run() -> dict:
    cases = [summarize_interval(c) for c in CASES]
    fail = reject_2057_calendar_disagreement()
    result = {
        "schema": "HUMANDESIGN_ZIWEI_EXPLICIT_FINITE_UTC_SECOND_SYNTHETIC_INTERVAL_SOURCE_V1",
        "status": (
            "INTEGER_SECOND_UTC_SOURCE_MECHANICS_NOT_REAL_PERSON_TIME_UNCERTAINTY_PROPAGATION"
        ),
        "source_acceptance": (
            "Pinned original source engine as-next lunar leap, HKO raw and two external calendars"
        ),
        "fictional_UTC_intervals": len(CASES),
        "fake_integer_UTC_seconds_by_case": {
            c["case_id"]: c["total_original_UTC_integer_second_inclusive_samples"] for c in cases
        },
        "total_fake_integer_second_instants_unique_by_case": sum(
            c["total_original_UTC_integer_second_inclusive_samples"] for c in cases
        ),
        "number_of_declared_calendar_hour_policies_per_case": 4,
        "independent_original_HKO_for_all_source_days": False,
        "human_birth_zone_from_approximate_location_inferred": False,
        "source_true_apparent_solar_and_23h_Zi_day_not_supported": True,
        "only_exact_integer_second_UTC_interval_no_real_unknown_clock_to_instant_conversion": True,
        "human_personal_birth_records_or_survey_responses": 0,
        "real_human_predictive_validations": 0,
        "runtime_astrological_promotions": 0,
        "case_results": cases,
        "disputed_original_calendar_interval_rejection": fail,
        "unique_source_calendar_hour_key_count": source_chart.cache_info().currsize,
    }
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
