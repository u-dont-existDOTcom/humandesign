from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
assert not any((B/f).exists() for f in ["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json"])
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"];M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5080 and I["batches"][-1]["id"]=="B04f"
assert I["next"]["chapter"]=="LXXXVII" and I["next"]["printed_chapter_numeral"]=="LXXXVI"
assert I["original_printed_chapter_heading_crosswalk"]["duplicate_printed_numeral"]=="LXXXV"
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert len(D)==33 and len(M)==6 and len(U["issues"])==18
assert all(H(x["path"])==x["sha256"] for x in W["original_images"])
assert all(r["original_printed_chapter_numeral"]=="LXXXVI" for r in D[:-2])
assert all(r["original_printed_chapter_numeral"]=="LXXXVII" for r in D[-2:])
mapped=[x for g in M for x in g["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==33
rs=[{**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,"accepted_for_primary_historical_text_reference":True,
 "independently_authenticated_preferment_outcome":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for n,r in enumerate(D,start=5081)]
assert [r["record_number"] for r in rs]==list(range(5081,5114))
R={"batch":"B04g","kind":"1647_PREFERMENT_HORARY_HISTORICAL_ONLY",
 "status":"DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_PUBLICATION",
 "documentary_accepted_locally":True,"record_count":33,
 "first_record":5081,"last_record":5113,"substantive_preferment_units":31,
 "following_chapter_navigation_only":2,"source_passages":6,
 "unresolved_source_limits":18,
 "source_editorial_sequence_chapter":"LXXXVII",
 "source_original_printed_chapter":"LXXXVI",
 "source_original_duplicate_LXXXV_crosswalk_retained":True,
 "independent_appointment_outcomes_verified":0,
 "new_empirical_validations":0,"runtime_promotions":0,
 "rules":rs}
dump("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in rs}
dump("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04g","source_spans":[
 {**g,"accepted_global_record_ids":[lookup[k] for k in g["mapped_local_ids"]]} for g in M],
 "span_count":6,"mapped_source_records":33})
dump("SOURCE_ORDER.json",{"batch":"B04g","first_record":5081,"last_record":5113,"record_count":33,
 "original_pdf_pages":[490,491],
 "records":[{"record_number":r["record_number"],"printed_chapter":r["original_printed_chapter_numeral"],
             "role":r["role"],"pdf_pages":r["original_pdf_pages"]} for r in rs],
 "independent_validations":0})
U["status"]="SOURCE_UNCERTAINTIES_RETAINED";dump("UNRESOLVED.json",U)
A={"batch":"B04g","status":"DOCUMENTARY_LOCALLY_ACCEPTED_PENDING_ARCHIVE_GITHUB",
 "prior_lilly_accepted":5080,"new_documentary_records":33,
 "first_record":"R5081","last_record":"R5113",
 "lilly_if_published":5113,"ptolemy_retained":1066,"combined_if_published":6179,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[490,491],"next_original_pdf":491,
 "next_editorial_chapter":"LXXXVIII","next_original_printed_chapter":"LXXXVII",
 "source_spans":6,"unresolved_source_limits":18,
 "original_printed_chapter":"LXXXVI","editorial_sequential_alias":"LXXXVII",
 "independently_verified_office_outcomes":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261016.md","source_visual_audit_sha256")]:A[k]=H(f)
dump("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04g","records":33,"Lilly_if_published":5113,"total_if_published":6179}))
