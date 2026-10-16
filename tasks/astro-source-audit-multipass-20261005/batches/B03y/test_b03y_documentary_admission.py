import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json');U=J('UNRESOLVED.json')
def check(rows):
 assert len(rows)==41
 assert [r['record_number'] for r in rows]==list(range(4509,4550))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(4509,4550)]
 assert all(r['historical_documentary_accepted'] and r['global_record_number']==r['record_number']
  and not r['independently_authenticated_parsonage_case']
  and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXIX' for r in rows[:-2])
 assert all(r['chapter']=='LXXX_NAVIGATION_ONLY' for r in rows[-2:])
class Admission(unittest.TestCase):
 def test_ids_sequential_boundary_and_nonvalidation(self):check(R)
 def test_draft_source_content_preserved(self):
  for d,r in zip(D,R,strict=True):
   for k in ('source_local_id','original_pdf_pages','role','historical_author_paraphrase',
    'original_source_qualifications','chapter','short_original_anchor_not_diplomatic'):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d['global_record_number'])
 def test_bidirectional_mapping_exact(self):
  gids=[k for s in M['source_spans'] for k in s['accepted_global_record_ids']]
  self.assertEqual(len(gids),41)
  self.assertEqual(sorted(gids),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],7)
 def test_accepted_source_hashes(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')]:
   self.assertEqual(H(f),A[k],f)
 def test_empirical_case_not_validated(self):
  self.assertEqual(A['prior_lilly_accepted'],4508)
  self.assertEqual(A['new_documentary_records'],41)
  self.assertEqual(A['lilly_if_published'],4549)
  self.assertEqual(A['combined_if_published'],5615)
  self.assertEqual(A['next_chapter'],'LXXX')
  self.assertEqual(len(U['issues']),17)
  self.assertEqual(A['authorial_unverified_outcome_reports'],1)
  self.assertEqual(A['independently_verified_parsonage_outcomes'],0)
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertFalse(A['remote_canonical_published'])
 def test_false_prediction_mutant_rejected(self):
  changed=copy.deepcopy(R);changed[12]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(changed)
if __name__=='__main__':unittest.main(verbosity=2)
