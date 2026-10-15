#!/usr/bin/env python3
"""Source-first documentary transcription map: Lilly Book II Chapter LIII, original 1647.
Every row is an editorial source assertion, NOT empirical support, an astrology algorithm,
a medical/legal recommendation, or a complete diplomatic transcription.
No original 141MB PDF, participant records, or private data are included.
"""
import hashlib
import json
import pathlib

P = pathlib.Path(__file__).resolve().parent
ROWS = []
SPANS = []

def entry(pages, label, *units):
    """Add one contiguous original passage, with one or more distinct editorial units.
    Unit fields: role, short source anchor, conservative paraphrase, limitation/condition.
    """
    span_id = f"LIII-S{len(SPANS)+1:03}"
    ids = []
    for role, anchor, sense, cond in units:
        rid = f"LIII-C{len(ROWS)+1:03}"
        ids.append(rid)
        ROWS.append({
            "local_id":rid,"global_record_number":None,"batch":"B02y",
            "source":"William Lilly Christian Astrology 1647 original Wellcome b30338724",
            "book":"II", "chapter":"LIII" if role != "next_heading_boundary" else "LIV_HEADING_NAVIGATION_ONLY",
            "original_pdf_pages":list(pages),"original_printed_pages":[x-34 for x in pages],
            "source_anchor_editorial_abbreviation":anchor,
            "source_anchor_claimed_word_for_word_complete":False,
            "source_statement_paraphrase":sense,
            "source_predicates_and_qualifiers":cond,
            "record_role":role,
            "source_original_image_is_authoritative":True,
            "is_provisional":True,"accepted_historical_documentary":False,
            "empirically_verified_case":False,
            "model_runtime_promotion":False,
            "safe_for_real_person_prognosis":False
        })
    SPANS.append({
        "span_id":span_id,"original_pdf_pages":list(pages),
        "original_printed_pages":[x-34 for x in pages],
        "source_anchor_as_descriptive_label_not_full_quote":label,
        "draft_local_ids":ids
    })

entry([405],"chapter LIII and Hunting opening below divider",
 ("heading","CHAP. LIII. Of Hunting.","The Chapter LIII heading opens below LII's divider on original PDF405, printed page 371.","Do not ascribe the above-divider LII relocation text to this chapter."))
entry([405],"contemporaneous marginal aside on the hunting material",
 ("marginal_author_note","Sith the Ancients have taken notice of such trifles, I must consent.","The printed marginalia characterize this subject as a traditional minor topic.","An authorial aside, not an operational astrological prediction."))
entry([405],"hunting significators and hour condition",
 ("assignment","lord of hunting by the ascendant, the Moon","Hunting is considered using the ascendant, Moon and their associated significations.","The text additionally mentions the lord of the Moon-degree's term and the lord of the hour."),
 ("assignment","lord of the terme of the degree of the Moon, and ... lord of the hour","The lord of the lunar degree's term and lord of the hour are specifically named.","Do not replace the hour lord with a convenient substitute."),
 ("condition","the lord of the hour is of great force ... in the ascendant","Lilly adds special force to the hour lord when in the ascendant.","Scope: hunting judgment; hour lord positional requirement retained."))
entry([405,406],"four-footed and earthly signs; condition crossing the 371-372 seam",
 ("condition","ascendant a signe of four footed beasts","For four-footed quarry Lilly says to look for four-footed/earthly ascending signs.","Qualified to the hunted animal and place, not a universal success rule."),
 ("condition","good for hunting amongst mountaines, and hils","Earthly/four-footed signs are especially indicated for mountain/hill hunting.","Retain the specific terrain and quarry conditions."),
 ("condition","behold the lord of the ascendant, and the lord of the hour","Assess those two lords' fortune, infortune, aspects, separation and whether one falls from the other.","The paragraph starts on PDF405 and continues on PDF406; not a single unqualified yes/no."))
entry([406],"seventh-house sign and Lord of Hour outcomes",
 ("conditional_outcome","seventh ... a signe of four footed beasts","If the seventh is a four-footed sign with its lord or the hour lord/angular lord fortunate, Lilly predicts finding and taking the quarry.","Keep conjunctive/alternative wording as printed; do not collapse to seventh sign alone."),
 ("conditional_outcome","lord of the seventh ... Infortune, and the Moon infortunate","Under several adverse indicators Lilly predicts prolonged search, bodily exhaustion and little quarry taken.","Depends also on fortunate planets falling from the Moon."),
 ("condition","which shall be the truer, if the lord of the ascendant be Saturn","He adds Saturn as ascendant lord and a four-footed seventh-house sign to strengthen the adverse hunting forecast.","Keep 'truer' as a source qualifier, not an empirical confidence estimate."),
 ("conditional_outcome","Moon in the seventh or in any of the angles","An angular/seventh-house Moon or a fortunate seventh lord is given as an argument for good hunting.","The original refers to specific chart placements; cannot generalize to all hunting."))
entry([406],"unnumbered litigation subsection heading and roles",
 ("subheading","Of a Law-suit or Controversie betwixt two","A substantial unnumbered subsection begins within LIII on lawsuits, composition and recourse to court.","This is NOT a new numbered chapter."),
 ("assignment","ascendant, his lord and Moon ... the querent","Querent is signified by ascendant, its lord, and Moon.","Scope: dispute between two parties."),
 ("assignment","seventh house and his lord ... the Adversary","The seventh house and its lord signify the adversary.","Scope: same litigation question."))
entry([406],"easy accord by conjunction or mutually received favorable aspect",
 ("conditional_outcome","joined to the Lord of the seventh ... sextile or trine with mutual Reception","Conjunction of first lord/Moon with seventh lord, or sextile/trine with mutual reception, is said to favor accord.","Conditions are alternatives; mutual reception explicitly attaches to the favorable aspects in printed syntax."),
 ("conditional_outcome","compose all differences without mediation ... or ... a little entreaty","In that favorable configuration Lilly predicts settlement without intervention or after little entreaty.","Do not force an absolute prohibition on all third-party input."))
entry([406],"one-way reception and third-party negotiation",
 ("conditional_outcome","if one receive the other, and he that is received, receive not","One-way reception is said to indicate agreement without litigation.","The original separately forecasts outside intermediation."),
 ("conditional_outcome","not without intermission of a third party or more","That one-way reception forecast includes involvement of one or more third parties, often friends of the receiving significator.","Retain directional asymmetry; do not equate one-way reception with mutual reception."))
entry([406],"hard aspects versus easy aspects without reception",
 ("conditional_outcome","square or opposition with mutuall Reception","Mutual reception with square/opposition is grouped with sextile/trine without reception as eventual reconciliation after a legal skirmish.","Hard aspects and reception categories are distinct alternatives."),
 ("conditional_outcome","sextile or trine without Reception ... reconciled ... little combate","The source says a little litigation precedes reconciliation under those configurations.","Contrasts with the earlier easy/without-suit reception rule."),
 ("condition","unity ... from ... Significator ... lesse ponderous","The less ponderous significator's party is said to initiate agreement; mutual reception increases firmness.","Relative planetary weight is not converted to a modern score."))
entry([406],"lighter-to-heavier planet reception wording",
 ("conditional_outcome","lighter Planet ... joined to the more weighty","Where the lighter joins the heavier and the superior receives it, Lilly argues the receiver would agree.","The passage explicitly distinguishes which party receives which other."),
 ("limitation","and receive him not, but the superiour Planet receive him","Original syntax has asymmetric reception; record without reversing direction.","Avoid inferring modern willingness or consent of real litigants."))
entry([407],"judge intervention, translation of light, court delay",
 ("assignment","significator of the Judge ... the Lord of the tenth house","The tenth-house lord signifies the judge in this subsection.","Do not conflate judge with seventh-house opponent."),
 ("conditional_outcome","tenth house doth frustrate their conjunction","A judge's significator frustrating the impending union of the disputants is said to prevent pre-suit agreement.","The author speculates the judge or lawyer may be culpable; not real-world evidential proof."),
 ("condition","see if the Moon transferre light between ... first and seventh","Moon-mediated transfer of light can mark mediation between parties even during court proceedings.","Test this as historical assertion only."),
 ("conditional_outcome","some other Planet carry their influence or light","Another planet conveying light is likewise described as third-party intercession and reconciliation.","Do not make the Moon the only possible mediator."))
entry([407],"stronger significator, receptions, and prominence",
 ("conditional_outcome","he whose significator is most powerfull, ought to have the victory","Victory is attributed to the party whose significator is stronger.","An author's heuristic, not a validated legal-outcome predictor."),
 ("condition","in an angle ... essential Dignities","Angle placement and essential dignities are explicitly relevant to the strength comparison.","No numeric dignity weights are supplied."),
 ("condition","received by any other Planet ... more Friends to assist","Additional reception is presented as an argument for more allies.","An asserted historical interpretation, not observed human support."))
entry([407],"who offers settlement and cadent weakness",
 ("condition","first mover ... the lighter Planet","If settlement is shown, the lighter planet's party is said to move first.","The text adds commitment of the lighter's disposition to the other; no automatic 'winner' inference."),
 ("conditional_outcome","lord of the ascendant ... more light ... seventh more ponderous","Under the specified weight ordering Lilly says the querent initiates peace, with a literal 'e contrario' converse.","Keep converse verbatim as a limit; do not invent edge cases."),
 ("condition","Planet in a cadent house is more weak","Cadent placement weakens the significator unless received or assisted.","Explicit exception for reception/support retained."))
entry([407],"seventh-house Lord in ascendant and opposing phrasing",
 ("conditional_outcome","lord of the seventh house be in the ascendant","The author says the querent overcomes and adversary yields under this placement.","The nearby 'like happens to the querent' wording is elliptical; not adjudicated into a converse mapping."),
 ("limitation","the like happens to the querent ... that he shall be overcome","An elliptical parallel claims that the querent can also be overcome, but does not spell out a symmetrical positional antecedent.","Retain unresolved rather than reconstruct a missing clause."),
 ("scope","not onely in law Suits ... Fights, Duels and Warre","The author extends the comparison to finance lawsuits, fights, duels and warfare.","Historical scope extension only; no conflict/violence advice."))
entry([407,408],"retrograde parties and the 373-374 page transition",
 ("conditional_outcome","lord of the ascendant be retrograde","Querent's retrograde lord is said to signify weakness and disputed right/title.","The source also alleges that a party may deny truth; not a real honesty diagnostic."),
 ("conditional_outcome","lord of the seventh be retrograde","A retrograde seventh lord is said to imply analogous weakness on the adversary's side.","This is the cross-page continuation of the preceding conditional paragraph."))
entry([408],"tenth-house judge, speed and separation of parties",
 ("conditional_outcome","Lord of the tenth ... direct ... proceed according to order of law","Judge's significator direct is said to predict regular proceedings and efforts toward speedy judgment.","Full planet/house qualifiers retained."),
 ("conditional_outcome","if he be Retrograde ... prolong it a longer time","Retrograde judge's significator is said to imply disorder/delay.","Additional independent indicator: separating significators of first and seventh."),
 ("condition","Lord of the ascendant ... separated from ... Lord of the seventh","Separation between the disputants' significators is grouped as supporting delay.","Do not treat as a stand-alone demonstrated predictor."))
entry([408],"luminaries, prohibited bodily conjunction, and heart of Sun",
 ("condition","Lord ... ascendant ... aspect with the Sun or Moon","The author considers aspects/connections to Sun or Moon as arguments about querent strength.","Requires absence of intervening planetary obstruction."),
 ("limitation","beware it be not a corporall conjunction","A bodily conjunction is expressly excepted as an impediment.","Do not convert all Sun/Moon conjunctions to favorable aspects."),
 ("exception","unlesse ... heart of the Sun ... fortified thereby","A planet in the heart of the Sun is stated as an exception to that impediment.","Original text gives no exact degree orb; avoid encoding a modern orb."),
 ("condition","either of the houses of the Luminaries","Placement in the luminaries' houses and Sun/Moon in ascendant are given as further power indications.","Keep distinct from previous aspect and bodily-conjunction clauses."))
entry([408],"qualifications and two parties' analogues",
 ("conditional_outcome","these argue the potency of the querent","Those luminary and dignity conditions are asserted to favor querent potency.","Subject to the exact previous conditions and exceptions."),
 ("conditional_outcome","Lord of the seventh be dignified ... on ... quesited","Similar qualifications of the seventh lord are said to imply adversary strength.","Do not pool opposite-party scores."),
 ("limitation","qualified as before I mentioned of the Lord of the ascendant","The comparison is explicitly symmetric only for stated qualifying dignity conditions.","No general symmetrical inference outside the stated passage."))
entry([408],"claim about judge access and payments",
 ("conditional_outcome","ascendant ... joyned to the Lord of the tenth","This is said to indicate querent approaching the judge or making efforts to do so.","Possible bribery is described as speculative authorial language, not verified conduct."),
 ("historical_allegation","may be he will endeavour to bribe the Judge","Lilly conjectures attempted bribery as a possible interpretation.","Must not be used to accuse actual people."),
 ("conditional_outcome","Lord of the tenth receive the lord of the second","Reception of the second lord by tenth is said to mean judge receives money for efforts.","Does not establish bribery; historical claim only."),
 ("conditional_outcome","tenth receive the lord of the ascendant","Receiving the ascending lord is said to indicate judge hears querent's concerns.","Contrasted with 'otherwise not' in the printed source."))
entry([408,409],"judge favor and both disputants' approaches; page seam",
 ("conditional_outcome","Lord of the tenth ... more light ... joyned unto [ascendant]","If judge's lord is lighter and joined to querent's lord, Lilly predicts acting on the querent's behalf.","No need to speak to the judge in this stated scenario."),
 ("conditional_outcome","lord of the second ... joyned ... lord of the tenth","This is said to show the adversary approaching the judge.","The text's 'lord of the second' is preserved, although house-role logic may be ambiguous."),
 ("conditional_outcome","Lord of the tenth receive ... seventh","Judge receiving the seventh lord is said to favor the adversary.","Explicit direction of reception."),
 ("conditional_outcome","receive the lord of the eighth ... take his Money","Receiving the eighth lord is associated with taking adversary's money.","Not evidence of actual corrupt behavior."),
 ("conditional_outcome","receive both significators ... compose ... before full Tryall","Judge receiving both parties' significators is said to signal composition before full trial.","The sentence starts at bottom of PDF408 and completes at top of PDF409."))
entry([409],"dignity of judicial significator",
 ("conditional_outcome","Lord of the tenth ... tenth ... owne house","With tenth lord in tenth and its own house, Lilly says judge acts justly.","Explicit exception involving Saturn follows."),
 ("exception","unlesse that Planet be Saturn","Saturn is excluded from the favorable judicial reading.","Do not silently drop the Saturn exception."),
 ("conditional_outcome","only in his owne Termes or Triplicity","Even only terms/triplicity dignity is said to produce determination of the cause, regardless of outcome.","Distinguishes resolution from fair/rewarding resolution."),
 ("conditional_outcome","Planet ... tenth ... no dignity ... not in Reception","A tenth-house planet without dignity or reception is said to imply dissatisfaction with the sentence.","Do not flatten to 'any tenth-house planet'."))
entry([409],"Saturn judge and aspects/reputation",
 ("historical_allegation","if Saturn be Judge, he will not judge as he ought","Lilly asserts Saturn as judge signifies improper judgment.","Not a supported description of any actual judge."),
 ("conditional_outcome","Jupiter Venus Sun Mercury or Moon ... aspect to Saturn but opposition","The author associates favorable-planet aspects to Saturn other than opposition with temporary ill-repute and later clearance.","The printed phrase is any aspect EXCEPT opposition; it is not an opposition rule, and subsequent square language gives a more severe outcome."),
 ("conditional_outcome","if any of those be in square to Saturn","These squares are said to cause longer-lasting reputational damage.","Do not equate with the preceding opposition result."),
 ("conditional_outcome","Mars be in square to Saturn ... unlesse ... Capricorn","Mars square Saturn is presented as severe defamation; exception if Mars with Saturn in Capricorn mitigates scandal.","The printed original's exception must remain visible."))
entry([409],"summary of role assignment and strongest party",
 ("assignment","Querent ... ascendant ... Adversary ... seventh ... Judge ... tenth","A summary maps querent to first, opponent to seventh, judge to tenth, outcome/end to fourth.","Keep four roles separate; this is a source convention."),
 ("conditional_outcome","Planet ... most strong, and best posited ... victory","Lilly's conclusion selects the better-placed, stronger significator as best cause/winner.","No independent success evidence, no algorithmic numeric comparison."))
entry([409],"supporters and intercession",
 ("conditional_outcome","more Planets ... ascendant and second ... most Friends","More planets in first/second is said to favor more friends for the querent, with source-given converse.","Leave 'sic e contrario' unexpanded in formal predictions."),
 ("conditional_outcome","both Significators give their vertue to one Planet","A single receiving planet is said to indicate somebody intervening between parties.","Source term 'give their vertue' retained without speculative modern mechanics."))
entry([409],"sign modality and trouble in litigation",
 ("conditional_outcome","Signe ascending and seventh be fixed","Fixed signs in first and seventh are said to indicate persistence in dispute.","Condition: both first and seventh."),
 ("conditional_outcome","movable Signes ... end it very shortly","Movable signs are said to forecast little willingness to litigate and quick settlement.","Condition: those houses; not all charts."),
 ("conditional_outcome","common Signes ... continue the Suit long","Common signs in the relevant houses are said to signal prolonged proceedings and movement between courts.","Keep court-transfer claim separate from fixed-sign persistence."),
 ("conditional_outcome","on whose part you find the Infortunes","Malefic placement relative to parties is said to forecast the greater prejudice, sorrow and trouble.","Not a modern evidence-based legal risk assessment."))
entry([410],"final original-page transition sentence before LIV divider",
 ("interpretive_note","the Moon ... from whom she is separated ... Planet to whom she applyes","Lilly instructs that Moon's separating/applying planets be considered alongside first/seventh significators.","Original p376 above the horizontal divider is the closing LIII sentence."))
entry([410],"chapter LIV navigation-only physical boundary",
 ("next_heading_boundary","CHAP. LIV. Of Buying and Selling Commodities.","Marks the start of LIV BELOW the divider on PDF410/printed376; excludes all its body.","Navigation-only, not a Chapter LIV source claim or acceptance."))

assert len(ROWS) == len({x['local_id'] for x in ROWS})
assert [x['local_id'] for x in ROWS] == [f'LIII-C{i:03}' for i in range(1, len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages'] == [405]
assert SPANS[-1]['original_pdf_pages'] == [410]
assert [p for s in SPANS for p in s['original_pdf_pages']] == sorted([p for s in SPANS for p in s['original_pdf_pages']])
assert len([r for r in ROWS if r['record_role']=='next_heading_boundary']) == 1

def dump(name, obj):
    (P/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

images=[]
for n in range(405,411):
    f=P/'evidence'/f'pdf_1647-{n}.jpg'
    if not f.is_file(): raise SystemExit(f'MISSING source scan {f}')
    b=f.read_bytes()
    images.append({'pdf_page':n,'printed_page':n-34,
                   'relative_path':f.relative_to(P).as_posix(),
                   'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
                   'original_witness':'Wellcome b30338724 scan; PDF index matches original physical sequence'})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B02y','status':'PROVISIONAL_SOURCE_FIRST_NON_ACCEPTED','record_count':len(ROWS),
 'source_id':'1647 Wellcome b30338724 original physical source',
 'authoring_method':'direct original-image reading of 405-410; source anchors are short editorial abbreviations, not diplomatic transcription',
 'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B02y','status':'PROVISIONAL_SOURCE_TO_DRAFT_VISUAL_MAP',
 'complete_chapter_claimed':False,'independent_diplomatic_transcription_claimed':False,
 'source_spans':SPANS,'span_count':len(SPANS),'draft_source_units':len(ROWS),
 'source_window':{'first_pdf':405,'last_pdf':410,
                  'start_position':'PDF405 BELOW LII/LIII divider',
                  'end_position':'PDF410 ABOVE LIII/LIV divider; LIV heading navigational only'},
 'empirical_outcomes':0})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B02y','status':'PROVISIONAL',
 'ordered_local_ids':[x['local_id'] for x in ROWS],
 'cross_page_local_ids':[x['local_id'] for x in ROWS if len(x['original_pdf_pages'])>1],
 'navigation_only_last_id':ROWS[-1]['local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B02y','status':'PROVISIONAL','source_id':'ORIGINAL_1647_WELLCOME_B30338724',
 'original_full_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'previously_accepted_lilly_count':3071,'last_accepted_chapter':'LII',
 'chapter':'LIII','original_pdf_pages':list(range(405,411)),
 'opening':'PDF405 bottom BELOW divider','closing':'PDF410 top ABOVE divider',
 'images':images,'original_image_visual_review':True,'blind_word_for_word_transcription':False})
dump('CLAIM_LEDGER.json',{
 'batch':'B02y','status':'PROVISIONAL_SOURCE_ONLY',
 'authorial_historical_asterisms_only':True,
 'source_first_units':len(ROWS),'reverse_spans':len(SPANS),
 'new_globally_accepted_records':0,'accepted_lilly_baseline':3071,
 'retained_ptolemy_baseline':1066,'accepted_combined_baseline':4137,
 'real_hunting_trials':0,'authenticated_court_outcomes':0,
 'predictions_validated':0,'new_runtime_rules':0,
 'not_factual_real_person_honesty_or_corruption_diagnostics':True})
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B02y','status':'RETAINED_UNRESOLVED_NOT_MODELED',
 'points':[
  {'id':'LIII-U01','location':'PDF405 lower half','limit':'The original hunting heading also governs a long unnumbered lawsuit section; do not split at the lawsuit subheading.'},
  {'id':'LIII-U02','location':'PDF405 margin','limit':'Ancients/trifles author aside is not a hunting judgment.'},
  {'id':'LIII-U03','location':'PDF405-406','limit':'Hunting ' + 'lord/hour/term terminology not reducible to a unique algorithm from this paragraph.'},
  {'id':'LIII-U04','location':'PDF406','limit':'Four-footed signs and hunting outcomes depend on multiple placements; no isolated unconditional predictions.'},
  {'id':'LIII-U05','location':'PDF406','limit':'One-way versus mutual receptions have opposite mediation conditions; maintain direction.'},
  {'id':'LIII-U06','location':'PDF406','limit':'Lighter and heavier/superior planetary language not quantified; keep source-native comparative wording.'},
  {'id':'LIII-U07','location':'PDF407','limit':'The phrase "the like happens to the querent ... overcome" omits a clear positional antecedent; do not invent a symmetric premise.'},
  {'id':'LIII-U08','location':'PDF407','limit':'The converse "e contrario" is retained without operational expansion.'},
  {'id':'LIII-U09','location':'PDF408','limit':'The Sun-heart exception has no orb stated; do not insert a chosen orb.'},
  {'id':'LIII-U10','location':'PDF408','limit':'Claims of judge bribery/payment or litigant dishonesty are untested historical allegations.'},
  {'id':'LIII-U11','location':'PDF408','limit':'Second-house-lord joining judge representing adversary is textually surprising; do not "correct" house to eighth without documentary basis.'},
  {'id':'LIII-U12','location':'PDF409','limit':'Judicial reputation interpretations of Saturn/aspects are source-only and symbol-sensitive.'},
  {'id':'LIII-U13','location':'PDF409','limit':'Lilly distinguishes strong/essential dignities but provides no frozen scoring rule in this paragraph.'},
  {'id':'LIII-U14','location':'PDF409','limit':'"sic e contrario" supporters converse is not expanded to all missing cases.'},
  {'id':'LIII-U15','location':'PDF410','limit':'Moon separation/application reference is a closing condition in LIII, not the opening of LIV.'},
  {'id':'LIII-U16','location':'PDF405-410','limit':'Source-first normalizations are not complete independent diplomatic transcription or validation of efficacy.'}
]})
print(f'B02y provisional: {len(ROWS)} source units; {len(SPANS)} original-source passages; {len(images)} original scans; no canonical count change')
