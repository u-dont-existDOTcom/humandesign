#!/usr/bin/env python3
"""Lilly original 1647 Chapter LXXXI Philosopher's Stone, primary-source-first."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
J=lambda name:json.loads((B/name).read_text(encoding="utf-8"))
def dump(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")
assert G["source_spans"]==len(G["source_groups"])==11
assert G["source_units"]==sum(len(z["claims"]) for z in G["source_groups"])==57
ROWS=[];SPANS=[]
for group in G["source_groups"]:
 sid=f"LXXXI-S{len(SPANS)+1:03}";ids=[]
 for role,anchor,meaning,limit in group["claims"]:
  local=f"LXXXI-C{len(ROWS)+1:03}";ids.append(local)
  ROWS.append({"source_local_id":local,"batch":"B04a",
   "role":role,"chapter":"LXXXI" if role!="next_navigation" else "LXXXII_NAVIGATION_ONLY",
   "source_span_id":sid,"original_pdf_pages":group["pages"],
   "printed_pages":[n-34 for n in group["pages"]],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,
   "original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_philosophers_stone_case":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 SPANS.append({"span_id":sid,"original_pdf_pages":group["pages"],
   "passage_label":group["label"],"mapped_local_ids":ids})
assert len(ROWS)==57 and len(SPANS)==11
assert all(r["chapter"]=="LXXXI" for r in ROWS[:-3])
assert all(r["chapter"]=="LXXXII_NAVIGATION_ONLY" for r in ROWS[-3:])
sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (476,477,478):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
   "path":p.relative_to(B).as_posix(),"bytes":len(raw),
   "sha256":hashlib.sha256(raw).hexdigest()})
# The opening witness image must have identical bytes to the preceding chapter.
assert images[0]["sha256"]=="d776ad9f25c4742b22e23638701d1b03bbb332ee79109b1654760f2199206146"
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B04a","status":"SOURCE_FIRST_PROVISIONAL_ORIGINAL_TEXT",
 "source_units":57,"original_full_pdf_sha256":sha,"rows":ROWS})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B04a","source_spans":SPANS,"span_count":11,
 "mapped_source_units":57,"original_body_pdf_pages":[476,477,478],
 "following_heading_pdf":478,"independent_second_diplomatic_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{"batch":"B04a",
 "ordered_ids":[r["source_local_id"] for r in ROWS],
 "cross_page_ids":[r["source_local_id"] for r in ROWS if len(r["original_pdf_pages"])>1],
 "following_section_navigation_only":[r["source_local_id"] for r in ROWS[-3:]]})
dump("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B04a","original_full_pdf_sha256":sha,"original_images":images,
 "original_body_pdf_pages":[476,477,478],"next_heading_pdf":478,
 "previous_accepted_lilly":4631,"first_proposed_record":4632,
 "following_chapter":"LXXXII","original_begin":"PDF476/printed442 BELOW LXXX divider",
 "original_end":"PDF478/printed444 ABOVE Tenth House decorative divider",
 "source_figure_timestamp":"27 May 1647 10:45 AM",
 "independently_authenticated_elixir_outputs":0,
 "independently_authenticated_medical_diagnoses":0})
issues=[
 "The Philosophers Stone and elixir are objects of the author's personal belief; source narrative is not proof either exists.",
 "The author says revelation by angels is likelier than human skill; this is metaphysical explanation, not tested causal evidence.",
 "The horary question is narrowed from universal possibility to a specific querent's capability; preserve this semantic shift.",
 "The querent is unidentified and no independent signed 1647 questionnaire or contemporaneous chart calculation is available.",
 "Original 27 May 1647 10:45 AM square figure is preserved unmodified; ephemeris, cusps and calendar have no second calculation.",
 "Mars is called cadent yet in its own term and face; opposed dignities cannot be collapsed into a single weak indicator.",
 "Mars's square to Mercury and Saturn, including their fixed sign/term relation, requires specialist original-glyph parity.",
 "Mercury is said to have been retrograde, become slowly direct and approached a second Mars square; no independent event chart replay.",
 "A previous failed elixir search is Lilly's asserted inference, not authenticated laboratory or historical participant record.",
 "The source's renewed desire and hope are inferred from horary symbolism, not independently observed psychological responses.",
 "Mercury's later Gemini position belongs to a subsequent application, not necessarily the figure's initial sign.",
 "The author's alleged advice to stop the search has no external contemporary document or receipt.",
 "Lilly's speculative chemical failure explanation (gross/heavy matter, defective composition) has no tested sample, assay, recipe or reproducible protocol.",
 "Saturn/Mercury combinations are used to infer intellect and imagination but provide no validated assessment of real cognition.",
 "The source introduces a separate claim that the querent may suffer from consumption, an unverified historical medical diagnosis.",
 "Repeated squares are reused in both elixir failure and medical danger; not independent evidence and no high-stakes diagnostic utility.",
 "Saturn sixth and Mars twelfth references do not establish a medical mechanism, disease severity or prognosis.",
 "No medical observation, actual outcome, treatment response, external disease registry or follow-up of the queried man is recorded.",
 "A decorative divider and separate Tenth House / LXXXII question begin after this example on PDF478; do not import later generic office rules.",
 "There is no independent successful stone manufacture, no dated first-person transcript, no blind forecast registration, no controls or predictive validation; zero runtime promotion."
]
dump("UNRESOLVED_SOURCE_LIMITS.json",{"batch":"B04a",
 "issues":[{"id":f"B04a-U{i:02}","issue":s} for i,s in enumerate(issues,1)]})
dump("CLAIM_LEDGER.json",{"batch":"B04a","status":"SOURCE_FIRST_PROVISIONAL",
 "source_records_drafted":57,"source_passage_groups":11,"source_uncertainties":len(issues),
 "prior_accepted_lilly":4631,"new_accepted_records":0,
 "authorial_beliefs_about_elixir":sum(r["role"]=="authorial_belief" for r in ROWS),
 "independently_proven_philosophers_stones":0,
 "independently_authenticated_consumption_diagnoses":0,
 "new_empirical_predictive_validations":0,"runtime_promotions":0})
print(json.dumps({"batch":"B04a","draft_units":len(ROWS),"spans":len(SPANS),
 "issues":len(issues),"following_chapter":"LXXXII","accepted":0}))
