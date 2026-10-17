import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_original_accepted_index_preserved(self):
  prior=J(B/"recovery/INDEX_BEFORE_B04z.json")
  self.assertEqual(prior["records_count"],6145)
  self.assertEqual(prior["batches"],I["batches"][:-1])
  self.assertEqual(H(B/"recovery/INDEX_BEFORE_B04z.json"),P["prior_index_sha256"])
 def test_cumulative_count_and_numbered_chapters(self):
  self.assertEqual(I["records_count"],6215)
  self.assertEqual(sum(b["records_count"] for b in I["batches"]),6215)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,103)))
  self.assertEqual(I["batches"][-1]["id"],"B04z")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
 def test_next_chapter_boundary_and_no_validation(self):
  self.assertEqual(I["next"]["chapter"],"CIII")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CII")
  self.assertEqual(I["next"]["pdf_page"],558)
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
 def test_original_book_identity_stable(self):
  previous=J(B/"recovery/INDEX_BEFORE_B04z.json")
  self.assertEqual(previous["source_sha256"],I["source_sha256"])
  self.assertEqual(I["source_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
 def test_index_and_archive_byte_hashes(self):
  for f,k in ((IDX,"new_index_sha256"),
   (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
   (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04z_REGIOMONTANUS_METHOD.md","latest_report_sha256"),
   (ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md","progress_sha256"),
   (B/"RULES.json","rules_sha256")):
   self.assertEqual(H(f),P[k])
  Z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Z["owner_download_path"]),P["archive_sha256"])
  self.assertEqual(Z["extracted_tests_passed"],20)
if __name__=="__main__":unittest.main(verbosity=2)
