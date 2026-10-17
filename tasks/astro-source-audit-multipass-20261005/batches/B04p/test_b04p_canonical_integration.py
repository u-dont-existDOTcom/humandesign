import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
I=J(IDX);R=J(B/"RULES.json")
class Canonical(unittest.TestCase):
 def test_previous_index_preserved(self):
  prev=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04p.json"
  self.assertEqual(H(prev),P["old_index_sha256"])
  j=J(prev);self.assertEqual(j["records_count"],5510)
  self.assertEqual(j["batches"],I["batches"][:-1])
 def test_record_continuity(self):
  self.assertEqual(I["records_count"],5552)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),5552)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,97)))
  self.assertEqual([x["record_number"] for x in R["rules"]],list(range(5511,5553)))
 def test_next_separate_chapter(self):
  self.assertEqual(I["next"]["chapter"],"XCVII")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"XCVI")
  self.assertEqual(I["next"]["pdf_page"],505)
 def test_source_and_report_hashes(self):
  self.assertEqual(H(IDX),P["new_index_sha256"])
  self.assertEqual(H(B/"RULES.json"),P["accepted_rules_sha256"])
  self.assertEqual(H(ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"),P["new_current_state_sha256"])
  self.assertEqual(H(ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04p_CHAPTER_XCVI_COMPLETE.md"),P["new_report_sha256"])
 def test_archive_and_science(self):
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(z["owner_download_path"])),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],18)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(R["independently_authenticated_fugitive_outcomes"],0)
if __name__=="__main__":unittest.main(verbosity=2)
