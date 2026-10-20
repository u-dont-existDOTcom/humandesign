#!/usr/bin/env python3
"""Explicit Chinese source-versus-external implementation chart comparison.

10 exact original HKO Gregorian-lunar dates, each with 12 synthetic hour
branches, male/female, and BOTH variants of leap handling when relevant.
Not personal data, not a future prediction or blind human test. The outside
vendor is an algorithmic comparator, not a Chinese original source witness.

Run:
  IZTRO_MODULE_DIR=/tmp/hd-iztro-parity-20261020/node_modules/iztro \
    python3 audit_source_against_iztro_2_6_0.py --output REPORT.json
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "ziwei"))
from dual_witness_civil_lunar import HKO_WITNESS, frozen_hko_example  # noqa: E402
from quan_shu_fourteen_stars import fourteen_from_lunar_inputs  # noqa: E402
from ziwei_source_mechanics import BRANCHES  # noqa: E402

ZH_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
ZH_STARS = {
    "紫微": "ZiWei", "天机": "TianJi", "太阳": "TaiYang",
    "武曲": "WuQu", "天同": "TianTong", "廉贞": "LianZhen",
    "天府": "TianFu", "太阴": "TaiYin", "贪狼": "TanLang",
    "巨门": "JuMen", "天相": "TianXiang", "天梁": "TianLiang",
    "七杀": "QiSha", "破军": "PoJun",
}
ZH_BUREAUS = {"水二局": 2, "木三局": 3, "金四局": 4, "土五局": 5, "火六局": 6}
SOURCE_BRANCH_INPUTS = BRANCHES
NODE_BRIDGE = Path(__file__).with_name("iztro_2_6_0_oracle_bridge.cjs")
IZTRO_PINNED = "2.6.0"


def normalize_iztro_star_positions(stars: dict[str, str]) -> dict[str, str]:
    if set(stars) != set(ZH_STARS):
        raise ValueError(f"Iztro changed exact fourteen principal-star names: {set(stars) ^ set(ZH_STARS)}")
    return {ZH_STARS[name]: SOURCE_BRANCH_INPUTS[ZH_BRANCHES.index(house)]
            for name, house in stars.items()}


def parse_iztro_palace(house: str) -> str:
    if house not in ZH_BRANCHES:
        raise ValueError("Outside tool returned unrecognized Chinese earthly branch")
    return SOURCE_BRANCH_INPUTS[ZH_BRANCHES.index(house)]


def build_inputs():
    hko = json.loads(HKO_WITNESS.read_text(encoding="utf-8"))
    hko_days = [record["gregorian_date"] for record in hko["samples"]]
    if len(hko_days) != 10 or len(set(hko_days)) != 10:
        raise ValueError("Original independent official HKO example registry changed")
    cases = []
    expected = {}
    for greg in hko_days:
        lunar = frozen_hko_example(greg)
        # Traditional Quan Shu leap-month = next month, unlike modern
        # half-leap variants (d<=15 current, d>15 next).
        for hour_index, hour_branch in enumerate(SOURCE_BRANCH_INPUTS):
            for gender in ("male", "female"):
                for fix_leap in ((False, True) if lunar.is_leap_month else (True,)):
                    id_ = f"{greg}|H{hour_index:02d}|{gender}|fixLeap{int(fix_leap)}"
                    if id_ in expected:
                        raise ValueError("Duplicate synthetic source chart input")
                    source = fourteen_from_lunar_inputs(
                        lunar.year_heavenly_stem,
                        lunar.month,
                        hour_branch,
                        lunar.day,
                        is_leap_month=lunar.is_leap_month,
                        documented_nayin_emendations=True,
                        documented_diagram_corrections=True,
                    )
                    if source.stars is None or len(source.stars) != 14:
                        raise ValueError(f"Original source partial engine did not resolve {id_}")
                    cases.append({
                        "id": id_,
                        "lunar_ymd": f"{lunar.year}-{lunar.month}-{lunar.day}",
                        "time_index": hour_index,
                        "gender": gender,
                        "leap": lunar.is_leap_month,
                        "fix_leap": fix_leap
                    })
                    expected[id_] = {
                        "gregorian_reference_date": greg,
                        "lunar_year": lunar.year,
                        "lunar_month": lunar.month,
                        "lunar_day": lunar.day,
                        "is_leap_month": lunar.is_leap_month,
                        "hour_branch": hour_branch,
                        "source_status": source.status,
                        "life_palace": source.partial_natal.life_palace,
                        "body_palace": source.partial_natal.body_palace,
                        "bureau_number": source.partial_natal.bureau.bureau_number,
                        "source_purple_star_provenance": source.partial_natal.purple_star.source_status,
                        "source_bureau_provenance": source.partial_natal.bureau.source_status,
                        "star_palaces": source.stars,
                        "gender": gender,
                        "fix_leap": fix_leap,
                    }
    return cases, expected


def run(package_directory: Path):
    if not package_directory.is_absolute() or not package_directory.is_dir():
        raise ValueError("Explicit installed pinned iztro module directory required")
    package_json_path=package_directory/"package.json"
    pkg=json.loads(package_json_path.read_text())
    if pkg["version"] != IZTRO_PINNED:
        raise ValueError("Unexpected outside iztro package version")
    cases,expected=build_inputs()
    assert len(cases)==312, (len(cases),len(expected))
    cmd=["node",str(NODE_BRIDGE)]
    env=os.environ.copy()
    env["IZTRO_MODULE_DIR"]=str(package_directory)
    actual=subprocess.run(
        cmd,input=json.dumps({"cases":cases},ensure_ascii=False),text=True,capture_output=True,
        env=env,check=True,timeout=90
    )
    parsed=json.loads(actual.stdout)
    if parsed["pinned_version"]!=IZTRO_PINNED or parsed["config"] != {
        "yearDivide":"normal","dayDivide":"forward","algorithm":"default","horoscopeDivide":"normal"
    }:
        raise ValueError("Unexpected outside implementation version or school-method settings")
    if len(parsed["cases"])!=312:
        raise ValueError("External implementation lost test cases")
    joined=[]
    mismatches=[]
    status_counter=Counter()
    summary_counter=Counter()
    exact_ordinary=0
    for orig, other in zip(cases,parsed["cases"]):
        if orig["id"]!=other["id"]:
            raise ValueError("External chart reorder or ID mismatch")
        source=expected[orig["id"]]
        other_stars=normalize_iztro_star_positions(other["star_palaces"])
        actual_values={
            "life_palace":parse_iztro_palace(other["life_palace"]),
            "body_palace":parse_iztro_palace(other["body_palace"]),
            "bureau_number":ZH_BUREAUS[other["five_element_bureau"]],
            "star_palaces":other_stars
        }
        diff_fields=[field for field in actual_values if source[field]!=actual_values[field]]
        drift_stars={name:{"source":source["star_palaces"][name],"external_iztro":other_stars[name]}
                     for name in source["star_palaces"] if source["star_palaces"][name]!=other_stars[name]}
        if bool(diff_fields)!=bool(drift_stars or
                                  source["life_palace"]!=actual_values["life_palace"] or
                                  source["body_palace"]!=actual_values["body_palace"] or
                                  source["bureau_number"]!=actual_values["bureau_number"]):
            raise ValueError("Bug in drift-classification function")
        identical = not diff_fields
        status_counter[source["source_status"]]+=1
        status_key="exact_agreement" if identical else "disagreement"
        summary_counter[status_key]+=1
        if not source["is_leap_month"]:
            summary_counter["nonleap_total"]+=1
            if identical:
                exact_ordinary+=1
        else:
            summary_counter["leap_total"]+=1
            if orig["fix_leap"]:
                summary_counter["leap_modern_half_month_true_total"]+=1
                if identical:
                    summary_counter["leap_modern_half_month_true_agree"]+=1
            else:
                summary_counter["leap_month_unchanged_false_total"]+=1
                if identical:
                    summary_counter["leap_month_unchanged_false_agree"]+=1
        record={
            "id":orig["id"],
            "source_case":source,
            "iztro":actual_values,
            "match":identical,
            "differing_fields":diff_fields,
            "differing_14_stars":drift_stars,
            "comparison_classification": (
                "agreement" if identical else
                "leap_policy_mismatch_or_other_school_variant" if source["is_leap_month"] else
                "UNEXPECTED_non_leap_source_or_software_disagreement"
            ),
        }
        joined.append(record)
        if not identical:
            mismatches.append(record)
    if summary_counter["exact_agreement"]+summary_counter["disagreement"]!=312:
        raise ValueError("Lost synthetic chart in summary")
    stream=json.dumps(joined,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    return {
        "study":"Source-locked traditional Zi Wei 14 principal stars versus independent iztro 2.6.0 synthetic charts",
        "claim":"MECHANICAL CHART REPLAY, not a human predictive accuracy validation",
        "iztro_upstream":"https://github.com/SylarLong/iztro",
        "iztro_version":pkg["version"],
        "iztro_package_json_sha256":__import__("hashlib").sha256(package_json_path.read_bytes()).hexdigest(),
        "iztro_configuration":parsed["config"],
        "chosen_original_lunar_year_rule":"Chinese New Year, not Li Chun",
        "chosen_original_leap_rule":"transmitted Quan Shu leap month always counts as following month",
        "comparison_vendor_leap_fix_true":"iztro first half of leap month current month, second half next month",
        "comparison_vendor_leap_fix_false":"iztro leap month stays current for all dates",
        "scope":"10 HKO-authenticated Chinese reference dates (2023,2025-2028) x 12 synthetic hour branches x two genders x duplicate fixLeap options in 3 leap dates",
        "original_official_HKO_dates":10,
        "synthetic_cases":312,
        "identical_14_star_and_life_body_bureau_cases":summary_counter["exact_agreement"],
        "differing_cases":summary_counter["disagreement"],
        "nonleap_cases":summary_counter["nonleap_total"],
        "nonleap_identical":exact_ordinary,
        "leap_cases":summary_counter["leap_total"],
        "leap_fix_true_cases":summary_counter["leap_modern_half_month_true_total"],
        "leap_fix_true_identical":summary_counter["leap_modern_half_month_true_agree"],
        "leap_fix_false_cases":summary_counter["leap_month_unchanged_false_total"],
        "leap_fix_false_identical":summary_counter["leap_month_unchanged_false_agree"],
        "source_status_counts":dict(status_counter),
        "sha256_full_312_joined_output":hashlib.sha256(stream).hexdigest(),
        "all_312_case_records":joined,
        "all_disagreements":mismatches,
        "independent_ancient_imprint_authenticated":False,
        "birthplace_local_to_calendar_date_verified":False,
        "preregistered_blinded_real_person_tests":0,
        "runtime_astrological_forecast_promotions":0,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    p.add_argument("--iztro-module-dir",required=True)
    args=p.parse_args()
    result=run(Path(args.iztro_module_dir))
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    summary={k:result[k] for k in [
        "synthetic_cases","identical_14_star_and_life_body_bureau_cases","differing_cases",
        "nonleap_cases","nonleap_identical","leap_cases",
        "leap_fix_true_cases","leap_fix_true_identical",
        "leap_fix_false_cases","leap_fix_false_identical","sha256_full_312_joined_output"
    ]}
    print("RESULT",json.dumps(summary))
    for r in result["all_disagreements"][:12]:
        print("DIFF",r["id"],r["comparison_classification"],r["differing_fields"],
              list(r["differing_14_stars"].keys())[:4])


if __name__=="__main__":
    main()
