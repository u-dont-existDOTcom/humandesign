from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")
groups=G["source_groups"]
assert len(groups)==15 and sum(len(g["claims"]) for g in groups)==79
rows=[];spans=[]
for g in groups:
 sid=f"LXXXIV-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in g["claims"]:
  local=f"LXXXIV-C{len(rows)+1:03}";ids.append(local)
  rows.append({"source_local_id":local,"batch":"B04d","role":role,
  "chapter":"LXXXV_NAVIGATION_ONLY" if role=="next_navigation" else "LXXXIV",
  "source_span_id":sid,"original_pdf_pages":g["pages"],
  "printed_pages":[p-34 for p in g["pages"]],
  "short_original_anchor_not_diplomatic":anchor,
  "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
  "global_record_number":None,"historical_documentary_accepted":False,
  "independently_authenticated_vocational_outcome":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
 "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==79 and all(r["chapter"]=="LXXXIV" for r in rows[:-2]) and all(r["chapter"]=="LXXXV_NAVIGATION_ONLY" for r in rows[-2:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
ims=[]
for n in (484,485,486):
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 ims.append({"original_pdf_page":n,"printed_page":n-34,"path":f.relative_to(B).as_posix(),
 "bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04d","source_units":79,"original_full_pdf_sha256":sha,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04d","span_count":15,"source_spans":spans,"mapped_source_units":79})
dump("SOURCE_ORDER_DRAFT.json",{"batch":"B04d","ordered_ids":[r["source_local_id"] for r in rows]})
dump("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04d","original_full_pdf_sha256":sha,
 "original_images":ims,"previous_accepted_lilly":4875,"original_body_pdf_pages":[484,485],
 "following_heading_pdf":486,"next_numbered_chapter":"LXXXV",
 "following_figure_printed":"28 November 1642 9:23 AM","independent_real_vocational_outcomes":0})
print(json.dumps({"batch":"B04d","provisional_annotations":len(rows),"spans":len(spans)}))
