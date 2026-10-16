import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
L=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03p_CHAPTER_LXX_COMPLETE.md'
idx=J(I);R=J(B/'RULES.json');P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Integrated(unittest.TestCase):
 def test_predecessor_integrity(self):
  old=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03p_CANONICAL.json'
  self.assertEqual(H(old),P['old_index_sha256'])
  self.assertEqual(J(old)['records_count'],4007)
  self.assertEqual(J(old)['batches'][-1]['id'],'B03o')
 def test_record_integrity(self):
  self.assertEqual(idx['records_count'],4052)
  self.assertEqual(sum(x['records_count'] for x in idx['batches']),4052)
  self.assertEqual(idx['read_numbered_chapters'],list(range(1,71)))
  self.assertEqual(idx['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4008,4053)))
 def test_next_source_and_predictions(self):
  self.assertEqual(idx['next']['chapter'],'LXXI')
  self.assertEqual(idx['next']['pdf_page'],451)
  self.assertEqual(idx['empirical_validations'],0)
  self.assertEqual(idx['runtime_promotions'],0)
  self.assertEqual(R['independently_validated_historical_cases'],0)
 def test_hash_and_replay(self):
  self.assertEqual(H(I),P['new_index_sha256'])
  self.assertEqual(H(C),P['current_state_sha256'])
  self.assertEqual(H(L),P['latest_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['local_owner_zip_path']),P['archive_sha256'])
  self.assertEqual(z['replayed_tests'],12)
if __name__=='__main__':unittest.main(verbosity=2)
