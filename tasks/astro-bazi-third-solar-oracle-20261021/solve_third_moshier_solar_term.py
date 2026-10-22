#!/usr/bin/env python3
"""Development-only modern geocentric solar-term third numerical model.

Uses an isolated Swiss Ephemeris Moshier implementation; does NOT certify original
Chinese calendar source, real people, birth locations, or astrological outcomes.
"""
from __future__ import annotations
from datetime import datetime,timedelta
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
from typing import Any

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
PREVIOUS=ROOT/"tasks/astro-bazi-fourpillars-jieqi-20261021/BAZI_FOURPILLARS_480_RANDOM_PLUS_36_BOUNDARY_SYNTHETIC_V1.json"
OUTPUT=B/"BAZI_THIRD_MOSHIER_ORACLE_6_TERMS_36_FICTIONAL_CLOCKS_V1.json"
PIN=B/"THIRD_EPHEMERIS_PIN_MANIFEST_V1.json"
SWE_BIN=Path("/tmp/hd-bazi-third-ephemeris-20261021/swisseph.cpython-312-x86_64-linux-gnu.so")
PREV_SHA="bf67f3a45078676a0ccf45c26b2296b1b7c7ec0249f1a434034885c57c8ee78e"
BIN_SHA="2b3234b6678dfa5666c98e898c16ee7e8c6c8457100e293c24ce679cd4387764"
TERMS={
    "2023-02-04":315,
    "2026-01-05":285,
    "2026-02-04":315,
    "1912-12-07":255,
    "2057-08-07":135,
    "1965-12-07":255,
}
EPSILON_SECONDS=0.002
WHOLE_DAY_REFERENCE="FICTIONAL_FIXED_UTC_PLUS_08_CLOCK_NOT_BIRTHPLACE"

class SourceMismatch(ValueError):
    pass

def sha(blob:bytes)->str:
    return sha256(blob).hexdigest()

def load(path:Path)->dict:
    return json.loads(path.read_text(encoding="utf-8"))

def _astro_module():
    try:
        import swisseph as swe
    except ImportError as exc:
        raise SourceMismatch("Pinned third Moshier solar ephemeris unavailable") from exc
    if version("pysweph")!="2.10.3.6" or swe.version!="2.10.03":
        raise SourceMismatch("Third ephemeris exact package/internal version mismatch")
    if not SWE_BIN.is_file() or SWE_BIN.stat().st_size!=2391504 or sha(SWE_BIN.read_bytes())!=BIN_SHA:
        raise SourceMismatch("Installed Swiss/Moshier binary provenance has changed")
    return swe

def tropical_geocentric_apparent_sun(refclock:datetime,swe)->dict[str,Any]:
    if not isinstance(refclock,datetime) or refclock.tzinfo is not None:
        raise SourceMismatch("Only fictional naive fixed UTC+08 reference clock supported")
    if not 1901<=refclock.year<=2100:
        raise SourceMismatch("Timestamp outside 1901-2100 source testing limits")
    utc=refclock-timedelta(hours=8)
    hours=utc.hour+utc.minute/60+(utc.second+utc.microsecond/1000000)/3600
    JD_UT=swe.julday(utc.year,utc.month,utc.day,hours,swe.GREG_CAL)
    flags=swe.FLG_MOSEPH|swe.FLG_SPEED
    result=swe.calc_ut(JD_UT,swe.SUN,flags)
    if len(result)!=3:
        raise SourceMismatch("New pysweph source API expected exactly 3 return values")
    solar,actual_flags,error=result
    if actual_flags!=260 or flags!=260 or error:
        raise SourceMismatch("Third model silently changed flags or returned warning")
    if not 0.85<float(solar[3])<1.15 or not 0<=float(solar[0])<360:
        raise SourceMismatch("Source solar geocentric longitudinal position/speed unsupported")
    return {
        "apparent_tropical_geocentric_ecliptic_Sun_longitude_degrees":float(solar[0]),
        "sun_longitude_speed_degrees_per_day":float(solar[3]),
        "source_ephemeris_model":"Swiss Ephemeris 2.10.03 Moshier",
        "source_flag_returned":actual_flags,
        "Julian_day_UT":JD_UT,
    }

def angular_error_degrees(refclock:datetime,target:float,swe)->float:
    lon=tropical_geocentric_apparent_sun(refclock,swe)[
        "apparent_tropical_geocentric_ecliptic_Sun_longitude_degrees"
    ]
    return (lon-target+180)%360-180

def crossing(root_reference:datetime,solar_target:int,swe)->dict[str,Any]:
    if solar_target not in (135,255,285,315):
        raise SourceMismatch("Only exact six originally prespecified solar terms supported")
    lower=root_reference-timedelta(hours=3)
    upper=root_reference+timedelta(hours=3)
    if angular_error_degrees(lower,solar_target,swe)>=0 or angular_error_degrees(upper,solar_target,swe)<=0:
        raise SourceMismatch("Cannot bracket Sun crossing in +/-3h window")
    iters=0
    while (upper-lower).total_seconds()>EPSILON_SECONDS:
        middle=lower+(upper-lower)/2
        if angular_error_degrees(middle,solar_target,swe)>=0:
            upper=middle
        else:
            lower=middle
        iters+=1
        if iters>60:raise SourceMismatch("Numerical root solver exceeded 60 iterations")
    midpoint=lower+(upper-lower)/2
    final=tropical_geocentric_apparent_sun(midpoint,swe)
    if abs(angular_error_degrees(midpoint,solar_target,swe))>=0.0000002:
        raise SourceMismatch("Moshier source root does not meet angular residual tolerance")
    return {
        "source_third_clock":midpoint.isoformat(timespec="microseconds"),
        "solar_target_longitude_degrees":solar_target,
        "model_solar_longitude_at_root_degrees":final[
            "apparent_tropical_geocentric_ecliptic_Sun_longitude_degrees"
        ],
        "model_root_max_halfwidth_seconds":EPSILON_SECONDS,
        "model_root_iterations":iters,
        "ephemeris_actual_flags":final["source_flag_returned"],
    }

def run()->dict[str,Any]:
    if sha(PREVIOUS.read_bytes())!=PREV_SHA:
        raise SourceMismatch("Accepted prior 516-case two-source fixture changed")
    original=load(PREVIOUS)
    m=load(PIN)
    swe=_astro_module()
    if m["source_binary_sha256"]!=BIN_SHA or m["dependency_version"]!="2.10.3.6":
        raise SourceMismatch("Third-source manifest does not attest pinned binary")
    if original["naive_sxtwl_day_level_mismatches"]!=8 or len(original["precise_transition_boundary_cases"])!=36 or len(original["precise_transition_disagreements"])!=4:
        raise SourceMismatch("Original two-source measured bounds have changed")
    dates=[x["Jie_date"] for x in original["boundary_transition_switch_moments"]]
    if list(TERMS)!=dates:
        raise SourceMismatch("Only original six predeclared JieQi source dates admitted")
    entries=[];crosschecks=[];new_mismatches=[]
    for entry in original["boundary_transition_switch_moments"]:
        dt=entry["Jie_date"];target=TERMS[dt]
        sxtwl=datetime.fromisoformat(entry["sxtwl_precise_JieQi_datetime"])
        lunar_python=datetime.fromisoformat(entry["lunar_python_first_new_year_or_month_second"])
        result=crossing(sxtwl,target,swe)
        swiss=datetime.fromisoformat(result["source_third_clock"])
        source_examples=entry["boundary_samples"]
        if len(source_examples)!=6 or source_examples[0]["relative_to_sxtwl_Jie_seconds"]!=-600 or source_examples[-1]["relative_to_sxtwl_Jie_seconds"]!=600:
            raise SourceMismatch("Original source boundary sample order changed")
        oldstate=source_examples[0]["sxtwl_pillars"];newstate=source_examples[-1]["sxtwl_pillars"]
        selected=lambda p:(p["year"],p["month"])
        if selected(oldstate)==selected(newstate):
            raise SourceMismatch("Expected a source year/month solar term transition")
        discord=[]
        for row in source_examples:
            sample=datetime.fromisoformat(row["fictional_clock"])
            err=angular_error_degrees(sample,target,swe)
            time_delta=(sample-swiss).total_seconds()
            comparison=selected(newstate) if err>=0 else selected(oldstate)
            sxtwl_match=selected(row["sxtwl_pillars"])==comparison
            lunar_match=selected(row["lunar_python_pillars"])==comparison
            status="THREE_AGREE_NUMERICAL_ONLY" if sxtwl_match and lunar_match else (
                "ABSTAIN_TWO_WITNESSES_AGREE_AGAINST_THIRD" if not sxtwl_match and not lunar_match
                else "ABSTAIN_THREE_WITNESSES_DISAGREE"
            )
            reported={
                "fictional_reference_clock":row["fictional_clock"],
                "JieQi_date":dt,
                "relative_to_sxtwl_source_term_seconds":row["relative_to_sxtwl_Jie_seconds"],
                "third_source_apparent_sun_minus_target_arcsec":round(err*3600,8),
                "third_source_crossed_target":err>=0,
                "difference_seconds_from_Moshier_crossing":round(time_delta,6),
                "third_source_expected_year_month":dict(zip(("year","month"),comparison)),
                "source_sxtwl_year_month":dict(zip(("year","month"),selected(row["sxtwl_pillars"]))),
                "source_lunar_python_year_month":dict(zip(("year","month"),selected(row["lunar_python_pillars"]))),
                "source_sxtwl_matches_numerical_ephemeris":sxtwl_match,
                "source_lunar_python_matches_numerical_ephemeris":lunar_match,
                "status":status,
                "birth_chart_status":"DEVELOPMENT_ONLY_NEVER_REAL_PERSON",
            }
            crosschecks.append(reported)
            if not (sxtwl_match and lunar_match):
                discord.append(reported)
                new_mismatches.append(reported)
        entries.append({
            "JieQi_date":dt,
            "JieQi_apparent_tropical_target_degrees":target,
            "original_sxtwl_source_clock":sxtwl.isoformat(timespec="microseconds"),
            "source_lunar_python_first_changed_pillar_second":lunar_python.isoformat(timespec="seconds"),
            **result,
            "Moshier_minus_sxtwl_seconds":round((swiss-sxtwl).total_seconds(),6),
            "lunar_python_first_changed_second_minus_Moshier_seconds":round((lunar_python-swiss).total_seconds(),6),
            "original_source_two_library_disagreements":len(entry["disagreement_synthetic_clocks"]),
            "third_model_disagreeing_samples":len(discord),
            "new_source_mismatches":discord,
        })
    if len(crosschecks)!=36 or len(new_mismatches)!=5:
        raise SourceMismatch("Independent third model source result changed, retain raw disagreements")
    both_against=[x for x in new_mismatches if x["status"]=="ABSTAIN_TWO_WITNESSES_AGREE_AGAINST_THIRD"]
    if [x["fictional_reference_clock"] for x in both_against]!=["2057-08-07T07:34:09"]:
        raise SourceMismatch("Critical 2057 both-calendar-consensus-but-solar-lon preterm case missing")
    return {
        "schema":"BAZI_SIX_JIEQI_THREE_ASTRONOMICAL_SOFTWARE_WITNESS_COMPARISON_V1",
        "status":"DEVELOPMENT_ONLY_NOT_AUTHORITY_FOR_HISTORICAL_BIRTH_CHARTS",
        "input_previous_two_source_fixture_SHA256":PREV_SHA,
        "source_third_ephemeris_pin":m,
        "source_solar_positions_flags":"FLG_MOSEPH | FLG_SPEED, retflags 260",
        "source_time_conversion":"original fixed UTC+8 reference clock minus 8h => UT Julian day => Swiss calc_ut",
        "source_solar_term_targets":TERMS,
        "Moshier_implementation_not_JPL_ephemeris_files":True,
        "independent_ancient_printed_BaZi_school_certified":False,
        "precise_JieQi_dates":entries,
        "original_36_boundary_synthetic_comparisons":crosschecks,
        "all_three_model_nonunanimity_samples":new_mismatches,
        "two_calendar_libraries_agree_but_Moshier_diff_count":len(both_against),
        "all_third_witness_nonunanimity_count":len(new_mismatches),
        "human_birth_data_records":0,
        "human_blind_predictive_accuracy_validated":0,
        "runtime_astrology_rule_promotions":0,
        "unresolved_2057_one_or_more_model_errors":True,
    }

if __name__=="__main__":
    if OUTPUT.exists():
        raise SourceMismatch("Previous accepted source fixture exists, inspect before overwriting")
    out=run()
    OUTPUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "term_dates":len(out["precise_JieQi_dates"]),
        "prior_2_source_mismatches":4,
        "nonunanimous_three_source_instances":len(out["all_three_model_nonunanimity_samples"]),
        "both_calendar_libraries_agree_but_third_diff_count":out["two_calendar_libraries_agree_but_Moshier_diff_count"],
        "report_sha256":sha(OUTPUT.read_bytes())},ensure_ascii=False,indent=2))
