from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
read=lambda name:json.loads((B/name).read_text())
def put(name,data):(B/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
groups=read("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")["source_groups"]
rows=[];spans=[]
for group in groups:
 sid=f"LXXXIII-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in group["claims"]:
  local=f"LXXXIII-C{len(rows)+1:03}";ids.append(local)
  rows.append(dict(source_local_id=local,batch="B04c",role=role,
     chapter="LXXXIV_NAVIGATION_ONLY" if role=="next_navigation" else "LXXXIII",
     source_span_id=sid,original_pdf_pages=group["pages"],printed_pages=[n-34 for n in group["pages"]],
     short_original_anchor_not_diplomatic=anchor,historical_author_paraphrase=meaning,
     original_source_qualifications=limit,global_record_number=None,
     historical_documentary_accepted=False,independently_authenticated_restoration_outcome=False,
     empirically_validated_prediction=False,runtime_model_promoted=False))
 spans.append(dict(span_id=sid,original_pdf_pages=group["pages"],
                   passage_label=group["label"],mapped_local_ids=ids))
assert len(rows)==46 and len(spans)==8 and all(r["chapter"]=="LXXXIII" for r in rows[:-2]) and all(r["chapter"]=="LXXXIV_NAVIGATION_ONLY" for r in rows[-2:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in [482,483,484]:
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 images.append(dict(original_pdf_page=n,printed_page=n-34,path=f.relative_to(B).as_posix(),
                    bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
put("SOURCE_FIRST_CLAUSES_DRAFT.json",dict(batch="B04c",source_units=46,original_full_pdf_sha256=sha,rows=rows))
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",dict(batch="B04c",span_count=8,source_spans=spans,mapped_source_units=46))
put("SOURCE_ORDER_DRAFT.json",dict(batch="B04c",ordered_ids=[r["source_local_id"] for r in rows]))
put("SOURCE_WINDOW_MANIFEST.json",dict(batch="B04c",original_full_pdf_sha256=sha,
 original_images=images,original_body_pdf_pages=[482,483,484],previous_accepted_lilly=4829,
 following_heading_pdf=484,next_numbered_chapter="LXXXIV",independent_validations=0))
print(json.dumps(dict(batch="B04c",draft_records=len(rows),passages=len(spans))))
