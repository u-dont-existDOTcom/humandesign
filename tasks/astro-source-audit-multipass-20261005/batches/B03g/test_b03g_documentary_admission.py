import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
def validate(rs):
 assert len(rs)==35
 assert [r['record_number'] for r in rs]==list(range(3450,3485))
 assert [r['id'] for r in rs]==[f'R{i}' for i in range(3450,3485)]
 assert [r['source_local_id'] for r in rs]==[f'LXI-C{i:03}' for i in range(1,36)]
 assert all(r['historical_documentation_admitted'] and
  not r['real_outcome_independently_authenticated'] and
  not r['empirical_astrology_prediction_validated'] and
  not r['runtime_model_promoted'] and
  not r['accepted_as_empirical_prediction'] for r in rs)
 assert all(r['chapter']=='LXI' for r in rs[:-1])
 assert rs[-1]['chapter']=='LXII_NAVIGATION_ONLY'
 return True
class Admission(unittest.TestCase):
 def test_global_contiguous_documentary_units(self):
  self.assertTrue(validate(R['rules']))
  self.assertEqual(R['record_count'],35)
  self.assertEqual(R['chapter_lxi_source_units'],34)
 def test_original_draft_preserved(self):
  for before,after in zip(D,R['rules'],strict=True):
   for k in ('source_local_id','role','original_pdf_pages','printed_pages',
    'source_short_anchor_not_diplomatic','historical_author_report_paraphrase',
    'conditions_source_limits_or_chronology'):
    self.assertEqual(before[k],after[k])
   self.assertIsNone(before['global_record_number'])
   self.assertFalse(before['historical_documentation_admitted'])
 def test_each_original_span_maps_accepted_exactly_once(self):
  actual=[i for s in M['source_spans'] for i in s['canonical_record_ids']]
  self.assertEqual(sorted(actual),sorted(r['id'] for r in R['rules']))
  self.assertEqual(len(actual),35)
  self.assertEqual(M['span_count'],15)
 def test_original_images_sha256(self):
  for im in W['original_images']:
   self.assertEqual(H(im['path']),im['sha256'])
   self.assertEqual((B/im['path']).stat().st_size,im['bytes'])
 def test_frozen_acceptance_artifacts(self):
  for p,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_sha256')]:
   self.assertEqual(H(p),A[k],p)
 def test_historical_case_unverified(self):
  self.assertEqual(R['author_reported_servant_return_outcomes'],1)
  self.assertEqual(R['independently_authenticated_servant_outcomes'],0)
  self.assertEqual(R['empirically_validated_predictive_cases'],0)
  self.assertTrue(R['claim_one_or_two_days_not_scoreable_without_question_date'])
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertFalse(A['original_case_independently_authenticated'])
 def test_frozen_previous_source_counts(self):
  self.assertEqual(A['previous_accepted_lilly'],3449)
  self.assertEqual(A['new_documentary_records'],35)
  self.assertEqual(A['lilly_if_published'],3484)
  self.assertEqual(A['combined_if_published'],4550)
  self.assertEqual(len(U['issues']),16)
  self.assertFalse(A['canonical_published'])
 def test_author_explicit_qualification(self):
  txt=' '.join(r['historical_author_report_paraphrase'] for r in R['rules']).lower()
  self.assertIn('which if true',txt)
  self.assertIn('servant returned home early on the following friday',txt)
 def test_semantic_mutants_rejected(self):
  r=copy.deepcopy(R['rules']);r[4]['real_outcome_independently_authenticated']=True
  with self.assertRaises(AssertionError):validate(r)
  r=copy.deepcopy(R['rules']);r[-1]['chapter']='LXI'
  with self.assertRaises(AssertionError):validate(r)
  r=copy.deepcopy(R['rules']);r[0]['record_number']=1
  with self.assertRaises(AssertionError):validate(r)
if __name__=='__main__':unittest.main(verbosity=2)
