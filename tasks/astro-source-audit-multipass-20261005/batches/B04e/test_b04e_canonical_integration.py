import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04e_CHAPTER_LXXXV_COMPLETE.md"
IDX=J(I);R=J(B/"RULES.json");P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Integration(unittest.TestCase):
 def test_exact_prior_index_and_immutable_batches(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04e_CANONICAL.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  prev=J(old)
  self.assertEqual(prev["records_count"],4954)
  self.assertEqual(prev["batches"][-1]["id"],"B04d")
  self.assertEqual(prev["batches"],IDX["batches"][:-1])
 def test_canonical_source_units_and_ordinals(self):
  self.assertEqual(IDX["records_count"],5026)
  self.assertEqual(sum(b["records_count"] for b in IDX["batches"]),5026)
  self.assertEqual(IDX["read_numbered_chapters"],list(range(1,86)))
  self.assertEqual(IDX["batches"][-1]["id"],"B04e")
  self.assertEqual(IDX["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(4955,5027)))
 def test_next_chapter_and_retained_authorial_error(self):
  self.assertEqual(IDX["next"]["chapter"],"LXXXVI")
  self.assertEqual(IDX["next"]["pdf_page"],489)
  self.assertEqual(IDX["empirical_validations"],0)
  self.assertEqual(IDX["runtime_promotions"],0)
  self.assertTrue(R["author_acknowledged_partial_error"])
  self.assertTrue(R["pre_question_battle_not_prospective"])
  self.assertEqual(R["independently_verified_wartime_predictions"],0)
 def test_canonical_and_archive_bytes(self):
  self.assertEqual(H(I),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(LATEST),P["latest_state_sha256"])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],17)
  self.assertFalse(P["remote_published"])
if __name__=="__main__":unittest.main(verbosity=2)
