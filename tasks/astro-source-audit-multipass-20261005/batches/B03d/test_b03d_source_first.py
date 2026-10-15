"""Historical original-source boundaries, negative cases and mapping tests."""
import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
C=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
L=J('CLAIM_LEDGER.json')
def check(rows,spans):
 assert len(rows)==38 and len(spans)==18
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LVIII-C{i:03}' for i in range(1,39)]
 mapped=[i for s in spans for i in s['mapped_source_local_ids']]
 assert sorted(mapped)==sorted(ids) and len(mapped)==len(ids)
 by={r['source_local_id']:r for r in rows}
 assert all(by[id]['original_pdf_pages']==s['original_pdf_pages']
  for s in spans for id in s['mapped_source_local_ids'])
 assert all(r['global_record_number'] is None and not r['historical_documentation_accepted']
  and r['observed_real_adversary_cases']==0 and not r['empirical_predictive_validation']
  and not r['active_personality_or_honesty_classifier']
  and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LVIII' for r in rows[:-1])
 assert rows[-1]['role']=='next_heading_boundary' and rows[-1]['chapter']=='LIX_HEADING_ONLY'
 return True
class Source(unittest.TestCase):
 def test_bijection(self):self.assertTrue(check(D['rows'],C['source_spans']))
 def test_witnesses(self):
  self.assertEqual(W['source_original_pdf_pages'],[417,418,419])
  for v in W['images']:
   d=(B/v['relative_path']).read_bytes()
   self.assertEqual(hashlib.sha256(d).hexdigest(),v['sha256'])
   self.assertEqual(len(d),v['bytes'])
 def test_multiple_question_types(self):
  t=' '.join(x['historical_claim_paraphrase']+' '+x['conditions_and_limits'] for x in D['rows']).lower()
  for q in ('nominated','general','twelfth','reception','separating','applying','reconciliation'):
   self.assertIn(q,t)
 def test_first_person_not_independent(self):
  self.assertEqual(sum(r['role']=='marginal_author_claim' for r in D['rows']),1)
  self.assertEqual(L['new_predictive_validations'],0)
  self.assertEqual(L['independent_confirmations_of_hidden_adversaries'],0)
 def test_boundaries_and_limits(self):
  self.assertEqual(len(U['issues']),14)
  self.assertEqual(C['span_count'],18)
  self.assertEqual(W['previous_accepted_lilly_count'],3322)
 def test_mutation_no_duplicate_source(self):
  m=copy.deepcopy(C['source_spans']);m[0]['mapped_source_local_ids'].append(m[1]['mapped_source_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],m)
 def test_mutation_rejects_unverified_person_label(self):
  r=copy.deepcopy(D['rows']);r[4]['observed_real_adversary_cases']=1
  with self.assertRaises(AssertionError):check(r,C['source_spans'])
 def test_mutation_rejects_boundary_leak(self):
  r=copy.deepcopy(D['rows']);r[-1]['chapter']='LVIII'
  with self.assertRaises(AssertionError):check(r,C['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
