import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda f:json.loads(Path(f).read_text())
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Integration(unittest.TestCase):
 def test_prior_index_batch_history_preserved(self):
  before=J(B/"recovery/INDEX_BEFORE_B05d.json")
  self.assertEqual(before["records_count"],6383)
  self.assertEqual(before["batches"],I["batches"][:-1])
  self.assertEqual(H(B/"recovery/INDEX_BEFORE_B05d.json"),P["prior_index_sha256"])
 def test_canonical_ordinal_and_cumulative_total(self):
  self.assertEqual(I["records_count"],6415)
  self.assertEqual(sum(b["records_count"] for b in I["batches"]),6415)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,107)))
  self.assertEqual(I["batches"][-1]["id"],"B05d")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
 def test_true_next_source_and_no_prediction(self):
  self.assertEqual(I["next"]["chapter"],"CVII")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CVI")
  self.assertEqual(I["next"]["pdf_page"],566)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
 def test_first_edition_id_unchanged(self):
  x=J(B/"recovery/INDEX_BEFORE_B05d.json")
  self.assertEqual(I["source_sha256"],x["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_exact_index_report_archive_SHA256(self):
  for path,key in ((IDX,"new_index_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05d_LORD_GENITURE.md","report_sha256"),
    (B/"RULES.json","rules_sha256")):
   self.assertEqual(H(path),P[key])
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(z["owner_download_path"])),P["archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],17)
if __name__=="__main__":unittest.main(verbosity=2)
