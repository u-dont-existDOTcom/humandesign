#!/usr/bin/env python3
"""Lilly 1647 original Chapter LXIII historical source-only extraction."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def entry(pages,label,*items):
 sid=f'LXIII-S{len(SPANS)+1:03}'; ids=[]
 for role,anchor,meaning,limit in items:
  rid=f'LXIII-C{len(ROWS)+1:03}';ids.append(rid)
  ROWS.append({'local_id':rid,'role':role,
   'chapter':'LXIII' if role!='boundary' else 'NEXT_PRINTED_LIV_FISH_STOLEN_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'printed_pages':[p-34 for p in pages],
   'short_original_anchor_not_diplomatic':anchor,
   'historical_author_paraphrase':meaning,
   'source_conditions_and_uncertainty':limit,
   'global_record_number':None,'historical_documentary_admitted':False,
   'empirically_validated_thief_or_case':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
  'source_label':label,'mapped_local_ids':ids})
entry([428],"Chapter LXIII opening and historical source attribution",
 ('heading','CHAP. LXIII. Of Theft.','A numbered original section concerning the proposed astrological significator of a thief.','Source starts PDF428 below LXII divider; no dog-case text included.'),
 ('attribution','received opinion of Master Allen of Oxford','The author initially summarizes a method attributed to Master Allen of Oxford.','Attributed earlier doctrine, separate from Lilly own competing preference.'))
entry([428],"Allen basic peregrine planet criteria",
 ('rule','peregrine Planet in an angle or second house','Allen is quoted as selecting a peregrine planet in an angle or second house.','Additional seventh-house aspect condition must be retained.'),
 ('condition','and beholds seventh house','The chosen planet is required to behold the seventh house under the first rule.','Do not accept any angular peregrine without this condition.'))
entry([428],"fallback seventh lord and Moon aspects",
 ('fallback','if no peregrine Planet be in angle or second','When none meets the initial criteria, the seventh lord becomes a candidate.','Fallback includes seventh lord beholding the seventh.'),
 ('condition','Lord of seventh ... behold seventh','The fallback seventh-house ruler also must aspect its own house in this formulation.','Original source order controls alternative.'),
 ('fallback','otherwise Planet to whom Moon applyes','Failing the seventh ruler, the planet to which the Moon applies can signify thief.','Original adds its own condition beholding seventh.'),
 ('condition','if he behold seventh house','The Moon-applied planet is conditioned on beholding the seventh.','Do not omit scope.'),
 ('limitation','rather if Moon separate from Lord of ascendant','A separation from the ascendant lord introduces a competing lunar relation in the printed text.','Grammatical attachment to prior option unresolved.'))
entry([428],"qualifications and exceptional hour-ascendant overlap",
 ('exception','peregrine in angle shall not signify thief unlesse behold seventh or have dignity degree seventh','Allen demands seventh-aspect or dignity in seventh degree despite peregrine angular position.','Preserve explicit disjunction of aspect or dignity.'),
 ('exception','same Planet Lord of hour and of ascendant','Allen also lists identity of hour lord and ascendant lord as exception to prior constraints.','Original wording seemingly refers to beholding ascendant, not seventh; do not repair.'))
entry([428,429],"Lilly contrary source-priority of houses crossing page",
 ('authorial_priority','I have ever found ... peregrine in ascendant','Lilly states his own preference for peregrine planet in the first house.','Competing source-native preference, not independently verified outcome.'),
 ('authorial_priority','next angle South ... West ... fourth ... second','He orders alternative placements as southern angle, western angle, fourth house, then second house.','Do not collapse south and fourth into one heading without source explanation.'),
 ('conditional','many peregrine Planets in angles, many suspected','He conjectures many suspects when several angular peregrines appear.','Mistrust, suspicion and guilt are not independently established.'),
 ('conditional','conjunction sextile trine ... agreeing; square opposition ... nonconsenting','Aspect condition is associated with suspects acting together or not agreeing.','Attribution and original grammar span PDF428 to PDF429; retain aspect polarity.'),
 ('fallback','ever prefer peregrine nearest cusp of angle','He says to prioritize the peregrine planet nearest the cusp of its angular house.','No numeric closeness threshold or deterministic calculation given.'))
entry([429],"unnumbered worked stolen-money section and date",
 ('subheading','Money lost, who stole it? if recoverable?','A new unnumbered worked money-loss inquiry begins inside Chapter LXIII.','Not new numbered chapter, and not fish-theft case.'),
 ('figure','original round horoscope 24 May 1647','The original circular horoscope gives 24 May 1647 and chart house/planet placements.','Figure has uncertain additional hour characters and no independently verified calculation.'),
 ('figure_date','24 May 1647','The date printed inside the money-loss figure is 24 May 1647.','Do not conflate with a 1638 fish chart on following page.'),
 ('subheading','Judgment upon this Figure','The worked judgment of the theft figure begins below it on PDF429.','Narrative is source-internal and retrospective.'))
entry([429],"questioner physical and character descriptions",
 ('assignment','Mars here ascends and partly represents querent person','Mars is associated with ascendant and questioner.','Mars is not thereby established thief significator.'),
 ('characterization','Mars mind and disposition ... square Mercury and Saturn','The author characterizes querent as arrogant, proud, wasteful and ill-conditioned.','Unverified and ethically unsuitable accusations against historical person.'))
entry([429],"reason for rejecting Mars as thief",
 ('figure_condition','Mars 25 degrees 2 minutes Leo angular','Mars is described angular in Leo at approximately 25 degrees 2 minutes.','Original printed degrees and planetary placement authoritative; no independent ephemeris parity.'),
 ('exception','in own Terms and Decanate','His terms and decan status lead author to refuse Mars for thief identification.','Counterexample to simplistic malefic angular thief inference.'))
entry([430],"Saturn considered but rejected despite western angle",
 ('figure_condition','Saturn angle of West','Saturn is also placed in the western angle.','Angular status alone not proof of thief role.'),
 ('exception','Saturn own Terms and Decanate','The author passes over Saturn because it has its own terms and decan dignity.','Not proof of actual innocence.'))
entry([430],"Mercury selection over angular alternatives",
 ('figure_condition','Mercury 24 degrees 42 Taurus','Mercury is described at roughly 24 degrees 42 Taurus.','No independent ephemeris parity.'),
 ('figure_condition','Mercury lately square Mars, almost conjunct Saturn','The source describes prior square with Mars and near conjunction with Saturn.','Original includes editorial correction of aspect wording.'),
 ('assignment','Mercury peregrine, no essential dignity','Lilly selects Mercury as thief significator based on lack of dignity.','Historical author inference, not established criminal evidence.'))
entry([430],"uncertainty over purported thief sex",
 ('limitation','dispute whether Mercury Male or Female','The author says the alleged thief sex was disputed.','Original angles have mixed masculine and feminine testimony.'),
 ('conditional','Moon masculine and applying masculine Planet in masculine Sign','He uses lunar and planetary masculinity testimony to favor male.','Mercury is described as changeable in nature.'),
 ('authorial_inference','from hence Sex to be Male','Lilly concludes the suspected thief is male.','Not independently validated human inference.'))
entry([430],"age and bodily description conjectures",
 ('authorial_inference','young Youth fifteen or sixteen','A youth of about 15–16 is proposed.','Mercury youth symbolism plus Moon near Sun cited.'),
 ('characterization','thin visaged, hanging eyebrows, long forehead','The suspected youth is described with specific facial features.','Unverified astrological physiognomy.'),
 ('characterization','scars face, poor eyesight, dark hair','The source adds scarring, eyesight and hair conjectures.','Fixed-star claims are historical, not health diagnostics.'),
 ('characterization','scurvy countenance and suspected before','Lilly suggests the boy looked untrustworthy and had prior suspicion.','No independent criminal history; do not validate accusation.'))
entry([430],"neighbor relationship and geographic orientation",
 ('authorial_inference','Mercury with Saturn lord third and fourth','The author infers the suspected youth is a neighbor’s child.','Rulership assignment in original chart unverified independently.'),
 ('authorial_inference','Moon Gemini and Mercury Taurus, opposite or Southwest','He proposes residence opposite the querent or toward southwest.','Original alternatives kept; location not externally authenticated.'))
entry([430],"forecast and alternative accusation dispute",
 ('figure_condition','Fortune rising, Mars in tenth, Moon sextile within four degrees','He uses Fortune and Moon applying sextile to Mars with four-degree separation.','Source geometric claims not independently reconstructed.'),
 ('source_internal_forecast','hear of or recover Money within four days','Lilly predicts learning about or regaining lost money within four days.','Disjunctive hearing-versus-actual-return forecast.'),
 ('reported_dispute','questioner favored Woman-servant and Saturn person','The querent reportedly challenged Lilly and suspected other people.','No authenticated criminal findings about any person.'),
 ('authorial_disposition','refused both suspects as planets dignified','Lilly rejected alternative suspects because their significators were dignified.','Internal case narrative, not external guilt proof.'),
 ('source_internal_reported_outcome','money returned within three days','He claims the stolen money was returned within three days and his description was correct.','One author-reported result, not a prospectively frozen independent accuracy validation.'))
entry([431],"next distinct chapter heading with literal misprinted numeral",
 ('boundary','CHAP LIV. Fish Stolen.','A separate worked stolen-fish horoscope begins original PDF431/printed397.','Literal numeral LIV is printed, although its sequential position after LXIII corresponds to expected LXIV; navigation only, no fish case content.'))
assert len(set(x['local_id'] for x in ROWS))==len(ROWS)
assert [x['local_id'] for x in ROWS]==[f'LXIII-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[428] and SPANS[-1]['original_pdf_pages']==[431]
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
def dump(name,obj):(B/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for n in range(428,432):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
 images.append({'pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
 'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03i','status':'PROVISIONAL_SOURCE_FIRST_NON_ACCEPTED',
 'full_original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_units':len(ROWS),'independent_thief_case_verified':False,'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03i','status':'PROVISIONAL_ORIGINAL_IMAGE_REVERSE_SOURCE_PASS',
 'source_spans':SPANS,'span_count':len(SPANS),'source_units':len(ROWS),
 'original_text_body_pages':[428,429,430],
 'following_heading_pdf':431,
 'complete_second_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03i','status':'PROVISIONAL',
 'ordered_local_ids':[r['local_id'] for r in ROWS],
 'cross_page_ids':[r['local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'heading_boundary_id':ROWS[-1]['local_id']})
dump('SOURCE_FIRST_WINDOW_MANIFEST.json',{
 'batch':'B03i','status':'PROVISIONAL_ORIGINAL_TEXT',
 'original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'original_pdf_body_pages':[428,429,430],
 'original_next_heading_pdf':431,
 'next_heading_exact_original_roman':'LIV',
 'next_heading_logical_chapter':'LXIV',
 'original_page_images':images,'prior_accepted_lilly':3527,
 'author_reported_case_independently_validated':False})
issues=[
 ('PDF428','Chapter LXIII starts BELOW the horizontal divider after LXII dog and general fugitive statements.'),
 ('PDF428','Master Allen of Oxford attributed prior rules and Lilly separate personal preference cannot be conflated.'),
 ('PDF428','Seventh-house aspect, degree-dignity and applying/separating conditions are conjunctive or alternative according to printed syntax.'),
 ('PDF428-429','Conjunction, trine, sextile and square/opposition suspect agreement/disagreement statements cross page and are not validated evidence.'),
 ('PDF429','Original circular figure dated 24 May 1647; clock note difficult to read; no timezone or independent ephemeris parity.'),
 ('PDF429','Querent personality claims are unverified; angular Mars rejected as thief due to terms/decanate.'),
 ('PDF430','Saturn also rejected due own terms/decanate; avoid simplistic malefic-thief mapping.'),
 ('PDF430','Mercury square to Mars and applying bodily Saturn phrase includes self-correction, so do not infer exact orb or conjunction direction.'),
 ('PDF430','Sex of supposed thief acknowledged disputed despite later male inference; never a factual criminal identification.'),
 ('PDF430','Age, health/appearance, greed, and criminal history claims have no independent person records.'),
 ('PDF430','Geographic alternatives opposite/left or southwest and neighbors child are historical author narratives.'),
 ('PDF430','Forecast hearing OR recovering money within four days is not same as certain verified return or identification.'),
 ('PDF430','Author reports money returned within three days; no independent receipts, dated forecast freeze or thief conviction.'),
 ('PDF431','Next distinct source heading literally CHAP LIV Fish Stolen, contrary to logical expected LXIV; do not silently correct.'),
 ('PDF431','Next worked fish case must be kept out of Chapter LXIII and separate from earlier correctly-numbered LIV Buying/Selling.'),
 ('PDF428-431','Source annotations not complete independent diplomatic transcription or empirical horoscope backtest.')
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B03i','status':'PROVISIONAL_ALL_RETAINED',
 'issues':[{'id':f'B03i-U{i:02d}','original_pdf_anchor':a,'issue':v} for i,(a,v) in enumerate(issues,1)]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03i','status':'SOURCE_FIRST_PROVISIONAL_NON_ACCEPTED',
 'source_units':len(ROWS),'image_reverse_passages':len(SPANS),
 'prior_accepted_lilly':3527,'globally_accepted_new_units':0,
 'author_narrated_money_recovery_within_three_days':1,
 'independently_authenticated_thief_cases':0,'new_empirical_predictions':0,
 'new_runtime_model_predicates':0})
print(json.dumps({'batch':'B03i','provisional_source_units':len(ROWS),
 'source_spans':len(SPANS),'original_pdf_pages':[428,429,430],
 'next_heading_original_print':'LIV','next_logical_chapter':'LXIV'}))
