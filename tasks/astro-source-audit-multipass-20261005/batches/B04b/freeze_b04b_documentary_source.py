#!/usr/bin/env python3
"""Freeze Lilly 1647 LXXXII historical source, no empirical validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda f:json.loads((B/f).read_text(encoding="utf-8"))
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
names=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
       "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
assert not any((B/n).exists() for n in names)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json");C=J("CLAIM_LEDGER.json")
assert I["records_count"]==4688 and I["batches"][-1]["id"]=="B04a"
assert I["next"]["chapter"]=="LXXXII" and I["next"]["pdf_page"]==478
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert D["source_units"]==141 and M["span_count"]==21 and len(U["issues"])==26
assert C["new_empirically_validated_predictions"]==C["runtime_promotions"]==0
assert C["independently_verified_employment_outcomes"]==0
for x in W["original_images"]:
 assert H(x["path"])==x["sha256"] and (B/x["path"]).stat().st_size==x["bytes"]
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").is_file()
ids=[r["source_local_id"] for r in D["rows"]]
mapped=[k for s in M["source_spans"] for k in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==141 and sorted(ids)==sorted(mapped)
assert all(r["chapter"]=="LXXXII" for r in D["rows"][:-2])
assert all(r["chapter"]=="LXXXIII_NAVIGATION_ONLY" for r in D["rows"][-2:])
records=[]
for n,r in enumerate(D["rows"],start=4689):
 records.append({**r,"id":f"R{n}","record_number":n,
 "global_record_number":n,"historical_documentary_accepted":True,
 "accepted_for_primary_historical_text_reference":True,
 "independently_authenticated_office_outcome":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in records]==list(range(4689,4830))
dump("RULES.json",{"batch":"B04b",
 "kind":"ORIGINAL_1647_OFFICE_AND_RETENTION_HISTORICAL_SOURCE_ONLY",
 "status":"DOCUMENTARY_LOCALLY_ACCEPTED_NOT_YET_REMOTE",
 "documentary_accepted_locally":True,
 "record_count":141,"first_record":4689,"last_record":4829,
 "substantive_lxxxii_source_annotations":139,"following_heading_navigation_only":2,
 "original_pdf_pages":[478,479,480,481,482],
 "source_reverse_passages":21,"unresolved_source_limits":26,
 "separate_new_office_and_existing_office_endpoints":True,
 "independently_verified_office_outcomes":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0,
 "rules":records})
idmap={r["source_local_id"]:r["id"] for r in records}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04b","source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]}
    for s in M["source_spans"]],"span_count":21,"mapped_source_records":141})
dump("SOURCE_ORDER.json",{"batch":"B04b","first_record":4689,"last_record":4829,
 "record_count":141,"original_pdf_pages":[478,479,480,481,482],
 "records":[{"record_number":r["record_number"],"pdf_pages":r["original_pdf_pages"],
   "role":r["role"]} for r in records],"new_empirical_results":0})
U["status"]="ORIGINAL_SOURCE_LIMITS_RETAINED_AT_DOCUMENTARY_ADMISSION"
dump("UNRESOLVED.json",U)
A={"batch":"B04b","kind":"HISTORICAL_OFFICE_PREFERMENT_NOT_EMPIRICAL_PREDICTION",
 "status":"DOCUMENTARY_ADMITTED_LOCALLY_PENDING_ARCHIVE_GITHUB",
 "documentary_accepted_locally":True,
 "prior_lilly_accepted":4688,"new_documentary_records":141,
 "first_record":"R4689","last_record":"R4829",
 "lilly_if_published":4829,"ptolemy_retained":1066,"combined_if_published":5895,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[478,479,480,481,482],
 "following_heading_pdf":482,"next_chapter":"LXXXIII","next_original_pdf":482,
 "source_reverse_passages":21,"source_unresolved_limits":26,
 "office_acquisition_distinct_from_office_retention":True,
 "independently_verified_office_outcomes":0,
 "new_empirically_validated_predictions":0,"runtime_model_promotions":0,
 "independent_full_diplomatic_second_transcription":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
 A[k]=H(f)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04b","historical_documentary_local":141,
 "lilly_if_published":4829,"combined_if_published":5895,
 "verified_office_outcomes":0,"next_chapter":"LXXXIII"}))
