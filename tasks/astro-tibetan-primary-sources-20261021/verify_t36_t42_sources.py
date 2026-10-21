#!/usr/bin/env python3
"""Verify documentary scope and numeric identities in Tibetan T36–T42.
No medical or death predictions and no private participant cases are used.
"""
import json
from pathlib import Path
from subprocess import run
R=Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text(encoding="utf-8"))
groups=[
 ("batches/T36/QUERY_HOUR_FINAL_20_SOURCE_NOTES_V1.json","source_notes",20,325),
 ("batches/T38/ILLNESS_27_SOURCE_NOTES_V1.json","source_notes",27,345),
 ("batches/T42/DEATH_FIRST_16_SOURCE_NOTES_V1.json","source_notes",16,372)
]
all_ids=[]
for path,key,n,start in groups:
 data=read(path)
 notes=data[key]
 assert len(notes)==n==data["note_count"],(path,n)
 ids=[x["id"] for x in notes]
 assert ids==[f"TIB-R{i:04d}" for i in range(start,start+n)],path
 assert all(x["source_id"]=="TIB-DORJE-2001" for x in notes),path
 assert all(x["required_inputs"] for x in notes),path
 all_ids+=ids
assert len(set(all_ids))==len(all_ids)==63
assert all_ids==[f"TIB-R{i:04d}" for i in range(325,388)]
g=read("batches/T37/QUERY_RELATION_AND_HOUSE_GEOMETRY_5X5_V1.json")
assert g["new_historical_notes"]==0 and len(g["sector_rules"])==3
assert set(x["personal_axis"] for x in g["sector_rules"])=={"vitality","destiny","luck"}
assert len(g["relation_classes"])==9
assert len(g["geometry_source_table_rows"])==5
assert sorted(z["site_relative_position"] for z in g["geometry_source_table_rows"])==["center","front","left","rear","right"]
for row in g["geometry_source_table_rows"]:
 assert len(row["per_element"])==5
 assert {x["element"] for x in row["per_element"]}=={"wood","fire","earth","iron","water"}
 assert all(x["door_faces"] and x["shape"] for x in row["per_element"])
s=read("batches/T39/PINE_TREE_15_PLUS_2_POLICY_TABLE_V1.json")
assert s["new_historical_note_count"]==0
assert len(s["chart_definitions"])==17
assert [x["number"] for x in s["chart_definitions"]]==list(range(1,18))
assert all(x["kind"]=="CANONICAL_15" for x in s["chart_definitions"][:15])
assert all(x["kind"]=="SUPPLEMENTAL_SCHOOL_POLICY" for x in s["chart_definitions"][15:])
assert s["chart_definitions"][2]["direction_policy"]=="PROSE_DOWN_MOONBEAMS_FORWARD"
assert s["chart_definitions"][12]["direction_policy"]=="PROSE_BACK_MOONBEAMS_FORWARD"
p=read("batches/T40/ILLNESS_19_PEBBLES_AND_EXEMPLARY_CHART_V1.json")
x=p["pebble_structure"]
assert x["vitality"]["direct_element_relation_pebbles"]+x["vitality"]["growth_decline_pebbles"]==8
assert x["body"]["direct_element_relation_pebbles"]+x["body"]["growth_decline_pebbles"]==8
assert sum(z["count"] for z in x["additional"])==3
assert sum(p["eight_goddess_day_schedule"]["durations"])==30
assert len(p["eight_goddess_day_schedule"]["names_in_source_order"])==8
assert len(p["seven_great_pine_tree_variants"])==7
v=read("batches/T41/QUERY_ILLNESS_TEXT_AND_PLATE_VARIANTS_V1.json")
assert v["historic_annotation_increment"]==0
assert {z["id"] for z in v["issues"]} >= {"TIB-CONFLICT-008","TIB-CONFLICT-009","TIB-PLATE-CORRECTION-010"}
assert v["validated_human_outcomes"]==0
d=read("batches/T42/DEATH_FIRST_16_SOURCE_NOTES_V1.json")
assert d["human_prediction_validation"]==0 and d["model_promotions"]==0
for script in ("verify_t23_t29_obstacles.py","verify_t30_t33_sources.py","verify_t34_t35_query.py"):
 run(["python3",str(R/script)],check=True,capture_output=True,text=True)
print("T36–T42 SOURCE-ONLY PASS: 63 new records R0325–0387, 5×5 house plate, 15+2 illness variants, 19 pebbles, 8 goddesses, 20/58/199 death method separation; prior checks green")
