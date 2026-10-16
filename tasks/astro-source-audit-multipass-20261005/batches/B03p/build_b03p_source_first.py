#!/usr/bin/env python3
"""Original Lilly 1647 Chapter LXX spouse worked-case historical documentary audit."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def add(pages,label,*clauses):
 sid=f'LXX-S{len(SPANS)+1:03}';ids=[]
 for role,anchor,meaning,limits in clauses:
  id=f'LXX-C{len(ROWS)+1:03}';ids.append(id)
  ROWS.append({'local_id':id,'batch':'B03p','role':role,
   'chapter':'LXX' if role!='next_heading' else 'LXXI_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'original_printed_pages':[p-34 for p in pages],
   'original_short_anchor_not_full_diplomatic':anchor,
   'historical_author_claim_paraphrase':meaning,
   'source_scope_and_limitations':limits,'global_record_number':None,
   'historical_documentary_admitted':False,
   'independently_authenticated_clinical_case':False,
   'empirical_predictive_accuracy_validated':False,'runtime_rule_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
   'source_passage_label':label,'mapped_local_ids':ids})
add([449],'Separate worked Chapter LXX heading and chart',
 ('heading','Chap LXX Whether Man or Wife die first','The numbered question compares death order of spouses.','Separate from Chapter LXIX; an individual case is narrated.'),
 ('figure','original square twelve-house horoscope','A separate square chart is printed with original planetary figures.','No reconstructed modern ephemeris or independently archived chart.'),
 ('figure_time','6 Feb 1644 9:10 P.M.','The figure gives 6 February 1644 at 9:10 PM.','Original historical time/calendar context not independently reconciled.'),
 ('reported_question','whether himself or wife should die first','An unnamed person asked which of two spouses would die first.','Source report only; querent identity and later medical chronology not independently confirmed.'))
add([449],'Seventh-wife house and Saturn position',
 ('figure_assignment','seventh signifies Wife','The seventh is chosen for wife in the spouse comparison.','The lord of her own derived eighth differs from the querent eighth.'),
 ('figure_condition','Saturn in Aries in fall afflicts seventh','Saturn positioned in Aries and its fall is treated as afflicting the wifes seventh.','Source glyph and planetary strength not independently calculated.'))
add([449],'Mars, Mercury and Moon adverse derived houses',
 ('figure_assignment','Mars Lord seventh, cadent Gemini ninth','Mars as seventh ruler is described in Gemini and the ninth house.','The original page describes another condition involving Mars.'),
 ('figure_assignment','Mercury Lord sixth from seventh retrograde in fall','Mercury is given as ruler of derived sixth and is said to be retrograde and in fall.','Keep derived house and two distinct debilities; no external check.'),
 ('figure_condition','Moon in Scorpio eighth from seventh','The Moon is described in Scorpio as occupying wifes derived eighth.','House derivation is from seventh; not charts radical eighth.'),
 ('historical_inference','conditions moved me inquire wife sick consumption','Lilly states these conditions led him to ask whether the wife already suffered serious consumption.','The womans illness was an unblinded clinical clue prior to final forecast.'),
 ('reported_confirmation','also infirmed in secretis','The querent reportedly confirmed serious illness and another private infirmity.','Unverifiable and retrospective testimony; this prior illness materially affects forecast.'))
add([449,450],'Historical sickness assertions crossing original page seam',
 ('figure_condition','all Significators relation unto her unfortunate','The author asserts that planets referring to the woman lack essential dignity.','General assessment lacks frozen dignity table and case source.'),
 ('historical_inference','already ill','He infers illness existed before the forecast.','Retrospective information is not an independent prospective prediction.'))
add([450],'Original age and missing natal information',
 ('reported_information','exact Nativitie could not obtain','Lilly acknowledges the exact natal chart was unavailable.','Limits natal validation.'),
 ('reported_information','now in 42 year of age','The woman was reportedly in her forty-second year.','No independent birth record.'),
 ('historical_generalization','Climactericall year usually dangerous','He invokes the period belief that age 42 is high risk.','Not supported as a special epidemiologic interval.'),
 ('context','untoward Disease near that time','Existing serious illness was recognized as an additional concern.','Major non-chart prognostic information.'))
add([450],'Appearance assertions and claimed confirmation',
 ('historical_description','Corporature small or incurvating','The woman is described as small or bent.','No objective measurement.'),
 ('historical_description','visage long and leane, complexion dark pale','Lilly offers facial features and complexion.','Subjective historical description.'),
 ('historical_description','conditions waspish or froward','Temperament is attributed to the woman.','No independent psychological evidence.'),
 ('source_internal_report','which was confessed and afterwards found','Lilly claims his descriptions were confirmed.','Same-author report, no blinded witness.'))
add([450],'Chronic and recurring ailments',
 ('figure_condition','Saturn sheweth long lingering Diseases','Saturn is associated with prolonged illness.','Historical claim, not medicine.'),
 ('figure_condition','Mercury sixth Lord Retrograde','Retrograde Mercury as sixth lord is noted.','Distinct signification and motion.'),
 ('source_internal_forecast','relaps one Disease into another','A future illness recurrence is forecast.','Illness was reportedly known already.'))
add([450],'Attributed responsibility in source',
 ('historical_allegation','own obstinateness','The author assigns some responsibility to the womans behavior.','Unverified personal judgment.'),
 ('historical_allegation','errour of the Physician','He also attributes adverse treatment to physician error.','Unverified clinical assertion.'))
add([450],'Historical planetary role assignments',
 ('figure_assignment','Lord her ascendant Lord eighth','The author combines first and eighth rulership for the spouse.','Symbolic not physiological.'),
 ('figure_assignment','Physician signified Venus','Venus is assigned to the attending physician.','Not evidence of the quality of care.'),
 ('figure_condition','Venus square Saturn','A Venus-Saturn square is invoked as explanation.','No chart geometry verification.'))
add([450],'Spouse comparison and husbands relative condition',
 ('source_internal_forecast','I concluded woman would dye first','Lilly says his judgment favored wife preceding husband.','Retrospective author narrative.'),
 ('figure_condition','Significator of Man no manner affliction','The husbands planetary significator is called unafflicted.','Astrological source claims alone.'),
 ('figure_condition','Venus in her Hayme free from misfortune','Venus is described as strong and protective for the husband.','Do not infer actual future longevity.'),
 ('historical_inference','Man free from all Infirmities','The author alleges husband was healthy.','No independent person medical records.'))
add([450],'Astrological timing hypothesis for autumn',
 ('figure_condition','Saturn and Mars ill aspect','The author selects an approaching unfavorable aspect.','Planets associated with womans condition, not clinical cause.'),
 ('figure_condition','latter end of September Mars opposition Saturn','The claimed angular opposition is assigned to late September.','No independent ephemeris parity.'),
 ('figure_condition','Mars near place Moon at Question 2 Scorpio','The aspect is connected to the lunar position in the question figure.','Rough degree and sign are source-authored.'),
 ('figure_condition','Saturn in 2 Taurus; Moon then 20 Gemini','More source placements are provided for the forecast.','These planetary labels require independent numerical checking.'))
add([450],'Forecast time window and alternative outcomes',
 ('source_internal_forecast','late September or beginning October','The author proposes a seasonal timing window.','Not a unique exact October 8 forecast.'),
 ('source_internal_forecast','probable she die or be in great danger','Lilly gives either demise or grave danger in the same interval.','Disjunctive death-OR-danger outcome considerably broadens apparent accuracy.'))
add([450],'Author-reported outcome and follow-up chart',
 ('source_internal_reported_outcome','in truth she dyed eighth October','The author reports death on October 8.','No independent dated record, contemporaneous forecast freeze, or named person.'),
 ('figure_condition','that day Mars and Mercury in conjunction 8 Scorpio','Lilly cites a conjunction of Mars and Mercury at eight degrees Scorpio as retrospective correspondence.','Not independently verified; chosen after outcome was known.'),
 ('figure_condition','one lord ascendant, other lord sixth','He assigns the two planets to the womans life and sixth-house health.','Derived-house roles kept distinct.'),
 ('figure_condition','same degree Moon in Question; Moon 12 Libra','The author claims the angle echoed the original lunar place, with Moon then near twelve Libra.','Post-event explanation and original glyphs not independently tested.'),
 ('figure_condition','opposite degree her ascendant in Question','He interprets a lunar opposition relative to the original wife ascendant.','A retrospective chart feature, not a prior narrow forecast.'))
add([451],'Next chapter LXXI separately dated source marker',
 ('next_heading','CHAP LXXI woman asks after husband at sea','The next chapter asks about the status and return of an absent husband.','Navigation only; different person and square chart dated April 1645.'))
assert len({r['local_id'] for r in ROWS})==len(ROWS)
assert [r['local_id'] for r in ROWS]==[f'LXX-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[449] and SPANS[-1]['original_pdf_pages']==[451]
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
assert all(r['chapter']=='LXX' for r in ROWS[:-1])
assert ROWS[-1]['chapter']=='LXXI_NAVIGATION_ONLY'
def dump(n,obj):(B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
im=[]
for n in [449,450,451]:
 f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
 im.append({'pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
    'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03p','status':'ORIGINAL_SOURCE_FIRST_PROVISIONAL',
 'original_full_pdf_sha256':SHA,'source_units':len(ROWS),'rows':ROWS,
 'independent_case_validation':False})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03p','source_spans':SPANS,
 'span_count':len(SPANS),'mapped_source_units':len(ROWS),
 'original_body_pdf_pages':[449,450],'next_heading_pdf':451,
 'second_blind_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03p',
 'ordered_local_ids':[r['local_id'] for r in ROWS],
 'cross_page_local_ids':[r['local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_heading_only':ROWS[-1]['local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03p',
 'original_full_pdf_sha256':SHA,'source_body_pdf_pages':[449,450],
 'next_heading_pdf':451,'original_images':im,'prior_accepted_lilly':4007,
 'printed_chart_date':'6 February 1644','printed_chart_time':'9:10 PM',
 'independent_case_outcome_authenticated':False})
limits=[
 'The woman and questioner are unnamed; no independent original source case files or hospital records.',
 'The chart date/time 6 February 1644 at 9:10 PM is printed in the original figure; no independent horary parity.',
 'The source says exact nativity could not be obtained; natal risk comparisons cannot be reconstructed.',
 'The woman was reportedly already very sick before the final seasonal forecast, causing severe information leakage.',
 'Consumption and other clinical conditions are from source narrative, not independently assessed diagnoses.',
 'Original 42nd-year climacteric risk is not a validated biological hazard.',
 'Astrological physical description and character judgments are subject to narrative selection and no blind assessment.',
 'The source blames the patient and physician for care and illness; neither is an independently verified fact.',
 'Seventh versus sixth-from-seventh versus eighth-from-seventh must remain distinct house assignments.',
 'A husbands supposedly unaffected Venus does not independently establish health or subsequent survival.',
 'Forecast specifies an interval late September OR beginning October; it does not explicitly name October 8 in advance.',
 'Forecast outcome is death OR great danger, a flexible disjunctive alternative and no blind binary lock.',
 'The phrase following about 1644 is in author narrative; the outcome is self-reported with no external death certificate.',
 'The October 8 conjunction/house correspondences are given after the reported outcome, not a separate frozen future prediction.',
 'Source planetary dates and exact conjunction degrees not independently verified by ephemeris parity.',
 'No prospective timestamped record of the prediction is supplied other than Lilly published 1647 narrative.',
 'The dated case does not independently establish individual predictive accuracy, causal mechanism, or medical validity.',
 'The following LXXI is a distinct absent-sailor case; its chart and outcome cannot be included in LXX.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03p','status':'RETAIN_OPEN',
 'issues':[{'id':f'B03p-U{i:02}','issue':v} for i,v in enumerate(limits,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03p','status':'PROVISIONAL_DOCUMENTARY_ONLY',
 'source_annotations':len(ROWS),'source_spans':len(SPANS),
 'prior_accepted_lilly':4007,'new_accepted_records':0,
 'author_narrated_spouse_date_outcome_cases':1,
 'independently_authenticated_spouse_outcomes':0,
 'clinically_verified_predicted_cases':0,
 'empirically_validated_predictive_cases':0,'runtime_promotions':0,
 'forecast_time_window':'late September or beginning October',
 'forecast_outcome':'death OR great danger',
 'source_reported_event_date':'8 October; 1644 inferred only from narrative, not separate certificate'})
print(json.dumps({'batch':'B03p','rows':len(ROWS),'spans':len(SPANS),
 'limits':len(limits),'body_pages':[449,450],'independent_results':0}))
