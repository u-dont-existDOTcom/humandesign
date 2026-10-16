from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
assert not any((B/n).exists() for n in ["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json"])
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert idx["records_count"]==4829 and idx["batches"][-1]["id"]=="B04b" and idx["next"]["chapter"]=="LXXXIII"
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert len(D)==46 and len(M)==8 and len(U["issues"])==17
assert idx["source_sha256"]==W["original_full_pdf_sha256"]
assert all(H(z["path"])==z["sha256"] for z in W["original_images"])
rs=[]
for n,r in enumerate(D,start=4830):
 rs.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,"accepted_for_primary_historical_text_reference":True,
  "independently_authenticated_restoration_outcome":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rs]==list(range(4830,4876))
R={"batch":"B04c","kind":"ORIGINAL_1647_RESTORATION_EXILE_HISTORICAL_TEXT_ONLY",
 "status":"LOCALLY_DOCUMENTARY_ACCEPTED_PENDING_REMOTE",
 "documentary_accepted_locally":True,
 "record_count":46,"first_record":4830,"last_record":4875,
 "substantive_lxxxiii_units":44,"following_chapter_navigation":2,
 "source_spans":8,"unresolved_issues":17,
 "restoration_same_place_distinct_from_new_office_elsewhere":True,
 "independently_verified_restoration_outcomes":0,
 "empirically_validated_predictions":0,"runtime_promotions":0,"rules":rs}
put("RULES.json",R)
mapping={r["source_local_id"]:r["id"] for r in rs}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04c","source_spans":[
 {**s,"accepted_global_record_ids":[mapping[k] for k in s["mapped_local_ids"]]} for s in M],
 "span_count":8,"mapped_source_records":46})
put("SOURCE_ORDER.json",{"batch":"B04c","first_record":4830,"last_record":4875,
 "record_count":46,"original_pdf_pages":[482,483,484],
 "records":[{"record_number":r["record_number"],"role":r["role"],"pdf_pages":r["original_pdf_pages"]} for r in rs],
 "empirical_validations":0})
U["status"]="ORIGINAL_SOURCE_UNCERTAINTIES_RETAINED";put("UNRESOLVED.json",U)
A={"batch":"B04c","status":"DOCUMENTARY_ADMITTED_LOCAL_PENDING_ARCHIVE_REMOTE",
 "prior_lilly_accepted":4829,"new_documentary_records":46,"first_record":"R4830","last_record":"R4875",
 "lilly_if_published":4875,"ptolemy_retained":1066,"combined_if_published":5941,
 "original_pdf_sha256":W["original_full_pdf_sha256"],"next_chapter":"LXXXIV",
 "next_original_pdf":484,"source_spans":8,"original_unresolved_limits":17,
 "independently_verified_restoration_outcomes":0,"empirically_validated_predictions":0,
 "runtime_promotions":0,"remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04c","local_records":46,"if_published":5941}))
