#!/usr/bin/env python3
"""Source parity only for Henning printed English caption, not small Tibetan digits."""
from datetime import date
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/"batches/T58"),str(ROOT/"batches/T60"),str(ROOT/"batches/T53")]
import tibetan_almanac as a
import henning_almanac_names as h
from tibetan_calendar_reference import year_features
receipt=json.loads((ROOT/"batches/T61/HENNING_CAPTION_2003_JUNE8_SOURCE_FIXTURE_V1.json").read_text())
assert receipt["source_note_increment"]==receipt["human_prediction_tests"]==0
s=receipt["caption_directly_checked"]
assert s["Gregorian_date"]=="2003-06-08" and s["Tibetan_year"]=="Water Sheep"
civil=date.fromisoformat(s["Gregorian_date"])
j=civil.toordinal()+1721425
t=a.t54.gregorian_day_to_tibetan(civil,system="phugpa",epoch=1987,anomaly_policy="rounded")
assert t.jdn==j==2452799
assert (t.year,t.month,t.lunar_day)==(2003,4,8)
yr=year_features(t.year)
assert (yr["power_element"],yr["animal"])==("water","sheep")
z=a.almanac_for_civil_day(j,system="phugpa",epoch=1987,
                         anomaly_policy="rounded",karana_time_policy="undetermined")
n=h.named_day(z,name_tradition="tibetan_27")
assert n.weekday=="Sunday" and n.elemental_yoga_10=="Pragati"
assert (z.mansion_index_0_to_26,z.yoga_index_0_to_26)==(10,13)
assert list(z.mansion_mixed_radix())==receipt["derived_reconstruction_not_quoted_from_printed_table"]["Moon_mixed_radix_3"]
assert list(z.yoga_mixed_radix())==receipt["derived_reconstruction_not_quoted_from_printed_table"]["Yoga_mixed_radix_3"]
assert "NOT been independently decoded" in receipt["audit_boundary"]
subprocess.run(["python3",str(ROOT/"verify_t59_t60_henning.py")],
               check=True,capture_output=True,text=True)
print("T61 HENNING CAPTION SOURCE PASS: 2003-06-08 Water Sheep month4 day8.")
print("Small printed Tibetan numeral columns remain UNVERIFIED; no score claims.")
