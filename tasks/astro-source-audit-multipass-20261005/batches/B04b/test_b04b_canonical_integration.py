import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04b_CHAPTER_LXXXII_COMPLETE.md"
IDX=J(I);R=J(B/"RULES.json");P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Integration(unittest.TestCase):
 def test_exact_prior_index_preserved(self):
  previous=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04b_CANONICAL.json"
  self.assertEqual(H(previous),P["previous_index_sha256"])
  prev=J(previous)
  self.assertEqual(prev["records_count"],4688)
  self.assertEqual(prev["batches"][-1]["id"],"B04a")
  self.assertEqual(prev["batches"],IDX["batches"][:-1])
 def test_canonical_ordinals_and_counts(self):
  self.assertEqual(IDX["records_count"],4829)
  self.assertEqual(sum(b["records_count"] for b in IDX["batches"]),4829)
  self.assertEqual(IDX["read_numbered_chapters"],list(range(1,83)))
  self.assertEqual(IDX["batches"][-1]["id"],"B04b")
  self.assertEqual(IDX["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(4689,4830)))
 def test_next_chapter_and_empirical_separation(self):
  self.assertEqual(IDX["next"]["chapter"],"LXXXIII")
  self.assertEqual(IDX["next"]["pdf_page"],482)
  self.assertEqual(IDX["empirical_validations"],0)
  self.assertEqual(IDX["runtime_promotions"],0)
  self.assertEqual(R["independently_verified_office_outcomes"],0)
  self.assertTrue(R["separate_new_office_and_existing_office_endpoints"])
 def test_bytes_match_prepublication_receipts(self):
  self.assertEqual(H(I),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(LATEST),P["latest_state_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],18)
  self.assertFalse(P["remote_published"])
if __name__=="__main__":unittest.main(verbosity=2)
