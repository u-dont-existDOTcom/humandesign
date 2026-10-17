#!/usr/bin/env python3
"""Freeze historical Animodar clauses without prediction/rectification promotion."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
out=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/x).exists() for x in out)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5923 and I["batches"][-1]["id"]=="B04w"
assert I["read_numbered_chapters"]==list(range(1,100))
assert I["next"]["chapter"]=="C" and I["next"]["pdf_page"]==539
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==34 and len(M)==5 and len(U["issues"])==22
assert W["source_author_deems_Animodar_less_sure_than_accidents"]
assert W["no_externally_verified_natal_success"]
for w in W["original_images"]:
 assert H(w["path"])==w["sha256"] and (B/w["path"]).stat().st_size==w["bytes"]
sourceids=[r["source_local_id"] for r in D]
mapids=[x for s in M for x in s["mapped_local_ids"]]
assert len(mapids)==len(set(mapids))==34 and set(sourceids)==set(mapids)
records=[{**r,"id":f"R{k}","record_number":k,"global_record_number":k,
 "historical_documentary_accepted":True,
 "independently_authenticated_birth_time":False,
 "independently_validated_Animodar_accuracy":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for k,r in enumerate(D,5924)]
assert [r["record_number"] for r in records]==list(range(5924,5958))
assert all(r["chapter"]=="C" for r in records[:-3])
assert all(r["chapter"]=="CI_NAVIGATION_ONLY" for r in records[-3:])
rules={"batch":"B04x","status":"HISTORICAL_DOCUMENTARY_LOCALLY_ADMITTED_NOT_EMPIRICAL",
 "record_count":34,"first_record":5924,"last_record":5957,
 "printed_chapter":"XCIX","editorial_chapter":"C",
 "substantive_source_annotations":31,"following_chapter_navigation":3,
 "original_pdf_pages":[539,540,541],
 "source_spans":5,"source_limitations":22,
 "full_moon_or_new_moon_source_branch_preserved":True,
 "essential_dignity_ties_source_resolution_preserved":True,
 "source_Animodar_less_reliable_than_accidents":True,
 "preexisting_accident_rectification_causes_benchmark_leakage":True,
 "independent_known_birth_time_accuracies":0,
 "new_empirical_validations":0,"runtime_promotions":0,"rules":records}
put("RULES.json",rules)
lookup={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04x","span_count":5,"mapped_source_records":34,
 "source_spans":[{**s,"accepted_global_record_ids":[lookup[k] for k in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B04x","first_record":5924,"last_record":5957,"record_count":34,
 "original_pdf_pages":[539,540,541],
 "records":[{"record_number":r["record_number"],"source_span_id":r["source_span_id"],
 "role":r["role"],"original_pdf_pages":r["original_pdf_pages"]} for r in records]})
U["status"]="FIRST_EDITION_TEXTUAL_AND_VALIDITY_UNCERTAINTIES_RETAINED"
put("UNRESOLVED.json",U)
counts={}
for r in records:counts[r["role"]]=counts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04x","historical_source_units":34,"source_passages":5,"limits":22,
 "role_counts":counts,"merchant_actual_birth_time_authenticated":False,
 "Animodar_vs_accidents_independent_comparison":False,
 "new_empirical_validations":0,"runtime_promotions":0})
A={"batch":"B04x","status":"LOCAL_DOCUMENTARY_ACCEPTED_PENDING_ARCHIVE_GITHUB",
 "prior_lilly":5923,"new_documentary_records":34,
 "first_record":"R5924","last_record":"R5957","lilly_if_published":5957,
 "ptolemy_retained":1066,"combined_if_published":7023,
 "source_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[539,540],"next_heading_pdf":541,
 "next_printed_chapter":"C","next_editorial_chapter":"CI",
 "source_passages":5,"source_limits":22,
 "source_says_Animodar_weaker_than_accidents":True,
 "preexisting_accident_rectification_used_as_target":True,
 "independent_birth_time_accuracies":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04x","locally_admitted":34,"lilly_if_published":5957,
 "combined_if_published":7023,"next":"accidents PDF541","empirical_validations":0}))
