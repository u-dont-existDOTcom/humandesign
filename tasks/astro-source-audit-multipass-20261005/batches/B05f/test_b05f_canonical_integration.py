import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=J(IDX);P=J(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_old_index_history_preserved_exact(self):
  old=B/"recovery/INDEX_BEFORE_B05f.json"
  prev=J(old)
  self.assertEqual(prev["records_count"],6474)
  self.assertEqual(prev["batches"],I["batches"][:-1])
  self.assertEqual(H(old),P["previous_index_sha256"])
 def test_cumulative_counts_and_chapters(self):
  self.assertEqual(I["records_count"],6560)
  self.assertEqual(sum(x["records_count"] for x in I["batches"]),6560)
  self.assertEqual(I["read_numbered_chapters"],list(range(1,109)))
  self.assertEqual(I["batches"][-1]["id"],"B05f")
  self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
 def test_next_separate_printed_chapter(self):
  self.assertEqual(I["next"]["chapter"],"CIX")
  self.assertEqual(I["next"]["printed_chapter_numeral"],"CVIII")
  self.assertEqual(I["next"]["pdf_page"],573)
 def test_science_not_promoted(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
  self.assertEqual(P["independently_validated_personality"],0)
 def test_index_report_archive_hashes(self):
  for f,k in [(IDX,"new_index_sha256"),(ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md","current_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md","progress_report_sha256"),
    (ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B05f_MANNERS.md","latest_report_sha256"),
    (B/"RULES.json","accepted_rules_sha256")]:
   self.assertEqual(H(f),P[k],str(f))
  z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(H(z["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(z["extracted_tests_passed"],20)
if __name__=="__main__":unittest.main(verbosity=2)
