import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04a_CHAPTER_LXXXI_COMPLETE.md"
IDX=J(I);R=J(B/"RULES.json");P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Integration(unittest.TestCase):
 def test_previous_exact_index_preserved(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04a_CANONICAL.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  j=J(old);self.assertEqual(j["records_count"],4631)
  self.assertEqual(j["batches"][-1]["id"],"B03z")
  self.assertEqual(j["batches"],IDX["batches"][:-1])
 def test_global_record_ordinals_and_history(self):
  self.assertEqual(IDX["records_count"],4688)
  self.assertEqual(sum(k["records_count"] for k in IDX["batches"]),4688)
  self.assertEqual(IDX["read_numbered_chapters"],list(range(1,82)))
  self.assertEqual(IDX["batches"][-1]["id"],"B04a")
  self.assertEqual(IDX["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(4632,4689)))
 def test_next_boundary_and_epistemic_separation(self):
  self.assertEqual(IDX["next"]["chapter"],"LXXXII")
  self.assertEqual(IDX["next"]["pdf_page"],478)
  self.assertEqual(IDX["empirical_validations"],0)
  self.assertEqual(IDX["runtime_promotions"],0)
  self.assertEqual(R["independently_verified_alchemical_successes"],0)
  self.assertEqual(R["independently_authenticated_consumption_diagnoses"],0)
 def test_current_state_and_archive_exact_hashes(self):
  self.assertEqual(H(I),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(LATEST),P["latest_state_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],17)
  self.assertFalse(P["remote_published"])
if __name__=="__main__":unittest.main(verbosity=2)
