#!/usr/bin/env python3
"""Source-only documentary admission: printed XCI, editorial XCII."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
J=lambda name:json.loads((B/name).read_text(encoding="utf-8"))
H=lambda name:hashlib.sha256((B/name).read_bytes()).hexdigest()
def put(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
outputs=["RULES.json","SOURCE_ORDER.json","ACCEPTANCE.json",
 "UNRESOLVED.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/n).exists() for n in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5307 and I["batches"][-1]["id"]=="B04k"
assert I["next"]["chapter"]=="XCII" and I["next"]["pdf_page"]==497
assert I["read_numbered_chapters"]==list(range(1,92))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert D["source_units"]==31 and len(D["rows"])==31 and M["span_count"]==5
assert len(U["issues"])==19 and (B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").is_file()
for x in W["original_images"]:
 assert H(x["path"])==x["sha256"] and (B/x["path"]).stat().st_size==x["bytes"]
localids=[r["source_local_id"] for r in D["rows"]]
mapp=[c for s in M["source_spans"] for c in s["mapped_local_ids"]]
assert len(mapp)==len(set(mapp))==31 and set(localids)==set(mapp)
assert all(r["chapter"]=="XCII" for r in D["rows"][:-2])
assert all(r["chapter"]=="XCIII_NAVIGATION_ONLY" for r in D["rows"][-2:])
rules=[]
for n,r in enumerate(D["rows"],start=5308):
 rules.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,
  "accepted_for_primary_historical_text_reference":True,
  "independently_authenticated_captive_outcome":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rules]==list(range(5308,5339))
R={"batch":"B04l","kind":"ORIGINAL_1647_CAPTIVITY_HISTORICAL_SOURCE_ONLY",
 "status":"DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_PUBLICATION",
 "documentary_accepted_locally":True,"record_count":31,
 "first_record":5308,"last_record":5338,"substantive_source_annotations":29,
 "following_chapter_navigation_only":2,"source_reverse_passages":5,
 "source_uncertainties_retained":19,"original_pdf_pages":[497,498],
 "original_printed_chapter":"XCI","editorial_chapter":"XCII",
 "hour_rule_source_claims_not_facts":True,
 "independently_authenticated_captive_outcomes":0,
 "new_empirical_predictive_validations":0,
 "runtime_promotions":0,"rules":rules}
put("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rules}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04l",
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]}
 for s in M["source_spans"]],"span_count":5,"mapped_source_records":31})
put("SOURCE_ORDER.json",{"batch":"B04l","record_count":31,
 "first_record":5308,"last_record":5338,
 "original_pdf_pages":[497,498],"records":[{
 "record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]
 } for r in rules],"empirical_results":0})
U["status"]="ORIGINAL_SOURCE_ISSUES_RETAINED_AT_ADMISSION"
put("UNRESOLVED.json",U)
counts={}
for r in rules:counts[r["role"]]=counts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04l","status":"HISTORICAL_SOURCE_ONLY",
 "source_units":31,"source_passages":5,"source_uncertainties":19,
 "role_counts":counts,"next_chapter_navigation":2,"independent_captive_outcomes":0,
 "empirical_predictions_validated":0,"runtime_promotions":0})
A={"batch":"B04l","status":"LOCALLY_ADMITTED_PENDING_ARCHIVE_AND_REMOTE",
 "prior_lilly_accepted":5307,"new_documentary_records":31,
 "first_record":"R5308","last_record":"R5338",
 "lilly_if_published":5338,"retained_ptolemy":1066,
 "combined_if_published":6404,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_pdf_pages":[497,498],
 "following_heading_pdf":498,"next_editorial_chapter":"XCIII",
 "next_printed_chapter":"XCII","source_reverse_passages":5,
 "source_uncertainties":19,"independent_captive_outcomes":0,
 "new_empirical_validations":0,"runtime_promotions":0,
 "independent_full_diplomatic_transcription":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04l","historical_locally_accepted":31,
 "lilly_if_published":5338,"combined_if_published":6404,
 "independent_predictions":0}))
