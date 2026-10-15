#!/usr/bin/env python3
"""Source-first William Lilly Chapter LXII. Historical documentary only."""
from pathlib import Path
import hashlib, json
B=Path(__file__).resolve().parent
rows=[]
spans=[]
def add(pages,label,*claims):
    sid=f"LXII-S{len(spans)+1:03}"
    ids=[]
    for role,anchor,meaning,limit in claims:
        rid=f"LXII-C{len(rows)+1:03}"
        ids.append(rid)
        rows.append({"local_id":rid,"role":role,"chapter":"LXII" if role!="boundary" else "LXIII_BOUNDARY_ONLY",
            "original_pdf_pages":list(pages),"printed_pages":[p-34 for p in pages],
            "short_source_anchor_not_diplomatic":anchor,"source_paraphrase":meaning,
            "qualifiers_and_unresolved":limit,"global_record_number":None,
            "empirical_case_verified":False,"historical_documentary_admitted":False})
    spans.append({"span_id":sid,"original_pdf_pages":list(pages),"label":label,"mapped_local_ids":ids})
add([426],"own heading/horoscope below LXI divider",
 ("heading","CHAP LXII A Dogge missing","A separate numbered missing-dog question starts below the Chapter LXI divider","No preceding servant-case records"),
 ("figure","original square horoscope 29 Aug 1646","A distinct original square horoscope is printed under the missing-dog title","No independent modern chart calculation"),
 ("figure_date","29 Aug 1646 4:5 PM","The figure gives 29 August 1646, with a 4:5 PM time inscription","Calendar style and clock notation not independently reconciled"))
add([426,427],"original judgment opening across page boundary",
 ("subheading","Judgment upon this preceding Figure","The author starts the original judgment of the missing dog figure","This paragraph crosses original PDF426-427"),
 ("context","Living in London few small Cattles","The author explains why a missing dog supplies a small-animal example in London","Not a representative sample of farm animals"))
add([427],"reported question and dog category",
 ("question","a Dogge fled and missing","The dog had gone missing from its owner","Source-internal historical narrative"),
 ("question","what part of City search","The owner asked what area of London to search and whether it could be recovered","No independently frozen original question document"))
add([427],"owner significators and attributed traits",
 ("assignment","querent signe ascending Lord thereof","The dog owner is represented by the first house and its lord","Distinct from sixth-house dog"),
 ("characterization","Saturnine ... Cauda in ascendant","The author assigns Saturnine characteristics to the owner","Unverified person-level characterization"),
 ("characterization","deformed ... covetous","The author describes bodily deformity and great covetousness","Historical allegation, not empirical validation"))
add([427],"small animal house and alternative examples",
 ("assignment","Signe of sixt and Lord signifies Dogge","The sixth house and its ruler are assigned to the missing dog","No modern pet-location predictive validation"),
 ("scope","Sheep Hogges Coneys small Cattle","The author would treat other small animals similarly","Analogy only"))
add([427],"original directional testimonies",
 ("condition","Gemini is West and by South","The ascendant sign Gemini is associated with west-by-south","Compass language from original period"),
 ("condition","quarter of heaven West","The chart quarter contributes a westerly testimony","Not numeric bearing"),
 ("condition","Mercury Dogge Libra a Western Sign","Mercury in Libra is treated as dog significator in a western sign, southern heaven quadrant","Sign and quarter differ"),
 ("condition","Moon in Virgo a South-west Sign","Moon in Virgo contributes a southwesterly direction toward west angle","Distinct from Mercury"))
add([427],"nearby street locality and confirmatory aspects",
 ("forecast","plurality signifies West","The author judged that the missing animal was west of the home","Author narrated rather than independently witnessed prediction"),
 ("forecast","Temple-bar ... Long-acre or Drury-lane","The owner was at Temple-bar; Long-acre or upper Drury Lane was named as dog location","Place prediction lacks independently frozen timestamp"),
 ("condition","Mercury same Triplicity Gemini","Mercury's sign and Gemini rising share the cited triplicity","No independent ephemeris parity"),
 ("condition","Mercury applying trine cusp sixth","The dog significator applies to a trine of the sixth-house cusp","House-cusp aspect is not planet conjunction"),
 ("forecast","same quarter lines of Communication","The author thought the animal remained in the same urban quarter","Historical spatial vocabulary"),
 ("condition","Sun and Saturn trine","A Sun-Saturn trine is cited as corroboration","No modern score supplied"))
add([427],"indoor location and concealment",
 ("condition","Mercury Libra an airy signe","An airy Libra sign is used in the location interpretation","Astrological symbolism"),
 ("forecast","chamber or upper room ... secretly","The author judged an indoor or upper-room and private location","Reported finding under a table does not prove the upper-room part"),
 ("condition","Moon under beams of Sun","Moon under Sun's beams is associated with secrecy","No orb independently verified"),
 ("condition","Mercury Moon Sun eighth house","The planets are said to be in eighth house","Chart glyphs not reconstructed"))
add([427],"Monday aspects and qualified forecast",
 ("condition","Sun Monday dexter trine Saturn","Sun trine Saturn ascendant ruler is presented as Monday aspect","Period astrology geometry unverified"),
 ("condition","Moon sextile Mars","Moon to Mars sextile is cited independently","Do not conflate with solar trine"),
 ("forecast","Dog or news Monday or near","Dog return OR news is predicted on or near Monday","Alternative outcomes retained"))
add([427,428],"acquaintance finding the dog, reported as successful",
 ("reported_outcome","which was true acquaintance","An acquaintance reportedly found the missing dog","No independent corroboration"),
 ("reported_location","Long-acre under a table","The dog was allegedly found chained under a table in Long-acre","Does not establish prior upper-room prediction"),
 ("reported_outcome","sent home same day about ten","Lilly reports the dog was returned that Monday at about 10 AM","No external time-stamped event documentation"))
add([428],"author self-assessment and reservations",
 ("author_evaluation","my very great credit","The author praises his own apparent success","Self-assessment not validation"),
 ("author_caveat","cannot endure Fugitives or Thefts","He expresses reservations about such consultations","Belongs above Chapter LXIII divider"),
 ("author_intent","benefit Posterity","He states he supplied the case for later readers","Intent is source-internal"))
add([428],"unnumbered fugitive movement generalizations",
 ("generalization","all Fugitives go by Moon as varies her Sign","The Moon's sign changes are associated with movements of fugitives","Unverified source hypothesis"),
 ("generalization","East West North or South","The author describes possible changes in travel direction","No modern tracking applicability"))
add([428],"strength and resemblance method before physical boundary",
 ("procedure","compare Significator and Moon","Readers are instructed to compare strength of the fugitive planet and Moon","Historically defined fortitudes"),
 ("procedure","judge by stronger","The stronger of the two is prioritized","No numeric weighting given"),
 ("exception","if equivalent Fortitudes","Where strengths tie, choose by how well planet describes fugitive","Subjective condition"),
 ("exception","Moon if most resemble him","Moon may instead be chosen for closer resemblance","No deterministic individual evidence"),
 ("condition","nearest aspect relevant house cusp","Aspect to cusp is an additional comparison","No specified orb or timing tolerance"))
add([428],"next chapter boundary",
 ("boundary","CHAP LXIII Of Theft","A separate theft chapter opens beneath original PDF428 divider","No theft content imported"))
assert len(set(r['local_id'] for r in rows))==len(rows)
assert [r['local_id'] for r in rows]==[f"LXII-C{i:03}" for i in range(1,len(rows)+1)]
assert spans[0]['original_pdf_pages']==[426] and spans[-1]['original_pdf_pages']==[428]
assert [x['original_pdf_pages'][0] for x in spans]==sorted(x['original_pdf_pages'][0] for x in spans)
def dump(name,data):
    (B/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
images=[]
for n in (426,427,428):
    img=B/"evidence"/f"pdf_1647-{n}.jpg"
    raw=img.read_bytes()
    images.append({"pdf_page":n,"printed_page":n-34,
        "path":img.relative_to(B).as_posix(),
        "bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
    "batch":"B03h","status":"PROVISIONAL_DOCUMENTARY_SOURCE_FIRST",
    "original_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
    "source_units":len(rows),"real_case_verified":False,"rows":rows})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
    "batch":"B03h","status":"MANUAL_ORIGINAL_IMAGE_TO_DRAFT",
    "source_spans":spans,"span_count":len(spans),"source_units":len(rows),
    "original_pages":[426,427,428],"independent_diplomatic_transcription_done":False})
dump("SOURCE_WINDOW_MANIFEST.json",{
    "batch":"B03h","status":"PROVISIONAL",
    "original_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
    "physical_body_pages":[426,427,428],
    "opening":"PDF426 below Chapter LXI divider",
    "closing":"PDF428 above Chapter LXIII divider",
    "source_images":images,"previous_lilly":3484,
    "blind_second_original_reader":False})
dump("SOURCE_ORDER_DRAFT.json",{
    "batch":"B03h","ordered_ids":[r['local_id'] for r in rows],
    "cross_page_ids":[r['local_id'] for r in rows if len(r['original_pdf_pages'])>1],
    "next_heading_only":rows[-1]['local_id']})
limits=[
 "Dog case is separate from servant case on same source page",
 "Printed 29 Aug 1646 4:5 PM time lacks proven timezone/calendar conversion",
 "Urban dog is a selected example, not a random animal population",
 "Saturnine, deformed, greedy owner descriptions are unverified person claims",
 "Signs Gemini/Libra/Virgo and heaven quadrants supply distinct directions",
 "Mercury triplicity, cusp trine and Sun-Saturn trine lack independent ephemeris parity",
 "Predicted upper room is not demonstrated by reported under-table finding",
 "Secrecy and high floor are separate outcomes and must not be pooled",
 "Dog OR news on or near Monday is not an exact unqualified dog return rule",
 "Long-acre location and dog return are only self-reported in Lilly narrative",
 "No independent calendar parity, original forecast freeze or outcome witness",
 "Lilly’s great credit is authorial self-evaluation, not scientific validation",
 "Unheaded general fugitive maxims precede LXIII divider and belong to LXII",
 "Stronger planet versus Moon and subjective resemblance tie is not deterministic",
 "Nearest aspect to house cusp has no numerical tolerance or uniqueness guarantee",
 "Theft chapter LXIII starts below divider; only heading marker counted",
 "No blind independent transcription or external case verification"]
dump("UNRESOLVED_SOURCE_LIMITS.json",{
 "batch":"B03h","status":"RETAIN_UNRESOLVED",
 "issues":[{"id":f"B03h-U{i:02d}","issue":text} for i,text in enumerate(limits,1)]})
dump("CLAIM_LEDGER.json",{
 "batch":"B03h","status":"PROVISIONAL_HISTORICAL_DOCUMENTARY_ONLY",
 "source_first_annotations":len(rows),"original_passages":len(spans),
 "prior_accepted_lilly":3484,"globally_added":0,
 "historical_author_narrated_dog_return":1,
 "independently_authenticated_cases":0,"new_empirical_predictions":0,
 "model_runtime_promotions":0})
print(json.dumps({"batch":"B03h","source_units":len(rows),
 "source_spans":len(spans),"original_pages":[426,427,428],"accepted_units":0}))
