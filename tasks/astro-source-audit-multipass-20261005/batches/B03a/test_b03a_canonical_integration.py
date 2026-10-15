import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03a_CHAPTER_LV_COMPLETE.md'
I=J(IDX);A=J(B/'ACCEPTANCE.json');S=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Integration(unittest.TestCase):
 def test_source_predecessor(self):
  pre=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03a_CANONICAL.json'
  self.assertEqual(H(pre),S['old_index_sha256'])
  p=J(pre)
  self.assertEqual(p['records_count'],3171)
  self.assertEqual(p['batches'][-1]['id'],'B02z')
  self.assertEqual(p['next']['chapter'],'LV')
 def test_full_index_append(self):
  self.assertEqual(I['records_count'],3203)
  self.assertEqual(sum(b['records_count'] for b in I['batches']),3203)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,56)))
  self.assertEqual(I['batches'][-1]['id'],'B03a')
  self.assertEqual(I['batches'][-1]['records_count'],32)
  self.assertEqual(I['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual(I['next']['chapter'],'LVI')
  self.assertEqual(I['next']['pdf_page'],413)
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
 def test_state_and_source_receipts(self):
  self.assertEqual(H(IDX),S['new_index_sha256'])
  self.assertEqual(H(CUR),S['new_current_sha256'])
  self.assertEqual(H(LATEST),S['new_latest_sha256'])
  self.assertIn('3,203 Lilly + 1,066',LATEST.read_text())
  self.assertEqual(A['new_documentary_records'],32)
  self.assertFalse(A['canonical_published'])
 def test_zip_replay_not_empirical(self):
  x=J(B/'SOURCE_DOCUMENTARY_ACCEPTED_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(x['archive_os_downloads']),S['accepted_zip_sha256'])
  self.assertEqual(x['extracted_focused_test_count'],18)
  self.assertEqual(S['new_empirical_validations'],0)
  self.assertFalse(S['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
