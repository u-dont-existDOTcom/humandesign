from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
get=lambda n:json.loads((B/n).read_text())
def out(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
a=get("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")
rows=[];spans=[]
for group in a["source_groups"]:
 sid=f"LXXXIX-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,qual in group["claims"]:
  lid=f"LXXXIX-C{len(rows)+1:03}";ids.append(lid)
  rows.append(dict(source_local_id=lid,batch="B04i",source_span_id=sid,
    role=role,chapter="XC_NAVIGATION_ONLY" if role=="next_navigation" else "LXXXIX",
    printed_chapter="LXXXVIII",original_pdf_pages=group["pages"],
    printed_pages=[p-34 for p in group["pages"]],
    short_original_anchor_not_diplomatic=anchor,historical_author_paraphrase=meaning,
    original_source_qualifications=qual,global_record_number=None,
    historical_documentary_accepted=False,independently_verified_relationship_outcome=False,
    empirically_validated_prediction=False,runtime_model_promoted=False))
 spans.append(dict(span_id=sid,original_pdf_pages=group["pages"],
  passage_label=group["label"],mapped_local_ids=ids))
assert len(rows)==32 and all(r["chapter"]=="LXXXIX" for r in rows[:-2])
imgs=[]
for n in (493,494):
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 imgs.append(dict(original_pdf_page=n,printed_page=n-34,path=f.relative_to(B).as_posix(),
   bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
out("SOURCE_FIRST_CLAUSES_DRAFT.json",dict(batch="B04i",source_units=32,rows=rows))
out("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",dict(batch="B04i",source_spans=spans,span_count=4,mapped_source_units=32))
out("SOURCE_WINDOW_MANIFEST.json",dict(batch="B04i",original_full_pdf_sha256=sha,original_images=imgs,
  original_body_pdf_pages=[493],following_heading_pdf=494,previous_accepted_lilly=5161,
  original_printed_chapter="LXXXVIII",editorial_chapter="LXXXIX",next_printed="LXXXIX",next_editorial="XC"))
out("CLAIM_LEDGER.json",dict(batch="B04i",source_annotations=32,new_accepted=0,
  external_human_relationship_outcomes_verified=0,empirical_predictions=0,runtime_promotions=0))
print("B04i source-first",len(rows),"records",len(spans),"passages")
