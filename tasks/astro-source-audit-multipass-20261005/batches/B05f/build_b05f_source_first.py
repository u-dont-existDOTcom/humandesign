#!/usr/bin/env python3
"""Source first Lilly first-edition manners with precise boundaries and disclaimers."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
groups=J("SOURCE_GROUPS_PART1_20261017.json")+J("SOURCE_GROUPS_PART2_20261017.json")
assert len(groups)==14 and sum(len(g["claims"]) for g in groups)==86
rows=[];spans=[]
for q in groups:
 sid=f"MANNERS-S{len(spans)+1:03}";ids=[]
 for i,c in enumerate(q["claims"]):
  assert len(c)==4 and all(isinstance(x,str) and x.strip() for x in c)
  role,anchor,meaning,limit=c
  pages=q["pages"]
  if pages==[569,570]:
   pages=[569,570] if role=="source_continuation" else [569]
  elif pages==[570,571]:
   pages=[570,571] if role=="source_continuation" else [571]
  assert set(pages).issubset(set(q["pages"]))
  lid=f"MANNERS-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B05f","source_local_id":lid,"source_span_id":sid,
    "chapter":"CIX_NAVIGATION_ONLY" if role=="next_navigation" else "CVIII",
    "printed_chapter":"CVII","role":role,
    "original_pdf_pages":pages,"printed_pages":[p-34 for p in pages],
    "short_original_anchor_not_diplomatic":anchor,
    "historical_author_paraphrase":meaning,
    "original_source_qualifications":limit,
    "global_record_number":None,"historical_documentary_accepted":False,
    "independently_validated_human_personality":False,
    "independently_validated_criminal_or_medical_prognosis":False,
    "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":q["pages"],
   "passage_label":q["label"],"mapped_local_ids":ids})
assert len(rows)==86 and len(spans)==14
assert all(r["chapter"]=="CVIII" for r in rows[:-3])
assert all(r["chapter"]=="CIX_NAVIGATION_ONLY" for r in rows[-3:])
images=[]
for n in range(568,576):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
   "path":p.relative_to(B).as_posix(),"bytes":len(raw),
   "sha256":hashlib.sha256(raw).hexdigest()})
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{"batch":"B05f","source_units":86,
 "source_spans":14,"source_groups":groups})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B05f","source_units":86,
 "original_full_pdf_sha256":sha,"status":"PROVISIONAL_SOURCE_FIRST_NOT_EMPIRICAL","rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B05f","source_spans":spans,
 "span_count":14,"mapped_source_units":86,
 "original_body_pdf_pages":list(range(568,574)),
 "following_heading_pdf":573,
 "following_context_pages":[574,575],"full_independent_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B05f","source_local_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "following_manners_planet_chapter_nav":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B05f","original_full_pdf_sha256":sha,
 "original_images":images,"original_body_pdf_pages":list(range(568,574)),
 "following_heading_pdf":573,"following_context_pdf_pages":[574,575],
 "previous_accepted_lilly":6474,"next_global_record":6475,
 "printed_chapter":"CVII","editorial_chapter":"CVIII",
 "following_printed_chapter":"CVIII","following_editorial_chapter":"CIX",
 "source_Mercury_Moon_Ascendant_fallbacks_multiple":True,
 "Moon_direction_manners_change_source":True,
 "specific_fixed_star_violent_accusations_historical_only":True,
 "Johannes_Angelus_fine_degree_scheme_author_rejected":True,
 "twelve_sign_stereotypes_not_empirical":True,
 "independently_validated_human_personality_matches":0,
 "runtime_promotions":0})
print(json.dumps({"batch":"B05f","annotations":86,"source_spans":14,"image_witnesses":len(images),"next":"printed CVIII PDF573"}))
