#!/usr/bin/env python3
"""First edition Lilly, printed XCI / editorial XCII: captive or slave source."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
A=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
groups=A["source_groups"];assert len(groups)==A["source_spans"]==5
assert A["source_units"]==sum(len(g["claims"]) for g in groups)==31
rows=[];spans=[]
for g in groups:
 sid=f"XCII-S{len(spans)+1:03}"; ids=[]
 for claim in g["claims"]:
  role,anchor,meaning,qualification=claim
  assert all(isinstance(x,str) and x.strip() for x in claim)
  lid=f"XCII-C{len(rows)+1:03}";ids.append(lid)
  rows.append(dict(batch="B04l",source_local_id=lid,source_span_id=sid,
   printed_chapter="XCI",chapter="XCIII_NAVIGATION_ONLY" if role=="next_navigation" else "XCII",
   role=role,original_pdf_pages=g["pages"],printed_pages=[n-34 for n in g["pages"]],
   short_original_anchor_not_diplomatic=anchor,historical_author_paraphrase=meaning,
   original_source_qualifications=qualification,global_record_number=None,
   historical_documentary_accepted=False,independently_authenticated_captive_outcome=False,
   empirically_validated_prediction=False,runtime_model_promoted=False))
 spans.append(dict(span_id=sid,original_pdf_pages=g["pages"],passage_label=g["label"],mapped_local_ids=ids))
assert len(rows)==31 and all(r["chapter"]=="XCII" for r in rows[:-2]) and all(r["chapter"]=="XCIII_NAVIGATION_ONLY" for r in rows[-2:])
source_sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (497,498):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append(dict(original_pdf_page=n,printed_page=n-34,path=p.relative_to(B).as_posix(),
  bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
put("SOURCE_FIRST_CLAUSES_DRAFT.json",dict(batch="B04l",status="PROVISIONAL_1647_SOURCE",
 source_units=31,original_full_pdf_sha256=source_sha,rows=rows))
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",dict(batch="B04l",span_count=5,
 source_spans=spans,mapped_source_units=31,original_body_pdf_pages=[497,498],
 following_heading_pdf=498,independent_complete_diplomatic_transcription=False))
put("SOURCE_WINDOW_MANIFEST.json",dict(batch="B04l",original_full_pdf_sha256=source_sha,
 original_images=images,previous_accepted_lilly=5307,first_proposed_record=5308,
 original_body_pdf_pages=[497,498],original_printed_chapter="XCI",
 editorial_chapter="XCII",following_heading_pdf=498,next_printed_chapter="XCII",
 next_editorial_chapter="XCIII",no_identified_real_captive=True))
put("SOURCE_ORDER_DRAFT.json",dict(batch="B04l",ordered_ids=[r["source_local_id"] for r in rows],
 following_heading_navigation_only=[r["source_local_id"] for r in rows[-2:]],
 cross_page_source_ids=[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1]))
print(json.dumps(dict(batch="B04l",draft_records=31,span_groups=5,body_pages=[497,498],next="XCIII PDF498")))
