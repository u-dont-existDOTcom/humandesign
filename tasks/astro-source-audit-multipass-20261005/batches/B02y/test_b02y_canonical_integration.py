"""B02y documentary acceptance integrated into guarded in-repo canonical index."""
import hashlib
import json
import unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
S=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02y_CHAPTER_LIII_COMPLETE.md'
A=j(B/'ACCEPTANCE.json')
W=j(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
IDX=j(I)
R=j(B/'RULES.json')
class TestCanonicalIndex(unittest.TestCase):
 def test_immutable_parent_identity(self):
  self.assertEqual(H(B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02y_CANONICAL.json'),W['previous_index_sha256'])
  pre=j(B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02y_CANONICAL.json')
  self.assertEqual(pre['records_count'],3071)
  self.assertEqual(pre['batches'][-1]['id'],'B02x')
  self.assertEqual(pre['next']['chapter'],'LIII')
  self.assertEqual(pre['source_sha256'],IDX['source_sha256'])
 def test_full_index_chain(self):
  self.assertEqual(IDX['records_count'],3147)
  self.assertEqual(sum(b['records_count'] for b in IDX['batches']),3147)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,54)))
  self.assertEqual(IDX['batches'][-1]['id'],'B02y')
  self.assertEqual(IDX['batches'][-1]['path'],'batches/B02y/RULES.json')
  self.assertEqual(IDX['batches'][-1]['records_count'],76)
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual(IDX['next']['chapter'],'LIV')
  self.assertEqual(IDX['next']['pdf_page'],410)
  self.assertEqual(IDX['next']['printed_page'],376)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(IDX['empirical_validations'],0)
 def test_current_and_latest_history(self):
  self.assertEqual(H(I),W['new_index_sha256'])
  self.assertEqual(H(S),W['new_current_state_sha256'])
  self.assertEqual(H(LATEST),W['new_latest_state_sha256'])
  self.assertTrue(S.read_text().startswith('# Current astrology source audit — latest historical corpus checkpoint'))
  self.assertIn('3,147 Lilly + 1,066 retained Ptolemy',LATEST.read_text())
  self.assertIn('76 (R3072–R3147)',LATEST.read_text())
 def test_local_release_remote_not_yet(self):
  self.assertEqual(W['rules_sha256'],A['rules_sha256'])
  self.assertEqual(W['owner_release_sha256'],H(j(B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json')['archive_os_downloads']))
  self.assertFalse(W['remote_published'])
  self.assertEqual(R['record_count'],76)
  self.assertFalse(R['accepted_as_empirical_astro_prediction'])
  self.assertEqual(W['empirical_predictions_validated'],0)
if __name__=='__main__':unittest.main(verbosity=2)
