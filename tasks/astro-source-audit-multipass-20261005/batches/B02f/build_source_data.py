"""Rebuild Lilly XXIV-XXVI source inventory; historical reference only, no predictions."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
SID='LILLY1647_WELLCOME_B30338724'
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
SIGNS='Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces'.split()
RECORDS=[]
CHAPTER='XXIV'
def rec(title,pages,statement,requires=(),limits=(),kind='conditional_source_rule'):
    n=668+len(RECORDS)
    RECORDS.append({'id':f'LI.1647.II.{CHAPTER}.R{n}','title':title,'kind':kind,
      'source_locator':{'source_id':SID,'source_sha256':SHA,'book':'II','section_key':f'II.{CHAPTER}','pdf_pages':list(pages),'printed_sequence':[p-34 for p in pages]},
      'statement_type':'editor_normalized_paraphrase','source_statement':statement,
      'prerequisites':list(requires),'qualifications_and_limits':list(limits),
      'runtime_status':'REFERENCE_ONLY_NOT_PROMOTED','independent_evidence_unit':False})
def save(name,x):
    (ROOT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

# Chapter XXIV: distinct queries require distinct reference frames.
rec('At-home question: asker and unrelated familiar person',[181],
    'Ascendant and its lord represent the asker; seventh and its lord represent the familiar person to be visited, when not related.',
    ['Question is whether the asker will find that person at home.'],['Do not use this seventh-house assignment for every possible absent-person question.'])
AT_HOME_ROLES={'unrelated_familiar':7,'father':4,'mother':10,'child':5,'sibling':3,'neighbour':3}
rec('At-home question: relatives replace generic seventh',[181,188],AT_HOME_ROLES,
    ['Choose the actual relationship before selecting the house ruler.'],['Sibling/neighbour illustration is in XXV p154; the named roles are not a complete arbitrary-relationship ontology.'],kind='source_role_table')
PRESENCE={'angular':{'houses':[1,4,7,10],'claim':'at home'},'succedent':{'houses':[2,5,8,11],'claim':'not far from home'},'cadent':{'houses':[3,6,9,12],'claim':'far from home'}}
rec('Presence and angularity',[181],PRESENCE,['The planet must be the relevant person\'s significator.'],['These are historical claims, not a method for finding an actual missing person.'],kind='source_reference_table')
rec('Meeting or learning location on intended visit day',[181],
    'If the Ascendant lord applies to the seventh lord by a perfect aspect on the intended visit day, the asker meets the person en route OR hears where the person is.',
    ['Relevant at-home enquiry; same-day contact.'],['The two possible outcomes must not be narrowed to an inevitable face-to-face meeting.'])
rec('Intermediary supplies whereabouts',[181],
    'A planet or Moon separating from the seventh lord and transferring light to the Ascendant lord signifies an intermediary who supplies the location.',
    ['Direction is from the sought person toward the asker.'],['The short passage does not independently settle every translation prerequisite defined elsewhere.'])
rec('Historical description of the intermediary',[181],
    'Describe the translating planet; gender testimony uses planet, sign and quarter, with the greater masculine testimony giving a man, the contrary a woman.',
    limits=['Historical classification only; no modern identity inference and no numerical tie rule supplied.'])
rec('Sudden occurrence: chart origin',[182],
    'Erect the figure for the occurrence time, else when it was first heard of.',
    ['Enquiry is about the meaning of a sudden occurrence, rumour or report.'],['This is not automatically the separate question-receipt convention at pp166-167.'],kind='time_origin')
rec('Sudden occurrence: three candidate rulers',[182],
    'Compare ruler of the Sun\'s sign, ruler of the Moon\'s sign, and ruler of the life house/Ascendant; consider the one most powerful in the Ascendant.',
    limits=['No complete numerical strength ranking or tie-breaker supplied; power in Ascendant does not imply bodily presence there, as XXV illustrates.'])
rec('Sudden occurrence: favourable condition',[182],
    'Selected significator in sextile or trine to Sun, Jupiter or Venus indicates no evil following the event or report.',
    ['Significator selected through the preceding three-ruler enquiry.'],['Do not use an arbitrary benefic aspect as an unconditional event verdict.'])
rec('Sudden occurrence: adverse condition',[182],
    'If the selected planet is weak, combust, or in square, opposition or conjunction of Mars, Saturn or Mercury, some misfortune follows; its nature and occasion depend on the afflictor\'s position and nature.',
    limits=['Mercury is expressly included locally; mixed favourable/adverse conditions are not algorithmically resolved.'])
EVENT_AFFLICTOR_EXAMPLES={3:'neighbour or kinsman',2:'loss of substance',4:'parental discontent or land/houses',5:'discord in tavern/company or through a child'}
rec('Sudden occurrence: house-derived occasions',[182],EVENT_AFFLICTOR_EXAMPLES,
    ['The relevant planet afflicts the selected significator.'],['These are alternative occasions, not independent outcomes to accumulate.'],kind='reference_examples')
rec('Marks: author\'s reported motivation and success',[182,184],
    'Lilly calls the apparent accuracy of marks a chief reason for his deep engagement with astrology and reports successful informal trials in company.',
    limits=['Author-reported experience, not blinded measurement, a count of trials, or independent evidence.'],kind='author_experience_claim')
MARK_INPUTS=['Ascendant sign','Ascendant-lord sign','sixth-cusp sign','sixth-lord sign','Moon sign']
rec('Marks: five source inputs',[182,183],MARK_INPUTS,
    ['Horary figure has been erected for a demand.'],['Each is said to locate another mark on the sign-represented body part; no deduplication or base-rate model is specified.'],kind='reference_inputs')
rec('Marks: source examples for sign body regions',[182],{'Taurus':'neck','Gemini':'arms'},
    limits=['Do not infer a disease, or silently substitute the fixed house-to-body sequence.'],kind='reference_examples')
rec('Marks: Saturn and Mars modifiers',[183],
    'Saturn indicates a dark/black mark; Mars a scar or cut in a fiery sign, otherwise a red mole. Greater affliction of sign or planet makes the mark larger/more conspicuous.',
    limits=['No measured size, colour threshold or clinical classification is supplied.'])
rec('Marks: right side clause',[183],
    'Masculine sign AND masculine planet places the mark on the right side.',
    limits=['Mixed testimonies are not specified in this clause.'])
rec('Marks: contrary side clause',[183],
    'The contrary is judged when the sign is feminine and its lord is in a feminine sign.',
    limits=['The feminine clause does not repeat the masculine clause\'s planet-nature predicate; preserve this asymmetry.'])
rec('Marks: visibility and hemisphere',[183],
    {'houses_7_through_12':'front/visible/outside of member','houses_1_through_6':'back/not visible/inside of member'},
    limits=['Literal numbered-house groups; no inferred actual observer visibility or cusp equality convention.'],kind='reference_table')
rec('Marks: longitudinal position within member',[183],
    'Few degrees ascending or occupied by the ruler signify upper part; middle degrees middle part; latter degrees or Moon/first/sixth lord near sign end signify lower part.',
    limits=['No numerical cutoff for few/middle/latter is supplied; do not invent 0-10/10-20/20-30 bins.'])
rec('Marks: qualifications and clock warning',[183,184],
    'Claims depend on a radical question, correctly taken time and a person of sufficient age, not an infant. Short ascensions, invisible Sun and faulty clocks can mislead the Ascendant.',
    limits=['No numerical sufficient age or allowed clock uncertainty; do not retrofit these exclusions to excuse a failed prediction.'])
rec('Short-ascension illustrative durations',[184],
    {'Pisces_and_Aries':'three quarters of an hour and a few minutes each','Aquarius_and_Taurus':'an hour and odd minutes'},
    limits=['Historical local examples, not latitude-independent astronomical constants.'],kind='author_examples')
rec('Marks for a spouse use turned places',[184],
    'Use seventh sign/lord for the wife and twelfth sign/lord for her sixth, adding four source indications.',
    limits=['Twelfth is sixth counted inclusively from seventh; no new independent person-case implied.'])
HOUSE_BODY_OPENING={1:'face',2:'neck',3:'arms and shoulders',4:'breast and paps',5:'heart'}
rec('House-body correspondence remains separate from sign-body',[184],HOUSE_BODY_OPENING,
    limits=['First house means face whatever its sign; the text continues in order but only these five are explicitly enumerated here.'],kind='reference_table')
rec('Eye mark: lunar syzygy and additional conditions',[184],
    'Moon conjunct or opposite Sun frequently indicates a mark near an eye; the stronger assertion adds angular conjunction/opposition and an adverse Mars aspect to either luminary.',
    limits=['Do not drop the added conditions, or turn the statement into medical advice.'])
rec('General absent stranger: a different first-house frame',[185],
    'For a general absent-person question with no relation to the asker, first house, its lord and Moon signify the absent party.',
    limits=['Local exception to the seventh-house at-home role; the exact question matters.'])
rec('Absent person: eighth significator and cusp proximity',[185],
    'Eighth lord, a planet in the eighth, or one within five degrees of its cusp signify death or its quality in this enquiry.',
    limits=['Historical investigation only, not an actual missing-person or mortality classifier; exact five-degree equality and side not specified locally.'])
rec('Absent person: adverse union or opposition configurations',[185],
    'Bodily union of Ascendant lord, Moon and eighth lord/occupant, or opposing configurations in eighth-second or twelfth-sixth, argues deceased OR sick near death.',
    limits=['Do not collapse the disjunction to certain death. Ambiguous three-planet grouping is retained.'])
rec('Absent person: further adverse testimonies',[185],
    'Translation first lord to eighth, especially deep/lame/deficient degrees; reverse translation; eighth lord in Ascendant; or first lord and Moon in fourth are death testimonies.',
    limits=['Separate source configurations, not independence-proven evidence; conflicting surviving-state indications remain relevant.'])
PAST_SEPARATIONS={6:'recent sickness',8:'danger of death but NOT dead',12:'mental trouble/fear of imprisonment or arrests',2:'money shortage',7:'quarrel/contention',9:'journey trouble',3:'journey trouble'}
for house,claim in PAST_SEPARATIONS.items():
    rec(f'Absent person: past separation from house {house} lord',[185],claim,
        ['Ascendant lord has separated from an adverse aspect of the named lord.'],['Past state is not an assertion of present death.'],kind='conditional_reference_row')
rec('Absent person: journey-specific alternatives',[185],
    'Sea journey trouble may be winds or pirates; land travel trouble thieves or bad roads.',
    ['Prior adverse separation from third/ninth lord.'],['Location mode is contextual input, not a fitted after-the-fact choice.'])
rec('Absent person: contrary survival observation',[185],
    'Lilly reports finding the person alive with Ascendant lord in ninth, tenth or eleventh despite rumours of death.',
    limits=['Author observation; no independently verified denominator or precedence against all earlier adverse conditions.'],kind='author_experience_claim')
rec('News: ephemeris contact route',[185,186],
    'After judging the absent person alive, inspect when eleventh lord and Ascendant lord reach trine or sextile; news around that time, possibly that day.',
    ['Survival considered first; actual ephemeris contact needed.'],['This is not the same as symbolic degrees converted to time.'])
NEWS_UNITS={'moveable':'days','common':'weeks','fixed':'months'}
rec('News: symbolic lunar-distance route',[186],NEWS_UNITS,
    ['Moon applies by sextile/trine to Ascendant lord; use degrees remaining.'],['No day length/calendar-month convention, fractional rounding or mixed-sign rule supplied.'],kind='symbolic_unit_table')
rec('Second question figure reused for four teachings',[186],
    ['finding someone at home','sudden occurrence','marks on body','absent person dead or alive'],
    limits=['One diagram; later conditional reuses are not four independent observed trials.'],kind='figure_scope')

CHAPTER='XXV'
rec('Woman\'s son: actual enquiry and significators',[187],
    'A woman at Lilly\'s country house asks whether her son is at his master\'s or her own home. Venus represents her; fifth-house Pisces makes Jupiter the son\'s significator.',
    limits=['Reported historical case, not a present participant or natal interpretation.'],kind='worked_case')
rec('Son at mother\'s home: two stated testimonies',[187],
    'Jupiter in Ascendant and Moon applying dexter sextile to fourth-lord Saturn indicate the boy at the mother\'s dwelling; author reports she found him there.',
    limits=['A reported confirmation, not blinded validation; two testimonies are not two cases.'],kind='worked_case')
rec('Counterfactual son at master\'s home',[187],
    'Jupiter in tenth OR Moon separating from Jupiter and next applying a good/indifferent Sun aspect with Sun angular would have indicated the master\'s.',
    limits=['Explicit hypothetical branch, not something that happened.'],kind='counterfactual_example')
rec('Actual meeting: source date and time report',[187,188],
    'Jupiter and Venus are reported to trine on July 25 about two after noon; mother returned and met son about three that afternoon.',
    limits=['Author\'s report; historical date/time not converted to UTC or independently recalculated. Prediction, traveller action and report are not blinded.'],kind='reported_case_timing')
rec('Meeting versus news: distance qualification',[187,188],
    'Near sextile/trine day expect letter/news when distances allow; nearby people meet on the same day even without prior intention.',
    limits=['No numerical near/far threshold; the statement need not promise direct meeting across impossible distances.'])
rec('Counterfactual neighbour or sibling',[188],
    'Third-lord Jupiter would represent neighbour, brother or sister; its angularity would indicate at home.',
    limits=['Same figure, hypothetical different question, not another confirmation.'],kind='counterfactual_example')
rec('Counterfactual unrelated visitor: cusp exclusion',[188],
    'Seventh-lord Mars represents the stranger. It remains in second, more than five degrees before third cusp, and is not admitted third-house signification.',
    limits=['Negative boundary example supports exclusion beyond five degrees; does not settle exact equality.'],kind='counterfactual_example')
rec('Counterfactual stranger: location layers',[188,189],
    'Second house is succedent so near, not at home; northern quarter plus easterly Sagittarius gives northeast. A furlong or one/two fields is suggested. Rural sign places imply rising ground; in town Mars places imply smiths/butchers northeast of home.',
    limits=['Urban/rural context must be supplied; illustrative distance is not a universal conversion.'],kind='counterfactual_example')
rec('Sudden-occurrence hypothetical: Venus selection',[189],
    'For hypothetical event time, Sun rules itself, Jupiter Moon\'s Pisces, Venus Ascendant Libra. Venus has domicile and term rights at Ascendant and trines cusp and angular Jupiter, yielding a favourable reading.',
    limits=['Power at Ascendant is not bodily occupation. The literal term attribution is retained without selecting an unannounced term table.'],kind='counterfactual_example')
rec('Sudden-occurrence hypothetical: nearer opposition',[189],
    'Had Venus been nearer opposition to second-house Mars, the author would indicate loss or contention over money.',
    limits=['No cutoff for nearer; hypothetical, not a second event.'],kind='counterfactual_example')
rec('Mother\'s marks in the worked figure',[189,190],
    ['right face near mouth: Jupiter in Ascendant and masculine Libra/Jupiter','lower reins/haunches: later Libra degrees','forehead near hair: early Aries sixth cusp','right thigh middle/back: masculine Mars in Sagittarius below earth','extremity under left foot: Moon Pisces26:43 below earth'],
    limits=['Preserve sign-body and house-body channels separately. These are author-described marks, not examined photographs or clinical findings.'],kind='reported_case_marks')
rec('Son\'s turned marks',[190],
    'Fifth Pisces ninth degree is son\'s Ascendant: left cheek and foot near ankle; tenth Leo4 as sixth from fifth: right side below breast.',
    limits=['Multiple channels, one reported person. No natal-birth data or disease diagnosis.'],kind='reported_case_marks')
rec('Hypothetical absent person: favourable survival reasoning',[190],
    'Treat same Ascendant, Jupiter there, Venus and Moon as absent-person significators. Absence of the listed eighth/sixth afflictions, translations and fourth-house placements permits favourable judgment; Venus\'s preceding Mars opposition indicates past money trouble/fever, Jupiter relief.',
    limits=['This is expressly a supposed question, not a separately observed missing person.'],kind='counterfactual_example')
rec('Long-ascension square in news example',[190,191],
    'Mercury eleventh lord applying square to Ascendant Jupiter, both in long-ascension signs, is said equivalent to trine.',
    limits=['Source interpretive equivalence, not a change of the actual 90-degree geometry.'],kind='interpretive_equivalence')
rec('News timing in hypothetical: ten weeks OR ten days',[191],
    'About ten degrees to the square gives about ten weeks; if the person is known nearby, ten days because the signs are moveable.',
    limits=['Different from blindly applying the earlier moveable=days table. No quantitative distance threshold; no physical contact time computed.'],kind='counterfactual_timing')

CHAPTER='XXVI'
rec('Ship enquiry: topic location differs from earlier placement',[191],
    'Lilly reports that earlier authors put shipping under ninth because of voyages, but he places this judgment with first-house matters because most safety reasoning uses Ascendant, its lord and Moon.',
    limits=['Reported earlier classification and Lilly\'s selected method remain distinct; does not abolish every ninth-house travel enquiry.'],kind='source_method_disagreement')
SHIP_ROLES={'Ascendant_sign':['ship','goods'],'Moon':['ship','goods'],'Ascendant_lord':['people_sailing']}
rec('Ship and people have different significators',[191],SHIP_ROLES,
    limits=['One body can occupy multiple roles; roles are not independent astronomical observations.'],kind='role_table')
rec('Ship: adverse configuration and reception exception',[191],
    'The opening all-unfortunate case includes malefic in Ascendant with eighth dignities, Ascendant lord in eighth badly configured with eighth/twelfth/fourth/sixth lord, or Moon combust/below earth. Ship loss and drowned crew are asserted, except reception permits some sailors to escape the wreck.',
    limits=['The introductory all-unfortunate language and following disjunctions are preserved; no complete Boolean classifier or actual maritime prediction.'])
rec('Ship: all-free and mixed outcomes',[191],
    {'all_significators_free':'men and goods safe, strengthened by reception',
     'Ascendant_and_Moon_unfortunate_but_Ascendant_lord_fortunate':'ship lost but people saved'},
    limits=['Vessel survival, cargo and human survival cannot be interchangeable scoring targets.'])
SHIP_PARTS=dict(zip(SIGNS,[
 'breast of ship','under breast toward water','roother or stern','bottom or floor',
 'top above water','belly','between wind and water / sometimes above and below water',
 'where seamen lodge or do their office','mariners themselves','ends of ship','master or captain','oars']))
for sign,part in SHIP_PARTS.items():
    rec('Ship correspondence: '+sign,[192],part,
        limits=['Historical mapping attributed to some authors; not engineering or navigational guidance.'],kind='ship_correspondence_row')
rec('Ship parts: fortunate and unfortunate branches',[192],
    'Fortunate signs/Moon/ruler are associated with no defect or repair, while afflicted signs/Moon/sign ruler indicate damaged parts to warn about.',
    limits=['The fortunate paragraph nevertheless also literally says the ship will receive any detriment; this inconsistent wording is left unresolved, not silently negated.'])
rec('Departing ship: angular fortunes and weakened infortunes',[192],
    'Fortunes in or falling into angles, with infortunes remote, cadent, combust or under beams, signify safe arrival with cargo; infortunes angular or succedent bring hindrance in the sign-corresponding part.',
    limits=['Departure assessment distinguished from status of a ship already missing.'])
rec('Departing ship: Saturn and qualified Mars damage',[192,193],
    'Saturn in the adverse branch signifies splitting, drowning or injury from impact/grounding. Mars in essential dignity OR beholding its own dignity OR in an earthly sign similarly signifies grave damage.',
    limits=['Do not turn essential dignity into unconditional protection: here it qualifies adverse action.'])
rec('Ship damaged but most survive',[193],
    'Benefic rays to the malefic places, with angular rulers (especially Ascendant) and Moon\'s sign ruler free, mitigate to hard labour and much damage while most goods and people survive.',
    limits=['Mitigation is not proof of no damage; precise strength thresholds and competing conditions remain unspecified.'])
rec('Ship: enemy fear versus additional violence',[193],
    'Mars afflicting angular lords and Moon dispositor signifies fear of pirates/enemies. Further afflicted signs add bloodshed, quarrels, theft and cargo pilfering, especially signs assigned upper ship parts.',
    limits=['Fear, conflict and actual loss are distinct outputs; upper-part membership is not fully formalized by this paragraph.'])
rec('Ship: Saturn theft branch',[193],
    'Saturn afflicting analogously signifies theft and unexplained depletion but no bloodshed.',
    limits=['Do not carry Mars\'s bloodshed into this explicitly contrasting branch.'])
rec('Ship: underwater damage',[193],
    'Saturn, Mars or South Node afflicting signs assigned bottom/underwater parts signifies breaking, sinking or a dangerous leak.',
    limits=['Disjunct outcomes retained; no modern risk probability.'])
rec('Ship: aerial-fire branch',[193],
    'Mars afflicting signs at Midheaven points to fire, thunder/lightning or falling aerial matter, with fiery signs AND nearby violent fixed stars specified.',
    limits=['The added sign/star conditions must not disappear; no distance to star specified.'])
rec('Ship: fourth-house fire and hostile attack',[193,194],
    'Mars or the infortune in fourth-house sign indicates bottom fire; Mars there in Gemini/Libra/Aquarius signifies fire or destruction during enemy combat/grappling.',
    limits=['Enemy source of fire is a conditional refinement, not every fourth-house Mars interpretation.'])
rec('Ship: Saturn Midheaven or seventh',[194],
    'Saturn replacing Mars at Midheaven indicates contrary winds, leaks, torn/bad sails, scaled by strength and benefic distance; Saturn seventh points to stern damage.',
    limits=['No quantitative relation between strength, distance and damage is supplied.'])
rec('Ship: Ascendant damage',[194],
    'Infortune in Ascendant points to damage at the forepart, greater or less with the significator\'s condition.',
    limits=['This house-based location is separate from the sign-to-part table.'])
rec('Ship: retrograde return or harbour stop',[194],
    'Retrograde Ascendant lord means forward progress then return or harbour entry soon after setting out. Moveable Ascendant lord retrograde AND fourth lord retrograde strengthens return to original port through contrary winds.',
    limits=['No absolute time or objective wind forecast supplied.'])
rec('Ship: return can be without loss',[194],
    'Retrogradation as sole impediment gives return without loss; with another misfortune, return for repairs and danger.',
    limits=['Do not code all retrogradation or all returns as damage/loss.'])
rec('Ship: eighth lord and crew hierarchy',[194],
    'Eighth lord afflicting Ascendant lord indicates harm, especially if Ascendant lord in eighth. Afflicting Moon dispositor, Ascendant lord AND Moon imports death of captain, mate and principal officers.',
    limits=['Historical claims only; no personal mortality prognosis; preserve the expanded conjunction of prerequisites.'])
rec('Ship: commercial result separate from physical loss',[194,195],
    'Fortune AND second lord unfortunate signify poor sale/market or loss on goods. Head, Jupiter or Venus in relevant second-house/Fortune relationships signify profit, stronger with essential strength.',
    limits=['Node/planet grammar does not give the Head a literal domicile lordship; source alternatives are not a complete executable Boolean formula. Physical safety does not itself establish profit.'])
rec('Ship: journey duration',[195],
    'Slow Ascendant lord and Moon-sign lord and their dispositors signify a long voyage; quick signifies fast arrival and return sooner than expected.',
    limits=['Qualitative speeds and relative expectation, not a numerical speed or date algorithm.'])
rec('Ship: merchant versus sailors dispute',[195],
    'Ascendant lord and Moon-sign lord in square/opposition WITHOUT reception signify discord; the more dignified party prevails: Ascendant lord for sailors, Moon-sign lord for merchant.',
    limits=['Actual role and relative dignity required; ties are not resolved.'])
rec('Ship: provisions and ambiguous removed-from-second language',[195],
    'Second lord removed beyond its second (Taurus example Venus beyond Gemini), or removed from second to Moon\'s place (Moon Virgo example lord not Libra), or Fortune dispositor not with Fortune indicates scant provisions.',
    limits=['The first two conditions are textually awkward; do not normalize them into one invented distance predicate.'])
rec('Ship: kind of shortage',[195],
    'In the shortage branch, watery signs give lack of fresh water; earthly/airy signs lack of food and fire.',
    limits=['Fiery-sign branch not supplied. These are source categories, not practical provisioning advice.'])
rec('First ship: reported context and question',[196],
    'December1644 merchant\'s ship trading to Spain was rumoured lost after storms; insurance was unobtainable despite an offer of60 in100. A friend asks. Lilly judges recent danger but present recovery.',
    limits=['Author\'s historical case report, no verified insurance data or contemporary recommendation.'],kind='reported_case')
rec('First ship: damaged hull evidence',[196,197],
    'Cancer Ascendant11:33, Saturn\'s square and three Saturn-like rising stars yield a heavy/slow unsound vessel and former damage; the account reports confirmation. South Node in ninth adds journey distress, Saturn in Aries breast damage.',
    limits=['South Node, not Saturn, is the ninth-house symbol in this passage. Reported confirmation is not independent verification.'],kind='reported_case')
rec('First ship: mitigation and recovery reasoning',[196,197],
    'Exalted Moon in eleventh interposes a sextile toward Ascendant before opposed Sun/Mercury rays; applying trines, proximity to Jupiter, relevant significators above earth and no angular infortunes support vessel/crew survival.',
    limits=['Past damage and present survival coexist; no independent cases generated from each contributing feature.'],kind='reported_case')
rec('First ship: localization and reported resolution',[197],
    'Fixed Taurus Moon eleventh and application to Capricorn Mercury in west angle lead to southwest coast near Ireland/Wales and a harbour for repairs; report confirms west and harbour.',
    limits=['Reported west/harbour is less specific than all the proposed geography. Do not count full location prediction as independently verified.'],kind='reported_case')
rec('First ship: news deadline',[197,198],
    'Near applying trines, angular targets and swiftness lead to news that night OR in two days, reported as fulfilled.',
    limits=['Alternative deadline, no dated letter or independent contact-time calculation.'],kind='reported_case_timing')
rec('First ship: merchandise and reception',[198],
    'Fortune disposed by Mars, Mercury in reception with Mars and Moon applying to second-lord Sun encourage a favourable financial result.',
    limits=['Commercial inference separate from the report of vessel survival. Exact reception convention not specified locally.'],kind='reported_case')
rec('First ship: antiscion claims',[198],
    'Jupiter\'s antiscion in ninth degree of Leo is called the second cusp; Mars\'s antiscion is said to fall on the very Ascendant degree. Roles cited: Mars eleventh lord/Fortune dispositor, Jupiter tenth lord.',
    limits=['Retain printed chart coordinates and source claims separately. Exact-minute equality is not assumed from the prose.'],kind='source_geometry_claim')
rec('Moon applying to retrograde planet',[198],
    'Good aspect of Moon to a retrograde planet usually brings a speedy unexpected ending one way or another.',
    limits=['Speed/completion is not intrinsically benefit or safety. Generic favourable hope is given separately.'])
rec('Ship concluding favourable checklist',[198],
    'Ascendant free from infortunes; Ascendant lord, Moon and dispositors above earth; Ascendant lord ninth/tenth/eleventh; or trine/sextile to Jupiter or eleventh lord are good signs.',
    limits=['Summary shares evidence with preceding example and is not an independent observed case.'],kind='source_summary')
rec('Second ship: opposite reported outcome',[199,200],
    'A1646 chart is judged mostly/all investment lost and ship probably wrecked; author says it proved so. Ascendant and Moon signify vessel/crew in this opening.',
    limits=['Different local role compression from the earlier separated hull/crew roles; no independent outcome documentation.'],kind='reported_case')
rec('Second ship: sequence matters more than favourable aspect label',[199],
    'Moon separated square from eighth/ninth-lord Saturn, was void, then trines that same eighth lord before opposing Mercury twelfth/fourth lord; the trine does not cancel the adverse subject.',
    limits=['Later contacts involve sign changes; retain void-at-question versus future application distinction.'],kind='reported_case')
rec('Second ship: additional weak dispositors and money factors',[199],
    'Moon dispositor Mercury detriment and approaching combustion; its dispositor Jupiter below earth with Mars/malefic terms; Mars fallen near second cusp; Fortune sixth with retrograde second-house dispositor not beholding; further squares accompany the loss judgment.',
    limits=['No invented aggregation weights, no counting correlated dispositor roles as separate successful predictions.'],kind='reported_case')
rec('Second ship: below-earth closing statement',[199,200],
    'Principal significators below earth are adverse, most of all fourth-house placement, called a sure sinking testimony.',
    limits=['Source confidence is not a modern safety claim; retain earlier mitigation qualifications and no empirical calibration.'],kind='source_summary')
rec('Question time: arrival/first greeting rejected',[200],
    'Lilly rejects automatically using a visit\'s first arrival or greeting, since conversation can end with no actual question being asked.',
    limits=['Rejected attributed alternative, not a live rule to add to a model.'],kind='rejected_time_origin')
rec('Question time: actual request',[200],
    'Use the moment the querent propounds the desire to the astrologer.',
    limits=['Historical question chart, not native birth time or arbitrary first mention of a person.'],kind='time_origin')
rec('Question time: delayed letter',[200],
    'For a letter delivered earlier and read four/five hours later, use hour/minute when opened and the querent\'s intention is perceived, not mere delivery time.',
    limits=['Does not define modern asynchronous AI first-read/reprocessing semantics; those would require a separately declared convention.'],kind='time_origin')
rec('Self-question: reported objection and author\'s alternative',[200,201],
    'Lilly reports Bonatus and others warning against judging one\'s own question; he conjectures concern about partiality. He permits a genuinely troubling self-question at its arising time if impartial, urging all favour to one\'s cause be laid aside.',
    limits=['The reason attributed to Bonatus is Lilly\'s conjecture, not a checked quotation from Bonatus. Self-reported success is not blinded evidence.'],kind='source_disagreement')

# Explicitly selected chart fields only. Unreadable/unused numbers remain uncompleted.
CASES={
 'mother_son_1638':{'chart_pdf_page':186,'interpretation_pdf_pages':[187,188,189,190,191],
  'date_inscription':'1638, die Jupiter, 19 July, 23h45 P.M.','calendar_resolved':False,
  'selected_positions':{'Ascendant':['Libra',25,23],'Jupiter':['Libra',27,15],'Moon':['Pisces',26,43],'Sun':['Leo',7,3],'Fortune':['Gemini',15,3]},
  'partial_chart':True,'unresolved_fields':['historical clock notation','Mercury minute field','Mars/cusp minute readings not admitted as exact calculation inputs'],
  'reported_meeting':'July25, approximately15:00; contact asserted approximately14:00',
  'hypothetical_reuses':['neighbour/sibling','unrelated visitor','sudden event','unrelated absent person'],
  'independent_validation':False},
 'surviving_ship_1644':{'chart_pdf_page':196,'interpretation_pdf_pages':[196,197,198],
  'date_inscription':'1644, die Saturn, 28 December, 3h20 P.M.','calendar_resolved':False,
  'selected_positions':{'Ascendant':['Cancer',11,33],'second_cusp':['Leo',9,1],'Moon':['Taurus',16,49],'Sun':['Capricorn',17,54],'Mercury':['Capricorn',17,10],'Mars':['Gemini',19,26]},
  'degree_only_position':{'Jupiter':['Taurus',21,None]},'partial_chart':True,
  'antiscion_claims':['Jupiter to ninth degree Leo/second cusp','Mars to very Ascendant degree'],
  'reported_result':['ship survives','west and harbour','news that night or within two days'],
  'independent_validation':False},
 'lost_ship_1646':{'chart_pdf_page':199,'interpretation_pdf_pages':[199,200],
  'date_inscription':'1646, die Mars, 9 March, 10h15 A.M.','calendar_resolved':False,
  'selected_positions':{'Moon':['Virgo',10,44],'Sun':['Pisces',28,44],'Saturn':['Taurus',16,15]},
  'partial_chart':True,'unresolved_fields':['remaining chart fields not admitted for complete astronomical reconstruction'],
  'reported_result':'much/all invested property lost; inferred wreck reported fulfilled','independent_validation':False}}

ISSUES=[
 ('query_role_switch',[181,185,188],'At-home unrelated person uses seventh; general absent unrelated person uses first. A universal role default loses enquiry context.'),
 ('anchor_event_or_news',[182,200],'Sudden event/first-heard and deliberate request/letter-understanding are distinct clock rules; source does not define all modern interface cases.'),
 ('ruler_strength',[182,189],'Most powerful at Ascendant uses domicile/term/rays in worked example; no numeric resolver or tie rule.'),
 ('mark_gender_asymmetry',[183],'Right-side masculine sign and planet differs from opposite clause feminine sign plus lord in feminine sign.'),
 ('mark_degree_bands',[183],'Few/middle/latter cutoffs unquantified; no equal ten-degree bins inferred.'),
 ('mark_radicality_age',[183,184],'Radicality, sufficient age and clock-quality qualifications not operationally quantified; cannot erase failures post hoc.'),
 ('house_vs_sign_body',[184,189,190],'Face-from-house and body-part-from-sign are separate mappings; several marks can share one underlying indicator.'),
 ('absent_affliction_logic',[185],'Multiple planets in union/opposition and several adverse clauses do not fully specify conflict resolution against survival clauses.'),
 ('absent_news_scales',[186,191],'Default moveable/day table coexists with hypothetical moveable ten-week interval unless known nearby; no near-distance cutoff.'),
 ('case_clock1638',[186],'23h45 P.M. inscription left unresolved; do not convert to modern local or UTC instant.'),
 ('same_figure_reuse',[186,189,190],'Hypothetical teaching uses must not multiply author-reported empirical cases.'),
 ('square_equals_trine',[191],'Long-ascension interpretive equivalence does not change the computed 90-degree relation.'),
 ('ship_all_or',[191],'All-unfortunate heading followed by alternatives has unresolved Boolean grouping; one adverse factor is not silently made a complete rule.'),
 ('ship_reception',[191],'Reception is not assigned an exact pair/type in this passage; mitigation can save only some people, not the ship.'),
 ('ship_parts_polarity',[192],'Fortunate-parts sentence also literally says will receive any detriment; missing negation cannot be silently supplied.'),
 ('ship_dignified_mars',[193],'Essential dignity can strengthen adverse Mars outcome; do not map dignity to good valence globally.'),
 ('ship_star_distance',[193],'Fiery-sign/violent-star qualifier supplies no numerical proximity or catalogue.'),
 ('ship_return',[194],'Retrogradation alone can imply return without loss; return and damage are distinct.'),
 ('ship_sale_grammar',[195],'Head/Jupiter/Venus followed by alternative rulership/dispositorship grammar does not create domicile rulerships for the node.'),
 ('ship_provision_distance',[195],'Removed beyond second and not in second-to-Moon examples resist one exact uniform distance formula.'),
 ('ship_first_chart',[196,198],'Selected chart fields are sufficient only for declared static calculations; Jupiter minute not printed in selected field.'),
 ('ship_mars_antiscion',[196,198],'Mars19:26Gemini reflects10:34Cancer, versus11:33Cancer Ascendant:59arcminutes. Prose says very degree; do not replace either source.'),
 ('ship_jupiter_antiscion',[196,198],'Jupiter is printed at21Taurus without minutes; second cusp9:01Leo. Exact-minute coincidence not established.'),
 ('ship_saturn_location',[196,197],'The first ship narrative calls Saturn eleventh-house; the diagram places Saturn at Aries14:40 alongside a Midheaven cusp Aries14:31. The source house designation and plotted positions need collation; neither is silently replaced.'),
 ('ship_second_void',[199],'Void at question coexists with later contacts, apparently after sign change; do not impose an alternative void rule without source analysis.'),
 ('ship_report_specificity',[197],'Reported west/harbour is broader than proposed southwest coast between Ireland and Wales; no exact geographical verification.'),
 ('clock_self_impartiality',[200,201],'Self-question impartiality is required but cannot be mechanically certified; Bonatus rationale is Lilly\'s conjecture.'),
 ('no_full_scoring',[181,201],'This source inventory and helpers are not a general horary forecast engine or out-of-sample validation.')]

if __name__=='__main__':
    outputs={
      'RULES.json':{'schema_version':2,'batch_id':'B02f','records_count':len(RECORDS),'first_record_number':668,'last_record_number':667+len(RECORDS),'records':RECORDS},
      'QUERY_FRAMES.json':{'source_id':SID,'source_sha256':SHA,'at_home_roles':AT_HOME_ROLES,'general_absent_unrelated_origin':1,'presence_rows':PRESENCE,'ship_roles':SHIP_ROLES,'event_afflictor_examples':EVENT_AFFLICTOR_EXAMPLES},
      'SHIP_PARTS.json':{'source_id':SID,'source_sha256':SHA,'pdf_page':192,'parts':SHIP_PARTS,'modern_safety_use':False},
      'BODY_MARK_REFERENCE.json':{'source_id':SID,'source_sha256':SHA,'pdf_pages':[182,183,184,189,190],'input_roles':MARK_INPUTS,'house_body_explicit':HOUSE_BODY_OPENING,'clinical_use':False},
      'HISTORICAL_CASES.json':{'source_id':SID,'source_sha256':SHA,'cases':CASES,'current_participant_data':False,'empirical_validation':False},
      'TIMING_REFERENCES.json':{'source_id':SID,'source_sha256':SHA,'news_symbolic_units':NEWS_UNITS,'news_symbolic_profile':'Lilly_XXIV_p152_Moon_to_AscendantLord','hypothetical_ten_degree_options':{'ordinary_report':'about ten weeks','known_nearby':'ten days'},'physical_ephemeris_route':'eleventh lord and Ascendant lord sextile/trine','implicit_unit_selection_allowed':False},
      'UNRESOLVED.json':{'issues':[{'id':f'B02f-U{i:02d}','topic':k,'pdf_pages':p,'issue':v} for i,(k,p,v) in enumerate(ISSUES,1)]}}
    for name,obj in outputs.items():save(name,obj)
    print('SOURCE_RECORDS',len(RECORDS),'LAST',667+len(RECORDS),'SHIP_ROWS',len(SHIP_PARTS),'ISSUES',len(ISSUES))
