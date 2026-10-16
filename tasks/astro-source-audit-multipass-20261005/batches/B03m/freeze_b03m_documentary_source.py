#!/usr/bin/env python3
"""Historical-source admission of Lilly 1647 Chapter LXVII without predictive use."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,obj):
    (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
NEED_NEW=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
          "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER_ACCEPTED_LOCAL.json"]
assert not any((B/n).exists() for n in NEED_NEW),"No overwrite of accepted material"
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
P=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
CL=J("CLAIM_LEDGER.json")
PRIOR=J("SOURCE_WINDOW_PROVISIONAL.json")
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
index=json.loads(IDX.read_text(encoding="utf-8"))
assert index["records_count"]==3746 and index["batches"][-1]["id"]=="B03l"
assert index["next"]["chapter"]=="LXVII" and index["next"]["pdf_page"]==438
assert index["source_sha256"]==W["source_original_pdf_sha256"]
assert D["source_units"]==186 and P["span_count"]==38 and len(U["issues"])==31
assert W["original_pdf_pages"]==list(range(438,447))
assert PRIOR["accepted_predecessor_lilly_count"]==3746
assert not PRIOR["numbered_chapter_admitted"]
assert [r["source_local_id"] for r in D["rows"]]==[f"LXVII-C{i:03}" for i in range(1,187)]
mapped=[k for s in P["source_spans"] for k in s["mapped_source_local_ids"]]
assert len(mapped)==186 and sorted(mapped)==sorted(r["source_local_id"] for r in D["rows"])
by_source={r["source_local_id"]:r for r in D["rows"]}
assert all(s["original_pdf_pages"]==by_source[k]["original_pdf_pages"] for s in P["source_spans"] for k in s["mapped_source_local_ids"])
assert all(r["chapter"]=="LXVII" for r in D["rows"][:-2])
assert all(r["chapter"]=="LXVIII_NAVIGATION_ONLY" for r in D["rows"][-2:])
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").is_file()
for i,v in enumerate(W["original_images"]):
    assert v["original_pdf_page"]==438+i
    assert H(v["path"])==v["sha256"]
    assert (B/v["path"]).stat().st_size==v["bytes"]
    assert v["sha256"]==PRIOR["images"][i]["sha256"]
assert CL["observed_return_cases"]==CL["observed_lifespan_cases"]==0
assert CL["new_empirically_validated_astrological_outcomes"]==0
rules=[]
for n,r in enumerate(D["rows"],start=3747):
    rules.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
                  "historical_documentary_accepted":True,
                  "accepted_for_historical_source_reference":True,
                  "authenticated_individual_outcome":False,
                  "empirically_validated_astrology_prediction":False,
                  "usable_for_personal_death_or_health_judgment":False,
                  "runtime_model_promoted":False})
assert [r["record_number"] for r in rules]==list(range(3747,3933))
assert sum(r["chapter"]=="LXVII" for r in rules)==184
assert sum(r["chapter"]=="LXVIII_NAVIGATION_ONLY" for r in rules)==2
R={"batch":"B03m","kind":"LILLY1647_LXVII_HISTORICAL_ASSERTIONS_ONLY",
   "status":"CHAPTER_LXVII_DOCUMENTARY_ACCEPTED_LOCALLY_PENDING_ARCHIVE_AND_REMOTE",
   "documentary_accepted_locally":True,
   "whole_numbered_chapter_source_intake_complete":True,
   "source_original_full_pdf_sha256":W["source_original_pdf_sha256"],
   "source_original_pdf_pages":list(range(438,447)),
   "first_record":3747,"last_record":3932,"record_count":186,
   "substantive_chapter_lxvii_units":184,"next_heading_navigation_units":2,
   "original_visual_reverse_spans":38,"retained_original_source_limits":31,
   "independent_absent_person_return_outcomes":0,
   "independent_lifespan_outcomes":0,
   "independent_spouse_death_order_outcomes":0,
   "independent_medical_cause_of_death_outcomes":0,
   "new_empirical_astrology_forecasts_validated":0,
   "runtime_rule_promotions":0,
   "blind_complete_second_diplomatic_transcription":False,
   "allowed_for_real_person_prediction":False,
   "rules":rules}
dump("RULES.json",R)
global_by_local={r["source_local_id"]:r["id"] for r in rules}
MAP={"batch":"B03m","status":"LOCALLY_ADMITTED_PRIMARY_SOURCE_TO_DOCUMENTARY_RECORD",
     "source_spans":[{**s,"accepted_global_record_ids":[global_by_local[k] for k in s["mapped_source_local_ids"]]}
                     for s in P["source_spans"]],
     "span_count":38,"source_record_count":186,"full_blind_diplomatic_reader":False}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",MAP)
ORDER={"batch":"B03m","status":"ACCEPTED_LOCAL_ORIGINAL_PAGE_ORDER_HISTORICAL_ONLY",
       "original_pdf_pages":list(range(438,447)),
       "first_record":3747,"last_record":3932,"record_count":186,
       "visual_source_passages":38,
       "original_source_reverse_map":"ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",
       "records":[{"record_number":r["record_number"],"pages":r["original_pdf_pages"],
                   "role":r["role"]} for r in rules],
       "empirical_prediction_successes_counted":0}
dump("SOURCE_ORDER.json",ORDER)
U["status"]="RETAINED_AT_LOCAL_HISTORICAL_DOCUMENTARY_ADMISSION"
dump("UNRESOLVED.json",U)
new_ledger={**CL,"status":"LOCALLY_ACCEPTED_HISTORICAL_DOCUMENTARY_PENDING_GITHUB",
            "new_locally_accepted_source_units":186,
            "new_globally_accepted_source_units":0,
            "independent_case_evidence_added":0}
dump("CLAIM_LEDGER_ACCEPTED_LOCAL.json",new_ledger)
A={"batch":"B03m","kind":"SOURCE_DOCUMENTATION_NOT_HEALTH_OR_ABSENCE_PREDICTION",
   "status":"CHAPTER_LXVII_LOCAL_DOCUMENTARY_ADMISSION_PENDING_RELEASE_AND_GITHUB",
   "documentary_accepted_locally":True,
   "whole_chapter_lxvii_source_coverage_complete":True,
   "prior_accepted_lilly":3746,
   "new_documentary_source_records":186,
   "first_record":"R3747","last_record":"R3932",
   "lilly_if_published":3932,"ptolemy_retained":1066,
   "combined_if_published":4998,
   "original_reverse_passages":38,
   "unresolved_source_issues":31,
   "original_pdf_pages":list(range(438,447)),
   "original_full_pdf_sha256":W["source_original_pdf_sha256"],
   "next_numbered_chapter":"LXVIII","next_source_pdf_page":446,
   "source_returns_independently_verified":0,
   "source_deaths_independently_verified":0,
   "source_spousal_outcomes_independently_verified":0,
   "source_clinical_cause_of_death_verified":0,
   "new_empirically_validated_predictions":0,"runtime_model_promotions":0,
   "complete_independent_diplomatic_second_reader":False,
   "real_person_death_or_health_prediction_permitted":False,
   "remote_canonical_published":False}
for n,k in [("RULES.json","rules_sha256"),
  ("SOURCE_ORDER.json","source_order_sha256"),
  ("UNRESOLVED.json","unresolved_sha256"),
  ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","original_reverse_map_sha256"),
  ("CLAIM_LEDGER_ACCEPTED_LOCAL.json","claim_ledger_sha256"),
  ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","original_visual_audit_sha256")]:
    A[k]=H(n)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B03m","locally_accepted_source_annotations":186,
      "source_spans":38,"limits":31,
      "lilly_if_published":3932,"combined_if_published":4998,
      "empirical_validations":0,
      "rules_sha256":A["rules_sha256"]},ensure_ascii=False))
