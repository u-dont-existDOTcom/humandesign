#!/usr/bin/env python3
"""Source documentary admission, original Lilly Chapter LXVIII (spouse portion)."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,v):(B/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
NEW=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
     "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
assert not any((B/n).exists() for n in NEW)
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
L=J("CLAIM_LEDGER.json")
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=json.loads(IDX.read_text())
assert I["records_count"]==3932 and I["batches"][-1]["id"]=="B03m"
assert I["next"]["chapter"]=="LXVIII" and I["next"]["pdf_page"]==446
assert I["source_sha256"]==W["source_original_pdf_sha256"]
assert D["source_units"]==44 and M["span_count"]==11 and len(U["issues"])==15
assert [r["source_local_id"] for r in D["rows"]]==[f"LXVIII-C{i:03}" for i in range(1,45)]
assert all(r["chapter"]=="LXVIII" for r in D["rows"][:-1])
assert D["rows"][-1]["chapter"]=="LXIX_NAVIGATION_ONLY"
ids=[k for s in M["source_spans"] for k in s["mapped_source_local_ids"]]
assert len(ids)==44 and sorted(ids)==sorted(r["source_local_id"] for r in D["rows"])
by={r["source_local_id"]:r for r in D["rows"]}
assert all(s["original_pdf_pages"]==by[k]["original_pdf_pages"] for s in M["source_spans"] for k in s["mapped_source_local_ids"])
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").is_file()
for i in W["images"]:
    assert H(i["path"])==i["sha256"]
    assert (B/i["path"]).stat().st_size==i["bytes"]
rules=[]
for n,r in enumerate(D["rows"],start=3933):
    rules.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
         "documentary_admitted":True,"source_historical_reference_accepted":True,
         "independent_wealth_outcome_authenticated":False,
         "validated_predictive_case":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rules]==list(range(3933,3977))
R={"batch":"B03n","kind":"HISTORICAL_DOWRY_WEALTH_SOURCE_ONLY",
 "status":"CHAPTER_LXVIII_LOCALLY_DOCUMENTARY_ADMITTED_PENDING_RELEASE",
 "documentary_accepted_locally":True,
 "source_original_pdf_sha256":W["source_original_pdf_sha256"],
 "source_pdf_pages":[446,447,448],
 "record_count":44,"first_record":3933,"last_record":3976,
 "chapter_lxviii_source_units":43,"lxix_navigation_only_units":1,
 "reverse_source_passages":11,"retained_source_issues":15,
 "independent_dowry_receipts_verified":0,"independent_fraud_cases_verified":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0,
 "full_blind_second_diplomatic_transcription_done":False,
 "rules":rules}
dump("RULES.json",R)
mapping={r["source_local_id"]:r["id"] for r in rules}
REV={"batch":"B03n","status":"LOCALLY_ADMITTED_ORIGINAL_TO_RECORD_REVERSE_MAP",
 "source_spans":[{**s,"canonical_record_ids":[mapping[k] for k in s["mapped_source_local_ids"]]}
                 for s in M["source_spans"]],
 "span_count":11,"mapped_global_records":44}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",REV)
dump("SOURCE_ORDER.json",{"batch":"B03n","status":"LOCAL_ORIGINAL_SOURCE_ORDER",
 "original_pdf_pages":[446,447,448],"record_count":44,
 "first_record":3933,"last_record":3976,
 "records":[{"record_number":r["record_number"],"original_pdf_pages":r["original_pdf_pages"],
             "role":r["role"]} for r in rules],"empirical_cases_counted":0})
U["status"]="RETAINED_SOURCE_UNCERTAINTIES_AFTER_LOCAL_ADMISSION"
dump("UNRESOLVED.json",U)
A={"batch":"B03n","kind":"LILLY1647_LXVIII_DOCUMENTARY_SOURCE_NOT_EMPRICIAL",
 "status":"LOCAL_ADMISSION_PENDING_ARCHIVE_AND_GITHUB",
 "documentary_accepted_locally":True,
 "previous_lilly_accepted":3932,"new_documentary_records":44,
 "first_record":"R3933","last_record":"R3976",
 "lilly_if_published":3976,"ptolemy_retained":1066,"combined_if_published":5042,
 "original_reverse_spans":11,"unresolved_source_issues":15,
 "original_full_pdf_sha256":W["source_original_pdf_sha256"],
 "next_chapter":"LXIX","next_original_pdf_page":448,
 "independent_dowry_outcomes":0,"independent_fraud_claims_verified":0,
 "empirical_predictions_validated":0,"runtime_promotions":0,
 "original_blind_second_transcription":False,"canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),
 ("SOURCE_ORDER.json","order_sha256"),("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_audit_sha256")]:
    A[k]=H(f)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B03n","new_locally_admitted":44,
 "lilly_if_published":3976,"combined_if_published":5042,
 "source_passages":11,"new_empirical":0}))
