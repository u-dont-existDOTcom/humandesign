#!/usr/bin/env python3
"""Freeze first edition Rupert/Essex as documentary, never independently predictive."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
names=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
       "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
assert not any((B/n).exists() for n in names)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json");C=J("CLAIM_LEDGER.json")
assert I["records_count"]==4954 and I["batches"][-1]["id"]=="B04d"
assert I["next"]["chapter"]=="LXXXV" and I["next"]["pdf_page"]==486
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert D["source_units"]==72 and M["span_count"]==11 and len(U["issues"])==25
assert C["authorial_partial_error_acknowledgements"]==1
assert C["independent_wartime_outcomes_verified"]==0
for z in W["original_images"]:
 assert H(z["path"])==z["sha256"] and (B/z["path"]).stat().st_size==z["bytes"]
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").is_file()
ids=[r["source_local_id"] for r in D["rows"]]
mapped=[k for s in M["source_spans"] for k in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==72 and sorted(ids)==sorted(mapped)
assert all(r["chapter"]=="LXXXV" for r in D["rows"][:-2])
assert all(r["chapter"]=="LXXXVI_NAVIGATION_ONLY" for r in D["rows"][-2:])
rs=[]
for n,r in enumerate(D["rows"],start=4955):
 rs.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,"accepted_for_primary_historical_text_reference":True,
  "independently_authenticated_wartime_outcome":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rs]==list(range(4955,5027))
R={"batch":"B04e","kind":"ORIGINAL_1647_HISTORICAL_RUPERT_ESSEX_WAR_CASE_SOURCE_ONLY",
 "status":"LOCAL_DOCUMENTARY_ACCEPTED_NOT_REMOTE",
 "documentary_accepted_locally":True,
 "record_count":72,"first_record":4955,"last_record":5026,
 "substantive_lxxxv_source_annotations":70,"next_heading_navigation_only":2,
 "source_reverse_passages":11,"unresolved_source_limits":25,
 "original_pdf_pages":[486,487,488,489],
 "author_acknowledged_partial_error":True,
 "pre_question_battle_not_prospective":True,
 "independently_verified_wartime_predictions":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0,"rules":rs}
dump("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rs}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04e",
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]} for s in M["source_spans"]],
 "span_count":11,"mapped_source_records":72})
dump("SOURCE_ORDER.json",{"batch":"B04e","record_count":72,
 "first_record":4955,"last_record":5026,"original_pdf_pages":[486,487,488,489],
 "records":[{"record_number":r["record_number"],"role":r["role"],"pdf_pages":r["original_pdf_pages"]} for r in rs],
 "empirical_validations":0})
U["status"]="UNRESOLVED_SOURCE_LIMITS_RETAINED";dump("UNRESOLVED.json",U)
A={"batch":"B04e","kind":"AUTHOR_RETROSPECTIVE_MILITARY_PREDICTION_NOT_VERIFIED",
 "status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_RELEASE_AND_REMOTE",
 "documentary_accepted_locally":True,
 "prior_lilly_accepted":4954,"new_documentary_records":72,
 "first_record":"R4955","last_record":"R5026","lilly_if_published":5026,
 "ptolemy_retained":1066,"combined_if_published":6092,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[486,487,488],"following_heading_pdf":489,
 "next_chapter":"LXXXVI","next_original_pdf":489,
 "source_reverse_passages":11,"original_unresolved_limits":25,
 "rupert_authorial_partial_error_must_remain":True,
 "edgehill_pre_question_not_forecast":True,
 "independently_verified_wartime_outcomes":0,
 "new_empirically_validated_predictions":0,
 "runtime_model_promotions":0,
 "full_independent_diplomatic_transcription":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]: A[k]=H(f)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04e","local_historical_source_records":72,
 "lilly_if_published":5026,"combined_if_published":6092,
 "independent_success_count":0,"author_error_admissions":1}))
