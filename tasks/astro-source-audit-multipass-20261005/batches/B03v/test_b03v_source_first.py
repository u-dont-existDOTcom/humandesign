import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
M=J('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED_SOURCE_LIMITS.json')
C=J('CLAIM_LEDGER.json')
O=J('SOURCE_ORDER_DRAFT.json')
def check(rows,spans):
 assert len(rows)==62 and len(spans)==16
 ids=[r['source_local_id'] for r in rows]
 assert ids==[f'LXXVI-C{i:03}' for i in range(1,63)]
 mapped=[k for s in spans for k in s['mapped_local_ids']]
 assert len(mapped)==62 and sorted(mapped)==sorted(ids)
 assert all(s['original_pdf_pages']==rows[ids.index(k)]['original_pdf_pages']
  for s in spans for k in s['mapped_local_ids'])
 assert all(r['printed_pages']==[n-34 for n in r['original_pdf_pages']] for r in rows)
 assert all(r['global_record_number'] is None and
  not r['historical_documentary_accepted'] and
  not r['independent_ecclesiastical_outcome_verified'] and
  not r['empirically_validated_forecast'] and
  not r['runtime_rule_promoted'] for r in rows)
 assert all(r['chapter']=='LXXVI' for r in rows[:-2])
 assert all(r['chapter']=='LXXVII_NAVIGATION_ONLY' for r in rows[-2:])
 assert [s['original_pdf_pages'][0] for s in spans]==sorted(s['original_pdf_pages'][0] for s in spans)
class SourceFirst(unittest.TestCase):
 def test_unique_reverse_image_mapping(self):
  check(D['rows'],M['source_spans'])
  self.assertEqual(O['ordered_ids'],[r['source_local_id'] for r in D['rows']])
 def test_exact_original_scans(self):
  self.assertEqual(W['original_body_pdf_pages'],[466,467,468])
  self.assertEqual(len(W['original_images']),3)
  for im in W['original_images']:
   raw=(B/im['path']).read_bytes()
   self.assertEqual(len(raw),im['bytes'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),im['sha256'])
 def test_previous_accepted_and_next_boundary(self):
  self.assertEqual(W['previous_accepted_lilly'],4384)
  self.assertEqual(W['next_numbered_chapter'],'LXXVII')
  self.assertEqual(W['next_heading_pdf'],468)
  self.assertEqual(W['original_full_pdf_sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
 def test_two_page_crossings(self):
  self.assertEqual([s['original_pdf_pages'] for s in M['source_spans'] if len(s['original_pdf_pages'])>1],[[466,467],[467,468]])
  self.assertEqual(len(O['cross_page_ids']),len([r for r in D['rows'] if len(r['original_pdf_pages'])>1]))
 def test_qualifiers_and_distinct_outcomes(self):
  t=' '.join(r['historical_author_paraphrase']+' '+r['original_conditions_and_uncertainty'] for r in D['rows']).lower()
  for term in ('reception','effort','competitor','benefic','tenth','ninth','retrograd'):
   self.assertIn(term,t,term)
 def test_independent_cases_and_limits(self):
  self.assertEqual(C['independently_authenticated_appointment_cases'],0)
  self.assertEqual(C['independently_verified_corruption_cases'],0)
  self.assertEqual(C['new_empirically_validated_predictions'],0)
  self.assertEqual(len(U['issues']),20)
 def test_duplicate_mapping_mutant_rejected(self):
  sp=copy.deepcopy(M['source_spans']);sp[0]['mapped_local_ids'].append(sp[1]['mapped_local_ids'][0])
  with self.assertRaises(AssertionError):check(D['rows'],sp)
 def test_wrong_page_mutant_rejected(self):
  rs=copy.deepcopy(D['rows']);rs[7]['original_pdf_pages']=[467]
  with self.assertRaises(AssertionError):check(rs,M['source_spans'])
 def test_false_empirical_mutant_rejected(self):
  rs=copy.deepcopy(D['rows']);rs[20]['empirically_validated_forecast']=True
  with self.assertRaises(AssertionError):check(rs,M['source_spans'])
 def test_next_chapter_leak_mutant_rejected(self):
  rs=copy.deepcopy(D['rows']);rs[-1]['chapter']='LXXVI'
  with self.assertRaises(AssertionError):check(rs,M['source_spans'])
if __name__=='__main__':unittest.main(verbosity=2)
