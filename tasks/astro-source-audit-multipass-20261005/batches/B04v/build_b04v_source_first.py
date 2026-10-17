from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
g=sum((J(f"SOURCE_GROUPS_PART{i}.json") for i in (1,2,3)),[])
assert len(g)==14
all_n=sum(len(z["claims"]) for z in g)
assert all_n==71,all_n
rows=[];spans=[]
for group in g:
 sid=f"BOOKIII-INTRO-S{len(spans)+1:03}";ids=[]
 for c in group["claims"]:
  role,anchor,meaning,limit=c
  lid=f"BOOKIII-INTRO-C{len(rows)+1:03}";ids.append(lid)
  pages=group["pages"]
  rows.append({"batch":"B04v","source_local_id":lid,"source_span_id":sid,
   "section":"NEXT_RECTIFICATION_CHAPTER_NAVIGATION" if role=="next_navigation" else "BOOK_III_INTRO_AND_TABLES",
   "original_pdf_pages":pages,
   "printed_pages":[p-34 if 523<=p<=534 else None for p in pages],
   "role":role,"short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "full_reference_tables_numeric_cells_transcribed":False,
   "independently_validated_birth_time_rectification":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":group["pages"],
  "passage_label":group["label"],"mapped_local_ids":ids})
assert len(rows)==71 and len(spans)==14
assert all(r["section"]=="BOOK_III_INTRO_AND_TABLES" for r in rows[:-3])
assert all(r["section"]=="NEXT_RECTIFICATION_CHAPTER_NAVIGATION" for r in rows[-3:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in range(521,535):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34 if n>=523 else None,
 "path":p.relative_to(B).as_posix(),"bytes":len(raw),
 "sha256":hashlib.sha256(raw).hexdigest()})
num_tables=[
 {"type":"TIME_TO_EQUATOR_DEGREES","source_pages":[523],"numeric_complete":False,"validated_key_invariants":["1h=15 degrees","1 time minute=15 arcminutes","24h=360 degrees"]},
 {"type":"RIGHT_ASCENSION_12_ZODIAC_SIGNS","source_pages":[526,527],"numeric_complete":False,"spot_checks":["Aries 0 = RA 0","Cancer 1 = RA 91 degrees 5 minutes","Libra 0 = RA 180","Pisces 30 = RA 360"]},
 {"type":"OBLIQUE_ASCENSION_LATITUDE_34","source_pages":[528,529],"latitude_degrees":34,"numeric_complete":False},
 {"type":"OBLIQUE_ASCENSION_LATITUDE_49","source_pages":[530,531],"latitude_degrees":49,"numeric_complete":False},
 {"type":"OBLIQUE_ASCENSION_LATITUDE_53","source_pages":[532,533],"latitude_degrees":53,"numeric_complete":False,
 "source_example_5_scorpio_approximate_OA":"230 degrees 52 minutes"}
]
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{"batch":"B04v","source_groups":g,"source_units":71,"source_spans":14,
 "section":"BOOK_III_INTRO_TITLE_TIME_CONVERSION_ASCENSIONS"})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04v","source_units":71,"status":"HISTORICAL_REFERENCE_SOURCE_FIRST_PROVISIONAL",
 "rows":rows,"original_full_pdf_sha256":sha})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04v","source_spans":spans,"span_count":14,
 "mapped_source_units":71,"original_body_pages":list(range(521,534)),
 "following_heading_pdf":534})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04v","original_full_pdf_sha256":sha,
 "original_images":imgs,"original_body_pdf_pages":list(range(521,534)),
 "next_numbered_chapter_pdf_page":534,"next_printed_chapter":"XCVIII",
 "source_numeric_tables":num_tables,"all_numeric_cells_verified":False,
 "prior_accepted_lilly":5753,"next_global_record":5754,
 "source_printed_numeric_discrepancy":{"base_ra":"142 degrees 20 minutes",
 "printed_operation":"add 90 degrees","printed_result":"230 degrees 20 minutes",
 "computed_correct_result":"232 degrees 20 minutes","difference_arcminutes":120,
 "followup_page_525_uses_printed_value":True},
 "next_book_title_pdf":521,"original_source_page_span":[521,534]})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04v","ids":[r["source_local_id"] for r in rows],
 "next_chapter_navigation_ids":[r["source_local_id"] for r in rows[-3:]]})
print(json.dumps({"batch":"B04v","source_units":71,"source_groups":14,"witness_images":len(imgs),"numeric_tables":len(num_tables),"arithmetic_inconsistency_arcminutes":120}))
