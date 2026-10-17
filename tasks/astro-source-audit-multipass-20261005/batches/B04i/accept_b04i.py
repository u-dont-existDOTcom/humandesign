from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
get=lambda p:json.loads(Path(p).read_text())
def put(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
j=get(INDEX);W=get(B/"SOURCE_WINDOW_MANIFEST.json");D=get(B/"SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=get(B/"ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
assert j["records_count"]==5161 and j["batches"][-1]["id"]=="B04h"
assert j["next"]["chapter"]=="LXXXIX" and j["next"]["pdf_page"]==493
assert j["source_sha256"]==W["original_full_pdf_sha256"]
assert len(D)==32 and len(M)==4 and len(get(B/"UNRESOLVED_SOURCE_LIMITS.json")["issues"])==14
for w in W["original_images"]:
 p=B/w["path"];assert p.stat().st_size==w["bytes"] and H(p)==w["sha256"]
ids=[x for s in M for x in s["mapped_local_ids"]]
assert len(ids)==len(set(ids))==32
assert set(ids)=={r["source_local_id"] for r in D}
assert all(r["chapter"]=="LXXXIX" for r in D[:-2])
rows=[]
for n,r in enumerate(D,start=5162):
 rows.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,"independently_verified_relationship_outcome":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rows]==list(range(5162,5194))
R={"batch":"B04i","kind":"HISTORICAL_FRIENDSHIP_RELATIONSHIP_SOURCE_ONLY",
 "status":"DOCUMENTARY_SOURCE_ACCEPTED_LOCALLY","record_count":32,"first_record":5162,
 "last_record":5193,"substantive_lxxxix_source_units":30,"following_heading_navigation":2,
 "source_spans":4,"unresolved_source_limits":14,"printed_chapter":"LXXXVIII",
 "editorial_chapter":"LXXXIX","independently_verified_relationship_outcomes":0,
 "empirically_validated_predictions":0,"runtime_promotions":0,"rules":rows}
put(B/"RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rows}
put(B/"ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04i","source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]} for s in M],
 "span_count":4,"mapped_source_records":32})
put(B/"SOURCE_ORDER.json",{"batch":"B04i","first_record":5162,"last_record":5193,
 "record_count":32,"original_pdf_pages":[493,494],"ids":[r["id"] for r in rows]})
U=get(B/"UNRESOLVED_SOURCE_LIMITS.json");U["status"]="RETAINED";put(B/"UNRESOLVED.json",U)
A={"batch":"B04i","prior_lilly":5161,"new_documentary_records":32,"lilly_if_published":5193,
 "retained_ptolemy":1066,"combined_if_published":6259,
 "next_chapter":"XC","next_printed_chapter":"LXXXIX","next_original_pdf":494,
 "independent_relationship_outcomes_verified":0,"new_empirical_predictions":0,"runtime_promotions":0}
for name,key in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256")]:
 A[key]=H(B/name)
put(B/"ACCEPTANCE.json",A)
print(json.dumps(A))
