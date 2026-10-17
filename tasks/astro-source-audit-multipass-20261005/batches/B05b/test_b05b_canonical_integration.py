import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_exact_prior_history_preserved(self):
  old=B/"recovery/INDEX_BEFORE_B05b.json";prior=J(old)
  self.assertEqual(prior["records_count"],6244)
  self.assertEqual(prior["batches"],I["batches"][:-1])
  self.assertEqual(H(old),P["prior_index_sha256"])
 def test_cumulative_counts_and_numbered_chapters(self):
  self.assertEqual(I["records_count"],6309)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),6309)
  self.assertEqual(I["batches"][-1]["id"],"B05b")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual(I["read_numbered_chapters"],list(range(1,105)))
 def test_following_hyleg_separate_and_explicit_warning(self):
  self.assertEqual(I["next"]["chapter"],"CV")
  self.assertEqual(I["next"]["pdf_page"],561)
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CIV")
  self.assertTrue(P["original_explicit_warning_preserved"])
  self.assertTrue(P["original_medical_longevity_claims_unvalidated"])
 def test_no_empirical_validation_or_runtime_changes(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(P["combined_if_published"],7375)
 def test_index_report_archive_exact_sha256(self):
  for f,k in ((IDX,"new_index_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05b_LIFESPAN_SOURCE.md","latest_report_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md","progress_sha256"),
    (B/"RULES.json","accepted_rules_sha256")):
   self.assertEqual(H(f),P[k])
  Z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(Z["owner_download_path"])),P["owner_archive_sha256"])
  self.assertEqual(Z["extracted_tests_passed"],19)
if __name__=="__main__":unittest.main(verbosity=2)
