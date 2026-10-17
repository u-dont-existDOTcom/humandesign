from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
assert not (B/"RULES.json").exists()
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");E=J("EXTERNAL_HISTORICAL_EVENT_LEDGER_20261017.json")
assert I["records_count"]==5586 and I["batches"][-1]["id"]=="B04q"
assert I["next"]["chapter"]=="POST_XCVI_UNNUMBERED_ESSEX_AND_TABLES"
assert len(D)==43 and len(M)==7 and len(J("UNRESOLVED_SOURCE_LIMITS.json")["issues"])==20
assert I["source_sha256"]==W["original_full_pdf_sha256"]
for x in W["original_images"]:assert h(x["path"])==x["sha256"]
assert not E["external_authority"]["author_pre_event_astrology_prediction_independently_authenticated"]
records=[]
for n,r in enumerate(D,start=5587):
 records.append({**r,"id":f"R{n}","record_number":n,
 "global_record_number":n,"historical_documentary_accepted":True,
 "independently_authenticated_original_prediction":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in records]==list(range(5587,5630))
assert all(r["section"]=="UNNUMBERED_ESSEX" for r in records[:-2])
assert all(r["section"]=="PLANETARY_HOUR_TABLE_NAV_ONLY" for r in records[-2:])
rules={"batch":"B04s","status":"ORIGINAL_UNNUMBERED_DOCUMENTARY_ACCEPTED_LOCAL",
 "record_count":43,"first_record":5587,"last_record":5629,
 "substantive_essex_source_units":41,"next_table_navigation_units":2,
 "original_pdf_pages":[507,508],"source_passages":7,"source_limits":20,
 "historical_military_event_external_corroboration":True,
 "literal_personal_essex_surrender_refuted_by_historiography":True,
 "independent_prior_prediction_confirmations":0,
 "new_empirical_validations":0,"runtime_promotions":0,"rules":records}
put("RULES.json",rules)
idmap={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04s",
 "span_count":7,"mapped_source_records":43,
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]} for s in M]})
put("SOURCE_ORDER.json",{"batch":"B04s","record_count":43,"ids":[r["id"] for r in records],
 "next_table_pdf":508})
U=J("UNRESOLVED_SOURCE_LIMITS.json");put("UNRESOLVED.json",U)
A={"batch":"B04s","prior_lilly":5586,"new_documentary_records":43,
 "lilly_if_published":5629,"ptolemy_retained":1066,"combined_if_published":6695,
 "source_sha256":W["original_full_pdf_sha256"],"body_original_pdf_page":507,
 "next_source_unit":"PLANETARY_HOUR_TABLE","next_original_pdf_page":508,
 "source_passages":7,"unresolved_limits":20,
 "historical_army_arms_surrender_independently_corroborated":True,
 "historical_essex_personally_surrendered":False,
 "independently_verified_original_astrology_forecast":False,
 "new_empirical_validations":0,"runtime_promotions":0}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_INDEPENDENT_EVENT_AUDIT_20261017.md","audit_sha256"),
("EXTERNAL_HISTORICAL_EVENT_LEDGER_20261017.json","external_evidence_sha256")]:A[k]=h(f)
put("ACCEPTANCE.json",A)
print(json.dumps(A))
