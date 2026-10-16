import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
W=J('SOURCE_WINDOW_MANIFEST.json')
U=J('UNRESOLVED.json')
def check(rows):
 assert len(rows)==153
 assert [r['record_number'] for r in rows]==list(range(4171,4324))
 assert [r['id'] for r in rows]==[f'R{n}' for n in range(4171,4324)]
 assert all(r['global_record_number']==r['record_number'] and
  r['historical_documentary_accepted'] and
  not r['independently_authenticated_case_outcome'] and
  not r['empirically_validated_prediction'] and
  not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXIV' for r in rows[:-2])
 assert all(r['chapter']=='LXXV_NAVIGATION_ONLY' for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_accepted_ids_and_no_runtime(self):check(R)
 def test_provisional_original_unaltered(self):
  for a,b in zip(D,R,strict=True):
   for k in ('local_id','chapter','role','original_pdf_pages','historical_author_paraphrase',
    'source_condition_uncertainty'):
    self.assertEqual(a[k],b[k])
   self.assertIsNone(a['global_record_number'])
 def test_every_source_passage_mapped_once(self):
  mapped=[id for s in M['source_spans'] for id in s['accepted_record_ids']]
  self.assertEqual(len(mapped),153)
  self.assertEqual(sorted(mapped),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],28)
 def test_original_image_sha256(self):
  for v in W['original_images']:
   self.assertEqual(H(v['path']),v['sha256'])
   self.assertEqual((B/v['path']).stat().st_size,v['bytes'])
 def test_admission_receipts_stable(self):
  for f,k in [('RULES.json','rules_sha256'),
   ('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_source_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_audit_sha256')]:
   self.assertEqual(H(f),A[k])
 def test_canonical_boundary_and_no_case_claim(self):
  self.assertEqual(A['prior_accepted_lilly'],4170)
  self.assertEqual(A['new_documentary_records'],153)
  self.assertEqual(A['lilly_if_published'],4323)
  self.assertEqual(A['combined_if_published'],5389)
  self.assertEqual(A['next_numbered_chapter'],'LXXV')
  self.assertEqual(A['next_original_pdf_page'],463)
  self.assertEqual(len(U['issues']),32)
  self.assertTrue(A['no_independently_verified_journey_outcomes'])
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertFalse(A['remotely_published'])
 def test_wrong_number_mutation(self):
  rs=copy.deepcopy(R);rs[20]['record_number']=999
  with self.assertRaises(AssertionError):check(rs)
 def test_false_predictive_mutation(self):
  rs=copy.deepcopy(R);rs[48]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(rs)
 def test_swallowed_following_chapter_mutation(self):
  rs=copy.deepcopy(R);rs[-1]['chapter']='LXXIV'
  with self.assertRaises(AssertionError):check(rs)
if __name__=='__main__':unittest.main(verbosity=2)
