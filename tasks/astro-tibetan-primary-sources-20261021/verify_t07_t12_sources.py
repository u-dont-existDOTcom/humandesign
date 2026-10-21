import json
from pathlib import Path
R=Path(__file__).resolve().parent
def load(p):return json.loads((R/p).read_text())
a=load("batches/T07/WHITE_BERYL_NATAL_OMENS_AND_TRIPLES_V1.json")
b=load("batches/T09/WHITE_BERYL_FAMILY_YEAR_OMENS_14_NOTES_V1.json")
c=load("batches/T11/NATAL_SECTOR_CHILD_ARCHETYPES_20_NOTES_V1.json")
notes=a["source_notes"]+b["source_notes"]+c["source_notes"]
assert [n["id"] for n in notes]==[f"TIB-R{k:04d}" for k in range(113,163)]
assert [a["note_count"],b["note_count"],c["note_count"]]==[16,14,20]
assert all(n["source_id"]=="TIB-DORJE-2001" for n in notes)
assert all(n["required_inputs"] and n["dependency_family"] for n in notes)
t8=load("batches/T08/MATERNAL_AND_SYMBOLIC_PLANETARY_TABLES_V1.json")
m=t8["tables"]["mother_childbirth_age_8_column"]
p=t8["tables"]["subject_sex_symbolic_planetary_triples"]
assert len(m)==len(p)==8
assert sorted(x for row in m for x in row["mother_age_at_childbirth"])==list(range(15,51))
assert all(len(x["mother_natal_signs"])==len(x["mother_age_at_childbirth"]) for x in m)
t10=load("batches/T10/ANIMAL_SEASON_AND_ODD_EVEN_VARIANTS_V1.json")
assert all(len(v)==5 for v in t10["tables"].values())
t12=load("batches/T12/SECTOR_PAIR_CHILD_CLASS_AND_GENERATIONS_V1.json")
assert len(t12["sector_polarity_pairs"])==6
assert sorted(map(len,t12["child_21_model_types"].values()))==[7,7,7]
assert len(t12["four_generation_destiny_examples"])==5
assert a["actual_blind_human_tests"]==b["human_validation_count"]==c["real_human_tests"]==0
print("PASS: T07–T12 50 contiguous new notes, checked symbolic lookup structures, zero human predictions")
