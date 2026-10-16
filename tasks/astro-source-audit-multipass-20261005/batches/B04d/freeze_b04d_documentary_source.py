from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
assert not any((B/n).exists() for n in ["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json"])
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert idx["records_count"]==4875 and idx["batches"][-1]["id"]=="B04c" and idx["next"]["chapter"]=="LXXXIV"
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert len(D)==79 and len(M)==15 and len(U["issues"])==24
assert idx["source_sha256"]==W["original_full_pdf_sha256"]
assert all(H(x["path"])==x["sha256"] for x in W["original_images"])
rs=[]
for n,r in enumerate(D,start=4876):
 rs.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,"accepted_for_primary_historical_text_reference":True,
 "independently_authenticated_vocational_outcome":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rs]==list(range(4876,4955))
R={"batch":"B04d","kind":"ORIGINAL_1647_HISTORICAL_PROFESSION_SIGN_MAPPING_ONLY",
 "status":"DOCUMENTARY_ACCEPTED_LOCAL_PENDING_GITHUB",
 "documentary_accepted_locally":True,"record_count":79,"first_record":4876,"last_record":4954,
 "substantive_lxxxiv_units":77,"following_chapter_navigation":2,
 "original_pdf_pages":[484,485,486],"source_spans":15,"source_uncertainties":24,
 "vocational_glyphs_verified_mars_venus":True,
 "real_vocational_outcomes_independently_verified":0,
 "empirically_validated_predictions":0,"runtime_promotions":0,"rules":rs}
put("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in rs}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04d","source_spans":[
 {**s,"accepted_global_record_ids":[lookup[k] for k in s["mapped_local_ids"]]} for s in M],
 "span_count":15,"mapped_source_records":79})
put("SOURCE_ORDER.json",{"batch":"B04d","record_count":79,"first_record":4876,"last_record":4954,
 "original_pdf_pages":[484,485,486],
 "records":[{"record_number":r["record_number"],"role":r["role"],"pdf_pages":r["original_pdf_pages"]} for r in rs],
 "empirical_validations":0})
U["status"]="ORIGINAL_SOURCE_LIMITS_RETAINED";put("UNRESOLVED.json",U)
A={"batch":"B04d","status":"DOCUMENTARY_ADMITTED_LOCAL_PENDING_ARCHIVE_REMOTE",
 "prior_lilly_accepted":4875,"new_documentary_records":79,
 "first_record":"R4876","last_record":"R4954",
 "lilly_if_published":4954,"ptolemy_retained":1066,"combined_if_published":6020,
 "original_pdf_sha256":W["original_full_pdf_sha256"],"original_body_pdf_pages":[484,485],
 "next_chapter":"LXXXV","next_original_pdf":486,"source_spans":15,
 "source_unresolved_limits":24,"Mars_Venus_glyph_original_verified":True,
 "independently_verified_vocational_outcomes":0,
 "empirically_validated_predictions":0,"runtime_promotions":0,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04d","locally_admitted":79,"if_published":6020,"empirical":0}))
