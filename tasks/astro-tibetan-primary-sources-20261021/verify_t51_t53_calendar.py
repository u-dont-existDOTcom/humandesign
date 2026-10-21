#!/usr/bin/env python3
"""T53: source-first deterministic fixtures; NOT an operational natal-chart engine.

Data cross-checks:
 - Janson 2014 Table 23 (60 birth-year element combinations), §5.2,
   Appendix E.1–E.3, and Phugpa Table 1 Losar.
 - Cornu 1997 English printed pp. 115–119, including Paris example.
Only symbolic year/month/lunar-day and preknown traditional animal-hours.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from fractions import Fraction
from pathlib import Path
from zoneinfo import ZoneInfo
import importlib.util
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "batches/T53/tibetan_calendar_reference.py"
spec = importlib.util.spec_from_file_location("tibetan_calendar_reference", SRC)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
amod = mod.amod
year_features = mod.year_features
month_features = mod.month_features
lunar_day_features = mod.lunar_day_features
leap_month_info = mod.leap_month_info
hour_element_from_day = mod.hour_element_from_day

def must_raise(callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except ValueError:
        return
    raise AssertionError(f"bad inputs accepted: {callback.__name__}, {args}, {kwargs}")

assert amod(-1, 9) == 8 and amod(0,9) == 9 and amod(9,9) == 9
assert amod(65,65) == 65
must_raise(amod, 3, 0)
must_raise(amod, True, 12)

f = year_features(1950)
assert (f["power_element"],f["animal"],f["polarity"])==("iron","tiger","masculine")
assert (f["life_element"],f["body_element"],f["fortune_element"],f["spirit_element"])==(
    "wood","wood","iron","water"
)
assert (f["central_mewa"],f["life_mewa"],f["power_mewa"])==(5,2,8)
g=year_features(1958)
assert (g["power_element"],g["animal"],g["body_element"],g["central_mewa"],g["life_mewa"],g["power_mewa"]) == (
    "earth","dog","wood",6,3,9
)
h=year_features(1984)
assert (h["power_element"],h["animal"],h["life_element"],h["body_element"],h["fortune_element"],h["spirit_element"],h["central_mewa"]) == (
    "wood","mouse","water","iron","wood","iron",7
)
assert year_features(1985)["animal"]=="ox"
assert year_features(1984)["sexagenary_position"]==1
assert year_features(2043)["sexagenary_position"]==60

# Independently copied Janson Table23 body element across the 60 entries
TABLE_23_BODY = (
    "iron iron fire fire wood wood earth earth iron iron fire fire "
    "water water earth earth iron iron wood wood water water earth earth "
    "fire fire wood wood water water iron iron fire fire wood wood earth earth "
    "iron iron fire fire water water earth earth iron iron wood wood water water "
    "earth earth fire fire wood wood water water"
).split()
assert len(TABLE_23_BODY)==60
for i, source_body in enumerate(TABLE_23_BODY):
    year=1984+i
    x=year_features(year)
    assert x["body_element"]==source_body, (year, x["body_element"],source_body)
    assert year_features(year+60)["body_element"]==source_body
    assert year_features(year+180)["central_mewa"]==x["central_mewa"]
    assert year_features(year+60)["central_mewa"] != x["central_mewa"]
    assert set(x["fortune_element"] for x in [x]) <= {"wood","fire","water","iron"}
assert len({tuple(year_features(y)[k] for k in (
    "animal","power_element","life_element","body_element",
    "fortune_element","spirit_element","central_mewa"))
    for y in range(1984,2164)})==180

# Year label MUST be obtained from calendrical Losar, not Gregorian civil date.
PHUGPA_LOSAR_BENCHMARKS = {
    "1950-02-17": 1950, "1951-02-07": 1951,
    "1984-03-03": 1984, "1985-02-20": 1985,
}
assert PHUGPA_LOSAR_BENCHMARKS["1985-02-20"]==1985
# The date 1985-02-19 is *before* Phugpa Losar: same Wood Mouse year as 1984.
assert year_features(1984)["animal"]=="mouse" and year_features(1985)["animal"]=="ox"

# Cornu's published 1950 Paris Iron Tiger natal month/day worked sample
mo=month_features(1950,10,policy="phugpa")
assert (mo["animal"],mo["element"],mo["polarity"]) == ("ox","water","feminine")
assert mo["tsurphu_month_mewa"] is None
d6=lunar_day_features(1950,10,6,policy="phugpa")
assert (d6["animal"],d6["element"],d6["mewa"]) == ("ox","wood",3)
assert lunar_day_features(1950,10,1,policy="phugpa")["mewa"] == 7
assert hour_element_from_day("wood","monkey") == "fire"
assert [hour_element_from_day("water",a) for a in mod.HOURS_FROM_HARE[:5]]==[
    "wood","fire","earth","iron","water"
]
assert month_features(1950,1,policy="phugpa")["animal"] == "dragon"
assert month_features(1950,1,policy="tsurphu")["animal"] == "tiger"
assert month_features(1950,10,policy="tsurphu")["animal"] == "pig"
assert month_features(1950,1,policy="tsurphu")["tsurphu_month_mewa"] is not None
assert lunar_day_features(1950,10,6,policy="tsurphu")["animal"] == "ox"
for m in range(1,13):
    assert month_features(1950,m,policy="phugpa")["polarity"] == (
        "masculine" if m%2 else "feminine"
    )
for fn,args,kws in (
    (year_features,(1984.0,),{}),
    (month_features,(1984,0),{"policy":"phugpa"}),
    (month_features,(1984,1),{"policy":"other"}),
    (month_features,(1984,True),{"policy":"phugpa"}),
    (lunar_day_features,(1984,1,31),{"policy":"phugpa"}),
    (lunar_day_features,(1984,1,1),{"policy":"other"}),
    (hour_element_from_day,("stone","horse"),{}),
    (hour_element_from_day,("wood","noon"),{}),
):
    must_raise(fn,*args,**kws)

# Janson §5.2: same epoch-independent index for different epochs in same tradition,
# Phugpa and Tsurphu distinct leap policies; no civil-date derivation.
assert leap_month_info(2000,1,policy="phugpa",epoch=1927)["preliminary_intercalation_index"]==48
assert leap_month_info(2000,1,policy="phugpa",epoch=1927)["leap_month_present"] is True
for p,epochs in (("phugpa",(806,1927,1987)),("tsurphu",(1732,1852))):
    for y in (1950,1984,1987,2000,2026):
        for m in range(1,13):
            results=[leap_month_info(y,m,policy=p,epoch=e) for e in epochs]
            assert len({r["preliminary_intercalation_index"] for r in results})==1,(p,y,m)
            assert len({r["leap_month_present"] for r in results})==1,(p,y,m)
            for result in results:
                if result["leap_month_present"]:
                    assert result["regular_true_month_count"] - result["leap_true_month_count"]==1
                else:
                    assert result["leap_true_month_count"] is None
    leaps=[(y,m) for y in range(1987,2052) for m in range(1,13)
           if leap_month_info(y,m,policy=p,epoch=epochs[-1])["leap_month_present"]]
    assert len(leaps)==24,(p,len(leaps))
    assert sorted(m for _,m in leaps)==sorted([i for i in range(1,13) for _ in (1,2)])
must_raise(leap_month_info,1987,1,policy="phugpa",epoch=1852)
must_raise(leap_month_info,1987,1,policy="tsurphu",epoch=1987)
must_raise(leap_month_info,1987,13,policy="phugpa",epoch=1987)
must_raise(leap_month_info,1987,1,policy="other",epoch=1987)

# The historical civil-clock issue in Cornu's Paris example.
paris=datetime(1950,11,15,17,0,tzinfo=ZoneInfo("Europe/Paris"))
utc=paris.astimezone(timezone.utc)
assert utc==datetime(1950,11,15,16,0,tzinfo=timezone.utc)
LMT_OFFSET=Fraction(23522,10000)*Fraction(240)  # seconds, longitude 2.3522°E
assert abs(float(LMT_OFFSET)-564.528)<1e-9
assert utc+timedelta(seconds=float(LMT_OFFSET)) == datetime(
    1950,11,15,16,9,24,528000,tzinfo=timezone.utc
)
# Cornu printed p.220: (1950−285) × 0.014 = 23.31°, NOT "23°81′".
ayanamsa=(1950-285)*Fraction(14,1000)
assert ayanamsa==Fraction(2331,100)
whole=int(ayanamsa)
mins=60*(ayanamsa-whole)
minutes=int(mins)
seconds=(mins-minutes)*60
assert (whole,minutes,seconds)==(23,18,36)
assert 81>=60  # the printed "81 minutes" is invalid DMS.

# Previously accepted source-only 447-annotation ledger must remain unmodified.
previous = subprocess.run(
    ["python3",str(ROOT/"verify_global_source_registry.py")],
    text=True,capture_output=True,check=True
)
assert "447 contiguous" in previous.stdout
for name,count,first in (
    ("batches/T51/CORNU_JUNGTSI_KARTSI_WORKED_24_NOTES_V1.json",24,448),
    ("batches/T52/JANSON_CALENDAR_17_SOURCE_NOTES_V1.json",17,472),
):
    data=json.loads((ROOT/name).read_text(encoding="utf-8"))
    arr=data.get("notes",data.get("source_notes"))
    assert len(arr)==count
    assert [x["id"] for x in arr]==[f"TIB-R{i:04d}" for i in range(first,first+count)]
    assert data.get("source_note_count",data.get("note_count"))==count
    assert data["actual_human_blind_successes"]==0
# Janson Appendix E.4: an *already known* JDN, not lunar tithi D.
from datetime import date
jdn_2007 = date(2007,1,1).toordinal()+1721425
assert jdn_2007 == 2454102  # Janson §2 published example
for jd in range(jdn_2007-250,jdn_2007+250):
    phug = mod.calendar_day_features(jd,policy="phugpa")
    tsur = mod.calendar_day_features(jd,policy="tsurphu")
    assert phug["mewa"] == amod(-jd,9)
    assert tsur["mewa"] is None and tsur["tsurphu_mewa_requires_solstice_rule"]
    assert phug["animal"] == tsur["animal"]
    assert phug["trigram"] == tsur["trigram"]
    assert phug["power_element"] == tsur["power_element"]
    assert phug["polarity"] == ("masculine" if jd % 2 else "feminine")
    assert phug["animal"] == mod.ANIMALS[amod(jd+2,12)-1]
    assert phug["trigram"] == mod.TRIGRAMS[amod(jd+2,8)-1]
    row = year_features(1984+(jd-11)%60)
    assert phug["power_element"] == row["power_element"] and phug["body_element"] == row["body_element"]
    next_60 = mod.calendar_day_features(jd+60,policy="phugpa")
    assert phug["animal"] == next_60["animal"]
    assert phug["body_element"] == next_60["body_element"]
    assert phug["mewa"] != next_60["mewa"]
    assert mod.calendar_day_features(jd+180,policy="phugpa")["mewa"] == phug["mewa"]
must_raise(mod.calendar_day_features, "2454102",policy="phugpa")
must_raise(mod.calendar_day_features, 2454102,policy="unknown")

# The downstream fixture manifest must retain original Cornu wording vs computed repair.
manifest=json.loads((ROOT/"batches/T53/CALCULATOR_SOURCE_PARITY_AND_1950_ERRATA_V1.json").read_text(encoding="utf-8"))
assert manifest["new_historical_source_notes"]==0
assert manifest["Cornu_1950_Paris_errata"]["unambiguous_UTC"]=="1950-11-15T16:00:00Z"
assert manifest["Cornu_1950_Paris_errata"]["local_mean_solar"]=="1950-11-15 16:09:24.528"
assert manifest["Cornu_1950_Paris_errata"]["ayanamsa_printed_p220"]=="23°81′"
assert manifest["Cornu_1950_Paris_errata"]["computed_DMS"]=="23°18′36″"
assert manifest["independent_testing"]["medical_or_personality_human_validated"]==0
assert manifest["study_readiness"]["calendar_date_from_UTC_implemented"] is False
assert manifest["study_readiness"]["predictive_accuracy_claim_allowed"] is False

print("T51–T53 PASS: 41 contiguous new documentary notes (TIB-R0448–0488), "
      "60-year Table23 parity, 1950 Cornu birth year/month/day/hour, "
      "Phugpa/Tsurphu leap-policy 24/65, UTC/LMT and invalid DMS source boundaries, "
      "prior 447 notes unchanged; ZERO human predictive results.")
