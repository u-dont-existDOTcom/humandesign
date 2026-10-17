#!/usr/bin/env python3
"""Source-first Lilly temperament as historical four-humours, no human validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert G["source_units"]==sum(len(g["claims"]) for g in G["source_groups"])==59
assert len(G["source_groups"])==G["source_spans"]==9
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"TEMPER-S{len(spans)+1:03}";ids=[]
 for i,c in enumerate(g["claims"]):
  assert len(c)==4
  role,anchor,meaning,qual=c
  pages=g["pages"]
  if pages==[568,569]:
   pages=[568] if i<2 else [569]
  assert set(pages).issubset(set(g["pages"]))
  lid=f"TEMPER-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B05e","source_local_id":lid,"source_span_id":sid,
   "chapter":"CVIII_NAVIGATION_ONLY" if role=="next_navigation" else "CVII",
   "printed_chapter":"CVI","role":role,"original_pdf_pages":pages,
   "printed_pages":[p-34 for p in pages],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,
   "original_source_qualifications":qual,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_validated_temperament_or_health":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
   "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==59 and len(spans)==9
assert all(r["chapter"]=="CVII" for r in rows[:-3])
assert all(r["chapter"]=="CVIII_NAVIGATION_ONLY" for r in rows[-3:])
imgs=[]
for n in range(566,570):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";data=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
  "path":p.relative_to(B).as_posix(),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B05e","source_units":59,
 "original_full_pdf_sha256":sha,"status":"PROVISIONAL_FIRST_EDITION_SOURCE_ONLY","rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B05e","source_spans":spans,
 "span_count":9,"mapped_source_units":59,"original_body_pdf_pages":[566,567,568],
 "following_heading_pdf":568,"following_context_pdf":569,"independent_full_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B05e",
 "ordered_local_ids":[r["source_local_id"] for r in rows],
 "next_chapter_navigation_only":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B05e","original_full_pdf_sha256":sha,
 "original_images":imgs,"original_body_pdf_pages":[566,567,568],
 "following_heading_pdf":568,"following_context_pdf":569,
 "previous_accepted_lilly":6415,"next_global_record":6416,
 "printed_chapter":"CVI","editorial_chapter":"CVII",
 "next_printed_chapter":"CVII","next_editorial_chapter":"CVIII",
 "four_humours_source_labels":["sanguine","phlegmatic","choleric","melancholic"],
 "testimony_counts_cancel_opposed_equal":True,
 "lord_geniture_and_ascendant_planet_threefold":True,
 "moon_in_ascendant_twofold":True,
 "actual_human_humoral_biomedical_validation":False,
 "new_empirical_validations":0,"runtime_promotions":0})
print(json.dumps({"batch":"B05e","source_units":59,"passages":9,"images":4,"next":"Manners CVII"}))
