#!/usr/bin/env python3
"""Lilly 1647 Book II Chapter LXV: Waller-Hopton 29 March 1644, historical source only."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[]
SPANS=[]
def add(pages,label,*items):
 sid=f'LXV-S{len(SPANS)+1:03}'
 ids=[]
 for role,anchor,meaning,limit in items:
  rid=f'LXV-C{len(ROWS)+1:03}'
  ids.append(rid)
  ROWS.append({
   'local_id':rid,'role':role,
   'chapter':'LXV' if role!='boundary' else 'LXVI_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),
   'original_printed_pages':[p-34 for p in pages],
   'source_abbreviated_anchor_not_full_quote':anchor,
   'historical_author_claim_paraphrase':meaning,
   'source_conditions_and_limitations':limit,
   'global_record_number':None,'historically_admitted':False,
   'source_case_independently_authenticated':False,
   'empirical_astrological_prediction_validated':False,
   'runtime_rule_promoted':False
  })
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
   'source_passage_label':label,'mapped_local_ids':ids})
add([433],"numbered LXV heading and disputed Battle of Alresford",
 ("heading","Chap. LXV. Waller or Hopton should overcome","A distinct numbered Chapter LXV presents a question about two military commanders.","Begins PDF433/printed399 below Fish Stolen divider."),
 ("reported_question","whether Waller or Hopton should overcome","The question is framed as comparing the possible outcomes for Sir William Waller and Sir Ralph Hopton.","Historical military question, not actionable combat guidance."),
 ("original_event_setting","supposed engaged neer Alsford","The armies were said to be supposed engaged near Alsford/Alresford.","Source suggests contemporaneous expectation, not independent proof of battle start time."),
 ("figure_date","29th March 1644 heading","The printed heading explicitly dates the question 29 March 1644.","Keep civil-date and old-style calendar context, not a verified prediction timestamp."))
add([433],"own square original war figure and date-time",
 ("figure","square horary 29 Mar 1644","The source prints its own square twelve-house military horoscope.","Not the fish-theft square diagram above the divider."),
 ("figure_time","29 Mar 1644 10:12 AM","The original chart centre gives 29 March 1644 at 10:12 AM.","The enlarged original source reads Mar, consistent with heading, not May; timezone not established."),
 ("figure_context","Moon, Venus and Mercury aspects in figure centre","The diagram contains shorthand aspects used in the later judgment.","Exact degrees, orbs and sign placements have not been independently ephemeris reproduced."))
add([433],"parliamentarian army and command assignments",
 ("figure_assignment","ascendant for our Army","Lilly takes the ascendant as significator of his favored army.","The author's political allegiance is explicit; judgments are not blinded."),
 ("figure_assignment","Moon Jupiter Venus for our Generals","The Moon, Jupiter and Venus are allocated to Waller's commanders.","Involves distinct planets, not a single victory indicator."),
 ("historical_identity","Sir William and Major General Browne","Sir William Waller and Major General Browne are named as generals.","Historical reference only, not personal chart of either commander."))
add([433,434],"opposing commander, seventh house and reinforcements",
 ("figure_assignment","Sir Ralph Hopton Saturn Lord seventh","Saturn as seventh lord represents Sir Ralph Hopton.","Original status distinct from army's sign."),
 ("figure_assignment","enemy Army by Capricorn descending","Capricorn on the descendant is assigned to Hopton's army.","The sentence crosses original PDF433-434, so both pages are referenced."),
 ("figure_assignment","ninth house enemy friends and assistants","The ninth-house region is used for opposing reinforcements.","Unusual tactical-house assignment stays source-specific, not an operational rule."),
 ("figure_condition","only Mars and South node ninth","Mars and a lunar node in the ninth are used to argue few reinforcements.","The author predicts no ready assistance; this is not a validated logistics assessment."),
 ("historical_outcome_forecast","Hopton had no supplies ready","Lilly infers insufficient immediate reinforcement for the opposing side.","Source claim only, not independently observed evidence."))
add([434],"Moon, Jupiter and Sun conditions favoring army",
 ("figure_condition","Moon exaltation eleventh with Jupiter","The Moon is described exalted, in the eleventh with Jupiter.","Original printed dignity/house assertions not ephemeris verified."),
 ("historical_forecast","I concluded all was well and victory ours","Lilly states that he favored the army represented by the ascendant.","A reported first-person conclusion, not independently frozen forecast."),
 ("figure_condition","Moon separation from Jupiter","Moon's separating from Jupiter is used to infer already performed service.","This is a judgment about past/perceived events, not a future prediction."),
 ("historical_inference","already gained some ammunition","The author infers his side had already acquired matériel.","The actual acquisition timing relative to the question is unverified."),
 ("figure_condition","Sun tenth in degree of exaltation","Sun in tenth with exaltation is added as favor to the army's auxiliaries.","No independent raw chart parity."),
 ("historical_inference","victory accompanied by further successes","The author interprets combined dignities as favoring success.","Qualitative strength, not validated probability."))
add([434],"Saturn Sun proximity qualifies scope of claimed victory",
 ("exception","proximity of Saturn to Sun","Lilly says Saturn's closeness to Sun reduces prospects of total victory.","Preserve this negative qualification, rather than claiming wholly decisive result."),
 ("historical_forecast","not gaine whole, or perfect victory without diminution","He expressly allows a success with some diminution or incomplete scope.","The original later narrative emphasizes captured prisoners/ammunition, not an independently confirmed total rout."),
 ("historical_forecast","considerable proportion of Ammunition","The forecast includes obtaining a substantial amount of ammunition.","Source-internal military material expectation, not advice."))
add([434],"Moon applying Venus then Mercury and timing forecast",
 ("figure_condition","Moon applying to Venus","The Moon is said to apply to Venus.","First event in a two-step application argument."),
 ("figure_condition","then Moon sextile Mercury angular","The Moon is then expected to apply by sextile to angular Mercury.","Do not collapse into simultaneous Venus-Mercury aspect."),
 ("source_internal_forecast","perfect good news within eleven or twelve hours","Lilly claims to have predicted favorable news within about 11–12 hours of question.","No independently documented delivery time or prospective recording."),
 ("timing_context","battle within fifty miles of London","He selects hours rather than days partly because the conflict was close to London.","Source-specific judgment and distance premise, not an algorithm for conflicts."),
 ("timing_measure","Moon distant Venus eleven degrees, swift increasing light","He cites eleven degrees of Moon-Venus separation and the Moon's swift increasing light.","No independent degree parity; precision of derived hours unverified."))
add([434],"letter and prisoner/ammunition report",
 ("source_internal_reported_outcome","same Friday Letter came from Army","Lilly says an army letter on that Friday reported favorable results.","Original account only; source does not give exact arrival hour."),
 ("source_internal_reported_outcome","Thursday before one hundred twenty Commanders","The letter reportedly said 120 opposing commanders or gentlemen were captured the preceding Thursday.","Original narrative counts uncorroborated by this document."),
 ("source_internal_reported_outcome","five hundred sixty common Souldiers","The letter reportedly described 560 ordinary soldiers taken.","Do not substitute independent military casualty data without separate sources."),
 ("source_internal_reported_outcome","much Ammunition","Large ammunition captures were also reported.","Qualitative source outcome, not a measured victory percentage."),
 ("historical_assessment","Enemies routing","The author describes defeat and retreat of the opposing troops.","Source-internal; do not infer full permanent defeat."))
add([434],"adverse testimonies assigned to Hopton's significator",
 ("figure_condition","Saturn Hopton significator sub radiis","Saturn is said to be under the Sun's rays.","One of several historical adverse conditions, not direct combat observation."),
 ("figure_condition","Saturn in Fall","A Saturn essential debility is stated.","No numerical weight or independent chart calculation."),
 ("figure_condition","Saturn wholly peregrine, no aspect of any Planet","Lilly asserts absence of effective favorable aspects to Saturn.","Source-native unfortified condition with glyph and orb limitations."),
 ("figure_condition","Saturn beholds cusp seventh by dexter square","He links Saturn's dexter square to the seventh cusp to defeat and dishonor.","Original chart/degree details not independently verified."),
 ("historical_inference","disadvantage to army and commander","He argues these conditions indicate loss and dishonor for the opposing side.","An author's astrological inference, not independently established attribution."))
add([435],"next distinct Reading siege chapter heading, navigation only",
 ("boundary","CHAP. LXVI. Essex to take Reading","A new chapter asks whether Robert Earl of Essex would take Reading while surrounding it.","Starts PDF435/printed401 at top after page break; no Reading siege rules imported into LXV."))
assert len(set(r['local_id'] for r in ROWS))==len(ROWS)
assert [r['local_id'] for r in ROWS]==[f'LXV-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[433] and SPANS[-1]['original_pdf_pages']==[435]
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
def dump(n,x):
 (B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for n in [433,434,435]:
 f=B/'evidence'/f'pdf_1647-{n}.jpg'
 data=f.read_bytes()
 images.append({'pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03k','status':'ORIGINAL_SOURCE_FIRST_PROVISIONAL',
 'source_full_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_units':len(ROWS),'source_case_independently_authenticated':False,'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03k','status':'MANUALLY_COLLATED_ORIGINAL_SOURCE',
 'source_spans':SPANS,'span_count':len(SPANS),'source_units':len(ROWS),
 'original_chapter_body_pdf_pages':[433,434],
 'next_heading_pdf_page':435,
 'second_diplomatic_reader':False})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03k','status':'PROVISIONAL',
 'ordered_local_ids':[x['local_id'] for x in ROWS],
 'cross_page_ids':[x['local_id'] for x in ROWS if len(x['original_pdf_pages'])>1],
 'next_heading_only':ROWS[-1]['local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B03k','status':'PROVISIONAL_SOURCE_FIRST',
 'full_original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'chapter':'LXV','source_body_pdf_pages':[433,434],
 'opening':'Original PDF433 lower BELOW Fish Stolen divider',
 'closing':'Original PDF434 bottom before PDF435 Chapter LXVI',
 'next_heading_pdf_page':435,'next_chapter':'LXVI',
 'original_page_images':images,'prior_accepted_lilly':3630,
 'chart_original_date':'29 March 1644',
 'chart_original_time':'10:12 AM',
 'independent_case_authentication':False,
 'blind_diplomatic_second_transcription':False})
issues=[
 ('PDF433','Chapter LXV begins below the Fish Stolen divider, whose originally printed heading is LIV but sequentially LXIV.'),
 ('PDF433 figure','Enlarged primary witness reads 29 Mar 1644, not May; heading and figure agree but time/location basis unverified.'),
 ('PDF433','They were supposed engaged; actual battle onset and information known to querent at question time are not independently frozen.'),
 ('PDF433-434','Ascendant is assigned to Lilly preferred army; political allegiance makes this source a non-blind historical judgment.'),
 ('PDF433-434','Unusual ninth-house assignment for enemy reinforcements is source-specific and not an operational battle rule.'),
 ('PDF433-434','Planetary placements/aspects/dignities and exact degree geometry not independently calculated from ephemerides.'),
 ('PDF434','Moon separating from Jupiter implies alleged already accomplished gains; not a prospective forecast.'),
 ('PDF434','The original expects victory with diminution; do not score as prediction of complete and decisive rout.'),
 ('PDF434','Expected capture of ammunition not independent evidence, only the same-author narrated letter afterwards.'),
 ('PDF434','Prediction of favorable news within 11–12 hours lacks exact independent letter arrival clock time.'),
 ('PDF434','Source gives 11-degree Moon/Venus interval and local fight-distance argument, not an independently calibrated timing equation.'),
 ('PDF434','Author reports a Friday letter about events Thursday; original independent letter or named witnesses unavailable.'),
 ('PDF434','Reported 120 commanders, 560 soldiers and much ammunition are not independently audited counts.'),
 ('PDF434','The same source claims enemy defeat and retreat; external military sources would require a separate historical-source corroboration lane.'),
 ('PDF434','Saturn under beams/fall/peregrine and dexter seventh-cusp square are author-specific conditions, not validated predictions.'),
 ('PDF435','Chapter LXVI Reading siege starts at top of next original page; its separate figure must be excluded.'),
 ('PDF433-435','No complete independent diplomatic transcription, blind case freezing, controlled decoys or verified predictive superiority.'),
 ('PDF433-435','Study documentation must not become practical combat advice or judgement about current people.')
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B03k','status':'RETAIN_ALL_ORIGINAL_LIMITATIONS',
 'issues':[{'id':f'B03k-U{i:02}','source':p,'issue':t} for i,(p,t) in enumerate(issues,1)]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03k','status':'ORIGINAL_HISTORICAL_SOURCE_PROVISIONAL',
 'original_source_annotations':len(ROWS),
 'source_visual_passages':len(SPANS),'prior_accepted_lilly':3630,
 'new_accepted_historical_records':0,
 'author_reported_favorable_battle_letter_cases':1,
 'independent_favorable_outcomes_authenticated':0,
 'independently_time_verified_11_to_12_hour_news_predictions':0,
 'source_reports_possible_incomplete_victory':True,
 'new_empirically_validated_astrology_predictions':0,
 'new_runtime_rules':0})
print(json.dumps({'batch':'B03k','provisional_rows':len(ROWS),
 'source_spans':len(SPANS),'original_pdf_body_pages':[433,434],
 'uncertainty_count':len(issues),'new_accepted':0}))
