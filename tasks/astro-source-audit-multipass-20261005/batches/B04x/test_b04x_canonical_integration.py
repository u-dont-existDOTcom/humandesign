import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_exact_prior_index_preserved(self):
  old=B/"recovery/INDEX_BEFORE_B04x.json";o=J(old)
  self.assertEqual(o["records_count"],5923)
  self.assertEqual(o["batches"],I["batches"][:-1])
  self.assertEqual(H(old),P["old_index_sha256"])
 def test_contiguous_acceptance_and_batches_total(self):
  self.assertEqual(I["records_count"],5957)
  self.assertEqual(sum(r["records_count"] for r in I["batches"]),5957)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,101)))
  self.assertEqual(I["batches"][-1]["id"],"B04x")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
 def test_next_chapter_on_correct_original_page(self):
  self.assertEqual(I["next"]["chapter"],"CI")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"C")
  self.assertEqual(I["next"]["pdf_page"],541)
 def test_independent_validation_not_promoted(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(P["new_empirical_validations"],0)
 def test_index_report_progress_and_zip_hashes(self):
  self.assertEqual(H(IDX),P["new_index_sha256"])
  self.assertEqual(H(ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"),P["current_sha256"])
  self.assertEqual(H(ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04x_ANIMODAR_COMPLETE.md"),P["report_sha256"])
  self.assertEqual(H(ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"),P["progress_report_sha256"])
  self.assertEqual(H(B/"RULES.json"),P["rules_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(z["owner_download_path"])),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],19)
  self.assertTrue(z["full_extraction_pass"])
 def test_source_edition_hash_unchanged(self):
  o=J(B/"recovery/INDEX_BEFORE_B04x.json")
  self.assertEqual(o["source_sha256"],I["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
if __name__=="__main__":unittest.main(verbosity=2)
