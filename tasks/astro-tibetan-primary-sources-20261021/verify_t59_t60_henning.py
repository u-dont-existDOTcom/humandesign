#!/usr/bin/env python3
"""Henning Chapter IV/App I source naming: 10 vs 27 vs 28 yogas and karaṇa.

The mathematical almanac continues to come from Janson T58. This test checks
source naming and explicit tradition differences, not source accuracy in human
forecasts, physical ephemerides or real-life event tests.
"""
from __future__ import annotations

from pathlib import Path
from collections import Counter
from datetime import date
import importlib.util
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def load(path, name):
 spec=importlib.util.spec_from_file_location(name,path)
 assert spec and spec.loader
 obj=importlib.util.module_from_spec(spec)
 sys.modules[spec.name]=obj
 spec.loader.exec_module(obj)
 return obj

hn=load(ROOT/"batches/T60/henning_almanac_names.py","henning_names_test")
al=load(ROOT/"batches/T58/tibetan_almanac.py","tibetan_almanac_henning_test")
doc=json.loads((ROOT/"batches/T59/HENNING_ALMANAC_20_SOURCE_NOTES_V1.json").read_text())
assert doc["note_count"]==20
assert [z["id"] for z in doc["notes"]]==[f"TIB-R{i:04d}" for i in range(523,543)]
assert all(z["source_id"]=="TIB-HENNING-2007" and z["required_inputs"]
           and z["human_outcome_validated"] is False
           and z["model_promoted"] is False for z in doc["notes"])
assert doc["human_prediction_tests"]==doc["model_promotions"]==0

assert len(hn.MANSION_TIBETAN_27)==len(hn.MANSION_ELEMENTS_27)==27
assert len(hn.ANGULAR_YOGA_PHUGPA_27)==27
assert len(hn.ELEMENTAL_YOGAS)==10
assert len(hn.CHANGING_KARANA_7)==7
assert len(hn.FIXED_KARANA_BY_H)==4
assert hn.mansion_name(3,name_tradition="tibetan_27")=="Rohiṇī"
assert hn.MANSION_ELEMENTS_27[3]=="earth"
assert hn.mansion_name(21,name_tradition="tibetan_27")=="Śravaṇa"
assert hn.mansion_name(21,name_tradition="indian_27")=="Abhijit"
assert all(hn.mansion_name(i,name_tradition="tibetan_27")==
           hn.mansion_name(i,name_tradition="indian_27")
           for i in range(27) if i!=21)
assert hn.MANSION_ELEMENTS_27[21]=="earth"
assert hn.angular_yoga_name(0,calendar_policy="phugpa")=="Viṣkambha"
assert hn.angular_yoga_name(0,calendar_policy="tsurphu")=="Vaidhṛti"
assert hn.angular_yoga_name(1,calendar_policy="tsurphu")=="Viṣkambha"
assert hn.angular_yoga_name(26,calendar_policy="phugpa")=="Vaidhṛti"
assert set(hn.angular_yoga_name(i,calendar_policy="tsurphu")
           for i in range(27))==set(hn.ANGULAR_YOGA_PHUGPA_27)

# Henning's explicit pp203–204 example Saturday+Rohini => earth+earth Siddhi.
assert hn.elemental_yoga_name(0,3)=="Siddhi"
# All 7 weekdays x 27 mansions produce exactly 10 unordered categories.
seen={hn.elemental_yoga_name(w,m) for w in range(7) for m in range(27)}
assert len(seen)==10
assert len({frozenset((a,b)) for a,b in hn.ELEMENTAL_YOGAS})==10
assert hn.elemental_yoga_name(2,19)=="Amṛta"  # Monday Water, lunar mansion19 Water
for invalid in (-1,27,False,"21",28):
 try: hn.mansion_name(invalid,name_tradition="tibetan_27")
 except ValueError: pass
 else: raise AssertionError(invalid)
for invalid in ("unknown",""):
 try: hn.mansion_name(0,name_tradition=invalid)
 except ValueError: pass
 else: raise AssertionError(invalid)

assert [i for i in range(1,61) if i in hn.FIXED_KARANA_BY_H]==[1,58,59,60]
assert hn.karana_names_for_tithi(1)==("Kintughna","Vava")
assert hn.karana_names_for_tithi(29)==("Viṣṭi","Śakuni")
assert hn.karana_names_for_tithi(30)==("Catuṣpada","Nāga")
changed=[hn.karana_name_at_H(i) for i in range(2,58)]
assert Counter(changed)=={name:8 for name in hn.CHANGING_KARANA_7}
assert len(set(hn.karana_name_at_H(i) for i in range(1,61)))==11
for h in range(1,61):
 source=al.karana_from_half_position(h)
 named=hn.karana_name_at_H(h)
 assert source.fixed==(h in (1,58,59,60))
 if source.fixed:
  assert named==hn.FIXED_KARANA_BY_H[h]
 else:
  assert named==hn.CHANGING_KARANA_7[int(source.type_id.split("_")[1])-1]

# One accepted source worked calendar day and another first duplicated day.
data=al.almanac_for_civil_day(2433601,system="phugpa",epoch=1987,
                             anomaly_policy="rounded",
                             karana_time_policy="undetermined")
named=hn.named_day(data,name_tradition="tibetan_27")
assert named is not None
assert named.weekday=="Wednesday"
assert named.weekday_element=="water"
assert named.mansion_element in ("fire","earth","water","wind")
assert named.karana_at_dawn is None
assert named.unknown_other_weekday_mansion_yoga_28 is None
with_karana=al.almanac_for_civil_day(2433601,system="phugpa",epoch=1987,
                                    anomaly_policy="rounded",
                                    karana_time_policy="henning_equal_duration")
assert hn.named_day(with_karana,name_tradition="tibetan_27").karana_at_dawn is not None
for year in (1985,2000,2026):
 for m in (1,3,8):
  for n,is_leap in al.t54.month_instances(year,m,system="phugpa",epoch=1987):
   for item in al.t54.month_days(year,m,leap_month=is_leap,system="phugpa",epoch=1987,
                                 anomaly_policy="rounded"):
    a=al.almanac_for_tibetan_day(year,m,item.lunar_day,leap_month=is_leap,
             leap_day=item.leap_day,system="phugpa",epoch=1987,
             anomaly_policy="rounded",karana_time_policy="undetermined")
    result=hn.named_day(a,name_tradition="tibetan_27")
    if item.skipped:
     assert result is None
    else:
     assert result is not None
     assert result.elemental_yoga_10==hn.elemental_yoga_name(
        a.weekday_number,a.mansion_index_0_to_26)
     assert result.angular_yoga_27==hn.angular_yoga_name(
        a.yoga_index_0_to_26,calendar_policy="phugpa")

out=subprocess.run(["python3",str(ROOT/"verify_t57_t58_almanac.py")],
                   check=True,capture_output=True,text=True)
assert "22 nonduplicated" in out.stdout
print("T59–T60 HENNING SOURCE PASS: 20 new notes, 27 mansion+name policy,")
print("  seven weekday elements, all ten elemental yogas, 27 angular yogas,")
print("  four fixed + seven changing karaṇa names and all 60 halves.")
print("  Separately acknowledged 28 extra weekday-mansion yogas not invented;")
print("  all previous 522 documentary notes/tests green; zero human validation.")
