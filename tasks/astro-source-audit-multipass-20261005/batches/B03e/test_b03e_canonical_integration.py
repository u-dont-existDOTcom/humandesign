"""Original 1647 LIX source-only canonical progression tests."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
S=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03e_CHAPTER_LIX_COMPLETE.md'
IDX=J(I);A=J(B/'ACCEPTANCE.json');Q=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Integration(unittest.TestCase):
 def test_previous_index_exact_bytes(self):
  p=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03e_CANONICAL.json'
  self.assertEqual(H(p),Q['prior_index_sha256'])
  prior=J(p)
  self.assertEqual(prior['records_count'],3360)
  self.assertEqual(prior['batches'][-1]['id'],'B03d')
  self.assertEqual(prior['next']['chapter'],'LIX')
 def test_numbered_sequence_source_only(self):
  self.assertEqual(IDX['records_count'],3418)
  self.assertEqual(sum(b['records_count'] for b in IDX['batches']),3418)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,60)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03e')
  self.assertEqual(IDX['batches'][-1]['records_count'],58)
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual(IDX['next']['chapter'],'LX')
  self.assertEqual(IDX['next']['pdf_page'],423)
 def test_outputs_and_preserved_witness(self):
  self.assertEqual(H(I),Q['new_index_sha256'])
  self.assertEqual(H(C),Q['new_current_sha256'])
  self.assertEqual(H(S),Q['new_latest_sha256'])
  self.assertEqual(A['source_reverse_passages'],25)
  self.assertEqual(A['retained_ambiguities'],18)
  self.assertEqual(A['distinct_next_case_date'],'11 June 1646 chart in PDF423')
 def test_replayed_release_and_no_case_overclaim(self):
  r=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(r['archive_on_laptop']),Q['zip_release_sha256'])
  self.assertTrue(r['zip_crc_pass'] and r['file_sha256_and_bytes_pass'])
  self.assertEqual(r['extracted_source_test_count'],13)
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(A['independently_confirmed_marriage_outcome'],0)
  self.assertFalse(Q['remote_publication_verified'])
if __name__=='__main__':unittest.main(verbosity=2)
