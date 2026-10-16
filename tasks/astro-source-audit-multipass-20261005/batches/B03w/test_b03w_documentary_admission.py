import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text(encoding='utf-8'))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
def check(rows):
 assert len(rows)==38
 assert [r['record_number'] for r in rows]==list(range(4447,4485))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(4447,4485)]
 assert all(r['historical_documentary_accepted'] and
  r['global_record_number']==r['record_number'] and
  not r['independently_authenticated_dream_case'] and
  not r['empirically_validated_prediction'] and
  not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXVII' for r in rows[:-2])
 assert all(r['chapter']=='LXXVIII_NAVIGATION_ONLY' for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_contiguous_original_global_ids(self):check(R)
 def test_original_clauses_survive(self):
  for old,new in zip(D,R,strict=True):
   for k in ('source_local_id','role','original_pdf_pages',
    'historical_author_paraphrase','original_source_qualifications','chapter'):
    self.assertEqual(old[k],new[k])
   self.assertIsNone(old['global_record_number'])
 def test_source_reverse_bijection(self):
  refs=[k for s in M['source_spans'] for k in s['accepted_global_record_ids']]
  self.assertEqual(len(refs),38)
  self.assertEqual(sorted(refs),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],8)
 def test_byte_identity(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')]:
   self.assertEqual(H(f),A[k],f)
 def test_no_independent_outcomes_or_runtime(self):
  self.assertEqual(A['prior_lilly_accepted'],4446)
  self.assertEqual(A['new_documentary_records'],38)
  self.assertEqual(A['lilly_if_published'],4484)
  self.assertEqual(A['combined_if_published'],5550)
  self.assertEqual(A['next_chapter'],'LXXVIII')
  self.assertEqual(len(U['issues']),15)
  self.assertEqual(A['independently_verified_dream_outcomes'],0)
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertFalse(A['remote_canonical_published'])
 def test_semantic_mutants(self):
  rs=copy.deepcopy(R);rs[2]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(rs)
  rs=copy.deepcopy(R);rs[-1]['chapter']='LXXVII'
  with self.assertRaises(AssertionError):check(rs)
if __name__=='__main__':unittest.main(verbosity=2)
