import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04d_CHAPTER_LXXXIV_COMPLETE.md"
IDX=J(I);R=J(B/"RULES.json");P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Integration(unittest.TestCase):
 def test_exact_previous_index(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04d_CANONICAL.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  prev=J(old);self.assertEqual(prev["records_count"],4875)
  self.assertEqual(prev["batches"][-1]["id"],"B04c")
  self.assertEqual(prev["batches"],IDX["batches"][:-1])
 def test_cumulative_counts_ids(self):
  self.assertEqual(IDX["records_count"],4954)
  self.assertEqual(sum(r["records_count"] for r in IDX["batches"]),4954)
  self.assertEqual(IDX["read_numbered_chapters"],list(range(1,85)))
  self.assertEqual(IDX["batches"][-1]["id"],"B04d")
  self.assertEqual(IDX["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(4876,4955)))
 def test_boundary_and_empirical_partition(self):
  self.assertEqual(IDX["next"]["chapter"],"LXXXV")
  self.assertEqual(IDX["next"]["pdf_page"],486)
  self.assertEqual(IDX["empirical_validations"],0)
  self.assertEqual(IDX["runtime_promotions"],0)
  self.assertTrue(R["vocational_glyphs_verified_mars_venus"])
  self.assertEqual(R["real_vocational_outcomes_independently_verified"],0)
 def test_state_hash_and_zip(self):
  self.assertEqual(H(I),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(LATEST),P["latest_state_sha256"])
  ziprec=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
  self.assertEqual(H(ziprec["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(ziprec["extracted_tests_passed"],15)
  self.assertFalse(P["remote_published"])
if __name__=="__main__":unittest.main(verbosity=2)
