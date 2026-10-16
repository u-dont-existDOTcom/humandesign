#!/usr/bin/env python3
"""Lilly original 1647 Book II LXXVIII: source-first, retrospective dream example."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[]; SPANS=[]
def add(pages,label,*claims):
    sid=f'LXXVIII-S{len(SPANS)+1:03}';ids=[]
    for role,anchor,meaning,limit in claims:
        local=f'LXXVIII-C{len(ROWS)+1:03}';ids.append(local)
        ROWS.append({'source_local_id':local,'batch':'B03x','role':role,
          'chapter':'LXXVIII' if role!='next_navigation' else 'LXXIX_NAVIGATION_ONLY',
          'original_pdf_pages':list(pages),'printed_pages':[p-34 for p in pages],
          'short_original_anchor_not_diplomatic':anchor,
          'historical_author_paraphrase':meaning,
          'original_source_qualifications':limit,
          'global_record_number':None,'historical_documentary_accepted':False,
          'independently_authenticated_dream_case':False,
          'empirically_validated_prediction':False,'runtime_model_promoted':False})
    SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
      'passage_label':label,'mapped_local_ids':ids})

add([470],'Separate dream-case heading, dated square horoscope',
 ('heading','Chap. LXXVIII. Terrible Dreames.','A separate worked horary reading considers terrible dreams.','New case starts at PDF470/printed436.'),
 ('chart_timestamp','26 Ianu. 1648. 9:27 AM','The printed square horoscope is dated 26 January 1648, 9:27 AM.','Calendar convention and consistency with the 1647 title date unresolved; no independent recasting.'),
 ('source_context','occasion of his Dreames','Lilly describes the man as disturbed by dreams; he does not reproduce a verbatim dream report.','Unidentified historical querent; no independently authenticated firsthand log.'))

add([470],'Ninth rulers and earlier-author dream-vanity reading',
 ('condition','Lords of the ninth','Lilly names Jupiter and Saturn as lords of the ninth for this chart.','Original source claim, without independently verified house-lord reconstruction.'),
 ('condition','accidentally posited twelfth','He places both rulers accidentally in the twelfth house.','Position is source asserted, not calculated anew.'),
 ('condition','square aspect cusp ninth','He describes a square to the cusp of the ninth.','Aspect depends on chart position/house method not independently calibrated.'),
 ('authorial_attribution','best Authors vanity Dreame','Lilly says earlier authorities interpret that configuration as an inconsequential dream arising from disturbed imagination and worldly worries.','Attribution to authorities is not independent case verification.'))

add([470],'Angular Mars and private-estate anxiety interpretation',
 ('condition','Mars only Planet in an Angle','Mars is the only angular planet according to the printed judgment.','Astrological statement from source; no ephemeris parity.'),
 ('method','Mars best expresse the cause','Lilly switches to Mars to explain the dream cause and its favorable or unfavorable consequences.','This is a second interpretive path after the ninth-house ruler reading.'),
 ('condition','Mars Lord of ascendant','Mars is treated as ruler of the ascendant.','Source-derived role, not a modern chart recalculation.'),
 ('condition','disposer of Part of Fortune','Mars is described as disposer of the Part of Fortune.','Separate relation from angularity.'),
 ('condition','Mars in conjunction Fortune','The author invokes Mars conjoined with the Part of Fortune.','Printed conjunction sign; no independent chart validation.'),
 ('historical_inference','Estate and Fortune intrusted out','He offers anxiety about money entrusted out and thought lost as one possible cause of the dreams.','Lilly says the explanation might be construed two ways, not a unique precommitted diagnosis.'),
 ('historical_inference','Fancy disturbed rest by night','He conjectures that preoccupation disturbed his normal nighttime rest.','No independently assessed sleep outcome.'))

add([470],'Office and social-standing alternative explanation',
 ('condition','Saturn Lord of tenth','Lilly makes Saturn ruler of the tenth, associated with office and command.','Historical house assignment only.'),
 ('condition','did afflict Jupiter or impede','He says Saturn afflicted Jupiter, lord of the ninth, or at least impeded Jupiter.','Preserve source uncertainty between affliction and impediment.'),
 ('historical_inference','lost benefit some good Place','Lilly told the man he suspected a lost benefit or good Commonwealth position.','Author-reported retrospective interpretation, not independently authenticated dismissal.'),
 ('historical_inference','solicitous former credit','He conjectures the man feared losing his former public credit or status.','Alternative explanation, distinct from entrusted money.'))

add([471],'Mars/Jupiter aspect, two distinct forecasts, retrospective success assertion',
 ('condition','Jupiter Mars sextile symbol','Lilly gives a favorable star/sextile aspect between Jupiter and Mars.','The star-like sextile glyph is not a generic planetary association.'),
 ('source_internal_forecast','no matter of perill to his person','He judged that the dreams signaled no peril to his person.','Separate bodily-safety forecast; no externally verified follow-up.'),
 ('source_internal_forecast','onely some dammage in Estate','He instead forecast some damage to his estate.','Different financial endpoint from personal injury.'),
 ('authorial_outcome_claim','this really proved true','Lilly asserts that the forecast proved true.','Uncorroborated authorial success report; cannot be scored as independent validation.'))

add([471],'Following separate ecclesiastical office case navigation',
 ('next_navigation','Chap. LXXIX Parsonage','The next chapter asks whether another querent will obtain a desired parsonage.','Starts below the divider on the same original PDF471; separate case.'),
 ('next_navigation','6 August 1644 8:24 PM','The next chapter has its own circular figure dated 6 August 1644, 8:24 PM.','This is not the dream horoscope.'))

assert len(ROWS)==24 and len(SPANS)==6
assert [r['source_local_id'] for r in ROWS]==[f'LXXVIII-C{i:03}' for i in range(1,25)]
assert all(r['chapter']=='LXXVIII' for r in ROWS[:-2])
assert all(r['chapter']=='LXXIX_NAVIGATION_ONLY' for r in ROWS[-2:])
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
pdfhash='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
images=[]
for n in (470,471):
    f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
    images.append({'original_pdf_page':n,'printed_page':n-34,
      'path':f.relative_to(B).as_posix(),'bytes':len(raw),
      'sha256':hashlib.sha256(raw).hexdigest()})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03x','status':'PROVISIONAL_NOT_CANONICAL',
  'source_units':24,'original_full_pdf_sha256':pdfhash,'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03x','span_count':6,
  'source_spans':SPANS,'mapped_source_units':24,'original_body_pdf_pages':[470,471],
  'next_heading_pdf':471,'no_independent_diplomatic_second_transcription':True})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03x','original_full_pdf_sha256':pdfhash,
  'original_images':images,'original_body_pdf_pages':[470,471],
  'previous_accepted_lilly':4484,'first_record':4485,'next_numbered_chapter':'LXXIX',
  'following_heading_pdf':471,'chapter_end':'PDF471 above LXXIX divider',
  'author_claims_success':True,'independent_predicted_outcomes':0})
issues=[
 'Printed dream figure says 26 January 1648 despite the 1647 first-edition title date; chronology/calendar must not be silently repaired.',
 'Original horoscope and house rulerships not independently recast or checked against historical calendar conventions.',
 'No first-person verbatim dream report or independently authenticated case identity.',
 'Jupiter/Saturn ninth rulers and twelfth-house placements are source statements rather than independently verified computations.',
 'The earlier-author ninth/twelfth-house dream vanity explanation is distinct from the later angular Mars interpretation.',
 'Mars angularity, ascendant rulership, Fortune disposition and conjunction are separate premises; original printed figure not independently calculated.',
 'Lilly gives two alternative causes, lost entrusted fortune and loss of office/credit; do not collapse into a unique hit.',
 'Sleep disturbance, thoughts and psychological states are inferred by author, not measured clinically.',
 'The printed Saturn-Jupiter adverse relation carries an authorial hedge "or did impede him at least".',
 'Lilly separately denies bodily injury while predicting estate damage; these endpoints must be scored separately if ever tested.',
 'The favorable Jupiter/Mars aspect is an internal source condition, not prospective prediction evidence.',
 'Author states "this really proved true" but gives no external dated outcome record or independent control.',
 'Another ecclesiastical/parsonage case begins later on PDF471, with its own 1644 figure; it must not be merged with LXXVIII.',
 'No blind preregistration, untouched participant, unexposed outcome or out-of-sample evidence; no runtime promotion.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03x','issues':[{'id':f'B03x-U{i:02}','issue':s} for i,s in enumerate(issues,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03x','source_annotations':24,'source_spans':6,
  'retained_source_issues':len(issues),'prior_lilly':4484,'new_accepted':0,
  'author_asserted_retrospective_confirmation':1,'independently_authenticated_case_outcomes':0,
  'independently_validated_predictions':0,'runtime_promotions':0})
print(json.dumps({'batch':'B03x','source_annotations':24,'spans':6,
  'issues':len(issues),'pages':[470,471],'next':'LXXIX PDF471'}))
