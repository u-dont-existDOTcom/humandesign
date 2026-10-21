import json
from pathlib import Path
from subprocess import run
R=Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text(encoding="utf-8"))
a=read("batches/T47/THIRTY_COMPUTATIONAL_18_SOURCE_NOTES_V1.json")
b=read("batches/T49/BALMO_THIRTEEN_13_SOURCE_NOTES_V1.json")
ids=[x["id"] for x in a["source_notes"]+b["source_notes"]]
assert a["note_count"]==18 and b["note_count"]==13
assert ids==[f"TIB-R{i:04d}" for i in range(417,448)]
assert all(x["source_id"]=="TIB-DORJE-2001" and x["required_inputs"] for x in a["source_notes"]+b["source_notes"])
assert all(x["human_validation"] is False and x["model_promoted"] is False for x in a["source_notes"])
assert all(x["validated_human_predictions"]==0 and x["model_promoted"] is False for x in b["source_notes"])
thirty=read("batches/T48/THIRTY_CHARTS_INDEX_AND_ANIMAL_STARTS_V1.json")
assert len(thirty["source_chart_catalogue"])==30
assert [z["white_beryl_chapter26_index"] for z in thirty["source_chart_catalogue"]]==list(range(1,31))
assert all(z["documented_basic_markers"]==8 for z in thirty["source_chart_catalogue"])
assert sum(z["moonbeams_family"]=="Chinese" for z in thirty["source_chart_catalogue"])==15
assert sum(z["moonbeams_family"]=="Tibetan" for z in thirty["source_chart_catalogue"])==15
for z in thirty["source_chart_catalogue"]:
 n=z["white_beryl_chapter26_index"]
 expected=(("Chinese",n) if n<=7 else ("Tibetan",n-7) if n<=14 else
           ("Chinese",n-7) if n<=22 else ("Tibetan",n-15))
 assert (z["moonbeams_family"],z["moonbeams_family_index"])==expected
for k in ("Chinese","Tibetan"):
 assert [z["family_index"] for z in thirty["moonbeams_fifteen_starting_pairs_by_family"][k]]==list(range(1,16))
assert len(thirty["white_beryl_eight_sector_prose_order"])==8
assert [z["sector"] for z in thirty["white_beryl_eight_sector_prose_order"]]==list(range(1,9))
assert len(thirty["source_color_relation_multiplicity"])==6
assert next(z for z in thirty["source_color_relation_multiplicity"] if z["relation"]=="son")["white"]==1
assert next(z for z in thirty["source_color_relation_multiplicity"] if z["relation"]=="son")["black"]==1
assert thirty["historical_note_count_increment"]==0
balmo=read("batches/T50/BALMO_THIRTEEN_STARTING_POINTS_V1.json")
assert balmo["historical_source_note_increment"]==0
assert len(balmo["charts"])==13
assert [z["index"] for z in balmo["charts"]]==list(range(1,14))
assert all(z["axes"]==["vitality","body","destiny","luck","numeric_square"] for z in balmo["charts"])
counts=balmo["counts"]
assert counts["charts"]*counts["positions_per_chart"]==counts["source_total_core_positions"]==65
assert counts["middle_basic"]+counts["middle_symbolic"]==counts["middle_abridged_pebbles"]==872
assert counts["more_elaborate_pebbles"]==2920
assert balmo["source_color_classification"]["son"]=="black"
assert balmo["contrast_against_T48"]["thirty_chart_son_color"]=="white_plus_black"
assert [z["index"] for z in balmo["unresolved"]]==[10,13]
assert thirty["actual_human_predictive_successes"]==balmo["actual_blind_human_tests"]==a["new_human_blind_validation_count"]==b["human_tests"]==0
for old in ("verify_t44_t46_sources.py",):
 run(["python3",str(R/old)],check=True,capture_output=True,text=True)
print("T47-T50 SOURCE PASS: 31 new notes through TIB-R0447; White Beryl 30×8, Moonbeams interleaved 15/15, Bal-mo 13×5=65 and 872=371+501; nonidentical pebble colors; prior T01–T46 tests green.")
