import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_original_parent_exact_preservation(self):
  old=B/"recovery/INDEX_BEFORE_B05a.json"
  prior=J(old)
  self.assertEqual(prior["records_count"],6215)
  self.assertEqual(prior["batches"],I["batches"][:-1])
  self.assertEqual(H(old),P["old_index_sha256"])
 def test_total_and_order(self):
  self.assertEqual(I["records_count"],6244)
  self.assertEqual(sum(b["records_count"] for b in I["batches"]),6244)
  self.assertEqual(I["batches"][-1]["id"],"B05a")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual(I["read_numbered_chapters"],list(range(1,104)))
 def test_lifespan_chapter_separate(self):
  self.assertEqual(I["next"]["chapter"],"CIV")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CIII")
  self.assertEqual(I["next"]["pdf_page"],559)
  self.assertEqual(P["records_added"],29)
  self.assertEqual(P["combined_if_published"],7310)
 def test_no_empirical_credit(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(P["new_empirical_validations"],0)
 def test_index_report_archive_byte_identity(self):
  for f,k in ((IDX,"new_index_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05a_NATAL_CONDITIONS.md","latest_report_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md","progress_sha256"),
    (B/"RULES.json","accepted_rules_sha256")):
   self.assertEqual(H(f),P[k],str(f))
  Z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(Path(Z["owner_download_path"])),P["owner_archive_sha256"])
  self.assertEqual(Z["archive_replayed_tests"],17)
if __name__=="__main__":unittest.main(verbosity=2)
