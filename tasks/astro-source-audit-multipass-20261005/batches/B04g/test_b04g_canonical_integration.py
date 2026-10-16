import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
I=J(IDX);P=J(B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json')
R=J(B/'RULES.json')
class Index(unittest.TestCase):
 def test_previous_index_and_accepted_lineage(self):
  old=B/'recovery/LILLY_INDEX_AFTER_CROSSWALK_BEFORE_B04g_CANONICAL.json'
  self.assertEqual(H(old),P['previous_index_sha256'])
  previous=J(old);self.assertEqual(previous['records_count'],5080)
  self.assertEqual(previous['batches'],I['batches'][:-1])
  self.assertEqual(previous['next']['printed_chapter_numeral'],'LXXXVI')
 def test_cumulative_record_numbers(self):
  self.assertEqual(I['records_count'],5113)
  self.assertEqual(sum(v['records_count'] for v in I['batches']),5113)
  self.assertEqual(I['read_numbered_chapters'],list(range(1,88)))
  self.assertEqual(I['batches'][-1]['id'],'B04g')
  self.assertEqual(I['batches'][-1]['sha256'],H(B/'RULES.json'))
  self.assertEqual([r['record_number'] for r in R['rules']],list(range(5081,5114)))
 def test_next_literal_heading_and_validation_partition(self):
  self.assertEqual(I['next']['chapter'],'LXXXVIII')
  self.assertEqual(I['next']['printed_chapter_numeral'],'LXXXVII')
  self.assertEqual(I['next']['pdf_page'],491)
  self.assertEqual(I['empirical_validations'],0)
  self.assertEqual(I['runtime_promotions'],0)
  self.assertEqual(R['independent_appointment_outcomes_verified'],0)
 def test_exact_bytes_report_receipts_archive(self):
  self.assertEqual(H(IDX),P['new_index_sha256'])
  self.assertEqual(H(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'),P['current_state_sha256'])
  self.assertEqual(H(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04g_CHAPTER_LXXXVII_COMPLETE.md'),P['latest_state_sha256'])
  z=J(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json')
  self.assertEqual(H(z['owner_download_path']),P['owner_archive_sha256'])
  self.assertEqual(z['extracted_tests_passed'],14)
if __name__=='__main__':unittest.main(verbosity=2)
