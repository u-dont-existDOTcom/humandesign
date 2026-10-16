#!/usr/bin/env python3
"""Original 1647 William Lilly Chapter LXXIII promised-portion worked source, no empirical proof."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def add(pages,label,*claims):
 sid=f'LXXIII-S{len(SPANS)+1:03}';refs=[]
 for role,anchor,paraphrase,limit in claims:
  lid=f'LXXIII-C{len(ROWS)+1:03}';refs.append(lid)
  ROWS.append({'source_local_id':lid,'batch':'B03s','role':role,
    'chapter':'LXXIII' if role not in ('next_heading','next_section_preface') else 'LXXIV_NAVIGATION_ONLY',
    'original_pdf_pages':list(pages),'printed_pages':[p-34 for p in pages],
    'short_anchor_not_diplomatic_quote':anchor,
    'historical_author_paraphrase':paraphrase,
    'original_scope_uncertainty':limit,
    'global_record_number':None,'historical_documentary_admitted':False,
    'independent_payment_outcome_verified':False,
    'empirically_validated_prediction':False,'runtime_rule_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
   'passage_label':label,'mapped_source_local_ids':refs})
add([455],'Separate numbered LXXIII and dated horoscope',
 ('heading','CHAP LXXIII If have the Portion promised','A new numbered chapter asks whether a promised marriage portion will be paid.','Distinct from earlier LXVIII general wealth/dowry rules.'),
 ('figure','original square horoscope dated 13 July 1634','Lilly prints a square horary and its original house/planet glyphs.','Source chart is not equivalent to a reconstructive modern horoscope.'),
 ('figure_time','6:15 P.M.','The figure center prints 6:15 PM.','Location and historic time standard not independently documented.'),
 ('question','if have Portion promised','The specific question concerns fulfillment of an existing financial promise.','Amount, deadline and transaction counterparties unspecified.'))
add([455],'Querent Saturn, retrogradation and despair',
 ('figure_assignment','Saturn significator querent','Saturn stands for the person asking the question.','Do not confuse Saturn with the wife second-house lord below.'),
 ('figure_condition','Retrograde and in twelfth house','Saturn is placed retrograde in twelfth.','Period source conditions, not independently calculated.'),
 ('reported_context','as if querent had been in some despaire','Lilly infers the questioner felt discouraged about fulfillment.','Presented without blind independent questionnaire or pre-event notes.'),
 ('source_internal_confirmation','and so he confessed','The querent allegedly confirmed worry about the promise.','Source-internal testimony; the presenting question already reveals concern.'))
add([455],'Woman Jupiter/Moon character and strength',
 ('figure_assignment','Woman signified Jupiter and Moon','Jupiter and Moon are assigned to the spouse.','Two significators with distinct source properties.'),
 ('figure_condition','Jupiter in his Exaltation','Jupiter is described as exalted.','Source dignity not independently recomputed.'),
 ('figure_condition','Moon in Leo a fixed signe','Moon occupies Leo, a fixed sign.','Sign modality is another source condition.'),
 ('historical_characterization','well conceited of herself','Lilly infers self-confidence.','Unverified subjective personality assertion.'),
 ('historical_characterization','confident yet virtuous and modest','The author adds virtue and modesty with confidence.','Subjective characterization, not a blind target.'))
add([455],'Moon near Sun and body characteristic',
 ('figure_condition','Moon near Sun','Lilly uses lunar proximity to Sun in describing the woman.','Original positioning does not independently validate physical traits.'),
 ('historical_characterization','scar near right eye','A scar near the woman right eye is predicted or narrated.','No external photograph or confirmation document.'),
 ('authorial_explanation','Moon signifies in Women right Eye','The text supplies a source-native body-sign correspondence.','Historical occult association, not biological evidence.'))
add([455],'Eighth house for woman derived second and wealth',
 ('figure_assignment','Venus in eighth house womans second','An eighth-house planet is said to occupy the spouse derived second, signifying property.','Distinguish radical eighth from derived second, and planet occupation from ruler.'),
 ('figure_assignment','Sun Lord thereof in own house','Sun is assigned ruler of the eighth/derived second, in its own sign.','Source-native house and essential dignity testimony.'),
 ('figure_condition','eighth house planet Venus','Benefic Venus in the eighth is treated as favorable.','Do not treat a single benefic as absolute evidence of payment.'))
add([455],'Moon separating Sun and transferring to Saturn',
 ('figure_condition','Moon separated sextile Sun','The Moon is said to separate from a sextile to Sun.','Past separation versus future applying must be retained.'),
 ('figure_condition','Moon transferred Sun virtue unto Saturn','The source describes transfer of virtue or light to Saturn.','Historical transfer rule involves an ordered previous and subsequent aspect.'),
 ('figure_assignment','Saturn Lord ascendant','Saturn is tied to the querent role again.','Distinguish querent body role and money role.'),
 ('figure_assignment','Saturn Disposer of Part of Fortune','Saturn is also described as dispositor of Part of Fortune.','This strengthens claim under the original doctrine only.'),
 ('figure_assignment','Saturn Lord querents second','Saturn is additionally assigned to the questioner second house.','Querent own property source role separate from spouse eighth.'))
add([455],'Assurance of actual promised portion',
 ('source_internal_forecast','no cause to fear not-payment','Lilly says the querent should not fear nonpayment.','A statement about event, not just emotional reassurance.'),
 ('source_internal_forecast','really be performed','The promised portion is predicted to be fulfilled.','No amount, date, or partial-payment threshold provided.'),
 ('source_internal_forecast','whatsoever was or had been promised','The positive forecast covers the amount promised.','Original breadth means specific sum cannot be tested from this page.'))
add([455,456],'Cross-page end of promise and additional character reading',
 ('source_seam','promised; and further comfort','The word promised finishes across printed pages 421–422.','Both original PDF455 and 456 are required for documentary coverage.'),
 ('historical_characterization','chast virtuous woman but somewhat proud','The author also characterizes the wife as virtuous but proud.','A subjective ancillary claim, not a payment outcome.'))
add([456],'Retrospective confirmation attributed to the same querent',
 ('authorial_reported_confirmation','all this proved true','Lilly reports his judgments were confirmed.','The phrase may refer to payment and character collectively, without itemized verification.'),
 ('authorial_reported_confirmation','from the querents own Mouth','The stated source for the confirmation is the questioner himself.','Not independent receipts, bank, estate or legal documentation.'),
 ('evidence_limit','no separate payment receipt','The printed case provides no contemporaneous payment instrument or exact paid date.','No independent empirical outcome counted.'))
add([456],'Next ninth-house introduction and LXXIV',
 ('next_section_preface','The ninth House Long Journies Religion Pilgrimage Dreames','An ornamental divider introduces ninth-house questions.','Section preface begins after LXXIII end; not part of dowry case.'),
 ('next_heading','CHAP LXXIV Of good or ill concerning this House','A distinct numbered general ninth-house section begins.','Next chapter navigation only; voyages and religion are outside LXXIII.'))
assert [r['source_local_id'] for r in ROWS]==[f'LXXIII-C{i:03}' for i in range(1,len(ROWS)+1)]
assert all(r['chapter']=='LXXIII' for r in ROWS[:-2])
assert all(r['chapter']=='LXXIV_NAVIGATION_ONLY' for r in ROWS[-2:])
def dump(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
images=[]
for n in (455,456):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
 images.append({'pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
   'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03s','status':'PROVISIONAL_SOURCE_FIRST',
 'original_full_pdf_sha256':SHA,'source_units':len(ROWS),'rows':ROWS,
 'independent_case_outcome_verified':False})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03s',
 'source_spans':SPANS,'span_count':len(SPANS),'source_units':len(ROWS),
 'original_body_pages':[455,456],'next_navigation_pdf':456,
 'independent_blind_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03s',
 'ordered_ids':[r['source_local_id'] for r in ROWS],
 'cross_page_ids':[r['source_local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_navigation_only':[r['source_local_id'] for r in ROWS[-2:]]})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03s','original_full_pdf_sha256':SHA,
 'source_body_pdf_pages':[455,456],'next_section_pdf':456,
 'original_images':images,'previous_accepted_lilly':4136,
 'source_chart_date':'13 July 1634','source_chart_time':'6:15 PM',
 'independently_confirmed_payment_receipts':0})
limits=[
 'Original chart in 1634 and book published in 1647, after the queried event.',
 'No independently identified participants or payment records.',
 'The question itself provides a clue to anxiety about payment.',
 'Querent Saturn retrograde twelfth does not by itself establish nonpayment.',
 'Two different woman significators and dignity signs must stay distinct.',
 'Scar and personality descriptions lack independent witness confirmation.',
 'Moon right-eye correspondence is period symbolic anatomy, not physiology.',
 'Wife derived second and querent second are different house roles.',
 'Favorable eighth lord and occupiers are conditional, not a receipt.',
 'Moon separating Sun sextile and transferring to Saturn is an ordered source rule.',
 'Saturn holds separate ascendant, second-house and Fortune-dispositor roles.',
 'The promised amount, fulfillment date and definition of full payment not specified.',
 'The statement all proved true from questioner mouth is not itemized.',
 'Source-internal self-report cannot authenticate actual dowry transfer.',
 'The original narrative sentence crosses PDF455-456.',
 'Following ninth-house preface and Chapter LXXIV belong to the next section.',
 'No independent chart calculation, blinded test or duplicate diplomatic reading.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03s','status':'ORIGINAL_SOURCE_LIMITS_OPEN',
 'issues':[{'id':f'B03s-U{i:02}','issue':x} for i,x in enumerate(limits,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03s','status':'HISTORICAL_SOURCE_FIRST_NOT_ADMITTED',
 'source_annotations':len(ROWS),'source_visual_passages':len(SPANS),
 'prior_accepted_lilly':4136,'globally_admitted_new_units':0,
 'author_reported_general_success_claims':1,
 'separately_verified_paid_portion_cases':0,
 'empirically_validated_astrological_predictions':0,
 'runtime_promotions':0})
print(json.dumps({'batch':'B03s','rows':len(ROWS),'passages':len(SPANS),
 'source_issues':len(limits),'original_pages':[455,456],'new_global_records':0}))
