import json
from pathlib import Path
R=Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text(encoding="utf-8"))
n=read("batches/T21/OBSTACLE_YEAR_12_SOURCE_NOTES_V1.json")
assert n["note_count"]==12
assert [x["id"] for x in n["source_notes"]]==[f"TIB-R{i:04d}" for i in range(209,221)]
assert all(x["source_id"]=="TIB-DORJE-2001" for x in n["source_notes"])
assert all(x["required_inputs"] and not x["human_prediction_validated"] for x in n["source_notes"])
x=read("batches/T22/OBSTACLE_47_PEBBLES_AND_HARSHNESS_V1.json")
assert x["historical_note_increment"]==0
assert [a["count"] for a in x["pebbles"]]==[6,24,4,7,4,2]
assert sum(a["count"] for a in x["pebbles"])==47
assert len(x["unchanging_factors"])==6
assert len(x["four_axes"])==4
assert len(x["harshness_conditions"])==7
assert x["logmen_sex_sectors"]["male"]["heaven_gate"]=="dog"
assert x["logmen_sex_sectors"]["female"]["heaven_gate"]=="dragon"
assert x["example_natal_year_returns"]==list(range(13,74,12))
assert x["example_seventh_removed_years"]==list(range(7,56,12))
assert x["human_predictions_validated"]==n["actual_human_outcomes_verified"]==0
print("T21-T22 PASS: 12 source notes, 47-pebble structure, seven harshness classes, zero human tests")
