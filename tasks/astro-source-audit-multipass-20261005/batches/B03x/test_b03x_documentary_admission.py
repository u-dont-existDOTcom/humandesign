import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda n:json.loads((B/n).read_text())
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules'];M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json');U=J('UNRESOLVED.json')
def check(rows):
 assert len(rows)==24
 assert [r['record_number'] for r in rows]==list(range(4485,4509))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(4485,4509)]
 assert all(r['historical_documentary_accepted'] and not r['independently_authenticated_dream_case']
  and not r['empirically_validated_prediction'] and not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXXVIII' for r in rows[:-2])
 assert all(r['chapter']=='LXXIX_NAVIGATION_ONLY' for r in rows[-2:])
 assert len([r for r in rows if r['role']=='authorial_outcome_claim'])==1
class Admission(unittest.TestCase):
 def test_complete_contiguous_ids_and_isolation(self):check(R)
 def test_source_first_fields_immutable(self):
  for d,r in zip(D,R,strict=True):
   for k in ('source_local_id','role','original_pdf_pages','historical_author_paraphrase',
             'original_source_qualifications','chapter','short_original_anchor_not_diplomatic'):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d['global_record_number'])
 def test_reverse_coverage(self):
  g=[k for s in M['source_spans'] for k in s['accepted_global_record_ids']]
  self.assertEqual(len(g),len(set(g)))
  self.assertEqual(sorted(g),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],6)
 def test_hashes(self):
  for n,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),
    ('UNRESOLVED.json','unresolved_sha256'),('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
    ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','source_visual_audit_sha256')]:
   self.assertEqual(H(n),A[k],n)
 def test_historical_evidence_not_empirical(self):
  self.assertEqual(A['prior_lilly_accepted'],4484)
  self.assertEqual(A['lilly_if_published'],4508)
  self.assertEqual(A['combined_if_published'],5574)
  self.assertEqual(A['authorial_unverified_success_reports'],1)
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertEqual(len(U['issues']),14)
  self.assertFalse(A['remote_canonical_published'])
 def test_false_independent_validation_mutant(self):
  changed=copy.deepcopy(R)
  changed[-3]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):check(changed)
if __name__=='__main__':unittest.main(verbosity=2)
