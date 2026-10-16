#!/usr/bin/env python3
"""Freeze source-only Lilly LXXXI without alchemy or health predictive credit."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
outs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
assert not any((B/x).exists() for x in outs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json");C=J("CLAIM_LEDGER.json")
assert I["records_count"]==4631 and I["batches"][-1]["id"]=="B03z"
assert I["next"]["chapter"]=="LXXXI" and I["next"]["pdf_page"]==476
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert D["source_units"]==57 and M["span_count"]==11 and len(U["issues"])==20
assert C["independently_proven_philosophers_stones"]==0
assert C["independently_authenticated_consumption_diagnoses"]==0
assert C["new_empirical_predictive_validations"]==C["runtime_promotions"]==0
for item in W["original_images"]:
 assert H(item["path"])==item["sha256"]
 assert (B/item["path"]).stat().st_size==item["bytes"]
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261016.md").exists()
ids=[r["source_local_id"] for r in D["rows"]]
mapped=[x for s in M["source_spans"] for x in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==57 and sorted(mapped)==sorted(ids)
assert all(r["chapter"]=="LXXXI" for r in D["rows"][:-3])
assert all(r["chapter"]=="LXXXII_NAVIGATION_ONLY" for r in D["rows"][-3:])
rows=[]
for n,r in enumerate(D["rows"],start=4632):
 rows.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "accepted_for_primary_historical_text_reference":True,
 "independently_authenticated_philosophers_stone_case":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rows]==list(range(4632,4689))
R={"batch":"B04a","kind":"ORIGINAL_1647_ALCHEMY_AND_HEALTH_HISTORICAL_SOURCE_ONLY",
 "status":"DOCUMENTARY_SOURCE_ADMITTED_LOCALLY_PENDING_REMOTE",
 "documentary_accepted_locally":True,
 "record_count":57,"first_record":4632,"last_record":4688,
 "substantive_lxxxi_source_annotations":54,"next_section_and_heading_navigation_only":3,
 "source_reverse_passages":11,"unresolved_source_limits":20,
 "original_pdf_pages":[476,477,478],
 "historical_source_belief_in_stone_not_proof":True,
 "historical_health_warnings_not_medical_evidence":True,
 "independently_verified_alchemical_successes":0,
 "independently_authenticated_consumption_diagnoses":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0,
 "rules":rows}
dump("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rows}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04a","source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]}
  for s in M["source_spans"]],"span_count":11,"mapped_source_records":57})
dump("SOURCE_ORDER.json",{
 "batch":"B04a","first_record":4632,"last_record":4688,
 "record_count":57,"original_pdf_pages":[476,477,478],
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "pdf_pages":r["original_pdf_pages"]} for r in rows],
 "independent_empirical_results":0})
U["status"]="SOURCE_UNCERTAINTIES_RETAINED_AT_DOCUMENTARY_ADMISSION"
dump("UNRESOLVED.json",U)
A={"batch":"B04a","kind":"ALCHEMY_HISTORICAL_AND_UNVERIFIED_MEDICAL_TEXT_NOT_EMPIRICAL",
 "status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_ARCHIVE_AND_REMOTE",
 "documentary_accepted_locally":True,"prior_lilly_accepted":4631,
 "new_documentary_records":57,"first_record":"R4632","last_record":"R4688",
 "lilly_if_published":4688,"ptolemy_retained":1066,"combined_if_published":5754,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[476,477,478],"next_chapter":"LXXXII",
 "next_original_pdf":478,"source_reverse_passages":11,
 "unresolved_source_limits":20,"authorial_belief_is_not_validated_elixir":True,
 "medical_allegation_is_not_confirmed_diagnosis":True,
 "independently_verified_alchemical_successes":0,
 "independently_authenticated_medical_diagnoses":0,
 "new_empirically_validated_predictions":0,"runtime_model_promotions":0,
 "original_full_independent_diplomatic_transcription":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
 A[k]=H(f)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04a","locally_admitted":57,"first":"R4632","last":"R4688",
 "lilly_if_published":4688,"combined_if_published":5754,"empirical":0}))
