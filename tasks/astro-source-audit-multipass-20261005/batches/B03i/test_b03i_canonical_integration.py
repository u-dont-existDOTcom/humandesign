import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda f:json.loads(Path(f).read_text())
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
C=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03i_CHAPTER_LXIII_COMPLETE.md'
j=J(I);p=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json')
class Integration(unittest.TestCase):
 def test_frozen_previous_index(self):
  original=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03i_CANONICAL.json'
  self.assertEqual(H(original),p['old_index_sha256'])
  x=J(original)
  self.assertEqual(x['records_count'],3527)
  self.assertEqual(x['next']['chapter'],'LXIII')
 def test_contiguous_append(self):
  self.assertEqual(j['records_count'],3571)
  self.assertEqual(sum(x['records_count'] for x in j['batches']),3571)
  self.assertEqual(j['read_numbered_chapters'],list(range(1,64)))
  self.assertEqual(j['batches'][-1]['id'],'B03i')
  self.assertEqual(j['batches'][-1]['sha256'],H(B/'RULES.json'))
 def test_original_printing_exception(self):
  self.assertEqual(j['next']['chapter'],'LXIV')
  self.assertEqual(j['next']['printed_chapter_numeral'],'LIV')
  self.assertEqual(j['next']['pdf_page'],431)
  self.assertEqual(j['next']['heading'],'Fish Stolen.')
 def test_exact_state_hashes(self):
  self.assertEqual(H(I),p['new_index_sha256'])
  self.assertEqual(H(C),p['new_current_sha256'])
  self.assertEqual(H(LATEST),p['new_latest_sha256'])
  self.assertEqual(j['empirical_validations'],0)
  self.assertEqual(j['runtime_promotions'],0)
 def test_source_zip_replay(self):
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
  self.assertEqual(H(z['download_path']),p['release_zip_sha256'])
  self.assertEqual(z['extracted_focused_tests_passed'],19)
  self.assertEqual(z['extracted_test_exit_code'],0)
  self.assertFalse(p['remote_published'])
if __name__=='__main__':unittest.main(verbosity=2)
