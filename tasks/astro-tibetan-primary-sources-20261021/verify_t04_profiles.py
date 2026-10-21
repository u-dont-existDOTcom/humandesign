from pathlib import Path
import json
root = Path(__file__).resolve().parent
new = json.loads((root/"batches/T04/WHITE_BERYL_60_PROFILES_V1.json").read_text())
old = json.loads((root/"batches/T03/SOURCE_NOTES_T03.json").read_text())
p = new["profiles"]
assert len(p) == 60
assert [r["cycle_index"] for r in p] == list(range(1,61))
assert len(set(x["source_note_id"] for x in p)) == 60
assert new["human_blind_predictions"] == new["runtime_promotions"] == 0
animals = ("mouse","ox","tiger","hare","dragon","snake","horse","sheep","monkey","bird","dog","pig")
elements = ("Wood","Fire","Earth","Iron","Water")
for i,x in enumerate(p,1):
    assert x["animal"] == animals[(i-1)%12]
    assert x["year_element"] == elements[((i-1)//2)%5]
    assert x["year_polarity"] == ("male" if i%2 else "female")
    assert x["pdf_page_1based"] == x["printed_page"]+1
    assert x["evidence_class"] == "historical_source_claim_only"
    assert x["subject_data_checked"] is False
    if x["claimed_obstacle_count"] is None: 
        assert x["obstacle_qualifier"] in ("not_stated","three_sets_of_three_obstacles")
    else:
        assert 1 <= x["claimed_obstacle_count"] <= 12
older = {x["id"] for x in old["source_notes"]}
assert p[4]["source_note_id"]=="TIB-R0029" and p[13]["source_note_id"]=="TIB-R0030"
assert p[4]["source_note_id"] in older and p[13]["source_note_id"] in older
new_ids=[x["source_note_id"] for x in p if not x["reuses_prior_note"]]
assert new_ids == [f"TIB-R{i:04d}" for i in range(34,92)]
assert new["methodology_note"]["id"]=="TIB-R0033"
assert p[18]["claimed_lifespan_years"]==[77,57]
assert p[30]["obstacle_qualifier"]=="three_sets_of_three_obstacles"
print("T04 PASS: 60 profiles, 58 new unique claims, no human validation")
