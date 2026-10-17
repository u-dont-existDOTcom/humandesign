#!/usr/bin/env python3
"""Documentary-only admission of original dated horse-recovery question."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
 "ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/n).exists() for n in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5413 and I["batches"][-1]["id"]=="B04m"
assert I["read_numbered_chapters"]==list(range(1,94))
assert I["next"]["chapter"]=="XCIV" and I["next"]["pdf_page"]==501
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert D["source_units"]==44 and M["span_count"]==7 and len(U["issues"])==20
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").is_file()
for p in W["original_images"]:
 assert H(p["path"])==p["sha256"] and (B/p["path"]).stat().st_size==p["bytes"]
ids=[r["source_local_id"] for r in D["rows"]]
mapped=[k for s in M["source_spans"] for k in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==44 and sorted(ids)==sorted(mapped)
by={r["source_local_id"]:r for r in D["rows"]}
assert all(set(by[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
           for s in M["source_spans"] for k in s["mapped_local_ids"])
assert all(r["chapter"]=="XCIV" for r in D["rows"][:-2])
assert all(r["chapter"]=="XCV_NAVIGATION_ONLY" for r in D["rows"][-2:])
rows=[]
for n,r in enumerate(D["rows"],start=5414):
 rows.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,
  "accepted_for_primary_historical_text_reference":True,
  "independently_authenticated_horse_recovery":False,
  "independently_authenticated_theft_or_riders":False,
  "empirically_validated_prediction":False,
  "runtime_model_promoted":False})
assert [r["record_number"] for r in rows]==list(range(5414,5458))
R={"batch":"B04n","kind":"ORIGINAL_1647_HENLEY_LOST_HORSE_RETROSPECTIVE_SOURCE_ONLY",
 "status":"LOCALLY_ACCEPTED_DOCUMENTARY_PENDING_GITHUB",
 "documentary_accepted_locally":True,
 "record_count":44,"first_record":5414,"last_record":5457,
 "substantive_xciv_source_units":42,"next_chapter_navigation":2,
 "original_pdf_pages":[501,502],"source_reverse_passages":7,
 "source_uncertainties":20,
 "printed_chapter":"XCIII","editorial_chapter":"XCIV",
 "author_initial_one_two_day_prediction":True,
 "author_reports_three_day_return":True,
 "author_reports_one_day_early_estimate":True,
 "actual_day_january_13_or_14_ambiguous":True,
 "independently_authenticated_horse_outcomes":0,
 "independently_identified_thieves":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0,
 "rules":rows}
put("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rows}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04n",
 "span_count":7,"mapped_source_records":44,
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]}
   for s in M["source_spans"]]})
put("SOURCE_ORDER.json",{"batch":"B04n","first_record":5414,
 "last_record":5457,"record_count":44,"original_pdf_pages":[501,502],
 "records":[{"record_number":r["record_number"],"role":r["role"],
  "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]}
 for r in rows],"empirical_results":0})
U["status"]="SOURCE_LIMITATIONS_RETAINED_AT_ADMISSION"
put("UNRESOLVED.json",U)
rc={}
for r in rows:rc[r["role"]]=rc.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04n","historical_source_units":44,
 "source_passages":7,"retained_limitations":20,
 "roles":rc,"self_reported_recovery":1,
 "self_reported_lateness_or_timing_discrepancy":1,
 "printed_return_day_ambiguity":True,
 "independent_real_horse_outcomes":0,
 "empirically_validated_predictions":0,"runtime_promotions":0})
A={"batch":"B04n","status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_REMOTE",
 "prior_lilly_accepted":5413,"new_documentary_records":44,
 "first_record":"R5414","last_record":"R5457",
 "lilly_if_published":5457,"ptolemy_retained":1066,"combined_if_published":6523,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_pdf_pages":[501,502],"following_heading_pdf":502,
 "next_chapter":"XCV","next_printed_chapter":"XCIV",
 "source_reverse_passages":7,"source_unresolved_limits":20,
 "source_author_timing_shortfall_preserved":True,
 "absolute_reported_actual_day_ambiguous":True,
 "independently_verified_recovered_horses":0,
 "independent_theft_confirmed":0,"new_empirical_validations":0,
 "runtime_model_promotions":0,"independent_chart_recast":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04n","local_source_records":44,
 "lilly_if_published":5457,"combined_if_published":6523,
 "source_author_timing_shortfall_preserved":True,"independent_predictions":0}))
