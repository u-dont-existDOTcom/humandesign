"""G38: Conditional full-time-interval Sun Gene Key and Line feasibility.

Reads existing strict Swiss Ephemeris, not user natal charts. A declared
maximum Sun angular speed bound is propagated over the WHOLE possible UTC
birth-time interval. Gate width 5.625°, Line width 0.9375°.

The incumbent maximum 1.1°/day is a historical source-declared bound,
not independently certified for every year, so even a stable output is
conditional and DOES NOT authorize actual person predictions.
"""
from __future__ import annotations

from datetime import UTC,datetime,timedelta
from decimal import Decimal,ROUND_FLOOR
from pathlib import Path
import hashlib
import json
import sys

THIS=Path(__file__).resolve().parent
SRC=str(THIS.parents[1]/"src")
if SRC not in sys.path:sys.path.insert(0,SRC)

from hdmatch.chart.ephemeris import SwissEphemerisProvider,CelestialBody
from hdmatch.chart.rave_mandala import (
    RAVE_GATE_ORDER, RAVE_MANDALA_START_DEGREES,
    GATE_WIDTH_DEGREES, LINE_WIDTH_DEGREES, longitude_to_gate_line,
)

GATE=Decimal("5.625")
LINE=Decimal("0.9375")
ANCHOR=Decimal("302")
CYCLE_SECTORS=384
WINDOWS=(1,2,6,12,24)

def _decimal(value)->Decimal:
    if type(value) is bool:raise ValueError("Boolean is not a longitude or angular limit")
    try:a=Decimal(str(value))
    except Exception as exc:raise ValueError("numeric input required") from exc
    if not a.is_finite():raise ValueError("nonfinite longitudes not permitted")
    return a


def source_sun_line_enclosure(
    *, center_longitude, hours_width, max_abs_speed_deg_per_day
)->dict:
    center=_decimal(center_longitude)
    hours=_decimal(hours_width)
    speed=_decimal(max_abs_speed_deg_per_day)
    if not 0<=center<360:raise ValueError("physical center ecliptic longitude must be in [0,360)")
    if not 0<=hours<=48:raise ValueError("max 48h continuous research window")
    if speed<0 or speed>30:raise ValueError("speed bound must be positive plausible angular max")
    radius=(speed*hours)/Decimal(48)
    lo=(center-ANCHOR-radius)/LINE
    hi=(center-ANCHOR+radius)/LINE
    idxlo=int(lo.to_integral_value(rounding=ROUND_FLOOR))
    idxhi=int(hi.to_integral_value(rounding=ROUND_FLOOR))
    span=idxhi-idxlo+1
    if span>=CYCLE_SECTORS:
        sector_indices=set(range(CYCLE_SECTORS))
    else:
        sector_indices={i%CYCLE_SECTORS for i in range(idxlo,idxhi+1)}
    possible_gate_lines={
        (RAVE_GATE_ORDER[index//6],index%6+1)
        for index in sector_indices
    }
    gate_set=sorted({g for g,line in possible_gate_lines})
    line_set=sorted({line for g,line in possible_gate_lines})
    x=longitude_to_gate_line(float(center))
    if (x.gate,x.line) not in possible_gate_lines:
        raise AssertionError("exact noon center absent from guaranteed envelope")
    return {
        "center_gate":x.gate,
        "center_line":x.line,
        "source_line_width_deg":str(LINE),
        "source_gate_width_deg":str(GATE),
        "total_time_window_hours":str(hours),
        "source_declared_max_abs_speed_deg_day":str(speed),
        "conditional_motion_radius_degrees":str(radius),
        "possible_gate_line_pairs":sorted([{"gate":g,"line":line}
                                           for g,line in possible_gate_lines],
                                           key=lambda r:(r["gate"],r["line"])),
        "possible_gate_numbers":gate_set,
        "possible_line_numbers":line_set,
        "gate_stable_IF_speed_bound_and_UTC_interval_complete":len(gate_set)==1,
        "line_stable_IF_speed_bound_and_UTC_interval_complete":len(line_set)==1,
        "gate_and_line_stable_IF_complete":len(possible_gate_lines)==1,
        "real_human_claim_admissible":False,
        "full_historical_Sun_max_speed_independently_proved":False,
        "local_birth_timezone_and_clock_quality_verified":False,
        "input_is_synthetic":True,
    }


def synthetic_calendar_stability(ephemeris_dir:Path)->dict:
    p=ephemeris_dir.expanduser().resolve()
    provider=SwissEphemerisProvider((p/"sepl_18.se1",p/"semo_18.se1"))
    bound=provider.max_abs_speed_degrees_per_day(CelestialBody.SUN)
    if not Decimal("1.0")<=_decimal(bound)<=Decimal("1.1"):
        raise ValueError("upstream Sun speed contract unexpectedly altered")
    cursor=datetime(2020,1,1,12,tzinfo=UTC)
    last=datetime(2021,1,1,12,tzinfo=UTC)
    results=[]
    while cursor<last:
        pos=provider.position(CelestialBody.SUN,cursor)
        positions={}
        for hours in WINDOWS:
            e=source_sun_line_enclosure(
                center_longitude=pos.longitude,
                hours_width=hours,max_abs_speed_deg_per_day=bound)
            positions[str(hours)] = {
                "possible_line_numbers":e["possible_line_numbers"],
                "possible_gate_numbers":e["possible_gate_numbers"],
                "gate_stable":e["gate_stable_IF_speed_bound_and_UTC_interval_complete"],
                "line_stable":e["line_stable_IF_speed_bound_and_UTC_interval_complete"],
                "gate_and_line_stable":e["gate_and_line_stable_IF_complete"],
                "possible_gate_line_count":len(e["possible_gate_line_pairs"]),
            }
        results.append({
            "synthetic_UTC_midpoint":cursor.isoformat(),
            "actual_strict_Swiss_Sun_longitude":pos.longitude,
            "reported_Sun_max_speed_deg_day":bound,
            "windows_hours":positions
        })
        cursor+=timedelta(days=1)
    if len(results)!=366:raise AssertionError("expected 366 leap-year UTC noon cases")
    checks={}
    for hours in WINDOWS:
        x=[r["windows_hours"][str(hours)] for r in results]
        checks[str(hours)] = {
            "synthetic_midpoints":len(x),
            "conditionally_stable_gene_key_numbers":sum(a["gate_stable"] for a in x),
            "conditionally_stable_lines":sum(a["line_stable"] for a in x),
            "conditionally_stable_joint_gate_line":sum(a["gate_and_line_stable"] for a in x),
            "ambiguous_line_midpoints":sum(not a["line_stable"] for a in x),
        }
    body={
        "schema":"HUMANDESIGN_G38_SYNTHETIC_2020_SUN_LINE_TIME_UNCERTAINTY_V1",
        "source":"Incumbent strict local Swiss .se1 Sun and Rave Mandala exact geometry",
        "owner_birth_or_other_person_data_used":False,
        "calendar":"2020_leap_year_366_synthetic_midpoint_instants",
        "Sun_declared_max_speed_deg_day":bound,
        "max_speed_not_independently_proved_across_the_actual_human_cohort":True,
        "Sun_equal_line_width_deg":str(LINE),
        "Sun_equal_gene_key_width_deg":str(GATE),
        "source_ephemeris_hashes":sorted({f.sha256 for f in provider.metadata.files}),
        "house_or_prenatal_Design_required_for_natal_Sun_line":False,
        "Gene_Keys_official_profile_parity_verified":False,
        "zero_real_births_and_zero_human_outcomes":True,
        "window_hour_counts":checks,
        "synthetic_midpoints":results
    }
    body["source_research_digest_sha256"]=hashlib.sha256(
        json.dumps(body,ensure_ascii=False,sort_keys=True,
                   separators=(",",":")).encode()).hexdigest()
    return body


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--ephemeris-dir",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    data=synthetic_calendar_stability(args.ephemeris_dir)
    args.out.write_text(json.dumps(data,indent=2,sort_keys=True,
                                   ensure_ascii=False)+"\n")
    print("G38_CONDITIONAL_SYNTHETIC_SUN_TIME_WINDOWS",data["window_hour_counts"])
