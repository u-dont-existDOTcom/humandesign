"""Documentary chapter append verification against immutable accepted prior chapter."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
S=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03b_CHAPTER_LVI_COMPLETE.md'
IDX=J(I)
A=J(B/'ACCEPTANCE.json')
REC=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
R=J(B/'RULES.json')
class Integration(unittest.TestCase):
 def test_prior_accepted_index_is_immutable(self):
  before=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03b_CANONICAL.json'
  self.assertEqual(H(before),REC['previous_index_sha256'])
  old=J(before)
  self.assertEqual(old['records_count'],3203)
  self.assertEqual(old['batches'][-1]['id'],'B03a')
  self.assertEqual(old['next']['chapter'],'LVI')
 def test_atomic_source_order_no_duplicate_units(self):
  self.assertEqual(IDX['records_count'],3248)
  self.assertEqual(sum(p['records_count'] for p in IDX['batches']),3248)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,57)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03b')
  self.assertEqual(IDX['batches'][-1]['records_count'],45)
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3204,3249)))
  self.assertEqual(IDX['next']['chapter'],'LVII')
  self.assertEqual(IDX['next']['pdf_page'],414)
 def test_record_count_index_state_has_provenance(self):
  self.assertEqual(H(I),REC['new_index_sha256'])
  self.assertEqual(H(S),REC['new_current_state_sha256'])
  self.assertEqual(H(LATEST),REC['new_latest_state_sha256'])
  self.assertIn('Lilly 3,248 + Ptolemy retained 1,066',LATEST.read_text())
  self.assertEqual(A['previous_lilly_accepted'],3203)
  self.assertEqual(A['added_historical_units'],45)
  self.assertEqual(A['combined_if_published'],4314)
 def test_no_empirical_or_runtime_substitution(self):
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(REC['new_empirical_predictions_validated'],0)
  self.assertEqual(REC['runtime_predicate_promotions'],0)
  self.assertFalse(REC['remote_published'])
  self.assertFalse(A['canonical_source_published'])
 def test_archive_and_extraction_verified(self):
  r=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(Path(r['archive_on_laptop'])),REC['owner_zip_sha256'])
  self.assertTrue(r['zip_crc_pass'])
  self.assertTrue(r['member_sha256_pass'])
  self.assertTrue(r['actual_extraction_pass'])
  self.assertEqual(r['extracted_test_count'],17)
if __name__=='__main__':unittest.main(verbosity=2)
