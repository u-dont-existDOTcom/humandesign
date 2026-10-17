#!/usr/bin/env python3
"""Freeze first edition Lilly historical lifespan claims without medical or predictive validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
out=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/n).exists() for n in out)
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=json.loads(IDX.read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==6244 and I["batches"][-1]["id"]=="B05a"
assert I["next"]["chapter"]=="CIV" and I["next"]["pdf_page"]==559
assert I["read_numbered_chapters"]==list(range(1,104))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==65 and len(M)==6 and len(U["issues"])==25
assert W["original_explicit_do_not_pronounce_death_rashly"]
assert W["original_lunar_phase_competing_conditions_retained"]
assert not W["source_mortality_clinical_evidence"]
for w in W["original_images"]:
 assert H(w["path"])==w["sha256"] and (B/w["path"]).stat().st_size==w["bytes"]
allids=[r["source_local_id"] for r in D];mapped=[i for s in M for i in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==65 and set(allids)==set(mapped)
records=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "independently_authenticated_infant_survival_outcome":False,
 "medical_survival_predictive_validity":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for n,r in enumerate(D,6245)]
assert [r["record_number"] for r in records]==list(range(6245,6310))
assert all(r["chapter"]=="CIV" for r in records[:-3])
assert all(r["chapter"]=="CV_NAVIGATION_ONLY" for r in records[-3:])
R={"batch":"B05b","kind":"ORIGINAL_1647_INFANT_LONGEVITY_MORTALITY_ASTROLOGY_HISTORICAL_SOURCE_ONLY",
 "status":"LOCALLY_ACCEPTED_HISTORICAL_DOCUMENTARY_NOT_MEDICAL_VALIDITY",
 "record_count":65,"first_record":6245,"last_record":6309,
 "source_substantive_annotations":62,"next_hyleg_navigation_annotations":3,
 "printed_chapter":"CIII","editorial_chapter":"CIV",
 "original_pdf_pages":[559,560,561],
 "source_passages":6,"unresolved_source_limits":25,
 "physical_last_source_page_shared_with_next_chapter":True,
 "opposing_lunar_phase_claims_retained":True,
 "author_warns_not_to_pronounce_death_rashly":True,
 "source_author_claims_not_clinical_survival_data":True,
 "independent_infant_outcomes_verified":0,
 "empirical_predictive_validations":0,"runtime_promotions":0,
 "rules":records}
put("RULES.json",R)
by={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B05b","span_count":6,"mapped_source_records":65,
 "source_spans":[{**s,"accepted_global_record_ids":[by[q] for q in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B05b","first_record":6245,
 "last_record":6309,"record_count":65,"source_pdf_pages":[559,560,561],
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in records]})
U["status"]="HISTORICAL_MORTALITY_SOURCE_CAVEATS_RETAINED_NOT_MEDICAL_EVIDENCE"
put("UNRESOLVED.json",U)
roles={}
for r in records:roles[r["role"]]=roles.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B05b","original_source_annotations":65,
 "original_source_passages":6,"source_limits":25,"role_counts":roles,
 "original_lunar_phase_competing_branches":True,
 "original_explicit_no_rash_death_judgments":True,
 "independent_infant_outcome_cases":0,
 "new_empirical_prediction_successes":0,"runtime_promotions":0})
A={"batch":"B05b","status":"LOCALLY_ACCEPTED_DOCUMENTARY_PENDING_ARCHIVE_REMOTE",
 "previous_lilly":6244,"new_historical_documentary_records":65,
 "first_record":"R6245","last_record":"R6309",
 "lilly_if_published":6309,"ptolemy_retained":1066,"combined_if_published":7375,
 "original_full_pdf_sha256":W["original_full_pdf_sha256"],
 "source_body_pdf_pages":[559,560,561],"next_heading_pdf_page":561,
 "next_printed_chapter":"CIV","next_editorial_chapter":"CV",
 "source_groups":6,"source_unresolved_limit_count":25,
 "source_asserted_survival_predictions_unvalidated":True,
 "actual_independently_verified_infant_survival_records":0,
 "new_empirical_validations":0,"runtime_promotions":0,
 "remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B05b","new_source_annotations":65,
 "lilly_if_published":6309,"combined_if_published":7375,
 "independent_survival_validations":0}))
