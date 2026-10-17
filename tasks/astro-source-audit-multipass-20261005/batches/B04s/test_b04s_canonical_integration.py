import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;root=B.parents[3]
j=lambda p:json.loads(Path(p).read_text())
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
idx=root/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
d=j(idx);p=j(B/"CANONICAL_INDEX_PREPARE_RECEIPT_20261017.json")
class Check(unittest.TestCase):
 def test_parent(self):
  x=j(B/"recovery/INDEX_BEFORE_B04s.json")
  self.assertEqual(x["records_count"],5586)
  self.assertEqual(x["batches"],d["batches"][:-1])
 def test_total(self):
  self.assertEqual(d["records_count"],sum(k["records_count"] for k in d["batches"]))
  self.assertEqual(d["records_count"],5629)
 def test_no_new_numbered_chapter(self):
  self.assertEqual(d["read_numbered_chapters"],list(range(1,98)))
  self.assertEqual(d["next"]["chapter"],"PLANETARY_HOUR_TABLE")
 def test_hashes(self):
  self.assertEqual(h(idx),p["new_index_sha256"])
  self.assertEqual(h(B/"RULES.json"),p["accepted_rules_sha256"])
  self.assertEqual(h(root/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261017_B04s_ESSEX_ACCEPTED.md"),p["report_sha256"])
 def test_no_predictive_credit(self):
  self.assertEqual(d["empirical_validations"],0)
  self.assertEqual(d["runtime_promotions"],0)
  self.assertFalse(p["independent_original_astrology_forecast"])
if __name__=="__main__":unittest.main(verbosity=2)
