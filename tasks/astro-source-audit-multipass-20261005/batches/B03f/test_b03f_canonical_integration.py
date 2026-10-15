import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03f_CHAPTER_LX_COMPLETE.md'
I=J(IDX);A=J(B/'ACCEPTANCE.json')
R=J(B/'RULES.json')
C=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Canonical(unittest.TestCase):
 def test_frozen_predecessor(self):
  pre=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03f_CANONICAL.json'
  self.assertEqual(H(pre),C['old_index_sha256'])
  p=J(pre)
  self.assertEqual(p['records_count'],3418)
  self.assertEqual(p['batches'][-1]['id'],'B03e')
  self.assertEqual(p['next']['chapter'],'LX')
 def test_source_edition_contiguous(self):
  self.assertEqual(I['records_count'],3449)
  self.assertEqual(sum(x['records_count'] for x in I['batches']),3449)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,61)))
  self.assertEqual(I['batches'][-1]['id'],'B03f')
  self.assertEqual(I['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3419,3450)))
 def test_next_chapter_and_false_case_separation(self):
  self.assertEqual(I['next']['chapter'],'LXI')
  self.assertEqual(I['next']['pdf_page'],424)
  self.assertEqual(I['next']['printed_page'],390)
  self.assertEqual(R['source_internal_reported_marriage_outcomes'],1)
  self.assertFalse(R['original_case_independently_authenticated'])
  self.assertFalse(R['accepted_as_empirical_prediction'] if 'accepted_as_empirical_prediction' in R else False)
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
 def test_exact_state_hash_receipt(self):
  self.assertEqual(H(IDX),C['new_index_sha256'])
  self.assertEqual(H(CUR),C['new_state_sha256'])
  self.assertEqual(H(LATEST),C['new_latest_source_state_sha256'])
  self.assertIn('11 June 1646',LATEST.read_text())
  self.assertIn('different',LATEST.read_text().lower())
 def test_archive_replay_still_exact(self):
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(z['owner_os_download_path']),C['release_zip_sha256'])
  self.assertEqual(z['extracted_source_tests_passed'],18)
  self.assertEqual(z['extracted_test_exit_code'],0)
  self.assertFalse(C['remotely_published'])
if __name__=='__main__':unittest.main(verbosity=2)
