#!/usr/bin/env python3
"""Lilly first-edition printed XCII / editorial XCIII historical belief and remedies."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert G["source_spans"]==len(G["source_groups"])==11
assert G["source_units"]==sum(len(g["claims"]) for g in G["source_groups"])==75
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"XCIII-S{len(spans)+1:03}";ids=[]
 for x in g["claims"]:
  assert len(x) in (4,5)
  role,anchor,meaning,limit=x[:4]
  assert all(isinstance(v,str) and v.strip() for v in x[:4])
  pages=x[4] if len(x)==5 else g["pages"]
  assert set(pages).issubset(set(g["pages"]))
  lid=f"XCIII-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"source_local_id":lid,"batch":"B04m","source_span_id":sid,
   "role":role,"chapter":"XCIV_NAVIGATION_ONLY" if role=="next_navigation" else "XCIII",
   "original_printed_chapter":"XCII",
   "original_pdf_pages":pages,"printed_pages":[n-34 for n in pages],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_occult_causation":False,
   "independently_authenticated_treatment_success":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
   "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==75 and len(spans)==11
assert all(r["chapter"]=="XCIII" for r in rows[:-3])
assert all(r["chapter"]=="XCIV_NAVIGATION_ONLY" for r in rows[-3:])
assert [r["source_local_id"] for r in rows]==[f"XCIII-C{i:03}" for i in range(1,76)]
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (498,499,500,501):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
  "path":p.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04m","status":"ORIGINAL_TEXT_SOURCE_FIRST_PROVISIONAL",
 "source_units":75,"original_full_pdf_sha256":sha,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04m","span_count":11,
 "source_spans":spans,"mapped_source_units":75,
 "original_body_pdf_pages":[498,499,500],"following_heading_pdf":501,
 "independent_full_second_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04m","ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "next_chapter_navigation_only":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04m","original_full_pdf_sha256":sha,
 "original_images":images,"original_body_pdf_pages":[498,499,500],
 "following_heading_pdf":501,"next_numbered_chapter":"XCIV",
 "next_printed_chapter":"XCIII","previous_accepted_lilly":5338,
 "next_global_record":5339,"original_begin":"PDF498/printed464 BELOW Captive or Slave divider",
 "original_end":"PDF500/printed466 through end, next heading PDF501/printed467",
 "unnumbered_remedies_subheading_within_same_chapter":True,
 "original_supernatural_and_treatment_claims_unverified":True})
print(json.dumps({"batch":"B04m","draft_annotations":len(rows),"passages":len(spans),
 "body_pages":[498,499,500],"next":"XCIV printed XCIII PDF501"}))
