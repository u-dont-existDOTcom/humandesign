import unittest,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
class Admission(unittest.TestCase):
 def test_contiguous_ids(self):
  self.assertEqual([r['record_number'] for r in R],list(range(4008,4053)))
  self.assertTrue(all(r['historical_documentary_admitted'] and not r['empirical_predictive_accuracy_validated'] for r in R))
  self.assertEqual(R[-1]['chapter'],'LXXI_NAVIGATION_ONLY')
 def test_provisional_source_preserved(self):
  for a,b in zip(D,R,strict=True):
   for k in ('local_id','role','historical_author_claim_paraphrase','source_scope_and_limitations','original_pdf_pages'):
    self.assertEqual(a[k],b[k])
 def test_reverse_source_coverage(self):
  seen=[k for s in M['source_spans'] for k in s['canonical_record_ids']]
  self.assertEqual(len(seen),45)
  self.assertEqual(sorted(seen),sorted(r['id'] for r in R))
 def test_original_hashes(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
   ('UNRESOLVED.json','limits_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','audit_sha256')]:
    self.assertEqual(H(f),A[k])
 def test_outcomes_not_empirical(self):
  self.assertEqual(A['historical_author_reported_cases'],1)
  self.assertEqual(A['independently_authenticated_cases'],0)
  self.assertEqual(A['new_empirically_validated_predictions'],0)
  self.assertEqual(A['previous_lilly'],4007)
  self.assertEqual(A['combined_if_published'],5118)
  self.assertFalse(A['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
