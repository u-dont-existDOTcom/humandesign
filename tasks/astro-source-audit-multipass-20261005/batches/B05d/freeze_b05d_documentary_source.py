#!/usr/bin/env python3
"""Guard original printed CV Lord of Geniture source, source-only admission."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/q).exists() for q in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==6383 and I["batches"][-1]["id"]=="B05c"
assert I["read_numbered_chapters"]==list(range(1,106))
assert I["next"]["chapter"]=="CVI" and I["next"]["pdf_page"]==565
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==32 and len(M)==6 and len(U["issues"])==19
assert W["source_discarded_Firmicus_rule"] and W["source_author_near_equal_planet_mixture"]
for z in W["original_images"]:
 assert H(z["path"])==z["sha256"] and (B/z["path"]).stat().st_size==z["bytes"]
ids=[r["source_local_id"] for r in D];links=[k for s in M for k in s["mapped_local_ids"]]
assert len(links)==len(set(links))==32 and set(links)==set(ids)
records=[{**r,"id":f"R{k}","record_number":k,"global_record_number":k,
 "historical_documentary_accepted":True,
 "independently_verified_lord_geniture_personality":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for k,r in enumerate(D,6384)]
assert [r["record_number"] for r in records]==list(range(6384,6416))
assert all(r["chapter"]=="CVI" for r in records[:-3])
assert all(r["chapter"]=="CVII_NAVIGATION_ONLY" for r in records[-3:])
R={"batch":"B05d","kind":"ORIGINAL_1647_LORD_GENITURE_ALTERNATIVE_METHODS_HISTORICAL_ONLY",
 "status":"HISTORICAL_DOCUMENTARY_ACCEPTED_LOCAL_PENDING_PUBLISH",
 "record_count":32,"first_record":6384,"last_record":6415,
 "substantive_chapter_units":29,"next_chapter_navigation":3,
 "original_pdf_pages":[565,566,567],"source_passages":6,"source_limits":19,
 "original_printed_chapter":"CV","editorial_chapter":"CVI",
 "Firmicus_successor_sign_scheme_rejected":True,
 "alternative_essential_dignity_aggregate_documented":True,
 "Lilly_preferred_essential_plus_accidental_and_elevation":True,
 "nearly_equal_planet_mixture_allowed_without_threshold":True,
 "Greek_Moon_Mercury_method_documented":True,
 "independently_validated_human_personality_outcomes":0,
 "new_empirical_validations":0,"runtime_promotions":0,"rules":records}
put("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B05d",
 "span_count":6,"mapped_source_records":32,
 "source_spans":[{**s,"accepted_global_record_ids":[lookup[k] for k in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B05d","first_record":6384,"last_record":6415,"record_count":32,
 "original_pdf_pages":[565,566,567],"records":[{"record_number":r["record_number"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"],"role":r["role"]} for r in records]})
U["status"]="PERIOD_TEXTUAL_SCORING_AND_HUMAN_VALIDATION_LIMITS_RETAINED"
put("UNRESOLVED.json",U)
roles={}
for r in records:roles[r["role"]]=roles.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B05d","historical_annotations":32,
 "source_passages":6,"source_limits":19,"roles":roles,
 "rejected_Firmicus_sign_successor_procedure":1,
 "positive_essential_dignity_aggregate_competing":1,
 "preferred_essential_accidental_strength_procedure":1,
 "Greek_alternative_Moon_and_Mercury":1,
 "independent_tested_births":0,"independent_personality_predictions":0,
 "empirical_validations":0,"runtime_promotions":0})
A={"batch":"B05d","status":"LOCAL_DOCUMENTARY_ACCEPTED_PENDING_REMOTE",
 "prior_lilly":6383,"new_historical_annotations":32,
 "lilly_if_published":6415,"ptolemy_retained":1066,"combined_if_published":7481,
 "first_record":"R6384","last_record":"R6415",
 "original_full_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[565,566],"following_heading_pdf":566,
 "next_printed_chapter":"CVI","next_editorial_chapter":"CVII",
 "original_source_groups":6,"unresolved_limits":19,
 "runnerup_and_nearequal_planet_allowed":True,
 "no_frozen_numeric_weights_or_thresholds":True,
 "independent_human_personality_validations":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,key in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","audit_sha256")]:A[key]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B05d","local_documentary_annotations":32,
 "lilly_if_published":6415,"combined_if_published":7481,"next":"Complexion CVI PDF566"}))
