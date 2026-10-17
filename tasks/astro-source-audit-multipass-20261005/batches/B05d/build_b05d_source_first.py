#!/usr/bin/env python3
"""Source-first first-edition Lord of Geniture, no empirical claims."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
g=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert g["source_spans"]==len(g["source_groups"])==6
assert g["source_units"]==sum(len(x["claims"]) for x in g["source_groups"])==32
rows=[];spans=[]
for q in g["source_groups"]:
 sid=f"GENITURE-S{len(spans)+1:03}";ids=[]
 for i,c in enumerate(q["claims"]):
  assert len(c)==4 and all(isinstance(t,str) and t.strip() for t in c)
  role,anchor,summary,limit=c
  pages=q["pages"]
  if pages==[565,566]:
   pages=[565,566] if i==0 else [566]
  elif pages==[566,567]:
   pages=[566] if i<2 else [567]
  assert set(pages).issubset(set(q["pages"]))
  lid=f"GENITURE-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B05d","source_local_id":lid,"source_span_id":sid,
    "chapter":"CVII_NAVIGATION_ONLY" if role=="next_navigation" else "CVI",
    "printed_chapter":"CV","role":role,"original_pdf_pages":pages,
    "printed_pages":[p-34 for p in pages],
    "short_original_anchor_not_diplomatic":anchor,
    "historical_author_paraphrase":summary,
    "original_source_qualifications":limit,
    "global_record_number":None,"historical_documentary_accepted":False,
    "independently_verified_lord_geniture_personality":False,
    "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":q["pages"],"passage_label":q["label"],"mapped_local_ids":ids})
assert len(rows)==32 and len(spans)==6
assert all(x["chapter"]=="CVI" for x in rows[:-3])
assert all(x["chapter"]=="CVII_NAVIGATION_ONLY" for x in rows[-3:])
hash_source="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in range(565,568):
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,"path":f.relative_to(B).as_posix(),
    "bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B05d","status":"FIRST_EDITION_SOURCE_FIRST_LOCAL_UNADMITTED","source_units":32,
    "original_full_pdf_sha256":hash_source,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B05d","source_spans":spans,
    "span_count":6,"mapped_source_units":32,
    "body_original_pdf_pages":[565,566],"following_heading_pdf":566,"following_context_pdf":567,
    "full_diplomatic_second_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B05d","source_local_ids":[x["source_local_id"] for x in rows],
    "next_chapter_nav_ids":[x["source_local_id"] for x in rows[-3:]],
    "cross_page_ids":[x["source_local_id"] for x in rows if len(x["original_pdf_pages"])>1]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B05d","original_full_pdf_sha256":hash_source,
    "original_images":images,"original_body_pdf_pages":[565,566],
    "following_heading_pdf":566,"following_context_pdf":567,
    "prior_lilly_accepted":6383,"next_global_record":6384,
    "source_printed_chapter":"CV","editorial_chapter":"CVI",
    "next_printed_chapter":"CVI","next_editorial_chapter":"CVII",
    "source_discarded_Firmicus_rule":True,
    "source_three_competing_lord_selection_approaches":True,
    "source_author_near_equal_planet_mixture":True,
    "independent_personality_classification_validations":0,"runtime_promotions":0})
print(json.dumps({"batch":"B05d","source_annotations":len(rows),"spans":len(spans),"images":len(images)}))
