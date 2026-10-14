"""One-time image-first p362 correction: 'greatest number' ≠ majority testimony.
Preserve earlier producer bytes. Source fidelity only.
"""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
SRC=B/"PRODUCER_SOURCE_DRAFT_P396_397.json"
BACK=B/"recovery/producer_p396_397_before_20261014_p362_age_review.json"
assert not BACK.exists(),"Already corrected"
raw=SRC.read_bytes()
d=json.loads(raw)
r=[x for x in d["units"] if x["kind"]=="age_majority_methods"]
assert len(r)==1
r=r[0]
assert r["pdf_pages"]==[396]
assert r["source_statement"]=="Lilly explicitly recommends considering most of the alternative age methods and choosing the greatest amount of agreeing testimony."
r["kind"]="age_methods_greatest_number_textual"
r["source_statement"]="After giving several different ways to assign an alleged person's age, Lilly says to consider most of these ways and 'pitch upon the greatest number'; the source does not explicitly prescribe choosing the greatest amount of agreeing testimony."
r["preconditions"]=["Multiple previously listed age-number methods have been considered."]
r["exceptions_and_uncertainty"]=["Literal 'greatest number' may mean the numerically highest age result; majority-vote/most-supported age interpretation is not textually stated. No selection may be retrospectively tuned to actual ages."]
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
un=B/"UNRESOLVED_DRAFT.json"
u=json.loads(un.read_text())
assert all(x["id"]!="U49" for x in u["issues"])
u["issues"].append({"id":"U49","description":"PDF396/printed362 prints 'consider most of these wayes, and pitch upon the greatest number' in age methods. Producer interpreted greatest amount of agreeing testimony, not explicitly in source. Corrected R2873 to source-literal reading; whether numerically greatest estimate or consensus intended remains uncertain.","status":"RETAINED"})
u["retained_count"]=len(u["issues"])
un.write_text(json.dumps(u,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"old_sha256":hashlib.sha256(raw).hexdigest(),
"new_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
"source_correction":r["kind"],"retained_issues":len(u["issues"]),"accepted":False},indent=2))
