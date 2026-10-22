#!/usr/bin/env python3
"""SWIEPH fourth numerical ephemeris-model check of preselected six Chinese JieQi days.

Never treat SWIEPH vs MOSEPH vs two lunar libraries as independent human
astrology validation. Fictional fixed UTC+8 reference-clock timestamps only.
Actual Swiss return flag 258 is REQUIRED; source .se1 files checked SHA/bytes.
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
THIRD=ROOT/"tasks/astro-bazi-third-solar-oracle-20261021/BAZI_THIRD_MOSHIER_ORACLE_6_TERMS_36_FICTIONAL_CLOCKS_V1.json"
PIN=B/"FOURTH_SWIEPH_SOURCE_PIN_MANIFEST.json"
OUTPUT=B/"BAZI_FOURTH_SWIEPH_6_TERMS_36_FICTIONAL_CLOCKS_V1.json"
DATA=Path("/home/joel/humandesign/data/ephemeris")
BINARY=Path("/tmp/hd-bazi-third-ephemeris-20261021/swisseph.cpython-312-x86_64-linux-gnu.so")
THIRD_SHA="48d9b068797c4ef2209761c4d94532d035e26205b48c8f3cfb250c61722d06b1"
SEPL_SHA="ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66"
SEMO_SHA="1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7"
BINARY_SHA="2b3234b6678dfa5666c98e898c16ee7e8c6c8457100e293c24ce679cd4387764"
SOURCE_FLAG=258
MAX_ROOT_SECONDS=0.002

class FourthSourceError(ValueError):
    pass


def sha(buf:bytes)->str:
    return sha256(buf).hexdigest()


def rd(path:Path)->dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_swisseph():
    try:
        import swisseph as swe
    except ImportError as exc:
        raise FourthSourceError("SWIEPH package unavailable") from exc
    if version("pysweph")!="2.10.3.6" or swe.version!="2.10.03":
        raise FourthSourceError("SWIEPH Python + engine versions not pinned")
    if Path(swe.__file__).resolve()!=BINARY.resolve():
        raise FourthSourceError("Python loaded another unpinned ephemeris module")
    if not BINARY.is_file() or BINARY.stat().st_size!=2391504 or sha(BINARY.read_bytes())!=BINARY_SHA:
        raise FourthSourceError("Wrapper binary bytes/SHA changed")
    for name,size,digest in (("sepl_18.se1",484061,SEPL_SHA),("semo_18.se1",1304771,SEMO_SHA)):
        file=DATA/name
        if not file.is_file() or file.stat().st_size!=size or sha(file.read_bytes())!=digest:
            raise FourthSourceError("Compressed ephemeris source changed: "+name)
    declared=rd(DATA/"swisseph_ephemeris_manifest.json")
    if declared["source_commit"]!="3fd0f956d73898b91cc4f67cf18b21af656d1342":
        raise FourthSourceError("Ephemeris provenance source commit differs")
    for file,digest in (("sepl_18.se1",SEPL_SHA),("semo_18.se1",SEMO_SHA)):
        if declared["files"][file]["sha256"]!=digest:
            raise FourthSourceError("Ephemeris provenance manifest mismatch")
    swe.set_ephe_path(str(DATA))
    return swe


def solar_apparent_geocentric_lon(local_reference:datetime,swe)->tuple[float,int,float]:
    if not isinstance(local_reference,datetime) or local_reference.tzinfo is not None:
        raise FourthSourceError("Only synthetic naive fixed UTC+8 reference-clock datetime")
    if not (1901<=local_reference.year<=2100):
        raise FourthSourceError("Reference-clock year outside research supported range")
    ut=local_reference-timedelta(hours=8)
    hours=ut.hour+(ut.minute+(ut.second+ut.microsecond/1e6)/60)/60
    julian_day_UT=swe.julday(ut.year,ut.month,ut.day,hours,swe.GREG_CAL)
    coords,ret_flags,error=swe.calc_ut(julian_day_UT,swe.SUN,swe.FLG_SWIEPH|swe.FLG_SPEED)
    if (ret_flags, swe.FLG_SWIEPH|swe.FLG_SPEED)!=(SOURCE_FLAG,SOURCE_FLAG) or error:
        raise FourthSourceError("Requested SWIEPH compressed ephemeris was not returned; no fallback allowed")
    if not 0<=coords[0]<360 or not .85<float(coords[3])<1.15:
        raise FourthSourceError("Sun coords or angular velocity out of certified development domain")
    return float(coords[0]),ret_flags,julian_day_UT


def difference(local:datetime,solar_target:int,swe)->float:
    longitude,_,_=solar_apparent_geocentric_lon(local,swe)
    return (longitude-solar_target+180)%360-180


def crossing(moshier_date:datetime,solar_target:int,swe)->dict[str,Any]:
    if solar_target not in (135,255,285,315):
        raise FourthSourceError("Solar target not from source-selected JieQi days")
    low=moshier_date-timedelta(hours=3)
    high=moshier_date+timedelta(hours=3)
    if difference(low,solar_target,swe)>=0 or difference(high,solar_target,swe)<=0:
        raise FourthSourceError("SWIEPH term must be bracketed by originally selected 6h window")
    loops=0
    while (high-low).total_seconds()>MAX_ROOT_SECONDS:
        mid=low+(high-low)/2
        if difference(mid,solar_target,swe)>=0:
            high=mid
        else:
            low=mid
        loops+=1
        if loops>60:
            raise FourthSourceError("Unstable Swiss root/too many iterations")
    moment=low+(high-low)/2
    final_lon,final_flags,JD=solar_apparent_geocentric_lon(moment,swe)
    residual=difference(moment,solar_target,swe)
    if abs(residual)>0.0000002:
        raise FourthSourceError("Fourth source numeric root angular residual exceeds tolerance")
    return {
        "SWIEPH_term_reference_clock":moment.isoformat(timespec="microseconds"),
        "returned_ephemeris_flags":final_flags,
        "solar_target_degrees":solar_target,
        "geocentric_apparent_tropical_sun_longitude_degrees":final_lon,
        "Julian_day_UT":JD,
        "root_bracket_precision_seconds":MAX_ROOT_SECONDS,
        "root_iterations":loops,
    }


def run()->dict[str,Any]:
    if sha(THIRD.read_bytes())!=THIRD_SHA:
        raise FourthSourceError("Earlier accepted third model original source changed")
    third=rd(THIRD)
    expected=rd(PIN)
    if expected["previous_third_source_SHA256"]!=THIRD_SHA or expected["expected_swieph_flags"]!=SOURCE_FLAG:
        raise FourthSourceError("Pinned ephemeris model metadata changed")
    swe=source_swisseph()
    terms=third["precise_JieQi_dates"]
    original_clocks=third["original_36_boundary_synthetic_comparisons"]
    if len(terms)!=6 or len(original_clocks)!=36:
        raise FourthSourceError("Previously accepted third source six dates/36 synthetic clocks changed")
    term_data=[];clock_checks=[];discord=[]
    term_targets=expected["original_6_dates"]
    for row in terms:
        label=row["JieQi_date"]
        if label not in term_targets or term_targets[label]!=row["JieQi_apparent_tropical_target_degrees"]:
            raise FourthSourceError("Six previously selected solar longitude term targets no longer match")
        target=term_targets[label]
        src_moshier=datetime.fromisoformat(row["source_third_clock"])
        src_sxtwl=datetime.fromisoformat(row["original_sxtwl_source_clock"])
        src_lunar=datetime.fromisoformat(row["source_lunar_python_first_changed_pillar_second"])
        swieph_cross=crossing(src_moshier,target,swe)
        exact=datetime.fromisoformat(swieph_cross["SWIEPH_term_reference_clock"])
        related=[x for x in original_clocks if x["JieQi_date"]==label]
        if len(related)!=6 or len(set(x["fictional_reference_clock"] for x in related))!=6:
            raise FourthSourceError("Original fictional six clock cases missing or duplicated")
        first=related[0]["source_sxtwl_year_month"]
        last=related[-1]["source_sxtwl_year_month"]
        if first==last:
            raise FourthSourceError("No source-defined year/month crossing on selected day")
        mismatches=[]
        for x in related:
            clock=datetime.fromisoformat(x["fictional_reference_clock"])
            d=difference(clock,target,swe)
            pre=d<0
            reference=first if pre else last
            calendar1=x["source_sxtwl_year_month"]==reference
            calendar2=x["source_lunar_python_year_month"]==reference
            moshier=x["third_source_expected_year_month"]==reference
            agrees=calendar1 and calendar2 and moshier
            status=("FOUR_SOFTWARE_OUTPUTS_AGREE_NOT_ASTRO_ACCURACY" if agrees
                    else "ABSTAIN_ONE_OR_MORE_SOFTWARE_WITNESSES_NONUNANIMOUS")
            sample={
                "original_fictional_fixed_UTC8_reference_clock":x["fictional_reference_clock"],
                "original_JieQi_day":label,
                "source_Swiss_file_ephemeris_flag_returned":SOURCE_FLAG,
                "source_swieph_sun_minus_target_arcseconds":round(d*3600,9),
                "source_swieph_sun_crossed_target":not pre,
                "source_swieph_selected_year_month":reference,
                "original_sxtwl_reported_year_month":x["source_sxtwl_year_month"],
                "original_lunar_python_reported_year_month":x["source_lunar_python_year_month"],
                "original_Moshier_selected_year_month":x["third_source_expected_year_month"],
                "source_sxtwl_matches_swieph":calendar1,
                "source_lunar_python_matches_swieph":calendar2,
                "source_Moshier_matches_swieph":moshier,
                "status":status,
                "human_birth_or_person_input_involved":False,
            }
            clock_checks.append(sample)
            if not agrees:
                mismatches.append(sample);discord.append(sample)
        term_data.append({
            "JieQi_reference_date":label,
            "angle_target_degrees":target,
            "original_source_sxtwl_UTC8_term_clock":src_sxtwl.isoformat(timespec="microseconds"),
            "original_source_lunar_python_switch_clock":src_lunar.isoformat(timespec="seconds"),
            "original_Moshier_model_crossing_clock":src_moshier.isoformat(timespec="microseconds"),
            **swieph_cross,
            "SWIEPH_minus_Moshier_seconds":round((exact-src_moshier).total_seconds(),6),
            "SWIEPH_minus_sxtwl_seconds":round((exact-src_sxtwl).total_seconds(),6),
            "lunar_python_minus_SWIEPH_seconds":round((src_lunar-exact).total_seconds(),6),
            "original_6_clock_case_count":len(related),
            "unanimity_disagreement_count":len(mismatches),
            "unanimity_disagreement_samples":mismatches,
        })
    if len(clock_checks)!=36 or len(set(r["original_fictional_fixed_UTC8_reference_clock"] for r in clock_checks))!=36:
        raise FourthSourceError("Full frozen source clocks lost or duplicated")
    consensus_conflicts=[x for x in discord if x["source_sxtwl_matches_swieph"]==x["source_lunar_python_matches_swieph"]==False]
    return {
        "schema":"BAZI_SWIEPH_COMPRESSED_EPHEMERIS_FOURTH_BACKEND_6_JIEQI_36_CLOCKS_V1",
        "status":"ENGINEERING_COMPARISON_ONLY_NOT_REAL_CHINESE_BIRTH_CHART_VALIDATION",
        "parent_third_source_report_SHA256":THIRD_SHA,
        "vendor_Swiss_ephemeris_source":expected,
        "source_Swiss_EPHE_return_flags_258_required":True,
        "source_Swiss_prior_Moshier_flag_260_is_distinct":True,
        "model_ephemeris_data_source_is_file_backed":True,
        "six_term_swieph_apparent_geocentric_Sun_crossings":term_data,
        "all_original_36_fictional_fixed_UTC8_clock_comparisons":clock_checks,
        "all_four_nonunanimity_clocks":discord,
        "new_two_calendar_consensus_against_SWIEPH_clocks":consensus_conflicts,
        "all_four_unanimity_count":36-len(discord),
        "all_four_nonunanimity_count":len(discord),
        "historical_Chinese_original_printed_source_independently_verified":False,
        "human_birth_input_records":0,
        "real_blinded_human_predictive_validations":0,
        "runtime_astrology_rule_promotions":0,
    }


if __name__=="__main__":
    if OUTPUT.exists():
        raise FourthSourceError("Existing report should be reviewed, not overwritten")
    report=run()
    OUTPUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "six_terms":len(report["six_term_swieph_apparent_geocentric_Sun_crossings"]),
        "original_boundary_clocks":len(report["all_original_36_fictional_fixed_UTC8_clock_comparisons"]),
        "nonunanimity":report["all_four_nonunanimity_count"],
        "two_calendar_consensus_contrary_to_SWIEPH":len(report["new_two_calendar_consensus_against_SWIEPH_clocks"]),
        "source_SHA256":sha(OUTPUT.read_bytes()),
        "switch_offsets":[(x["JieQi_reference_date"],x["SWIEPH_minus_Moshier_seconds"],x["lunar_python_minus_SWIEPH_seconds"])
                          for x in report["six_term_swieph_apparent_geocentric_Sun_crossings"]],
    },ensure_ascii=False,indent=2))
