import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
REPORT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04m_CHAPTER_XCIII_COMPLETE.md"
P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
I=J(IDX);R=J(B/"RULES.json")
class Integration(unittest.TestCase):
 def test_exact_parent_original_identity(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04m.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  prev=J(old)
  self.assertEqual(prev["records_count"],5338)
  self.assertEqual(prev["batches"][-1]["id"],"B04l")
  self.assertEqual(prev["batches"],I["batches"][:-1])
 def test_cumulative_count_and_ordinals(self):
  self.assertEqual(I["records_count"],5413)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),5413)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,94)))
  self.assertEqual(I["batches"][-1]["id"],"B04m")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(5339,5414)))
 def test_original_chapter_boundary_and_no_predictive_credit(self):
  self.assertEqual(I["next"]["chapter"],"XCIV")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"XCIII")
  self.assertEqual(I["next"]["pdf_page"],501)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(R["independent_verified_witchcraft_cases"],0)
  self.assertEqual(R["independent_verified_remedy_outcomes"],0)
 def test_archive_source_report_and_index_exact_bytes(self):
  self.assertEqual(H(IDX),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(REPORT),P["latest_report_sha256"])
  self.assertEqual(H(B/"RULES.json"),P["accepted_rules_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],21)
  self.assertTrue(z["full_extraction_pass"] and z["member_hashes_pass"])
  self.assertFalse(P["remote_published"])
 def test_parent_pdf_witness_preserved(self):
  old=J(B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04m.json")
  self.assertEqual(old["source_sha256"],I["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
if __name__=="__main__":unittest.main(verbosity=2)
