import unittest,json,hashlib,copy
from pathlib import Path
B=Path(__file__).resolve().parent
J=lambda f:json.loads((B/f).read_text())
H=lambda f:hashlib.sha256((B/f).read_bytes()).hexdigest()
D=J('SOURCE_FIRST_CLAUSES_DRAFT.json')['rows']
R=J('RULES.json')['rules']
M=J('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json')
A=J('ACCEPTANCE.json')
class Admission(unittest.TestCase):
 def test_ids_and_chapters(self):
  self.assertEqual([r['record_number'] for r in R],list(range(4053,4094)))
  self.assertTrue(all(r['chapter']=='LXXI' for r in R[:-1]))
  self.assertEqual(R[-1]['chapter'],'LXXII_NAVIGATION_ONLY')
 def test_draft_same_content(self):
  for d,r in zip(D,R,strict=True):
   for k in ('source_local_id','original_pdf_pages','role',
    'historical_author_report_paraphrase','conditions_original_uncertainty'):
    self.assertEqual(d[k],r[k])
   self.assertIsNone(d['global_record_number'])
 def test_full_reverse_mapping(self):
  ids=[k for s in M['source_spans'] for k in s['canonical_record_ids']]
  self.assertEqual(len(ids),41)
  self.assertEqual(sorted(ids),sorted(r['id'] for r in R))
 def test_acceptance_hashes(self):
  for f,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','order_sha256'),
   ('UNRESOLVED.json','uncertainties_sha256'),
   ('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','reverse_map_sha256'),
   ('SOURCE_FIRST_IMAGE_AUDIT_20261016.md','visual_audit_sha256')]:
   self.assertEqual(H(f),A[k])
 def test_three_outcomes_unverified(self):
  self.assertEqual(A['author_reported_first_false_rumor'],1)
  self.assertEqual(A['author_reported_may_news'],1)
  self.assertEqual(A['author_reported_july_return'],1)
  self.assertEqual(A['independent_verified_outcomes'],0)
  self.assertEqual(A['empirically_validated_predictions'],0)
 def test_source_baseline(self):
  self.assertEqual(A['prior_lilly'],4052)
  self.assertEqual(A['new_documentary_records'],41)
  self.assertEqual(A['lilly_if_published'],4093)
  self.assertEqual(A['combined_if_published'],5159)
  self.assertFalse(A['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
