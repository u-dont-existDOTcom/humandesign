from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
groups=sum((J(f"SOURCE_GROUPS_PART{i}.json") for i in (1,2,3)),[])
assert len(groups)==13 and sum(len(g["claims"]) for g in groups)==114
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{
 "batch":"B04u","printed_chapter":"XCVII","editorial_chapter":"XCVIII",
 "source_spans":13,"source_units":114,"source_groups":groups})
rows=[];spans=[]
for g in groups:
 sid=f"XCVIII-S{len(spans)+1:03}";ids=[]
 for claim in g["claims"]:
  assert len(claim) in (4,5)
  role,anchor,meaning,qual=claim[:4]
  pages=claim[4] if len(claim)==5 else g["pages"]
  assert set(pages).issubset(set(g["pages"]))
  lid=f"XCVIII-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B04u","source_local_id":lid,"source_span_id":sid,
   "chapter":"BOOK_III_NAVIGATION_ONLY" if role=="next_book_navigation" else "XCVIII",
   "printed_chapter":"XCVII","role":role,"original_pdf_pages":pages,
   "printed_pages":[p-34 if p!=521 else None for p in pages],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,
   "original_source_qualifications":qual,"global_record_number":None,
   "historical_documentary_accepted":False,
   "independently_validated_planetary_hour_effect":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],"passage_label":g["label"],
   "mapped_local_ids":ids})
assert len(rows)==114 and len(spans)==13
assert all(r["chapter"]=="XCVIII" for r in rows[:-5])
assert all(r["chapter"]=="BOOK_III_NAVIGATION_ONLY" for r in rows[-5:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in range(516,522):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34 if n<=520 else None,
  "path":p.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04u","status":"ORIGINAL_SOURCE_PROVISIONAL",
 "source_units":114,"original_full_pdf_sha256":sha,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04u","source_spans":spans,"span_count":13,
 "mapped_source_units":114,"original_numbered_body_pages":[516,517,518,519,520],
 "next_book_title_pdf":521,"independent_full_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04u","ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "book3_navigation_only":[r["source_local_id"] for r in rows[-5:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04u","original_full_pdf_sha256":sha,
 "original_images":imgs,"original_body_pdf_pages":list(range(516,521)),
 "following_book_title_pdf":521,"source_final_printed_chapter":"XCVII",
 "editorial_chapter":"XCVIII","prior_accepted_lilly":5639,
 "next_global_record":5640,"signed_book_ii_conclusion":"June 11, 1647, William Lilly",
 "book_iii_begins_at_pdf":521,
 "previous_table_full_numeric_transcription_complete":False,
 "worked_examples_calculable_but_nonempirical":True})
print(json.dumps({"batch":"B04u","source_annotations":114,
 "substantive":109,"book3_nav":5,"spans":13,
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1]}))
