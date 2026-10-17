#!/usr/bin/env python3
"""Admit Lilly printed XCV escaped-prisoner first-edition testimony as documentary only."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/n).exists() for n in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_PROVISIONAL_20261017.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5510 and I["batches"][-1]["id"]=="B04o"
assert I["read_numbered_chapters"]==list(range(1,96))
assert I["next"]["chapter"]=="XCVI" and I["next"]["pdf_page"]==504
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D["rows"])==D["source_units"]==42
assert len(M["source_spans"])==M["span_count"]==7
assert len(U["issues"])==20
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").exists()
for w in W["original_images"]:
 assert H(w["path"])==w["sha256"] and (B/w["path"]).stat().st_size==w["bytes"]
ids=[r["source_local_id"] for r in D["rows"]]
mapped=[i for s in M["source_spans"] for i in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==42 and sorted(ids)==sorted(mapped)
sourcebyid={r["source_local_id"]:r for r in D["rows"]}
assert all(set(sourcebyid[x]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
           for s in M["source_spans"] for x in s["mapped_local_ids"])
assert all(r["chapter"]=="XCVI" for r in D["rows"][:-3])
assert all(r["chapter"]=="XCVII_NAVIGATION_ONLY" for r in D["rows"][-3:])
records=[]
for n,r in enumerate(D["rows"],start=5511):
 records.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,
  "accepted_for_primary_historical_text_reference":True,
  "independently_verified_escaped_prisoner_identity":False,
  "independently_authenticated_fugitive_recapture":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in records]==list(range(5511,5553))
R={"batch":"B04p","kind":"ORIGINAL_1647_ESCAPED_PRISONER_RETROSPECTIVE_DOCUMENTARY_ONLY",
 "status":"DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_PUBLICATION",
 "record_count":42,"first_record":5511,"last_record":5552,
 "substantive_chapter_annotations":39,"next_heading_navigation":3,
 "original_pdf_pages":[504,505],"source_reverse_passages":7,
 "source_unresolved_limits":20,"printed_chapter":"XCV","editorial_chapter":"XCVI",
 "author_claims_east_travel_and_recapture":True,
 "author_reports_friday_letter_and_sunday_apprehension":True,
 "six_seven_day_source_timing_uncertainty":True,
 "independently_authenticated_fugitive_outcomes":0,
 "independently_authenticated_prison_records":0,
 "new_empirically_validated_predictions":0,
 "runtime_promotions":0,"rules":records}
put("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04p","span_count":7,"mapped_source_records":42,
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]}
   for s in M["source_spans"]]})
put("SOURCE_ORDER.json",{"batch":"B04p","first_record":5511,"last_record":5552,
 "record_count":42,"original_pdf_pages":[504,505],
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "original_pdf_pages":r["original_pdf_pages"],"source_span_id":r["source_span_id"]}
 for r in records],"empirical_results":0})
U["status"]="ALL_SOURCE_INTERPRETIVE_LIMITS_RETAINED_AT_DOCUMENTARY_ACCEPTANCE"
put("UNRESOLVED.json",U)
roles={}
for r in records:roles[r["role"]]=roles.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04p","historical_source_annotations":42,
 "source_passages":7,"source_limitations":20,"role_counts":roles,
 "author_reported_direction":1,"author_reported_friday_letter":1,
 "author_reported_sunday_apprehension":1,
 "independent_prisoner_outcomes":0,"new_empirical_validations":0,"runtime_promotions":0})
A={"batch":"B04p","status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_ARCHIVE_REMOTE",
 "prior_lilly_accepted":5510,"new_documentary_records":42,
 "first_record":"R5511","last_record":"R5552",
 "lilly_if_published":5552,"ptolemy_retained":1066,"combined_if_published":6618,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_pdf_pages":[504,505],"following_heading_pdf":505,
 "next_editorial_chapter":"XCVII","next_printed_chapter":"XCVI",
 "source_reverse_passages":7,"source_unresolved_limits":20,
 "independent_recaptures_verified":0,"independent_direction_outcomes_verified":0,
 "independent_prisoner_identity":0,"new_empirical_validations":0,
 "runtime_model_promotions":0,"independent_chart_recast":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04p","historical_locally_accepted":42,
 "lilly_if_published":5552,"combined_if_published":6618,
 "independent_predictive_validations":0}))
