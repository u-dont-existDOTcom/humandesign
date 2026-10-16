from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
outs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
      "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
assert not any((B/n).exists() for n in outs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json");C=J("CLAIM_LEDGER.json")
assert I["records_count"]==5026 and I["batches"][-1]["id"]=="B04e"
assert I["next"]["chapter"]=="LXXXVI" and I["next"]["pdf_page"]==489
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert len(D)==54 and len(M)==10 and len(U["issues"])==24
assert C["independently_verified_royal_military_outcomes"]==C["new_empirical_validations"]==C["runtime_promotions"]==0
assert all(H(x["path"])==x["sha256"] for x in W["original_images"])
ids=[r["source_local_id"] for r in D]
mapped=[k for g in M for k in g["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==54 and sorted(ids)==sorted(mapped)
rs=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
    "historical_documentary_accepted":True,
    "accepted_for_primary_historical_text_reference":True,
    "independently_authenticated_royal_military_outcome":False,
    "empirically_validated_prediction":False,"runtime_model_promoted":False}
    for n,r in enumerate(D,start=5027)]
assert [r["record_number"] for r in rs]==list(range(5027,5081))
R={"batch":"B04f","kind":"ORIGINAL_1647_KING_IRISH_FORCES_QUEEN_HISTORICAL_ONLY",
 "status":"LOCALLY_ACCEPTED_DOCUMENTARY_PENDING_GITHUB",
 "documentary_accepted_locally":True,"record_count":54,
 "first_record":5027,"last_record":5080,
 "substantive_lxxxvi_records":52,"next_chapter_navigation_only":2,
 "source_reverse_passages":10,"unresolved_source_issues":24,
 "original_pdf_pages":[489,490],"source_figure_absolute_date_not_printed":True,
 "author_historical_meeting_date_reported":"about 14 July 1643",
 "author_reported_partial_Queen_forces_loss":True,
 "independently_verified_royal_military_outcomes":0,
 "new_empirical_predictive_validations":0,"runtime_promotions":0,"rules":rs}
put("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in rs}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04f",
 "span_count":10,"source_spans":[{**g,"accepted_global_record_ids":[lookup[k] for k in g["mapped_local_ids"]]}
 for g in M],"mapped_source_records":54})
put("SOURCE_ORDER.json",{"batch":"B04f","first_record":5027,"last_record":5080,
 "record_count":54,"original_pdf_pages":[489,490],
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "pdf_pages":r["original_pdf_pages"]} for r in rs],
 "new_empirical_validations":0})
U["status"]="ORIGINAL_SOURCE_LIMITS_RETAINED_AT_DOCUMENTARY_ADMISSION"
put("UNRESOLVED.json",U)
A={"batch":"B04f","status":"DOCUMENTARY_LOCALLY_ADMITTED_PENDING_ARCHIVE_GITHUB",
 "documentary_accepted_locally":True,"prior_lilly_accepted":5026,
 "new_documentary_records":54,"first_record":"R5027","last_record":"R5080",
 "lilly_if_published":5080,"ptolemy_retained":1066,"combined_if_published":6146,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[489,490],"following_heading_pdf":490,
 "source_reverse_passages":10,"unresolved_source_issues":24,
 "next_chapter":"LXXXVII","next_original_pdf":490,
 "figure_absolute_date_unresolved":True,
 "Queen_army_destroyed_claim_unverified_partial_miss":True,
 "independently_verified_royal_military_outcomes":0,
 "new_empirically_validated_predictions":0,"runtime_model_promotions":0,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04f","new_records":54,
 "lilly_if_published":5080,"combined_if_published":6146}))
