"""Append truly omitted source clauses and headings; preserve all prior stable IDs.

Requires both A and B fixed originals. Missing source units are NOT additional
observed outcomes. Explicit anchor order is created for next phase deduplication.
"""
from pathlib import Path
import json,copy,shutil
B=Path(__file__).resolve().parent
back=B/"recovery"/"before_missing_review_b"
assert not (back/"PHASE1_RULES_DRAFT.json").exists(),"Additions already processed; inspect state"
back.mkdir(parents=True,exist_ok=True)
shutil.copy2(B/"PHASE1_RULES_DRAFT.json",back/"PHASE1_RULES_DRAFT.json")
p=B/"PHASE1_RULES_DRAFT.json"
D=json.loads(p.read_text())
assert D["record_count"]==len(D["rules"])==148
R={x["record_number"]:x for x in D["rules"]}
assert max(R)==2285
def add(kind,s,pages,after,pre,limits):
 assert kind not in {x["source_record_kind"] for x in R.values()},kind
 n=max(R)+1
 x=copy.deepcopy(R[2139])
 x.update(id=f"LI.1647.II.L.PHASE1.R{n}",record_number=n,
  source_record_kind=kind,source_statement=s,
  preconditions=[pre],exceptions_and_evidence_limits=[limits],
  source_draft_part="INDEPENDENT_B_MISSING_SOURCE_UNIT",
  source_review_inserted=True,source_order_after=after)
 x["source_locator"]={"pdf_pages":pages,
  "printed_pages":[v-34 for v in pages],
  "page_images":[f"evidence/pdf-{v}.png" for v in pages],
  "source_statement_is_verbatim":False}
 R[n]=x
 return n
items=[
 ("lost_goods_same_quadrant_town_hundred",
  "For a lost thing the SIGNIFICATOR OF THE THING or MOON in SAME QUADRANT as the querent is said to place it within same TOWN or HUNDRED.",
  [360],2211,"Same quadrant for thing's significator OR Moon and querent.","Historical 'Hundred' is jurisdiction/district, not 100 metres or modern distance."),
 ("pound_saturn_four_house_stay",
  "SATURN in FIRST, FOURTH, EIGHTH OR TWELFTH is said to signify cattle LONG IN POUND, without repeating the earlier unfortunate-status clause.",
  [361,362],2227,"Saturn occupies any of FOUR named houses.","This can contradict the separate ascendant lord IN EIGHTH mortality claim; do not silently unify."),
 ("pound_twelfth_ruler_and_beast_unfortunate",
  "When TWELFTH LORD AND PRINCIPAL BEAST SIGNIFICATOR are both UNFORTUNATE, cattle are said to be in POUND or obscured in PRIVATE/CLOSE place.",
  [361],2225,"Twelfth lord and principal animal significator both unfortunate.","Do not confuse with Moon IN twelfth 'what signification soever' or Moon unfortunate."),
 ("sixth_beholds_moon_soft",
  "SIXTH LORD BEHOLDING MOON OR MOON'S HOUSE LORD by SEXTILE OR TRINE is offered as an alternate route for cattle RECOVERED.",
  [362],2232,"Sixth lord acts on Moon or her house lord with a favourable aspect.","This differs from aspect to first lord, already recorded in R2232."),
 ("sixth_beholds_moon_hard",
  "SIXTH LORD BEHOLDING MOON OR MOON'S HOUSE LORD by SQUARE OR OPPOSITION is said to leave cattle STOPPED or STAYED in a VILLAGE OR TOWN.",
  [362],2232,"Sixth lord's aspect target is lunar Moon or domicile lord; hard aspect.","Historical claimed custody; not a real farm-animal event."),
 ("airy_cadent_left_going_farther",
  "With SIXTH LORD in AIRY sign and CADENT house, the beasts are said to be on LEFT and GOING AWAY, 'Straying further from their right Owner'.",
  [360,361],2218,"Sixth-house lord AIRY and CADENT.","This is not a westward outcome, unlike angular and succedent branches."),
 ("watery_angular_north",
  "With SIXTH LORD in WATERY sign and ANGLE, cattle are said to lie in CLOSE GROUND NORTH.",
  [361],2219,"Watery sixth lord angular.","Not same as wet meadows/cadent branch."),
 ("watery_succedent_north",
  "With SIXTH LORD in WATERY sign and SUCCEDENT house, cattle are said to be to RIGHT HAND NORTH.",
  [361],2219,"Watery sixth lord succedent.","Not the angular or cadent result."),
 ("watery_cadent_meadows",
  "With SIXTH LORD in WATERY sign and CADENT house, cattle are said to be on LEFT COMMON where WATER, MEADOWS or cattle WATERING places occur.",
  [361],2219,"Watery sixth lord cadent.","The water-meadows details belong specifically to this branch."),
 ("which_way_source_heading",
  "Printed heading 'WHICH WAY' introduces sixth-lord fiery/earthy/airy/watery directional and angularity tests.",
  [360],2216,"Structural printed heading.","No independently witnessed recovery event."),
 ("in_what_place_source_heading",
  "Printed heading 'IN WHAT PLACE THEY ARE' begins sixth-lord angular/succedent/cadent location conditions.",
  [360],2215,"Structural printed heading.","Not a separate location success."),
 ("long_in_pound_heading",
  "Printed heading 'LONG IN POUND' introduces multiple Saturn/Moon custody conditions, and a later unqualified Saturn four-house clause.",
  [361],2226,"Printed unnumbered section.","Not a new observed livestock case."),
 ("fugitive_of_moon_heading",
  "Printed heading 'OF THE MOON' introduces Moon as the NATURAL SIGNIFICATRIX of FUGITIVE.",
  [362],2236,"Printed section, distinct from initial querent-lord/Sun paragraph.","Not a new or independently observed fugitive."),
 ("fugitive_whether_taken_heading",
  "Printed heading 'WHETHER HE SHALL BE TAKEN' introduces capture versus detention based on seventh lord and infortune angularity.",
  [363],2242,"Another original section after lunar general indicators.","Preserve forced vs voluntary outcomes.")
]
for item in items:add(*item)
D["rules"]=list(R.values())
D["record_count"]=len(R)
D["provisional_end"]=f"R{max(R)}"
D["status"]="REVIEW_A_AND_B_REPAIRED_SOURCE_DRAFT_NOT_ACCEPTED"
D["original_pre_review_draft_count"]=129
D["source_review_added_documentary_units"]=len(R)-129
D["chapter_L_fully_complete"]=False
p.write_text(json.dumps(D,indent=2,ensure_ascii=False)+"\n")
# Stable source appearance order, separate from contiguous stable source IDs.
order=list(range(2138,2267))
for n in range(2267,max(R)+1):
 anchor=R[n].get("source_order_after")
 assert isinstance(anchor,int) and anchor in order,(n,anchor)
 j=order.index(anchor)
 while j+1<len(order) and order[j+1]>2266 and R[order[j+1]].get("source_order_after")==anchor:
  j+=1
 order.insert(j+1,n)
assert len(order)==len(set(order))==len(R)
d={"batch":"B02t","phase":"1","status":"EDITORIAL_SOURCE_ORDER_NOT_ORIGINAL_NUMBERED_APHORISMS",
  "ids":order,"source_ids_stable_sorted":[r["record_number"] for r in D["rules"]],
  "source_order_not_evidence":True,
  "overlapping_original_pdf_364_boundary":True}
(B/"SOURCE_ORDER.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"source_only_units":len(R),"additions_from_first_129":len(R)-129,
                  "review_B_missing_units":len(items),"last_id":D["provisional_end"],
                  "all_L_complete":False,"source_order":len(order)}))
