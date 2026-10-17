#!/usr/bin/env python3
"""Local documentary admission original Lilly Regiomontanus worked figure only."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
files=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/f).exists() for f in files)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
N=J("SOURCE_NUMERIC_ARITHMETIC_AUDIT_20261017.json")
assert I["records_count"]==6145 and I["batches"][-1]["id"]=="B04y"
assert I["next"]["chapter"]=="CII" and I["next"]["pdf_page"]==553
assert I["read_numbered_chapters"]==list(range(1,102))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==70 and len(M)==6 and len(U["issues"])==24
assert not W["full_astrological_ephemeris_parity"] and not N["independently_authenticated_merchant_birth_time"]
for q in W["original_images"]:
 assert H(q["path"])==q["sha256"] and (B/q["path"]).stat().st_size==q["bytes"]
ids=[r["source_local_id"] for r in D]
mapped=[x for s in M for x in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==70 and set(ids)==set(mapped)
rows=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "full_source_numeric_tables_independently_parity_checked":False,
 "independently_verified_natal_birth_instant":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for n,r in enumerate(D,6146)]
assert [r["record_number"] for r in rows]==list(range(6146,6216))
assert all(r["chapter"]=="CII" for r in rows[:-3])
assert all(r["chapter"]=="CIII_NAVIGATION_ONLY" for r in rows[-3:])
R={"batch":"B04z","kind":"ORIGINAL_1647_REGIOMONTANUS_HOUSE_COMPUTATION_DOCUMENTARY_ONLY",
 "status":"LOCALLY_ACCEPTED_PENDING_REMOTE",
 "record_count":70,"first_record":6146,"last_record":6215,
 "substantive_source_annotations":67,"next_heading_navigation_annotations":3,
 "source_spans":6,"source_limitations":24,"printed_chapter":"CI","editorial_chapter":"CII",
 "original_pdf_pages":list(range(553,559)),
 "input_birth_time_source":"19 Sep 1616 14:24:25 latitude53",
 "source_Midheaven_RA":"222deg10","more_precise_internal_Midheaven_RA":"222deg10min10sec",
 "source_ascendant":"Capricorn6deg37",
 "printed_table_interpolation_implies_ascendant_approx":"Capricorn6deg40",
 "independent_birth_time_or_full_house_parity":False,
 "new_empirical_validations":0,"runtime_promotions":0,"rules":rows}
put("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in rows}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04z",
 "span_count":6,"mapped_source_records":70,
 "source_spans":[{**s,"accepted_global_record_ids":[lookup[k] for k in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B04z","first_record":6146,"last_record":6215,
 "record_count":70,"source_pdf_pages":list(range(553,559)),
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in rows]})
U["status"]="SOURCE_TABLE_ROUNDING_AND_HISTORICAL_UNCERTAINTIES_RETAINED"
put("UNRESOLVED.json",U)
counts={}
for r in rows:counts[r["role"]]=counts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04z","historical_records":70,"source_spans":6,
 "source_unresolved_limits":24,"role_counts":counts,
 "worked_internal_Midheaven_arithmetic_consistent":True,
 "worked_ascendant_interpolation_approx_three_arcminutes_discrepancy":True,
 "independent_human_birth_records":0,
 "empirical_prediction_validations":0,"runtime_promotions":0})
A={"batch":"B04z","status":"LOCAL_DOCUMENTARY_ACCEPTED_PENDING_ZIP_GITHUB",
 "previous_lilly":6145,"added_historical_records":70,
 "first_record":"R6146","last_record":"R6215",
 "lilly_if_published":6215,"ptolemy_retained":1066,"combined_if_published":7281,
 "original_full_pdf_sha256":W["original_full_pdf_sha256"],
 "original_source_pages":list(range(553,559)),
 "next_original_pdf_page":558,"next_printed_chapter":"CII","next_editorial_chapter":"CIII",
 "source_passages":6,"source_unresolved_limits":24,
 "printed_vs_interpolated_ascendant_discrepancy_minutes_approximately":3,
 "more_precise_internal_Midheaven_diff_arcseconds":10,
 "independent_natal_birth_time_verified":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_NUMERIC_ARITHMETIC_AUDIT_20261017.json","arithmetic_audit_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04z","locally_admitted":70,"lilly_if_published":6215,
 "combined_if_published":7281,"original_math_differences_preserved":True,"empirical_validations":0}))
