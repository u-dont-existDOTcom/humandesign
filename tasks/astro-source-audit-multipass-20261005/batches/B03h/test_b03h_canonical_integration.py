import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
L=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03h_CHAPTER_LXII_COMPLETE.md'
j=J(I);p=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Integration(unittest.TestCase):
 def test_frozen_previous_source(self):
  before=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03h_CANONICAL.json'
  self.assertEqual(H(before),p['old_index_sha256'])
  b=J(before)
  self.assertEqual(b['records_count'],3484)
  self.assertEqual(b['batches'][-1]['id'],'B03g')
  self.assertEqual(b['next']['chapter'],'LXII')
 def test_new_contiguous_source(self):
  self.assertEqual(j['records_count'],3527)
  self.assertEqual(sum(x['records_count'] for x in j['batches']),3527)
  self.assertEqual(j['read_numbered_chapters'],list(range(1,63)))
  self.assertEqual(j['batches'][-1]['id'],'B03h')
  self.assertEqual(j['batches'][-1]['records_count'],43)
  self.assertEqual(j['batches'][-1]['sha256'],H(B/'RULES.json'))
 def test_next_source_physical_boundary(self):
  self.assertEqual(j['next']['chapter'],'LXIII')
  self.assertEqual(j['next']['pdf_page'],428)
  self.assertEqual(j['next']['printed_page'],394)
 def test_source_and_state_hashes(self):
  self.assertEqual(H(I),p['new_index_sha256'])
  self.assertEqual(H(C),p['new_current_sha256'])
  self.assertEqual(H(L),p['new_latest_sha256'])
  self.assertEqual(j['empirical_validations'],0)
  self.assertEqual(j['runtime_promotions'],0)
 def test_extracted_archive_and_count(self):
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(z['download_path']),p['source_zip_sha256'])
  self.assertEqual(z['extracted_test_count'],17)
  self.assertEqual(z['extracted_test_exit_code'],0)
  self.assertFalse(p['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
