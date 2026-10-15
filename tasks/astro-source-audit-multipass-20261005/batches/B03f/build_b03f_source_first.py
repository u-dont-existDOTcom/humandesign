#!/usr/bin/env python3
"""Original 1647 Lilly Chapter LX: two-page marriage figure and narrative.
Editorial source annotations, NOT independent validation of astrology.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def span(pages,label,*items):
 sid=f'LX-S{len(SPANS)+1:03}'
 ids=[]
 for role,anchor,meaning,caveat in items:
  rid=f'LX-C{len(ROWS)+1:03}';ids.append(rid)
  ROWS.append({
   'source_local_id':rid,'batch':'B03f','book':'II',
   'chapter':'LX' if role!='next_chapter_boundary' else 'LXI_NAVIGATION_ONLY',
   'role':role,'original_pdf_pages':list(pages),
   'printed_pages':[x-34 for x in pages],
   'source_short_anchor_not_diplomatic':anchor,
   'historical_author_report_paraphrase':meaning,
   'conditions_source_limits_or_chronology':caveat,
   'global_record_number':None,'original_scan_is_authority':True,
   'is_independently_blinded_case':False,'complete_diplomatic_second_transcription':False,
   'historical_documentation_admitted':False,
   'real_outcome_independently_authenticated':False,
   'empirical_astrology_prediction_validated':False,
   'runtime_model_promoted':False
  })
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
  'printed_pages':[x-34 for x in pages],
  'source_label_not_verbatim_transcription':label,
  'mapped_source_local_ids':ids})
span([423],"physical Chapter LX heading and distinct case",
 ('heading','CHAP. LX. If she should marry the man desired?',
  'Chapter LX asks whether the querent would marry a desired man; this is a distinct worked horary from Chapter LIX.',
  'Opening on original PDF423, printed389; the immediately preceding LIX chart has a different printed date.'))
span([423],"original square horoscope figure, source date and figure placement",
 ('figure','original square horary figure under Chap. LX',
  'Lilly prints a complete square twelve-house astrology diagram with signs, planet glyphs, and numerical angular annotations.',
  'Preserve original 1647 image as diagram authority, not a reconstructed computerized horoscope.'),
 ('figure_timestamp','11 June. 1646. 10:38 A.M.',
  'The centre of the separate Chapter LX figure gives 11 June 1646 and 10:38 AM.',
  'Historical manuscript/printed civil date; neither timezone, birthplace nor Gregorian conversion is supplied here.'),
 ('figure_reading','Moon separated square of Jupiter and applying trine to Mercury',
  'The diagram centre includes astrological shorthand matching the judgment paragraph about the Moon separating from Jupiter and applying to Mercury.',
  'Astrological symbol reading is tied to the visible chart and later original prose, not a fresh ephemeris calculation.'))
span([423],"The Judgment heading and authorial account convention",
 ('subheading','The Judgment.',
  'The author supplies the interpretation of the diagram and descriptions of both parties.',
  'Source-internal worked case, not a preregistered independent human dataset.'))
span([423],"querent and quesited appearance descriptions",
 ('historical_description','querent was of tall stature, ruddy complexioned',
  'The author describes the questioner as tall, ruddy, sober, discreet and well spoken.',
  'No independent biographical identity or measurement is supplied.'),
 ('historical_description','quesited was very tall, slender, leane ... black haire',
  'The desired partner is described as very tall, slender, lean, long-faced and black-haired.',
  'No independently authenticated external person record.'))
span([423],"Jupiter Venus terms and seventh-cusp rationale",
 ('figure_interpretation','his talnesse I attribute to Jupiter',
  'Lilly attributes the man’s tallness to Jupiter as his significator.',
  'Source explanation, not a general empirically calibrated stature predictor.'),
 ('figure_condition','Jupiter ... being in the Termes of Venus',
  'He adds Jupiter being in the terms of Venus to explain the description.',
  'The printed terms designation is author-reported; do not silently substitute a chosen dignity table.'),
 ('figure_condition','cusp of the seventh being also in his Termes',
  'He also invokes the seventh-house cusp being in the relevant terms.',
  'Pronoun referent in the historical expression is not separately chart-verified.'))
span([423],"general source-native influence of planetary terms",
 ('historical_rule','significator in the Termes of any Planet',
  'The author generalizes that a significator in a planet’s terms can modify the person’s description or constitution.',
  'This is the author’s original historical rule, not an independent personal-trait validation.'),
 ('historical_rule_qualifier','small or great tincture from that Planet',
  'The size of the claimed change is said to vary with that planet’s dignity.',
  'The text does not supply a numeric score or measured effect size.'))
span([423],"hair-color explanation and ambiguous pronoun",
 ('figure_interpretation','sadnesse of his haire ... Jupiter his aspect to Saturn',
  'Dark hair is conjecturally attributed to Jupiter’s aspect with Saturn.',
  'Lilly says "I conceive"; this is speculative even in the original authorial account.'),
 ('figure_condition','Moon her square unto him, being her selfe subterranean',
  'He adds a lunar square and the Moon being below the horizon to the same description.',
  'The "him" antecedent could refer to Saturn/Jupiter; preserve source wording rather than assert an exact receiving planet.'))
span([423,424],"querent Mercury retrograde and under Sun beams, page seam",
 ('figure_assignment','Mercury is here Significatrix of the querent',
  'Mercury is the woman’s significator in this worked figure.',
  'The Chapter LX assigning rule cannot be copied from Chapter LIX without recalculation.'),
 ('figure_condition','Retrograde, under the Sun-beames',
  'The woman’s Mercury is described as retrograde and under the Sun’s beams.',
  'Exact sentence crosses original PDF423→424 after the word Sun; no modern orb supplied.'),
 ('historical_mental_state','in some distresse and feare ... would not have her',
  'Lilly interprets those conditions as the woman’s worry that the man would not accept her.',
  'This is an author-reported feeling, not an independently documented psychological assessment.'))
span([424],"quesited Jupiter exaltation, Venus and alternative attachment",
 ('figure_condition','Jupiter was in his Exaltation',
  'He identifies Jupiter as exalted in the case.',
  'This is one stated condition in the narrated interpretation.'),
 ('figure_condition','neer the sextile of Venus',
  'A near sextile to Venus is also part of the man’s delineation.',
  'Nearness and exact geometry are author reported, not recalculated against independent ephemerides.'),
 ('historical_inference','man stood upon high termes ... tampering with another',
  'Lilly takes those conditions to suggest the man was demanding and involved with another.',
  'Untested historical psychological and relationship inference about a third party.'))
span([424],"semi-sextile of parties and interpretation of potential affection",
 ('figure_condition','both Significators in a Semisextile ... good houses',
  'He describes the two primary significators as in a semisextile and placed in good houses.',
  'A semisextile is source-specific; do not silently replace with sextile.'),
 ('historical_inference','some sparks of love betwixt them',
  'From the semisextile and house placements he infers some mutual affection.',
  'Source internal interpretation, not independently measured feelings.'))
span([424],"Moon separation and moving light to the ascendant lord",
 ('figure_condition','Moon separating from a square of Jupiter',
  'The Moon is described as separating from a square with Jupiter.',
  'Distinguish past/separating aspect from future applying aspect.'),
 ('figure_condition','carrying his light by a trine aspect to Mercury',
  'He invokes transfer of light from Jupiter through the Moon via a trine to Mercury.',
  'Aspect direction and source-native terminology preserved.'),
 ('figure_assignment','Mercury the Lord of the ascendant',
  'Mercury is explicitly identified as ruler of the ascendant in this case.',
  'Do not switch significators or reconstruct another marriage chart.'),
 ('figure_condition','he in an angle, receiving willingly, by his Retrograde motion',
  'He describes angular, receptive and retrograde characteristics of Mercury in receiving the Moon’s carried light.',
  'Source wording is gendered planetically ("he"); do not read as the man’s consent or a generic reception algorithm.'))
span([424],"reported prediction and outcome: mediation",
 ('source_internal_forecast','I was confident the Match would suddenly be brought to passe',
  'The author reports being confident the marriage would happen soon after considering the lunar transfer.',
  'Retrospectively narrated confidence; no frozen prospective dated prediction supplied.'),
 ('source_internal_forecast','by such a one as Moon was, or represented by her',
  'A Moon-associated person is predicted or described as facilitating the marriage.',
  'No named independent mediator or time window; personification is source-dependent.'),
 ('source_internal_reported_outcome','who did much interpose ... at last ... produced the Marriage',
  'The author reports an intervening person eventually helped bring about the marriage after some difficulty.',
  'An outcome asserted within the same historical author account, not independently authenticated; mediation can affect outcome.'),
 ('source_internal_reported_outcome','to the content of both parties',
  'He says the marriage satisfied both parties.',
  'Later relationship stability and objective outcome details are not documented in these two pages.'))
span([424],"next numbered chapter physical boundary",
 ('next_chapter_boundary','CHAP. LXI. A Fugitive Servant, which way gone, when returne?',
  'Chapter LXI begins below the divider; its unrelated fugitive-servant diagram is excluded from LX.',
  'Navigation-only marker; zero Chapter LXI body rows in this batch.'))
assert len(set(x['source_local_id'] for x in ROWS))==len(ROWS)
assert [x['source_local_id'] for x in ROWS]==[f'LX-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[423] and SPANS[-1]['original_pdf_pages']==[424]
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
def dump(name,obj):
 (B/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
imgs=[]
for page in [423,424]:
 f=B/'evidence'/f'pdf_1647-{page}.jpg';b=f.read_bytes()
 imgs.append({'pdf_page':page,'printed_page':page-34,'path':f.relative_to(B).as_posix(),
 'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
 'source':'original Wellcome b30338724 1647 image'})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03f','status':'SOURCE_FIRST_UNACCEPTED',
 'source_original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_units':len(ROWS),'original_case_independently_authenticated':False,'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03f','status':'MANUALLY_MAPPED_VISUAL_SOURCE_PROVISIONAL',
 'source_spans':SPANS,'span_count':len(SPANS),'mapped_source_units':len(ROWS),
 'source_window':'PDF423 full Chapter LX diagram and judgment to PDF424 above LXI divider',
 'independent_diplomatic_second_transcription_claimed':False,
 'empirically_validated_predictions':0})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03f','status':'PROVISIONAL',
 'ordered_local_ids':[x['source_local_id'] for x in ROWS],
 'cross_page_ids':[x['source_local_id'] for x in ROWS if len(x['original_pdf_pages'])>1],
 'next_boundary_id':ROWS[-1]['source_local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B03f','status':'PROVISIONAL',
 'source_full_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_body_pdf_pages':[423,424],
 'source_printed_pages':[389,390],
 'opening':'Chapter LX heading and chart at PDF423 top',
 'closing':'End of marriage judgment at PDF424 above Chapter LXI divider',
 'original_images':imgs,
 'prior_accepted_lilly':3418,
 'new_empirically_verified_predictions':0,
 'case_independently_authenticated':False,'frozen_prospective_prediction':False,
 'independent_complete_diplomatic_second_reader':False})
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B03f','status':'RETAIN_UNRESOLVED',
 'issues':[
 {'id':'B03f-U01','source':'PDF423','issue':'LIX and LX present different cases/dates (16 vs 11 June 1646). Do not pool their charts.'},
 {'id':'B03f-U02','source':'PDF423 diagram','issue':'The 11 June 1646, 10:38 AM inscription has no independently authenticated location or timezone and the civil-calendar conversion is unspecified.'},
 {'id':'B03f-U03','source':'PDF423 diagram','issue':'Original house cusps and planetary glyphs need independent astronomical and symbolic parity; no modern chart generation or correction.'},
 {'id':'B03f-U04','source':'PDF423','issue':'The terms of Venus and house-cusp pronoun have context-dependent 17th-century astrological grammar.'},
 {'id':'B03f-U05','source':'PDF423','issue':'Dark hair is a conjectural author explanation; Moon square "unto him" has uncertain exact antecedent.'},
 {'id':'B03f-U06','source':'PDF423-424','issue':'Mercury under Sun-beams sentence crosses physical pages. No modern combustion orb introduced.'},
 {'id':'B03f-U07','source':'PDF424','issue':'The claim of the man communicating with another is unverified person-level allegation.'},
 {'id':'B03f-U08','source':'PDF424','issue':'Semisextile must not silently be substituted with sextile or merged with Jupiter–Venus sextile.'},
 {'id':'B03f-U09','source':'PDF424','issue':'Moon separates from Jupiter square and applies to Mercury trine; direction must survive conversion.'},
 {'id':'B03f-U10','source':'PDF424','issue':'Mercury reception by retrograde motion not reduced to numeric runtime weight or current generic doctrine.'},
 {'id':'B03f-U11','source':'PDF424','issue':'Marriage success and mediator are solely author reported; no independent outcome record, prospective freeze or comparison decoys.'},
 {'id':'B03f-U12','source':'PDF424','issue':'No actual date of marriage, validated onset window, external identity, or long-term partnership follow-up.'},
 {'id':'B03f-U13','source':'PDF424','issue':'LXI begins below the divider with a different figure; exclude LXI body from this packet.'}
 ]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03f','scope':'1647_LILLY_HISTORICAL_WORKED_CASE_ONLY',
 'source_units_provisional':len(ROWS),'image_reverse_passages':len(SPANS),
 'canonical_lilly_before':3418,'globally_accepted_new_units':0,
 'original_case_independently_verified':False,
 'new_empirically_validated_astrology_predictions':0,
 'new_blinded_decoy_comparisons':0,
 'runtime_astrology_rules_promoted':0,
 'source_internal_reported_positive_outcome_count':1})
print(json.dumps({'batch':'B03f','source_rows':len(ROWS),'source_spans':len(SPANS),
 'images':len(imgs),'canonical_count_increment':0}))
