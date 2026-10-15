import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03j_FISH_STOLEN_COMPLETE.md'
I=J(IDX)
A=J(B/'ACCEPTANCE.json')
R=J(B/'RULES.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Canonical(unittest.TestCase):
 def test_exact_unmodified_predecessor(self):
  prev=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03j_CANONICAL.json'
  self.assertEqual(H(prev),P['original_parent_index_sha256'])
  x=J(prev)
  self.assertEqual(x['records_count'],3571)
  self.assertEqual(x['batches'][-1]['id'],'B03i')
  self.assertEqual(x['next']['printed_chapter_numeral'],'LIV')
  self.assertEqual(x['next']['chapter'],'LXIV')
 def test_contiguous_complete_source_index(self):
  self.assertEqual(I['records_count'],3630)
  self.assertEqual(sum(x['records_count'] for x in I['batches']),3630)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,65)))
  self.assertEqual(I['batches'][-1]['id'],'B03j')
  self.assertEqual(I['batches'][-1]['records_count'],59)
  self.assertEqual(I['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3572,3631)))
 def test_two_distinct_LIV_printed_cases(self):
  ids=[x['id'] for x in I['batches']]
  self.assertEqual(ids.count('B02z'),1)
  self.assertEqual(ids.count('B03j'),1)
  self.assertEqual(A['original_printed_heading'],'LIV')
  self.assertEqual(A['logical_number'],'LXIV')
 def test_next_original_source_heading(self):
  self.assertEqual(I['next']['chapter'],'LXV')
  self.assertEqual(I['next']['pdf_page'],433)
  self.assertEqual(I['next']['printed_page'],399)
  self.assertEqual(I['next']['printed_chapter_numeral'],'LXV')
 def test_state_hash_receipts(self):
  self.assertEqual(H(IDX),P['new_source_index_sha256'])
  self.assertEqual(H(CUR),P['new_current_state_sha256'])
  self.assertEqual(H(LATEST),P['new_latest_state_sha256'])
  self.assertIn('3,630',LATEST.read_text())
  self.assertIn('4,696',LATEST.read_text())
 def test_release_archive_identity(self):
  Z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(Z['owner_os_download_path']),P['owner_release_zip_sha256'])
  self.assertEqual(Z['extracted_focused_tests_passed'],21)
  self.assertEqual(Z['extracted_test_exit_code'],0)
  self.assertTrue(Z['actual_extraction_pass'])
 def test_source_outcomes_not_empirically_published(self):
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
  self.assertEqual(R['author_reported_partially_recovered_fish_cases'] if 'author_reported_partially_recovered_fish_cases' in R else R['author_reported_partial_fish_recovery_cases'],1)
  self.assertEqual(R['author_reported_full_fish_recovery_cases'],0)
  self.assertFalse(P['remotely_published'])
if __name__=='__main__':unittest.main(verbosity=2)
