from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def out(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
assert not (B/"RULES.json").exists()
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert idx["records_count"]==5552 and idx["next"]["chapter"]=="XCVII" and idx["batches"][-1]["id"]=="B04p"
d=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
spans=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
assert idx["source_sha256"]==W["original_full_pdf_sha256"] and len(d)==34 and len(spans)==7
assert len(J("UNRESOLVED_SOURCE_LIMITS.json")["issues"])==19
for w in W["original_images"]:assert H(w["path"])==w["sha256"]
records=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "independently_authenticated_imprisoned_husband_outcome":False,
 "independently_verified_prior_garrison_capture":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for n,r in enumerate(d,5553)]
assert [r["record_number"] for r in records]==list(range(5553,5587))
assert all(r["chapter"]=="XCVII" for r in records[:-4])
assert all(r["chapter"]=="POST_XCVI_NAVIGATION_ONLY" for r in records[-4:])
rules={"batch":"B04q","record_count":34,"first_record":5553,"last_record":5586,
 "printed_chapter":"XCVI","editorial_chapter":"XCVII","status":"HISTORICAL_SOURCE_ACCEPTED_LOCAL",
 "substantive_source_annotations":30,"postchapter_navigation_annotations":4,
 "source_passages":7,"source_limitations":19,
 "author_past_or_future_release":True,"author_prior_day_events":True,
 "independent_verified_outcomes":0,"empirical_validations":0,"runtime_promotions":0,"rules":records}
out("RULES.json",rules)
lookup={r["source_local_id"]:r["id"] for r in records}
out("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04q","span_count":7,"mapped_source_records":34,
 "source_spans":[{**s,"accepted_global_record_ids":[lookup[k] for k in s["mapped_local_ids"]]} for s in spans]})
out("SOURCE_ORDER.json",{"batch":"B04q","record_count":34,"ids":[r["id"] for r in records]})
U=J("UNRESOLVED_SOURCE_LIMITS.json");out("UNRESOLVED.json",U)
A={"batch":"B04q","previous_lilly":5552,"new_records":34,"lilly_if_published":5586,
 "ptolemy_retained":1066,"combined_if_published":6652,
 "source_sha256":W["original_full_pdf_sha256"],"next":"UNNUMBERED_ESSEX_AND_TABLES",
 "independent_outcomes":0,"empirical_validations":0,"runtime_promotions":0}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256")]:A[k]=H(f)
out("ACCEPTANCE.json",A)
print(json.dumps(A))
