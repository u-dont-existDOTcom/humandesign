import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[3]
j=lambda p:json.loads(Path(p).read_text())
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
i=R/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
idx=j(i);P=j(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Index(unittest.TestCase):
 def test_original_parent(self):
  old=j(B/"recovery/INDEX_BEFORE_B04t.json")
  self.assertEqual(old["records_count"],5629)
  self.assertEqual(old["batches"],idx["batches"][:-1])
 def test_total_and_numbered_order(self):
  self.assertEqual(idx["records_count"],sum(x["records_count"] for x in idx["batches"]))
  self.assertEqual(idx["records_count"],5639)
  self.assertEqual(idx["read_numbered_chapters"],list(range(1,98)))
 def test_next_chapter(self):
  self.assertEqual(idx["next"]["chapter"],"XCVIII")
  self.assertEqual(idx["next"]["printed_chapter_numeral"],"XCVII")
  self.assertEqual(idx["next"]["pdf_page"],516)
 def test_scientific_limit_preserved(self):
  self.assertFalse(P["numeric_cell_transcription_complete"])
  self.assertEqual(idx["empirical_validations"],0)
  self.assertEqual(idx["runtime_promotions"],0)
 def test_hashes_and_release(self):
  self.assertEqual(h(i),P["new_index_sha256"])
  self.assertEqual(h(B/"RULES.json"),P["rules_sha256"])
  self.assertEqual(h(R/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04t_PLANETARY_TABLE_IMAGES.md"),P["report_sha256"])
  a=j(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(h(Path(a["owner_download_path"])),P["owner_archive_sha256"])
if __name__=="__main__":unittest.main(verbosity=2)
