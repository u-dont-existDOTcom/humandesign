import copy,hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
U=J('UNRESOLVED.json')
def validate(rows):
 assert [r['record_number'] for r in rows]==list(range(3977,4008))
 assert [r['id'] for r in rows]==[f'R{i}' for i in range(3977,4008)]
 assert all(r['historical_documentary_admitted'] and
  not r['independent_danger_outcome_verified'] and
  not r['empirically_validated_prediction'] and
  not r['runtime_model_promoted'] for r in rows)
 assert all(r['chapter']=='LXIX' for r in rows[:-1])
 assert rows[-1]['chapter']=='LXX_NAVIGATION_ONLY'
class Admission(unittest.TestCase):
 def test_contiguous_ids(self):validate(R)
 def test_exact_provisional_draft_preserved(self):
  for a,b in zip(D,R,strict=True):
   for k in ('local_id','original_pdf_pages','role','historical_author_paraphrase','source_conditions_and_limits'):
    self.assertEqual(a[k],b[k])
   self.assertIsNone(a['global_record_number'])
 def test_original_reverse_source_bijection(self):
  ids=[k for s in M['source_spans'] for k in s['canonical_record_ids']]
  self.assertEqual(len(ids),31)
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R))
  self.assertEqual(M['span_count'],12)
 def test_original_hashes(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
   ('UNRESOLVED.json','unresolved_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','audit_sha256')]:
    self.assertEqual(H(f),A[k])
 def test_canonical_previous_boundaries(self):
  self.assertEqual(A['previous_lilly_accepted'],3976)
  self.assertEqual(A['new_documentary_records'],31)
  self.assertEqual(A['lilly_if_published'],4007)
  self.assertEqual(A['combined_if_published'],5073)
  self.assertEqual(A['next_chapter'],'LXX')
  self.assertEqual(len(U['issues']),14)
  self.assertFalse(A['remote_published'])
 def test_no_unverified_actual_events(self):
  self.assertEqual(A['independent_danger_outcomes'],0)
  self.assertEqual(A['empirically_validated_predictions'],0)
  self.assertEqual(A['runtime_promotions'],0)
 def test_mutated_outcome_disallowed(self):
  bad=copy.deepcopy(R);bad[7]['empirically_validated_prediction']=True
  with self.assertRaises(AssertionError):validate(bad)
 def test_mutated_heading_disallowed(self):
  bad=copy.deepcopy(R);bad[-1]['chapter']='LXIX'
  with self.assertRaises(AssertionError):validate(bad)
if __name__=='__main__':unittest.main(verbosity=2)
