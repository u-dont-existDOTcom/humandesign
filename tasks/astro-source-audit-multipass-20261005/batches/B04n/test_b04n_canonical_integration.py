import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04n_CHAPTER_XCIV_COMPLETE.md"
P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
I=J(IDX);R=J(B/"RULES.json")
class Canonical(unittest.TestCase):
 def test_exact_parent_preserved(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04n.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  parent=J(old)
  self.assertEqual(parent["records_count"],5413)
  self.assertEqual(parent["batches"][-1]["id"],"B04m")
  self.assertEqual(parent["batches"],I["batches"][:-1])
 def test_cumulative_ordinals_and_per_batch_total(self):
  self.assertEqual(I["records_count"],5457)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),5457)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,95)))
  self.assertEqual(I["batches"][-1]["id"],"B04n")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(5414,5458)))
 def test_next_chapter_and_science_partition(self):
  self.assertEqual(I["next"]["chapter"],"XCV")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"XCIV")
  self.assertEqual(I["next"]["pdf_page"],502)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertTrue(R["author_reports_one_day_early_estimate"])
  self.assertTrue(R["actual_day_january_13_or_14_ambiguous"])
  self.assertEqual(R["independently_authenticated_horse_outcomes"],0)
 def test_source_archival_sha_and_state_report_exact(self):
  self.assertEqual(H(IDX),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(LATEST),P["latest_report_sha256"])
  self.assertEqual(H(B/"RULES.json"),P["accepted_rules_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],18)
  self.assertTrue(z["full_extraction_pass"] and z["member_hashes_pass"])
  self.assertFalse(P["remote_published"])
 def test_original_book_provenance_identical(self):
  parent=J(B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04n.json")
  self.assertEqual(parent["source_sha256"],I["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
if __name__=="__main__":unittest.main(verbosity=2)
