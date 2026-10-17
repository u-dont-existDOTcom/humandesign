import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[3]
j=lambda p:json.loads(Path(p).read_text())
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
idx=R/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=j(idx);P=j(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Integration(unittest.TestCase):
 def test_exact_prior_index_preserved(self):
  o=j(B/"recovery/INDEX_BEFORE_B04v.json")
  self.assertEqual(o["records_count"],5753)
  self.assertEqual(o["batches"],I["batches"][:-1])
  self.assertEqual(h(B/"recovery/INDEX_BEFORE_B04v.json"),P["prior_index_sha256"])
 def test_cumulative_source_counts(self):
  self.assertEqual(I["records_count"],sum(z["records_count"] for z in I["batches"]))
  self.assertEqual(I["records_count"],5824)
  self.assertEqual(I["batches"][-1]["id"],"B04v")
  self.assertEqual(I["read_numbered_chapters"],list(range(1,99)))
 def test_next_numbered_rectification_and_numeric_caveats(self):
  self.assertEqual(I["next"]["chapter"],"XCIX")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"XCVIII")
  self.assertEqual(I["next"]["pdf_page"],534)
  self.assertFalse(P["numeric_tables_full_digitization"])
  self.assertEqual(P["printed_arithmetic_discrepancy_arcminutes"],120)
 def test_verification_and_no_empirical_data(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(P["combined_if_published"],6890)
 def test_exact_index_report_archive_sha256(self):
  self.assertEqual(h(idx),P["new_index_sha256"])
  self.assertEqual(h(B/"RULES.json"),P["rules_sha256"])
  self.assertEqual(h(R/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"),P["current_state_sha256"])
  self.assertEqual(h(R/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04v_BOOK_III_INTRO_COMPLETE.md"),P["report_sha256"])
  z=j(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(h(Path(z["owner_download_path"])),P["owner_archive_sha256"])
if __name__=="__main__":unittest.main(verbosity=2)
