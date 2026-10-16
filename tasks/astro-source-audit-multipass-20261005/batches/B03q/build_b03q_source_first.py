#!/usr/bin/env python3
"""Original Lilly 1647 Chapter LXXI husband-at-sea historical case only."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def add(pages,label,*claims):
 sid=f'LXXI-S{len(SPANS)+1:03}';ids=[]
 for role,anchor,meaning,limit in claims:
  lid=f'LXXI-C{len(ROWS)+1:03}';ids.append(lid)
  ROWS.append({'source_local_id':lid,'role':role,
   'chapter':'LXXI' if role!='next_heading' else 'LXXII_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'printed_pages':[p-34 for p in pages],
   'short_original_anchor':anchor,'historical_author_report_paraphrase':meaning,
   'conditions_original_uncertainty':limit,
   'global_record_number':None,'documentary_accepted':False,
   'independently_authenticated_return_case':False,
   'empirical_prediction_validated':False,'runtime_rule_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
   'source_passage_label':label,'mapped_local_ids':ids})
add([451],'Chapter LXXI heading and original figure',
 ('heading','Chap LXXI Woman of husband at Sea','The chapter concerns a wife asking about an absent husband traveling by sea.','New worked case, distinct from preceding spouse mortality case.'),
 ('figure','original square horoscope','Lilly prints a separate square horary figure.','No independent modern ephemeris parity.'),
 ('figure_timestamp','15 April 1645 1:10 PM','The chart center gives 15 April 1645 at 1:10 PM.','Source time convention unverified.'),
 ('reported_question','alive where and when return','The user question asks about status, location and return of absent husband.','Alive, location, hearing news and reunion are distinct outcomes.'))
add([451],'Wife significator and reported condition',
 ('figure_assignment','Mercury Lord ascendant signifies querent','Mercury is assigned to the wife/questioner.','Distinct from Jupiter representing husband.'),
 ('figure_condition','Mercury conjunction Moon and Saturn Aries','Mercury, Moon and Saturn are invoked in the querent description.','Printed source text exact house glyphs have not been independently checked.'),
 ('historical_characterization','face disfigured by smallpox, weak eyes','Lilly reports wife with smallpox marks and weak eyesight.','Source-internal subjective claim, no independent record.'),
 ('historical_characterization','much grief and sorrow for husband','He alleges deep concern for the absent husband.','Her question itself reveals concern; not blind inference.'),
 ('historical_characterization','lisping and ill speech','The author attributes a speech impediment to the wife.','No independent witness or medical validation.'))
add([451],'Husband significator and former voyage',
 ('figure_assignment','Jupiter Lord seventh in tenth','Jupiter is assigned as the husband significator and located in tenth.','Seventh-house derivation essential.'),
 ('figure_condition','Jupiter lately separated sextile Venus in ninth','The source cites a recent favorable Jupiter-Venus aspect.','Separation refers to the recent past, not a future prediction.'),
 ('figure_assignment','Venus Lady third','Venus is described as ruler of third.','Part of his travel inference; not an unrelated natal fact.'),
 ('historical_inference','lately some voyage South-east','The source infers an earlier journey toward southeast.','Same-author retrospective claim, not independently verified.'),
 ('figure_condition','Jupiter swift and not afflicted','Jupiter is judged swift and free of affliction.','Other weakness appears on next page; do not claim unconditionally strong.'),
 ('historical_inference','man was alive and in health','Lilly initially concludes the absent man was living and healthy.','No independent person status verification.'))
add([451,452],'Derived danger houses and adverse past',
 ('figure_assignment','Mercury disposes Jupiter, Lord second eighth from seventh','Mercury is described as disposer and ruler of eighth from the husband derived first.','Do not replace derived eighth with radical eighth.'),
 ('figure_condition','Moon exceedingly afflicted by Mercury and Saturn','The Moon is associated with adverse planets in the wife concern.','Exact aspects and time sequence not independently recomputed.'),
 ('historical_inference','man had been in danger by treachery','Lilly infers a recent threatening experience involving other people.','Unverified accusation against unnamed adversaries.'),
 ('historical_inference','many afflictions during absence','He supposes the man experienced many hardships.','No external logs of voyage or captivity supplied.'))
add([452],'Jupiter with detriment and fixed-star condition',
 ('figure_assignment','Mercury Lord seventh from husbands ascendant','Mercury is recast as ruler of seventh derived from husband.','Derived significator differs from wife role in main chart.'),
 ('figure_assignment','Saturn twelfth from seventh','Saturn is assigned as derived twelfth of absent husband.','Period symbolism, not verification of imprisonment.'),
 ('figure_condition','Jupiter accidentally fortified, not essentially, detriment','Jupiter is described as accidentally stronger but essentially debilitated.','Do not discard essential detriment because of accidental strength.'),
 ('figure_condition','with Oculus fixed Star','A fixed star called Oculus is cited with Jupiter.','No independent stellar longitude/aspect parity.'),
 ('historical_inference','many sudden and violent chances','Lilly interprets the combination as turbulent experiences.','Source-only and retrospectively flexible.'))
add([452],'Direction and source location prediction',
 ('condition','Jupiter more fortified than Moon','Jupiter receives priority over Moon for travel direction.','Comparative strength judgment uncalibrated.'),
 ('condition','Mercury Southerly Sign, Jupiter Gemini West, south quarter','The author combines planet/sign and heaven-quarter directional testimonies.','Do not infer a unique numeric compass bearing.'),
 ('source_internal_forecast','South-west England, some Harbour','He judges the husband was in southwestern England in a harbor.','No independently dated location proof before feedback.'),
 ('figure_condition','Jupiter angular','An angular placement is invoked as support for a settled location.','Historically source-native interpretation.'))
add([452],'Moon separation and short-term rumor',
 ('figure_condition','Moon separates Saturn, applies conjunction Mercury','A Moon movement from Saturn toward wife-significator Mercury is the timing premise.','Separation and applying conjunction are distinct.'),
 ('source_internal_forecast','hear of husband in two or three days','He predicts first news within two to three days.','Hearing news is not physical reunion.'),
 ('timing_condition','Moon distance one degree, Sign movable','He cites roughly one-degree gap and movable-sign character for timing.','A mapping from zodiac degrees to days is asserted, not independently calibrated.'),
 ('source_internal_reported_outcome','so she did hear','Lilly says she did hear something within the short window.','Source self-report, no dated letter or witness.'),
 ('source_internal_reported_outcome','first report husband in Town false','The early rumor was that he was in town but was mistaken.','A genuine report can be FALSE concerning husband location, not a true location success.'))
add([452],'Conjunction May 5 and later reliable news',
 ('figure_condition','Mercury and Jupiter hasten conjunction Gemini','A future joining between wife and husband significators is used.','Source describes the predicted geometry, no ephemeris parity.'),
 ('source_internal_forecast','conjunction fifth of May, certain news or home','Lilly predicts definite news at about 5 May or possible return.','Different date and endpoints than the earlier rumor.'),
 ('source_internal_reported_outcome','second week May heard certain news','The woman reportedly received reliable news during second week of May.','Later than exactly May 5; self-reported and not independent.'),
 ('source_internal_reported_outcome','no actual return until second week July','The husband reportedly returned only in the second week of July.','A return in July is not an on-time May reunion.'))
add([452],'Later reported route and place at question time',
 ('source_internal_reported_outcome','several Voyages West parts','The source states he made several voyages in western England.','Historical source narrative only.'),
 ('source_internal_reported_outcome','taken Prisoner Kings Forces','It reports detention by Royalist forces.','No independent military detention evidence supplied.'),
 ('source_internal_reported_outcome','at time of Question was at Barnstable','The author later locates him at Barnstable (Barnstaple) at query time.','No authenticated original location document or neutral adjudication.'))
add([453],'Separate LXXII header on historical Archbishop case',
 ('next_heading','CHAP LXXII Canterbury manner of death','A new numbered Archbishop of Canterbury case begins on printed419.','Navigation-only; its separate 3 December 1644 horoscope not imported.'))
assert [r['source_local_id'] for r in ROWS]==[f'LXXI-C{i:03}' for i in range(1,len(ROWS)+1)]
assert all(r['chapter']=='LXXI' for r in ROWS[:-1]) and ROWS[-1]['chapter']=='LXXII_NAVIGATION_ONLY'
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
imgs=[]
for n in (451,452,453):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';data=f.read_bytes()
 imgs.append({'original_pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
 'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03q','status':'PROVISIONAL_SOURCE_FIRST',
 'original_pdf_sha256':SHA,'source_units':len(ROWS),'rows':ROWS,'independent_case_outcome_validated':False})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03q',
 'source_spans':SPANS,'span_count':len(SPANS),'source_units':len(ROWS),
 'original_body_pdf_pages':[451,452],'next_heading_page':453,
 'independent_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03q','ordered_ids':[r['source_local_id'] for r in ROWS],
 'cross_page_ids':[r['source_local_id'] for r in ROWS if len(r['original_pdf_pages'])>1]})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03q','original_pdf_sha256':SHA,
 'original_body_pages':[451,452],'next_heading_page':453,'original_images':imgs,
 'previous_lilly_accepted':4052,'original_figure_date':'15 April 1645',
 'original_figure_time':'1:10 PM','independent_case_outcome_authenticated':False})
issues=[
 'Persons and independent correspondence records are unavailable.',
 'Original chart date and time not independently verified.',
 'Wife appearance and prior concern are not blinded information.',
 'Derived house roles are context-specific and must be separately traced.',
 'Jupiter accidental dignity and essential detriment must both be retained.',
 'Planetary positions and fixed star geometry not independently reproduced.',
 'Living/healthy spouse remains a retrospective author report.',
 'Adversary treachery and detention not independently authenticated.',
 'Southwest travel direction is not a unique coordinate.',
 'Source report of location at Barnstable lacks dated external proof.',
 'False first rumor distinguished from actual location.',
 'Hearing early rumor is not accurate location or physical reunion.',
 'Predicted around May 5 versus second week May reliable news are not identical dates.',
 'News second week May and return second week July must not be pooled.',
 'Imprisonment and itinerary narrated retrospectively without separate case file.',
 'No prospective forecast freeze, control charts or second blind source transcription.',
 'Next Archbishop case starts printed419, outside this worked episode.',
 'Period missing-person and health inference is not dependable contemporary practice.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03q','status':'RETAIN_UNRESOLVED',
 'issues':[{'id':f'B03q-U{i:02}','issue':x} for i,x in enumerate(issues,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03q','status':'SOURCE_FIRST_PROVISIONAL',
 'source_annotations':len(ROWS),'source_visual_passages':len(SPANS),
 'prior_lilly':4052,'globally_added':0,
 'early_false_rumor_author_reports':1,'later_reliable_news_author_reports':1,
 'later_person_return_author_reports':1,
 'independent_outcomes_verified':0,'empirical_predictions_validated':0,'runtime_promotions':0})
print(json.dumps({'batch':'B03q','rows':len(ROWS),'spans':len(SPANS),
 'limits':len(issues),'original_pages':[451,452],'next':453}))
