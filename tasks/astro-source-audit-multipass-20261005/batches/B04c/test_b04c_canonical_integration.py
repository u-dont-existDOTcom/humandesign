import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04c_CHAPTER_LXXXIII_COMPLETE.md"
IDX=J(I);R=J(B/"RULES.json");P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Integration(unittest.TestCase):
 def test_exact_parent_index_preserved(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04c_CANONICAL.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  x=J(old)
  self.assertEqual(x["records_count"],4829)
  self.assertEqual(x["batches"][-1]["id"],"B04b")
  self.assertEqual(x["batches"],IDX["batches"][:-1])
 def test_new_counts_and_record_ids(self):
  self.assertEqual(IDX["records_count"],4875)
  self.assertEqual(sum(x["records_count"] for x in IDX["batches"]),4875)
  self.assertEqual(IDX["read_numbered_chapters"],list(range(1,84)))
  self.assertEqual(IDX["batches"][-1]["id"],"B04c")
  self.assertEqual(IDX["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(4830,4876)))
 def test_next_lxxxiv_and_empirical_isolation(self):
  self.assertEqual(IDX["next"]["chapter"],"LXXXIV")
  self.assertEqual(IDX["next"]["pdf_page"],484)
  self.assertEqual(IDX["empirical_validations"],0)
  self.assertEqual(IDX["runtime_promotions"],0)
  self.assertEqual(R["independently_verified_restoration_outcomes"],0)
 def test_source_state_zip_hashes(self):
  self.assertEqual(H(I),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(LATEST),P["latest_state_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],16)
  self.assertFalse(P["remote_published"])
if __name__=="__main__":unittest.main(verbosity=2)
