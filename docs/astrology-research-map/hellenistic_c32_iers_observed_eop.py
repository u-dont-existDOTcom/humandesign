"""C32 observed IERS EOP C04 UT1-UTC audit (research-only).

Raw, large IERS 20 C04 file is supplied explicitly, never stored in Git.
The 5 MB versioned source is available via a public mirror and hashed.

For leap-second boundaries, interpolate UT1-TAI (continuous), then
restore TAI-UTC at the requested UTC instant; raw UT1-UTC is discontinuous
at a leap second and MUST NOT be directly interpolated.
"""
from __future__ import annotations

from datetime import UTC,datetime,date,timedelta
from pathlib import Path
import hashlib
import importlib
import json

from hellenistic_c32_independent_iau_angle_audit import (
    erfa_iau06_angles,swiss_angle_reference,circular_arcseconds,
    synthetic_cases,
)

SOURCE_FILENAME_SHA256 = "ed3ee86f9a6470a0f6c33e080991745069cf1a7a0899bf6fa9122d10bbd89181"
SOURCE_URL = ("https://www.simplespacedata.org/eop/iers/"
              "c04_20u24/latest/EOP_C04_one_file_1962-now.txt")
SOURCE_HEADER_ACTUAL = "EOP (IERS) 20 C04 TIME SERIES"
SOURCE_HEADER_NOT = "20u24 C04"


def load_pinned_eop(filename:Path)->dict[date,dict]:
    original=filename.read_bytes()
    if hashlib.sha256(original).hexdigest()!=SOURCE_FILENAME_SHA256:
        raise ValueError("IERS file version SHA does not match source-frozen C32 input")
    text=original.decode("utf8")
    if SOURCE_HEADER_ACTUAL not in text:
        raise ValueError("different official EOP series identity")
    rows={}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        fields=line.split()
        if len(fields)<19:
            raise ValueError("malformed IERS C04 daily record")
        yy,mm,dd,hh=map(int,fields[:4])
        if hh!=0:
            raise ValueError("only 0h UTC IERS C04 observations permitted")
        day=date(yy,mm,dd)
        if day in rows:
            raise ValueError("duplicate EOP day")
        rows[day]={
            "date":day.isoformat(),
            "MJD":float(fields[4]),
            "x_pole_arcsec":float(fields[5]),
            "y_pole_arcsec":float(fields[6]),
            "dut1_seconds":float(fields[7]),
            "sigma_dut1_seconds":float(fields[15])
        }
    if not rows or min(rows)!=date(1962,1,1):
        raise ValueError("unexpected IERS time horizon")
    return rows


def observed_dut1_for_datetime(utc:datetime,rows:dict[date,dict])->dict:
    """UTC clock -> IERS daily UT1-UTC; interpolate continuous UT1-TAI.

    This is a reproducible interpolation approximation between IERS 0h
    records, not an IERS asserted sub-daily observation or a complete EOP
    error budget. Polar motion x/y is separately recorded, not applied
    to the Swiss house/angle latitude in this proof-of-concept.
    """
    if utc.tzinfo is None or utc.utcoffset() is None:
        raise ValueError("timezone-aware UTC required")
    dt=utc.astimezone(UTC)
    day=dt.date()
    tomorrow=day+timedelta(days=1)
    if day not in rows or tomorrow not in rows:
        return {"available":False,"reason":"OUTSIDE_PINNED_IERS_TWO_DAY_RANGE"}
    erfa=importlib.import_module("erfa")
    before,after=rows[day],rows[tomorrow]
    frac=(dt.hour*3600+dt.minute*60+dt.second+
          dt.microsecond/1e6)/86400.
    da0=float(erfa.dat(day.year,day.month,day.day,0.))
    da1=float(erfa.dat(tomorrow.year,tomorrow.month,tomorrow.day,0.))
    dac=float(erfa.dat(day.year,day.month,day.day,frac))
    u_tai0=before["dut1_seconds"]-da0
    u_tai1=after["dut1_seconds"]-da1
    dut1=(1-frac)*u_tai0+frac*u_tai1+dac
    sigma=max(before["sigma_dut1_seconds"],after["sigma_dut1_seconds"])
    return {
        "available":True,
        "dut1_seconds":dut1,
        "source_day0":before["date"],
        "source_day1":after["date"],
        "two_original_daily_records":[before,after],
        "TAI_minus_UTC_at_day0_seconds":da0,
        "TAI_minus_UTC_at_day1_seconds":da1,
        "TAI_minus_UTC_at_instant_seconds":dac,
        "interpolation_fraction":frac,
        "linear_interpolation_of_UT1_minus_TAI":True,
        "observational_DUT1_not_independent_UTC_timezone_check":True,
        "polar_motion_not_applied":True,
        "max_tabulated_formal_UT1_sigma_seconds":sigma,
    }


def swiss_with_observed_ut1(utc:datetime,lat:float,lon:float,dut1:float):
    """Swiss UT1 Julian Day with externally observed DUT1, no private data."""
    swe=importlib.import_module("swisseph")
    dt=utc.astimezone(UTC)
    fraction=(dt.hour+dt.minute/60+dt.second/3600+
              dt.microsecond/3.6e9)
    jd_ut1=swe.julday(dt.year,dt.month,dt.day,fraction,swe.GREG_CAL)+dut1/86400.
    _,ascmc=swe.houses_ex(jd_ut1,lat,lon,b"P",0)
    return float(ascmc[0]),float(ascmc[1])


def audit_observed_eop(raw_filename:Path)->dict:
    data=load_pinned_eop(raw_filename)
    sample=[]
    skipped=[]
    for time,lat,lon in synthetic_cases():
        obs=observed_dut1_for_datetime(time,data)
        if not obs["available"]:
            skipped.append({"year":time.year,"reason":obs["reason"]})
            continue
        observed=float(obs["dut1_seconds"])
        iau=erfa_iau06_angles(time,latitude=lat,longitude=lon,
                              dut1_seconds=observed)
        swiss=swiss_with_observed_ut1(time,lat,lon,observed)
        baseline=swiss_angle_reference(time,latitude=lat,longitude=lon)
        sample.append({
            "utc":time.isoformat(),"latitude":lat,"longitude":lon,
            "IERS_observed_dut1_seconds":observed,
            "IERS_source_days":[obs["source_day0"],obs["source_day1"]],
            "IERS_source_daily_records":obs["two_original_daily_records"],
            "interpolated_UT1_minus_TAI_fraction":obs["interpolation_fraction"],
            "day0_TAI_minus_UTC_seconds":obs["TAI_minus_UTC_at_day0_seconds"],
            "day1_TAI_minus_UTC_seconds":obs["TAI_minus_UTC_at_day1_seconds"],
            "instant_TAI_minus_UTC_seconds":obs["TAI_minus_UTC_at_instant_seconds"],
            "IERS_formal_sigma_max_seconds":obs["max_tabulated_formal_UT1_sigma_seconds"],
            "ERFA_asc_observed_UT1":iau["asc"],
            "Swiss_asc_observed_UT1":swiss[0],
            "ERFA_mc_observed_UT1":iau["mc"],
            "Swiss_mc_observed_UT1":swiss[1],
            "asc_ERFA_vs_Swiss_arcsec":circular_arcseconds(iau["asc"],swiss[0]),
            "mc_ERFA_vs_Swiss_arcsec":circular_arcseconds(iau["mc"],swiss[1]),
            "asc_observed_EOP_shift_from_assumed0_arcsec":
                circular_arcseconds(swiss[0],baseline[0]),
            "mc_observed_EOP_shift_from_assumed0_arcsec":
                circular_arcseconds(swiss[1],baseline[1]),
            "no_private_birth_data":True,
        })
    return {
        "schema":"HUMANDESIGN_C32_OBSERVED_IERS_EOP_SENSITIVITY_V1",
        "source_mirror":SOURCE_URL,
        "raw_IERS_file_sha256":SOURCE_FILENAME_SHA256,
        "actual_file_header_series":SOURCE_HEADER_ACTUAL,
        "not_automatically_equivalent_to_20u24_latest":True,
        "file_first_day":min(data).isoformat(),
        "file_last_day":max(data).isoformat(),
        "file_daily_rows":len(data),
        "source_version_frozen_at_retrieval":True,
        "synthetic_samples_total":len(sample)+len(skipped),
        "IERS_available_synthetic_samples":len(sample),
        "skipped_synthetic_samples":skipped,
        "max_asc_ERFA_vs_Swiss_observed_EOP_arcseconds":
            max(x["asc_ERFA_vs_Swiss_arcsec"] for x in sample),
        "max_mc_ERFA_vs_Swiss_observed_EOP_arcseconds":
            max(x["mc_ERFA_vs_Swiss_arcsec"] for x in sample),
        "max_asc_actual_EOP_shift_from_assumed0_arcseconds":
            max(x["asc_observed_EOP_shift_from_assumed0_arcsec"] for x in sample),
        "max_mc_actual_EOP_shift_from_assumed0_arcseconds":
            max(x["mc_observed_EOP_shift_from_assumed0_arcsec"] for x in sample),
        "polar_motion_and_dX_dY_not_implemented":True,
        "historical_civil_time_and_birthplace_not_audited":True,
        "independent_private_birth_case_not_included":True,
        "high_stakes_or_human_prediction_certified":False,
        "human_predictive_validations":0,
        "samples":sample,
    }

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("file",type=Path)
    r=p.parse_args()
    print(json.dumps(audit_observed_eop(r.file),sort_keys=True,indent=2))
