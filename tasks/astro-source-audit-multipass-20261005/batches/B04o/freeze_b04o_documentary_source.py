#!/usr/bin/env python3
"""Documentary admission of Lilly original dated illness/bewitchment example."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/n).exists() for n in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5457 and I["batches"][-1]["id"]=="B04n"
assert I["next"]["chapter"]=="XCV" and I["next"]["pdf_page"]==502
assert I["read_numbered_chapters"]==list(range(1,95))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert D["source_units"]==53 and M["span_count"]==10 and len(U["issues"])==22
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").is_file()
for z in W["original_images"]:
 assert H(z["path"])==z["sha256"] and (B/z["path"]).stat().st_size==z["bytes"]
localids=[r["source_local_id"] for r in D["rows"]]
mapped=[c for s in M["source_spans"] for c in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==53 and set(localids)==set(mapped)
assert all(r["chapter"]=="XCV" for r in D["rows"][:-3])
assert all(r["chapter"]=="XCVI_NAVIGATION_ONLY" for r in D["rows"][-3:])
records=[]
for n,r in enumerate(D["rows"],start=5458):
 records.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,
  "accepted_for_primary_historical_text_reference":True,
  "independently_authenticated_occult_cause":False,
  "independently_authenticated_medical_diagnosis":False,
  "independently_verified_medical_recovery":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in records]==list(range(5458,5511))
R={"batch":"B04o",
 "kind":"ORIGINAL_1647_UNVERIFIED_MEDICAL_VERSUS_OCCULT_HORARY_CASE",
 "status":"DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_REMOTE",
 "documentary_accepted_locally":True,"record_count":53,
 "first_record":5458,"last_record":5510,
 "substantive_xcv_source_units":50,"next_heading_navigation":3,
 "original_pdf_pages":[502,503,504],"source_reverse_passages":10,
 "source_unresolved_limits":22,
 "printed_chapter":"XCIV","editorial_chapter":"XCV",
 "initial_witchcraft_suspicion_described":True,
 "definitive_source_witchcraft_judgment_negative":True,
 "author_does_not_confirm_syphilis":True,
 "author_reported_recovery_about_three_weeks":True,
 "independent_verified_occult_causes":0,
 "independent_verified_medical_diagnoses":0,
 "independent_verified_medical_outcomes":0,
 "new_empirically_validated_predictions":0,
 "runtime_promotions":0,"rules":records}
put("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04o","span_count":10,"mapped_source_records":53,
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]} for s in M["source_spans"]]})
put("SOURCE_ORDER.json",{"batch":"B04o","record_count":53,
 "first_record":5458,"last_record":5510,
 "original_pdf_pages":[502,503,504],
 "records":[{"record_number":r["record_number"],"role":r["role"],
   "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]}
 for r in records],"empirical_results":0})
U["status"]="ORIGINAL_SOURCE_MEDICAL_UNCERTAINTIES_RETAINED"
put("UNRESOLVED.json",U)
rolecounts={}
for r in records:rolecounts[r["role"]]=rolecounts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04o","status":"HISTORICAL_DOCUMENTARY",
 "source_annotations":53,"passages":10,"source_issues":22,"role_counts":rolecounts,
 "preexisting_illness_worsening_author_report":1,
 "final_witchcraft_denial_author_report":1,
 "medical_hypothesis_not_confirmed":1,
 "recovery_within_three_weeks_author_report":1,
 "independent_patient_diagnoses":0,
 "independently_verified_treatment_successes":0,
 "new_empirical_predictions":0,"runtime_promotions":0})
A={"batch":"B04o","status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_ARCHIVE_REMOTE",
 "prior_lilly_accepted":5457,"new_documentary_records":53,
 "first_record":"R5458","last_record":"R5510",
 "lilly_if_published":5510,"ptolemy_retained":1066,"combined_if_published":6576,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[502,503],"following_heading_pdf":504,
 "next_editorial_chapter":"XCVI","next_printed_chapter":"XCV",
 "source_reverse_passages":10,"source_unresolved_limits":22,
 "author_final_witchcraft_verdict_negative":True,
 "author_never_confirmed_syphilis":True,
 "author_recovery_is_only_authorial_outcome_claim":True,
 "independent_medical_diagnoses":0,
 "independent_treatment_outcomes":0,"independent_occult_causes":0,
 "new_empirical_validations":0,"runtime_model_promotions":0,
 "full_independent_diplomatic_transcription":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04o","locally_accepted":53,
 "lilly_if_published":5510,"combined_if_published":6576,
 "new_empirical_validations":0}))
