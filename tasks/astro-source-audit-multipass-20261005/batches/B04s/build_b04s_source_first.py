from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
def out(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
groups=G["source_groups"]
assert G["source_units"]==sum(len(g["claims"]) for g in groups)==43 and len(groups)==7
rows=[];spans=[]
for g in groups:
 sid=f"ESSEX-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in g["claims"]:
  lid=f"ESSEX-C{len(rows)+1:03}";ids.append(lid)
  rows.append(dict(source_local_id=lid,source_span_id=sid,batch="B04s",
    section="PLANETARY_HOUR_TABLE_NAV_ONLY" if role=="next_navigation" else "UNNUMBERED_ESSEX",
    original_pdf_pages=g["pages"],printed_pages=[p-34 for p in g["pages"]],
    role=role,short_original_anchor_not_diplomatic=anchor,
    historical_author_paraphrase=meaning,original_source_qualifications=limit,
    global_record_number=None,historical_documentary_accepted=False,
    independently_authenticated_original_prediction=False,
    empirically_validated_prediction=False,runtime_model_promoted=False))
 spans.append(dict(span_id=sid,original_pdf_pages=g["pages"],passage_label=g["label"],mapped_local_ids=ids))
assert len(rows)==43 and all(r["section"]=="UNNUMBERED_ESSEX" for r in rows[:-2])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (507,508):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append(dict(original_pdf_page=n,printed_page=n-34,path=p.relative_to(B).as_posix(),
  bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
out("SOURCE_FIRST_CLAUSES_DRAFT.json",dict(batch="B04s",source_units=43,rows=rows,
 original_full_pdf_sha256=sha))
out("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",dict(batch="B04s",source_spans=spans,span_count=7,mapped_source_units=43))
out("SOURCE_WINDOW_MANIFEST.json",dict(batch="B04s",original_full_pdf_sha256=sha,original_images=images,
 original_body_pdf_page=507,next_table_pdf_page=508,
 preceding_printed_chapter="XCVI",section="UNNUMBERED_ESSEX",
 previous_accepted_lilly=5586,first_proposed_record=5587,
 historic_case_chart_date="Monday 13 May 1644 12:29 PM",
 next_source_unit="PLANETARY_HOUR_TABLE",next_table_range=[508,515],
 independent_military_event_corroboration=True,independent_previous_prediction_corroboration=False))
out("SOURCE_ORDER_DRAFT.json",dict(batch="B04s",ordered_ids=[r["source_local_id"] for r in rows],next_table_nav_ids=[r["source_local_id"] for r in rows[-2:]]))
print(json.dumps({"batch":"B04s","provisional_source_units":43,"passage_groups":7,"body":507,"next":508}))
