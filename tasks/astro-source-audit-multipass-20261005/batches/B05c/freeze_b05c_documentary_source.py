#!/usr/bin/env python3
"""Admit first-edition Hyleg/Anareta/Alcochodon documentary clauses without mortality prediction credit."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
out=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/x).exists() for x in out)
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=json.loads(IDX.read_text(encoding="utf-8"))
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==6309 and I["batches"][-1]["id"]=="B05b"
assert I["next"]["chapter"]=="CV" and I["next"]["pdf_page"]==561
assert I["read_numbered_chapters"]==list(range(1,105))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==74 and len(M)==7 and len(U["issues"])==30
assert W["source_hyleg_anareta_alcochodon_uncertainty_admitted"]
assert W["source_25_degree_ascendant_exception"]
assert not W["source_Alcochodon_numeric_year_values_independently_verified"]
for w in W["original_images"]:
 assert H(w["path"])==w["sha256"] and (B/w["path"]).stat().st_size==w["bytes"]
locals=[r["source_local_id"] for r in D]
mapped=[y for s in M for y in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==74 and set(locals)==set(mapped)
records=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "independently_authenticated_death_or_survival":False,
 "medical_longevity_prediction_validated":False,
 "empirically_validated_prediction":False,
 "runtime_model_promoted":False}
 for n,r in enumerate(D,6310)]
assert [r["record_number"] for r in records]==list(range(6310,6384))
assert all(r["chapter"]=="CV" for r in records[:-3])
assert all(r["chapter"]=="CVI_NAVIGATION_ONLY" for r in records[-3:])
R={"batch":"B05c","kind":"FIRST_EDITION_1647_HYLEG_ANARETA_ALCOCHODON_UNVERIFIED_HISTORICAL_SOURCE",
 "status":"LOCAL_DOCUMENTARY_ACCEPTED_NOT_HUMAN_VALIDATION",
 "record_count":74,"first_record":6310,"last_record":6383,
 "original_printed_chapter":"CIV","editorial_chapter":"CV",
 "substantive_historical_source_annotations":71,
 "following_lord_geniture_navigation":3,
 "original_pdf_pages":list(range(561,567)),
 "source_passages":7,"source_uncertainties":30,
 "source_hyleg_eligibility_ascendant_exception_25deg":True,
 "source_eighth_anareta_before_after_cusp_deg":[5,25],
 "multiple_life_significator_candidates_and_tie_branches":True,
 "author_explicitly_uncertain_Hyleg_Anareta_Alcochodon":True,
 "author_rejects_one_conjunction_based_anareta_candidate":True,
 "independent_death_or_survival_outcomes":0,
 "new_empirical_validations":0,"runtime_promotions":0,"rules":records}
put("RULES.json",R)
by={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B05c","span_count":7,"mapped_source_records":74,
 "source_spans":[{**s,"accepted_global_record_ids":[by[k] for k in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B05c","first_record":6310,
 "last_record":6383,"record_count":74,
 "original_pdf_pages":list(range(561,567)),
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in records]})
U["status"]="ORIGINAL_MORTALITY_MODEL_AND_NUMERIC_LIMITS_RETAINED"
put("UNRESOLVED.json",U)
counts={}
for r in records:counts[r["role"]]=counts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B05c","source_annotations":74,
 "original_page_passages":7,"unresolved_source_limits":30,
 "role_counts":counts,"author_uncertainty_about_three_technical_models":True,
 "initial_death_or_survival_independent_outcomes":0,
 "predictive_validations":0,"runtime_promotions":0})
A={"batch":"B05c","status":"LOCAL_DOCUMENTARY_ACCEPTED_PENDING_ARCHIVE_GITHUB",
 "prior_lilly":6309,"added_documentary_records":74,
 "first_record":"R6310","last_record":"R6383",
 "lilly_if_published":6383,"retained_ptolemy":1066,
 "combined_if_published":7449,
 "original_source_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[561,562,563,564,565],
 "following_heading_pdf_page":565,
 "following_printed_chapter":"CV","following_editorial_chapter":"CVI",
 "source_passages":7,"source_limits":30,
 "original_author_skepticism_explicit":True,
 "original_Alcochodon_years_independent_accuracy":False,
 "independently_verified_death_survival":0,
 "new_empirical_validations":0,"runtime_promotions":0,
 "remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B05c","historical_admitted":74,"lilly_if_published":6383,
 "combined_if_published":7449,"author_skepticism_retained":True,
 "independent_human_outcomes":0}))
