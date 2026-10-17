#!/usr/bin/env python3
"""Source-first Lilly 1647 Henley horse worked horary, outcome vs timing preserved."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert G["source_spans"]==len(G["source_groups"])==7
assert G["source_units"]==sum(len(s["claims"]) for s in G["source_groups"])==44
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"XCIV-S{len(spans)+1:03}";ids=[]
 for c in g["claims"]:
  assert len(c) in (4,5)
  role,anchor,paraphrase,limit=c[:4]
  assert all(isinstance(x,str) and x.strip() for x in c[:4])
  pages=c[4] if len(c)==5 else g["pages"]
  assert set(pages).issubset(set(g["pages"]))
  lid=f"XCIV-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B04n","source_local_id":lid,"source_span_id":sid,
   "role":role,"chapter":"XCV_NAVIGATION_ONLY" if role=="next_navigation" else "XCIV",
   "printed_chapter":"XCIII","original_pdf_pages":pages,
   "printed_pages":[p-34 for p in pages],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":paraphrase,
   "original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_horse_recovery":False,
   "independently_authenticated_theft_or_riders":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
  "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==44 and len(spans)==7
assert all(r["chapter"]=="XCIV" for r in rows[:-2])
assert all(r["chapter"]=="XCV_NAVIGATION_ONLY" for r in rows[-2:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in (501,502):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
  "path":p.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04n",
 "original_full_pdf_sha256":sha,"source_units":44,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04n",
 "source_spans":spans,"span_count":7,"mapped_source_units":44,
 "original_body_pdf_pages":[501,502],"next_heading_pdf":502,
 "independent_diplomatic_second_transcription":False})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04n",
 "original_full_pdf_sha256":sha,"original_images":imgs,
 "original_body_pdf_pages":[501,502],"following_heading_pdf":502,
 "printed_chapter":"XCIII","editorial_chapter":"XCIV",
 "next_printed_chapter":"XCIV","next_editorial_chapter":"XCV",
 "previous_accepted_lilly":5413,"next_global_record":5414,
 "printed_question_date":"11 January 1646","printed_question_local_clock":"2:59 PM",
 "author_reported_three_days":True,"author_original_one_two_day_forecast":True,
 "reported_exact_return_day_ambiguous":True,
 "independent_horse_outcome_verified":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04n",
 "ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "next_heading_navigation_only":[r["source_local_id"] for r in rows[-2:]]})
print(json.dumps({"batch":"B04n","draft_annotations":44,
 "source_passages":7,"next":"XCV printed XCIV PDF502"}))
