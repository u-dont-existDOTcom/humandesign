#!/usr/bin/env python3
"""Lilly 1647 LXXXVI Irish forces/Queen: source-first historical text only."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")
assert G["source_spans"]==len(G["source_groups"])==10
assert G["source_units"]==sum(len(z["claims"]) for z in G["source_groups"])==54
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"LXXXVI-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in g["claims"]:
  loc=f"LXXXVI-C{len(rows)+1:03}";ids.append(loc)
  rows.append({"source_local_id":loc,"batch":"B04f","role":role,
   "chapter":"LXXXVII_NAVIGATION_ONLY" if role=="next_navigation" else "LXXXVI",
   "source_span_id":sid,"original_pdf_pages":g["pages"],
   "printed_pages":[p-34 for p in g["pages"]],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,
   "original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_royal_military_outcome":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
 "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==54 and len(spans)==10
assert all(r["chapter"]=="LXXXVI" for r in rows[:-2])
assert all(r["chapter"]=="LXXXVII_NAVIGATION_ONLY" for r in rows[-2:])
full="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for p in (489,490):
 f=B/"evidence"/f"pdf_1647-{p}.jpg";raw=f.read_bytes()
 images.append({"original_pdf_page":p,"printed_page":p-34,
   "path":f.relative_to(B).as_posix(),"bytes":len(raw),
   "sha256":hashlib.sha256(raw).hexdigest()})
assert images[0]["sha256"]=="bf7bf966149ea94c2b042646cc6b1ccd345313789e7e13ead41e237e157916c6"
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B04f","status":"SOURCE_FIRST_PROVISIONAL",
 "original_full_pdf_sha256":full,"source_units":54,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B04f","span_count":10,"source_spans":spans,
 "mapped_source_units":54,"original_body_pdf_pages":[489,490],
 "next_heading_pdf":490,"independent_diplomatic_second_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{
 "batch":"B04f","ordered_ids":[r["source_local_id"] for r in rows],
 "original_page_bridge_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "next_chapter_navigation_ids":[r["source_local_id"] for r in rows[-2:]]})
dump("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B04f","original_full_pdf_sha256":full,
 "original_images":images,"previous_accepted_lilly":5026,
 "first_proposed_record":5027,"original_body_pdf_pages":[489,490],
 "next_numbered_chapter":"LXXXVII","next_heading_pdf":490,
 "source_figure_absolute_date_unresolved":True,
 "reported_July_14_1643_meeting_retrospective":True,
 "Queen_army_not_totally_destroyed_in_author_account":True,
 "independent_military_validations":0})
print(json.dumps({"batch":"B04f","units":54,"spans":10,"source_page":[489,490]}))
