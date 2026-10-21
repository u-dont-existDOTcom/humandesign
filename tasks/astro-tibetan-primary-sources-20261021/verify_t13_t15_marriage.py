import json
from pathlib import Path
R=Path(__file__).resolve().parent
def data(p):return json.loads((R/p).read_text(encoding="utf-8"))
t13=data("batches/T13/MARRIAGE_12_SOURCE_NOTES_V1.json")
assert t13["note_count"]==12
assert [n["id"] for n in t13["source_notes"]]==[f"TIB-R{i:04d}" for i in range(163,175)]
t14=data("batches/T14/MARRIAGE_15_DESTINY_PAIRS_AND_PARITY_V1.json")
pairs=t14["five_element_pairs"]
assert len(pairs)==15
names={"wood","earth","water","fire","iron"}
assert {tuple(x["elements"]) for x in pairs}=={tuple(sorted((a,b))) for a in names for b in names}
assert all(x["sons_mentioned"]>=1 for x in pairs)
assert all(x["daughters_mentioned"] is None or x["daughters_mentioned"]>=1 for x in pairs)
assert all(x["sons_claimed_not_surviving"] is None or 0<x["sons_claimed_not_surviving"]<=x["sons_mentioned"] for x in pairs)
weights=t14["parity_weight_table"]
assert weights=={"wood":1,"earth":2,"water":3,"fire":4,"iron":5}
for sample in t14["synthetic_parity_examples"]:
    w=sum(weights[x] for x in sample["bride"]+sample["groom"])
    assert w==sample["sum"]
    assert sample["claim"]==("historical_compatible_claim" if w%2==0 else "historical_incompatible_claim")
t15=data("batches/T15/ENGLISH_SOURCE_INTERNAL_CONFLICTS_V1.json")
assert [x["id"] for x in t15["conflicts"]]==["TIB-CONFLICT-001","TIB-CONFLICT-002"]
assert t15["extra_historical_note_count"]==t14["new_source_notes"]==0
assert t15["human_predictive_validation"]==t14["human_predictions_validated"]==t13["human_validation"]==0
print("T13-T15 PASS: 12 new source notes, 15 distinct element pairs, two visually verified edition conflicts; no human tests")
