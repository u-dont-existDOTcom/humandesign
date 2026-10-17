#!/usr/bin/env python3
"""Accept original first-edition Lilly natal prejudgment conditional clauses as historical source only."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
out=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/q).exists() for q in out)
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=json.loads(IDX.read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==6215 and I["batches"][-1]["id"]=="B04z"
assert I["next"]["chapter"]=="CIII" and I["next"]["pdf_page"]==558
assert I["read_numbered_chapters"]==list(range(1,103))
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert len(D)==29 and len(M)==4 and len(U["issues"])==17
assert not W["source_antiscia_numeric_orb_stated"] and not W["source_fixed_stars_small_latitude_numeric_threshold_stated"]
for x in W["original_images"]:
 assert H(x["path"])==x["sha256"] and (B/x["path"]).stat().st_size==x["bytes"]
local=[x["source_local_id"] for x in D]
mapped=[y for s in M for y in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==29 and set(mapped)==set(local)
records=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "independently_verified_natal_outcome":False,
 "empirically_validated_prediction":False,
 "runtime_model_promoted":False}
 for n,r in enumerate(D,6216)]
assert [r["record_number"] for r in records]==list(range(6216,6245))
assert all(r["chapter"]=="CIII" for r in records[:-3])
assert all(r["chapter"]=="CIV_NAVIGATION_ONLY" for r in records[-3:])
R={"batch":"B05a","kind":"FIRST_EDITION_1647_NATAL_PREJUDGMENT_CONDITIONAL_SOURCE_ONLY",
 "status":"LOCALLY_DOCUMENTARY_ACCEPTED_PENDING_PUBLICATION",
 "record_count":29,"first_record":6216,"last_record":6244,
 "source_substantive_annotations":26,"following_lifespan_navigation":3,
 "printed_chapter":"CII","editorial_chapter":"CIII",
 "original_pdf_pages":[558,559],"original_source_spans":4,
 "unresolved_source_limits":17,
 "source_accident_rectification_author_preferred":True,
 "source_unquantified_antiscia_orb":True,
 "source_unquantified_fixed_star_latitude_threshold":True,
 "source_next_chapter_mortality_not_imported":True,
 "independent_natal_cases_confirmed":0,
 "new_empirical_validations":0,"runtime_promotions":0,"rules":records}
put("RULES.json",R)
by={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B05a","span_count":4,"mapped_source_records":29,
 "source_spans":[{**s,"accepted_global_record_ids":[by[x] for x in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B05a",
 "first_record":6216,"last_record":6244,"record_count":29,
 "original_pdf_pages":[558,559],
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in records]})
U["status"]="UNQUANTIFIED_ORBS_AND_HISTORICAL_CLAIMS_RETAINED_AT_ACCEPTANCE"
put("UNRESOLVED.json",U)
roles={}
for r in records:roles[r["role"]]=roles.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B05a","documentary_annotations":29,
 "source_groups":4,"source_limits":17,"role_counts":roles,
 "numerically_quantified_antiscia_distance":False,
 "numerically_quantified_fixed_star_latitude":False,
 "observed_prediction_cases":0,"new_empirical_validations":0,"runtime_promotions":0})
A={"batch":"B05a","status":"LOCALLY_ACCEPTED_DOCUMENTARY_PENDING_ARCHIVE_GITHUB",
 "prior_lilly":6215,"new_documentary_records":29,
 "first_record":"R6216","last_record":"R6244",
 "lilly_if_published":6244,"ptolemy_retained":1066,"combined_if_published":7310,
 "original_full_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[558],"following_heading_pdf":559,
 "next_printed_chapter":"CIII","next_editorial_chapter":"CIV",
 "source_spans":4,"source_unresolved_limits":17,
 "source_antiscia_and_fixed_star_numeric_thresholds_unspecified":True,
 "actual_person_outcomes_verified":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B05a","source_records_added":29,
 "lilly_if_published":6244,"combined_if_published":7310,
 "next":"printed CIII lifespan original PDF559","empirical_validations":0}))
