from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
j=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/q).exists() for q in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=j("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
M=j("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=j("SOURCE_WINDOW_MANIFEST.json")
U=j("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5753 and I["batches"][-1]["id"]=="B04u"
assert I["next"]["chapter"]=="BOOK_III_TITLE_AND_NATIVITY_PROCEDURE" and I["next"]["pdf_page"]==521
assert I["read_numbered_chapters"]==list(range(1,99))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==71 and len(M)==14 and len(U["issues"])==24
assert not W["all_numeric_cells_verified"]
err=W["source_printed_numeric_discrepancy"]
assert err["difference_arcminutes"]==120
assert err["printed_result"]=="230 degrees 20 minutes" and err["computed_correct_result"]=="232 degrees 20 minutes"
for x in W["original_images"]:
 assert h(x["path"])==x["sha256"] and (B/x["path"]).stat().st_size==x["bytes"]
ids=[r["source_local_id"] for r in D]
mapped=[x for s in M for x in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==71 and set(ids)==set(mapped)
records=[{**r,"id":f"R{k}","record_number":k,"global_record_number":k,
 "historical_documentary_accepted":True,
 "full_reference_tables_numeric_cells_transcribed":False,
 "independently_validated_birth_time_rectification":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False}
 for k,r in enumerate(D,5754)]
assert [r["record_number"] for r in records]==list(range(5754,5825))
assert all(r["section"]=="BOOK_III_INTRO_AND_TABLES" for r in records[:-3])
assert all(r["section"]=="NEXT_RECTIFICATION_CHAPTER_NAVIGATION" for r in records[-3:])
R={"batch":"B04v","kind":"ORIGINAL_1647_BOOK_III_INTRO_AND_ASCENSION_TABLE_IMAGES_SOURCE_ONLY",
 "status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_PUBLICATION",
 "record_count":71,"first_record":5754,"last_record":5824,
 "substantive_intro_and_numeric_table_image_records":68,
 "next_chapter_navigation":3,"source_passages":14,"source_limits":24,
 "original_pdf_pages":list(range(521,535)),
 "table_page_groups":5,"complete_numeric_table_cell_transcription":False,
 "worked_source_corrected_arithmetic_produces_232deg20min":True,
 "original_printed_worked_arithmetic_230deg20min":True,
 "two_degree_source_inconsistency_preserved":True,
 "first_printed_book3_chapter_next":"XCVIII",
 "new_independently_verified_birth_time_predictions":0,
 "empirical_validations":0,"runtime_promotions":0,"rules":records}
put("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in records}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04v","source_spans":[{**s,"accepted_global_record_ids":[idmap[x] for x in s["mapped_local_ids"]]} for s in M],
 "span_count":14,"mapped_source_records":71})
put("SOURCE_ORDER.json",{"batch":"B04v","first_record":5754,"last_record":5824,
 "record_count":71,"original_source_pdf_pages":list(range(521,535)),
 "records":[{"record_number":r["record_number"],"kind":r["role"],"pdf_pages":r["original_pdf_pages"],"source_span":r["source_span_id"]} for r in records]})
U["status"]="ORIGINAL_NUMERIC_AND_SOURCE_LIMITATIONS_RETAINED_AT_ADMISSION"
put("UNRESOLVED.json",U)
counts={}
for r in records:counts[r["role"]]=counts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04v","documentary_annotations":71,
 "source_passages":14,"unresolved_evidence_limits":24,
 "role_counts":counts,"original_full_scans":14,
 "dense_numeric_table_leaves":9,"numeric_cells_exhaustively_transcribed":False,
 "source_worked_arithmetic_inconsistency_degrees":2,
 "independent_birth_time_rectification_outcomes":0,
 "empirical_prediction_validations":0,"runtime_promotions":0})
A={"batch":"B04v","status":"LOCALLY_ACCEPTED_DOCUMENTARY_PENDING_ARCHIVE_REMOTE",
 "prior_lilly":5753,"new_documentary_records":71,
 "lilly_if_published":5824,"ptolemy_retained":1066,"combined_if_published":6890,
 "first_record":"R5754","last_record":"R5824",
 "original_source_pdf_sha256":W["original_full_pdf_sha256"],
 "original_pdf_pages":list(range(521,535)),"next_printed_chapter":"XCVIII",
 "next_editorial_chapter":"XCIX","next_original_pdf_page":534,
 "original_title_p521_unnumbered":True,
 "full_numeric_table_transcription_complete":False,
 "original_arithmetic_discrepancy_arcminutes":120,
 "original_printed_ascendant_lookup":"230deg20min",
 "mathematically_correct_summation":"232deg20min",
 "source_spans":14,"source_uncertainties":24,
 "independent_rectified_birth_times_verified":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
("UNRESOLVED.json","unresolved_sha256"),
("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:A[k]=h(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04v","documentary_locally_accepted":71,"lilly_if_published":5824,"combined_if_published":6890,"numeric_inconsistency_deg":2,"next":"CHAP XCVIII rectification"}))
