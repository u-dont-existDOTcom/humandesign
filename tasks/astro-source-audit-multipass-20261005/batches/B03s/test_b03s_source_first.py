import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
S=J('SOURCE_ORDER_DRAFT.json')
def valid(rows,spans):
 assert len(rows)==34 and len(spans)==10
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LXXIII-C{i:03}' for i in range(1,35)]
 m=[k for s in spans for k in s['mapped_source_local_ids']]
 assert len(m)==34 and sorted(m)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages'] for s in spans for k in s['mapped_source_local_ids'])
 assert all(r['printed_pages']==[p-34 for p in r['original_pdf_pages']] for r in rows)
 assert all(r['global_record_number'] is None and not r['historical_documentary_admitted'] and
  not r['independent_payment_outcome_verified'] and not r['empirically_validated_prediction'] and
  not r['runtime_rule_promoted'] for r in rows)
 assert all(r['chapter']=='LXXIII' for r in rows[:-2])
 assert all(r['chapter']=='LXXIV_NAVIGATION_ONLY' for r in rows[-2:])
 assert rows[-1]['original_pdf_pages']==[456]
class SourceFirst(unittest.TestCase):
 def test_original_to_draft_exact_map(self):
  valid(D['rows'],M['source_spans'])
  self.assertEqual(S['ordered_ids'],[r['source_local_id'] for r in D['rows']])
 def test_primary_page_hashes(self):
  self.assertEqual(W['source_body_pdf_pages'],[455,456])
  for v in W['original_images']:
   raw=(B/v['path']).read_bytes()
   self.assertEqual(len(raw),v['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),v['sha256'])
 def test_original_fig_and_predecessor(self):
  self.assertEqual(W['previous_accepted_lilly'],4136)
  self.assertEqual(W['source_chart_date'],'13 July 1634')
  self.assertEqual(W['source_chart_time'],'6:15 PM')
  self.assertEqual(W['independently_confirmed_payment_receipts'],0)
 def test_cross_page_and_navigation(self):
  self.assertEqual([s['original_pdf_pages'] for s in M['source_spans'] if len(s['original_pdf_pages'])>1],[[455,456]])
  self.assertEqual(len(S['next_navigation_only']),2)
 def test_conditional_roles_separate(self):
  t=' '.join(r['historical_author_paraphrase']+' '+r['original_scope_uncertainty'] for r in D['rows']).lower()
  for term in ('saturn','jupiter','moon','venus','derived second','transfer','confirmation'):
   self.assertIn(term,t,term)
 def test_no_independently_verified_success(self):
  self.assertEqual(C['author_reported_general_success_claims'],1)
  self.assertEqual(C['separately_verified_paid_portion_cases'],0)
  self.assertEqual(C['empirically_validated_astrological_predictions'],0)
  self.assertEqual(len(U['issues']),17)
 def test_duplicate_map_mutant_rejected(self):
  s=copy.deepcopy(M['source_spans']);s[0]['mapped_source_local_ids'].append(s[1]['mapped_source_local_ids'][0])
  with self.assertRaises(AssertionError):valid(D['rows'],s)
 def test_false_prediction_mutant_rejected(self):
  r=copy.deepcopy(D['rows']);r[4]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):valid(r,M['source_spans'])
 def test_boundary_mutant_rejected(self):
  r=copy.deepcopy(D['rows']);r[-1]['chapter']='LXXIII'
  with self.assertRaises(AssertionError):valid(r,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
