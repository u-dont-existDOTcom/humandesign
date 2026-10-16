#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def add(pages,label,*clauses):
 sid=f'LXXVI-S{len(SPANS)+1:03}'; ids=[]
 for role,anchor,claim,limits in clauses:
  lid=f'LXXVI-C{len(ROWS)+1:03}'; ids.append(lid)
  ROWS.append({'source_local_id':lid,'batch':'B03v',
   'chapter':'LXXVI' if role!='next_navigation' else 'LXXVII_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'printed_pages':[n-34 for n in pages],
   'role':role,'short_original_anchor_not_diplomatic':anchor,
   'historical_author_paraphrase':claim,'original_conditions_and_uncertainty':limits,
   'global_record_number':None,'historical_documentary_accepted':False,
   'independent_ecclesiastical_outcome_verified':False,
   'empirically_validated_forecast':False,'runtime_rule_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
   'source_passage_label':label,'mapped_local_ids':ids})
add([466],'Chapter heading and question',
 ('heading','LXXVI Priest good Parsonage','The chapter asks whether a cleric obtains a desirable appointment.','Separate from Chapter LXXV before the divider.'),
 ('question','Obtaine a good Parsonage','Outcome is church appointment rather than demonstrated moral worth.','No specific applicant independently identified.'),
 ('authorial_comment','Clergy covetous as others','The opening attacks perceived clergy greed.','Attributed polemic, not general fact.'),
 ('scope','Protestant Presbyter Papist','Lilly says the same question applies across denominations.','Do not assert sect-based character.'))
add([466],'Main actor and benefice assignments',
 ('figure_assignment','Lord first Minister','The first-house ruler signifies the applicant.','Distinct from employer or post.'),
 ('figure_assignment','Moon as applicant','Moon supplies a second applicant significator.','Alternates not identical.'),
 ('figure_assignment','Lord ninth Benefice','The ninth lord signifies the desired church living.','Distinct from candidate.'),
 ('conditional','first Lord or Moon joined ninth Lord','A connection between applicant and ninth ruler is favorable.','Moon OR first lord alternative.'))
add([466],'Favorable ninth house and required effort',
 ('conditional','ninth Lord in ninth or beholds it','Ninth ruler in or aspecting its house is positive.','Two alternatives.'),
 ('forecast','shall obtain Benefice','Lilly forecasts appointment.','No independently documented recipient or decision.'),
 ('qualification','labor pains and industry','Successful appointment may require substantial effort.','Success is not ease.'))
add([466],'Ninth-house placement with obstructive conditions',
 ('conditional','first Lord or Moon ninth','An applicant significator in ninth may be favorable.','Other contacts considered first.'),
 ('exception','Retrograde Combust unfortunate','Source lists conditions reversing favorable reading.','Do not treat ninth placement as sufficient.'),
 ('negative','square to infortune without Reception','Adverse square without reception portends trouble.','Reception is significant.'),
 ('forecast','matter destroyed near completion','Lilly proposes an appointment failing after seeming close.','Not independently authenticated.'),
 ('conditional','ninth Lord in first or applies applicant','Alternative favorable disposition of ninth ruler to applicant.','Distinguish occupancy from application.'),
 ('forecast','procure without much seeking','The author expects easier appointment.','No real outcome supplied.'))
add([466,467],'Favorable first Lord trine/sextile on page seam',
 ('conditional','first Lord trine sextile Sun Jupiter','Specific favorable aspects with Sun or Jupiter are cited.','Keep planet and aspect restrictions.'),
 ('conditional','Sun Jupiter in ascendant','The favorable planet is assumed in rising house.','House qualifier matters.'),
 ('forecast','Benefice or Preferment attained','The combination allegedly secures promotion.','Unverified historical forecast.'))
add([467],'Benefic aspect with reception and no bribery',
 ('conditional','first ninth Lord sextile or trine Reception','Beneficial first–ninth lord aspect with reception is favorable.','Reception is explicit.'),
 ('forecast','without bribe freely by desert','Lilly says the position may be obtained without a payment.','Speculative prediction and moral characterization.'),
 ('conditional','square with Reception','Hard square with reception is a separate outcome branch.','Do not collapse square with sextile.'),
 ('forecast','eventually obtained with contribution to Patron','He expects eventual success after difficulty or financial consideration.','The author mentions possible payment; not an independent bribery case.'))
add([467],'Translation of light and competing applicant',
 ('conditional','planet transfers ninth Lord light to first','A mediating planet carries influence between ninth lord and applicant.','Distinct from direct favorable aspect.'),
 ('forecast','interloping person obtains place','The author conjectures a third person may obtain the appointment.','No independently known competitor.'),
 ('exception','heavier planet carries translator virtue elsewhere','A subsequent transfer to another planet can overturn that reading.','An explicit third-party reversal condition.'),
 ('forecast','matter destroyed when near perfection','He allows a near-complete proceeding to collapse after subsequent contact.','Not a unique predictive case.'))
add([467],'Direct applicant to ninth and competition',
 ('conditional','first Lord applies ninth without obstructive aspect','Direct application without other adverse intervention favors success.','Absence of adverse interim aspect required.'),
 ('forecast','obtains with solicitation','The author expects success but with effort or petitioning.','Distinct from free appointment.'),
 ('method','many significators signal competitors','Multiple planets may represent additional applicants.','Alternative: many difficulties rather than competitors.'),
 ('forecast','many contentions and labours','The process may involve prolonged dispute or work.','Not the same endpoint as losing appointment.'))
add([467],'Malefic conjunction, reception and benefic transfer',
 ('conditional','Lord first conjunct Infortune no reception','A contact to malefic not ruling ninth and lacking reception is adverse.','Original combines two qualifications.'),
 ('forecast','business shall not be performed','Lilly predicts failure under adverse conditions.','No actual appointment result.'),
 ('exception','Infortune commits virtue to strong Fortune','Transfer from adverse planet to strong benefic is said to rescue outcome.','Another conditional reversal.'),
 ('forecast','then shall be perfected','An initially unfavorable matter becomes successful under the exception.','No independently documented candidate.'),
 ('conditional','Infortunes conjunction without Reception','Malefic conjunction without reception is framed as unproductive.','Not all conjunctions.'),
 ('conditional','conjunction with Reception','Reception changes the same adverse configuration to success with difficulty.','Explicit polarity difference.'))
add([467],'Angular, succedent and cadent outcome timing',
 ('conditional','planet effecting angular','The effecting planet in angle allegedly hastens appointment.','Angular placement has particular context.'),
 ('conditional','effecting planet succedent','A succedent position delays the matter.','Delay is not definitive failure.'),
 ('conditional','effecting planet cadent','A cadent effecting planet is claimed to destroy prospect.','Do not collapse cadent and succedent.'),
 ('exception','secret trick succeeds very rarely','Lilly admits a rare unexpected success even when other testimonies fail.','Extremely flexible retrospective exemption.'))
add([467],'Querent dissatisfaction and possible agents',
 ('conditional','malevolent aspects first Lord or Moon square opposition no Reception','Unfavorable square/opposition absent reception is an additional source condition.','Actor and aspect must be kept.'),
 ('historical_inference','querent much troubled','The author conjectures dissatisfaction with proceedings.','No independent personal statement.'),
 ('historical_allegation','negligently or knavishly treated','He attributes suspicion of negligent or corrupt intermediaries.','A reported belief, not proof that real agents were corrupt.'))
add([467,468],'Cooperative dispositors and interruption at folio seam',
 ('conditional','first and ninth Lords commit disposition to another Planet','Both source significators transfer influence to one planet.','Sentence crosses original PDF467–468.'),
 ('condition','receiving planet not impedited Retrograde before sign exit','Freedom from obstruction or retrograde reversal is a qualifier.','Grammar across page seam must be retained.'),
 ('forecast','performance of the business','Lilly interprets the combination as success.','No documentary employment or contract.'))
add([468],'Moon strength, friends and first/ninth–fourth links',
 ('conditional','Moon well dignified','A dignified Moon is linked to outside support.','Not proof of actual friends.'),
 ('historical_inference','many friends','The author expects allies or supporters.','No independently identified witnesses.'),
 ('conditional','ninth Lord joined fourth Lord or reverse','Ninth/fourth lord contact in either direction is an additional favorable rule.','Both aspect directions permitted.'),
 ('forecast','without much labour effecting','Appointment is expected with comparatively little effort.','Outcome ease distinct from obtaining.'))
add([468],'Size and desirability of the benefice',
 ('subheading','worth acceptance or lusty one','The author separately asks whether the appointment is valuable.','Different from whether appointed.'),
 ('figure_assignment','tenth house Lord and planets','The tenth and its ruler/occupants are used to assess the position value.','Ninth represents award; tenth value is different.'),
 ('conditional','tenth planets angular and dignified','Dignified angular planets are positive testimony.','Not all tenth-house occupants.'),
 ('forecast','good thumping Benefice','The author forecasts a lucrative living.','No salary, property or independent appointment documents.'))
add([468],'Original author commentary on clergy, astrology and simony',
 ('authorial_comment','clergy preached against Astrology','Lilly criticizes opponents of astrology among clergy.','Seventeenth-century polemical perspective, not universal fact.'),
 ('authorial_comment','never persuading to Simony','Lilly denies encouraging corrupt purchase of church positions.','Authorial self-claim, not independent verification of conduct.'),
 ('authorial_comment','Astrologo Mastix absurd','The author insults another critic of astrology.','Keep attribution and historical language separate from evidence.'),
 ('source_scope','polemical end of chapter','Closing text is argumentative rather than a worked predictive case.','Do not add empirical case success.'))
add([468],'Next numbered dream chapter boundary',
 ('next_navigation','CHAP LXXVII Of Dreams','A new numbered chapter on dreams starts beneath an ornamental divider.','Navigation only; its planetary dream content is outside LXXVI.'),
 ('next_navigation','whether Dreams signify any thing or not','The following chapter asks whether dream symbolism carries meaning.','Distinct historical source question.'))
assert [r['source_local_id'] for r in ROWS]==[f'LXXVI-C{i:03}' for i in range(1,len(ROWS)+1)]
assert all(r['chapter']=='LXXVI' for r in ROWS[:-2])
assert all(r['chapter']=='LXXVII_NAVIGATION_ONLY' for r in ROWS[-2:])
assert SPANS[0]['original_pdf_pages']==[466] and SPANS[-1]['original_pdf_pages']==[468]
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
def dump(n,obj):
 (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
imgs=[]
for n in (466,467,468):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
 imgs.append({'original_pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
              'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03v','status':'SOURCE_FIRST_ORIGINAL_PROVISIONAL',
 'original_full_pdf_sha256':SHA,'source_units':len(ROWS),'rows':ROWS,
 'independently_verified_appointments':False})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03v',
 'source_spans':SPANS,'span_count':len(SPANS),'source_units':len(ROWS),
 'body_original_pdf_pages':[466,467,468],
 'next_heading_pdf_page':468,'independent_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03v',
 'ordered_ids':[r['source_local_id'] for r in ROWS],
 'cross_page_ids':[r['source_local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_chapter_navigation_only':[r['source_local_id'] for r in ROWS[-2:]]})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03v',
 'original_full_pdf_sha256':SHA,'original_body_pdf_pages':[466,467,468],
 'next_heading_pdf':468,'previous_accepted_lilly':4384,
 'original_images':imgs,'original_printed_pages':[432,433,434],
 'boundary_start':'PDF466 below LXXV chapter divider',
 'boundary_end':'PDF468 above LXXVII dreams divider',
 'next_numbered_chapter':'LXXVII','independent_appointments_verified':False})
ISSUES=[
 'LXXVI starts below original PDF466 divider; ending LXXV content must not be counted.',
 'No named petitioner, granted parsonage, appointment instrument or independently documented result.',
 'First Lord, Moon and ninth Lord are distinct actor/thing significators; keep alternative conjunctions.',
 'Success can require labour; do not conflate winning the position with easy procurement.',
 'An adverse retrograde/combust/square-without-reception condition can reverse ninth occupancy.',
 'Applicant first–ninth trine or sextile with reception differs from square with reception and alleged payments.',
 'The source does not establish actual simony, bribery or clerical misconduct.',
 'Translation of light to a competing person can predict loss, unless subsequent transfer changes the claim.',
 'Multiple significators may mean several competitors OR difficulties; not a single identifiable outcome.',
 'Conjunction with malefic lacking reception is distinct from conjunction with reception.',
 'A malefic transferring to a strong benefic offers an exception to the earlier failure forecast.',
 'Angular haste, succedent delay, cadent destruction and rare secret trick are four different branches.',
 'Troubled petitioner and suspicion of corrupt representatives are authorial hypothetical interpretations.',
 'The shared applicant/post disposition transfer sentence crosses PDF467 to PDF468, with obstruction qualifiers.',
 'Moon being dignified is source testimony about supporters, not evidence of actual friends.',
 'Ninth and fourth lord aspects may promise easy appointment, conditional on other signs.',
 'Tenth house is used for economic size of the post; it differs from whether a post is obtained.',
 'The author comments on clergy and critics of astrology polemically; not externally verified generalizations.',
 'Chapter LXXVII dream interpretation begins below divider on PDF468, excluded from current substantive body.',
 'No independent modern ephemeris parity, blind second source reading, control group or empirical prediction result.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03v','status':'ORIGINAL_SOURCE_LIMITATIONS_RETAIN',
 'issues':[{'id':f'B03v-U{i:03}','issue':v} for i,v in enumerate(ISSUES,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03v','status':'ORIGINAL_HISTORICAL_PROVISIONAL',
 'source_first_annotations':len(ROWS),'original_passages':len(SPANS),
 'prior_accepted_lilly':4384,'new_globally_accepted_source_units':0,
 'author_reported_ecclesiastical_actual_cases':0,
 'independently_authenticated_appointment_cases':0,
 'independently_verified_corruption_cases':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0})
print(json.dumps({'batch':'B03v','rows':len(ROWS),'spans':len(SPANS),
 'limits':len(ISSUES),'body_original_pdf_pages':[466,467,468],
 'next_chapter':'LXXVII','new_accepted':0}))
