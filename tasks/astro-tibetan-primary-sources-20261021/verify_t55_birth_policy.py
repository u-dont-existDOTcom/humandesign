#!/usr/bin/env python3
"""Synthetic and author-published chart fixtures for an EXPLICIT experimental birth
mean-solar-dawn policy. This is not a claim that Tibetan astrologers used a
universal worldwide birthplace procedure, nor predictive human validation.
"""
from datetime import datetime, timezone, timedelta, date
from pathlib import Path
from zoneinfo import ZoneInfo
import importlib.util
import sys
import subprocess

ROOT=Path(__file__).resolve().parent
MOD=ROOT/"batches/T55/natal_mean_dawn_candidate.py"
spec=importlib.util.spec_from_file_location("natal_mean_dawn_candidate_t55",MOD)
assert spec and spec.loader
c=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=c
spec.loader.exec_module(c)
def chart(t,lon=0,policy="project_extension_05_LMT_dawn",system="phugpa",epoch=1987):
    return c.calculate_mean_dawn_candidate(
        utc_instant=t,site_longitude_East=lon,
        mean_dawn_policy=policy,calendar_system=system,
        calendar_epoch=epoch,lunar_anomaly_policy="rounded")

# Independently reconstruct all four pillars from Cornu's 1950 published example.
# Janson date computation, IANA timezone, solar-longitude correction, Cornu elements.
original=datetime(1950,11,15,17,tzinfo=ZoneInfo("Europe/Paris"))
utc=original.astimezone(timezone.utc)
assert utc==datetime(1950,11,15,16,tzinfo=timezone.utc)
p=chart(utc,"2.3522")
assert p.local_mean_solar_clock=="1950-11-15T16:09:24.528"
assert "+00:00" not in p.local_mean_solar_clock  # mean-solar clock is not UTC
assert p.theoretical_dawn_day_label=="1950-11-15"
assert (p.year_label,p.month,p.lunar_day,p.traditional_hour_animal)==(
    1950,10,6,"monkey")
assert p.four_animal_element_pairs==(
    ("tiger","iron"),("ox","water"),("ox","wood"),("monkey","fire")
)
assert p.five_year_forces=={
    "life":"wood","body":"wood","power":"iron",
    "fortune":"iron","spirit":"water"
}
assert p.year_mewa==5 and p.lunar_day_mewa==3

# A theoretical mean-LMT dawn is a deliberately required explicit policy.
# Gregorian day label 2026-02-18 begins at mean-solar 05:00, not midnight.
before=chart(datetime(2026,2,18,4,59,tzinfo=timezone.utc))
after=chart(datetime(2026,2,18,5,0,tzinfo=timezone.utc))
assert before.theoretical_dawn_day_label=="2026-02-17"
assert after.theoretical_dawn_day_label=="2026-02-18"
assert before.traditional_hour_animal=="tiger"
assert after.traditional_hour_animal=="hare"
assert before.year_label==2025
assert after.year_label==2026
assert before.four_animal_element_pairs[0]==("snake","wood")
assert after.four_animal_element_pairs[0]==("horse","fire")

# A nonzero longitude shifts the *explicit hypothesis* day boundary, not UTC.
at_0=chart(datetime(2024,2,10,5,0,tzinfo=timezone.utc),0)
at_west=chart(datetime(2024,2,10,5,0,tzinfo=timezone.utc),"-17.45")
assert at_0.theoretical_dawn_day_label=="2024-02-10"
assert at_west.theoretical_dawn_day_label=="2024-02-09"
assert at_0.year_label==2024 and at_west.year_label==2023
assert at_west.traditional_hour_animal=="tiger"

# Explicit Phugpa/Tsurphu alternates may yield different month signs.
x=datetime(1984,3,5,16,tzinfo=timezone.utc)
ph=chart(x,"2.3522",system="phugpa",epoch=1987)
ts=chart(x,"2.3522",system="tsurphu",epoch=1852)
assert ph.four_animal_element_pairs[0] == ts.four_animal_element_pairs[0]
assert ph.four_animal_element_pairs[1] != ts.four_animal_element_pairs[1]
assert (ph.calendar_system,ts.calendar_system)==("phugpa","tsurphu")

def fails(**kw):
    try:
        c.calculate_mean_dawn_candidate(**kw)
    except ValueError:
        return
    raise AssertionError(f"Invalid input wrongly admitted: {kw}")

base=dict(utc_instant=utc,site_longitude_East="2.3522",
          mean_dawn_policy="project_extension_05_LMT_dawn",
          calendar_system="phugpa",calendar_epoch=1987,
          lunar_anomaly_policy="rounded")
for val in ("nan","181","not a number",True,"-181"):
    fails(**{**base,"site_longitude_East":val})
fails(**{**base,"utc_instant":datetime(1950,11,15,16)})
fails(**{**base,"utc_instant":original})
fails(**{**base,"mean_dawn_policy":"automatic_sunrise"})
fails(**{**base,"calendar_system":"unknown"})
fails(**{**base,"calendar_epoch":1852})
fails(**{**base,"lunar_anomaly_policy":"unknown"})

q=subprocess.run(["python3",str(ROOT/"verify_t54_true_dates.py")],
                 check=True,capture_output=True,text=True)
assert "12 calendar-years" in q.stdout
print("T55 BIRTH-POLICY SOURCE/SYNTHETIC PASS: independent Cornu four pillars 1950,")
print("  year/day/hour dawn boundaries, policy and longitude sensitivity, UTC/DST guards;")
print("  NOT a validated real-person predictive horoscope.")
