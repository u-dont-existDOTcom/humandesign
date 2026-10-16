import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda x:json.loads(Path(x).read_text())
H=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
L=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03n_CHAPTER_LXVIII_COMPLETE.md'
IDX=J(I);R=J(B/'RULES.json');A=J(B/'ACCEPTANCE.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integration(unittest.TestCase):
 def test_unchanged_predecessor(self):
  f=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03n_CANONICAL.json'
  self.assertEqual(H(f),P['old_index_sha256'])
  old=J(f)
  self.assertEqual(old['records_count'],3932)
  self.assertEqual(old['batches'][-1]['id'],'B03m')
  self.assertEqual(old['next']['chapter'],'LXVIII')
 def test_contiguous_source_append(self):
  self.assertEqual(IDX['records_count'],3976)
  self.assertEqual(sum(x['records_count'] for x in IDX['batches']),3976)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,69)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03n')
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3933,3977)))
 def test_next_source_no_empirical(self):
  self.assertEqual(IDX['next']['chapter'],'LXIX')
  self.assertEqual(IDX['next']['pdf_page'],448)
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(R['independent_dowry_receipts_verified'],0)
 def test_state_hashes_and_replay(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(C),P['new_current_state_sha256'])
  self.assertEqual(H(L),P['new_latest_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['accepted_owner_archive_sha256'])
  self.assertEqual(z['replay_tests_passed'],16)
  self.assertEqual(z['replay_test_exit_code'],0)
  self.assertFalse(P['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
