import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04o_CHAPTER_XCV_COMPLETE.md"
P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
I=J(IDX);R=J(B/"RULES.json")
class Canonical(unittest.TestCase):
 def test_exact_prior_index_and_source_lineage(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04o.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  x=J(old)
  self.assertEqual(x["records_count"],5457)
  self.assertEqual(x["batches"][-1]["id"],"B04n")
  self.assertEqual(x["batches"],I["batches"][:-1])
 def test_contiguous_ids_and_cumulative_counts(self):
  self.assertEqual(I["records_count"],5510)
  self.assertEqual(sum(r["records_count"] for r in I["batches"]),5510)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,96)))
  self.assertEqual(I["batches"][-1]["id"],"B04o")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(5458,5511)))
 def test_true_next_boundary_and_zero_scientific_promotion(self):
  self.assertEqual(I["next"]["chapter"],"XCVI")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"XCV")
  self.assertEqual(I["next"]["pdf_page"],504)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertTrue(R["definitive_source_witchcraft_judgment_negative"])
  self.assertTrue(R["author_does_not_confirm_syphilis"])
  self.assertEqual(R["independent_verified_medical_outcomes"],0)
 def test_exact_archive_and_report_sha256(self):
  self.assertEqual(H(IDX),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(REPORT),P["latest_report_sha256"])
  self.assertEqual(H(B/"RULES.json"),P["accepted_rules_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertTrue(z["full_extraction_pass"] and z["member_hashes_pass"])
  self.assertEqual(z["extracted_tests_passed"],21)
  self.assertFalse(P["remote_published"])
 def test_book_first_edition_hash_unchanged(self):
  old=J(B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04o.json")
  self.assertEqual(old["source_sha256"],I["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
if __name__=="__main__":unittest.main(verbosity=2)
