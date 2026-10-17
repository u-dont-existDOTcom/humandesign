#!/usr/bin/env python3
"""First-edition Lilly natal prejudgment source-first, unvalidated documentary annotations."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert G["batch"]=="B05a" and G["source_units"]==29 and G["source_spans"]==4
assert len(G["source_groups"])==4 and sum(len(g["claims"]) for g in G["source_groups"])==29
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"NATAL-PREJUDGMENT-S{len(spans)+1:03}";ids=[]
 for item in g["claims"]:
  assert len(item)==4
  role,anchor,claim,caveat=item
  assert all(isinstance(x,str) and x.strip() for x in item)
  lid=f"NATAL-PREJUDGMENT-C{len(rows)+1:03}";ids.append(lid)
  rows.append({
   "batch":"B05a","source_local_id":lid,"source_span_id":sid,
   "chapter":"CIV_NAVIGATION_ONLY" if role=="next_navigation" else "CIII",
   "printed_chapter":"CII","role":role,"original_pdf_pages":g["pages"],
   "printed_pages":[p-34 for p in g["pages"]],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":claim,"original_source_qualifications":caveat,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_verified_natal_outcome":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
  "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==29 and len(spans)==4
assert all(r["chapter"]=="CIII" for r in rows[:-3])
assert all(r["chapter"]=="CIV_NAVIGATION_ONLY" for r in rows[-3:])
fullsha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in [558,559]:
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
 "path":f.relative_to(B).as_posix(),"bytes":len(raw),
 "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B05a",
 "status":"ORIGINAL_SOURCE_FIRST_DOCUMENTARY_ONLY_UNADMITTED",
 "source_units":29,"original_full_pdf_sha256":fullsha,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B05a","source_spans":spans,
 "span_count":4,"mapped_source_units":29,
 "body_original_pdf_pages":[558],"following_heading_pdf_page":559,
 "complete_independent_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B05a",
 "ordered_ids":[r["source_local_id"] for r in rows],
 "following_chapter_navigation":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B05a","original_full_pdf_sha256":fullsha,
 "original_images":images,"previous_accepted_lilly":6215,"next_global_record":6216,
 "body_original_pdf_page":558,"next_original_pdf_page":559,
 "printed_chapter":"CII","editorial_chapter":"CIII",
 "next_printed_chapter":"CIII","next_editorial_chapter":"CIV",
 "original_chapter_only_one_page":True,
 "source_antiscia_numeric_orb_stated":False,
 "source_fixed_stars_small_latitude_numeric_threshold_stated":False,
 "source_accident_based_method_favored":True,
 "independent_predicted_person_cases":0,
 "empirical_validations":0,"runtime_promotions":0})
print(json.dumps({"batch":"B05a","source_units":29,"passages":4,
 "substantive":26,"following_navigation":3,"images":2,
 "next_printed_chapter":"CIII"}))
