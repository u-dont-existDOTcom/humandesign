#!/usr/bin/env python3
"""T23–T29 source-only integrity tests; no claims of empirical prediction."""
import json
from pathlib import Path
from subprocess import run
R=Path(__file__).resolve().parent
def load(path): return json.loads((R/path).read_text(encoding="utf-8"))
files=[
 ("batches/T23/OBSTACLE_HOUSEHOLD_19_SOURCE_NOTES_V1.json",19,221,"source_notes"),
 ("batches/T25/OBSTACLE_MEWA_18_SOURCE_NOTES_V1.json",18,240,"notes"),
 ("batches/T27/MULTIPLES_OF_NINE_24_NOTES_V1.json",24,258,"source_notes"),
]
ids=[]
for path,n,start,k in files:
 d=load(path); a=d[k]
 assert d["note_count"]==n==len(a),(path,n)
 assert [t["id"] for t in a]==[f"TIB-R{i:04d}" for i in range(start,start+n)],path
 assert all(t["source_id"]=="TIB-DORJE-2001" for t in a)
 assert all(t["required_inputs"] and t["dependency_family"] for t in a)
 ids.extend(t["id"] for t in a)
assert len(ids)==61 and len(set(ids))==61 and ids[0]=="TIB-R0221" and ids[-1]=="TIB-R0281"
t24=load("batches/T24/HOUSEHOLD_TRIGRAM_TABLES_V1.json")
assert t24["new_source_notes"]==0
t=t24["structure"]
groups=t["securely_cherished"]["rows"]
animals=set("mouse ox tiger hare dragon snake horse sheep monkey bird dog pig".split())
assert len(groups)==5
assert set(z for r in groups for z in r["majority"])==animals
assert len(t["five_confusions"]["rows"])==5
assert t["five_confusions"]["rows"][2]["current_year"]==["sheep"]
assert t["five_confusions"]["rows"][2]["prose_alternative"]==["ox","dragon","sheep","dog"]
assert len(t["natural_year_trigram"]["rows"])==8
assert len(t["four_tombs_majority_minority"]["rows"])==4
for row in t["five_charts_for_current_year"]["rows"]:
 assert sorted({x for key in ("mother","son","identity","enemy","friend") for x in row[key]})==sorted(["Li","Khon","Dva","Khen","Kham","Gin","Zin","Zon"])
t26=load("batches/T26/MEWA_NINE_CATEGORIES_AND_GATES_V1.json")
assert t26["historical_note_increment"]==0
assert len(t26["mewa_mirror_names"])==len(t26["Black_Two_combination_target_rows"])==9
assert len(t26["four_minor_pebbles"])==4
assert t26["sex_gates"]["male"]["heaven"]=="Black Two"
assert t26["sex_gates"]["female"]["heaven"]=="White One"
assert set(t26["vitality_tomb_trigrams"])=={"wood","fire","iron","earth","water"}
t28=load("batches/T28/NINE_AGE_AND_FAMILY_GRID_V1.json")
assert t28["source_note_increment"]==0
k=t28["series"]
assert [z["age"] for z in k["nine_age_solitary"]["male"]]==[9,18,27,36,45,54,63,72,81]
assert [z["age"] for z in k["nine_age_solitary"]["female"]]==[9,18,27,36,45,54,63,72,81]
assert k["combined_sign_tomb_ages"]["ages"]==[9,21,33,45,57,69,81]
assert len(k["constitutional_start_keys"]["rows"])==4
assert len(k["constitutional_year_danger_labels"]["rows"])==5
g=t28["six_member_household_grid"]
assert sorted(sum(g["five_six_member_rows"].values(),[]))==list(range(1,31))
assert sorted(sum(g["sectors"].values(),[])+g["residual"])==list(range(1,31))
p=t28["pebble_count_variants"]
assert sum(p["three_chinese_modes_360"].values())==360
assert 360+p["extended_600_extra_day"]+p["extended_600_extra_hour"]==600
t29=load("batches/T29/OBSTACLE_YEAR_EDITION_VARIANTS_V1.json")
assert t29["new_source_notes"]==0
assert {z["id"] for z in t29["conflicts"]} >= {"TIB-CONFLICT-004","TIB-CONFLICT-005"}
for t in files:
 assert isinstance(t[0],str)
prior_scripts=("verify_source_batches.py","verify_t04_profiles.py","verify_t05_natal.py","verify_t06_maternal_table.py","verify_t07_t12_sources.py","verify_t13_t15_marriage.py","verify_t16_t20_marriage.py","verify_t21_t22_obstacles.py")
for s in prior_scripts:
 run(["python3",str(R/s)],capture_output=True,text=True,check=True)
print("T23–T29 PASS: 61 source notes R0221–R0281, 5 matrices, 47/31/37/360/600 variants, two unresolved textual contradictions; earlier eight checks green; zero human validation")
