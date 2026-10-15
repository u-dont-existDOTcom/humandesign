import hashlib,json,unittest,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
A=J('ACCEPTANCE.json')
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
U=J('UNRESOLVED.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
def valid(rs):
 assert len(rs)==59
 assert [r['record_number'] for r in rs]==list(range(3572,3631))
 assert [r['id'] for r in rs]==[f'R{i}' for i in range(3572,3631)]
 assert all(r['accepted_historical_documentary'] and
  not r['real_world_case_independently_authenticated'] and
  not r['empirical_predictive_outcome_validated'] and
  not r['runtime_rule_promoted'] and
  not r['accepted_as_empirical_prediction'] for r in rs)
 assert all(r['chapter_logical']=='LXIV' and r['chapter_printed_original']=='LIV' for r in rs[:-1])
 assert rs[-1]['chapter_logical']=='LXV_NAVIGATION_ONLY'
class Admission(unittest.TestCase):
 def test_contiguous_global_ids(self):valid(R)
 def test_original_paraphrase_preserved(self):
  for d,r in zip(D,R,strict=True):
   for k in ('local_id','role','chapter_logical','chapter_printed_original',
    'original_pdf_pages','historical_source_paraphrase','source_conditions_uncertainty'):
    self.assertEqual(d[k],r[k],(d['local_id'],k))
   self.assertIsNone(d['global_record_number'])
 def test_source_to_accepted_bijection(self):
  got=[i for sp in M['source_spans'] for i in sp['canonical_record_ids']]
  self.assertEqual(len(got),59)
  self.assertEqual(sorted(got),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],18)
 def test_source_images_sha(self):
  for im in W['original_images']:
   self.assertEqual(H(im['path']),im['sha256'])
   self.assertEqual((B/im['path']).stat().st_size,im['bytes'])
 def test_frozen_admission_hashes(self):
  for f,key in [('RULES.json','rules_sha256'),
   ('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261015.md','original_visual_review_sha256')]:
   self.assertEqual(H(f),A[key],f)
 def test_case_outcome_not_validated(self):
  self.assertEqual(A['author_reported_partially_recovered_fish_cases'],1)
  self.assertEqual(A['author_reported_complete_recovery_cases'],0)
  self.assertEqual(A['independently_verified_case_outcomes'],0)
  self.assertEqual(A['independently_verified_thief_identity'],0)
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertTrue(A['remaining_fish_unrecovered_or_relinquished'])
 def test_bounded_original_numbering(self):
  self.assertEqual(A['previous_accepted_lilly'],3571)
  self.assertEqual(A['new_documentary_records'],59)
  self.assertEqual(A['lilly_if_published'],3630)
  self.assertEqual(A['combined_if_published'],4696)
  self.assertEqual(A['original_printed_heading'],'LIV')
  self.assertEqual(A['logical_number'],'LXIV')
  self.assertEqual(A['next_printed_chapter'],'LXV')
  self.assertEqual(len(U['issues']),20)
  self.assertFalse(A['canonical_published'])
 def test_mutants_rejected(self):
  bad=copy.deepcopy(R);bad[5]['record_number']=999
  with self.assertRaises(AssertionError):valid(bad)
  bad=copy.deepcopy(R);bad[12]['real_world_case_independently_authenticated']=True
  with self.assertRaises(AssertionError):valid(bad)
  bad=copy.deepcopy(R);bad[-1]['chapter_logical']='LXIV'
  with self.assertRaises(AssertionError):valid(bad)
  bad=copy.deepcopy(R);bad[0]['chapter_printed_original']='LXIV'
  with self.assertRaises(AssertionError):valid(bad)
if __name__=='__main__':unittest.main(verbosity=2)
