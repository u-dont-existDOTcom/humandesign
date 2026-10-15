import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
S=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02z_CHAPTER_LIV_COMPLETE.md'
IDX=J(I);R=J(B/'RULES.json');A=J(B/'ACCEPTANCE.json')
REC=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class TestCanonical(unittest.TestCase):
 def test_source_identity_predecessor(self):
  pre=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02z_CANONICAL.json'
  self.assertEqual(sha(pre),REC['previous_index_sha256'])
  p=J(pre)
  self.assertEqual(p['records_count'],3147)
  self.assertEqual(p['batches'][-1]['id'],'B02y')
  self.assertEqual(p['next']['chapter'],'LIV')
 def test_complete_contiguous_append(self):
  self.assertEqual(IDX['records_count'],3171)
  self.assertEqual(sum(x['records_count'] for x in IDX['batches']),3171)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,55)))
  self.assertEqual(IDX['batches'][-1]['id'],'B02z')
  self.assertEqual(IDX['batches'][-1]['records_count'],24)
  self.assertEqual(IDX['batches'][-1]['sha256'],sha(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3148,3172)))
  self.assertEqual(IDX['next']['chapter'],'LV')
  self.assertEqual(IDX['next']['pdf_page'],411)
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
 def test_state_provenance(self):
  self.assertEqual(sha(I),REC['new_index_sha256'])
  self.assertEqual(sha(C),REC['new_current_state_sha256'])
  self.assertEqual(sha(S),REC['new_latest_state_sha256'])
  self.assertIn('3,171 Lilly + 1,066 retained Ptolemy',C.read_text()[:450])
 def test_archive_preserved(self):
  rr=J(B/'SOURCE_DOCUMENTARY_ACCEPTED_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(sha(rr['archive_os_downloads']),REC['accepted_owner_release_sha256'])
  self.assertEqual(rr['extracted_focused_test_count'],19)
  self.assertEqual(A['new_documentary_records'],24)
  self.assertEqual(A['source_uncertainties_retained'],14)
  self.assertFalse(A['canonical_published'])
  self.assertFalse(REC['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
