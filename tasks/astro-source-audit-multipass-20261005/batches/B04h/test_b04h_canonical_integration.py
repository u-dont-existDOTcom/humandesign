import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
I=J(IDX);P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json');R=J(B/'RULES.json')
class Index(unittest.TestCase):
 def test_prior_index_identity(self):
  old=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04h_CANONICAL.json'
  self.assertEqual(H(old),P['previous_index_sha256'])
  j=J(old);self.assertEqual(j['records_count'],5113)
  self.assertEqual(j['batches'][-1]['id'],'B04g')
  self.assertEqual(j['batches'],I['batches'][:-1])
 def test_record_counts_and_source_alias(self):
  self.assertEqual(I['records_count'],5161)
  self.assertEqual(sum(x['records_count'] for x in I['batches']),5161)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,89)))
  self.assertEqual(I['batches'][-1]['id'],'B04h')
  self.assertEqual(I['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(5114,5162)))
 def test_literal_next_chapter_retained(self):
  self.assertEqual(I['next']['chapter'],'LXXXIX')
  self.assertEqual(I['next']['printed_chapter_numeral'],'LXXXVIII')
  self.assertEqual(I['next']['pdf_page'],493)
  self.assertEqual(I['original_printed_chapter_heading_crosswalk']['duplicate_printed_numeral'],'LXXXV')
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
 def test_hashes_of_archive_index_report(self):
  self.assertEqual(H(IDX),P['new_index_sha256'])
  self.assertEqual(H(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'),P['current_state_sha256'])
  self.assertEqual(H(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04h_CHAPTER_LXXXVIII_COMPLETE.md'),P['latest_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['owner_archive_sha256'])
  self.assertEqual(z['extracted_tests_passed'],15)
if __name__=='__main__':unittest.main(verbosity=2)
