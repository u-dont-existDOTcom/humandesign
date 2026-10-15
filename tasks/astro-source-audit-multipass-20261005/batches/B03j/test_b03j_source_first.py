import unittest
import copy,hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
O=J('SOURCE_ORDER_DRAFT.json')
def validate(rows,spans):
 assert len(rows)==59 and len(spans)==18
 ids=[r['local_id'] for r in rows]
 assert ids==[f'LXIV-C{i:03}' for i in range(1,60)]
 mapped=[k for s in spans for k in s['mapped_local_ids']]
 assert len(mapped)==59 and sorted(mapped)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages'] for s in spans for k in s['mapped_local_ids'])
 assert all(r['global_record_number'] is None and not r['accepted_historical_documentary'] and
  not r['real_world_case_independently_authenticated'] and
  not r['empirical_predictive_outcome_validated'] and not r['runtime_rule_promoted'] for r in rows)
 assert all(r['original_printed_pages']==[n-34 for n in r['original_pdf_pages']] for r in rows)
 assert all(r['chapter_logical']=='LXIV' and r['chapter_printed_original']=='LIV' for r in rows[:-1])
 assert rows[-1]['role']=='boundary' and rows[-1]['chapter_logical']=='LXV_NAVIGATION_ONLY'
 return True
class SourceFirst(unittest.TestCase):
 def test_bijection(self):
  self.assertTrue(validate(D['rows'],M['source_spans']))
  self.assertEqual(O['ordered_local_ids'],[r['local_id'] for r in D['rows']])
 def test_actual_1647_images(self):
  self.assertEqual(W['original_body_pdf_pages'],[431,432,433])
  for x in W['original_images']:
   data=(B/x['path']).read_bytes()
   self.assertEqual(len(data),x['bytes'])
   self.assertEqual(hashlib.sha256(data).hexdigest(),x['sha256'])
 def test_source_body_boundaries(self):
  self.assertEqual(W['printed_heading_literal'],'LIV')
  self.assertEqual(W['sequential_chapter_identity'],'LXIV')
  self.assertEqual(W['following_chapter_printed'],'LXV')
  self.assertEqual(W['previous_accepted_lilly'],3571)
 def test_case_and_date(self):
  text=' '.join(r['historical_source_paraphrase'] for r in D['rows']).lower()
  self.assertIn('10 february 1638',text)
  self.assertIn('8:45 am',text)
  self.assertIn('1637',text)
 def test_nonresponse_and_partial_recovery(self):
  txt=' '.join(r['historical_source_paraphrase']+' '+r['source_conditions_uncertainty'] for r in D['rows']).lower()
  self.assertIn('failed initial search',txt)
  self.assertIn('partial',txt)
  self.assertIn('some fish',txt)
  self.assertIn('onions',txt)
  self.assertEqual(C['source_author_reported_partially_recovered_fish_case_count'],1)
  self.assertEqual(C['source_author_reported_full_recovery_case_count'],0)
 def test_negative_general_rule_retained(self):
  t=' '.join(r['historical_source_paraphrase'] for r in D['rows']).lower()
  self.assertIn('discovery without goods returned',t)
  self.assertIn('complete recovery',t)
  self.assertIn('partial return',t)
 def test_uncertainty_count(self):
  self.assertEqual(len(U['issues']),20)
  self.assertEqual(M['span_count'],18)
  self.assertEqual(C['new_empirically_validated_astrology_predictions'],0)
 def test_cross_page_continuity(self):
  spans=[x['original_pdf_pages'] for x in M['source_spans'] if len(x['original_pdf_pages'])>1]
  self.assertEqual(spans,[[431,432],[432,433]])
 def test_mutant_duplicate_record(self):
  fake=copy.deepcopy(M['source_spans'])
  fake[0]['mapped_local_ids'].append(fake[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):validate(D['rows'],fake)
 def test_mutant_claimed_empirical(self):
  fake=copy.deepcopy(D['rows'])
  fake[10]['empirical_predictive_outcome_validated']=True
  with self.assertRaises(AssertionError):validate(fake,M['source_spans'])
 def test_mutant_wrong_original_page(self):
  fake=copy.deepcopy(D['rows'])
  fake[1]['original_pdf_pages']=[432]
  with self.assertRaises(AssertionError):validate(fake,M['source_spans'])
 def test_mutant_numbering_merge(self):
  fake=copy.deepcopy(D['rows'])
  fake[0]['chapter_printed_original']='LXIV'
  with self.assertRaises(AssertionError):validate(fake,M['source_spans'])
 def test_mutant_boundary(self):
  fake=copy.deepcopy(D['rows'])
  fake[-1]['chapter_logical']='LXIV'
  with self.assertRaises(AssertionError):validate(fake,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
