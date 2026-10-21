from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
t6=json.loads((ROOT/"batches/T06/MATERNAL_FIVE_GRADE_SOURCE_TABLE_V1.json").read_text())
t5=json.loads((ROOT/"batches/T05/WHITE_BERYL_NATAL_CONDITIONAL_21_SOURCE_NOTES.json").read_text())
assert t6["status"] == "EXPLICIT_SOURCE_TABLE_DIGITIZATION_NOT_VALIDATED_ASTROLOGY"
assert t6["human_validated"] == 0 and t6["promoted_to_runtime"] is False
assert t6["new_historical_source_note_count"] == 0
assert set(t6["previous_covered_source_note_ids"]) <= {n["id"] for n in t5["source_notes"]}
assert t6["provenance"]["pdf_page_1based"] == 160
assert t6["grade_order"] == ["divine_parentage","glorious_offspring","harmonious_lifespan","potent_spirit","impotent_demon"]
columns=t6["mother_columns"]
assert [c["representative_maternal_trigram"] for c in columns]==["Zin","Li","Khon","Dva","Kham"]
assert sorted(n["number"] for c in columns for n in c["mewa_groups"])==list(range(1,10))
v=t6["axis_matrices"]["child_year_animal_vitality"]["grades_to_columns"]
el=t6["axis_matrices"]["child_body_element"]["grades_to_columns"]
animals={"mouse","ox","tiger","hare","dragon","snake","horse","sheep","monkey","bird","dog","pig"}
elements={"wood","fire","earth","iron","water"}
assert len(v)==len(el)==5 and all(len(row)==5 for row in v+el)
for i in range(5):
    cells=[animal for row in v for animal in row[i]]
    assert len(cells)==12 and set(cells)==animals and len(set(cells))==12
    assert set(row[i] for row in el)==elements
for axis in ("child_body_element","child_destiny_element","child_luck_element"):
    assert t6["axis_matrices"][axis]["grades_to_columns"]==el
def grade_for_year(col,animal):
    return t6["grade_order"][next(row for row in range(5) if animal in v[row][col])]
def grade_for_element(col,element):
    return t6["grade_order"][next(row for row in range(5) if element == el[row][col])]
assert grade_for_year(0,"horse")=="divine_parentage"
assert grade_for_year(3,"mouse")=="divine_parentage"
assert grade_for_year(4,"horse")=="impotent_demon"
assert grade_for_element(0,"fire")=="divine_parentage"
assert grade_for_element(2,"fire")=="glorious_offspring"
assert grade_for_element(4,"fire")=="impotent_demon"
assert t6["graded_relations"]=={"mother":"divine_parentage","son":"glorious_offspring","identity":"harmonious_lifespan","friend":"potent_spirit","enemy":"impotent_demon"}
print("T06 SOURCE TABLE PASS: 5 maternal columns, 9 numeric squares, 60 animal cells, 25 elemental cells per axis, synthetic lookups only")
