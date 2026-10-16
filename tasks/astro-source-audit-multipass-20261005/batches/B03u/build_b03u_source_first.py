#!/usr/bin/env python3
"""Original 1647 William Lilly Book II LXXV: science/learning, absent persons, travel direction.
First-edition scans have transposed printed folio numbers 430/431; physical sequence is correct.
Historic source assertions only; no independent prospective prediction validation.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
PRINTED_BY_PDF={463:429,464:431,465:430,466:432}
def add(pages,label,*units):
 sid=f'LXXV-S{len(SPANS)+1:03}'
 ids=[]
 for role,anchor,meaning,limit in units:
  id=f'LXXV-C{len(ROWS)+1:03}';ids.append(id)
  ROWS.append({'source_local_id':id,'batch':'B03u',
    'original_pdf_pages':list(pages),
    'printed_page_numerals_as_physically_imprinted':[PRINTED_BY_PDF[n] for n in pages],
    'logical_text_order_pdf_pages':list(pages),
    'role':role,'chapter':'LXXV' if role!='next_chapter_navigation' else 'LXXVI_NAVIGATION_ONLY',
    'short_source_anchor_not_diplomatic':anchor,
    'historical_author_paraphrase':meaning,'source_conditions_uncertainty':limit,
    'global_record_number':None,'historical_documentary_accepted':False,
    'individual_case_independently_verified':False,
    'empirical_forecast_validated':False,'runtime_model_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
   'printed_page_numerals_as_imprinted':[PRINTED_BY_PDF[n] for n in pages],
   'source_passage_label':label,'mapped_local_ids':ids})
add([463],'Numbered Chapter LXXV specialty and profit question',
 ('heading','CHAP LXXV If one shall profit by his Knowledge','A numbered question concerns benefit from an individual\'s acquired specialist knowledge.','Starts original PDF463 printed429 below prior LXXIV horizontal divider.'),
 ('scope','Chymistry Chyrurgery or if he be perfect','Chemistry, surgery and other disciplines are examples of specialism or competence.','No independently measured expertise or clinical performance provided.'))
add([463],'Querent and ninth-house science significators',
 ('figure_assignment','querent ascendant his Lord and Moon','The questioner is signified by first house, its ruler and Moon.','Distinct from the ninth for the skill under consideration.'),
 ('figure_assignment','ninth house its Planet and Lord for Science','Science or knowledge is represented by ninth house and its lord and occupant.','The source separates house, ruler and planet occupancy.'),
 ('condition','Lord ninth fortunate, Oriental or Occidental','The source considers ninth lord strength, orientation and angular status.','Not a single unconditional ninth-lord rule.'),
 ('condition','angle or succedent versus cadent','Angular/succedent or cadent placement are separately considered.','No numerical skill score supplied.'))
add([463],'Favorable knowledge and economic usefulness',
 ('condition','Lord ninth behold Lord ascendant sextile or trine','A favorable aspect between ninth and first lord is supportive.','Original uses sextile OR trine, not arbitrary planetary interaction.'),
 ('condition','Lord ninth Fortune and aspect first','A benefic ninth lord aspecting first is an alternative positive testimony.','Requires actual relation to questioner significator.'),
 ('source_internal_forecast','man has good knowledge and reported true','The author predicts genuine knowledge and accurate reputation under favorable conditions.','No externally verified claimant or knowledge outcome.'),
 ('source_internal_forecast','will do good by knowledge','Lilly adds usefulness or profit from specialization.','Having skill and making financial use of it are distinct endpoints.'),
 ('exception','more if reception','Reception increases the favorable claim.','A conditional modifier, not universally assumed.'))
add([463],'Opposing aspects, unproductive knowledge and infortune',
 ('condition','aspect square or opposition','A square or opposition between significators changes the judgment.','The source allows substantial knowledge but inadequate benefit.'),
 ('source_internal_forecast','knows much but does no good thereby','The author allows high knowledge but failure to profit.','Distinct from knowing little or nothing.'),
 ('condition','infortune afflicts first or ninth lord','Adverse contact from a malefic is another negative premise.','Do not fuse with the hard aspect as always simultaneous.'),
 ('source_internal_forecast','weary himself never perfect desired knowledge','He says effort may be fruitless and mastery remain unattained.','Source conjecture, not actual professional outcomes.'))
add([463,464],'Unnumbered source heading after page boundary',
 ('subheading','Of Science Cunning or Wisdome in a man whether true','An unnumbered subsection separately asks if another person truly possesses claimed knowledge.','The original heading begins at top PDF464, after end PDF463 knowledge-profit clause.'),
 ('witness_page_anomaly','printed PDF464 header 431, not 430','The physical source image in the next scan has printed page numeral 431.','PDF465 subsequently carries printed numeral 430, although source text flows normally from PDF464 to PDF465.'))
add([464],'Science claimed by another and ninth house',
 ('scope','give ascendant him of whom asked','The ascendant is assigned to the person whose ability is queried.','Different from questioner as default first house in prior question.'),
 ('figure_assignment','ninth house for science','The ninth represents the field of knowledge.','No named individual or measured competency.'),
 ('condition','Fortunes ninth or ninth Lord fortunate behold ascendant','Benefics in ninth OR strong ninth lord aspecting first are positive testimony.','Preserve original disjunction and aspect to first.'),
 ('source_internal_forecast','there is Science in that man','The author infers genuine learning under favorable conditions.','Not tested on independently assessed real expertise.'),
 ('condition','infortunes ninth or ninth Lord unfortunate and not behold first','A negative condition uses adverse ninth testimony with lack of first-lord aspect.','Both adverse ninth position and failure to behold first are material.'),
 ('source_internal_forecast','no or little knowledge','Lilly draws a negative skill assessment.','Does not independently demonstrate incompetence.'))
add([464],'Moon and ninth Lord applying good versus evil',
 ('condition','Moon and Lord ninth apply fortunes','Moon and ninth lord applying to benefics support actual knowledge.','Original needs both Moon and ninth lord relationship.'),
 ('source_internal_forecast','knowledge in the man','The claim is that the person knows the field.','No observable skill scoring.'),
 ('condition','Moon and Lord ninth apply infortunes','Malefic application gives negative knowledge testimony.','Distinct from no ninth-to-first aspect.'),
 ('source_internal_forecast','contrary to knowledge','The author draws an unfavorable conclusion.','No observed outcome.'),
 ('condition','ninth and lord unfortunate nor behold ascendant','The source repeats combined adverse ninth and absent first aspect testimony.','If this is about querent versus someone else, role selection changes.'),
 ('historical_inference','knowledge useless even if claimant has some','The source allows some knowledge without useful application.','Preserves economic usefulness versus competence distinction.'))
add([464],'Unnumbered multiple absent people inquiry',
 ('subheading','Of many Persons absent or travelling in what Condition','A new unnumbered subsection introduces multiple absentees whose circumstances are asked about.','Begins original PDF464, after the knowledge-authenticity rules.'),
 ('scope','four or five or more travelling in a company','The inquiry can cover a group of several people overseas or distant.','The people are hypothetical; no identified genuine travellers.'),
 ('method','querent write all names in order','Lilly requires an ordered list of the absentees.','Participant enumeration sequence matters for the claimed algorithm.'))
add([464],'Sequential lunar applications assign people',
 ('method','Moon first application first listed man','The Moon first applying planet is used for first listed person.','The ordering depends on the list; cannot infer real status.'),
 ('method','check position dignity aspects separation application','The author instructs evaluation of the planet dignity and contacts for condition.','Planetary context, separating and applying phases remain separate.'),
 ('historical_allegation','health and welfare of first man','The author\'s projected result includes the first person\'s circumstances, health and safety.','No independent real missing-person or clinical evidence.'),
 ('method','Moon second application second named man','A second lunar application gives second person.','Not an independently measured state.'),
 ('historical_allegation','second person\'s state by fortune or affliction','The author infers a second person\'s circumstances from next planet.','Source statement continues across PDF464 to PDF465.'))
add([464,465],'Multiple absentee sentence carried across swapped printed folio numbers',
 ('source_seam','how well / or ill being of that Planet','The first PDF464 line ending regarding the second person\'s condition continues on PDF465 with favorable or unfavorable testimony.','The physical scan order is correct even though printed folios read 431 then 430.'),
 ('method','successive Moon applications for later people','The author proposes following Moon applications to third, fourth and further absentees.','This is a sequential allocation convention, not real observations.'))
add([465],'Cycling through numerous persons and women',
 ('condition','consider retrogradations directions combustions','Lilly includes motion, directions and combustion when classifying later persons.','Each is another source qualifier, not a verified person outcome.'),
 ('method','repeat Moon application sequence if more than seven','He instructs repeating the cycle if the list exceeds seven persons.','Cycling introduces multiple possible interpretations rather than unique identification.'),
 ('scope','also Man asking after many Women','The same sequence is applied when a man asks about several women.','Historical gender framing; no case cohort.'))
add([465],'New subsection: best travel direction',
 ('subheading','To what part of Heaven Traveller had best direct Journey','A separate unnumbered section considers which compass quarter someone should travel toward.','Still Chapter LXXV; some ideas recur from earlier general travel methods.'),
 ('reported_question','to what part of World best for me to travel','The source describes an ideal-direction question.','No independent comparison among possible destinations.'),
 ('method','locate where fortunate Planets placed, most fortified','Lilly favors quadrants containing strong benefics.','This is broad source doctrine, not safe modern travel advice.'))
add([465],'Compass quadrant associations and opposite adverse warning',
 ('conditional','Fortune east quadrant travel eastward','East-quadrant benefic planets are associated with eastward travel.','Planet strength and favorable status assumed.'),
 ('conditional','Fortune south quarter travel southward','South quadrant is linked to southerly travel.','No map coordinate or distance given.'),
 ('conditional','Fortune west quadrant travel westward','West quadrant is linked to westerly travel.','Independent of seasonal weather and route.'),
 ('conditional','Fortune north quadrant travel northward','North quadrant is linked to northerly travel.','No measured comparison.'),
 ('method','choose quarter with greatest number fortunes','A plurality of strong benefics can dominate choice.','Does not specify a deterministic weighting for exact degrees or houses.'),
 ('negative','avoid quarters where Infortunes posited','The source discourages choosing an adverse quadrant.','Unsafe to infer actual hazards from positions.'),
 ('condition','include South Node among Infortunes','Lilly specifically adds the lunar south node as adverse.','Period symbolic source only.'))
add([465],'Second versus eighth wealth when settling or returning',
 ('figure_assignment','second and eighth Houses special care','The text treats these two financial houses as separate outcomes.','House choice changes depending on staying abroad versus return.'),
 ('negative','adverse eighth gives little gain in country going to','An unfavorable occupant in eighth predicts little material success at destination.','Not a real trade or employment comparison.'),
 ('negative','adverse second gives poor results after returning','Malefic second occupancy is linked to financial difficulty back home.','Distinct destination-house role from eighth.'),
 ('condition','good eighth for fortune in foreign destination','The source elects fortunate eighth for successful settlement abroad.','An electional example, not an observed scenario.'),
 ('condition','good second to live happily after return home','Favorable second-house condition is contrasted for happy circumstances after returning.','Sentence spans physical PDF465–466.'))
add([465,466],'Closing original sentence and south-node exception',
 ('source_seam','fortunate Planet / is in the second','The final original choice of favorable second-house placement continues onto PDF466.','Underlying scan text continuous despite swapped prior printed numbers.'),
 ('negative','beware Cauda in second on return or eighth when setting forth','Lilly warns about lunar south node in second for return and eighth for departure.','Two stages and houses; no independent financial outcome or travel hazard.'))
add([466],'Next distinct numbered Chapter LXXVI',
 ('next_chapter_navigation','CHAP LXXVI If an idle covetous Priest ... good Parsonage','A new numbered chapter concerns a cleric seeking an ecclesiastical benefice.','New chapter begins after horizontal divider on original PDF466, printed432.'),
 ('next_chapter_navigation','whether he shall obtain Parsonage','The subject changes from general science, absentee and direction rules to an appointment question.','Heading only, no following LXXVI claims admitted into LXXV.'))
assert len(ROWS)==len({r['source_local_id'] for r in ROWS})
assert [r['source_local_id'] for r in ROWS]==[f'LXXV-C{i:03}' for i in range(1,len(ROWS)+1)]
assert all(r['chapter']=='LXXV' for r in ROWS[:-2])
assert all(r['chapter']=='LXXVI_NAVIGATION_ONLY' for r in ROWS[-2:])
assert [sp['original_pdf_pages'][0] for sp in SPANS]==sorted(sp['original_pdf_pages'][0] for sp in SPANS)
assert [PRINTED_BY_PDF[i] for i in (463,464,465,466)]==[429,431,430,432]
def dump(n,obj):
 (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for n in (463,464,465,466):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
 images.append({'original_pdf_scan_id':n,'printed_folio_as_scanned':PRINTED_BY_PDF[n],
  'path':f.relative_to(B).as_posix(),
  'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
SOURCE_SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03u','status':'ORIGINAL_SOURCE_FIRST_PROVISIONAL_UNADMITTED',
 'source_original_full_pdf_sha256':SOURCE_SHA,'source_units':len(ROWS),
 'original_scan_text_order':[463,464,465,466],
 'imprinted_printed_folio_numbers':[429,431,430,432],
 'independent_expertise_or_journey_cases_verified':False,
 'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03u','status':'ORIGINAL_IMAGE_SOURCE_REVERSE_COVERAGE_PROVISIONAL',
 'source_spans':SPANS,'span_count':len(SPANS),'source_units':len(ROWS),
 'original_scan_order':[463,464,465,466],
 'imprinted_printed_folio_numbers':[429,431,430,432],
 'independent_blind_full_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03u','status':'TEXTUAL_ORDER_DIFFERENT_FROM_IMPRINTED_PAGE_NUMBER_ORDER',
 'ordered_local_ids':[r['source_local_id'] for r in ROWS],
 'page_crossing_local_ids':[r['source_local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_heading_only':[r['source_local_id'] for r in ROWS[-2:]]})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B03u','status':'PRIMARY_1647_SCANS_ORDER_FROZEN',
 'original_full_pdf_sha256':SOURCE_SHA,'original_scan_order':[463,464,465,466],
 'original_imprinted_page_numerals':[429,431,430,432],
 'imprinted_folio_transposition':'Scans PDF464 and PDF465 preserve TEXT order, but imprinted numerals 431 and 430 appear reversed. Do not reorder scans.',
 'boundary_start':'Original PDF463/printed429 after LXXIV divider',
 'boundary_end':'Original PDF466/printed432 above LXXVI divider',
 'next_chapter':'LXXVI','next_chapter_pdf':466,
 'original_images':images,'previous_lilly_accepted':4323,
 'full_second_independent_diplomatic_transcription':False})
LIMITS=[
 ('PDF463','Chapter LXXV begins after previous travel-length horizontal divider; earlier voyage rules cannot be double-counted.'),
 ('PDF463','Positive skill vs actual economic usefulness are distinct outcomes; square/opposition may mean knowledge without benefit.'),
 ('PDF463','Benefic ninth, ninth Lord dignity, aspects and reception are conditional, not independently observed competence.'),
 ('PDF463-464','The page-end fragment Of carries into the unnumbered Of Science subsection at PDF464; no missing section.'),
 ('PDF464','CRITICAL: original PDF464 has imprinted folio 431, even though it follows PDF463/printed429 coherently.'),
 ('PDF465','CRITICAL: original PDF465 has imprinted folio 430, but text continues directly from original PDF464, so DO NOT swap image order.'),
 ('PDF464','Knowledge verification is based on querent vs quesited first-house role and ninth house, not a single stable birth-chart predicate.'),
 ('PDF464','True competence, low competence and useless competence are different outcomes with broad symbolic conditions.'),
 ('PDF464','Moon and ninth Lord applying favorable/unfavorable are two separate source alternatives requiring direction.'),
 ('PDF464-465','Lunar first, second and later applications represent named travellers in their listed order; source does not supply real named cases.'),
 ('PDF464','The many-absentees rules assert status and health; no independent missing-person outcome supports use in reality.'),
 ('PDF465','Cycling lunar applications for groups longer than seven introduces ambiguity and retrospective flexibility.'),
 ('PDF465','The directional quadrants are relative to the horoscope with no unique compass longitude or verified trip utility.'),
 ('PDF465','Source says preferential travel in quadrant with most fortunes and disfavor infortunes; not measured itinerary guidance.'),
 ('PDF465','Malefic eighth and second yield distinct financial outcomes in destination vs home; do not conflate them.'),
 ('PDF465-466','The closing favorable second-house return statement spans the physical scan boundary; both original JPEG IDs needed.'),
 ('PDF466','The printed rule about lunar south node specifies different houses on return and on setting forth.'),
 ('PDF466','Following ecclesiastical appointment question is distinct numbered Chapter LXXVI; no priest-case body admitted here.'),
 ('PDF463-466','Original 1647 printed folios 430 and 431 are transposed while scanned source text continuity is intact; later transcript normalized numbering is secondary.'),
 ('PDF463-466','No named skills test, payment proof, actual group travelers, contemporaneous forecast freeze, control panel or independent full diplomatic second transcription.')
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B03u','status':'ALL_SOURCE_ISSUES_RETAINED',
 'issues':[{'id':f'B03u-U{i:02}','source_window':page,'issue':x}
           for i,(page,x) in enumerate(LIMITS,1)]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03u','status':'SOURCE_FIRST_PROVISIONAL_NOT_CANONICAL',
 'original_historical_source_annotations':len(ROWS),
 'original_reverse_passages':len(SPANS),
 'retained_original_source_issues':len(LIMITS),
 'previous_accepted_lilly':4323,
 'new_globally_accepted_units':0,
 'separately_verified_competency_cases':0,'separately_verified_traveler_cases':0,
 'separately_verified_economic_outcomes':0,
 'empirically_validated_astrology_predictions':0,'runtime_promotions':0,
 'imprinted_folio_numbers':[429,431,430,432],
 'original_textual_scan_order':[463,464,465,466]})
print(json.dumps({'batch':'B03u','source_units':len(ROWS),
 'source_spans':len(SPANS),'retained_source_limitations':len(LIMITS),
 'pdf_scan_order':[463,464,465,466],
 'printed_folios_as_scanned':[429,431,430,432],
 'next_chapter':'LXXVI','source_only':True}))
