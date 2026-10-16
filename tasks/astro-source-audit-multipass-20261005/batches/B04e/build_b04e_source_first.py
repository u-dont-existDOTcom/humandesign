#!/usr/bin/env python3
"""Original 1647 Lilly Chapter LXXXV first-edition source-first annotations."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
G=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")
groups=G["source_groups"];assert len(groups)==G["source_spans"]==11
assert sum(len(g["claims"]) for g in groups)==G["source_units"]==72
rows=[];spans=[]
for group in groups:
 sid=f"LXXXV-S{len(spans)+1:03}";ids=[]
 for role,anchor,meaning,limit in group["claims"]:
  assert all(isinstance(v,str) and v for v in (role,anchor,meaning,limit))
  local=f"LXXXV-C{len(rows)+1:03}";ids.append(local)
  rows.append({"source_local_id":local,"batch":"B04e","role":role,
   "chapter":"LXXXVI_NAVIGATION_ONLY" if role=="next_navigation" else "LXXXV",
   "source_span_id":sid,"original_pdf_pages":group["pages"],
   "printed_pages":[p-34 for p in group["pages"]],
   "short_original_anchor_not_diplomatic":anchor,
   "historical_author_paraphrase":meaning,"original_source_qualifications":limit,
   "global_record_number":None,"historical_documentary_accepted":False,
   "independently_authenticated_wartime_outcome":False,
   "empirically_validated_prediction":False,"runtime_model_promoted":False})
 spans.append({"span_id":sid,"original_pdf_pages":group["pages"],
 "passage_label":group["label"],"mapped_local_ids":ids})
assert len(rows)==72 and len(spans)==11
assert all(r["chapter"]=="LXXXV" for r in rows[:-2])
assert all(r["chapter"]=="LXXXVI_NAVIGATION_ONLY" for r in rows[-2:])
SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
images=[]
for n in (486,487,488,489):
 p=B/"evidence"/f"pdf_1647-{n}.jpg";raw=p.read_bytes()
 images.append({"original_pdf_page":n,"printed_page":n-34,
 "path":p.relative_to(B).as_posix(),"bytes":len(raw),
 "sha256":hashlib.sha256(raw).hexdigest()})
assert images[0]["sha256"]=="ada1c54f859ae672218bdc7fb03c3ab7fc12235e7608a798d71ce7edb5ffe2ba"
assert images[1]["sha256"]=="0ae0ae9cdc9115308a0ce4b901690bc19b9a797a133093aa9e918be2c580b533"
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{"batch":"B04e","source_units":72,
 "original_full_pdf_sha256":SHA,"status":"SOURCE_FIRST_ORIGINAL_TEXT_PROVISIONAL","rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{"batch":"B04e","span_count":11,
 "source_spans":spans,"mapped_source_units":72,"original_body_pdf_pages":[486,487,488],
 "next_heading_pdf":489,"independent_second_diplomatic_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{"batch":"B04e",
 "ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "next_heading_navigation_only":[r["source_local_id"] for r in rows[-2:]]})
dump("SOURCE_WINDOW_MANIFEST.json",{"batch":"B04e","original_full_pdf_sha256":SHA,
 "original_images":images,"original_body_pdf_pages":[486,487,488],
 "previous_accepted_lilly":4954,"next_numbered_chapter":"LXXXVI","following_heading_pdf":489,
 "original_begin":"PDF486/printed452 new Prince Rupert/Essex polygonal horary",
 "original_end":"PDF488/printed454 before separate LXXXVI heading",
 "original_question_timestamp":"28 November 1642 9:23 AM",
 "independent_wartime_outcomes_verified":0})
limits=[
 "Original LXXXV starts on PDF486 and closes end of PDF488, before LXXXVI begins PDF489.",
 "Multiple questions about military honor, overcoming Essex, life, confinement and later fate must not be pooled as a single outcome.",
 "The original square/polygonal chart dated 28 November 1642 9:23 AM is preserved, but horary ephemeris and old-style time not independently recast.",
 "The querent's parliamentary loyalties and material involvement are source claims; no independently identified signed question survives here.",
 "Lilly says vulgar or ordinary Guido/Haly rules do not adequately handle the question, increasing interpretation flexibility.",
 "The author reports 24 hours' deliberation; initial favorable respect language and eventual dishonor verdict are different phases.",
 "Moon sinister trine and Jupiter dexter trine to tenth cannot be substituted for each other.",
 "Rupert is assigned tenth-house Scorpio with Mars ruler; this assignment is context-specific and not a verified astronomical chart.",
 "Lilly expects Rupert to live while not gaining glory; negative death, status, battlefield and captivity outcomes are separate.",
 "Inferences of obstinacy and perverseness from Mars detriment or fixed sign are unverified moral/personality assessments.",
 "Essex as Venus ruler of opposite Taurus is a derived assignment; no independent calculation of reception/aspect parity.",
 "The Battle of Edgehill had already taken place more than a month before the dated question: no subsequent event was predicted by identifying it.",
 "Lilly claims Essex had the better at Edgehill because Essex held ground, but whether that counts as historical victory is contested and has not been independently adjudicated here.",
 "Lilly attributes supportive battle testimony to King's officers, but gives no separately authenticated first-person reports.",
 "Lilly's 'Rupert should never prevail over Essex' and 'nor did he' are separate forecast and authorial later retrospective claim, not independent blind predictive validation.",
 "A prospective forecast cannot be established from a retrospective book published later unless independent contemporary date-frozen prediction survives.",
 "A vague forecast of general hostility, respect or honor has no frozen scoring definition, population threshold or observation period.",
 "Rupert predicted at Parliament's full disposal/custody was a stronger outcome than being temporarily subject to political negotiation.",
 "The author expressly confesses 'an errour in part' and calls later events 'very near truth'; do not relabel this as exact hit.",
 "Lilly reports the 1646 Oxford siege and Rupert's later Oatlands movement: original history and agreement details require independent archival verification.",
 "Allowing Rupert to depart and his actual escape directly qualify or undermine a literal capture/discretion prediction.",
 "Lilly's claimed national fate overriding his private forecast is itself authorial admission of predictive limitation.",
 "Rupert/Essex war and Oxford events have no matched independent prospective forecast file or controls in this chapter.",
 "Following LXXXVI new Irish forces/Queen war chart on PDF489 is excluded except for navigation.",
 "No independent medical, military or historical outcome validation and no runtime model rule promotion are permitted from this documentary batch."
]
dump("UNRESOLVED_SOURCE_LIMITS.json",{"batch":"B04e","issues":[
 {"id":f"B04e-U{i:02}","issue":x} for i,x in enumerate(limits,1)]})
dump("CLAIM_LEDGER.json",{"batch":"B04e","status":"ORIGINAL_SOURCE_FIRST_PROVISIONAL",
 "source_annotations":72,"source_spans":11,"retained_source_uncertainties":len(limits),
 "prior_accepted_lilly":4954,"new_accepted":0,
 "authorial_partial_error_acknowledgements":sum(r["role"]=="authorial_error_admission" for r in rows),
 "pre_question_Edgehill_references_not_predictions":True,
 "independent_wartime_outcomes_verified":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0})
print(json.dumps({"batch":"B04e","draft_records":72,"spans":11,"limits":len(limits),"admitted":0}))
