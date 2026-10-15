import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED.json')
def acceptable(rows):
 assert [r['record_number'] for r in rows]==list(range(3419,3450))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(3419,3450)]
 assert all(r['global_record_number']==r['record_number'] for r in rows)
 assert all(r['historical_documentation_admitted'] and
  not r['empirical_astrology_prediction_validated'] and
  not r['real_outcome_independently_authenticated'] and
  not r['runtime_model_promoted'] and
  not r['accepted_as_empirical_prediction'] for r in rows)
 assert all(r['chapter']=='LX' for r in rows[:-1])
 assert rows[-1]['chapter']=='LXI_NAVIGATION_ONLY'
class Admission(unittest.TestCase):
 def test_consecutive_record_numbers(self):
  acceptable(R['rules'])
  self.assertEqual(R['record_count'],31)
  self.assertEqual(R['substantive_lx_records'],30)
  self.assertEqual(R['lxi_heading_only'],1)
 def test_provisional_source_exact_preserved(self):
  for before,after in zip(D,R['rules'],strict=True):
   for k in ('source_local_id','chapter','role','original_pdf_pages',
             'printed_pages','historical_author_report_paraphrase',
             'source_short_anchor_not_diplomatic','conditions_source_limits_or_chronology'):
    self.assertEqual(before[k],after[k],(k,before['source_local_id']))
   self.assertIsNone(before['global_record_number'])
   self.assertFalse(before['historical_documentation_admitted'])
 def test_source_map_bijective(self):
  ids=[i for s in M['source_spans'] for i in s['canonical_record_ids']]
  self.assertEqual(len(ids),31)
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R['rules']))
  self.assertEqual(M['span_count'],13)
 def test_original_images_integrity(self):
  for img in W['original_images']:
   self.assertEqual(H(img['path']),img['sha256'])
   self.assertEqual((B/img['path']).stat().st_size,img['size_bytes'])
 def test_frozen_acceptance_files(self):
  for n,key in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','source_reverse_map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','image_audit_sha256')]:
   self.assertEqual(H(n),A[key],n)
 def test_historical_case_not_empirical(self):
  self.assertFalse(R['original_case_independently_authenticated'])
  self.assertEqual(R['source_internal_reported_marriage_outcomes'],1)
  self.assertEqual(R['independently_confirmed_marriage_outcomes'],0)
  self.assertEqual(R['new_empirical_predictions_validated'],0)
  self.assertEqual(R['runtime_promotions'],0)
  self.assertEqual(A['empirical_astrology_predictions_validated'],0)
 def test_source_limits(self):
  self.assertEqual(len(U['issues']),13)
  self.assertEqual(A['previous_lilly_accepted'],3418)
  self.assertEqual(A['lilly_if_published'],3449)
  self.assertEqual(A['combined_if_published'],4515)
 def test_mutants_detected(self):
  bad=copy.deepcopy(R['rules']);bad[4]['real_outcome_independently_authenticated']=True
  with self.assertRaises(AssertionError):acceptable(bad)
  bad=copy.deepcopy(R['rules']);bad[-1]['chapter']='LX'
  with self.assertRaises(AssertionError):acceptable(bad)
  bad=copy.deepcopy(R['rules']);bad[0]['record_number']=3449
  with self.assertRaises(AssertionError):acceptable(bad)
if __name__=='__main__':unittest.main(verbosity=2)
