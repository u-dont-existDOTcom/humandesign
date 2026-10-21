#!/usr/bin/env python3
"""Deterministic source-integrity check for T44–T45, not predictive validation."""
import json
from pathlib import Path
from subprocess import run
R=Path(__file__).resolve().parent
def get(p):return json.loads((R/p).read_text(encoding="utf-8"))
d=get("batches/T44/DEATH_REMAINDER_29_SOURCE_NOTES_V1.json")
notes=d["source_notes"]
assert d["note_count"]==len(notes)==29
assert [x["id"] for x in notes]==[f"TIB-R{i:04d}" for i in range(388,417)]
assert all(x["source_id"]=="TIB-DORJE-2001" for x in notes)
assert all(x["required_inputs"] for x in notes)
assert all(x["independently_tested_on_humans"] is False and x["model_promoted"] is False for x in notes)
assert d["human_blind_predictions"]==d["model_promotions"]==0
a=get("batches/T45/DEATH_FUNERAL_REBIRTH_TABLES_V1.json")
assert a["historical_source_note_increment"]==0
t=a["source_tables"]
animals=set("mouse ox tiger hare dragon snake horse sheep monkey bird dog pig".split())
seen=[x for row in t["six_realm_by_hour_animal"] for x in row["animals"]]
assert len(t["six_realm_by_hour_animal"])==6 and len(seen)==12 and set(seen)==animals
sectors=[x for row in t["six_realm_by_growth_decline_sector"] for x in row["paired_sectors"]]
assert len(t["six_realm_by_growth_decline_sector"])==6 and len(sectors)==12 and len(set(sectors))==12
mewa=t["mewa_to_rebirth_categories"]
assert len(mewa)==4
assert sum("Yellow Five" in row["mewa_values"] for row in mewa)==2
funeral=t["funeral_elemental_methods"]
assert len(funeral)==5 and {r["element"] for r in funeral}=={"wood","fire","earth","iron","water"}
groups=t["five_deceased_year_direction_avoidance"]
assert len(groups)==5
keys=[x for r in groups for x in r["natal_year_animals"]]
assert len(keys)==12 and set(keys)==animals
n=a["historical_source_counts"]
assert n["funeral_Moonbeams_underlying"]+n["funeral_Moonbeams_predictive"]==n["funeral_Moonbeams_total"]==199
assert n["ceremony_public_base"]+n["ceremony_public_recognition"]==n["ceremony_public_total"]==2920
assert n["recurrence_base"]+1==n["recurrence_total"]==11
assert n["eye_of_death_resultant"]+n["eye_of_death_recognition"]==94
assert n["eighteen_status_classes"]==18 and n["bon_buddhist_twelve_rites"]==12 and n["corpse_types"]==13
assert a["empirical_human_predictive_tests"]==0
run(["python3",str(R/"verify_t36_t42_sources.py")],check=True,capture_output=True,text=True)
print("T44-T46 SOURCE PASS: 29 death-chapter notes through R0416; 6+6 afterlife pairs, 5 funeral methods, 199/2920 distinct totals, T01–T42 checks green; no human tests")
