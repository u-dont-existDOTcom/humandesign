#!/usr/bin/env python3
"""Admit Lilly event-fitted rectification as historical source only, never predictive evidence."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
out=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/x).exists() for x in out)
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert idx["records_count"]==5957 and idx["batches"][-1]["id"]=="B04x"
assert idx["next"]["chapter"]=="CI" and idx["next"]["pdf_page"]==541
assert idx["read_numbered_chapters"]==list(range(1,101))
assert idx["source_sha256"]==W["original_full_pdf_sha256"]
assert idx["empirical_validations"]==idx["runtime_promotions"]==0
assert len(D)==188 and len(M)==13 and len(U["issues"])==25
assert W["source_fever_age_mismatch_unresolved"] and not W["all_speculum_numeric_cells_transcribed"]
assert W["source_page546_apparent_misprint"]=="105deg44" and W["source_page547_follows_correct_value"]=="205deg44"
for image in W["original_images"]:
 assert H(image["path"])==image["sha256"] and (B/image["path"]).stat().st_size==image["bytes"]
local=[r["source_local_id"] for r in D];mapped=[q for s in M for q in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==188 and set(local)==set(mapped)
records=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "independently_authenticated_merchant_life_event":False,
 "independently_validated_birth_time_rectification":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for n,r in enumerate(D,5958)]
assert [r["record_number"] for r in records]==list(range(5958,6146))
assert all(r["chapter"]=="CI" for r in records[:-3])
assert all(r["chapter"]=="CII_NAVIGATION_ONLY" for r in records[-3:])
R={"batch":"B04y","status":"ORIGINAL_1647_HISTORICAL_DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_REMOTE",
 "kind":"RETROSPECTIVE_ACCIDENT_FITTING_AND_SPECULUM_SOURCE_WITH_NEGATIVE_CHRONOLOGY",
 "record_count":188,"first_record":5958,"last_record":6145,
 "substantive_chapter_source_units":185,"next_numbered_chapter_navigation":3,
 "printed_chapter":"C","editorial_chapter":"CI",
 "original_pdf_pages":list(range(541,555)),
 "source_passages":13,"source_unresolved_limits":25,
 "all_original_image_witnesses_complete":True,
 "full_numeric_speculum_transcription_complete":False,
 "merchant_initial_reported_event_count":4,
 "calibration_hit_career_16y7m":True,
 "fever_initial_target_20y10m_vs_later_fit_19y10m10d_unresolved":True,
 "biquintile_105vs205_source_discrepancy":True,
 "accepts_year_only_events":True,
 "candidate_chart_adjustment_forward_backward":True,
 "independently_verified_true_birth_time":False,
 "out_of_sample_predictive_validation":False,
 "new_empirical_validations":0,"runtime_promotions":0,
 "rules":records}
put("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04y","span_count":13,"mapped_source_records":188,
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[q] for q in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B04y","first_record":5958,"last_record":6145,
 "record_count":188,"source_pdf_pages":list(range(541,555)),
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in records]})
U["status"]="ORIGINAL_HISTORICAL_NUMERIC_AND_EVALUATION_LIMITATIONS_RETAINED"
put("UNRESOLVED.json",U)
roles={}
for r in records:roles[r["role"]]=roles.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04y","source_annotations":188,
 "passage_groups":13,"source_limits":25,"role_counts":roles,
 "merchant_original_four_events":4,
 "merchant_event_records_independently_authenticated":0,
 "reported_career_fit_16y7m":True,
 "discrepant_fever_timing_original_vs_fitted":True,
 "biquintile_source_number_discrepancy":True,
 "out_of_sample_predictions_validated":0,"runtime_promotions":0})
A={"batch":"B04y","status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_ARCHIVE_GITHUB",
 "prior_lilly_accepted":5957,"new_documentary_records":188,
 "first_record":"R5958","last_record":"R6145",
 "lilly_if_published":6145,"retained_ptolemy":1066,"combined_if_published":7211,
 "original_source_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":list(range(541,554)),
 "next_heading_pdf":553,"following_printed_chapter":"CI",
 "next_editorial_chapter":"CII",
 "source_passages":13,"source_limits":25,
 "source_original_reported_fever":"20y10m",
 "source_directed_fever_fit":"19y10m10d",
 "source_fever_timing_mismatch_unresolved":True,
 "source_biquintile_page546_misprint":"105deg44",
 "arithmetic_biquintile_correct":"205deg44",
 "source_speculum_full_numeric_data_complete":False,
 "event_fitting_in_sample_only":True,
 "independent_birth_times_verified":0,
 "new_empirical_validations":0,"runtime_promotions":0,
 "remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04y","locally_accepted_historical_records":188,
 "lilly_if_published":6145,"combined_if_published":7211,
 "merchant_independent_matches":0,"source_fever_mismatch":True}))
