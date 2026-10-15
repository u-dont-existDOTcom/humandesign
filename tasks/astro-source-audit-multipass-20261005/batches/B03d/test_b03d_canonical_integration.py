"""Chapter LVIII accepted source index succession and release evidence."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
S=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03d_CHAPTER_LVIII_COMPLETE.md'
A=J(B/'ACCEPTANCE.json')
R=J(B/'RULES.json')
Q=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
IDX=J(I)
class IndexAdmission(unittest.TestCase):
 def test_previous_index_frozen(self):
  old=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03d_CANONICAL.json'
  self.assertEqual(H(old),Q['prior_index_sha256'])
  j=J(old)
  self.assertEqual(j['records_count'],3322)
  self.assertEqual(j['batches'][-1]['id'],'B03c')
  self.assertEqual(j['next']['chapter'],'LVIII')
 def test_records_source_order(self):
  self.assertEqual(IDX['records_count'],3360)
  self.assertEqual(sum(x['records_count'] for x in IDX['batches']),3360)
  self.assertEqual(IDX['read_numbered_chapters'],list(range(1,59)))
  self.assertEqual(IDX['batches'][-1]['id'],'B03d')
  self.assertEqual(IDX['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual(IDX['batches'][-1]['records_count'],38)
  self.assertEqual(IDX['next']['chapter'],'LIX')
  self.assertEqual(IDX['next']['pdf_page'],419)
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(3323,3361)))
 def test_exact_state_and_archive_hashes(self):
  self.assertEqual(H(I),Q['new_index_sha256'])
  self.assertEqual(H(C),Q['new_current_sha256'])
  self.assertEqual(H(S),Q['new_latest_sha256'])
  self.assertEqual(A['new_historical_documentary_units'],38)
  rec=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(rec['archive_on_laptop']),Q['owner_zip_sha256'])
  self.assertEqual(rec['extracted_test_count'],15)
 def test_empirical_fences(self):
  self.assertEqual(IDX['empirical_validations'],0)
  self.assertEqual(IDX['runtime_promotions'],0)
  self.assertEqual(Q['new_empirical_validations'],0)
  self.assertEqual(Q['new_runtime_models'],0)
  self.assertFalse(Q['remote_published'])
  self.assertFalse(A['canonical_publication_verified'])
if __name__=='__main__':unittest.main(verbosity=2)
