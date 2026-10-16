import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
IDX=J(I);P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Index(unittest.TestCase):
 def test_before_after(self):
  old=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04f_CANONICAL.json'
  self.assertEqual(H(old),P['previous_index_sha256'])
  prior=J(old);self.assertEqual(prior['records_count'],5026)
  self.assertEqual(prior['batches'],IDX['batches'][:-1])
 def test_counts(self):
  self.assertEqual(IDX['records_count'],5080)
  self.assertEqual(sum(b['records_count'] for b in IDX['batches']),5080)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,87)))
  self.assertEqual(IDX['batches'][-1]['id'],'B04f')
  self.assertEqual([r['record_number'] for r in J(B/'RULES.json')['rules']],list(range(5027,5081)))
 def test_next_and_validation(self):
  self.assertEqual(IDX['next']['chapter'],'LXXXVII')
  self.assertEqual(IDX['next']['pdf_page'],490)
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
 def test_exact_receipt_hashes(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'),P['current_state_sha256'])
  self.assertEqual(H(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04f_CHAPTER_LXXXVI_COMPLETE.md'),P['latest_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['owner_archive_sha256'])
if __name__=='__main__':unittest.main(verbosity=2)
