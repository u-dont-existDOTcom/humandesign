#!/usr/bin/env python3
"""William Lilly 1647 Book II Chapter LXXII original historical clauses.
Archbishop William Laud execution: independently real event, NOT verified prospective astrology.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def add(pages,label,*claims):
 sid=f'LXXII-S{len(SPANS)+1:03}'
 ids=[]
 for role,anchor,meaning,caveat in claims:
  lid=f'LXXII-C{len(ROWS)+1:03}';ids.append(lid)
  ROWS.append({'source_local_id':lid,'batch':'B03r','role':role,
   'chapter':'LXXII' if role!='next_navigation' else 'LXXIII_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'printed_pages':[n-34 for n in pages],
   'original_short_anchor_not_complete_quote':anchor,
   'historical_author_paraphrase':meaning,'limits_and_attribution':caveat,
   'global_record_number':None,'historical_documentary_accepted':False,
   'historical_execution_event_verified_independently':role in {'source_internal_reported_outcome','independent_historical_context'},
   'prospective_astrology_prediction_validated':False,'runtime_rule_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),'passage_label':label,
   'mapped_source_local_ids':ids})
add([453],'Separate numbered Canterbury worked chapter and issue',
 ('heading','CHAP LXXII What manner of Death CANTERBURY should dye','The chapter asks about the manner of death of the Archbishop of Canterbury.','Historical case, no independently frozen contemporary question.'),
 ('question','what manner of Death Canterbury should dye','Lilly frames a concern about how the already incarcerated Archbishop might be killed.','Archbishop identity and execution risk publicly known; not a secret event.'),
 ('chart','original circular horoscope printed on page','An original round twelve-house figure accompanies the question.','Do not borrow a preceding spouse-case square chart.'),
 ('chart_date','3 Dec 1644','The center of the original horoscope prints 3 December 1644.','Original 17th-century time/calendar standard not independently reconciled.'),
 ('chart_time','2:24 PM','The center of the figure prints 2:24 PM.','No external prospective chart freeze or witness.'),
 ('chart_annotation','hor astr Sun','The center also records a planetary hour-ruler notation.','Do not infer a separate clock or location.'))
add([453],'Authorial claim of representative chart and historical position',
 ('authorial_claim','none wisest men could better have represented person','Lilly claims the chart powerfully represented Laud and his situation.','Self-evaluated retrospectively; no blind comparison with decoys.'),
 ('context','old man in present state of trouble','The text explicitly references an elderly churchman already involved in political strife.','Known confounder before astrological judgment; no novel risk identification.'),
 ('scope','present state condition and manner of death','The author considers current circumstances and later purported mode of execution.','Current imprisonment and prospective manner must not be scored as one success.'))
add([453],'Ninth-house derived ascendant and Saturn condition',
 ('figure_assignment','Churchman ascendant Capricorn cusp ninth','For the cleric, Capricorn at the ninth-house cusp is used as his derived ascendant.','Not the radical first-house ascendant.'),
 ('figure_assignment','Saturn Lord of sign','Saturn is used as Laud significator through Capricorn rulership.','Do not assign the bishop to the questioner default first lord.'),
 ('figure_condition','Saturn in Aries his Fall','Saturn is described in Aries in its fall.','Period dignity assertion not independently computed.'),
 ('figure_condition','a long time Retrograde','Saturn is said to have been retrograde a long time.','Timing/ephemeris parity not independently performed.'),
 ('figure_condition','Saturn in twelfth, fourth from his ascendant','Saturn is placed in radical twelfth, derived fourth from the cleric ascendant.','Radical/derived house relation essential.'))
add([453],'Source character allegations and public misfortune',
 ('historical_inference','violent spirit, turbulent, envious','Lilly describes the cleric in unfavorable character terms.','Historical opinion, not a verified psychology diagnosis.'),
 ('historical_inference','involved in troubles, imprisoned','The source relates the chart to imprisonment and turmoil.','Already observable public history at December 1644.'),
 ('figure_assignment','Jupiter general significator Church-men','Jupiter is invoked as general significator of clergy.','Separate from personal lord Saturn.'),
 ('historical_context','eminency in Commonwealth','The source emphasizes the public prominence of the churchman.','Pre-existing historical status, no predictive novelty.'),
 ('figure_condition','Jupiter Retrograde fixed Stars Mars and Moon nature','The figure is linked to retrogradation and a class of fixed stars.','Which precise stars/longitudes have not been validated.'),
 ('historical_inference','deep laden with misfortunes and vulgar Clamours','The source describes existing troubles and public condemnation.','Not a prospective forecast; contemporaneous context already known.'))
add([453,454],'Moon fourth versus eighth-from-bishop source page seam',
 ('figure_assignment','Moon Lady of fourth in Figure','The Moon is assigned to the radical fourth house.','Original sentence continues across the physical page boundary.'),
 ('figure_assignment','but eighth as to his ascendant','The Moon also rules the eighth house derived from the ninth-house cleric ascendant.','The two roles must not be conflated.'),
 ('figure_condition','Moon separates from Saturn','Lilly describes the Moon separating from Saturn.','Backward-looking separation, not identical to a future applying aspect.'))
add([454],'Moon opposite Sun near derived eighth and Mars',
 ('figure_condition','Moon applies opposition Sun near eighth cusp','The Moon is said to apply by opposition to Sun near the eighth-house cusp.','Original aspect geometry and precise house referent require verification.'),
 ('figure_condition','Sun in fiery Sign','Sun is described as in a fire sign.','Elemental association is part of source logic, not a clinical mechanism.'),
 ('figure_condition','Sun applies opposition Mars','The Sun is described as applying to an opposition of Mars.','Application direction and linked aspect distinct from Moon-Sun opposition.'),
 ('figure_assignment','Mars Dispositor of aged Bishop','Mars is treated as dispositor of the bishop significator.','Explicit intermediary between Sun and represented person.'),
 ('figure_condition','Mars in Ayery Sign and humane','Mars is described in an airy and human sign.','Original classification untested; preserve literal source language.'))
add([454],'Distinct mode-of-execution forecast, not hanging',
 ('source_internal_forecast','should not be hanged','Lilly says he judged Laud would not be executed by hanging.','Prospective timing and independent forecast documentation absent.'),
 ('source_internal_forecast','but suffer a more noble kind of death','He predicts an alternative execution method termed more noble.','The printed forecast does not explicitly specify beheading by name.'),
 ('source_internal_forecast','within space six or seven weeks or thereabouts','The author gives a broad six/seven-week approximate period.','The qualifier or thereabouts is material; no exact Jan10 prediction.'),
 ('figure_condition','Moon wanted seven degrees of body Mars','He says Moon lacked seven degrees to reach Mars, supplying the claimed interval.','This aspect relation and choice of weeks require ephemeris parity.'))
add([454],'Historical execution outcome and timing comparison',
 ('source_internal_reported_outcome','beheaded about tenth January following','Lilly says Laud was beheaded about 10 January following his December chart.','The historic 10 January 1645 execution is independently corroborated, but not Lilly forecast.'),
 ('independent_historical_context','10 January 1645 Tower Hill','The Bodleian biographical collection independently dates the beheading to 10 January 1645.','Historical event provenance only; does not authenticate a prospective horoscope prediction.'),
 ('date_window_limit','December 3 to January 10 is shorter than six weeks','The actual interval precedes the strict six-week lower bound, but author used or thereabouts.','Do not score as an exact six/seven-week hit without frozen tolerance.'))
add([454],'Author emotional and political disclaimer',
 ('authorial_context','I write not as rejoiced death','Lilly says he did not rejoice in the execution.','Personal authorial claim, not an observed astrological outcome.'),
 ('authorial_context','ever honoured man though never acquainted','He says he respected Laud but never personally knew him.','Authorship stance rather than testimony from a direct personal witness.'),
 ('authorial_context','great uncertainty of humane affairs','He expresses sorrow and calls human affairs uncertain.','This comment cannot be treated as scientific calibration of the forecast.'))
add([454],'Oxford manuscripts, legacy, and contested martyr label',
 ('historical_claim','liberal Maecenas to Oxford, good manuscripts','The author praises Laud as benefactor to Oxford University and collector of manuscripts.','A historical biographical claim, not a predictive rule.'),
 ('historical_opinion','let imperfections be buried in silence','Lilly urges charity in judging faults after death.','Not an astrological prediction.'),
 ('historical_opinion','not a Martyr as one Else did','He rejects a competing description of Laud as martyr.','Contested seventeenth-century political/religious framing.'),
 ('historical_claim','sentence of Parliament brought to his end','The death is described as resulting from Parliament decision.','Historical context of already advanced proceedings, not a surprising unknown outcome.'))
add([455],'Distinct next LXXIII wife portion worked chapter',
 ('next_navigation','CHAP LXXIII If have Portion promised','The following chapter asks about promised wife portion and has its own dated 1634 square chart.','Only heading-navigation, no LXXIII body or outcomes included.'))
assert [r['source_local_id'] for r in ROWS]==[f'LXXII-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[453] and SPANS[-1]['original_pdf_pages']==[455]
assert all(r['chapter']=='LXXII' for r in ROWS[:-1])
assert ROWS[-1]['chapter']=='LXXIII_NAVIGATION_ONLY'
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
imgs=[]
for n in (453,454,455):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';data=f.read_bytes()
 imgs.append({'original_pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
   'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03r','status':'ORIGINAL_SOURCE_FIRST_PROVISIONAL',
 'original_full_pdf_sha256':SHA,'source_units':len(ROWS),
 'event_independently_confirmed':True,
 'prospective_horary_forecast_independently_confirmed':False,
 'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03r','source_spans':SPANS,'span_count':len(SPANS),
 'mapped_source_units':len(ROWS),'body_original_pdf_pages':[453,454],
 'next_heading_pdf':455,'blind_second_transcription_done':False})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03r','ordered_source_local_ids':[r['source_local_id'] for r in ROWS],
 'cross_page_local_ids':[r['source_local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_heading_only':ROWS[-1]['source_local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B03r','original_full_pdf_sha256':SHA,
 'original_body_pdf_pages':[453,454],'next_heading_pdf':455,
 'previous_lilly_accepted':4093,'original_images':imgs,
 'chart_printed_date':'3 December 1644','chart_printed_time':'2:24 PM',
 'external_confirmed_execution_date':'10 January 1645',
 'external_source_kind':'Oxford Bodleian Archives biographical catalogue',
 'external_primary_source':'https://archives.bodleian.ox.ac.uk/dept/scwmss/wmss/online/1500-1900/laudCLD/laudCLD.html',
 'independent_prospective_forecast_freeze':False})
limits=[
 'The original chart is dated 3 December 1644 at 2:24 PM, but a contemporaneously frozen forecast is unavailable.',
 'Laud was already imprisoned and subject to treason proceedings before the original question, a substantial unblinded political risk.',
 'The original seventeenth-century text was published in 1647, after the historical January 1645 execution.',
 'The event date 10 January 1645 is independently confirmed by Bodleian archives, but not the horoscope prediction timing or content.',
 'The author says six or seven weeks or thereabouts, not an exact January 10 date; the historical interval was less than a strict six weeks.',
 'The author says not hanging, rather a more noble kind of death, without explicitly specifying beheading as the predicted mode.',
 'The Moon fourth versus derived eighth house from cleric must not be collapsed into a radical eighth occupancy.',
 'Moon separating Saturn, Moon applying opposition Sun, and Sun applying opposition Mars are distinct temporal aspect claims.',
 'Moon short by seven degrees of Mars is given as source logic; ephemeris, orb and timing conversion are unverified.',
 'The questioner and first forecast-record witness are unknown; source narrative produced post-outcome.',
 'Churchmen represented by ninth-house Capricorn and personal Saturn are separate significator roles.',
 'Saturn in fall/retrograde/twelfth and Jupiter general Churchman attribution are different source conditions.',
 'Fixed-star testimonies are imprecise; no independent stellar longitude parity was performed.',
 'The author descriptions of violence, envy and temperament are historical opinion, not verified psychological evidence.',
 'The author expressly states he had no personal acquaintance with Laud; later praise is not eyewitness evidence.',
 'A statement of respect for Laud and rejection of martyrdom are authorial political perspectives, not predictions.',
 'The method was not compared against baseline probability of a public execution during the known political crisis.',
 'The next original Chapter LXXIII begins on PDF455 with a distinct promised-portion horary figure.'
]
dump("UNRESOLVED_SOURCE_LIMITS.json",{
 "batch":"B03r","status":"SOURCE_LIMITATIONS_OPEN",
 "issues":[{"id":"B03r-U%02d"%i,"issue":v} for i,v in enumerate(limits,1)]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03r','status':'SOURCE_DOCUMENTARY_PROVISIONAL',
 'source_annotations':len(ROWS),'source_passages':len(SPANS),
 'prior_accepted_lilly':4093,'new_globally_accepted_units':0,
 'author_reported_cases':1,'independently_confirmed_historical_events':1,
 'independently_authenticated_prior_forecasts':0,
 'empirically_validated_astrology_predictions':0,'runtime_promotions':0,
 'original_approx_forecast':'6 or 7 weeks or thereabouts',
 'historical_execution':'10 January 1645'})
print(json.dumps({'batch':'B03r','annotations':len(ROWS),'spans':len(SPANS),
 'limits':len(limits),'independent_event':1,'independent_forecast':0}))
