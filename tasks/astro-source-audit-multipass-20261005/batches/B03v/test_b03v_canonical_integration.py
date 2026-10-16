import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03v_CHAPTER_LXXVI_COMPLETE.md'
IDX=J(I);R=J(B/'RULES.json');A=J(B/'ACCEPTANCE.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integration(unittest.TestCase):
 def test_exact_original_predecessor(self):
  f=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03v_CANONICAL.json'
  self.assertEqual(H(f),P['prior_index_sha256'])
  old=J(f)
  self.assertEqual(old['records_count'],4384)
  self.assertEqual(old['batches'][-1]['id'],'B03u')
  self.assertEqual(old['next']['chapter'],'LXXVI')
  self.assertEqual(old['batches'],IDX['batches'][:-1])
 def test_full_index_contiguity(self):
  self.assertEqual(IDX['records_count'],4446)
  self.assertEqual(sum(v['records_count'] for v in IDX['batches']),4446)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,77)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03v')
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4385,4447)))
 def test_next_original_source_and_no_empirical_claim(self):
  self.assertEqual(IDX['next']['chapter'],'LXXVII')
  self.assertEqual(IDX['next']['pdf_page'],468)
  self.assertEqual(IDX['next']['printed_page'],434)
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(R['independently_verified_clerical_appointments'],0)
 def test_state_sha_and_archive_identity(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(CUR),P['current_state_sha256'])
  self.assertEqual(H(LATEST),P['latest_source_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['owner_zip_sha256'])
  self.assertEqual(z['replayed_tests_passed'],18)
  self.assertEqual(z['test_exit_code'],0)
  self.assertFalse(P['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
