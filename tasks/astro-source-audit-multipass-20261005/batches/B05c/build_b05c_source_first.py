#!/usr/bin/env python3
"""Lilly 1647 printed CIV Hyleg Anareta Alcochodon first-edition source-first clauses."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def put(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
groups=J("SOURCE_GROUPS_PART1_20261017.json")+J("SOURCE_GROUPS_PART2_20261017.json")
assert len(groups)==7
n=sum(len(g["claims"]) for g in groups)
assert n==74,n
assert [g["pages"] for g in groups]==[[561,562],[562],[563],[564],[564,565],[565],[565,566]]
rows=[];spans=[]
for group in groups:
 sid=f"HYLEG-S{len(spans)+1:03}";ids=[]
 for claim in group["claims"]:
  assert len(claim) in (4,5)
  role,anchor,paraphrase,limit=claim[:4]
  pages=claim[4] if len(claim)==5 else group["pages"]
  assert all(isinstance(z,str) and z.strip() for z in claim[:4])
  assert set(pages).issubset(set(group["pages"]))
  lid=f"HYLEG-C{len(rows)+1:03}";ids.append(lid)
  rows.append({"batch":"B05c","source_local_id":lid,"source_span_id":sid,
   "chapter":"CVI_NAVIGATION_ONLY" if role=="next_navigation" else "CV",
   "printed_chapter":"CIV","role":role,
   "original_pdf_pages":pages,"printed_pages":[p-34 for p in pages],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":paraphrase,
   "original_source_qualifications":limit,
   "global_record_number":None,
   "historical_documentary_accepted":False,
   "independently_authenticated_death_or_survival":False,
   "medical_longevity_prediction_validated":False,
   "empirically_validated_prediction":False,
   "runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":group["pages"],
   "passage_label":group["label"],"mapped_local_ids":ids})
assert len(rows)==74 and len(spans)==7
assert all(r["chapter"]=="CV" for r in rows[:-3])
assert all(r["chapter"]=="CVI_NAVIGATION_ONLY" for r in rows[-3:])
assert len([r for r in rows if len(r["original_pdf_pages"])==2])==3
fullsha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in range(561,567):
 f=B/"evidence"/f"pdf_1647-{n}.jpg";raw=f.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
 "path":f.relative_to(B).as_posix(),"bytes":len(raw),
 "sha256":hashlib.sha256(raw).hexdigest()})
put("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",{
 "batch":"B05c","source_groups":groups,"source_units":74,"source_spans":7})
put("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B05c","status":"FIRST_EDITION_HISTORICAL_SOURCE_DRAFT_UNADMITTED",
 "source_units":74,"original_full_pdf_sha256":fullsha,"rows":rows})
put("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B05c","source_spans":spans,"span_count":7,"mapped_source_units":74,
 "original_body_pdf_pages":[561,562,563,564,565],"following_heading_pdf_page":565,
 "full_second_diplomatic_transcription":False})
put("SOURCE_ORDER_DRAFT.json",{
 "batch":"B05c","ordered_local_ids":[r["source_local_id"] for r in rows],
 "source_page_seam_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "following_chapter_navigation_ids":[r["source_local_id"] for r in rows[-3:]]})
put("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B05c","original_full_pdf_sha256":fullsha,
 "original_images":images,"prior_lilly_accepted":6309,"next_global_record":6310,
 "original_body_pdf_pages":[561,562,563,564,565],"following_heading_pdf_page":565,
 "source_printed_chapter":"CIV","editorial_chapter":"CV",
 "following_printed_chapter":"CV","following_editorial_chapter":"CVI",
 "source_hyleg_anareta_alcochodon_uncertainty_admitted":True,
 "source_25_degree_ascendant_exception":True,
 "source_Anareta_eighth_cusp_window_before_after_degrees":[5,25],
 "source_Alcochodon_numeric_year_values_independently_verified":False,
 "independent_actual_deaths_or_birth_times":0,
 "empirical_validations":0,"runtime_promotions":0})
print(json.dumps({"batch":"B05c","source_units":74,"passages":7,
 "source_images":6,"source_cross_page_units":3,
 "next_printed":"CV","next_heading_pdf":565,"independent_deaths_verified":0}))
