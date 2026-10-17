#!/usr/bin/env python3
"""Read original source-first descriptions of Lilly's dated fugitive horary."""
from pathlib import Path
import json
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,j):(B/n).write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
W=J("SOURCE_WINDOW_PROVISIONAL_20261017.json")
assert G["source_spans"]==len(G["source_groups"])==7
assert G["source_units"]==sum(len(g["claims"]) for g in G["source_groups"])==42
assert W["parent_accepted_lilly"]==5510 and W["next_global_record_number"]==5511
assert W["original_body_pdf_pages"]==[504,505] and W["following_heading_pdf"]==505
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"XCVI-S{len(spans)+1:03}";ids=[]
 for c in g["claims"]:
  assert len(c) in (4,5)
  role,anchor,paraphrase,qual=c[:4]
  assert all(isinstance(z,str) and z.strip() for z in c[:4])
  pages=c[4] if len(c)==5 else g["pages"]
  assert set(pages).issubset(set(g["pages"]))
  lid=f"XCVI-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"source_local_id":lid,"batch":"B04p","source_span_id":sid,
   "chapter":"XCVII_NAVIGATION_ONLY" if role=="next_navigation" else "XCVI",
   "printed_chapter":"XCV","role":role,
   "original_pdf_pages":pages,"printed_pages":[p-34 for p in pages],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":paraphrase,"original_source_qualifications":qual,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_verified_escaped_prisoner_identity":False,
   "independently_authenticated_fugitive_recapture":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
  "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==42 and len(spans)==7
assert all(r["chapter"]=="XCVI" for r in rows[:-3])
assert all(r["chapter"]=="XCVII_NAVIGATION_ONLY" for r in rows[-3:])
assert [r["source_local_id"] for r in rows]==[f"XCVI-C{i:03}" for i in range(1,43)]
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B04p","status":"ORIGINAL_FIRST_EDITION_SOURCE_FIRST_NOT_ADMITTED",
 "source_units":42,"original_full_pdf_sha256":W["original_full_pdf_sha256"],
 "rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B04p","source_spans":spans,"span_count":7,
 "mapped_source_units":42,"original_body_pdf_pages":[504,505],
 "following_heading_pdf":505,"independent_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04p",
 "ordered_source_local_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "navigation_only":[r["source_local_id"] for r in rows[-3:]]})
put("CLAIM_LEDGER_PROVISIONAL.json",{"batch":"B04p","source_units":42,
 "source_passages":7,"unresolved_limits":len(J("UNRESOLVED_SOURCE_LIMITS.json")["issues"]),
 "author_reported_east_direction":1,"author_reported_friday_letter":1,
 "author_reported_sunday_recapture":1,
 "independent_witnessed_fugitive_outcomes":0,"empirical_validations":0,"runtime_promotions":0})
print(json.dumps({"batch":"B04p","draft_records":42,"groups":7,
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1]}))
