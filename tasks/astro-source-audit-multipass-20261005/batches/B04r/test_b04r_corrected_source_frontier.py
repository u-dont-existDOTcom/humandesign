from pathlib import Path
import json,hashlib,unittest
B=Path(__file__).resolve().parent;R=B.parents[3]
j=lambda p:json.loads(Path(p).read_text())
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
index=R/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
I=j(index);C=j(B/"SOURCE_ORDER_CORRECTION_RECEIPT_20261017.json")
class Audit(unittest.TestCase):
 def test_same_accepted_baseline(self):
  self.assertEqual(I["records_count"],5586)
  self.assertEqual(I["batches"][-1]["id"],"B04q")
  self.assertEqual(C["new_documentary_records"],0)
 def test_page_hashes(self):
  for p in C["page_witnesses"]:
   f=B/"evidence"/f"pdf_1647-{p['original_pdf_page']}.jpg"
   self.assertEqual(h(f),p["sha256"])
 def test_next_numbered_chapter(self):
  s=I["next"]["postchapter_source_order"]
  self.assertEqual((s[2]["first_pdf"],s[2]["last_pdf"]),(516,520))
  self.assertEqual(s[3]["pdf_page"],521)
 def test_parent_preserved(self):
  old=j(B/"recovery/INDEX_BEFORE_B04r_SOURCE_BOUNDARY_CORRECTION.json")
  self.assertEqual(old["batches"],I["batches"])
  self.assertEqual(h(index),C["new_index_sha256"])
 def test_zero_empirical_validation(self):
  self.assertEqual(I["empirical_validations"],0)
  self.assertEqual(I["runtime_promotions"],0)
if __name__=="__main__":unittest.main(verbosity=2)
