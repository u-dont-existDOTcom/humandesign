#!/usr/bin/env python3
"""Compose existing source-first Chinese calendar/Palaces/NaYin ZiWei mechanics.

Only modern fixed-UTC+08 sample timestamps, and only LIFE/BODY, source year
stem, NaYin five-element bureau, conditional Zi Wei/Tian Fu placements. Keep
different lunar-year and LiChun-year candidates explicit. Source manuscript
glyph gaps stay null. This is NOT a full 14-star traditional natal/timing
engine, personal character chart, nor evidence of human predictive validity.
"""
from __future__ import annotations
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from partial_chinese_chart_candidates import (
    CHINA_CIVIL_FIXED_UTC_PLUS8, source_candidate,
)
from ziwei_nayin_bureau_source import (
    STEMS_CH, STEMS_ROMAN, conditional_source_bureau, ORIGINAL_SHA,
)
from ziwei_original_bureau_candidate import candidate_given_bureau_day

HERE=Path(__file__).resolve().parent
TEST_CASES=(
    ("calendar_winter_1985_fixed_noon_exercise",1985,1,29,12,0),
    ("intercalary_second_month_2023",2023,3,22,12,0),
    ("LiChun_2024_before_solar_term_noon",2024,2,4,12,0),
    ("LiChun_2024_before_term_minutes",2024,2,4,16,26),
    ("LiChun_2024_after_term_minutes",2024,2,4,16,30),
    ("LiChun_2024_next_day_before_lunar_newyear",2024,2,5,12,0),
    ("late_Zi_2024_unresolved_day_change",2024,2,4,23,30),
    ("after_2024_lunar_newyear",2024,2,10,12,0),
    ("leap_Gregorian_february_2000",2000,2,29,12,0),
    ("October_2026",2026,10,20,12,0),
)

def conditional_for_given_year_policy(calendar_data,year_stem,policy_name):
    assert year_stem in STEMS_ROMAN
    bureau=conditional_source_bureau(year_stem,calendar_data.ziwei_life_palace_partial)
    raw=asdict(bureau)
    value=bureau.source_conditional_bureau_Chinese
    if value is not None:
        source_ziwei=candidate_given_bureau_day(value,calendar_data.lunar_ymd[2])
        source_ziwei=asdict(source_ziwei)
    else:
        source_ziwei=None
    return {
        "source_year_convention":policy_name,
        "source_birth_year_stem_as_provided_under_this_convention":year_stem,
        "life_palace_branch_as_computed_from_frozen_original_mechanics":calendar_data.ziwei_life_palace_partial,
        "lunar_day_as_computed_by_two_CST_chinese_calendar_libraries":calendar_data.lunar_ymd[2],
        "source_NaYin_bureau":raw,
        "given_bureau_day_ZiWei_TianFu_transmitted_table_lookup":source_ziwei,
        "possible_ziwei_palace_as_original_transmitted_source_only":None if source_ziwei is None else source_ziwei["literal_ziwei_branch_if_single_source_label"],
        "possible_tianfu_palace_as_original_transmitted_source_only":None if source_ziwei is None else source_ziwei["derived_tianfu_branch_if_single_ziwei_label"],
        "source_material_used_as_person_prediction":False,
        "confirmed_classical_birth_chart_against_independent_reference":False,
    }

def one_sample(label,y,m,d,h,minute):
    at=datetime(y,m,d,h,minute,tzinfo=CHINA_CIVIL_FIXED_UTC_PLUS8)
    cal=source_candidate(at)
    lunar_year_stem=cal.ziwei_calendar_year_stem_lunar_new_year
    lichun_year_stem=STEMS_ROMAN[STEMS_CH.index(cal.bazi_year_LiChun_exact[0])]
    source_policies={
       "natal_lunar_new_year_convention":conditional_for_given_year_policy(cal,lunar_year_stem,"LUNAR_NEW_YEAR_YEAR_STEM_NOT_UNIVERSAL_TO_ALL_LINEAGES"),
       "natal_LiChun_convention":conditional_for_given_year_policy(cal,lichun_year_stem,"LiCHUN_SOLAR_YEAR_STEM_EXACT_LUNAR_PYTHON_TERM_POLICY"),
    }
    line1=source_policies["natal_lunar_new_year_convention"]
    line2=source_policies["natal_LiChun_convention"]
    keys=("source_birth_year_stem_as_provided_under_this_convention",
          "possible_ziwei_palace_as_original_transmitted_source_only",
          "possible_tianfu_palace_as_original_transmitted_source_only")
    difference=any(line1[key]!=line2[key] for key in keys)
    return {
        "synthetic_calendar_case_label":label,
        "fixed_china_civil_time_UTC_plus_8":at.isoformat(),
        "calendar_candidate":asdict(cal),
        "two_unmerged_natal_year_conventions":source_policies,
        "different_source_year_policy_or_star_position":difference,
        "no_historical_native_true_solar_localtime_chart_verified":True,
        "full_ZiWei14_primary_stars_original_parity_verified":False,
        "real_human_observational_outcomes":0,
    }

def build_result():
    results=[one_sample(*spec) for spec in TEST_CASES]
    return {
        "schema":"SOURCE_CONDITIONAL_PARTIAL_ZIWEI_CALENDAR_TO_MAIN_TWO_STARS_V1",
        "source_witness_original_Wikisource_ZiWei_VolII_oldid1963110_sha256":ORIGINAL_SHA,
        "policy_scope":"Modern proleptic Gregorian fixed China standard UTC+08 input only. Both Lunar-New-Year and LiChun-year stem alternatives emitted; no chronology/location assumptions hidden.",
        "original_worked_example":"Jia birth year, Life palace Yin => Bing Yin, Fire six bureau, first lunar day Zi Wei You; demonstrated separately without assigning to real person.",
        "sample_count":len(results),
        "year_policy_ambiguity_sample_count":sum(x["different_source_year_policy_or_star_position"] for x in results),
        "cases_with_unresolved_original_source_glyphs": [
            {"case":x["synthetic_calendar_case_label"],"year_policy":policy}
            for x in results
            for policy,output in x["two_unmerged_natal_year_conventions"].items()
            if output["source_NaYin_bureau"]["source_conditional_bureau_Chinese"] is None
        ],
        "unverified_original_source_early_woodblock":True,
        "full_natal_14_star_chart_and_timing_computation_verified":False,
        "birth_place_and_historical_time_zone_normalization_verified":False,
        "full_original_LiChun_calendar_source_policy_expert_validated":False,
        "personal_life_or_illness_predictions_made":0,
        "independent_real_human_predictions_validated":0,
        "runtime_model_promotions":0,
        "scenarios":results,
    }

def main():
    output=HERE/'ZIWEI_PARTIAL_END_TO_END_10_SYNTHETIC_CHARTS_20261020.json'
    result=build_result()
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"samples":result["sample_count"],
        "birthyear_policy_ambiguous_samples":result["year_policy_ambiguity_sample_count"],
        "original_source_missing_glyphs_in_sample":len(result["cases_with_unresolved_original_source_glyphs"]),
        "real_people_validated":0,
        "per_sample":[{"label":x["synthetic_calendar_case_label"],
          "year_conventions_differ":x["different_source_year_policy_or_star_position"],
          "source_candidate_Lunar_year_bureau":x["two_unmerged_natal_year_conventions"]["natal_lunar_new_year_convention"]["source_NaYin_bureau"]["source_conditional_bureau_Chinese"],
          "source_candidate_Lunar_year_ZiWei":x["two_unmerged_natal_year_conventions"]["natal_lunar_new_year_convention"]["possible_ziwei_palace_as_original_transmitted_source_only"]} for x in result["scenarios"]]},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
