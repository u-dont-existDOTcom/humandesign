#!/usr/bin/env python3
"""Original Lilly Book II LXXX text-first source inventory; not predictive validation."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
def J(name):return json.loads((B/name).read_text(encoding="utf-8"))
def dump(name,obj):(B/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
A=J("SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json")
P=J("SOURCE_WINDOW_PROVISIONAL_20261016.json")
assert A["source_spans"]==len(A["source_groups"])==13
assert A["source_units"]==sum(len(g["claims"]) for g in A["source_groups"])==82
assert P["previous_authenticated_lilly_count"]==4549 and P["new_accepted_documentary_records"]==0
rows=[];spans=[]
for group in A["source_groups"]:
    span_id=f"LXXX-S{len(spans)+1:03}"
    ids=[]
    for claim in group["claims"]:
        assert len(claim) in (4,5)
        role,anchor,paraphrase,qualification=claim[:4]
        pages=claim[4] if len(claim)==5 else group["pages"]
        assert set(pages).issubset(set(group["pages"]))
        assert role and anchor and paraphrase and qualification
        sid=f"LXXX-C{len(rows)+1:03}";ids.append(sid)
        rows.append({"source_local_id":sid,"batch":"B03z","role":role,
         "chapter":"LXXX" if role!="next_navigation" else "LXXXI_NAVIGATION_ONLY",
         "original_pdf_pages":pages,"printed_pages":[n-34 for n in pages],
         "source_span_id":span_id,"short_original_anchor_not_diplomatic":anchor,
         "historical_author_paraphrase":paraphrase,
         "original_source_qualifications":qualification,
         "global_record_number":None,"historical_documentary_accepted":False,
         "independently_authenticated_religious_political_outcome":False,
         "empirically_validated_prediction":False,"runtime_model_promoted":False})
    spans.append({"span_id":span_id,"original_pdf_pages":group["pages"],
        "passage_label":group["label"],"mapped_local_ids":ids})
assert len(rows)==82 and len(spans)==13
assert all(r["chapter"]=="LXXX" for r in rows[:-2])
assert all(r["chapter"]=="LXXXI_NAVIGATION_ONLY" for r in rows[-2:])
assert sum(len(x["mapped_local_ids"]) for x in spans)==82
assert [r["source_local_id"] for r in rows]==[f"LXXX-C{i:03}" for i in range(1,83)]
full=P["original_full_pdf_sha256"]
print_date=P["opening_figure_date_printed"]
imgs=P["original_page_images"]
for img in imgs:
    f=B/img["path"]; raw=f.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==img["sha256"]
    assert len(raw)==img["bytes"]
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B03z","status":"ORIGINAL_1647_SOURCE_FIRST_PROVISIONAL",
 "original_full_pdf_sha256":full,"source_units":82,
 "content_chapter":"LXXX","printed_chart_dual_year":print_date,
 "real_events_externally_authenticated":False,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B03z","source_spans":spans,"span_count":13,
 "mapped_source_units":82,"original_body_pdf_pages":[473,474,475,476],
 "following_heading_pdf":476,"independent_second_diplomatic_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{
 "batch":"B03z","ordered_ids":[r["source_local_id"] for r in rows],
 "cross_page_ids":[r["source_local_id"] for r in rows if len(r["original_pdf_pages"])>1],
 "next_heading_navigation_only":[r["source_local_id"] for r in rows[-2:]]})
dump("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B03z","original_full_pdf_sha256":full,"original_images":imgs,
 "original_body_pdf_pages":[473,474,475,476],
 "following_heading_pdf":476,"next_numbered_chapter":"LXXXI",
 "previous_accepted_lilly":4549,"next_global_record":4550,
 "source_begin":"Original PDF473/printed439 Chapter LXXX",
 "source_end":"Original PDF476/printed442 ABOVE LXXXI divider",
 "separate_next_figure":"27 May 1647 10:45 AM",
 "printed_chart_date":"11 March 1646 over 7, 4:45 PM",
 "real_events_independently_verified":0})
limits=[
 "LXXX is a public-political question about 1640s English Presbytery, not a modern empirical political prediction study.",
 "Original horary chart prints 11 March 1646 over 7; English Old Style dual-year date has not been silently normalized.",
 "Original first-edition figure geometry, cusp positions, dignities, houses, aspects and planetary motion have not been independently recalculated.",
 "Mutable angles and fixed Taurus ninth are distinct chart features, not contradictory conditions.",
 "Saturn's ninth-house location and Jupiter's general religion attribution are distinct source mechanisms.",
 "Jupiter's retrograde station, ingress through Cancer/Leo, Saturn bounds, troublesome fixed stars and Mercury bounds are a conditional sequence; no independent ephemeris parity.",
 "Venus is both lady of the ninth and in Aries eighth, twelfth by derivation from Taurus; do not assume the Venus return to Taurus actually happened within forecast window.",
 "The Venus square-with-Jupiter then square-with-Mars passage is astrologically specialized and full independent diplomatic glyph transcription is outstanding.",
 "Lilly says significant effect from squares would require Saturn stronger, or monastic/novel religious-order circumstances; preserve conditional branches rather than turning into firm forecast.",
 "Only Jupiter essentially dignified is an author's source judgment; planetary fall/detriment and Moon via combusta require period rulebook and independent chart calculation.",
 "Moon separates from Venus, is subsequently void of course, then squares Mars and Jupiter; chronological aspect sequence is central.",
 "The author explicitly says his judgment is conjectural, not positive or affirmative; preserve this qualification even where later prose sounds certain.",
 "Saturn harshness and English temperament, younger/elder clergy motives and moral accusations are the author's interpretation, not observed personality evidence.",
 "Clergy opposition, gentry opposition, popular opposition, soldier action and new governance are distinct proposed outcomes and may overlap or conflict.",
 "The author offers alternatives to abolition: change in discipline, popular acceptability, primitive purity, or moderated demands.",
 "Three whole years from hence is a bounded timing claim referenced to the dual-year chart date; exact historical endpoint not specified.",
 "The term statu quo qualifies noncontinuance: cannot automatically score the source as forecasting disappearance of all Presbyterian practice.",
 "Fiscal contribution withholding and military denial of obedience are distinguishable events requiring independent primary sources to validate.",
 "The author invokes divine Providence or civil Authority as possible actors, so a retrospective match has large interpretive flexibility.",
 "Historical English constitutional and religious outcomes have not been sourced or tested in an independent blinded chronology for this batch.",
 "No independently confirmed contemporaneous prediction deposit, fixed event-scoring rule, unexposed follow-up, control base rate or calibration.",
 "Following LXXXI philosopher's stone square chart on PDF476 is separate; no navigational material may be treated as LXXX astronomical premise.",
 "Presbytery description expresses Lilly's normative view and should not be generalized to present-day Presbyterian people or institutions.",
 "All historical text records are documentary-only; no runtime rule promotions or empirically validated forecasts."
]
dump("UNRESOLVED_SOURCE_LIMITS.json",{"batch":"B03z","status":"ORIGINAL_SOURCE_LIMITATIONS",
 "issues":[{"id":f"B03z-U{i:02}","issue":s} for i,s in enumerate(limits,1)]})
dump("CLAIM_LEDGER.json",{
 "batch":"B03z","status":"PROVISIONAL_NOT_CANONICAL",
 "source_units":82,"source_span_groups":13,"source_issues":len(limits),
 "previous_authenticated_lilly_count":4549,
 "new_accepted_historical_documentary_records":0,
 "source_internal_timing_forecasts":sum(r["role"]=="source_internal_forecast" for r in rows),
 "historically_independently_verified_outcomes":0,
 "independently_validated_predictive_results":0,
 "runtime_model_promotions":0})
print(json.dumps({"batch":"B03z","draft_units":len(rows),"spans":len(spans),
 "issues":len(limits),"next":"LXXXI original PDF476","accepted":0}))
