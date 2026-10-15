#!/usr/bin/env python3
"""Documentary clauses: Lilly 1647 Book II, Chapter LXI (fugitive servant case).
Original scans are authoritative; no independent outcome verification.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[]; SPANS=[]
def add(pages,label,*items):
    sid=f'LXI-S{len(SPANS)+1:03}'
    ids=[]
    for kind,anchor,interpretation,limit in items:
        rid=f'LXI-C{len(ROWS)+1:03}'
        ids.append(rid)
        ROWS.append({
            'source_local_id':rid,'batch':'B03g','book':'II',
            'chapter':'LXI' if kind!='next_chapter_boundary' else 'LXII_NAVIGATION_ONLY',
            'role':kind,'original_pdf_pages':list(pages),
            'printed_pages':[p-34 for p in pages],
            'source_short_anchor_not_diplomatic':anchor,
            'historical_author_report_paraphrase':interpretation,
            'conditions_source_limits_or_chronology':limit,
            'global_record_number':None,'original_scan_is_authority':True,
            'is_independently_blinded_case':False,
            'complete_diplomatic_second_transcription':False,
            'historical_documentation_admitted':False,
            'real_outcome_independently_authenticated':False,
            'empirical_astrology_prediction_validated':False,
            'runtime_model_promoted':False
        })
    SPANS.append({
        'span_id':sid,'original_pdf_pages':list(pages),
        'printed_pages':[p-34 for p in pages],
        'source_label_not_verbatim_transcription':label,
        'mapped_source_local_ids':ids
    })
add([424],"Chapter LXI heading and original square horary figure",
 ('heading','CHAP. LXI. A Fugitive Servant, which way gone, when returne?',
  'Chapter LXI introduces a worked question about a servant who had fled, asking where he went and when he would return.',
  'Chapter begins beneath the LX marriage divider; do not conflate with LX marriage case or LXII missing-dog case.'),
 ('figure','A Servant Fled',
  'The original 1647 image contains a distinct square horoscope headed A Servant Fled with house and planetary symbols.',
  'Original diagram, not an independently calculated ephemeris; no exact date, birthplace or timezone is stated in this figure.'))
add([425],"Judgment opening and querent role",
 ('subheading','Judgment upon the Figure foregoing.',
  'The author explicitly connects the judgment on printed page 391 to the preceding original fugitive-servant figure.',
  'Opening of the worked judgment, not a general independently tested predictive rule.'),
 ('figure_assignment','ascendant and Mercury in Aquarius, together with Mars posited in ascendant',
  'The ascendant, Mercury in Aquarius and Mars placed in the ascendant are used to characterize the servant’s master.',
  'Distinct from Mars serving as fugitive significator in this figure; source applies both roles according to context.'))
add([425],"master's reported body and complexion",
 ('historical_description','Master ... short of stature, corpulent ... ruddy, fresh countenance',
  'The master is characterized as short, heavyset, healthy-complexioned and ruddy-faced.',
  'Reported case description without external identification or anthropometric records.'),
 ('figure_interpretation','fatnesse ... north latitude of Mercury ... about one degree',
  'The author attributes the master’s fatness partly to Mercury having approximately one degree of northern latitude.',
  'Qualitative author explanation, not empirically calibrated physiognomy.'))
add([425],"airy and watery-sign terms/decans and Moon aspect for body",
 ('figure_condition','degrees ascending ... Terms of Mars ... ayery Signe ... Face or Decanate of Sun',
  'He further invokes the rising degree in Mars terms, an airy sign, and the Sun’s face or decan.',
  'Specific original dignity language, no normalized terms table or contemporary sign-trait diagnosis.'),
 ('figure_condition','Sun ... in a watry Signe ... partill trine to Moon',
  'The Sun in a watery sign and an exact trine to the Moon are included among the author’s body-type premises.',
  'The original states both planets are in moist signs; original scan glyphs are controlling.'),
 ('figure_interpretation','argued a flegmatick, full body',
  'The author draws a phlegmatic/full-body conclusion from the listed moist and other chart conditions.',
  'Historical humoral theory, not a validated health or temperament assessment.'))
add([425],"servant's significator and competing traditional assignment",
 ('figure_assignment','Significator of Servant was Mars peculiarly in this Figure',
  'Mars is specifically assigned as significator of the missing servant in this case.',
  'The author explicitly distinguishes chart-specific Mars from his usual Mercury assignment.'),
 ('scope_exception','although many times Mercury shall signifie a fugitive Servant',
  'He notes Mercury often signifies a fugitive servant in other judgments.',
  'Do not override the present case’s expressly selected Mars significator.'))
add([425],"author's reported servant age and appearance",
 ('historical_description','young Fellow of about nineteen',
  'The missing servant is described as a young man approximately 19 years old.',
  'Historical narrative about an unidentified person; not corroborated by surviving records.'),
 ('historical_description','well set ... short, big joynted, broad and full faced, dark browne haire',
  'The author describes a short, strongly jointed, broad-faced young man with dark brown hair.',
  'Author-reported appearance cannot validate astrology traits without independent data.'),
 ('historical_description','his teeth growing ilsavouredly ... Sun-burnt ... skin ... cleer',
  'Additional details concern irregular teeth, sunburnt/dark outward complexion and clear skin elsewhere.',
  'The source differentiates face from body; avoid flattening or treating as pathology.'))
add([425],"Sunday departure and Moon in Gemini then",
 ('reported_event','went away from his Master the Sunday preceding',
  'The servant is reported to have left on the Sunday preceding the consultation.',
  'The printed figure does not provide a question date, so elapsed days to Friday cannot be independently computed.'),
 ('historical_direction_condition','at which time the Moon was in Gemini, a Westerne Signe',
  'The author relates the Moon’s alleged Gemini position at departure to a westerly direction.',
  'Historical chart symbolism; cannot independently validate departure time or sign.'))
add([425],"present Mars and generic Mercury signs/quarters",
 ('figure_condition','now Mars, Significator ... in same Signe',
  'At the consultation Mars is said to occupy Gemini, the same sign as the Moon at the servant’s departure.',
  'Relative dates and referents retained; no exact calculation from missing event times.'),
 ('figure_condition','Mercury ... in Aquarius, a Westerne Signe ... South quarter',
  'Mercury in Aquarius is described as a westerly sign located in the southern quarter of the sky.',
  'The author also discusses Gemini’s southern and Aquarius’s northern quarter associations.'),
 ('scope','Gemini hath ... South ... Aquarius ... North',
  'The author notes different cardinal-quarter associations in addition to sign-based directional meaning.',
  'Do not mechanically substitute one cardinal rule for another.'))
add([425],"west direction judgment and competing significator strength",
 ('source_internal_forecast','Servant went westward at his first departing',
  'Lilly reports having judged that the missing servant initially traveled westward.',
  'This is the author’s self-reported forecast, not an authenticated original dated prediction.'),
 ('source_internal_forecast','at the time of the Question ... West from the querents house',
  'He reports judging the servant was west of the master’s home when asked.',
  'No independent location record at consultation time.'),
 ('figure_condition','Mars was angular ... every way as strong as Moon',
  'Mars is preferred because the author judges him angular and as strong as the Moon.',
  'He says otherwise he would have judged by the Moon; retain this priority condition.'))
add([425],"Mars to Mercury trine and return interval",
 ('figure_condition','Mars Significator ... Mercury Lord of ascendant ... hastening to a trine',
  'Mars and Mercury are described as approaching a trine while leaving angular houses.',
  'Direction and role assignments are central; not a retrospective numerical ephemeris model.'),
 ('source_internal_forecast','within a day or two ... have his Servant againe',
  'The author claims to have forecast the servant returning within one or two days of the consultation.',
  'Exact consultation date unprovided here; cannot compare the interval against the reported Friday return.'))
add([425],"servant estate, Moon second house and recovered goods",
 ('figure_condition','Moon in second, in her owne house ... Servant part of Masters Estate',
  'The author uses a Moon in the second house, its own house, together with estate symbolism.',
  'Do not infer literal ownership of people or convert this into present-day norms.'),
 ('source_internal_forecast','Master should not lose ... recover forthwith his lost Goods',
  'Lilly says he forecast that the master would recover missing goods and avoid a loss.',
  'The later narrative reports return but does not independently confirm specific goods or value.'),
 ('figure_condition','Moon ... perfect trine of Sun in eleventh ... both Moiety ascending',
  'He adduces an exact Moon–Sun trine between the second and eleventh houses, with source-specific moiety wording.',
  'Original diagram and text are the authority; no modern orb or scoring weight inferred.'))
add([425,426],"closest Mars to rising degree and distance, page seam",
 ('figure_condition','neerenesse of Mars to degree ascending',
  'The closing paragraph cites Mars being near the ascendant degree as relevant to distance.',
  'The sentence crosses from bottom of original PDF425 to top of PDF426.'),
 ('source_internal_forecast','not above three or four houses Westward',
  'The author says he expected the servant to be only three or four houses west of the master’s dwelling.',
  'A distinctive concrete distance claim, not obviously the same as the subsequent claim of Kingston upon Thames.'))
add([426],"reported Friday return with qualified Kingston narrative",
 ('source_internal_reported_outcome','Friday following betimes in the morning, he came home',
  'The author states that the servant returned home early on the following Friday.',
  'Source-internal report; no court, servant, household or external dated record corroborates the return.'),
 ('reported_unverified_testimony','said he had been at Kingston upon Thames',
  'The returned servant reportedly said he had stayed at Kingston upon Thames.',
  'This is hearsay narrated by Lilly, not observed location at the consultation.'),
 ('limitation','which if true',
  'The author explicitly qualifies the servant’s statement about Kingston with the words “which if true.”',
  'Preserve uncertainty rather than treat the Kingston account as independently confirmed.'))
add([426],"direction and proximity to river offered after narrative",
 ('retrospective_alignment','full West, or a little to South, and neer a great Water ... Thames',
  'Lilly interprets the claimed Kingston visit as westerly or slightly southerly and near the Thames.',
  'Retrospective geographic alignment; note tension with the earlier three-or-four-houses distance estimate.'),
 ('figure_interpretation','as Moon in Cancer did or might signifie',
  'He offers the Moon in Cancer as a possible signification of the nearby water.',
  'The original uses tentative “did or might”; no independent positional confirmation.'))
add([426],"next chapter heading and diagram boundary",
 ('next_chapter_boundary','CHAP. LXII. A Dogge missing, where?',
  'Chapter LXII on a missing dog begins below the divider, with its own figure; all of its body is excluded.',
  'Navigation-only marker for the next original numbered chapter.'))
assert len({r['source_local_id'] for r in ROWS})==len(ROWS)
assert [r['source_local_id'] for r in ROWS]==[f'LXI-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[424] and SPANS[-1]['original_pdf_pages']==[426]
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
def dump(f,obj):
 (B/f).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for n in (424,425,426):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
 images.append({'pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
  'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'original_1647_scan_authoritative':True})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03g','status':'HISTORICAL_SOURCE_FIRST_PROVISIONAL',
 'source_original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_units':len(ROWS),'source_case_independently_authenticated':False,'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03g','status':'SOURCE_TO_DRAFT_VISUALLY_COLLATED',
 'source_spans':SPANS,'span_count':len(SPANS),'mapped_source_units':len(ROWS),
 'source_window':'PDF424 below LX divider through PDF426 above LXII divider',
 'blind_complete_second_diplomatic_transcription':False,
 'empirical_predictions_validated':0})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03g','status':'PROVISIONAL',
 'ordered_local_ids':[r['source_local_id'] for r in ROWS],
 'cross_page_ids':[r['source_local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_heading_only':ROWS[-1]['source_local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B03g','status':'PROVISIONAL_SOURCE_FIRST',
 'source_full_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_body_pdf_pages':[424,425,426],
 'opening':'PDF424 BELOW Chapter LX divider',
 'closing':'PDF426 ABOVE Chapter LXII divider',
 'next_header':'Chapter LXII A Dogge missing, where?',
 'original_images':images,
 'prior_accepted_lilly':3449,
 'source_outcome_independently_authenticated':False,
 'fully_diplomatic_second_reader_done':False})
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B03g','status':'UNRESOLVED_HISTORICAL_SOURCE_ONLY',
 'issues':[
 {'id':'B03g-U01','source':'PDF424','issue':'Horoscope lacks clearly printed consultation date or geographical location; prohibit retrospective assignment from Sunday/Friday alone.'},
 {'id':'B03g-U02','source':'PDF424','issue':'The servant figure is distinct from prior marriage case and subsequent dog figure.'},
 {'id':'B03g-U03','source':'PDF425','issue':'Case selects Mars to signify servant even while source calls Mercury the common fugitive-servant significator.'},
 {'id':'B03g-U04','source':'PDF425','issue':'Moon in Gemini at Sunday departure vs Moon in Cancer at question/river reading; do not flatten time states.'},
 {'id':'B03g-U05','source':'PDF425','issue':'Mercury in Aquarius is a western sign in a southern heaven quadrant; Gemini/South Aquarius/North nuance retained.'},
 {'id':'B03g-U06','source':'PDF425','issue':'Mars preferred over Moon only when stronger/angular; retain fallback to Moon.'},
 {'id':'B03g-U07','source':'PDF425','issue':'One/two-day return claim cannot be validated against Friday return without exact question calendar date.'},
 {'id':'B03g-U08','source':'PDF425','issue':'Moon second-house connection to masters estate is historical social/ownership wording, not modern moral endorsement.'},
 {'id':'B03g-U09','source':'PDF425','issue':'Lost goods recovery forecast is not separately documented by the reported servant return.'},
 {'id':'B03g-U10','source':'PDF425-426','issue':'Three/four houses west distance forecast does not automatically match stated Kingston-upon-Thames; location may be distant.'},
 {'id':'B03g-U11','source':'PDF426','issue':'Author says servant reportedly named Kingston and explicitly adds “which if true”; keep as conditional hearsay.'},
 {'id':'B03g-U12','source':'PDF426','issue':'Friday return is sole author-reported positive outcome; independent testimony and original question-time proof unavailable.'},
 {'id':'B03g-U13','source':'PDF426','issue':'Water/Thames and Moon in Cancer reading is retrospective and tentative “did or might”.'},
 {'id':'B03g-U14','source':'PDF426','issue':'Chapter LXII starts below divider with a different figure; do not import dog or general later fugitive maxims into Chapter LXI.'},
 {'id':'B03g-U15','source':'PDF424-426','issue':'No complete independent second diplomatic transcription or original horoscope ephemeris parity; glyphs remain source witness.'},
 {'id':'B03g-U16','source':'PDF424-426','issue':'No blind, pre-frozen prediction package, decoy controls, external person IDs or empirically measured accuracy.'}
 ]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03g','scope':'1647_LILLY_WORKED_FUGITIVE_SERVANT_CASE_ONLY',
 'provisional_source_units':len(ROWS),'original_reverse_spans':len(SPANS),
 'prior_lilly_accepted':3449,'globally_accepted_new_source_units':0,
 'source_internal_servant_return_reports':1,
 'independently_verified_return_cases':0,
 'independently_verified_geographic_forecasts':0,
 'empirical_predictions_validated':0,'runtime_rule_promotions':0,
 'source_stated_distance_issue_unresolved':True})
print(json.dumps({'batch':'B03g','original_source_rows':len(ROWS),
 'source_spans':len(SPANS),'original_scan_pages':[424,425,426],
 'new_accepted':0},ensure_ascii=False))
