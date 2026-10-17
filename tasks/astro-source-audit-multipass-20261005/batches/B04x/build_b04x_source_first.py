#!/usr/bin/env python3
"""Original first-edition Lilly Animodar source-first clauses; no predictive-credit admission."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,j):(B/n).write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert G["source_spans"]==len(G["source_groups"])==5
assert G["source_units"]==sum(len(g["claims"]) for g in G["source_groups"])==34
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
rows=[];groups=[]
for g in G["source_groups"]:
 sid=f"ANIMODAR-S{len(groups)+1:03}";ids=[]
 for c in g["claims"]:
  role,anchor,paraphrase,limit=c
  assert all(isinstance(z,str) and z.strip() for z in c)
  lid=f"ANIMODAR-C{len(rows)+1:03}";ids.append(lid)
  pages=g["pages"]
  rows.append({"batch":"B04x","source_local_id":lid,"source_span_id":sid,
   "chapter":"CI_NAVIGATION_ONLY" if role=="next_navigation" else "C",
   "printed_chapter":"XCIX","role":role,"original_pdf_pages":pages,
   "printed_pages":[p-34 for p in pages],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":paraphrase,
   "original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_birth_time":False,
   "independently_validated_Animodar_accuracy":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 groups.append({"span_id":sid,"original_pdf_pages":g["pages"],"passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==34 and len(groups)==5
assert all(r["chapter"]=="C" for r in rows[:-3])
assert all(r["chapter"]=="CI_NAVIGATION_ONLY" for r in rows[-3:])
imgs=[]
for n in [539,540,541]:
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
   "path":p.relative_to(B).as_posix(),"bytes":len(raw),
   "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04x","status":"ORIGINAL_FIRST_EDITION_SOURCE_FIRST_PROVISIONAL",
 "source_units":34,"original_full_pdf_sha256":sha,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04x","source_spans":groups,"span_count":5,
 "mapped_source_units":34,"body_pdf_pages":[539,540],"following_heading_pdf":541,
 "full_independent_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04x","ordered_local_ids":[r["source_local_id"] for r in rows],
 "following_heading_nav_ids":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04x","original_full_pdf_sha256":sha,
 "original_images":imgs,"original_body_pdf_pages":[539,540],"following_heading_pdf":541,
 "previous_lilly_accepted":5923,"next_global_record":5924,
 "editorial_chapter":"C","printed_chapter":"XCIX",
 "source_example_full_moon_date":"15 September 1616","source_merchant_birth_date":"19 September 1616",
 "source_example_Sun_at_full_moon":"Libra 2 degrees 32 minutes",
 "source_example_dignity_winner":"Saturn",
 "source_Animodar_ascendant":"Capricorn 9 degrees 2 minutes",
 "source_author_deems_Animodar_less_sure_than_accidents":True,
 "independent_birth_time_certificate":False,
 "source_requires_dignities_external_table":True,
 "no_externally_verified_natal_success":True})
print(json.dumps({"batch":"B04x","provisional_source_units":34,"spans":5,
 "original_images":3,"next":"printed Chapter C on PDF541"}))
