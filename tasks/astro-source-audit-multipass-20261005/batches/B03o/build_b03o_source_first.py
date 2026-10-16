#!/usr/bin/env python3
"""Original 1647 Lilly LXIX historical fear/danger source, not predictive validation."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
R=[];S=[]
def add(pages,label,*claims):
 sid=f'LXIX-S{len(S)+1:03}';ids=[]
 for role,anchor,meaning,limit in claims:
  lid=f'LXIX-C{len(R)+1:03}';ids.append(lid)
  R.append({'local_id':lid,'role':role,'chapter':'LXIX' if role!='next_heading' else 'LXX_NAVIGATION_ONLY',
   'original_pdf_pages':list(pages),'printed_pages':[p-34 for p in pages],
   'source_short_anchor_not_diplomatic':anchor,'historical_author_paraphrase':meaning,
   'source_conditions_and_limits':limit,'global_record_number':None,
   'historical_documentary_admitted':False,'independent_danger_outcome_verified':False,
   'empirically_validated_prediction':False,'runtime_model_promoted':False})
 S.append({'span_id':sid,'original_pdf_pages':list(pages),'source_passage_label':label,
  'mapped_local_ids':ids})
add([448],'Heading and scope of question',
 ('heading','Chap LXIX. If one be afraid of a thing','A numbered chapter examines a question about fear.','Historical theory only, no dated worked case.'),
 ('question','whether shall be in danger of the same or not','The question distinguishes feeling afraid from whether actual danger will occur.','No external evidence or fear questionnaire.'))
add([448],'Ascendant, lord and Moon adverse',
 ('assignment','behold ascendant and his Lord and Moon','Lilly uses the rising sign, ruler and Moon.','Distinct astrological significators.'),
 ('condition','Moon unfortunate or Lord ascendant unfortunate','Lilly describes afflicted Moon OR afflicted ascendant ruler as adverse.','Alternative conditions must not be treated as conjunctive.'))
add([448],'Falling from angle and twelfth qualification',
 ('condition','Lord ascendant unfortunate and falling from an angle','An afflicted first lord falling from angular house increases adverse judgment.','Both affliction and change of placement matter.'),
 ('condition','especially in twelfth and Moon with him','A twelfth-house lord together with Moon strengthens the adverse argument.','Not an unconditional twelfth-house rule.'),
 ('forecast','same Fear is true and certain cause for it','The author alleges grounds for the fear.','No independently observed real danger.'))
add([448],'Burden, grief, alleged wrongful or actual accusations',
 ('forecast','great labour and grief shall molest him','The feared event may be replaced by great toil or grief.','Objective harm and worry are different endpoints.'),
 ('forecast','charged with matters not appertaining to him','The author includes being wrongly accused or burdened.','An accusation is not proof of guilt.'),
 ('allegation','or of which he is guilty','Another alternative supposes a person guilty.','Historical source cannot diagnose criminality.'))
add([448],'Relief on ascending from twelfth and Fortune contact',
 ('condition','Lord ascendant from twelfth into eleventh or tenth','Transition from twelfth into eleventh/tenth is favorable.','Mere residence in tenth is not identical.'),
 ('condition','or shall be joined to Fortunes','Benefic conjunction is an alternative favorable source condition.','Not necessarily simultaneous with twelfth ascent.'),
 ('forecast','thing feared shall not appertain to him','Fear is judged not to affect the person.','No independently tested non-event.'),
 ('forecast','escape fear; matter shall not do him ill','The author forecasts relief or no harm.','Relief and absence of physical harm must not be conflated.'))
add([448],'One-degree conjunction and favorable qualifiers',
 ('condition','Lord ascendant one degree with Fortunes','A one-degree conjunction with favorable planets is singled out.','Other aspects and house positions further qualify it.'),
 ('condition','Fortunes to which lord applies, or they unto him','The application can be in either direction.','Applying differs from separating.'),
 ('condition','Fortunes in mid heaven','Favorable planets are described at the midheaven.','Retain this positional qualifier.'),
 ('condition','Moon applying to fortunes and angular','Moon application together with angular or elevated placement is cited.','Printed referents partly ambiguous.'),
 ('forecast','easily delivered from fear; no grounds','An unwarranted fear is predicted to dissipate.','No observed case supplied.'))
add([448],'Applying planetary testimony',
 ('condition','signifier applying to Infortunes','The unfavorable applying aspect is presented as adverse.','Applying is distinct from separation.'),
 ('forecast','it is true','The matter is considered genuine by the author.','No real case is supplied.'))
add([448],'Benefic aspect branch',
 ('condition','to a fortune without infortune reception','The benefic condition is distinguished from unfavorable applying aspect.','Unfavorable reception must be absent.'),
 ('forecast','it is false','The source labels the feared matter false.','No independent source outcome.'))
add([448],'Attributed lunar cadent-house interpretation',
 ('attribution','Many have judged','The source attributes a rumor reading to other astrologers.','Not independently tested by Lilly.'),
 ('condition','Moon eighth sixth twelfth applies cadent Planet','Lunar house and applying to a cadent planet jointly matter.','Bare lunar placement is insufficient.'),
 ('forecast','Suspition not true or report will hold long','Rumor could be false or persist.','False event and prolonged report are different outcomes.'),
 ('forecast','smothered and vanish to nothing','The source says the report can eventually dissipate.','No observed rumor provided.'))
add([448],'Moon aspect and disclosure',
 ('condition','Moon trine Sun','The lunar-solar trine is named.','Separate from cadent rumors.'),
 ('forecast','discovers all suddenly','A sudden revelation is proposed.','No independently verified event.'))
add([448],'Documentary scope',('limitation','no worked chart','The original chapter is generic doctrine.','Following case is separate.'))
add([449],'Next chapter boundary',
 ('next_heading','CHAP LXX and separate spouse case','A new numbered chapter starts on the following printed page.','Only navigation retained; no body borrowed.'))
assert [r['local_id'] for r in R]==[f'LXIX-C{i:03}' for i in range(1,len(R)+1)]
assert all(r['chapter']=='LXIX' for r in R[:-1]) and R[-1]['chapter']=='LXX_NAVIGATION_ONLY'
def dump(n,obj):
 (B/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
im=[]
for n in (448,449):
 f=B/'evidence'/f'pdf_1647-{n}.jpg';b=f.read_bytes()
 im.append({'original_pdf_page':n,'printed_page':n-34,'path':f.relative_to(B).as_posix(),
            'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
src='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03o','status':'ORIGINAL_SOURCE_FIRST_PROVISIONAL',
 'source_original_pdf_sha256':src,'source_units':len(R),'rows':R,'independent_case_verified':False})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03o',
 'source_spans':S,'span_count':len(S),'source_units':len(R),'original_body_page':[448],
 'next_navigation_pdf_page':449,'independent_full_diplomatic_transcription':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03o','ordered_ids':[r['local_id'] for r in R],
 'next_heading_only':R[-1]['local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03o','source_original_pdf_sha256':src,
 'source_body_pdf_pages':[448],'next_heading_pdf_page':449,'original_images':im,
 'previous_accepted_lilly':3976,'independent_outcomes_verified':False})
limits=[
 'Only a one-page general rules chapter; no dated question or real outcome.',
 'Rising sign, first lord and Moon are different roles; bad testimony can be disjunctive.',
 'Afflicted first lord and falling from angle are conjunctive in one branch.',
 'Special twelfth-plus-Moon variant cannot be treated as any twelfth-house occupant.',
 'Fear, actual harm, labour, grief, wrongful accusation and guilt are not equivalent endpoints.',
 'Ascent from twelfth to eleventh/tenth and benefic joining are distinct favorable options.',
 'One-degree benefic contact has nested midheaven and Moon-application qualifications.',
 'Applying to infortunes vs fortunes with no infortune reception are distinct polarities.',
 'Other astrologers are cited for false suspicion under Moon cadent aspects; not Lilly worked result.',
 'Long-standing rumor vs ultimate dissolution are distinct outcomes.',
 'Moon trine Sun revelation is unverified and has no timestamp.',
 'No independent case or control group, physiological effect or measured real threat.',
 'The next Chapter LXX has an independent figure and must not be imported into LXIX.',
 'Primary original text not subjected to an independent complete blind diplomatic second transcription.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03o','status':'PROVISIONAL_UNRESOLVED',
 'issues':[{'id':f'B03o-U{i:02}','issue':v} for i,v in enumerate(limits,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03o','status':'PROVISIONAL_HISTORICAL_ONLY',
 'source_first_units':len(R),'source_visual_passages':len(S),'prior_lilly':3976,
 'globally_admitted_new_records':0,'independently_verified_risk_outcomes':0,
 'empirically_validated_predictions':0,'runtime_promotions':0})
print(json.dumps({'batch':'B03o','units':len(R),'spans':len(S),'limits':len(limits),
 'body_original_pdf':448,'new_accepted':0}))

