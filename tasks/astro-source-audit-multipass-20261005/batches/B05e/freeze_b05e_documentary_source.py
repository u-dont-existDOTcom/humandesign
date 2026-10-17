#!/usr/bin/env python3
"""Locally admit original classical complexion source, explicitly not biomedical."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
assert not any((B/f).exists() for f in ("RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"))
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==6415 and I["batches"][-1]["id"]=="B05d"
assert I["next"]["chapter"]=="CVII" and I["next"]["pdf_page"]==566
assert I["read_numbered_chapters"]==list(range(1,107))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==59 and len(M)==9 and len(U["issues"])==23
for q in W["original_images"]:assert H(q["path"])==q["sha256"] and (B/q["path"]).stat().st_size==q["bytes"]
local=[r["source_local_id"] for r in D];ids=[x for s in M for x in s["mapped_local_ids"]]
assert len(ids)==len(set(ids))==59 and set(ids)==set(local)
rows=[{**r,"id":f"R{k}","record_number":k,"global_record_number":k,
 "historical_documentary_accepted":True,
 "independently_validated_temperament_or_health":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for k,r in enumerate(D,6416)]
assert [r["record_number"] for r in rows]==list(range(6416,6475))
assert all(r["chapter"]=="CVII" for r in rows[:-3])
assert all(r["chapter"]=="CVIII_NAVIGATION_ONLY" for r in rows[-3:])
R={"batch":"B05e","kind":"FIRST_EDITION_HISTORIC_FOUR_HUMOURS_COMPLICATION_AND_WEIGHTING_ONLY",
 "status":"HISTORICAL_DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_PUBLISH",
 "record_count":59,"first_record":6416,"last_record":6474,
 "source_body_records":56,"following_manners_navigation":3,
 "source_spans":9,"source_unresolved_limits":23,
 "original_source_pdf_pages":[566,567,568,569],
 "original_printed_chapter":"CVI","editorial_chapter":"CVII",
 "four_historical_quality_pairs_preserved":True,
 "adverse_Saturn_Mars_qualifier":True,
 "opposing_equal_testimonies_cancel":True,
 "triple_LordGeniture_Asc_ruler_conditional_weight":True,
 "double_Moon_in_Asc_weight":True,
 "historical_humour_not_clinical_diagnosis":True,
 "independent_human_personality_or_medical_validation":0,
 "new_empirical_validations":0,"runtime_promotions":0,
 "rules":rows}
put("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in rows}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B05e",
 "span_count":9,"mapped_source_records":59,
 "source_spans":[{**s,"accepted_global_record_ids":[lookup[x] for x in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B05e","first_record":6416,"last_record":6474,
 "record_count":59,"original_pdf_pages":[566,567,568,569],
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in rows]})
U["status"]="HISTORIC_MEDICAL_PSYCHOMETRIC_AND_SOURCE_UNCERTAINTY_RETAINED"
put("UNRESOLVED.json",U)
roles={}
for r in rows:roles[r["role"]]=roles.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B05e","historical_source_records":59,
 "original_passages":9,"unresolved_limits":23,"role_counts":roles,
 "four_humours_source_categories":4,
 "planet_oriental_occidental_conditions":10,
 "lunar_quarter_conditions":4,
 "sign_triplicity_conditions":4,
 "opposed_quality_cancellation":True,
 "conditional_triple_double_weights":True,
 "independent_personality_outcomes":0,"new_empirical_validations":0,"runtime_promotions":0})
A={"batch":"B05e","status":"LOCAL_SOURCE_ADMITTED_PENDING_GITHUB",
 "prior_lilly_accepted":6415,"new_documentary_records":59,
 "first_record":"R6416","last_record":"R6474",
 "lilly_if_published":6474,"retained_ptolemy":1066,"combined_if_published":7540,
 "original_full_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[566,567,568],"following_heading_pdf":568,
 "next_printed_chapter":"CVII","next_editorial_chapter":"CVIII",
 "source_passages":9,"source_uncertainties":23,
 "equal_opposed_hot_cold_testimony_cancellation":True,
 "conditional_triple_lord_geniture_ascendant":True,
 "conditional_double_moon_ascendant":True,
 "out_of_sample_human_temperament_matches":0,
 "empirical_predictions_validated":0,"runtime_promotions":0,"remote_published":False}
for f,k in (("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")):
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B05e","source_added":59,"lilly_if_published":6474,"combined_if_published":7540,"human_validations":0}))
