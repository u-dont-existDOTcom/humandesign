import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Integration(unittest.TestCase):
 def test_exact_source_index_parent_preserved(self):
  old=B/"recovery/INDEX_BEFORE_B04y_CANONICAL.json"
  prior=J(old)
  self.assertEqual(H(old),P["prior_index_sha256"])
  self.assertEqual(prior["records_count"],5957)
  self.assertEqual(prior["batches"],I["batches"][:-1])
 def test_complete_cumulative_counts_and_ordinals(self):
  self.assertEqual(I["records_count"],6145)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),6145)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,102)))
  self.assertEqual(I["batches"][-1]["id"],"B04y")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  R=J(B/"RULES.json")
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(5958,6146)))
 def test_true_following_regiomontanus_and_source_discrepancies(self):
  self.assertEqual(I["next"]["chapter"],"CII")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CI")
  self.assertEqual(I["next"]["pdf_page"],553)
  self.assertTrue(P["source_fever_age_mismatch_preserved"])
  self.assertTrue(P["source_biquintile_misprint_preserved"])
 def test_empirical_predictions_and_runtime_not_assigned(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(P["empirical_validations"],0)
  self.assertEqual(P["runtime_promotions"],0)
  self.assertEqual(P["combined_if_published"],7211)
 def test_exact_archive_report_index_progress_hashes(self):
  for f,k in ((IDX,"new_index_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04y_ACCIDENT_RECTIFICATION.md","latest_report_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md","progress_report_sha256"),
    (B/"RULES.json","accepted_rules_sha256")):
   self.assertEqual(H(f),P[k],str(f))
  Z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(Z["extracted_tests_passed"],28)
if __name__=="__main__":unittest.main(verbosity=2)
