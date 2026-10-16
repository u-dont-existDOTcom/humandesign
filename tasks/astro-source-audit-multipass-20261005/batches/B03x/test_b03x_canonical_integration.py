import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03x_CHAPTER_LXXVIII_COMPLETE.md'
IDX=J(I);R=J(B/'RULES.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integration(unittest.TestCase):
 def test_exact_previous_index_preserved(self):
  old=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03x_CANONICAL.json'
  self.assertEqual(H(old),P['previous_index_sha256'])
  before=J(old)
  self.assertEqual(before['records_count'],4484)
  self.assertEqual(before['batches'][-1]['id'],'B03w')
  self.assertEqual(before['batches'],IDX['batches'][:-1])
 def test_canonical_counts_ordinals_and_hashes(self):
  self.assertEqual(IDX['records_count'],4508)
  self.assertEqual(sum(k['records_count'] for k in IDX['batches']),4508)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,79)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03x')
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4485,4509)))
 def test_next_chapter_and_verification_separation(self):
  self.assertEqual(IDX['next']['chapter'],'LXXIX')
  self.assertEqual(IDX['next']['pdf_page'],471)
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(R['authorial_unverified_success_reports'],1)
  self.assertEqual(R['independently_verified_dream_outcomes'],0)
 def test_source_state_and_archive_receipt(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(CUR),P['current_state_sha256'])
  self.assertEqual(H(LATEST),P['latest_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['owner_archive_sha256'])
  self.assertEqual(z['extracted_tests_passed'],14)
  self.assertFalse(P['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
