#!/usr/bin/env python3
"""Source-first clauses for Lilly printed Chapter C/event-fitted birth times."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
groups=sum((J(f"SOURCE_GROUPS_PART{i}_20261017.json") for i in [1,2,3]),[])
n=sum(len(g["claims"]) for g in groups)
assert len(groups)==13 and n==188,(len(groups),n)
assert [g["pages"][0] for g in groups]==list(range(541,554))
rows=[];spans=[]
for g in groups:
 sid=f"ACCIDENT-S{len(spans)+1:03}";ids=[]
 for c in g["claims"]:
  assert len(c)==4
  role,anchor,paraphrase,limit=c
  assert all(isinstance(x,str) and x.strip() for x in c)
  lid=f"ACCIDENT-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B04y","source_local_id":lid,"source_span_id":sid,
    "chapter":"CII_NAVIGATION_ONLY" if role=="next_navigation" else "CI",
    "printed_chapter":"C","role":role,
    "original_pdf_pages":g["pages"],"printed_pages":[p-34 for p in g["pages"]],
    "short_original_anchor_not_diplomatic":anchor,
    "historical_author_paraphrase":paraphrase,
    "original_source_qualifications":limit,
    "global_record_number":None,"historical_documentary_accepted":False,
    "independently_authenticated_merchant_life_event":False,
    "independently_validated_birth_time_rectification":False,
    "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
   "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==188 and len(spans)==13
assert all(r["chapter"]=="CI" for r in rows[:-3])
assert all(r["chapter"]=="CII_NAVIGATION_ONLY" for r in rows[-3:])
fullsha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in range(541,555):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
   "path":p.relative_to(B).as_posix(),"bytes":len(raw),
   "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{"batch":"B04y","source_groups":groups,
 "source_spans":13,"source_units":188,"original_printed_chapter":"C","editorial_chapter":"CI"})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04y",
 "status":"ORIGINAL_IMAGE_SOURCE_FIRST_DOCUMENTARY_ONLY_UNADMITTED",
 "source_units":188,"original_full_pdf_sha256":fullsha,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04y",
 "source_spans":spans,"span_count":13,"mapped_source_units":188,
 "original_body_pdf_pages":list(range(541,554)),
 "following_heading_pdf":553,"following_context_pdf":554,
 "full_second_diplomatic_transcription":False,
 "full_speculum_numeric_cells_digitized":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04y",
 "ordered_local_ids":[r["source_local_id"] for r in rows],
 "following_chapter_navigation_only":[r["source_local_id"] for r in rows[-3:]],
 "independent_validated_predictions":0})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04y",
 "original_full_pdf_sha256":fullsha,"original_images":imgs,
 "previous_accepted_lilly":5957,"next_global_record":5958,
 "original_pdf_body_pages":list(range(541,554)),
 "following_heading_pdf_page":553,
 "following_printed_chapter":"CI","following_editorial_chapter":"CII",
 "retrospective_event_merchant_initial_target_ages":[
  {"event":"master appointment","years":16,"months":7},
  {"event":"sea voyage","years":20,"months":4},
  {"event":"burning fever","years":20,"months":10},
  {"event":"later fever melancholy scurvy","years":24,"months":11}],
 "source_mars_opposition_fit_age":{"years":19,"months":10,"days":10},
 "source_fever_age_mismatch_unresolved":True,
 "source_Moon61deg44_plus144_correct": "205deg44",
 "source_page546_apparent_misprint":"105deg44",
 "source_page547_follows_correct_value":"205deg44",
 "first_edition_speculum_image_page":543,
 "all_speculum_numeric_cells_transcribed":False,
 "in_sample_accident_fitting_only":True,
 "independent_merchant_birth_certificate":False,
 "new_empirical_validations":0,"runtime_model_promotions":0})
print(json.dumps({"batch":"B04y","source_units":188,"source_passages":13,
"image_witnesses":14,"next_printed":"CI","next_pdf":553,"no_predictive_validation":True}))
