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
'M11':['can afford the ingredients','fair split'],
'WORKING-METHOD':['six awkward steps'],
'D0':['one short phrase','ten-second phrase','no test or deadline'],
'M05':['route you know well','normally never uses'],
'M06':['do not know well','do not know the normal route'],
'M09':['simple, familiar, works offline','shared reminders','more complex'],
'R07':['ten hours each day','comfortable temperature','sleep and eat normally'],
'R08':['four weeks','ten hours a day','six days a week'],
'R10':['internal disagreements','attempts to sort out the disagreements'],
'STATUS':['genuinely admire','rewarding to you in itself'],
'ROMANCE-FADE':['Apart from losing the things you already said help closeness']
}
for i,needles in expect.items():
    for n in needles:
        check(f"repair_text:{i}:{n}", n in by[i]['question'], by[i]['question'])

check('M06_guard', 'direct constraints' in by['M06']['admission'] and 'direct hazards' in by['M06']['admission'])
check('M06_same_interpretation_task', 'What would you make of that?' in by['M06']['question'] and 'concern' not in by['M06']['question'].lower(), by['M06']['question'])
check('M06_no_assumed_reduced_reliance', 'Do not assume concern or reduced reliance' in by['M06']['interpretation_limit'], by['M06']['interpretation_limit'])
check('VERIFY_guard', 'group/source' in by['VERIFY']['admission'] and 'would not decide themselves' in by['VERIFY']['admission'])
check('ROMANCE_guard', 'ordinary inverse' in by['ROMANCE-FADE']['admission'])

explore=bank.get('exploratory_questions',[])
check('exploratory_count', len(explore)==1)
if explore:
    ex=explore[0]
    check('exploratory_unmapped', ex.get('mapping_status')=='unmapped_neutral_candidate')
    check('exploratory_no_credit', ex.get('automatic_evidence_credit') is False)

for phrase in ['ask only the missing piece','premise sufficiency','Inverse wording is not independent corroboration','Stop when no remaining route is both admissible','A brief, fleeting, or inconsistent reaction is still an eligible antecedent']:
    check('protocol:'+phrase, phrase.lower() in protocol.lower())

ev=json.loads((HERE/'EVIDENCE-GUIDE-v7.json').read_text())
ev_facets={x['facet_id'] for x in ev}
check('evidence_73_facets', len(ev)==73, str(len(ev)))
check('evidence_matches_requirements', ev_facets==facet_ids)
for x in ev:
    check(f"evidence_routes:{x['facet_id']}", bool(x.get('question_routes')) and all(r in idset for r in x.get('question_routes',[])), str(x.get('question_routes')))
check('no_evidence_route_to_retired_C0', all('C0' not in x.get('question_routes',[]) for x in ev))
x04=[x for x in ev if x['facet_id']=='X04.context_and_limits'][0]
check('X04_paired_interpretation', 'When paired with M05' in x04['narrow_supported_reading'], x04['narrow_supported_reading'])
check('X04_no_unearned_reduced_reliance', 'Reduced reliance' in x04['unsupported_extension'], x04['unsupported_extension'])

print(json.dumps({'ok':not errors,'errors':errors,'checks':len(checks),'passed':sum(1 for _,ok,_ in checks if ok)},indent=2))
if errors:
    raise SystemExit(1)
