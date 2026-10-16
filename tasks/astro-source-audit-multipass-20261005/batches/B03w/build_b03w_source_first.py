#!/usr/bin/env python3
"""Lilly first edition 1647 Book II Chapter LXXVII dreams, historical source only."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def add(pages,label,*claims):
 sid=f'LXXVII-S{len(SPANS)+1:03}';ids=[]
 for role,anchor,meaning,limit in claims:
  local=f'LXXVII-C{len(ROWS)+1:03}';ids.append(local)
  ROWS.append({'source_local_id':local,'batch':'B03w','role':role,
   'chapter':'LXXVII' if role!='next_navigation' else 'LXXVIII_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'printed_pages':[n-34 for n in pages],
   'short_original_anchor_not_diplomatic':anchor,
   'historical_author_paraphrase':meaning,
   'original_source_qualifications':limit,
   'global_record_number':None,'historical_documentary_accepted':False,
   'independently_authenticated_dream_case':False,
   'empirically_validated_prediction':False,'runtime_model_promoted':False})
 SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
  'passage_label':label,'mapped_local_ids':ids})
add([468],'Original dream heading and earlier authority',
 ('heading','CHAP LXXVII Of Dreams','The chapter asks whether dreams signify anything.','Begins below LXXVI divider on PDF468.'),
 ('authorial_attribution','Bonatus farre exceeds Haly','Lilly judges Bonatus better than Haly for this specific dream question.','Lilly adds Bonatus is less judicious in many other questions; no empirical proof.'),
 ('question','effect of his Dreame','The original asks about consequences of a reported dream.','No single validated dream case is given in this chapter.'))
add([468],'Ninth-house general rule and planets there',
 ('figure_assignment','behold ninth house','The ninth house is assigned to dream interpretation.','Source-native astrology rather than cognitive science.'),
 ('condition','seven planets therein','The planet in ninth is used to explain dream content.','Different planets carry distinct source associations.'),
 ('condition','Saturn ninth','Saturn in ninth is connected to frightening and disturbing dreams.','Original has particular fear language, not a verified psychological diagnosis.'),
 ('historical_inference','inordinate matter not natural','The author conjectures an unnatural worry as dream source.','Subjective account without independent measurement.'),
 ('condition','South Node ninth','A lunar node in ninth is associated with more intense feared aggression.','Explicit comparison with Saturn branch.'),
 ('historical_inference','persecuted and difficulty escaping','The source imagines a dreamer feeling threatened by others.','No real threat is established.'))
add([468,469],'Capricorn/Aquarius and relationship-house interpretation',
 ('condition','Capricorn Aquarius rise','Certain Saturn-ruled signs at the ascendant imply fear originating within the dreamer.','Interpretation requires particular signs rising.'),
 ('historical_inference','feare proceeds from himselfe','Lilly interprets the worry as personal.','Not a clinical determination.'),
 ('condition','on cusp second','A similar sign on the second-house cusp is linked to monetary affairs.','Source sentence crosses PDF468–469.'),
 ('historical_inference','money or personal Estate occasioned dream','The dream is tied to finances in that derived location.','No verified financial event.'),
 ('condition','on cusp third','Same signs on third cusp are linked to kin or neighbors.','Different from second-house cause.'),
 ('historical_inference','kinred brethren neighbours reports','The author offers family/neighbors or rumors as reasons.','Several possible explanations, not one unique target.'))
add([469],'Fallback house search if ninth empty',
 ('condition','no Planet ninth then tenth','If ninth is empty Lilly next inspects tenth for meaning.','A prioritized fallback, not concurrent use of every house.'),
 ('condition','no tenth then ascendant','Without a tenth planet he moves to the ascendant.','Ordered exclusion required.'),
 ('condition','no ascendant then seventh','Seventh becomes the next fallback.','The chapter explicitly orders consideration.'),
 ('condition','then fourth third','Fourth and third are later fallbacks.','Do not reverse order.'),
 ('condition','then second fifth sixth eighth eleventh twelfth','Remaining houses are consulted in the order printed.','Source lists six more houses.'),
 ('historical_inference','no Planet everywhere dream vanity','If none of the searched houses gives testimony, dream is judged without effect.','A sweeping period assertion, not a valid neuroscientific criterion.'))
add([469],'Harm from lord ninth to first-house body',
 ('method','true way judging Dream influence','The author claims a method to decide if a dream has influence.','Unsupported source assertion, not proven validity.'),
 ('condition','ninth Lord or occupant square opposition Lord first','An adverse aspect to the first lord is the key condition.','Requires particular ninth connection, not any harsh aspect.'),
 ('source_internal_forecast','querent receive prejudice bodily','The author predicts injury or affliction to the person.','Not actionable for health, no external case.'),
 ('historical_inference','crosses to his person','Lilly also invokes troubles or bodily crosses as alternatives.','Different harm magnitudes and outcomes.'))
add([469],'Financial branch and extending the house method',
 ('condition','ninth Lord afflicts second Lord','An adverse ninth-to-second-lord aspect is an alternate source condition.','Separate from first/body.'),
 ('source_internal_forecast','prejudice in point of Estate','The source predicts property or money trouble.','No financial transaction evidence.'),
 ('method','so in all other houses','He generalizes the house-ruler approach to other life domains.','Very broad retrospective interpretive flexibility.'),
 ('source_scope','consideratis considerandis','He explicitly warns that relevant circumstances must be considered.','Does not supply a frozen method or objective weights.'))
add([469],'Benefic ninth/ascendant protection and unfavorable counterparts',
 ('condition','good Planet ninth','Benefic occupancy of ninth is treated as dream non-harm.','Not every ninth planet; benefic identity matters.'),
 ('source_internal_forecast','no ill from Dreame','Lilly proposes absence of adverse consequences.','Cannot establish actual safety.'),
 ('condition','good Planet ascendant','Benefic in first is an alternative protective sign.','Distinct house from ninth.'),
 ('condition','first Lord trine Sun Jupiter Venus','A favorable aspect between first lord and benefic planets is included.','Specified aspect and beneficiary, not all contacts.'),
 ('source_internal_forecast','same favourable result','He expects no harm under the positive conditions.','No independent observation.'),
 ('condition','Infortunes contrary','Malefic involvement reverses favorable reading.','The text leaves detailed polarity to the reader.'),
 ('authorial_limit','vaine to be more large','The author ends saying further discussion is unnecessary.','Not an empirical outcome; section ends above next heading.'))
add([470],'Next separate worked dream case boundary',
 ('next_navigation','CHAP LXXVIII Terrible Dreams','The next chapter begins a dated worked example about distressing dreams.','Navigation only; its case is separate from general source rules.'),
 ('next_navigation','26 January 1648 9:27 AM','The original next square figure is dated January 26, 1648 at 9:27 AM.','Not an LXXVII figure or prospective case.'))
assert [r['source_local_id'] for r in ROWS]==[f'LXXVII-C{i:03}' for i in range(1,len(ROWS)+1)]
assert all(r['chapter']=='LXXVII' for r in ROWS[:-2])
assert all(r['chapter']=='LXXVIII_NAVIGATION_ONLY' for r in ROWS[-2:])
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for n in (468,469,470):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
 images.append({'original_pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
  'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03w','status':'ORIGINAL_SOURCE_FIRST_PROVISIONAL',
 'original_full_pdf_sha256':SHA,'source_units':len(ROWS),'rows':ROWS,
 'independent_case_outcomes_authenticated':False})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03w',
 'source_spans':SPANS,'span_count':len(SPANS),'mapped_source_units':len(ROWS),
 'original_body_pdf_pages':[468,469],'next_heading_pdf':470,
 'blind_diplomatic_second_reader':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03w',
 'ordered_ids':[r['source_local_id'] for r in ROWS],
 'cross_page_ids':[r['source_local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'next_heading_navigation_only':[r['source_local_id'] for r in ROWS[-2:]]})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03w',
 'original_full_pdf_sha256':SHA,'original_images':images,
 'original_body_pdf_pages':[468,469],'following_heading_pdf':470,
 'previous_accepted_lilly':4446,'next_numbered_chapter':'LXXVIII',
 'original_begin':'Original PDF468/printed434 below LXXVI divider',
 'original_end':'Original PDF469/printed435 before distinct LXXVIII',
 'independent_dream_prediction_outcomes':0})
issues=[
 'Original LXXVII begins below PDF468 LXXVI divider; first-edition source is not a clinical dream study.',
 'The Bonatus versus Haly authority preference is not independent evidence of accurate forecasts.',
 'Source ninth-house planets are proposed as dream indicators without measured outcomes.',
 'Saturn and South Node imagined dream terrors are source symbols, not observed actual threats.',
 'Signs Capricorn/Aquarius and house cusps require original derivation; no full ephemeris parity.',
 'Original PDF468 to PDF469 seam separates source claim; body spans both pages.',
 'Fears caused by self, money or neighbors are distinct claims and all unverified.',
 'An empty ninth-house fallback to tenth, ascendant, seventh, fourth and others is an ordered heuristic, not unconditional simultaneous scoring.',
 'If all indicators absent the author calls the dream vain; absence of future event is not empirically verified.',
 'Ninth to first-lord harsh aspect is a bodily harm allegation without clinical evidence.',
 'Ninth to second-lord harsh aspect claims financial harm, a different target.',
 'The generalized judge other houses proviso gives very flexible retrospective interpretation.',
 'Benefic in ninth, first or trine first lord is supposed protective; negative malefic testimony changes polarity.',
 'The next LXXVIII contains a separate dated dream case on original PDF470 and is excluded from LXXVII body.',
 'No independently authenticated real dream, prospective chart freeze, complete blind second transcription, or prediction validation.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03w','status':'ORIGINAL_DREAM_SOURCE_LIMITS_OPEN',
 'issues':[{'id':f'B03w-U{i:02}','issue':x} for i,x in enumerate(issues,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03w','status':'SOURCE_FIRST_PROVISIONAL_NOT_CANONICAL',
 'source_annotations':len(ROWS),'original_source_spans':len(SPANS),
 'retained_source_uncertainties':len(issues),
 'previous_accepted_lilly':4446,'new_accepted_source_records':0,
 'independently_authenticated_dream_events':0,
 'independently_validated_predictive_outcomes':0,
 'runtime_promotions':0})
print(json.dumps({'batch':'B03w','annotations':len(ROWS),
 'spans':len(SPANS),'issues':len(issues),'body_pdf_pages':[468,469],
 'next_chapter':'LXXVIII','next_pdf_page':470,'new_accepted':0}))
