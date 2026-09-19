"""Static artifact checks. Does NOT classify answers or prove semantic validity."""
from pathlib import Path
import ast,hashlib,json,time
P=Path(__file__).resolve().parent

def check():
 start=time.perf_counter();results=[]
 def test(name,condition):
  results.append({'check':name,'passed':bool(condition)})
  if not condition: raise AssertionError(name)
 read=lambda name:json.loads((P/name).read_text())
 b=read('interviewer-bank-v5.json');qs=b['questions'];by={q['id']:q for q in qs}
 old=read('source-bank-v4.json'); audit=read('NODE-AUDIT.json');ev=read('EVIDENCE-REVIEW.json');req=read('source-requirements-v2.json');cases=read('DIALOGUE-CHALLENGES.json')
 test('Exact frozen source bank',hashlib.sha256((P/'source-bank-v4.json').read_bytes()).hexdigest()=='dced7797a726003d7efd1feb928feb7ca6566d8a87dbe68bab8c43db4a87ab01')
 test('79 unique candidate entries; 75 inherited entries preserved',len(qs)==len(by)==79 and {q['id'] for q in old['questions']}<=set(by))
 test('Every final entry has a specific review row',len(audit)==79 and {x['id'] for x in audit}==set(by) and all(x['question']==by[x['id']]['question'] for x in audit))
 test('No stale single-parent field beside explicit context references',all('parent' not in q for q in qs))
 test('Every context reference exists',all(x in by for q in qs for x in q['context_sources']))
 test('Every family contains each entry exactly once',sorted(x for ids in b['families'].values() for x in ids)==sorted(by))
 facets={f for d in req['domains'] for f in d['facets']}
 test('All 73 source identifiers reviewed with a narrow reading and prohibited extension',len(ev)==len(facets)==73 and {e['facet_id'] for e in ev}==facets and all(e['narrow_supported_reading'] and e['unsupported_extension'] for e in ev))
 test('Evidence-guide routes exist and actually target the identifier',all(e['question_routes'] and all(e['facet_id'] in by[r]['planning_targets'] for r in e['question_routes']) for e in ev))
 test('Question presentation never gives automatic evidence credit',all(q['automatic_evidence_credit'] is False for q in qs) and b['required_question_count'] is None)
 test('Invitation contrast asks the same response task',by['G06']['question'].endswith('What would you usually do?') and by['R02']['question'].endswith('What would you usually do?'))
 test('Cancellation is not the novelty route',by['C0']['planning_targets']==[] and 'D21.novelty_disruption' in by['ROUTINE-CHANGE']['planning_targets'])
 test('Promise question allows not continuing',by['M03']['question'].endswith('What would you usually do?') and 'keep you following' not in by['M03']['question'])
 test('32 complete authored dialogue review records',len(cases)==len({c['id'] for c in cases})==32 and all(c['supported_record'] and c['rejected_continuation'] and c['semantic_review'] for c in cases))
 test('Dialogue source and destination IDs exist',all(c['question_id'] in by and (c['next_question_id'] is None or c['next_question_id'] in by) for c in cases))
 test('All nonliteral delivered question wording is explicitly recorded',all(c['question']==by[c['question_id']]['question'] or c.get('adaptation') for c in cases) and all(c['next_question_id'] not in by or c['reviewed_next_utterance']==by[c['next_question_id']]['question'] or c.get('next_question_adaptation') for c in cases))
 test('Nonadjacent feeling reference is in actual delivered wording',cases[12]['question']=='After the argument you described earlier, what usually happens to that tension?')
 test('Pause-plus-answer case has no next question',cases[20]['next_question_id'] is None and '?' not in cases[20]['reviewed_next_utterance'])
 test('No-signal and no-skill examples do not launch dependent probes',cases[8]['next_question_id']=='G10' and cases[30]['next_question_id']=='G01')
 for f in P.glob('*.py'):ast.parse(f.read_text(),filename=f.name)
 test('All included Python files parse without executing models',True)
 return {'verification_class':'static artifact and explicitly authored-case consistency; not NLP or human validity','checks':results,'passed':len(results),'failed':0,'elapsed_seconds':time.perf_counter()-start,'runtime_model_calls':0}
if __name__=='__main__':print(json.dumps(check(),indent=2))
