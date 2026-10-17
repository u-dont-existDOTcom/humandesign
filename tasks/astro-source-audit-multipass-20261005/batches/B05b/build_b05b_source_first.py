#!/usr/bin/env python3
"""Original Lilly 1647 printed CIII infancy/lifespan source only (no individual prognosis)."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
groups=J("SOURCE_GROUPS_PART1_20261017.json")+J("SOURCE_GROUPS_PART2_20261017.json")
assert len(groups)==6
n=sum(len(g["claims"]) for g in groups)
assert n==65,n
assert [g["pages"] for g in groups]==[[559],[559,560],[560],[560,561],[561],[561]]
rows=[];spans=[]
for g in groups:
 sid=f"LIFESPAN-S{len(spans)+1:03}";ids=[]
 for claim in g["claims"]:
  assert len(claim) in (4,5)
  role,anchor,meaning,qual=claim[:4]
  original_pages=claim[4] if len(claim)==5 else g["pages"]
  assert all(isinstance(z,str) and z.strip() for z in claim[:4])
  assert set(original_pages).issubset(set(g["pages"]))
  lid=f"LIFESPAN-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B05b","source_local_id":lid,"source_span_id":sid,
    "chapter":"CV_NAVIGATION_ONLY" if role=="next_navigation" else "CIV",
    "printed_chapter":"CIII","role":role,
    "original_pdf_pages":original_pages,
    "printed_pages":[p-34 for p in original_pages],
    "short_original_anchor_not_diplomatic":anchor,
    "historical_author_paraphrase":meaning,
    "original_source_qualifications":qual,
    "global_record_number":None,"historical_documentary_accepted":False,
    "independently_authenticated_infant_survival_outcome":False,
    "medical_survival_predictive_validity":False,
    "empirically_validated_prediction":False,
    "runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
  "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==65 and len(spans)==6
assert all(r["chapter"]=="CIV" for r in rows[:-3])
assert all(r["chapter"]=="CV_NAVIGATION_ONLY" for r in rows[-3:])
assert len([r for r in rows if len(r["original_pdf_pages"])>1])==2
fullsha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (559,560,561):
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
  "path":f.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{"batch":"B05b","source_groups":groups,
 "source_units":65,"source_spans":6})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B05b",
 "status":"HISTORICAL_INFANT_LONGEVITY_SOURCE_FIRST_UNADMITTED",
 "source_units":65,"original_full_pdf_sha256":fullsha,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B05b",
 "source_spans":spans,"span_count":6,"mapped_source_units":65,
 "original_body_pdf_pages":[559,560,561],
 "following_heading_pdf":561,
 "physical_shared_chapter_page":561,
 "full_independent_diplomatic_second_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{"batch":"B05b",
 "ordered_local_ids":[r["source_local_id"] for r in rows],
 "cross_page_local_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "following_hyleg_navigation_ids":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{"batch":"B05b",
 "original_full_pdf_sha256":fullsha,"original_images":images,
 "previous_accepted_lilly":6244,"first_global_record":6245,
 "original_chapter_body_pdf_pages":[559,560,561],
 "following_hyleg_heading_pdf":561,
 "original_printed_chapter":"CIII","editorial_chapter":"CIV",
 "following_printed_chapter":"CIV","following_editorial_chapter":"CV",
 "original_lunar_phase_competing_conditions_retained":True,
 "original_explicit_do_not_pronounce_death_rashly":True,
 "source_mortality_clinical_evidence":False,
 "independent_survival_outcome_cases":0,
 "empirical_predictive_validations":0,
 "runtime_promotions":0})
print(json.dumps({"batch":"B05b","source_units":65,"spans":6,
 "shared_page":561,"substantive":62,"navigation":3,
 "independent_survival_results":0}))
