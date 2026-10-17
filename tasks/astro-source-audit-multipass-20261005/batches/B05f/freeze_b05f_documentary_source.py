#!/usr/bin/env python3
"""First edition manners source local documentary admission, no human-character inference."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
out=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/p).exists() for p in out)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==6474 and I["batches"][-1]["id"]=="B05e"
assert I["next"]["chapter"]=="CVIII" and I["next"]["pdf_page"]==568
assert I["read_numbered_chapters"]==list(range(1,108))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==86 and len(M)==14 and len(U["issues"])==30
assert W["Johannes_Angelus_fine_degree_scheme_author_rejected"]
assert W["specific_fixed_star_violent_accusations_historical_only"]
assert W["independently_validated_human_personality_matches"]==0
for z in W["original_images"]:
 assert H(z["path"])==z["sha256"] and (B/z["path"]).stat().st_size==z["bytes"]
local=[r["source_local_id"] for r in D]
flat=[x for s in M for x in s["mapped_local_ids"]]
assert len(flat)==len(set(flat))==86 and set(local)==set(flat)
rows=[{**r,"id":f"R{k}","record_number":k,"global_record_number":k,
 "historical_documentary_accepted":True,
 "independently_validated_human_personality":False,
 "independently_validated_criminal_or_medical_prognosis":False,
 "empirically_validated_prediction":False,
 "runtime_model_promoted":False} for k,r in enumerate(D,6475)]
assert [r["record_number"] for r in rows]==list(range(6475,6561))
assert all(r["chapter"]=="CVIII" for r in rows[:-3])
assert all(r["chapter"]=="CIX_NAVIGATION_ONLY" for r in rows[-3:])
R={"batch":"B05f","kind":"ORIGINAL_1647_MANNERS_FALLBACKS_SIGNS_FIXED_STARS_SOURCE_ONLY",
 "status":"LOCALLY_ACCEPTED_HISTORICAL_DOCUMENTARY_PENDING_REMOTE",
 "record_count":86,"first_record":6475,"last_record":6560,
 "substantive_original_claims":83,"next_chapter_navigation":3,
 "original_body_pdf_pages":[568,569,570,571,572,573],
 "following_context_pdf_pages":[574,575],
 "source_passages":14,"source_limits":30,
 "printed_chapter":"CVII","editorial_chapter":"CVIII",
 "multiple_Mercury_Moon_Ascendant_significator_fallbacks":True,
 "Moon_direction_dynamical_manners_claim":True,
 "historical_fixed_star_criminal_accusations_unverified":True,
 "source_rejects_degree_strictness_of_Angelus":True,
 "twelve_sign_stereotypes_not_validated":True,
 "independent_human_personality_classification_successes":0,
 "new_empirical_validations":0,"runtime_promotions":0,"rules":rows}
put("RULES.json",R)
mapped={r["source_local_id"]:r["id"] for r in rows}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B05f","span_count":14,
 "mapped_source_records":86,
 "source_spans":[{**s,"accepted_global_record_ids":[mapped[k] for k in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B05f","first_record":6475,"last_record":6560,
 "record_count":86,"source_pdf_pages":list(range(568,576)),
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in rows]})
U["status"]="HISTORICAL_FIXED_STAR_SIGN_PERSONALITY_STEREOTYPES_NOT_HUMAN_VALIDATED"
put("UNRESOLVED.json",U)
roles={}
for r in rows:roles[r["role"]]=roles.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B05f","source_historical_records":86,
 "source_passages":14,"source_limits":30,"role_counts":roles,
 "ancient_degree_specific_Angelus_rejected":True,
 "twelve_sign_personality_stereotypes":12,"four_humour_manners_classes":4,
 "conditional_fixed_star_claims_historical_not_forensic":True,
 "independent_human_personality_outcomes":0,
 "empirically_validated_predictions":0,"runtime_promotions":0})
A={"batch":"B05f","status":"LOCAL_SOURCE_ONLY_ADMITTED_PENDING_ARCHIVE_GITHUB",
 "prior_lilly":6474,"new_documentary_records":86,
 "first_record":"R6475","last_record":"R6560",
 "lilly_if_published":6560,"ptolemy_retained":1066,"combined_if_published":7626,
 "original_full_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[568,569,570,571,572,573],
 "following_heading_pdf":573,
 "next_printed_chapter":"CVIII","next_editorial_chapter":"CIX",
 "source_passages":14,"source_unresolved_limits":30,
 "no_independently_verified_mental_or_forensic_traits":True,
 "source_rejected_fine_degree_personality_scheme":True,
 "actual_blinded_human_personality_matches":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
("UNRESOLVED.json","unresolved_sha256"),
("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B05f","local_records":86,"lilly_if_published":6560,"combined_if_published":7626,"blinded_personality_validation":0}))
