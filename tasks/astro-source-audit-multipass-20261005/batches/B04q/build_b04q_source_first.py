#!/usr/bin/env python3
"""Original 1647 printed XCVI wife-husband imprisonment case documentary extraction."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert len(G["source_groups"])==G["source_spans"]==7
assert G["source_units"]==sum(len(s["claims"]) for s in G["source_groups"])==34
rows=[];spans=[]
for group in G["source_groups"]:
 sid=f"XCVII-S{len(spans)+1:03}";ids=[]
 for item in group["claims"]:
  assert len(item) in (4,5)
  role,anchor,meaning,qual=item[:4]
  assert all(isinstance(v,str) and v.strip() for v in item[:4])
  pages=item[4] if len(item)==5 else group["pages"]
  assert set(pages).issubset(set(group["pages"]))
  lid=f"XCVII-C{len(rows)+1:03}";ids.append(lid)
  rows.append(dict(batch="B04q",source_local_id=lid,source_span_id=sid,
   chapter="POST_XCVI_NAVIGATION_ONLY" if role=="next_navigation" else "XCVII",
   printed_chapter="XCVI",role=role,original_pdf_pages=pages,
   printed_pages=[x-34 for x in pages],
   short_original_anchor_not_diplomatic=anchor,historical_author_paraphrase=meaning,
   original_source_qualifications=qual,global_record_number=None,
   historical_documentary_accepted=False,
   independently_authenticated_imprisoned_husband_outcome=False,
   independently_verified_prior_garrison_capture=False,
   empirically_validated_prediction=False,runtime_model_promoted=False))
 spans.append(dict(span_id=sid,original_pdf_pages=group["pages"],passage_label=group["label"],mapped_local_ids=ids))
assert len(rows)==34 and len(spans)==7
assert all(r["chapter"]=="XCVII" for r in rows[:-4])
assert all(r["chapter"]=="POST_XCVI_NAVIGATION_ONLY" for r in rows[-4:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (505,506,507):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append(dict(original_pdf_page=n,printed_page=n-34,path=p.relative_to(B).as_posix(),
  bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",dict(batch="B04q",original_full_pdf_sha256=sha,source_units=34,rows=rows))
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",dict(batch="B04q",source_spans=spans,span_count=7,mapped_source_units=34,original_numbered_body_pages=[505,506],following_unnumbered_pdf_page=507,full_second_diplomatic_transcription=False))
dump("SOURCE_ORDER_DRAFT.json",dict(batch="B04q",ordered_ids=[r["source_local_id"] for r in rows],cross_page_ids=[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],unnumbered_next_nav=[r["source_local_id"] for r in rows[-4:]]))
dump("SOURCE_WINDOW_MANIFEST.json",dict(batch="B04q",original_full_pdf_sha256=sha,original_images=images,
 original_numbered_body_pages=[505,506],following_unnumbered_page=507,
 previous_accepted_lilly=5552,first_global_record=5553,
 original_printed_chapter="XCVI",editorial_chapter="XCVII",
 original_chart_date="19 October 1645, unverified Old Style handling",
 original_chart_clock="7:20 PM",
 author_claims_release_occurred_day_before_question=True,
 author_past_or_future_release_disjunction=True,
 unnumbered_source_study_remains_open=True,
 independent_external_military_or_custody_records=0))
print(json.dumps(dict(batch="B04q",draft_records=34,spans=7,nav=4,next="unnumbered Essex and tables")))
