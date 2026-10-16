#!/usr/bin/env python3
"""Admit original Chapter LXXX as historical source, never as predictive proof."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
         "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
assert not any((B/n).exists() for n in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json"); M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json"); U=J("UNRESOLVED_SOURCE_LIMITS.json")
C=J("CLAIM_LEDGER.json")
assert I["records_count"]==4549 and I["batches"][-1]["id"]=="B03y"
assert I["next"]["chapter"]=="LXXX" and I["next"]["pdf_page"]==473
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert D["source_units"]==82 and M["span_count"]==13 and len(U["issues"])==24
assert C["historically_independently_verified_outcomes"]==0
assert C["independently_validated_predictive_results"]==0
assert C["runtime_model_promotions"]==0
for x in W["original_images"]:
    assert H(x["path"])==x["sha256"]
    assert (B/x["path"]).stat().st_size==x["bytes"]
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").is_file()
ids=[r["source_local_id"] for r in D["rows"]]
mapped=[k for s in M["source_spans"] for k in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==82 and sorted(ids)==sorted(mapped)
byid={r["source_local_id"]:r for r in D["rows"]}
assert all(set(byid[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
    for s in M["source_spans"] for k in s["mapped_local_ids"])
assert all(r["chapter"]=="LXXX" for r in D["rows"][:-2])
assert all(r["chapter"]=="LXXXI_NAVIGATION_ONLY" for r in D["rows"][-2:])
rules=[]
for n,r in enumerate(D["rows"],start=4550):
    rules.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
     "historical_documentary_accepted":True,
     "accepted_for_primary_historical_text_reference":True,
     "independently_authenticated_religious_political_outcome":False,
     "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rules]==list(range(4550,4632))
R={"batch":"B03z","kind":"ORIGINAL_1647_HISTORICAL_ENGLISH_PRESBYTERY_SOURCE_ONLY",
   "status":"LOCALLY_HISTORICAL_ACCEPTED_PENDING_RELEASE_REMOTE",
   "documentary_accepted_locally":True,
   "record_count":82,"first_record":4550,"last_record":4631,
   "substantive_lxxx_source_annotations":80,"next_heading_navigation_only":2,
   "source_reverse_passages":13,"unresolved_source_issues":24,
   "original_pdf_pages":[473,474,475,476],
   "printed_question_time":"11 March 1646 over 7, 4:45 PM",
   "historical_three_year_claim_documented":True,
   "historical_status_quo_reform_qualification_retained":True,
   "independently_verified_political_events":0,
   "new_empirically_validated_predictions":0,"runtime_promotions":0,
   "rules":rules}
dump("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rules}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B03z","source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]}
        for s in M["source_spans"]],
 "span_count":13,"mapped_source_records":82})
dump("SOURCE_ORDER.json",{"batch":"B03z","first_record":4550,"last_record":4631,
 "record_count":82,"original_pdf_pages":[473,474,475,476],
 "records":[{"record_number":r["record_number"],"role":r["role"],
            "pdf_pages":r["original_pdf_pages"],"source_span_id":r["source_span_id"]}
           for r in rules],"independent_empirical_results":0})
U["status"]="ORIGINAL_SOURCE_QUALIFICATIONS_RETAINED_AT_ADMISSION"
dump("UNRESOLVED.json",U)
A={"batch":"B03z","kind":"POLITICAL_RELIGIOUS_HISTORICAL_FORECAST_TEXT_NOT_VALIDATED",
 "status":"LOCAL_DOCUMENTARY_SOURCE_ADMITTED_PENDING_ARCHIVE_AND_GITHUB",
 "documentary_accepted_locally":True,
 "prior_lilly_accepted":4549,"new_documentary_records":82,
 "first_record":"R4550","last_record":"R4631","lilly_if_published":4631,
 "ptolemy_retained":1066,"combined_if_published":5697,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[473,474,475,476],
 "following_heading_pdf":476,"source_reverse_passages":13,
 "original_unresolved_limits":24,
 "next_chapter":"LXXXI","next_original_pdf":476,
 "source_predicted_window":"within three whole years of 11 March 1646/7",
 "status_quo_qualification_preserved":True,
 "independently_verified_political_outcomes":0,
 "new_empirically_validated_predictions":0,
 "runtime_model_promotions":0,
 "original_full_independent_diplomatic_transcription":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
 A[k]=H(f)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B03z","locally_admitted_source_annotations":82,
  "first":"R4550","last":"R4631","lilly_if_published":4631,
  "combined_if_published":5697,"empirical_validations":0}))
