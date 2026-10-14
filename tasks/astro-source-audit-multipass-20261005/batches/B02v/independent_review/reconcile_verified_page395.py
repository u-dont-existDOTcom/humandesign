"""One-time image-first correction of Part of Fortune symbol at PDF395/p361.
Preserve pre-edit source bytes, no acceptance, no empirical classification.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P393_395.json"
BACK=B/"recovery/producer_p393_395_before_20261014_p361_fortune_glyph.json"
assert not BACK.exists(), "Already applied: inspect backup."
raw=SRC.read_bytes()
data=json.loads(raw)
r=[x for x in data["units"] if x["kind"]=="fortune_seventh_free_first_offence"]
assert len(r)==1
r=r[0]
assert r["pdf_pages"]==[395]
assert r["source_statement"]=="A Fortune or seventh lord free from misfortunes is said to indicate first offence; Jupiter alone as thief significator is also offered."
r["kind"]="part_fortune_or_lord7_free_first_offence"
r["source_statement"]="The Part of Fortune (⊗) OR seventh-house lord free from misfortunes, OR Jupiter alone as thief significator, is said by Lilly to signify the alleged person's first offence."
r["preconditions"]=["Original PDF395/printed361 prints the Part-of-Fortune glyph (circle and diagonal cross), not the indefinite word 'Fortune'. The three branches are alternatives."]
r["exceptions_and_uncertainty"]=["Historical offender-description claim with no independently verified accuracy; do not interpret the symbol as a generic benefic planet."]
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
un=B/"UNRESOLVED_DRAFT.json"
u=json.loads(un.read_text())
assert all(x["id"]!="U48" for x in u["issues"])
u["issues"].append({"id":"U48","description":"Original PDF395/printed361 first-offence rule prints Part of Fortune ⊗, not generic 'a Fortune'. Corrected R2848 source identity with original source bytes preserved. No empirical validation.","status":"REVIEWED_SOURCE_CORRECTION"})
u["retained_count"]=len(u["issues"])
un.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"original_sha256":hashlib.sha256(raw).hexdigest(),
 "new_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
 "kind":r["kind"],"issues":len(u["issues"]),"accepted":False},indent=2))
