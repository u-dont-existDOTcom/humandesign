#!/usr/bin/env python3
"""Reproduce 480 synthetic fixed UTC+8 Four Pillars comparisons + term instants."""
from __future__ import annotations
import calendar
from datetime import datetime,timedelta
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import random

from dual_witness_bazi_fourpillars import (
    STEMS,BRANCHES,POLICY,PINNED_DEPENDENCIES,
    compare_fictional_reference_clock,lunar_python_fourpillars,sxtwl_fourpillars,
)

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
OUTPUT=B/"BAZI_FOURPILLARS_480_RANDOM_PLUS_36_BOUNDARY_SYNTHETIC_V1.json"
SOURCE_INDEX=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V30.json"
SOURCE_INDEX_SHA="6e46e87ca2019945301b1f47f8d3ee91bd58c1a89461912d50bace74bc9543de"
LIB_HOME=Path("/tmp/hd-calendar-parity-20261020")
YEARS=(1901,1912,1937,1965,1985,2000,2023,2025,2026,2036,2057,2090)
BOUNDARY_DATES=((2023,2,4),(2026,1,5),(2026,2,4),
                (1912,12,7),(2057,8,7),(1965,12,7))
TIME_OFFSETS=(-600,-60,-1,1,60,600)
SEED=20261021

def sha(raw:bytes)->str:
    return sha256(raw).hexdigest()


def source_sha_roster()->dict:
    if sha(SOURCE_INDEX.read_bytes())!=SOURCE_INDEX_SHA:
        raise ValueError("Accepted V30 historical source index changed")
    files=[
        LIB_HOME/"sxtwl.py",
        LIB_HOME/"_sxtwl.cpython-312-x86_64-linux-gnu.so",
    ]+sorted((LIB_HOME/"lunar_python").rglob("*.py"))
    if not all(x.is_file() for x in files):
        raise ValueError("Original accepted source-version research libraries unavailable")
    out={}
    for file in files:
        out[file.relative_to(LIB_HOME).as_posix()]={
            "sha256":sha(file.read_bytes()),"bytes":file.stat().st_size}
    if len(out)<6 or set(PINNED_DEPENDENCIES)!={"lunar-python","sxtwl"}:
        raise ValueError("Required two library provenance files absent")
    assert all(version(k)==v for k,v in PINNED_DEPENDENCIES.items())
    return out


def original_synthetic_samples()->list[datetime]:
    rng=random.Random(SEED)
    results=[]
    for year in YEARS:
        for _ in range(40):
            month=rng.randint(1,12)
            day=rng.randint(1,calendar.monthrange(year,month)[1])
            hour=rng.choice((0,1,6,12,21,22,23))
            results.append(datetime(year,month,day,hour,30,0))
    assert len(results)==480
    return results


def _lunar_python_year_month(t:datetime)->tuple[str,str]:
    v=lunar_python_fourpillars(t)["pillars"]
    return (v["year"],v["month"])


def lunar_python_Jie_transition_second(reference:datetime,post_year_month:tuple[str,str])->datetime:
    # This bisection compares source library behavior; it does not establish
    # astronomy truth, and all six chosen endpoints stay within the local day.
    lo=(reference-timedelta(hours=3)).replace(microsecond=0)
    hi=(reference+timedelta(hours=3)).replace(microsecond=0)
    changed=lambda t:_lunar_python_year_month(t)==post_year_month
    if changed(lo) or not changed(hi):
        raise ValueError("Original comparison bracket misses transition")
    while (hi-lo).total_seconds()>1:
        middle=lo+timedelta(seconds=int((hi-lo).total_seconds())//2)
        if changed(middle):
            hi=middle
        else:
            lo=middle
    return hi


def run()->dict:
    provenance=source_sha_roster()
    random_cases=[]
    naive_mismatches=[]
    corrected_mismatches=[]
    for t in original_synthetic_samples():
        compared=compare_fictional_reference_clock(t)
        original_untimed=sxtwl_fourpillars(t,day_transition_correction=False)["pillars"]
        given=compared["source_lunar_python"]["pillars"]
        if original_untimed!=given:
            naive_mismatches.append({"fictional_clock":t.isoformat(),"naive_date_lookup":original_untimed,"lunar_python_exact":given})
        if not compared["witness_agreement"]:
            corrected_mismatches.append(compared)
        random_cases.append({
            "clock":t.isoformat(),"corrected_sxtwl_pillars":compared["source_sxtwl"]["pillars"],
            "independent_lunar_python_pillars":given,
            "agrees":compared["witness_agreement"],
            "sxtwl_original_date_only_would_disagree":original_untimed!=given,
            "Jie_term_clock":compared["source_sxtwl"]["month_year_exact_Jie_term_datetime"],
        })
    if (len(random_cases),len(naive_mismatches),len(corrected_mismatches))!=(480,8,0):
        raise ValueError("Source parity baseline changed; preserve discrepancy rather than pass")
    boundary_cases=[];boundary_summary=[]
    for yr,month,day in BOUNDARY_DATES:
        clock=datetime(yr,month,day,12)
        x=compare_fictional_reference_clock(clock)
        iso=x["source_sxtwl"]["month_year_exact_Jie_term_datetime"]
        if not iso:raise ValueError("Exact JieQi source instant absent")
        midpoint=datetime.fromisoformat(iso)
        after=(midpoint+timedelta(hours=3)).replace(microsecond=0)
        if after.date()!=midpoint.date():
            raise ValueError("Post-Jie source evaluation crossed local calendar day")
        sxtwl_after=sxtwl_fourpillars(after)["pillars"]
        post=(sxtwl_after["year"],sxtwl_after["month"])
        lp_switch=lunar_python_Jie_transition_second(midpoint,post)
        step=[];flags=[]
        for diff in TIME_OFFSETS:
            candidate=(midpoint+timedelta(seconds=diff)).replace(microsecond=0)
            if (candidate.year,candidate.month,candidate.day)!=(yr,month,day):
                raise ValueError("Boundary control escaped same-day reference domain")
            row=compare_fictional_reference_clock(candidate)
            step.append({
                "fictional_clock":candidate.isoformat(),"relative_to_sxtwl_Jie_seconds":diff,
                "status":row["status"],"different_pillars":row["difference_components"],
                "sxtwl_pillars":row["source_sxtwl"]["pillars"],
                "lunar_python_pillars":row["source_lunar_python"]["pillars"],
            })
            boundary_cases.append(step[-1])
            if not row["witness_agreement"]:flags.append(candidate.isoformat())
        boundary_summary.append({
            "Jie_date":f"{yr:04d}-{month:02d}-{day:02d}",
            "sxtwl_precise_JieQi_datetime":midpoint.isoformat(timespec="microseconds"),
            "lunar_python_first_new_year_or_month_second":lp_switch.isoformat(timespec="seconds"),
            "relative_switch_offset_seconds":round((lp_switch-midpoint).total_seconds(),6),
            "disagreement_synthetic_clocks":flags,
            "boundary_samples":step,
        })
    disagree=[x for x in boundary_cases if x["different_pillars"]]
    if (len(boundary_cases),len(disagree))!=(36,4):
        raise ValueError("Different source solar-term boundary outcomes; retain negatives")
    return {
        "schema":"BAZI_TWO_WITNESS_FIXED_REFERENCE_FOURPILLARS_ENGINEERING_V1",
        "status":"DEVELOPMENT_ONLY_NOT_HUMAN_NATAL_CHART_OR_PREDICTIVE_VALIDATION",
        "scope_and_unselected_birth_policy":POLICY,
        "source_prior_accepted_chinese_index_sha256":SOURCE_INDEX_SHA,
        "synthetic_clock_seed":SEED,"synthetic_years":list(YEARS),
        "synthetic_sample_generation":"12 named years x 40 seeded Gregorian date/hour draws",
        "source_pinned_versions":PINNED_DEPENDENCIES,
        "source_library_files_SHA256_bytes":provenance,
        "naive_sxtwl_day_level_mismatches":len(naive_mismatches),
        "corrected_sxtwl_vs_lunar_python_mismatches":len(corrected_mismatches),
        "ordinary_synthetic_cases":random_cases,
        "original_naive_jieqi_day_mismatch_cases":naive_mismatches,
        "boundary_dates":list(map(list,BOUNDARY_DATES)),
        "boundary_relative_seconds":list(TIME_OFFSETS),
        "precise_transition_boundary_cases":boundary_cases,
        "precise_transition_disagreements":disagree,
        "boundary_transition_switch_moments":boundary_summary,
        "independently_authenticated_old_printed_BaZi_method":False,
        "actual_human_birth_inputs":0,
        "independent_real_human_blind_accuracy_studies":0,
        "astrology_runtime_rule_promotions":0,
        "synthetic_parity_does_not_establish_real_world_correctness":True,
    }


if __name__=="__main__":
    if OUTPUT.exists():
        raise ValueError("Accepted fixture exists; inspect rather than overwrite")
    doc=run()
    OUTPUT.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "ordinary":len(doc["ordinary_synthetic_cases"]),
        "ordinary_naive_mismatches":doc["naive_sxtwl_day_level_mismatches"],
        "ordinary_corrected_mismatches":doc["corrected_sxtwl_vs_lunar_python_mismatches"],
        "boundary":len(doc["precise_transition_boundary_cases"]),
        "boundary_disagreements":len(doc["precise_transition_disagreements"]),
        "boundary_switch_offsets":[x["relative_switch_offset_seconds"] for x in doc["boundary_transition_switch_moments"]],
        "SHA256":sha(OUTPUT.read_bytes())},ensure_ascii=False,indent=2))
