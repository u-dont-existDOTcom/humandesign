#!/usr/bin/env python3
"""First edition printed CI Regiomontanus house erection source-first, unvalidated."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
groups=J("SOURCE_GROUPS_PART1_20261017.json")+J("SOURCE_GROUPS_PART2_20261017.json")
assert len(groups)==6
n=sum(len(g["claims"]) for g in groups)
assert n==70,n
assert [g["pages"][0] for g in groups]==[553,554,555,556,557,558]
rows=[];spans=[]
for g in groups:
 sid=f"REGIOMONTANUS-S{len(spans)+1:03}";ids=[]
 for claim in g["claims"]:
  assert len(claim)==4
  role,anchor,meaning,limit=claim
  assert all(isinstance(x,str) and x.strip() for x in claim)
  lid=f"REGIOMONTANUS-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B04z","source_local_id":lid,"source_span_id":sid,
    "chapter":"CIII_NAVIGATION_ONLY" if role=="next_navigation" else "CII",
    "printed_chapter":"CI","role":role,
    "original_pdf_pages":g["pages"],"printed_pages":[p-34 for p in g["pages"]],
    "short_original_anchor_not_diplomatic":anchor,
    "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
    "global_record_number":None,"historical_documentary_accepted":False,
    "full_source_numeric_tables_independently_parity_checked":False,
    "independently_verified_natal_birth_instant":False,
    "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
    "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==70 and len(spans)==6
assert all(r["chapter"]=="CII" for r in rows[:-3])
assert all(r["chapter"]=="CIII_NAVIGATION_ONLY" for r in rows[-3:])
imgs=[]
for n in range(553,559):
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
 "path":f.relative_to(B).as_posix(),"bytes":len(raw),
 "sha256":hashlib.sha256(raw).hexdigest()})
fullsha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{"batch":"B04z","source_spans":6,"source_units":70,"source_groups":groups})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04z","source_units":70,"rows":rows,
 "original_full_pdf_sha256":fullsha,"status":"SOURCE_FIRST_LOCAL_UNADMITTED"})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04z","source_spans":spans,
 "span_count":6,"mapped_source_units":70,"body_pdf_pages":list(range(553,558)),
 "following_heading_pdf":558,"full_second_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B04z","ordered_local_ids":[r["source_local_id"] for r in rows],
 "next_heading_navigation_only":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04z","original_full_pdf_sha256":fullsha,
 "original_images":imgs,"body_pdf_pages":[553,554,555,556,557],
 "following_heading_pdf":558,"previous_accepted_lilly":6145,
 "first_global_record":6146,"printed_chapter":"CI","editorial_chapter":"CII",
 "next_printed_chapter":"CII","next_editorial_chapter":"CIII",
 "original_birth_time":"19 September 1616 14:24:25 historical local time",
 "source_uses_30_seconds_in_one_time_conversion":True,
 "source_MC_right_ascension":"222deg10",
 "precise_intermediate_MC_right_ascension":"222deg10min10sec",
 "source_ascendant":"Capricorn 6deg37",
 "interpolated_from_printed_table":"Capricorn approximately 6deg40",
 "full_astrological_ephemeris_parity":False,
 "independent_known_birth_instant":False})
print(json.dumps({"batch":"B04z","first_edition_source_units":70,"passages":6,
 "images":6,"following_heading":558,"independent_validations":0}))
