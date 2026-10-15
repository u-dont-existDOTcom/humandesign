import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads(Path(f).read_text(encoding='utf-8'))
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03g_CHAPTER_LXI_COMPLETE.md'
I=J(IDX);A=J(B/'ACCEPTANCE.json')
R=J(B/'RULES.json');P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Integration(unittest.TestCase):
 def test_unmodified_previous_source_snapshot(self):
  f=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03g_CANONICAL.json'
  self.assertEqual(sha(f),P['old_index_sha256'])
  x=J(f)
  self.assertEqual(x['records_count'],3449)
  self.assertEqual(x['batches'][-1]['id'],'B03f')
  self.assertEqual(x['next']['chapter'],'LXI')
  self.assertEqual(x['source_sha256'],I['source_sha256'])
 def test_contiguous_index_append(self):
  self.assertEqual(I['records_count'],3484)
  self.assertEqual(sum(b['records_count'] for b in I['batches']),3484)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,62)))
  self.assertEqual(I['batches'][-1]['id'],'B03g')
  self.assertEqual(I['batches'][-1]['records_count'],35)
  self.assertEqual(I['batches'][-1]['sha256'],sha(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3450,3485)))
 def test_new_original_boundary(self):
  self.assertEqual(I['next']['chapter'],'LXII')
  self.assertEqual(I['next']['pdf_page'],426)
  self.assertEqual(I['next']['printed_page'],392)
  self.assertEqual(R['rules'][-1]['chapter'],'LXII_NAVIGATION_ONLY')
 def test_zero_external_validation(self):
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
  self.assertEqual(R['independently_authenticated_servant_outcomes'],0)
  self.assertEqual(R['empirically_validated_predictive_cases'],0)
  self.assertFalse(A['original_case_independently_authenticated'])
 def test_exact_hashes_and_release(self):
  self.assertEqual(sha(IDX),P['new_index_sha256'])
  self.assertEqual(sha(CUR),P['new_current_state_sha256'])
  self.assertEqual(sha(LATEST),P['new_latest_source_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(sha(z['owner_designated_download_path']),P['owner_release_zip_sha256'])
  self.assertEqual(z['extracted_source_tests_passed'],21)
  self.assertEqual(z['extracted_test_exit_code'],0)
  self.assertFalse(P['remotely_published'])
if __name__=='__main__':unittest.main(verbosity=2)
