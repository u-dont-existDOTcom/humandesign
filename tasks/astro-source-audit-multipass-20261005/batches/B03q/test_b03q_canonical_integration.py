import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
L=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03q_CHAPTER_LXXI_COMPLETE.md'
D=J(I);R=J(B/'RULES.json');P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integration(unittest.TestCase):
 def test_predecessor_preservation(self):
  f=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03q_CANONICAL.json'
  self.assertEqual(H(f),P['old_index_sha256'])
  old=J(f)
  self.assertEqual(old['records_count'],4052)
  self.assertEqual(old['batches'][-1]['id'],'B03p')
 def test_new_consecutive_index(self):
  self.assertEqual(D['records_count'],4093)
  self.assertEqual(sum(b['records_count'] for b in D['batches']),4093)
  self.assertEqual(D['read_numbered_chapters'],list(range(1,72)))
  self.assertEqual(D['batches'][-1]['id'],'B03q')
  self.assertEqual(D['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4053,4094)))
 def test_next_chapter_and_case_status(self):
  self.assertEqual(D['next']['chapter'],'LXXII')
  self.assertEqual(D['next']['pdf_page'],453)
  self.assertEqual(D['empirical_validations'],0)
  self.assertEqual(D['runtime_promotions'],0)
  self.assertEqual(R['independently_verified_outcomes'],0)
 def test_exact_hash_replay(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(C),P['new_current_sha256'])
  self.assertEqual(H(L),P['new_latest_sha256'])
  Z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(Z['local_owner_path']),P['accepted_zip_sha256'])
  self.assertEqual(Z['tests_replayed'],10)
  self.assertEqual(Z['test_exit_code'],0)
  self.assertFalse(P['remote_published'])
if __name__=='__main__': unittest.main(verbosity=2)
