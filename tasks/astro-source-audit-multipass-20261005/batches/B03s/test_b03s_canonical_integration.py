import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03s_CHAPTER_LXXIII_COMPLETE.md'
INDEX=J(I);R=J(B/'RULES.json');A=J(B/'ACCEPTANCE.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Canonical(unittest.TestCase):
 def test_previous_baseline_unchanged(self):
  f=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03s_CANONICAL.json'
  self.assertEqual(H(f),P['prior_index_sha256'])
  v=J(f)
  self.assertEqual(v['records_count'],4136)
  self.assertEqual(v['batches'][-1]['id'],'B03r')
  self.assertEqual(v['next']['chapter'],'LXXIII')
 def test_exact_contiguous_accepted_index(self):
  self.assertEqual(INDEX['records_count'],4170)
  self.assertEqual(sum(b['records_count'] for b in INDEX['batches']),4170)
  self.assertEqual(INDEX['read_numbered_chapters'],list(range(1,74)))
  self.assertEqual(INDEX['batches'][-1]['id'],'B03s')
  self.assertEqual(INDEX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4137,4171)))
 def test_next_source_and_empirical_isolation(self):
  self.assertEqual(INDEX['next']['chapter'],'LXXIV')
  self.assertEqual(INDEX['next']['pdf_page'],456)
  self.assertEqual(INDEX['empirical_validations'],0)
  self.assertEqual(INDEX['runtime_promotions'],0)
  self.assertEqual(R['independently_verified_paid_portion_outcomes'],0)
 def test_generated_state_hashes(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(CUR),P['new_current_state_sha256'])
  self.assertEqual(H(LATEST),P['new_latest_state_sha256'])
  self.assertFalse(P['remotely_published'])
 def test_accepted_local_archive_replay_identity(self):
  Z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(Z['owner_download_path']),P['owner_release_zip_sha256'])
  self.assertTrue(Z['full_extraction_pass'])
  self.assertEqual(Z['extracted_tests_passed'],17)
  self.assertEqual(Z['extracted_exit_code'],0)
if __name__=='__main__':unittest.main(verbosity=2)
