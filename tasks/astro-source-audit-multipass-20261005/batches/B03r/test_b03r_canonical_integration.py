import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
L=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03r_CHAPTER_LXXII_COMPLETE.md'
IDX=J(I);R=J(B/'RULES.json');P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integration(unittest.TestCase):
 def test_predecessor_unchanged(self):
  old=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03r_CANONICAL.json'
  self.assertEqual(H(old),P['old_index_sha256'])
  self.assertEqual(J(old)['records_count'],4093)
  self.assertEqual(J(old)['batches'][-1]['id'],'B03q')
 def test_global_source_index_consecutive(self):
  self.assertEqual(IDX['records_count'],4136)
  self.assertEqual(sum(b['records_count'] for b in IDX['batches']),4136)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,73)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03r')
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4094,4137)))
 def test_next_and_accuracy_separation(self):
  self.assertEqual(IDX['next']['chapter'],'LXXIII')
  self.assertEqual(IDX['next']['pdf_page'],455)
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(R['independent_historical_execution_event_confirmed'],1)
  self.assertEqual(R['independent_prospective_astro_forecasts_verified'],0)
 def test_exact_integration_and_archive_hashes(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(C),P['new_current_sha256'])
  self.assertEqual(H(L),P['new_latest_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['owner_archive_sha256'])
  self.assertEqual(z['extracted_replay_tests_passed'],12)
  self.assertFalse(P['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
