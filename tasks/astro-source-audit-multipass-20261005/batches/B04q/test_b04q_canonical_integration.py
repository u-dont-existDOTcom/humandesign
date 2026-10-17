import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
idx=J(I);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_unchanged_parent(self):
  old=J(B/"recovery/INDEX_BEFORE_B04q.json")
  self.assertEqual(old["records_count"],5552)
  self.assertEqual(old["batches"],idx["batches"][:-1])
 def test_count_integrity(self):
  self.assertEqual(idx["records_count"],sum(x["records_count"] for x in idx["batches"]))
  self.assertEqual(idx["records_count"],5586)
  self.assertEqual(idx["read_numbered_chapters"],list(range(1,98)))
 def test_postchapter_unumbered(self):
  self.assertEqual(idx["next"]["chapter"],"POST_XCVI_UNNUMBERED_ESSEX_AND_TABLES")
  self.assertEqual(idx["next"]["pdf_page"],507)
  self.assertEqual(idx["empirical_validations"],0)
  self.assertEqual(idx["runtime_promotions"],0)
 def test_index_and_report_sha(self):
  self.assertEqual(H(I),P["new_index_sha256"])
  self.assertEqual(H(B/"RULES.json"),P["accepted_rules_sha256"])
  self.assertEqual(H(ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04q_CHAPTER_XCVII_COMPLETE.md"),P["latest_report_sha256"])
 def test_archive_sha(self):
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(z["owner_download_path"])),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],14)
if __name__=="__main__":unittest.main(verbosity=2)
