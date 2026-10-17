import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent; ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04l_CHAPTER_XCII_COMPLETE.md"
P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
I=J(IDX);R=J(B/"RULES.json")
class Canonical(unittest.TestCase):
 def test_parent_preserved_and_byte_identical(self):
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04l.json"
  self.assertEqual(H(old),P["previous_index_sha256"])
  prior=J(old)
  self.assertEqual(prior["records_count"],5307)
  self.assertEqual(prior["batches"][-1]["id"],"B04k")
  self.assertEqual(prior["batches"],I["batches"][:-1])
 def test_cumulative_index_and_explicit_numbering(self):
  self.assertEqual(I["records_count"],5338)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),5338)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,93)))
  self.assertEqual(I["batches"][-1]["id"],"B04l")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(5308,5339)))
 def test_next_divider_and_science_not_promoted(self):
  self.assertEqual(I["next"]["chapter"],"XCIII")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"XCII")
  self.assertEqual(I["next"]["pdf_page"],498)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(R["independently_authenticated_captive_outcomes"],0)
 def test_archive_report_index_provenance_sha(self):
  self.assertEqual(H(IDX),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["state_sha256"])
  self.assertEqual(H(LATEST),P["report_sha256"])
  self.assertEqual(H(B/"RULES.json"),P["rules_sha256"])
  Z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertTrue(Z["full_extraction_pass"] and Z["member_hashes_pass"])
  self.assertEqual(Z["extracted_tests_passed"],17)
  self.assertFalse(P["remote_published"])
 def test_original_full_pdf_identity(self):
  parent=J(B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04l.json")
  self.assertEqual(parent["source_sha256"],I["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
if __name__=="__main__":unittest.main(verbosity=2)
