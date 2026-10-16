import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03t_CHAPTER_LXXIV_COMPLETE.md'
INDEX=J(IDX); R=J(B/'RULES.json'); A=J(B/'ACCEPTANCE.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integration(unittest.TestCase):
 def test_exact_predecessor_preservation(self):
  f=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03t_CANONICAL.json'
  self.assertEqual(H(f),P['prior_index_sha256'])
  old=J(f)
  self.assertEqual(old['records_count'],4170)
  self.assertEqual(old['batches'][-1]['id'],'B03s')
  self.assertEqual(old['next']['chapter'],'LXXIV')
 def test_full_documentary_index_contiguous(self):
  self.assertEqual(INDEX['records_count'],4323)
  self.assertEqual(sum(b['records_count'] for b in INDEX['batches']),4323)
  self.assertEqual(INDEX['read_numbered_chapters'],list(range(1,75)))
  self.assertEqual(INDEX['batches'][-1]['id'],'B03t')
  self.assertEqual(INDEX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4171,4324)))
 def test_next_source_boundary(self):
  self.assertEqual(INDEX['next']['chapter'],'LXXV')
  self.assertEqual(INDEX['next']['pdf_page'],463)
  self.assertEqual(INDEX['next']['printed_page'],429)
  self.assertTrue(all(r['chapter']=='LXXV_NAVIGATION_ONLY' for r in R['rules'][-2:]))
 def test_empirical_separation(self):
  self.assertEqual(INDEX['empirical_validations'],0)
  self.assertEqual(INDEX['runtime_promotions'],0)
  self.assertEqual(R['independently_verified_journey_cases'],0)
  self.assertEqual(R['new_empirically_validated_astrological_predictions'],0)
 def test_exact_hashes_and_extracted_archive(self):
  self.assertEqual(H(IDX),P['new_index_sha256'])
  self.assertEqual(H(CUR),P['current_state_sha256'])
  self.assertEqual(H(LATEST),P['latest_source_state_sha256'])
  Z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(Z['owner_download_path']),P['accepted_owner_zip_sha256'])
  self.assertEqual(Z['extracted_tests_passed'],19)
  self.assertEqual(Z['extracted_test_exit_code'],0)
  self.assertFalse(P['remotely_published'])
if __name__=='__main__':unittest.main(verbosity=2)
