#!/usr/bin/env python3
"""Original Lilly 1647 Book II Chapter LXXIV ninth-house/voyages historical source only.
No live journey, criminal, health or missing-person inference authorized.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def add(pages,label,*clauses):
 sid=f'LXXIV-S{len(SPANS)+1:03}'
 ids=[]
 for role,anchor,paraphrase,limit in clauses:
  lid=f'LXXIV-C{len(ROWS)+1:03}';ids.append(lid)
  ROWS.append({'local_id':lid,'batch':'B03t','role':role,
   'chapter':'LXXIV' if role!='next_heading' else 'LXXV_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'printed_pages':[n-34 for n in pages],
   'short_anchor_not_diplomatic':anchor,'historical_author_paraphrase':paraphrase,
   'source_condition_uncertainty':limit,'global_record_number':None,
   'historical_documentary_accepted':False,
   'independently_authenticated_case_outcome':False,
   'empirically_validated_prediction':False,'runtime_model_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
   'passage_label':label,'mapped_local_ids':ids})
add([456],'Ninth-house preface and Chapter LXXIV heading',
 ('section_preface','The ninth House Long Journeys Religion Pilgrimage Dreams','The text introduces ninth-house travel, religion, pilgrimage and dream questions.','Preface also appeared as B03s next-section navigation; no new predictive claim.'),
 ('heading','CHAP LXXIV Of good or ill in questions concerning this House','Chapter LXXIV begins a new series of ninth-house conditional judgments.','Starts original PDF456/printed422 below preceding source divider.'))
add([456],'General ninth house fortune, governance and testimony',
 ('condition','good Planets governance possession or aspect','Benefics ruling, occupying or aspecting ninth are favorable alternatives.','Source permits rulership, residence OR aspect, not necessarily all.'),
 ('exception','without testimonies of Infortunes','Negative testimony may cancel favorable ninth-house condition.','Absence of malefic testimonies explicitly qualifies original.'),
 ('historical_inference','it signifieth good in all questions concerning this House','The author treats this as general favorable ninth-house testimony.','Not empirical travel or religion outcome.'))
add([456],'Voyage by sea and source favorable/unfavorable testimony',
 ('subheading','Of a Voyage by Sea and successe thereof','A distinct unnumbered sea-voyage subsection starts.','Still within LXXIV.'),
 ('method','look to ninth good and strong','An adequately dignified ninth house is the first favorable sea-voyage condition.','No objective journey risk score.'),
 ('condition','benefic aspects ninth, good planets therein','Favorable aspects or occupation add positive testimony.','Distinct from house strength.'),
 ('condition','Lord ascendant and tenth well affected','Favorable lord of first and tenth add corroboration.','Both specified in especially favorable condition.'),
 ('negative','Saturn or South Node therein','Saturn or lunar node in ninth is said to worsen voyage prospects.','No independent danger probability.'),
 ('negative','Lord ninth joined evil Planet','A malefic contact to ninth lord is an adverse alternative.','Distinguish ruler connection from occupant.'),
 ('historical_forecast','not speed well in way or get wealth','Adversity is applied to progress or financial gain, not just physical safety.','Outcome endpoints must remain separate.'),
 ('negative','Mars in ninth danger by thieves or pirates','Mars in ninth is linked to alleged theft or piracy.','Period statement, no modern travel/security advice.'),
 ('negative','Saturn threaten loss goods or sickness','Saturn is associated with illness or property loss.','No causal medical mechanism.'),
 ('negative','South Node import like Mars with deceit','The lunar node is linked to wrongdoing or misfortune.','Do not assert actual deception from astrology.'))
add([456,457],'Overseas expected gain and separate eighth-house wealth',
 ('figure_assignment','substance of Journey from tenth, second of ninth','The tenth is used as the derived second of ninth for wealth arising from a journey.','Not equivalent to radical second or eighth house.'),
 ('condition','eighth Lord or house strong','A strong eighth house or ruler is also considered for potential gain.','The source gives an additional financial-house test.'),
 ('negative','Saturn Mars or South Node eighth','Unfavorable eighth occupants are associated with no valuable return.','The claim that labor may not be worth the gain is distinct from safety.'),
 ('historical_forecast','nothing worth labour','The author predicts little financial value from the work.','No measured profit records.'))
add([457],'Unnumbered wind direction and severe versus gentle weather',
 ('subheading','What wind you shall have','The source introduces a distinct travel-weather subsection.','Not the same as traveler health or money.'),
 ('condition','Lord ascendant good planets strong friendly aspect','Strong benefic connection is described as favorable wind.','House/dignity and friendly aspect both retained.'),
 ('negative','evil Planets or cadent houses','Malefic/cadent contact is described as unfavorable wind.','Separate unfavorable source alternatives.'),
 ('condition','Significators opposition fixed Signs fixed stars','An opposition in fixed signs near violent fixed stars is linked to severe weather.','Original requires combined conditions, not every opposition.'),
 ('source_internal_forecast','impetuous storms sudden blasts contrary winds','Lilly predicts sudden storms, crosswinds or delays under adverse combinations.','No dated meteorological case.'),
 ('source_internal_forecast','wait days weeks or months for comfortable wind','He conjectures considerable wind-related travel delay.','Time horizon indefinite.'),
 ('condition','Significators trine out of airy signs','A trine involving airy signs is associated with milder gusts.','Specifically mentions Gemini, Libra and Aquarius.'),
 ('historical_forecast','gentle gusts of wind','The source expects relatively mild wind.','No independent weather measurement.'))
add([457],'Journey phases represented by four angles',
 ('subheading','Of him that taketh a Journey and successe thereof','Another unnumbered travel-outcome subsection begins.','Still within Chapter LXXIV.'),
 ('condition','Fortune ascendant','A benefic in rising house is linked to favorable departure.','Beginning of journey only.'),
 ('condition','Fortune midheaven','Benefic midheaven is linked to a favorable middle section.','Mid-journey distinct from starting phase.'),
 ('condition','Fortune seventh','A benefic in seventh is linked to satisfaction at destination.','Arrival not necessarily return home.'),
 ('condition','Fortune fourth','A benefic in fourth is linked to favorable homecoming.','Fourth-house role distinct from seventh.'))
add([457,458],'Jupiter Sun and Saturn classify claimed travel benefit',
 ('figure_assignment','Jupiter Fortune religious or learned person','Jupiter as benefic is associated with help from clergy, judges or people of status.','Original types depend on dignity and house context.'),
 ('figure_assignment','Sun rulership king magistrate or noble','The Sun is associated with support from royalty or officials.','Period social classification, no unique human target.'),
 ('figure_assignment','Saturn ancient man antiquity ground corn tillage','Saturn is tied to older people, land and farming/materials.','Source allows several alternatives, not one exact path.'),
 ('method','follow nature of relevant Planet and house','The author derives aid or occupation from planetary nature.','Flexible symbolic assignment and possible retrospective fit.'))
add([458],'Venus Mercury Moon and Jupiter as kinds of travel profit',
 ('figure_assignment','Venus women joy sport jewellery silk','Venus is associated with favorable help through women, pleasure or textiles/jewels.','Historical alternatives, not one validated profession.'),
 ('figure_assignment','Mercury writing wit merchandize accounts letters','Mercury is linked to writing, trading and communication.','No frozen single-cause classifier.'),
 ('figure_assignment','Moon service news sailor widow gaming','The Moon is linked to services, women, sailors, news and games.','Alternative occupations reflect broad interpretive freedom.'),
 ('method','Planet nature determines what commodity','Planetary classifications are used to propose what business brings benefit.','Context dependence reduces specificity.'))
add([458],'Original source example involving house and planet',
 ('subheading','Example of Fortune in tenth house','An example relates an advantageous outcome to a specific house occupation.','Generic illustration rather than a dated independent case.'),
 ('condition','Venus tenth yields delight or silks jewels','Venus in tenth is given as a favorable benefit source.','Must not confuse this with earlier Venus in eighth wealth.'),
 ('condition','Saturn strong as lord of that house','Saturn in that role changes benefit toward its own nature.','Original is conditional on strength and rulership.'),
 ('negative','Lord twelfth Saturn cold dry illness or treachery','An unfavorable planet ruling twelfth is linked to hardship.','No clinical/culpability evidence.'),
 ('negative','Saturn bestial sign four-footed creature','A bestial sign is used to conjecture an animal-caused event.','No biological inference, only period symbolic correspondence.'),
 ('negative','Saturn humane sign deceitful people','A human sign is linked to interpersonal deception.','Not a factual accusation.'),
 ('negative','Mars hot ailment or thieves','Mars as adverse alternative is linked to ailments or theft.','Multiple failure modes, no observed case.'))
add([458,459],'Unnumbered short/slow return and motion orientation',
 ('subheading','Of the short or slow return of him that taketh a Journey','A subsection separates short from delayed travel and homecoming.','Title occurs on PDF458 and body crosses onto PDF459.'),
 ('condition','swift significator Occidental, Moon movable','Swift significator and movable lunar/sign configurations with occidental status are discussed.','The occidental case involves short but troubled journey.'),
 ('historical_forecast','short but with trouble and pain','The author predicts brevity together with difficulty in this branch.','A short trip is not necessarily a safe trip.'),
 ('condition','swift significator Oriental','Oriental and swift travel significator is the contrasting condition.','Keep motion orientation separate from mere speed.'),
 ('historical_forecast','quick short without labour or trouble','This contrasting case predicts a quick passage with less difficulty.','No observed journey evidence.'))
add([459],'Short return by aspect exchange and transfer of light',
 ('condition','Lord first apply to Lord journeys','A first-house ruler applying to travel-house ruler suggests return.','Directed aspect, not mere copresence.'),
 ('condition','Lord journey applies to Lord first','The reverse application is also allowed.','Source includes alternate direction.'),
 ('condition','planet carries light of one to other','Translation of light is another favorable alternative.','Distinct from direct aspect.'),
 ('condition','Lord journey in ascendant','Placement of the journey lord in rising house favors return.','Different from first/journey lords aspecting.'),
 ('condition','Lord seventh in first or first in seventh','Exchange between first and seventh houses is additional return testimony.','Two possible directions.'),
 ('historical_forecast','short return according length of voyage','Lilly forecasts a comparatively prompt return under these conditions.','Relative, route-length-dependent timing with no unique exact clock.'))
add([459],'Fixed/cadent alternative and benefic travel-house outcomes',
 ('negative','most significators fixed angles, none earlier testimony','Fixed/angular placements without earlier favorable signs indicate lengthy absence or failed journey.','Original explicitly requires absence of the earlier return rules.'),
 ('historical_forecast','destruction Journey or great while absent','He gives destruction or long delay as separate possibilities.','Do not count mere delay as destruction.'),
 ('condition','Fortune ninth','A benefic in the journey house is interpreted as bodily wellbeing.','Original ninth role, not external health diagnosis.'),
 ('condition','Fortune midheaven','Benefic tenth house is interpreted as cheerful or pleasant companions.','Separate from travel health.'),
 ('condition','Fortune seventh fourth','Benefics in seventh/fourth are linked to good outcome and arrival.','Arrival and eventual return remain distinct.'))
add([459],'Fixed, common, Moon first ruler as itinerary complications',
 ('condition','Lord journey in fixed sign','Fixed-sign travel lord is read as lengthy journey.','Original condition not universal guarantee of never returning.'),
 ('condition','Lord journey in common sign','Common/mutable sign can imply changing the planned route.','Interpretive alternative rather than fixed destination.'),
 ('condition','Moon in sixth or opposition Lord sixth','Adverse lunar connection with illness house is invoked for illness and obstacles.','Do not collapse to any Moon position in sixth.'),
 ('exception','first Lord fortunate or house of truth not opposite','Lilly offers mitigating favorable first-house testimony.','This branch allows success despite difficulties.'),
 ('historical_forecast','business succeeds but with many obstructions','The author predicts ultimate success notwithstanding intermediate problems.','Do not score problems and success as a single binary claim.'))
add([459,460],'Long journey return subsection and slow alternatives',
 ('subheading','When he shall return that is gone a long Journey','Another unnumbered subsection asks when a distant traveler comes home.','Begins original PDF459 and continues through PDF461.'),
 ('condition','Lord ascendant in ascendant or midheaven','Placement in first or tenth is interpreted as intention to return.','Do not substitute one for the other without preserving option.'),
 ('condition','first Lord gives power to Planet in these places','Translation of power to an angular occupant is an alternative.','Not simply direct placement.'),
 ('historical_inference','thinking of return','The author infers mental intention to return.','Unverified third-party state of mind.'),
 ('condition','first Lord seventh or angle of earth','Seventh or fourth placements are interpreted as prolonged return.','The original compares delays; not never return.'),
 ('historical_forecast','return prolonged not gone far nor desire','He conjectures the person has not traveled far or yet wanted to return.','Distinct delayed-voyage/intent claims.'))
add([460],'Ninth/third Almuten and ascendant application',
 ('condition','Almuten first in ninth or third applying to planet first','The Almuten of first located in journey house applying to first occupant is interpreted as homeward movement.','Requires Almuten, travel house and application.'),
 ('historical_forecast','is in journey homewards','Author treats this as current return trip.','No tracked traveler case.'),
 ('condition','Lord first eighth or second applying planet tenth','Another source combination is interpreted as return.','Original allows eighth OR second; tenth application matters.'),
 ('negative','first lord cadent without angle application or first aspect','Cadency without angular/ascendant contact is an alternative nonreturn/delay source.','Merely cadent alone does not suffice.'),
 ('historical_inference','tarrying','The source indicates the traveler continues away.','Delay and permanent nonreturn are not equivalent.'))
add([460],'Retrograde return mitigated or blocked by affliction',
 ('condition','first Lord or Moon applies retrograde Planet','Application to retrograde planet can signify reversal homeward.','Requires relation to first and being able to see first house.'),
 ('condition','Lord first itself Retrograde and beholds ascendant','Retrograde first ruler aspecting ascendant is an alternative.','This differs from Moon applying a different retrograde planet.'),
 ('historical_forecast','is coming','Lilly claims return under the retrograde condition.','Unverified third-party location.'),
 ('negative','first Lord unfortunate and impedited','Adverse signification can hinder that return.','This reverses simplistic retrograde means return.'),
 ('historical_forecast','obstacle means tarry or cannot come','He offers either prolonged absence or inability to travel.','Not independently proven permanent inability.'))
add([460],'Moon transfer from first and relationship-derived house',
 ('condition','Moon gives power to first Lord near ascendant','Moon transfer of light to lord near ascendant supports prompt return.','A fallback if the first-lord testimonies are absent.'),
 ('condition','Moon in seventh ninth or third applies first Lord','Specific lunar houses and directed aspect are given.','Each is an alternative condition.'),
 ('condition','Moon separates under earth and applies above earth','A prior beneath-horizon contact followed by an above-horizon application is favorable.','Order of separation then application essential.'),
 ('historical_forecast','returns','The source treats these configurations as return testimony.','No prospective case with verified return.'),
 ('condition','Moon right hand rising and applies midheaven','Right-side Moon application to tenth is linked to slower return.','Source distinguishes right and left side.'),
 ('exception','Moon left hand would return sooner','The alternate lunar hemisphere gives quicker return.','Distinct comparative clock claim without calibrated values.'),
 ('negative','Moon house Lord infortune causes tarrying','An afflicted Moon dispositor modifies the return conclusion.','Might indicate delay rather than never.'),
 ('method','question about Son first use fifth, Brother third, Father fourth','Derived house selection depends on relation of absent person to querent.','Using radical first for everybody is an explicit source error.'))
add([460,461],'Derived traveler condition and angular return corroboration',
 ('method','behold Fortunes in absent person derived house','Planet positions in the selected related house modify absent-person condition.','The preceding source sentence crosses PDF460–461.'),
 ('condition','first Lord in first or second entering first','First-ruler position in first or second approaching ascendant is favorable.','Approaching direction in second is important.'),
 ('condition','first or journey Lord retrograde','Retrogradation of either significator is another favorable source alternative.','Original ties this to actual return only under source scope.'),
 ('condition','first Lord applies tenth Lord, or converse','Directed aspects between first and tenth rulers are offered as return signs.','Both directions explicitly permitted.'),
 ('condition','first Lord tenth or tenth Lord first','Mutual angular placements are alternative return testimony.','Distinct from aspect between rulers.'),
 ('condition','Moon received of tenth Lord or vice versa','Reception between lunar and tenth-house ruler is another option.','Reception directional and conditional.'),
 ('historical_forecast','absent returns speedily shortly','The author expects relatively prompt arrival under these signs.','Source lacks an externally calibrated timeframe.'))
add([461],'Separating, applying and subsequent aspect as past/present/future',
 ('method','first Lord separated Planet speaks of lately past','The planet from which the first lord separates signifies earlier history.','Past event not a future forecast.'),
 ('method','Planet first Lord applying speaks state now','Applying to another planet is used to interpret current circumstances.','Lilly describes present event in his original classification.'),
 ('method','Planet following application speaks future destination','A subsequent application is used as an intended future situation.','Requires chronology of three different planetary contacts.'))
add([461],'Sign ingress, relative fortune and source absence history',
 ('condition','travel significator goes out of one Sign into next','A change of signs is associated with changing location or beginning another journey.','Ingress alone does not establish direction or time.'),
 ('historical_inference','removed from former place or new journey','Lilly conjectures change of route or residence.','No independent case.'),
 ('method','compare which of two signs stronger or fortune','Source asks to compare dignities across before/after signs.','A flexible comparative doctrine with no independent weight.'))
add([461],'Combustion and danger versus news',
 ('negative','Combustion absent person source very ill','Combustion is linked to adversity or captivity.','This is historical high-stakes conjecture, not actual missing-person evidence.'),
 ('historical_allegation','imprisonment or great let','Lilly links combustion to detention and obstruction.','No proof of imprisonment from astrology.'),
 ('condition','Combustion near eighth House or Lord death','A location near eighth or contact eighth lord is given as stronger fatal condition.','This is NOT all combustion.'),
 ('historical_allegation','death except God miraculously deliver','The author offers a death conclusion but includes a miraculous exception.','Unreliable and non-actionable clinical/missing-person claim.'),
 ('condition','Mercury or Moon in ascendant or midheaven','Lilly identifies these planets as news/letter indicators.','Specific angular placement is required.'),
 ('historical_forecast','letters news shall come very shortly','The source predicts correspondence rather than actual traveler arrival.','Do not substitute news with reunion.'),
 ('figure_assignment','Mercury general significator of letters','Mercury is assigned to letters and news.','Source correspondence model, no external mail data.'))
add([462],'Lunar or Mercury prior contact and quality of incoming news',
 ('condition','Mercury Moon separated Fortune','Separation from benefic is treated as good news.','Past separation is the premise, not future application.'),
 ('historical_forecast','good joyful news','The source predicts pleasant correspondence.','No dated observed letter case.'),
 ('condition','separated infortunes','Separation from malefics is contrary testimony.','Opposite polarity from benefic separation.'),
 ('historical_forecast','ill news','Unfavorable news is predicted.','No independent later letter.'))
add([462],'Truth of letter by Mercury sign modality and aspects',
 ('subheading','Whether Letter be true or not','An unnumbered subsection distinguishes rumor/news truth.','Different target from time of arrival.'),
 ('condition','Mercury movable Sign beholds Saturn Mars','Mercury in a movable sign aspecting Saturn/Mars is linked to a false letter.','Conjunctive source condition; not all movable signs.'),
 ('historical_forecast','letter a lie','Lilly claims false information under the condition.','No externally adjudicated real letter.'),
 ('condition','Mercury fixed Sign','Fixed sign is interpreted as more reliable news.','Different from movable-with-malefic condition.'),
 ('historical_forecast','judge it true','The author claims truth.','Historically unverified.'),
 ('condition','Mercury common Sign','A mutable/common sign implies mixed truth.','Do not collapse to fully false.'),
 ('historical_forecast','part true and part false','The source explicitly offers a mixed result.','Very permissive target; not unique evidentiary verification.'))
add([462],'Travel motive inferred from Moon applying planet',
 ('subheading','The cause of a Journey and the successe thereof','The section asks why someone travels.','This is a new unnumbered subsection in the same chapter.'),
 ('condition','Moon applies Sun','An application of Moon to Sun is linked to employment by rulers or elites.','Source uses a directed aspect, not mere conjunction.'),
 ('condition','Moon applies Saturn','Application to Saturn is linked to older people or authority.','Historical social classification.'),
 ('condition','Moon applies Jupiter','Application to Jupiter is linked to clergy or gentry.','Source offers people categories, not verified causes.'),
 ('condition','Moon applies Mars','Application to Mars is linked to military matters.','Not a contemporary justification for conflict.'),
 ('condition','Moon applies Venus','Application to Venus is linked to women or seeking goods valued by women.','Multiple options with broad interpretation.'),
 ('condition','Moon applies Mercury','Application to Mercury is linked to merchants, scholars, languages and travels.','Different motives, no unique cause.'),
 ('condition','Moon herself signifies cause','The Moon alone is treated as indicating public service or hired work.','A source-specific alternative rather than applying to another planet.'))
add([462],'Ninth lord house role gives alternative travel reasons',
 ('figure_assignment','house where Lord ninth is located','The author further classifies motives from ninth lord location.','Planetary application and house location are different tests.'),
 ('conditional','Lord ninth in ascendant','Ninth ruler first indicates traveling by own accord.','Source-native house role.'),
 ('conditional','Lord ninth in second','Ninth ruler second indicates pursuit of gain.','Financial outcome separate from actual travel safety.'),
 ('conditional','Lord ninth in third','Ninth ruler third indicates purposive travel or business.','Original phrase terse; do not force unique action.'))
add([462,463],'Journey success four angular stages and homecoming',
 ('subheading','Success thereof','An additional source heading evaluates phases of journey success.','Distinct from purpose of travel.'),
 ('condition','benefic ascendant','A benefic in first portends favorable beginning.','Arrival cannot be inferred from starting testimony alone.'),
 ('condition','fortunate midheaven','Benefic tenth is used for favorable middle journey.','Different journey phase.'),
 ('condition','fortunate seventh','A benefic in seventh is used for favorable arrival/destination.','Not necessarily successful return home.'),
 ('condition','fortunes fourth','Benefic in fourth signifies favorable homecoming.','The sentence crosses PDF462–463.'),
 ('method','first Lord ninth Lord Moon all well affected','All three astrologically significant roles are expected strong for overall good passage.','Lilly supplies a conjunctive stronger condition.'),
 ('historical_forecast','fortunate Journey','The author predicts an overall favorable journey when conditions agree.','No independently observed traveler result.'))
add([463],'Unnumbered length of journey and variable speed',
 ('subheading','Length thereof','A separate unnumbered subsection addresses trip duration.','Ends above printed Chapter LXXV divider.'),
 ('condition','Lord ninth in ascendant','Ruler of journey house in first is said to shorten journey.','Original does not specify dates.'),
 ('condition','first Lord ninth','First lord in ninth is also given as short-trip testimony.','Reverse angular relation is alternative.'),
 ('condition','Lord first in seventh','First lord in seventh is another haste indicator.','Distinct from absence/return tests earlier.'),
 ('condition','significators cadent or movable Signs','Cadency, movable signs and movable angles are associated with speed.','Some other sections treat cadency differently: source-context vital.'),
 ('condition','angles fixed and significators there','Fixed angles and significators are read as lengthening duration.','Stronger than simple fixed sign alone in source statement.'),
 ('exception','Lord ninth in first swift and fortunate','Quickness and fortunate placement can jointly favor rapid safe voyage.','Trip speed and quality are different endpoints.'),
 ('condition','significators and Moon slow in motion','Slow planetary motion is used for tedious travel.','Not a clock-calibrated variable.'),
 ('historical_forecast','tedious Journey','The author predicts protracted travel under slow testimony.','No observed travel case to validate.'))
add([463],'Next numbered Chapter LXXV boundary',
 ('next_heading','CHAP LXXV If one shall profit by his Knowledge','The following chapter asks whether specialized learning will bring profit.','Navigation only; begins PDF463/printed429 below horizontal divider.'),
 ('next_heading','Chymistry Chyrurgery or perfection','The next heading lists chemistry, surgery and skill.','Do not import following paragraph house judgments into voyage chapter.'))
assert [r['local_id'] for r in ROWS]==[f'LXXIV-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[456] and SPANS[-1]['original_pdf_pages']==[463]
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
assert all(r['chapter']=='LXXIV' for r in ROWS[:-2])
assert all(r['chapter']=='LXXV_NAVIGATION_ONLY' for r in ROWS[-2:])
assert {p for s in SPANS for p in s['original_pdf_pages']}==set(range(456,464))
def dump(n,obj):
 (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for n in range(456,464):
 f=B/'evidence'/f'pdf_1647-{n}.jpg'
 raw=f.read_bytes()
 images.append({'original_pdf_page':n,'printed_page':n-34,
  'path':f.relative_to(B).as_posix(),'bytes':len(raw),
  'sha256':hashlib.sha256(raw).hexdigest()})
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03t','kind':'ORIGINAL_1647_NINTH_HOUSE_CHAPTER',
 'status':'PROVISIONAL_SOURCE_FIRST_NOT_CANONICAL',
 'original_full_pdf_sha256':SHA,'source_units':len(ROWS),
 'source_witness_pdf_pages':list(range(456,464)),
 'no_independent_verified_journey_cases':True,
 'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03t','status':'SOURCE_IMAGE_TO_EDITORIAL_CLAUSE_PROVISIONAL',
 'source_spans':SPANS,'span_count':len(SPANS),
 'mapped_source_units':len(ROWS),
 'body_pdf_pages':list(range(456,464)),
 'following_heading_pdf':463,
 'independent_complete_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03t','status':'ORIGINAL_PAGE_ORDER_PROVISIONAL',
 'ordered_local_ids':[r['local_id'] for r in ROWS],
 'cross_page_local_ids':[r['local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_heading_navigation_only':[r['local_id'] for r in ROWS[-2:]]})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B03t','status':'SOURCE_FIRST_NINTH_HOUSE_ORIGINAL_IMAGES',
 'source_original_full_pdf_sha256':SHA,
 'original_body_pdf_pages':list(range(456,464)),
 'original_printed_pages':list(range(422,430)),
 'start':'Original PDF456 below ninth-house preface: numbered LXXIV',
 'end':'Original PDF463 above horizontal divider; LXXV starts below',
 'next_chapter':'LXXV','next_chapter_pdf_page':463,
 'previous_accepted_lilly':4170,
 'original_images':images,
 'independent_case_outcomes_verified':False})
ISSUES=[
 ('456','Ninth-house preface already appears as next-heading navigation in B03s; the new chapter does not create another independent event.'),
 ('456','The ninth-house initial test includes ruling, occupying or aspecting, plus absence of other adverse testimony.'),
 ('456','Sea voyage positive testimony also requires first/tenth ruler corroboration; do not treat ninth occupancy alone as universal.'),
 ('456','Mars, Saturn and lunar node are distinct alleged voyage danger causes, not independently attested theft or illness.'),
 ('456-457','Derived profit house tenth from ninth versus financial eighth must not be confused with radical second.'),
 ('457','Wind source requires planet strength, friendly/hard aspects, fixed stars and actual sign modality; no calibrated weather forecast.'),
 ('457','The dangerous wind branch names multiple outcomes: storms, crosswinds and delays, not the same event.'),
 ('457','Four angular places classify travel stages; seventh arrival and fourth return are separate endpoints.'),
 ('457-458','Planet-specific assistance categories are extremely broad, flexible alternatives rather than uniquely identifying anyone.'),
 ('458','Original example of the tenth house is generic and not a dated successful voyage.'),
 ('458','Adverse Saturn bestial versus human sign and Mars alternatives are historical allegations, not proof of fraud, assault or sickness.'),
 ('458-459','Short return differentiates occidental versus oriental significator and trouble-versus-no trouble; do not collapse.'),
 ('459','Direct first/journey applications, transfer of light, and house occupation are separate alternatives.'),
 ('459','Source fixed angular branch predicts destruction OR delay, two materially different observable outcomes.'),
 ('459','Fixed versus common signs and Moon with sixth ruler are further conditional pathways.'),
 ('459-460','The long journey return subsection runs across original printed page seam and is not a new numbered chapter.'),
 ('460','The Almuten first, third/ninth house, application to ascendant must all be represented before interpreting homeward journey.'),
 ('460','Cadent without application implies waiting, but other retrograde aspects may reverse conclusion.'),
 ('460','Retrogradation of first Lord or joining retrograde planet must still aspect ascendant; a bad first Lord is an exception.'),
 ('460','Moon right-versus-left ascendant hemisphere is explicitly a relative delay distinction.'),
 ('460-461','For son, brother, father and other absent people the appropriate source derived house changes.'),
 ('461','Separating planet indicates claimed past, present applying planet and next application future; retrospective claims not future forecasts.'),
 ('461','Moving from one sign to another does not uniquely establish change of location; multiple sources can fit.'),
 ('461','Combustion associated with detention, eighth-house exception with death is unfounded and unsafe for real missing people.'),
 ('461','Mercury/Moon in ascendant or midheaven yields news rather than physical return.'),
 ('462','Truth or falsity of a letter depends on Mercury in movable/fixed/common signs and additionally hard planets; source not validated.'),
 ('462','The Moon to Sun/Saturn/Jupiter/Mars/Venus/Mercury categories include many possible journey purposes; not uniquely identifiable.'),
 ('462','Lord of ninth in first, second or third gives different motive assignments; role depends on question context.'),
 ('462-463','Success-phase fourth house statement crosses original PDF462-463 and is distinct from arrival in seventh.'),
 ('463','Journey length distinguishes fast/cadent/movable, slow/fixed and mixed qualities without a reproducible exact time unit.'),
 ('463','Chapter LXXV profit from knowledge begins below the divider and is not source content of LXXIV.'),
 ('456-463','No original independently frozen individual journey or clinical outcome, independent diplomatic second transcription, ephemeris parity or control test.')
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B03t','status':'RETAIN_HISTORICAL_SOURCE_LIMITS',
 'issues':[{'id':f'B03t-U{i:03}','original_page':p,'issue':v}
           for i,(p,v) in enumerate(ISSUES,1)]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03t','status':'HISTORICAL_SOURCE_FIRST_PROVISIONAL_UNADMITTED',
 'original_documentary_annotations':len(ROWS),
 'reverse_source_passages':len(SPANS),
 'original_source_images':len(images),
 'retained_original_source_limitations':len(ISSUES),
 'previous_lilly_accepted':4170,
 'new_globally_accepted_records':0,
 'source_author_reported_concrete_journey_cases':0,
 'independently_authenticated_journey_cases':0,
 'independently_authenticated_wind_or_weather_cases':0,
 'independently_authenticated_missing_person_cases':0,
 'new_empirically_validated_predictions':0,
 'runtime_promotions':0})
print(json.dumps({'batch':'B03t','source_units':len(ROWS),
 'source_spans':len(SPANS),'limits':len(ISSUES),
 'original_pdf_pages':list(range(456,464)),
 'next_numbered_chapter':'LXXV','next_source_pdf':463,
 'new_accepted':0,'empirical':0}))
