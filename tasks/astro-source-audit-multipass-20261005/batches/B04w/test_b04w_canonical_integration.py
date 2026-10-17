import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[3]
j=lambda p:json.loads(Path(p).read_text())
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
I=R/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
idx=j(I);P=j(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Canonical(unittest.TestCase):
 def test_parent_batched_sources_exact(self):
  old=j(B/"recovery/INDEX_BEFORE_B04w.json")
  self.assertEqual(old["records_count"],5824)
  self.assertEqual(old["batches"],idx["batches"][:-1])
  self.assertEqual(h(B/"recovery/INDEX_BEFORE_B04w.json"),P["prior_index_sha256"])
 def test_cumulative_id_and_numbering(self):
  self.assertEqual(idx["records_count"],sum(x["records_count"] for x in idx["batches"]))
  self.assertEqual(idx["records_count"],5923)
  self.assertEqual(idx["read_numbered_chapters"],list(range(1,100)))
  self.assertEqual(idx["batches"][-1]["id"],"B04w")
 def test_next_animodar(self):
  self.assertEqual(idx["next"]["chapter"],"C")
  self.assertEqual(idx["next"]["printed_chapter_numeral"],"XCIX")
  self.assertEqual(idx["next"]["pdf_page"],539)
 def test_promotion_separation(self):
  self.assertTrue(P["original_source_trutine_degree_precision_unreliable"])
  self.assertEqual(idx["empirical_validations"],0)
  self.assertEqual(idx["runtime_promotions"],0)
 def test_report_and_archive_byte_identical(self):
  self.assertEqual(h(I),P["new_index_sha256"])
  self.assertEqual(h(B/"RULES.json"),P["rules_sha256"])
  self.assertEqual(h(R/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"),P["current_sha256"])
  self.assertEqual(h(R/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04w_TRUTINE_RECTIFICATION.md"),P["report_sha256"])
  receipt=j(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json")
  self.assertEqual(h(Path(receipt["owner_download_path"])),P["owner_archive_sha256"])
if __name__=="__main__":unittest.main(verbosity=2)
