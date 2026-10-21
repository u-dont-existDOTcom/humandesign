import json
from pathlib import Path
R=Path(__file__).resolve().parent
def load(name):return json.loads((R/name).read_text(encoding="utf-8"))
a=load("batches/T16/MARRIAGE_CONSTITUTION_PERMUTATIONS_16_NOTES_V1.json")
b=load("batches/T18/MARRIAGE_ELECTIONAL_18_NOTES_V1.json")
notes=a["source_notes"]+b["source_notes"]
assert a["note_count"]==16 and b["note_count"]==18
assert [n["id"] for n in notes]==[f"TIB-R{i:04d}" for i in range(175,209)]
assert all(n["source_id"]=="TIB-DORJE-2001" for n in notes)
assert all(n["required_inputs"] and n["dependency_family"] for n in notes)
assert a["human_predictions_tested"]==a["runtime_promotions"]==0
assert b["human_outcomes_scored"]==b["model_promotions"]==0
p=load("batches/T17/BRIDE_MEWA_INCOMPLETE_PERMUTATION_VARIANTS_V1.json")
assert p["additional_historical_notes"]==0
v=p["variants"][1]
mapping={int(k):value for k,value in v["bride_mapping"].items()}
assert set(mapping)=={1,2,3,4,6,7,8,9}
assert v["unresolved_numerals"]==[5]
assert all(mapping[mapping[x]]==x for x in mapping)
assert mapping[6]==6 and mapping[7]==7
q=load("batches/T19/ELECTIONAL_TABLES_V1.json")
assert q["historical_note_increment"]==0
assert len(q["year_month_animal_rows"])==5
assert len(q["natal_month_to_day_rows"])==12
assert len(q["natal_trigram_to_weekday_rows"])==4
animals="mouse ox tiger hare dragon snake horse sheep monkey bird dog pig".split()
assert sorted(x["natal_month"] for x in q["natal_month_to_day_rows"])==sorted(animals)
assert sorted(x for row in q["year_month_animal_rows"] for x in row["natal_animals"])==sorted(animals)
assert sorted(x for row in q["natal_trigram_to_weekday_rows"] for x in row["natal_trigrams"])==sorted("Li Khon Dva Khen Kham Gin Zin Zon".split())
z=load("batches/T20/NUPTIAL_TRANSPORT_PROSE_VS_PLATE_V1.json")
assert z["historical_source_note_increment"]==0
assert z["prose_view"]["Khon"]==["sheep","dog"] and z["prose_view"]["Khen"] is None
assert z["illustrated_table_view"]["Khen"]=="dog"
assert z["human_validation_count"]==0
print("PASS T16-T20: 34 notes, partial 8-number permutation, electional lookup partitions, three-source conflicts preserved")
