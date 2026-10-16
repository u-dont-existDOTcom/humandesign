#!/usr/bin/env python3
"""One-time source documentary admission, Lilly LXVI original Reading siege.
Does not validate war outcomes, chart prediction accuracy or legal hypotheticals.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
sha=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,obj):
 (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
OUT=['RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
     'CLAIM_LEDGER_ACCEPTED_LOCAL.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
assert not any((B/f).exists() for f in OUT),"One-time freeze; do not overwrite documentary packet"
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json"); C=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json"); U=J("UNRESOLVED_SOURCE_LIMITS.json")
L=J("CLAIM_LEDGER.json")
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert idx["records_count"]==3670 and idx["batches"][-1]["id"]=="B03k"
assert idx["next"]["chapter"]=="LXVI" and idx["next"]["pdf_page"]==435
assert idx["source_sha256"]==W["original_full_pdf_sha256"]
assert D["source_units"]==76 and C["span_count"]==19 and len(U["issues"])==23
assert [r["source_local_id"] for r in D["rows"]]==[f"LXVI-C{i:03}" for i in range(1,77)]
mapped=[k for sp in C["source_spans"] for k in sp["mapped_source_local_ids"]]
assert len(mapped)==76 and sorted(mapped)==sorted(r["source_local_id"] for r in D["rows"])
assert all(r["chapter"]=="LXVI" for r in D["rows"][:-2])
assert all(r["chapter"]=="LXVII_NAVIGATION_ONLY" for r in D["rows"][-2:])
assert W["original_figure_date"]=="17 April 1643"
assert W["original_surrender_sentence_year"]=="1644"
assert W["historically_corrob_surrender_year"]=="1643"
assert L["surrender_forecast_days_late_as_admitted_by_author"]==3
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").is_file()
for f in W["original_images"]:
 assert sha(f["path"])==f["sha256"]
 assert (B/f["path"]).stat().st_size==f["size_bytes"]
rules=[]
for n,r in enumerate(D["rows"],start=3671):
    rules.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
       "historical_documentary_accepted":True,
       "source_record_admitted_for_documentary_reference":True,
       "source_case_outcome_independently_authenticated":False,
       "empirical_astrological_prediction_validated":False,
       "new_runtime_predicate_active":False})
assert [r["record_number"] for r in rules]==list(range(3671,3747))
assert sum(r["chapter"]=="LXVI" for r in rules)==74
assert sum(r["chapter"]=="LXVII_NAVIGATION_ONLY" for r in rules)==2
R={"batch":"B03l","kind":"LILLY_1647_READING_AND_COUNTERFACTUAL_LAWSUIT_SOURCE_ONLY",
   "status":"ORIGINAL_LXVI_HISTORICAL_DOCUMENTARY_ADMITTED_LOCALLY",
   "documentary_accepted_locally":True,"whole_chapter_lxvi_documentary_complete":True,
   "original_full_pdf_sha256":W["original_full_pdf_sha256"],
   "original_pdf_pages":[435,436,437,438],
   "record_count":76,"first_record":3671,"last_record":3746,
   "substantive_lxvi_annotations":74,"next_chapter_navigation_only":2,
   "original_reverse_source_passages":19,"original_text_limitations_retained":23,
   "original_chart_date":"17 April 1643","original_chart_time":"6:50 PM",
   "original_surrender_year_as_printed":"1644",
   "externally_corrob_surrender_year":"1643",
   "author_admitted_surrender_days_after_deadline":3,
   "negotiation_beginning_near_forecast_deadline_not_surrender":True,
   "author_reported_historical_Reading_cases":1,
   "independently_validated_predictive_cases":0,
   "hypothetical_lawsuits_empirically_observed":0,
   "independent_second_diplomatic_transcription_done":False,
   "runtime_promotions":0,"rules":rules}
dump("RULES.json",R)
by_local={r["source_local_id"]:r["id"] for r in rules}
rev={"batch":"B03l","status":"LOCALLY_ADMITTED_ORIGINAL_IMAGE_SOURCE_REVERSE_MAP",
     "source_spans":[{**sp,"canonical_record_ids":[by_local[k] for k in sp["mapped_source_local_ids"]]}
                     for sp in C["source_spans"]],
     "span_count":19,"mapped_unique_accepted_annotations":76,
     "independent_diplomatic_second_reader":False}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",rev)
order={"batch":"B03l","status":"LOCALLY_ADMITTED_HISTORICAL_ORIGINAL_SOURCE_ORDER",
       "original_pdf_pages":[435,436,437,438],"first_record":3671,"last_record":3746,
       "record_count":76,"source_spans":19,
       "records":[{"record_number":r["record_number"],
                   "original_pdf_pages":r["original_pdf_pages"],"role":r["role"]}
                  for r in rules],
       "original_source_reverse_map":"ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",
       "empirical_prediction_results_added":0}
dump("SOURCE_ORDER.json",order)
U["status"]="RETAINED_AT_LOCAL_DOCUMENTARY_ACCEPTANCE"
dump("UNRESOLVED.json",U)
localledger={**L,"status":"LOCALLY_ACCEPTED_DOCUMENTARY_NOT_YET_GITHUB_PUBLISHED",
             "locally_admitted_source_units":76,
             "globally_accepted_new_units":0,
             "reported_1644_typographic_year_marked_not_repaired":True,
             "source_internal_result_counted_as_empirical":0}
dump("CLAIM_LEDGER_ACCEPTED_LOCAL.json",localledger)
A={"batch":"B03l","kind":"DOCUMENTARY_ORIGINAL_LILLY_READING_SIEGE_AND_LAWSUIT_ONLY",
   "status":"CHAPTER_LXVI_SOURCE_ACCEPTED_LOCALLY_PENDING_RELEASE_AND_GITHUB",
   "documentary_accepted_locally":True,"whole_chapter_lxvi_documentary_complete":True,
   "previous_lilly_accepted":3670,"new_documentary_records":76,
   "first_record":"R3671","last_record":"R3746",
   "lilly_if_published":3746,"retained_ptolemy":1066,
   "combined_if_published":4812,"original_reverse_spans":19,
   "retained_source_issues":23,"original_body_pages":[435,436,437,438],
   "next_chapter":"LXVII","next_heading_pdf":438,
   "original_full_pdf_sha256":W["original_full_pdf_sha256"],
   "original_chart_date":"17 April 1643","original_chart_time":"6:50 PM",
   "original_literal_surrender_year":"1644",
   "historically_corrob_surrender_year":"1643",
   "surrender_three_days_late_as_author_says":True,
   "negotiations_near_deadline_not_identical_to_capture":True,
   "source_internal_favorable_historical_siege_cases":1,
   "independently_authenticated_predictive_cases":0,
   "independently_blind_observed_lawsuit_cases":0,
   "new_empirical_predictions_validated":0,"runtime_promotions":0,
   "blind_complete_diplomatic_second_transcription":False,
   "canonical_published":False}
for n,k in [("RULES.json","rules_sha256"),
            ("SOURCE_ORDER.json","source_order_sha256"),
            ("UNRESOLVED.json","unresolved_sha256"),
            ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_source_map_sha256"),
            ("CLAIM_LEDGER_ACCEPTED_LOCAL.json","claim_ledger_sha256"),
            ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","visual_audit_sha256")]:
    A[k]=sha(n)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B03l","locally_accepted":76,
      "lilly_if_published":3746,"combined_if_published":4812,
      "source_spans":19,"unresolved":23,
      "new_validated_cases":0,"rules_sha256":A["rules_sha256"]}))
