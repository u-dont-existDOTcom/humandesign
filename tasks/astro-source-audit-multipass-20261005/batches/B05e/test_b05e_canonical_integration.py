import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_prior_batches_unchanged(self):
  x=J(B/"recovery/INDEX_BEFORE_B05e.json")
  self.assertEqual(x["records_count"],6415)
  self.assertEqual(x["batches"],I["batches"][:-1])
  self.assertEqual(H(B/"recovery/INDEX_BEFORE_B05e.json"),P["prior_index_sha256"])
 def test_exact_cumulative_record_integrity(self):
  self.assertEqual(I["records_count"],6474)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),6474)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,108)))
  self.assertEqual(I["batches"][-1]["id"],"B05e")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
 def test_next_manners_and_no_scientific_validation(self):
  self.assertEqual(I["next"]["chapter"],"CVIII")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CVII")
  self.assertEqual(I["next"]["pdf_page"],568)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
 def test_source_edition_identity(self):
  old=J(B/"recovery/INDEX_BEFORE_B05e.json")
  self.assertEqual(I["source_sha256"],old["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_report_index_and_archive_exact_sha256(self):
  for f,k in [(IDX,"new_index_sha256"),
  (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
  (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05e_TEMPERAMENT.md","latest_report_sha256"),
  (ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md","progress_report_sha256"),
  (B/"RULES.json","accepted_rules_sha256")]:
   self.assertEqual(H(f),P[k])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(z["owner_download_path"])),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],19)
if __name__=="__main__":unittest.main(verbosity=2)
