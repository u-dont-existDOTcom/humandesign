import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
L=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03o_CHAPTER_LXIX_COMPLETE.md'
idx=J(I);r=J(B/'RULES.json')
p=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integration(unittest.TestCase):
 def test_previous_index(self):
  f=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03o_CANONICAL.json'
  self.assertEqual(H(f),p['previous_index_sha256'])
  self.assertEqual(J(f)['records_count'],3976)
 def test_new_records(self):
  self.assertEqual(idx['records_count'],4007)
  self.assertEqual(sum(x['records_count'] for x in idx['batches']),4007)
  self.assertEqual(idx['batches'][-1]['id'],'B03o')
  self.assertEqual(idx['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([v['record_number'] for v in r['rules']],list(range(3977,4008)))
 def test_next_original(self):
  self.assertEqual(idx['read_numbered_chapters'],list(range(1,70)))
  self.assertEqual(idx['next']['chapter'],'LXX')
  self.assertEqual(idx['next']['pdf_page'],449)
  self.assertEqual(idx['empirical_validations'],0)
  self.assertEqual(idx['runtime_promotions'],0)
 def test_generated_hashes_and_archive(self):
  self.assertEqual(H(I),p['new_index_sha256'])
  self.assertEqual(H(C),p['new_current_sha256'])
  self.assertEqual(H(L),p['new_latest_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_local_path']),p['archive_sha256'])
  self.assertEqual(z['replayed_tests_passed'],17)
  self.assertFalse(p['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
