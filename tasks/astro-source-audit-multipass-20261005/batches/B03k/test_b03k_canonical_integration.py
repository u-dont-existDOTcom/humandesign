import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03k_CHAPTER_LXV_COMPLETE.md'
I=J(IDX);R=J(B/'RULES.json');A=J(B/'ACCEPTANCE.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Integration(unittest.TestCase):
 def test_exact_predecessor_unchanged(self):
  before=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03k_CANONICAL.json'
  self.assertEqual(H(before),P['old_index_sha256'])
  x=J(before)
  self.assertEqual(x['records_count'],3630)
  self.assertEqual(x['batches'][-1]['id'],'B03j')
  self.assertEqual(x['next']['chapter'],'LXV')
 def test_contiguous_canonical_append(self):
  self.assertEqual(I['records_count'],3670)
  self.assertEqual(sum(x['records_count'] for x in I['batches']),3670)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,66)))
  self.assertEqual(I['batches'][-1]['id'],'B03k')
  self.assertEqual(I['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3631,3671)))
 def test_following_source_and_date(self):
  self.assertEqual(I['next']['chapter'],'LXVI')
  self.assertEqual(I['next']['pdf_page'],435)
  self.assertEqual(I['next']['printed_page'],401)
  self.assertEqual(A['original_chart_date'],'29 March 1644')
  self.assertEqual(A['original_chart_time'],'10:12 AM')
 def test_exact_generated_state_receipts(self):
  self.assertEqual(H(IDX),P['new_index_sha256'])
  self.assertEqual(H(CUR),P['new_current_sha256'])
  self.assertEqual(H(LATEST),P['new_latest_sha256'])
  self.assertIn('3,670',LATEST.read_text())
  self.assertIn('4,736',LATEST.read_text())
 def test_original_release_replay(self):
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(z['download_path']),P['release_archive_sha256'])
  self.assertEqual(z['extracted_test_count'],19)
  self.assertEqual(z['extracted_test_exit_code'],0)
  self.assertFalse(P['remote_published'])
 def test_zero_predictive_validation(self):
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
  self.assertEqual(A['independent_letter_arrival_time_evidence'],0)
  self.assertFalse(A['eleven_to_twelve_hour_claim_empirically_verified'])
if __name__=='__main__':unittest.main(verbosity=2)
