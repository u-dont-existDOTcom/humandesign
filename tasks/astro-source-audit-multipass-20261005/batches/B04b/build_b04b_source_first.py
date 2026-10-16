#!/usr/bin/env python3
"""First-edition original Chapter LXXXII office/permanence research; source only."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")
N=G["source_units"];K=G["source_spans"]
assert K==len(G["source_groups"])==21
assert N==sum(len(g["claims"]) for g in G["source_groups"])==141
rows=[];spans=[]
for g in G["source_groups"]:
 sid=f"LXXXII-S{len(spans)+1:03}";ids=[]
 for item in g["claims"]:
  assert len(item)==4
  role,anchor,meaning,limit=item
  assert all((role,anchor,meaning,limit))
  loc=f"LXXXII-C{len(rows)+1:03}";ids.append(loc)
  rows.append({"source_local_id":loc,"batch":"B04b",
   "role":role,"chapter":"LXXXII" if role!="next_navigation" else "LXXXIII_NAVIGATION_ONLY",
   "source_span_id":sid,"original_pdf_pages":g["pages"],
   "printed_pages":[v-34 for v in g["pages"]],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,
   "original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_office_outcome":False,
   "empirically_validated_prediction":False,
   "runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":g["pages"],
  "passage_label":g["label"],"mapped_local_ids":ids})
assert len(rows)==141 and len(spans)==21
assert all(r["chapter"]=="LXXXII" for r in rows[:-2])
assert all(r["chapter"]=="LXXXIII_NAVIGATION_ONLY" for r in rows[-2:])
assert [r["source_local_id"] for r in rows]==[f"LXXXII-C{v:03}" for v in range(1,142)]
source_sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
imgs=[]
for n in (478,479,480,481,482):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 imgs.append({"original_pdf_page":n,"printed_page":n-34,
  "path":p.relative_to(B).as_posix(),"bytes":len(raw),
  "sha256":hashlib.sha256(raw).hexdigest()})
assert imgs[0]["sha256"]=="b4cf1de8927a09a87b88368825174de28d4984b586215ec8e770a8fd76c5f714"
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B04b","status":"ORIGINAL_FIRST_EDITION_SOURCE_FIRST_PROVISIONAL",
 "original_full_pdf_sha256":source_sha,"source_units":N,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B04b","source_spans":spans,"span_count":K,
 "mapped_source_units":N,"original_body_pdf_pages":[478,479,480,481,482],
 "following_heading_pdf":482,"independent_diplomatic_second_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{
 "batch":"B04b","ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "following_heading_only":[r["source_local_id"] for r in rows[-2:]]})
dump("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B04b","original_full_pdf_sha256":source_sha,
 "original_images":imgs,"original_body_pdf_pages":[478,479,480,481,482],
 "following_heading_pdf":482,"next_numbered_chapter":"LXXXIII",
 "previous_accepted_lilly":4688,"first_proposed_record":4689,
 "original_begin":"original PDF478/printed444 below separate Tenth House divider",
 "original_end":"original PDF482/printed448 above Chapter LXXXIII divider",
 "topic_modes":["obtaining_new_office","continuing_or_leaving_existing_office"],
 "independently_verified_office_outcomes":0})
issues=[
 "LXXXII is general horary counsel rather than an independently authenticated individual employment case.",
 "The original chapter opens below a decorative Tenth House boundary, not at top of PDF478.",
 "Original text continues through upper PDF482 and LXXXIII follows below a distinct divider on that page.",
 "The tenth ruler signifies office; first ruler querent; original house/regional dignity method has not been independently reconstructed.",
 "Joining ascendant ruler and Moon to Sun or tenth is grammatically delicate; avoid making mutually inconsistent conjunctive readings mandatory.",
 "Success in obtaining an office, success without expense, ease of access, financial profit and difficulty of getting it are separate endpoints.",
 "The source sometimes treats malefic planets with strong dignities as successful; good/bad planet categories cannot be used as unconditional rules.",
 "Relative weight of applying lord, speed, oriental/direct status and no opposition are specialist calculations not checked by independent astronomy.",
 "Translation of light by a third planet is an interpretive intermediary model; no identified actual broker or appointment record.",
 "Complex malefic-to-malefic-to-Fortune-to-tenth chains admit many post-hoc fits without exact declared conjunction thresholds.",
 "The source both allows benefic placement with and without reception and later requires reception for a specific subcase; preserve this apparent tension.",
 "Angular/succedent/cadent temporal shorthand is not calibrated to actual days or employment history.",
 "A negative intermediary contact without reception may cause a fallout, while mitigating trine may spare enmity without getting the office; those endpoints are distinct.",
 "The source lists first/tenth dispositors joining a third unimpeded planet and Moon, not any conjunction or reception alone.",
 "Fourth-house involvement can allegedly lead to completion after delays, even apparent despair; no independent result is documented.",
 "Mid-chapter switches from initial appointment to remaining in office and reappointment after departure; do not pool these different questions.",
 "A claimed temporary departure and more honored reinstatement require distinct outcomes and at least two verified event dates.",
 "Retrogradation, combustion or change of sign for receiving planet are alternative alleged exit timing events; horoscope-time uncertainty and range unspecified.",
 "Severe malbehavior and threatened death are generic period assertions with explicit rank/office qualification, not health or legal predictions to act on.",
 "Reports or false witness accusations against an official are authorial hypotheticals, not actual misconduct findings.",
 "The officeholder may move to another command rather than simply lose office, depending on aspect to tenth; distinguish reassignment from removal.",
 "Depictions of country damaged by a governor are different endpoints from personal office retention.",
 "For final fourth-house exit branch, exact cardinal signs Aries Cancer Libra Capricorn and lunar dignity conditions are not recalculated.",
 "The source's numerous disjunctions, mixed reception, and alternative houses prevent a single simplistic predictive success claim.",
 "No blind fixed prediction deposit, actual named officeholder, independent historical appointment records, controls or validated forecast outcomes appear in chapter.",
 "No runtime empirical promotion, practical employment recommendation, or psychological diagnosis can be supported from source-only data."
]
dump("UNRESOLVED_SOURCE_LIMITS.json",{"batch":"B04b","issues":[
 {"id":f"B04b-U{i:02}","issue":t} for i,t in enumerate(issues,1)]})
dump("CLAIM_LEDGER.json",{"batch":"B04b","status":"PROVISIONAL_ORIGINAL_TEXT_NOT_ADMITTED",
 "source_units":N,"source_passages":K,"source_issues":len(issues),
 "previous_accepted_lilly":4688,"new_accepted_documentary":0,
 "separate_new_office_and_existing_office_endpoints":True,
 "independently_verified_employment_outcomes":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0})
print(json.dumps({"batch":"B04b","draft_records":N,"spans":K,
 "issues":len(issues),"next_chapter":"LXXXIII","accepted":0}))
