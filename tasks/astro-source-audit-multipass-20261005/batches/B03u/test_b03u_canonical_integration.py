import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03u_CHAPTER_LXXV_COMPLETE.md'
I=J(IDX);R=J(B/'RULES.json');A=J(B/'ACCEPTANCE.json')
P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
class Canonical(unittest.TestCase):
 def test_exact_previous_source_preserved(self):
  prev=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03u_CANONICAL.json'
  self.assertEqual(H(prev),P['previous_index_sha256'])
  j=J(prev)
  self.assertEqual(j['records_count'],4323)
  self.assertEqual(j['batches'][-1]['id'],'B03t')
  self.assertEqual(j['next']['chapter'],'LXXV')
  self.assertEqual(j['batches'],I['batches'][:-1])
 def test_canonical_append_and_count(self):
  self.assertEqual(I['records_count'],4384)
  self.assertEqual(sum(b['records_count'] for b in I['batches']),4384)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,76)))
  self.assertEqual(I['batches'][-1]['id'],'B03u')
  self.assertEqual(I['batches'][-1]['records_count'],61)
  self.assertEqual(I['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(4324,4385)))
 def test_physical_scan_order_preserves_wrong_folio_numbers(self):
  self.assertEqual(A['original_pdf_text_order'],[463,464,465,466])
  self.assertEqual(A['original_imprinted_folio_numbers'],[429,431,430,432])
  self.assertEqual(P['original_scan_order'],[463,464,465,466])
  self.assertEqual(P['literal_printed_folio_numbers'],[429,431,430,432])
  self.assertTrue(A['source_folio_pagination_numbers_transposed'])
  self.assertEqual(I['next']['chapter'],'LXXVI')
  self.assertEqual(I['next']['pdf_page'],466)
 def test_empirical_model_separation(self):
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
  self.assertEqual(R['independently_verified_skill_cases'],0)
  self.assertEqual(R['independently_verified_absent_travellers'],0)
  self.assertEqual(R['new_empirically_validated_predictions'],0)
 def test_frozen_hashes_and_release_replay(self):
  self.assertEqual(H(IDX),P['new_index_sha256'])
  self.assertEqual(H(CURRENT),P['new_current_state_sha256'])
  self.assertEqual(H(LATEST),P['new_latest_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['owner_release_archive_sha256'])
  self.assertTrue(z['actual_extraction_pass'])
  self.assertEqual(z['extracted_source_tests_passed'],20)
  self.assertEqual(z['extracted_test_exit_code'],0)
  self.assertFalse(P['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
