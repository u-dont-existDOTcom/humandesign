from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text())
h=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/x).exists() for x in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json")["rows"]
S=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")["source_spans"]
W=J("SOURCE_WINDOW_MANIFEST.json")
U=J("UNRESOLVED_SOURCE_LIMITS.json")
V=J("WORKED_HOUR_REPLAY_VECTORS_20261017.json")
assert I["records_count"]==5639 and I["batches"][-1]["id"]=="B04t"
assert I["next"]["chapter"]=="XCVIII" and I["next"]["pdf_page"]==516
assert I["read_numbered_chapters"]==list(range(1,98))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert len(D)==114 and len(S)==13 and len(U["issues"])==30
assert len(V["examples"])==3 and not W["previous_table_full_numeric_transcription_complete"]
for x in W["original_images"]:assert h(x["path"])==x["sha256"] and (B/x["path"]).stat().st_size==x["bytes"]
local=[r["source_local_id"] for r in D]; mapped=[x for s in S for x in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==114 and set(local)==set(mapped)
assert all(r["chapter"]=="XCVIII" for r in D[:-5])
assert all(r["chapter"]=="BOOK_III_NAVIGATION_ONLY" for r in D[-5:])
rows=[]
for n,r in enumerate(D,5640):
 rows.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
 "historical_documentary_accepted":True,
 "independently_validated_planetary_hour_effect":False,
 "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rows]==list(range(5640,5754))
R={"batch":"B04u","kind":"FIRST_EDITION_1647_PLANETARY_HOUR_METHOD_AND_BOOK_II_CONCLUSION_HISTORICAL_SOURCE_ONLY",
 "status":"LOCAL_DOCUMENTARY_ACCEPTED_PENDING_GITHUB",
 "record_count":114,"first_record":5640,"last_record":5753,
 "substantive_method_and_conclusion_source_units":109,
 "next_book_iii_navigation_only":5,
 "original_pdf_pages":[516,517,518,519,520,521],
 "source_spans":13,"unresolved_source_limits":30,
 "original_printed_chapter":"XCVII","editorial_chapter":"XCVIII",
 "worked_clock_examples_arithmetically_replayed":3,
 "prior_table_all_numeric_cells_transcribed":False,
 "signed_book_ii_conclusion_date":"11 June 1647",
 "independent_planetary_hour_behavioral_effects":0,
 "new_empirical_predictive_validations":0,"runtime_promotions":0,"rules":rows}
put("RULES.json",R)
lookup={r["source_local_id"]:r["id"] for r in rows}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{"batch":"B04u",
 "source_spans":[{**s,"accepted_global_record_ids":[lookup[k] for k in s["mapped_local_ids"]]} for s in S],
 "span_count":13,"mapped_source_records":114})
put("SOURCE_ORDER.json",{"batch":"B04u","record_count":114,
 "first_record":5640,"last_record":5753,
 "original_pdf_pages":[516,517,518,519,520,521],
 "records":[{"record_number":r["record_number"],"role":r["role"],
 "source_span_id":r["source_span_id"],"original_pdf_pages":r["original_pdf_pages"]} for r in rows]})
U["status"]="ORIGINAL_1647_SOURCE_UNCERTAINTIES_RETAINED"
put("UNRESOLVED.json",U)
rolecounts={}
for r in rows:rolecounts[r["role"]]=rolecounts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04u","historical_source_units":114,
 "substantive_historical_method_conclusion":109,
 "book_iii_navigation":5,"source_groups":13,"source_limits":30,
 "role_counts":rolecounts,"worked_time_examples_replayed":3,
 "source_table_all_numeric_cells_verified":False,
 "independent_person_outcomes":0,"empirical_predictive_validations":0,"runtime_promotions":0})
A={"batch":"B04u","status":"LOCAL_DOCUMENTARY_ADMITTED_PENDING_ARCHIVE_REMOTE",
 "prior_lilly_accepted":5639,"new_documentary_records":114,
 "first_record":"R5640","last_record":"R5753","lilly_if_published":5753,
 "retained_ptolemy":1066,"combined_if_published":6819,
 "original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_chapter_pdf_pages":[516,517,518,519,520],
 "following_book_title_pdf":521,"source_spans":13,"source_unresolved_limits":30,
 "signed_book_ii_conclusion_found":True,
 "new_book_iii_title_found":True,
 "worked_clock_examples_arithmetically_replayed":3,
 "planetary_table_complete_numeric_transcription":False,
 "independent_person_or_clinical_outcomes":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_sha256"),
 ("WORKED_HOUR_REPLAY_VECTORS_20261017.json","clock_vectors_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=h(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04u","accepted_historical_records":114,"lilly_if_published":5753,
 "combined_if_published":6819,"clock_vectors":3,"numeric_table_cells_complete":False}))
