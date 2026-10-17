import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_prior_source_index_unchanged(self):
  old=B/"recovery/INDEX_BEFORE_B05c.json";prior=J(old)
  self.assertEqual(prior["records_count"],6309)
  self.assertEqual(prior["batches"],I["batches"][:-1])
  self.assertEqual(H(old),P["original_index_sha256"])
 def test_append_counts_and_numbered_chapter_sequence(self):
  self.assertEqual(I["records_count"],6383)
  self.assertEqual(sum(q["records_count"] for q in I["batches"]),6383)
  self.assertEqual(I["batches"][-1]["id"],"B05c")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual(I["read_numbered_chapters"],list(range(1,106)))
 def test_next_chapter_and_author_skepticism_retained(self):
  self.assertEqual(I["next"]["chapter"],"CVI")
  self.assertEqual(I["next"]["pdf_page"],565)
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CV")
  self.assertTrue(P["original_author_uncertainty_preserved"])
  self.assertEqual(P["combined_if_published"],7449)
 def test_science_no_promotion(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(P["new_empirical_validations"],0)
  self.assertEqual(P["runtime_promotions"],0)
 def test_byte_hashes_and_archival_replay(self):
  for f,k in ((IDX,"new_index_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05c_HYLEG_SOURCE.md","latest_report_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md","progress_report_sha256"),
    (B/"RULES.json","rules_sha256")):
   self.assertEqual(H(f),P[k])
  Z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(Z["owner_download_path"])),P["owner_archive_sha256"])
  self.assertEqual(Z["extracted_tests_passed"],19)
if __name__=="__main__":unittest.main(verbosity=2)
