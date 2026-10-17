#!/usr/bin/env python3
"""First-edition Lilly separate dated medical/occult case: documentary claims only."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json")
assert G["source_spans"]==len(G["source_groups"])==10
assert G["source_units"]==sum(len(z["claims"]) for z in G["source_groups"])==53
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"XCV-S{len(spans)+1:03}";ids=[]
 for c in g["claims"]:
  role,anchor,meaning,limit=c
  assert all(isinstance(t,str) and t for t in c)
  local=f"XCV-C{len(rows)+1:03}";ids.append(local)
  rows.append({"batch":"B04o","source_local_id":local,"source_span_id":sid,
    "chapter":"XCVI_NAVIGATION_ONLY" if role=="next_navigation" else "XCV",
    "printed_chapter":"XCIV","role":role,"original_pdf_pages":g["pages"],
    "printed_pages":[p-34 for p in g["pages"]],
    "short_original_anchor_not_diplomatic":anchor,
    "historical_author_paraphrase":meaning,
    "original_source_qualifications":limit,"global_record_number":None,
    "historical_documentary_accepted":False,
    "independently_authenticated_occult_cause":False,
    "independently_authenticated_medical_diagnosis":False,
    "independently_verified_medical_recovery":False,
    "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
   "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==53 and len(spans)==10
assert all(r["chapter"]=="XCV" for r in rows[:-3])
assert all(r["chapter"]=="XCVI_NAVIGATION_ONLY" for r in rows[-3:])
assert [r["source_local_id"] for r in rows]==[f"XCV-C{i:03}" for i in range(1,54)]
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in (502,503,504):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
   "path":p.relative_to(B).as_posix(),"bytes":len(raw),
   "sha256":hashlib.sha256(raw).hexdigest()})
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B04o","status":"ORIGINAL_SOURCE_FIRST_PROVISIONAL",
 "source_units":53,"original_full_pdf_sha256":sha,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B04o","source_spans":spans,"span_count":10,
 "mapped_source_units":53,"original_body_pdf_pages":[502,503],
 "next_heading_pdf":504,"independent_second_diplomatic_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{
 "batch":"B04o","ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "following_heading_navigation_only":[r["source_local_id"] for r in rows[-3:]]})
dump("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B04o","original_full_pdf_sha256":sha,"original_images":imgs,
 "original_body_pdf_pages":[502,503],"following_heading_pdf":504,
 "next_numbered_chapter":"XCVI","next_printed_chapter":"XCV",
 "previous_accepted_lilly":5457,"next_global_record":5458,
 "original_chart_day_month_year":"13 March 1646",
 "original_chart_time_ambiguous":"Early morning appears 8:3 AM; exact minute unresolved",
 "separate_following_chart":"6 June 1647 8PM",
 "initial_source_witchcraft_suspicion":True,
 "ultimate_source_witchcraft_denial":True,
 "author_claims_medical_recovery_approximately_three_weeks":True,
 "independently_authenticated_medical_record":False})
print(json.dumps({"batch":"B04o","provisional_records":53,"passages":10,
 "next":"XCVI printed XCV original PDF504"}))
