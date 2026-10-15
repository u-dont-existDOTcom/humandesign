#!/usr/bin/env python3
"""Original William Lilly 1647 Book II chapter printed LIV (logical LXIV): Fish Stolen.
Historical documentary extraction only, not evidence of astrology's predictive power.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROWS=[]
SPANS=[]
def add(pages,label,*parts):
 sid=f"LXIV-S{len(SPANS)+1:03}"
 ids=[]
 for role,anchor,meaning,caveat in parts:
  rid=f"LXIV-C{len(ROWS)+1:03}"
  ids.append(rid)
  ROWS.append({
   "local_id":rid,"role":role,
   "chapter_logical":"LXIV" if role!="boundary" else "LXV_NAVIGATION_ONLY",
   "chapter_printed_original":"LIV" if role!="boundary" else "LXV",
   "original_pdf_pages":list(pages),"original_printed_pages":[p-34 for p in pages],
   "short_anchor_not_full_quote":anchor,
   "historical_source_paraphrase":meaning,
   "source_conditions_uncertainty":caveat,
   "global_record_number":None,"accepted_historical_documentary":False,
   "real_world_case_independently_authenticated":False,
   "empirical_predictive_outcome_validated":False,"runtime_rule_promoted":False
  })
 SPANS.append({"span_id":sid,"original_pdf_pages":list(pages),
  "source_label_not_quote":label,"mapped_local_ids":ids})
add([431],"Chapter title and original printed numbering",
 ("heading","CHAP. LIV. Fish Stolen.","A distinct section called Fish Stolen begins, printed with numeral LIV.","It follows LXIII in source order; logical position LXIV, do not conflate with earlier Buying and Selling chapter."),
 ("numbering_anomaly","printed LIV, sequential LXIV","The original numeral and sequential position differ.","Preserve both identifiers rather than silently correcting the source."))
add([431],"original fish-theft diagram and date",
 ("figure","square horoscope Fish Stolen","An original square twelve-house horoscope accompanies this question.","This is not the previous circular money theft figure."),
 ("figure_timestamp","10 Feb. 1638 8:45 A.M.","The diagram centre prints 10 February 1638, 8:45 AM.","Calendar and geographic time basis not independently authenticated."),
 ("figure_annotation","hor astr Jupiter","The chart carries an hour-ruler annotation involving Jupiter.","Keep original glyph and uncertainty; no ephemeris parity."))
add([431],"purchase and barge chronicle",
 ("historical_chronology","living in Country 1637; Fish for Lent","Lilly says he bought London fish while living in the country in 1637.","Historical chronology distinguished from figure year 1638."),
 ("historical_chronology","Walton boat delivery Saturday 10 February","The fish was brought by boat to Walton on 10 February.","Only original report, no independent consignment documents."),
 ("reported_event","Boatman said warehouse had been robbed","The author heard from a boatman that the warehouse had been robbed.","The news predates figure casting."),
 ("reported_event","my Fish stolen","He states that his fish had been stolen.","Thief identification remains disputed."))
add([431],"figure initiated after report and endpoints",
 ("figure_timestamp_origin","exact time first heard report","The author says he cast the horary at the precise moment he received news of loss.","No external prediction timestamp or independent witness."),
 ("question","what became Goods; recover part or all","He asks what happened to the missing fish and whether part or all could be recovered.","Different endpoints must not be pooled."),
 ("scope","first-person source-worked demonstration","This is a historical worked case with observations and eventual search.","Generalizations appear later before next numbered chapter."))
add([431],"Jupiter on seventh and absence of peregrine alternatives",
 ("condition","no peregrine Planet in angle but Jupiter","Lilly observes Jupiter as the only relevant peregrine planet in an angle.","Original original glyph and essential-dignity conditions matter."),
 ("condition","Jupiter on cusp seventh","Jupiter is said to be located at the seventh-house cusp.","Angle and cusp are distinct original source features."))
add([431],"water-sign dignities and proposed riverside suspect",
 ("condition","Jupiter in Scorpio moist Signe","Jupiter is described as occupying Scorpio, a moist sign.","Historic elemental classification; no modern causal inference."),
 ("condition","Mercury significator Goods in Pisces","Mercury as significator of goods is described as occupying Pisces.","Do not confuse goods-ruler with selected suspect significator Jupiter."),
 ("condition","Part Fortune in Cancer and Moon in Taurus","Part Fortune in Cancer and Moon in an earthy sign are invoked.","Authorial chart assertion only; independent ephemeris parity absent."),
 ("historical_inference","man whose calling was upon Water","Lilly infers that the person holding the goods worked on or around water.","A historical suspicion, not verified criminal evidence."),
 ("historical_inference","goods in moist place or low room","He infers a damp location or room near ground level.","Alternatives in a paragraph, not separately verified beforehand."))
add([431,432],"recovery hope from Moon, Mercury and Fortune",
 ("figure_condition","Mercury Lord second applied unto by sextile of Moon","Moon's sextile application to Mercury, second-house lord, is said to support hearing about goods.","Source does not claim immediate full recovery."),
 ("figure_condition","Moon Lady of Part Fortune","The Moon is tied to the Part of Fortune in the judgment.","Not a universally verified recovery indicator."),
 ("exception","Mercury in fall and detriment","The weak essential condition of Mercury reduces hopes of retrieving fish.","Explicit qualification; do not count full recovery."),
 ("exception","Mercury in own Terms","Mercury being in its own terms is presented as some mitigation.","Qualifying benefit does not erase fall/detriment."),
 ("figure_condition","trine to Part of Fortune","A trine with Part Fortune is added as recovery testimony.","Aspect belongs to source-native chart doctrine."),
 ("source_internal_forecast","hope of some of my Goods","Lilly says he expected information and some of the fish back, though not all.","A partial forecast, not unqualified full restitution."))
add([432],"investigating waterfront candidates",
 ("reported_investigation","no Walton Waterman matched Jupiter Scorpio","He says local boatmen failed to match the suspect description he inferred.","Failed initial search must not be omitted."),
 ("reported_investigation","examined Fishermen of that complexion","He then sought fishermen fitting the profile.","Search selection occurred after astrological interpretation; introduces investigator influence."))
add([432],"Mars seventh lord departure and suspected relocation",
 ("figure_assignment","Mars Lord seventh","Mars is treated as ruler of the seventh house for another part of the judgment.","Different from Jupiter on seventh cusp, with distinct interpretation."),
 ("figure_condition","Mars departing Scorpio, entering another Signe","Mars leaving Scorpio is interpreted as change of place.","The original speaks of Mars own sign; retain condition."),
 ("historical_inference","land sold or leaving proper house","Lilly uses this transition to suspect the person recently sold land or was moving residence.","Not shown independently before the subsequent inquiry."),
 ("reported_investigation","fisherman suspected departing habitation","He says he found a fisherman fitting the moving-residence possibility.","Investigative filtering influenced by prediction."),
 ("reported_location","lived near Thames side; conversant in waters","The suspect reportedly lived beside the Thames and worked as a fisherman.","Source allegation of involvement, not independently proven guilt."),
 ("historical_generalization","significators in watry Signs live near water","Lilly generalizes from watery signs to occupations or places near water.","A historical rule untested out of sample."))
add([432],"historical appearance profile applied to alleged fish holder",
 ("characterization","good stature, thick and full bodied","The suspected fisherman is described as substantial and full-bodied.","No independent anthropometric record."),
 ("characterization","fair complexion, red or yellowish hair","Lilly gives complexion and hair-color descriptions.","Source-native characterization, not verified identity or diagnostic evidence."))
add([432],"warrant, delayed search and recovered portions",
 ("reported_action","procured a Warrant from Justice of Peace","Lilly reports obtaining a legal warrant before the search.","Independent judicial documentation not supplied."),
 ("reported_chronology","Sunday eighteenth February following","He says the search occurred on Sunday 18 February, after the dated chart.","Chronology of investigation matters for interpreting reported outcomes."),
 ("reported_action","Constable and Barge-man searched one house","The author says he and companions searched only the chosen fisherman's house.","This is not a blind search of all comparable homes."),
 ("source_internal_outcome","part Fish in water, part eaten, part not consumed","He says some fish was found in water, some already eaten, and some still uneaten.","Partial recovery rather than complete recovery."),
 ("source_internal_outcome","all confessed","He asserts the people involved confessed in the search.","No external deposition or independent evidentiary record supplied."))
add([432],"fish and sack were separate lost articles",
 ("reported_loss","fish in a bag","Lilly says the fish had been contained in a bag.","Do not confuse fish recovery with return of the container."),
 ("reported_loss","bag taken together with Fish","He says the bag also went missing in the incident.","Separate loss/outcome: recovery not established at same level as fish."),
 ("reported_event","Barge-man whose sack said he recognized bag","A boatman is said to have noticed the sack at the searched home.","His awareness and earlier observation are disputed in original narrative."))
add([432],"bag statements and contested knowledge",
 ("reported_dialogue","woman never had a sack but husband's same night","The woman is reported as saying she had only a sack brought home by her husband that night.","Competing ownership/identification claims not independently adjudicated."),
 ("historical_allegation","woman washed sack clean","Lilly claims the bag had been washed, contributing to prior failure to recognize it.","Author interpretation, not independent proof of knowledge or concealment."),
 ("historical_dispute","boatman looked on sack many times, not knowing it","He asserts the boatman had seen the bag many times but did not recognize it because it was washed.","Do not conflate subjective recognition with independent chain of custody."))
add([432],"additional lost onions and alleged cooking",
 ("reported_loss","seven Portugall Onions lost","Lilly also says seven Portuguese onions had disappeared.","An additional item separate from fish and bag."),
 ("reported_dialogue","made pottage with Onions not knowing what they were","The woman reportedly admitted cooking the onions as pottage without recognizing them.","The asserted lack of knowledge must be preserved, not rewritten as intentional theft."))
add([432,433],"author final remittance and disputed compensation",
 ("source_internal_outcome","remainder of Fish freely remitted","The author says he forgave or relinquished the unrecovered remainder.","Retain as loss/nonrecovery rather than calling full restitution."),
 ("reported_dispute","Priest of Walton asserted satisfaction","He attributes to the local priest a claim that he had received satisfaction.","Third-party statement from the same author's narration, not independently verified."),
 ("historical_allegation","he never hurt himself with a lye","Lilly insinuates the priest was lying.","A historical accusation, not verified moral or criminal fact."))
add([433],"source conclusion about peregrine planets and first house",
 ("historical_generalization","peregrine Planet in angle describes Thiefe","Lilly generalizes that an angular peregrine planet describes the alleged thief.","Not independently tested; individual guilt cannot be inferred."),
 ("historical_generalization","Sun or Moon in ascendant in essential Dignities","He says Sun or Moon in the first house with essential dignity gives hope of identifying the person.","Both planetary placement and dignity are specified conditions."),
 ("historical_claim","assured hopes of discovering who it was","He characterizes these as assurances of discovery.","Author confidence wording, not measured probability."))
add([433],"conditional recovery outcomes and missing goods",
 ("historical_generalization","Moon apply to Lord second argues recovery","Applying Moon aspect to second-house lord is said to support recovering goods.","Original source says application, not merely any aspect."),
 ("conditional_outcome","full recovery if both essentially dignified","Complete recovery is associated with essential dignity of both Moon and second lord.","Must keep BOTH, and distinguish essential from accidental."),
 ("conditional_outcome","part if accidentally fortified","A partial return is predicted if they are accidentally fortified.","Source syntax needs preservation; no numeric threshold."),
 ("conditional_outcome","discovery no recovery if apply both peregrine","He says application between two peregrines can produce discovery without goods returned.","This is a negative case, essential to avoid cherry-picking the author's examples."))
add([433],"physical following chapter divider",
 ("boundary","CHAP. LXV. figure Waller and Hopton","A separate military horary chapter about Waller and Hopton begins below the divider on original PDF433.","Navigation-only; no Chapter LXV battle content included in Fish Stolen."))
assert len({r["local_id"] for r in ROWS})==len(ROWS)
assert [r["local_id"] for r in ROWS]==[f"LXIV-C{i:03}" for i in range(1,len(ROWS)+1)]
assert SPANS[0]["original_pdf_pages"]==[431]
assert SPANS[-1]["original_pdf_pages"]==[433]
assert [s["original_pdf_pages"][0] for s in SPANS]==sorted(s["original_pdf_pages"][0] for s in SPANS)
assert ROWS[-1]["chapter_logical"]=="LXV_NAVIGATION_ONLY"
def dump(f,x):
 (B/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
images=[]
for page in [431,432,433]:
 path=B/"evidence"/f"pdf_1647-{page}.jpg";data=path.read_bytes()
 images.append({"pdf_page":page,"printed_page":page-34,
  "path":path.relative_to(B).as_posix(),"bytes":len(data),
  "sha256":hashlib.sha256(data).hexdigest()})
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B03j","status":"ORIGINAL_SOURCE_FIRST_PROVISIONAL_UNACCEPTED",
 "source_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "printed_chapter_numeral":"LIV","logical_chapter_position":"LXIV",
 "source_units":len(ROWS),"independent_case_outcome_verified":False,"rows":ROWS})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B03j","status":"PROVISIONAL_MANUAL_SOURCE_TO_CLAUSE_MAP",
 "source_spans":SPANS,"span_count":len(SPANS),"source_units":len(ROWS),
 "original_body_pages":[431,432,433],"source_cross_page_clause_sets":sum(len(x["original_pdf_pages"])>1 for x in SPANS),
 "complete_independent_diplomatic_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{
 "batch":"B03j","status":"PROVISIONAL",
 "ordered_local_ids":[r["local_id"] for r in ROWS],
 "cross_page_local_ids":[r["local_id"] for r in ROWS if len(r["original_pdf_pages"])>1],
 "next_heading_only":ROWS[-1]["local_id"]})
dump("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B03j","status":"PROVISIONAL_ORIGINAL_1647_SOURCE_ONLY",
 "source_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "previous_accepted_lilly":3571,
 "original_body_pdf_pages":[431,432,433],
 "opening":"PDF431 top distinct Fish Stolen heading, printed CHAP LIV, logical LXIV",
 "closing":"PDF433 ABOVE following Chapter LXV divider",
 "original_images":images,
 "printed_heading_literal":"LIV","sequential_chapter_identity":"LXIV",
 "chart_printed_date":"10 February 1638","chart_printed_clock":"8:45 AM",
 "following_chapter_printed":"LXV","following_heading_pdf":433,
 "source_case_independently_authenticated":False,
 "blind_complete_second_diplomatic_transcription":False})
limits=[
 ("PDF431","Printed numeral LIV in Fish Stolen conflicts with logical sequence LXIV and earlier correctly printed LIV Buying and Selling; preserve all identities."),
 ("PDF431","Historical prose mentions the country in 1637 while chart reads February 1638, potentially Old Style chronology; do not convert without independent evidence."),
 ("PDF431 figure","Original square chart 10 February 1638 8:45 AM lacks independently verified civil calendar, clock, location or ephemeris parity."),
 ("PDF431","Original glyphs and Jupiter seventh-cusp/watery-sign rationale need image-backed reading, not algorithmic assumptions."),
 ("PDF431","Part of Fortune in Cancer and Moon earthy-sign contribution do not uniquely diagnose low room or exact residence."),
 ("PDF431-432","Hope of hearing about goods and some partial recovery is different from complete physical restitution."),
 ("PDF432","Source explicitly describes Mercury in fall/detriment and separately in own terms; mitigations must not remove negatives."),
 ("PDF432","Initial search found no boatman fitting proposed description; report this miss rather than counting only eventual finding."),
 ("PDF432","Investigative selection of a moving fisherman after interpreting Mars seventh-lord sign change creates retrospective confirmation risk."),
 ("PDF432","Watery occupations, riverside place, clothing or hair characteristics are historical narratives not independent evidence of theft or personality."),
 ("PDF432","Warrant, constable search, confession and physical goods are all narrated by Lilly with no archived external testimony or inventory."),
 ("PDF432","Partial fish discovered in water, portions eaten and portions intact are not full recovery; no independent numeric fraction given."),
 ("PDF432","Bag loss and boatman/housewife recognition disputes are not resolved by fish recovery."),
 ("PDF432","Seven Portugal onions cooked into pottage are a separate reportedly lost item with uncertain restitution and reported lack of knowledge."),
 ("PDF432-433","Author voluntarily remitted remaining fish; this is an explicit nonrecovered outcome, not hidden as success."),
 ("PDF433","Author calls local priest a liar; historical accusation must not be presented as verified character or guilt."),
 ("PDF433","General Moon/second lord application outcomes distinguish full essential dignity, partial accidental strength and discovery with no recovery when both peregrine."),
 ("PDF433","Next printed Chapter LXV military worked case begins below divider and is NOT Fish Stolen source content."),
 ("PDF431-433","The source supports historical author-reported events, not blinded independently corroborated astrological predictive validation."),
 ("PDF431-433","Source-first editorial paraphrases are not an independently blinded complete diplomatic transcription.")
]
dump("UNRESOLVED_SOURCE_LIMITS.json",{
 "batch":"B03j","status":"PROVISIONAL_RETAIN_UNRESOLVED",
 "issues":[{"id":f"B03j-U{i:02}","source":a,"issue":b} for i,(a,b) in enumerate(limits,1)]})
dump("CLAIM_LEDGER.json",{
 "batch":"B03j","kind":"LILLY_1647_HISTORICAL_FISH_THEFT_WORKED_CASE_ONLY",
 "status":"SOURCE_FIRST_PROVISIONAL_NOT_ADMITTED",
 "editorial_source_units":len(ROWS),"original_visual_source_spans":len(SPANS),
 "previous_accepted_lilly":3571,"new_globally_accepted_source_units":0,
 "source_author_reported_partially_recovered_fish_case_count":1,
 "source_author_reported_full_recovery_case_count":0,
 "fish_remaining_written_off_by_author":True,
 "independent_evidence_of_recovery":0,
 "independent_evidence_of_thief_identity":0,
 "new_empirically_validated_astrology_predictions":0,
 "new_runtime_model_changes":0})
print(json.dumps({"batch":"B03j","rows":len(ROWS),"spans":len(SPANS),
 "issues":len(limits),"original_source_pdf_pages":[431,432,433],
 "printed_heading":"LIV","logical_chapter":"LXIV","new_canonical_units":0}))
