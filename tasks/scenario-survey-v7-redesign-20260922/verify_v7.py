import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BANK=HERE/'interviewer-bank-v7.json'
REQ=ROOT/'tasks/scenario-graph-convergence-20260919/source/source-requirements-v2.json'
PROTOCOL=HERE/'INTERVIEW-PROTOCOL-v6.md'

bank=json.loads(BANK.read_text())
req=json.loads(REQ.read_text())
protocol=PROTOCOL.read_text()
questions=bank['questions']
ids=[q['id'] for q in questions]
idset=set(ids)
errors=[]
checks=[]

def check(name, cond, detail=''):
    checks.append((name,bool(cond),detail))
    if not cond: errors.append(name + (': '+detail if detail else ''))

check('version', bank['version']=='scenario-bank-v7.0-20260922', bank['version'])
check('node_count', bank['node_count']==len(questions), f"{bank['node_count']} vs {len(questions)}")
check('unique_ids', len(ids)==len(idset))
check('retired_C0', 'C0' not in idset)
check('routing_guards', set(bank.get('routing_guards',{}))=={'premise_sufficiency','construct_discrimination','redundancy','missing_piece','context_dependence','admission_stop'})
check('planner_output_final_admission', all(x in bank.get('planner_output_rule','').lower() for x in ['proposal-only','exact user-facing wording','context binding','premise sufficiency','construct discrimination','nonredundancy','construct alignment','single-response-task','expected-information-gain','weak preference','leave the facet unresolved']), bank.get('planner_output_rule',''))

family_members=[i for members in bank['families'].values() for i in members]
check('family_members_exist', all(i in idset for i in family_members))
check('family_one_to_one', len(family_members)==len(set(family_members))==len(questions))

for q in questions:
    check(f"context_sources:{q['id']}", all(i in idset for i in q.get('context_sources',[])), str(q.get('context_sources',[])))
    check(f"single_task_punctuation:{q['id']}", q.get('question','').count('?')<=1, q.get('question',''))
    check(f"protocol_ref:{q['id']}", 'INTERVIEW-PROTOCOL.md' not in q.get('admission',''), q.get('admission',''))

facet_ids={f for d in req.get('domains',[]) for f in d.get('facets',[])}
for q in questions:
    for target in q.get('planning_targets',[]):
        check(f"target:{q['id']}:{target}", target in facet_ids)

allowed_empty={'A0','E0','WHY'}
check('empty_target_allowlist', {q['id'] for q in questions if not q.get('planning_targets')}==allowed_empty, str({q['id'] for q in questions if not q.get('planning_targets')}))

texts='\n'.join(q['question'] for q in questions)
for bad in ['progress is poor','two unusually intense days','workload stays too heavy','practical benefits of what you do stay the same','guide works adequately for your task','A new tool has useful features','What would make that practice worth doing for you?']:
    check('retired_phrase:'+bad, bad not in texts)

by={q['id']:q for q in questions}
expect={
'G23':['friends or acquaintances','particular job'],
'M11':['paying for all the ingredients feels like too much','What would you say next?'],
'WORKING-METHOD':['six awkward steps'],
'D0':['one short phrase','ten-second phrase','no test or deadline'],
'M05':['route you know well','normally never uses'],
'M06':['what would you need to already know about a route','turn away from its usual path would carry any meaning'],
'M09':['simple, familiar, works offline','shared reminders','more complex'],
'R07':['same mentally demanding computer work','ten hours each day instead of six','before a longer rest'],
'R08':['four weeks','eight and a half hours a day','six days a week','one full day with no work obligations'],
'R10':['internal disagreements','attempts to sort out the disagreements'],
'STATUS':['genuinely admire','rewarding to you in itself'],
'ROMANCE-FADE':['Apart from losing the things you already said help closeness']
}
for i,needles in expect.items():
    for n in needles:
        check(f"repair_text:{i}:{n}", n in by[i]['question'], by[i]['question'])

check('M06_guard', all(x in by['M06']['admission'] for x in ['familiarity boundary','Do not introduce a second cue','map','directions','hazard']), by['M06']['admission'])
check('M06_direct_familiarity_boundary', all(x in by['M06']['question'] for x in ['what would you need to already know about a route','before a turn away from its usual path would carry any meaning']), by['M06']['question'])
check('M06_no_unexplained_expectation', 'did not expect' not in by['M06']['question'].lower() and 'surpris' not in by['M06']['question'].lower(), by['M06']['question'])
check('M06_no_replacement_cue', all(x in by['M06']['interpretation_limit'] for x in ['familiarity threshold','Do not infer danger','actual unfamiliar-route behavior','knowledge of the route']), by['M06']['interpretation_limit'])

check('F0_matched_audiences', all(x in by['F0']['question'] for x in ['friends you have known for years','friends you have known for only a few weeks','differently']), by['F0']['question'])
check('M11_concrete_objection', 'paying for all the ingredients feels like too much' in by['M11']['question'] and 'fair split' not in by['M11']['question'], by['M11']['question'])
check('G15_fixed_modality', 'six hours of mentally demanding computer work' in by['G15']['question'], by['G15']['question'])
check('R07_same_modality', 'Keep that same mentally demanding computer work' in by['R07']['question'] and 'ten hours each day instead of six' in by['R07']['question'], by['R07']['question'])
check('R08_same_modality', 'Keep that same mentally demanding computer work' in by['R08']['question'] and 'four weeks' in by['R08']['question'], by['R08']['question'])
check('G17_matched_consequence', '7:00 instead of 7:30' in by['G17']['question'] and 'dessert is chocolate' in by['G17']['question'] and 'differently' in by['G17']['question'], by['G17']['question'])
check('M07_ease_learning_contrast', 'came fairly easily' in by['M07']['question'] and 'learn or practise' in by['M07']['question'], by['M07']['question'])
check('G25_reason_supplied', 'they forgot and did not message beforehand' in by['G25']['question'], by['G25']['question'])

check('M03_bounded_feasible_task', all(x in by['M03']['question'] for x in ['thirty minutes','an hour','normally rested','nothing else urgent']), by['M03']['question'])
check('M04_energy_only_variant', 'same thirty-minute meal preparation' in by['M04']['question'] and 'unusually tired' in by['M04']['question'], by['M04']['question'])
check('G20_normalized_amount', 'one month of your ordinary living costs' in by['G20']['question'], by['G20']['question'])

check('M04_no_stipulated_intention', 'still intend to finish' not in by['M04']['question'].lower() and 'what, if anything, would that tiredness change about your intention' in by['M04']['question'].lower(), by['M04']['question'])
check('R08_explicit_recovery', all(x in by['R08']['question'] for x in ['eight and a half hours a day','one full day with no work obligations','no additional vacation or recovery period']), by['R08']['question'])
check('OWNERSHIP_concrete_access_equivalent', all(x in by['OWNERSHIP']['question'] for x in ['laptop owned by someone you trust','reliably available','files stay private','costs you nothing']), by['OWNERSHIP']['question'])
check('exploratory_separate_block', all('separately labeled exploratory block' in q['admission'] for q in bank.get('exploratory_questions',[])))

check('PHYSICAL_partial_scope', by['PHYSICAL-CLOSENESS'].get('target_scope')=={'D12.sensuality':'physical_affection_only'}, str(by['PHYSICAL-CLOSENESS'].get('target_scope')))
check('PREFER_split_routes', 'PREFER-INFLUENCE' not in by and by['PREFER-PERSUADE']['planning_targets']==['D05.preferred_use'] and by['PREFER-EXCHANGE']['planning_targets']==['X08.preferred_use'])
check('PREFER_split_contexts', by['PREFER-PERSUADE']['context_sources']==['F0','G05'] and by['PREFER-EXCHANGE']['context_sources']==['M11'])

check('explicit_context_requirements', all(by[i].get('context_requirement') for i in ['CARE-RESPONSIBILITY','CARE-LIMIT','ROMANCE-FADE']))

check('VERIFY_guard', 'group/source' in by['VERIFY']['admission'] and 'would not decide themselves' in by['VERIFY']['admission'])
check('ROMANCE_guard', 'ordinary inverse' in by['ROMANCE-FADE']['admission'])

explore=bank.get('exploratory_questions',[])
check('exploratory_count', len(explore)==1)
if explore:
    ex=explore[0]
    check('exploratory_unmapped', ex.get('mapping_status')=='unmapped_neutral_candidate')
    check('exploratory_no_credit', ex.get('automatic_evidence_credit') is False)

for phrase in ['ask only the missing piece','Final rendered-question admission','proposal, not admission','do not show the proposed question','Joining can depend on many unspecified factors','expected information gain','weak preference','premise sufficiency','Inverse wording is not independent corroboration','Stop when no remaining route is both admissible','A brief, fleeting, or inconsistent reaction is still an eligible antecedent','Do not credit a rationale, value, comparison, or leverage point merely because the stimulus supplied it','Do not stipulate the very intention, preference, trust, value, or other respondent state that a route is meant to measure','For a matched variant, hold every material non-target determinant constant','must itself elicit a comparison across at least two matched contexts','For promise/follow-through scenes, specify a bounded feasible remaining task','For resource-purpose scenes, normalize the amount','For multi-day or multi-week workload routes, state what happens on nonwork days','record the antecedent-to-target mapping explicitly','mark that partial scope in route metadata','Exploratory questions stay outside canonical routing and evidence credit','When a matched or transfer probe removes the information source that made an earlier cue meaningful']:
    check('protocol:'+phrase, phrase.lower() in protocol.lower())

ev=json.loads((HERE/'EVIDENCE-GUIDE-v7.json').read_text())
ev_facets={x['facet_id'] for x in ev}
check('evidence_73_facets', len(ev)==73, str(len(ev)))
check('evidence_matches_requirements', ev_facets==facet_ids)
for x in ev:
    check(f"evidence_routes:{x['facet_id']}", bool(x.get('question_routes')) and all(r in idset for r in x.get('question_routes',[])), str(x.get('question_routes')))
check('no_evidence_route_to_retired_C0', all('C0' not in x.get('question_routes',[]) for x in ev))
x04=[x for x in ev if x['facet_id']=='X04.context_and_limits'][0]
check('X04_boundary_interpretation', 'self-described familiarity boundary' in x04['narrow_supported_reading'], x04['narrow_supported_reading'])
check('X04_clean_boundary_guide', 'route-pattern deviation carries meaning' in x04['narrow_supported_reading'], x04['narrow_supported_reading'])
check('X04_no_unearned_transfer', all(x in x04['unsupported_extension'].lower() for x in ['danger','actual unfamiliar-route behavior','maps','directions','geography']), x04['unsupported_extension'])

x03=[x for x in ev if x['facet_id']=='X03.follow_through'][0]
check('X03_bounded_followthrough_guide', 'bounded, feasible promise' in x03['narrow_supported_reading'], x03['narrow_supported_reading'])
d19=[x for x in ev if x['facet_id']=='D19.resources_purpose'][0]
check('D19_normalized_amount_guide', 'one month of ordinary living costs' in d19['narrow_supported_reading'], d19['narrow_supported_reading'])

x03e=[x for x in ev if x['facet_id']=='X03.will_vs_available_energy'][0]
check('X03_answer_originated_intention', 'answer-originated' not in x03e['narrow_supported_reading'] or 'Reports whether lower available energy changes the respondent' in x03e['narrow_supported_reading'], x03e['narrow_supported_reading'])
d14p=[x for x in ev if x['facet_id']=='D14.prolonged_overload'][0]
check('D14_explicit_weekly_day_off', 'explicit weekly full day off' in d14p['narrow_supported_reading'], d14p['narrow_supported_reading'])
x04c=[x for x in ev if x['facet_id']=='X04.cue_form'][0]
check('X04_presented_deviation_semantics', 'presented familiarity-dependent route deviation' in x04c['narrow_supported_reading'], x04c['narrow_supported_reading'])

d12=[x for x in ev if x['facet_id']=='D12.sensuality'][0]
check('D12_partial_affection_guide', 'partial coverage limited to physical-affection' in d12['narrow_supported_reading'], d12['narrow_supported_reading'])
d05p=[x for x in ev if x['facet_id']=='D05.preferred_use'][0]
x08p=[x for x in ev if x['facet_id']=='X08.preferred_use'][0]
check('PREFER_context_scoped_guides', d05p['question_routes']==['PREFER-PERSUADE'] and x08p['question_routes']==['PREFER-EXCHANGE'] and 'F0/G05' in d05p['narrow_supported_reading'] and 'M11' in x08p['narrow_supported_reading'])


print(json.dumps({'ok':not errors,'errors':errors,'checks':len(checks),'passed':sum(1 for _,ok,_ in checks if ok)},indent=2))
if errors:
    raise SystemExit(1)
