#!/usr/bin/env python3
"""Janson §10 exact almanac arithmetic, structural/synthetic checks.

This does NOT demonstrate physical ephemeris accuracy, ritual effects,
or predictive human validity. Separated source policies are mandatory.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
from datetime import date
import importlib.util
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
P=ROOT/"batches/T58/tibetan_almanac.py"
spec=importlib.util.spec_from_file_location("tibetan_almanac_test",P)
assert spec and spec.loader
al=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=al
spec.loader.exec_module(al)
t=al.t54

def must_raise(fn,*args,**kwargs):
    try: fn(*args,**kwargs)
    except ValueError: return
    raise AssertionError(f"Expected invalid input rejection: {fn} {args} {kwargs}")

# Direct, bounded pass over new source annotations without changing prior 500.
notes=json.loads((ROOT/"batches/T57/JANSON_ALMANAC_22_SOURCE_NOTES_V1.json").read_text())
assert notes["count"]==22
assert [q["id"] for q in notes["notes"]]==[f"TIB-R{x:04d}" for x in range(501,523)]
assert all(q["source_id"]=="TIB-JANSON-2014" and q["required_inputs"] for q in notes["notes"])
assert all(q["actual_real_human_outcome_validated"] is False
           and q["production_model_promoted"] is False for q in notes["notes"])
assert notes["historical_human_prediction_successes"]==0

# Janson 10(viii): 60 named positions, exactly 4 fixed, 7 cyclic changing.
half=[al.karana_from_half_position(k) for k in range(1,61)]
fixed=[k.half_position for k in half if k.fixed]
assert fixed==[1,58,59,60]
assert len({k.type_id for k in half})==11
assert Counter(k.type_id for k in half if not k.fixed)=={
    f"changing_{k}":8 for k in range(1,8)
}
assert al.karana_for_tithi(1)[0].type_id=="fixed_1"
assert al.karana_for_tithi(29)[1].type_id=="fixed_58"
assert al.karana_for_tithi(30)[0].type_id=="fixed_59"
assert al.karana_for_tithi(30)[1].type_id=="fixed_60"
assert al.karana_for_tithi(29)[0].type_id=="changing_7"
for k in (-10,0,61,True,2.0):
    must_raise(al.karana_from_half_position,k)

# Exact mixed radix truncation: 27 stations; negative/wrapped longitudes
# and normalization roundtrips; source is truncation, never decimal rounding.
assert al.mixed_radix_truncate(F(1000,1001)*27,top_radix=27,
                              lower_radices=(60,60,6,67),number_terms=1)==(26,)
assert al.mixed_radix_truncate(F(1,2)*27,top_radix=27,
                              lower_radices=(60,60,6,67),number_terms=3)==(13,30,0)
assert al.mixed_radix_truncate(F(-1,2)*27,top_radix=27,
                              lower_radices=(60,60,6,67),number_terms=3)==(13,30,0)
assert al.mixed_radix_truncate(F(27),top_radix=27,
                              lower_radices=(60,60,6,67),number_terms=3)==(0,0,0)
must_raise(al.mixed_radix_truncate,F(1,2),top_radix=27,
           lower_radices=(60,),number_terms=4)

# T54 guaranteed civil days normal, skipped and repeated. The almanac must
# preserve true fractional-day weekday and approximate Moon start-of-day
# for actual dates WITHOUT silently assigning a calendar date to skipped tithis.
samples={"normal":None,"skipped":None,"leap_first":None,"leap_second":None}
count=0
for system,epoch in (("phugpa",1987),("tsurphu",1852)):
    for yr in (1985,2000,2024,2026):
        for month in range(1,13):
            for _, leap_m in t.month_instances(yr,month,system=system,epoch=epoch):
                dd=t.month_days(yr,month,leap_month=leap_m,system=system,
                                epoch=epoch,anomaly_policy="rounded")
                for item in dd:
                    label=("skipped" if item.skipped else
                           "leap_first" if item.leap_day else "normal")
                    entry=al.almanac_for_tibetan_day(
                        item.year,item.month,item.lunar_day,leap_month=item.leap_month,
                        leap_day=item.leap_day,system=system,epoch=epoch,
                        anomaly_policy="rounded",karana_time_policy="undetermined")
                    count+=1
                    assert entry.calendar_jdn==item.jdn
                    assert entry.skipped==item.skipped
                    assert entry.karana_at_dawn_id is None
                    assert 0<=entry.tithi_end_true_weekday<7
                    assert 0<=entry.model_true_sun_circle<1
                    assert 0<=entry.model_moon_tithi_end_circle<1
                    assert entry.model_moon_tithi_end_circle == (
                        entry.model_true_sun_circle+F(item.lunar_day,30))%1
                    assert entry.tithi_end_fraction == (entry.tithi_end_true_weekday%1)
                    if label=="skipped":
                        assert entry.mansion_index_0_to_26 is None
                        assert entry.model_moon_calendar_start_circle is None
                        assert entry.yoga_circle is None
                        assert entry.yoga_index_0_to_26 is None
                        assert entry.weekday_number is None
                    else:
                        assert 0<=entry.model_moon_calendar_start_circle<1
                        assert 0<=entry.yoga_circle<1
                        assert 0<=entry.mansion_index_0_to_26<27
                        assert 0<=entry.yoga_index_0_to_26<27
                        assert entry.mansion_index_0_to_26 == (27*entry.model_moon_calendar_start_circle).__floor__()
                        assert entry.yoga_index_0_to_26 == (27*entry.yoga_circle).__floor__()
                        assert entry.yoga_circle == (
                            entry.model_moon_calendar_start_circle +
                            entry.model_true_sun_circle)%1
                        assert entry.weekday_number==(item.jdn+2)%7
                        assert entry.weekday_name in ("Saturday","Sunday","Monday",
                           "Tuesday","Wednesday","Thursday","Friday")
                        assert entry.mansion_mixed_radix(3)[0]==entry.mansion_index_0_to_26
                        assert entry.yoga_mixed_radix(3)[0]==entry.yoga_index_0_to_26
                        if item.leap_day:
                            assert entry.weekday_mixed_radix()==(entry.weekday_number,60,0)
                            assert entry.model_moon_calendar_start_circle == (
                                entry.model_moon_tithi_end_circle-F(1,27))%1
                        else:
                            assert entry.model_moon_calendar_start_circle == (
                                entry.model_moon_tithi_end_circle -
                                entry.tithi_end_fraction/F(27))%1
                    if samples[label] is None: samples[label]=(item,entry)
                    if label=="leap_first":
                        partner=next(q for q in dd if q.lunar_day==item.lunar_day
                                     and not q.leap_day and not q.skipped)
                        second=al.almanac_for_tibetan_day(
                           partner.year,partner.month,partner.lunar_day,
                           leap_month=partner.leap_month,leap_day=False,
                           system=system,epoch=epoch,anomaly_policy="rounded",
                           karana_time_policy="undetermined")
                        assert second.model_true_sun_circle==entry.model_true_sun_circle
                        assert second.model_moon_tithi_end_circle==entry.model_moon_tithi_end_circle
                        assert second.model_moon_calendar_start_circle!=entry.model_moon_calendar_start_circle
                        if samples["leap_second"] is None:samples["leap_second"]=(partner,second)
assert all(samples.values()),samples

# Hour-of-day karana is NOT determined by index alone. A named equal-duration
# policy reconstructs a conditional category and must not be automatic.
first=samples["normal"][0]
undefined=al.almanac_for_tibetan_day(
   first.year,first.month,first.lunar_day,leap_month=first.leap_month,
   leap_day=first.leap_day,system="phugpa",epoch=1987,anomaly_policy="rounded",
   karana_time_policy="undetermined")
specified=al.almanac_for_tibetan_day(
   first.year,first.month,first.lunar_day,leap_month=first.leap_month,
   leap_day=first.leap_day,system="phugpa",epoch=1987,anomaly_policy="rounded",
   karana_time_policy="henning_equal_duration")
assert undefined.karana_at_dawn_id is None
assert specified.karana_at_dawn_id in {f"fixed_{h}" for h in (1,58,59,60)} | {
    f"changing_{h}" for h in range(1,8)}
must_raise(al.almanac_for_tibetan_day,first.year,first.month,
   first.lunar_day,leap_month=first.leap_month,leap_day=first.leap_day,
   system="phugpa",epoch=1987,anomaly_policy="rounded",karana_time_policy="unknown")
must_raise(al.almanac_for_civil_day,"2454102",system="phugpa",epoch=1987,
           anomaly_policy="rounded",karana_time_policy="undetermined")

# Cross-bind one accepted source day known from Cornu 1950; no personal outcomes.
paris=al.almanac_for_civil_day(2433601,system="phugpa",epoch=1987,
                               anomaly_policy="rounded",
                               karana_time_policy="undetermined")
assert (paris.year,paris.month,paris.lunar_day)==(1950,10,6)

# Upstream previous 500 source IDs and their Janson calendar parity still pass.
upstream=subprocess.run(["python3",str(ROOT/"verify_t54_t56_all.py")],
   text=True,capture_output=True,check=True)
assert "500 contiguous" in upstream.stdout
print("T57–T58 ALMANAC SOURCE PASS:",notes["count"],
      "nonduplicated annotations TIB-R0501–0522;",count,
      "sampled source calendar-day/skip/duplicate cases;")
print("  zero clinical efficacy, physical ephemeris accuracy or real human")
print("  predictive successes established. All previous 500 historical IDs intact.")
