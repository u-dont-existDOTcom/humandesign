"""Canonical cumulative index and historical-source publication prerequisites."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03c_CHAPTER_LVII_COMPLETE.md'
A=J(B/'ACCEPTANCE.json')
R=J(B/'RULES.json')
Q=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
IDX=J(I)
class Integration(unittest.TestCase):
 def test_prior_accepted_state_unmodified(self):
  old=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03c_CANONICAL.json'
  self.assertEqual(H(old),Q['previous_index_sha256'])
  p=J(old)
  self.assertEqual(p['records_count'],3248)
  self.assertEqual(p['batches'][-1]['id'],'B03b')
 def test_stable_increment(self):
  self.assertEqual(IDX['records_count'],3322)
  self.assertEqual(sum(x['records_count'] for x in IDX['batches']),3322)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,58)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03c')
  self.assertEqual(IDX['batches'][-1]['records_count'],74)
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3249,3323)))
  self.assertEqual(IDX['next']['chapter'],'LVIII')
  self.assertEqual(IDX['next']['pdf_page'],417)
 def test_canonical_hash_bindings(self):
  self.assertEqual(H(I),Q['new_index_sha256'])
  self.assertEqual(H(CURRENT),Q['new_current_state_sha256'])
  self.assertEqual(H(LATEST),Q['new_latest_state_sha256'])
  self.assertEqual(A['source_reverse_spans'],26)
  self.assertEqual(A['retained_source_issues'],19)
 def test_no_claim_upgrade(self):
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(Q['new_empirical_predictions'],0)
  self.assertEqual(Q['new_runtime_rules'],0)
  self.assertFalse(Q['remote_published'])
 def test_archive_replay_identity(self):
  p=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(p['archive_on_laptop']),Q['owner_zip_sha256'])
  self.assertTrue(p['zip_crc_pass'])
  self.assertTrue(p['member_sha256_pass'])
  self.assertEqual(p['extracted_test_count'],17)
if __name__=='__main__':unittest.main(verbosity=2)
