from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
j=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
out=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/x).exists() for x in out)
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=j("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=j("SOURCE_WINDOW_MANIFEST.json");U=j("UNRESOLVED_SOURCE_LIMITS.json")
assert idx["records_count"]==5824 and idx["batches"][-1]["id"]=="B04v"
assert idx["next"]["chapter"]=="XCIX" and idx["next"]["pdf_page"]==534
assert idx["read_numbered_chapters"]==list(range(1,99))
assert idx["source_sha256"]==W["original_full_pdf_sha256"]
assert idx["empirical_validations"]==idx["runtime_promotions"]==0
assert len(D)==99 and len(M)==13 and len(U["issues"])==27
assert W["trutine_sign_help_reported_exact_degree_rare"] and W["source_says_hour_of_conception_alternative_not_credited"]
assert not W["full_gestation_table_numeric_transcribed"]
for z in W["original_images"]:
 assert h(z["path"])==z["sha256"] and (B/z["path"]).stat().st_size==z["bytes"]
local=[r["source_local_id"] for r in D];links=[x for s in M for x in s["mapped_local_ids"]]
assert len(links)==len(set(links))==99 and set(links)==set(local)
rows=[]
for n,r in enumerate(D,5825):
 rows.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "source_numeric_table_fully_transcribed":False,
 "independently_verified_conception_event":False,
 "independently_verified_natal_birth_time":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rows]==list(range(5825,5924))
assert all(r["section"]=="TRUTINE_AND_OTHER_RECTIFICATION_METHODS" for r in rows[:-3])
assert all(r["section"]=="NEXT_ANIMODAR_NAV_ONLY" for r in rows[-3:])
R={"batch":"B04w","kind":"ORIGINAL_1647_TRUTINE_HERMES_CONCEPTION_AND_BIRTH_RECTIFICATION_SOURCE_ONLY",
 "status":"LOCALLY_ACCEPTED_DOCUMENTARY_PENDING_GITHUB",
 "record_count":99,"first_record":5825,"last_record":5923,
 "original_printed_chapter":"XCVIII","editorial_chapter":"XCIX",
 "substantive_chapter_annotations":96,"following_Animodar_navigation":3,
 "original_pdf_pages":[534,535,536,537,538,539],
 "source_passages":13,"unresolved_limitations":27,
 "gestation_table_full_numeric_transcription":False,
 "source_Trutine_sometimes_finds_sign_not_exact_degree":True,
 "source_author_prefers_accident_directed_rectification":True,
 "alternative_hour_of_conception_formula_author_rejects":True,
 "merchant_conception_day_derived_by_calendar":True,
 "merchant_actual_conception_independently_verified":False,
 "independent_birth_time_rectification_successes":0,
 "empirically_validated_predictions":0,"runtime_promotions":0,"rules":rows}
put("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in rows}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04w",
 "span_count":13,"mapped_source_records":99,
 "source_spans":[{**s,"accepted_global_record_ids":[lookup[k] for k in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B04w","first_record":5825,"last_record":5923,
 "record_count":99,"original_pdf_pages":list(range(534,540)),
 "records":[{"record_number":r["record_number"],"role":r["role"],"source_span":r["source_span_id"],
 "source_pdf_pages":r["original_pdf_pages"]} for r in rows]})
U["status"]="TEXTUAL_CALENDAR_EPHEMERIS_AND_VALIDATION_LIMITS_RETAINED"
put("UNRESOLVED.json",U)
counts={}
for r in rows:counts[r["role"]]=counts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04w","historical_source_records":99,
 "passages":13,"retained_uncertainties":27,"roles":counts,
 "coarse_rising_sign_usefulness_author_only":1,
 "exact_degree_failure_author_admitted":1,
 "merchant_deemed_rectified_by_accidents_author_only":1,
 "actual_conception_records":0,"independent_time_twins":0,
 "new_empirical_predictions":0,"runtime_promotions":0})
A={"batch":"B04w","status":"LOCALLY_ACCEPTED_SOURCE_ONLY_PENDING_ARCHIVE_REMOTE",
 "prior_lilly":5824,"new_documentary_records":99,
 "first_record":"R5825","last_record":"R5923",
 "lilly_if_published":5923,"ptolemy_retained":1066,"combined_if_published":6989,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":list(range(534,540)),
 "next_original_pdf":539,"next_editorial_chapter":"C","next_printed_chapter":"XCIX",
 "source_passages":13,"source_unresolved_limits":27,
 "Trutine_rising_sign_only_qualification":True,
 "Trutine_exact_degree_failure_admitted":True,
 "source_life_events_method_preferred":True,
 "source_conception_hour_method_not_credited":True,
 "merchant_1616_calendar_arithmetic_internally_verified":True,
 "independent_birth_time_successes":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
("UNRESOLVED.json","unresolved_sha256"),
("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:A[k]=h(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04w","local_source_records":99,"lilly_if_published":5923,
 "combined_if_published":6989,"numeric_gestation_table_complete":False,"birth_time_validation":0}))
