import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
def check(rows):
 assert len(rows)==32
 assert [r['record_number'] for r in rows]==list(range(3172,3204))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(3172,3204)]
 assert [r['source_local_id'] for r in rows]==[f'LV-C{i:03}' for i in range(1,33)]
 assert all(r['historical_documentary_admitted'] and not r['accepted_as_empirical_astro_prediction']
  and r['validated_predictive_results']==0 and r['new_independent_real_world_cases']==0
  and not r['runtime_promoted'] for r in rows)
 assert all(r['chapter']=='LV' for r in rows[:-1])
 assert rows[-1]['chapter']=='LVI_BOUNDARY_ONLY'
 return True
class TestAdmission(unittest.TestCase):
 def test_consecutive_id_and_scope(self):
  self.assertTrue(check(R['rules']))
  self.assertEqual(R['chapter_lv_substantive_units'],31)
  self.assertEqual(R['next_chapter_navigation_only_units'],1)
 def test_source_preservation(self):
  for before,after in zip(D['rows'],R['rules'],strict=True):
   for k in ('source_local_id','chapter','role','original_pdf_pages','printed_pages',
    'conditional_statement_author_claim_not_empirical','preconditions_and_disjunctions',
    'exception_or_ambiguity','anchor_editorially_shortened_not_diplomatic'):
    self.assertEqual(before[k],after[k])
   self.assertIsNone(before['global_record_number'])
   self.assertFalse(before['historical_documentary_admitted'])
 def test_two_way_mapping(self):
  mapped=[i for s in M['source_spans'] for i in s['canonical_record_ids']]
  self.assertEqual(sorted(mapped),sorted(r['id'] for r in R['rules']))
  self.assertEqual(len(mapped),32)
  self.assertEqual(len(M['source_spans']),17)
 def test_source_witness_integrity(self):
  for im in W['original_images']:
   self.assertEqual(H(im['relative_path']),im['sha256'])
   self.assertEqual((B/im['relative_path']).stat().st_size,im['bytes'])
  for p,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','source_reverse_map_sha256')]:
   self.assertEqual(H(p),A[k])
 def test_exceptions_and_uncertainties(self):
  self.assertEqual(len(U['issues']),16)
  self.assertEqual(A['source_uncertainties_retained'],16)
  self.assertEqual(A['new_empirical_astrological_predictions_validated'],0)
  self.assertEqual(A['new_authenticated_partnership_cases'],0)
  self.assertFalse(A['fully_diplomatic_second_reader_done'])
 def test_baseline_next_and_claim_safety(self):
  self.assertEqual(A['previous_accepted_lilly'],3171)
  self.assertEqual(A['lilly_if_published'],3203)
  self.assertEqual(A['combined_if_published'],4269)
  self.assertFalse(A['canonical_published'])
  self.assertEqual(R['rules'][-1]['original_pdf_pages'],[413])
  self.assertEqual(R['runtime_promotions'],0)
 def test_mutant_counterexamples(self):
  r=copy.deepcopy(R['rules']);r[4]['historical_documentary_admitted']=False
  with self.assertRaises(AssertionError):check(r)
  r=copy.deepcopy(R['rules']);r[-1]['chapter']='LV'
  with self.assertRaises(AssertionError):check(r)
  r=copy.deepcopy(R['rules']);r[2]['validated_predictive_results']=1
  with self.assertRaises(AssertionError):check(r)
if __name__=='__main__':unittest.main(verbosity=2)
