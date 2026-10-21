#!/usr/bin/env python3
"""Bounded historical source and arithmetic verification, T62–T66.

Janson Appendix D and Henning 2007 Chapter II/Chapter V calculations. This
confirms source arithmetic and independent worked-book examples; it is NOT a
physical sky ephemeris test and absolutely not human prediction validation.
"""
from datetime import date
from fractions import Fraction as F
from pathlib import Path
from subprocess import run
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parent


def read(path: str):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))


for path,start,count in (
    ("batches/T62/HENNING_KALACAKRA_TRANSLATION_16_NOTES_V1.json",543,16),
    ("batches/T63/HENNING_KALACAKRA_TRANSLATION_16_NOTES_V1.json",559,16),
    ("batches/T64/JANSON_PLANET_APPENDIX_16_NOTES_V1.json",575,16),
):
    data=read(path)
    assert data["note_count"] == count, path
    notes=data["notes"]
    assert len(notes)==count
    assert [x["id"] for x in notes]==[f"TIB-R{i:04d}" for i in range(start,start+count)],path
    assert all(x["source_id"] in ("TIB-JANSON-2014","TIB-HENNING-2007") for x in notes)
    assert all(x["human_validated"] is False for x in notes)
e=read("batches/T66/PLANETARY_SOLAR_EPOCH_CONFLICT_V1.json")
assert e["note_count"]==1
assert [v["id"] for v in e["new_source_notes"]]==["TIB-R0591"]
assert e["issue_id"]=="TIB-CONFLICT-012"
assert e["production_runtime_promotions"]==0
# No participant or real human result is needed to establish this arithmetic.
issue=e["source_values"]
num=issue["mixed_radix_digits"]
rad=issue["radix_units"]
source_mixed=(F(num[0])+F(num[1],rad[1])+
              F(num[2],rad[1]*rad[2])+
              F(num[3],rad[1]*rad[2]*rad[3])+
              F(num[4],rad[1]*rad[2]*rad[3]*rad[4]))/rad[0]
assert source_mixed==1-F(458672,6714405)
assert source_mixed!=1-F(458772,6714405)
delta=F(100,6714405)*360*3600
assert 19 < float(delta) < 20

SRC=ROOT/"batches/T65/planetary_phugpa_E1927.py"
spec=importlib.util.spec_from_file_location("tibetan_planets_source_t65",SRC)
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=m
spec.loader.exec_module(m)

# Compare Henning's actual printed 1 March 1995 worked example, NOT a modern
# ephemeris. Original user's PDF: Ch II printed pp57–87 (= PDF pp77–107).
jdn=date(1995,3,1).toordinal()+1721425
assert jdn==2449778
expected={
    "Mercury":{"part":4485,"helio":(13,45,55),"fast":(20,49,16)},
    "Venus":{"part":1191,"helio":(14,18,39),"fast":(19,38,58)},
    "Mars":{"part":231,"helio":(9,4,42),"slow":(9,9,23),"fast":(8,58,24)},
    "Jupiter":{"part":2778,"helio":(17,18,51),"slow":(16,57,46),"fast":(17,45,33)},
    "Saturn":{"part":9560,"helio":(23,58,31),"slow":(23,17,35),"fast":(23,14,23)},
}
correct=m.five_planets_at_JDN(jdn,system="phugpa",epoch=1927,
        solar_epoch_policy="henning_and_Janson_mixed_radix_458672")
literal=m.five_planets_at_JDN(jdn,system="phugpa",epoch=1927,
        solar_epoch_policy="janson_D9_literal_458772")
assert len(correct)==len(literal)==5
assert [x.planet for x in correct]==["Mercury","Venus","Mars","Jupiter","Saturn"]
assert all(x.general_day==24806 for x in correct)
assert m.circle_to_mansions_3(correct[0].mean_sun_circle)==(22,45,37)
assert correct[0].mean_sun_circle==(F(24806*18382-458672,6714405))%1
assert literal[0].mean_sun_circle==(F(24806*18382-458772,6714405))%1
assert correct[0].mean_sun_circle!=literal[0].mean_sun_circle
for p in correct:
    rule=expected[p.planet]
    assert p.solar_epoch_policy=="henning_and_Janson_mixed_radix_458672"
    assert p.particular_day==rule["part"],p
    assert m.circle_to_mansions_3(p.mean_heliocentric_circle)==rule["helio"],p
    if "slow" in rule:
        assert m.circle_to_mansions_3(p.true_slow_circle)==rule["slow"],p
    assert m.circle_to_mansions_3(p.traditional_geocentric_circle)==rule["fast"],p
    assert 0<=p.traditional_geocentric_circle<1
    assert p.longitude_degrees==p.traditional_geocentric_circle*360
assert m.circle_to_mansions_3(literal[0].traditional_geocentric_circle)==(20,49,15)
assert m.circle_to_mansions_3(literal[2].traditional_geocentric_circle)==(8,58,26)

# Rahu is a 6900 LUNAR-day retrograde model; never substitute solar days.
for year,month,d in ((1984,3,1),(1995,1,1),(2000,11,9),(2026,9,15)):
    a=m.rahu_at_lunar_day(year,month,d,leap_month=False,system="phugpa",epoch=1927)
    b=m.rahu_at_lunar_day(year,month,d,leap_month=False,system="phugpa",epoch=1987)
    assert a.head_longitude_circle==b.head_longitude_circle,(a,b)
    assert a.tail_longitude_circle==b.tail_longitude_circle
    assert (a.head_longitude_circle+F(1,2))%1==a.tail_longitude_circle
    assert a.head_longitude_circle==(-F(a.elapsed_lunar_days,6900))%1

def reject(fn,*args,**kwargs):
    try:fn(*args,**kwargs)
    except ValueError:return
    raise AssertionError(f"Accepted invalid source policy: {fn},{args},{kwargs}")

reject(m.five_planets_at_JDN,jdn,system="tsurphu",epoch=1852,
       solar_epoch_policy="henning_and_Janson_mixed_radix_458672")
reject(m.five_planets_at_JDN,jdn,system="phugpa",epoch=1987,
       solar_epoch_policy="henning_and_Janson_mixed_radix_458672")
reject(m.five_planets_at_JDN,jdn,system="phugpa",epoch=1927,
       solar_epoch_policy="auto")
reject(m.five_planets_at_JDN,2449778.0,system="phugpa",epoch=1927,
       solar_epoch_policy="janson_D9_literal_458772")
reject(m.rahu_at_lunar_day,1995,1,31,leap_month=False,system="phugpa",epoch=1927)
reject(m.rahu_at_lunar_day,1995,1,1,leap_month=False,system="tsurphu",epoch=1852)
reject(m.rahu_at_lunar_day,1995,1,1,leap_month="unknown",system="phugpa",epoch=1927)
root=run(["python3",str(ROOT/"verify_t61_henning_caption.py")],
         check=True,text=True,capture_output=True)
assert "HENNING CAPTION SOURCE PASS" in root.stdout
print("T62–T66 HISTORICAL/MATH SOURCE PASS: 49 new source notes TIB-R0543–0591;")
print("  five planetary model longitudes and 1 March 1995 Henning printed work,")
print("  Rahu epoch parity, Janson D.9 corrected mixed-radix source issue;")
print("  previously accepted 542 document annotations remain source-only.")
