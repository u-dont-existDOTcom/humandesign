import json
from pathlib import Path
R=Path(__file__).resolve().parent
def get(p):return json.loads((R/p).read_text(encoding="utf-8"))
n=get("batches/T34/HOUR_OF_DIVINATION_FIRST_12_NOTES_V1.json")
assert n["note_count"]==12
assert [x["id"] for x in n["source_notes"]]==[f"TIB-R{i:04d}" for i in range(313,325)]
assert all(x["required_inputs"] and x["source_id"]=="TIB-DORJE-2001" for x in n["source_notes"])
assert n["human_blind_tests"]==n["runtime_promotions"]==0
t=get("batches/T35/NINE_SECTOR_QUERY_CHART_PARTIAL_V1.json")
a=t["verified_sector_rows"]
assert len(a)==9
assert [r["ordinal"] for r in a]==list(range(1,10))
assert t["additional_historical_source_notes"]==0
assert t["source_conflicts"][0]["id"]=="TIB-CONFLICT-007"
assert t["chart_definition"]["directions_in_intro_prose"][7:]==["north","northeast"]
assert t["chart_definition"]["directions_in_printed_table"][7:]==["northeast","north"]
assert t["chart_definition"]["directions"]=="UNRESOLVED_EIGHTH_NINTH_SECTOR_CONFLICT"
assert a[2]["relative_comparison"]=="sector_mewa_v_day_mewa"
assert "ENHANCES" in a[6]["source_relation"]
assert a[7]["direction"]=="northeast_in_printed_table"
assert a[8]["direction"]=="north_in_printed_table"
assert t["human_prediction_validation"]==0
print("T34-T35 PASS: 12 consultation-hour notes and 9 source cells, unique 8/9 direction conflict preserved.")
