"""B02v postpublication historical-source provenance checks."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
read=lambda n:json.loads((B/n).read_text())
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
class PublicationReceiptChecks(unittest.TestCase):
 def test_canonical_index_binds_exact_accepted_source(self):
  j=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
  p=read("PUBLICATION_RECEIPT.json")
  self.assertEqual(j["records_count"],p["accepted_lilly_after"])
  self.assertEqual(j["batches"][-1]["sha256"],sha(B/"RULES.json"))
  self.assertEqual(j["next"]["chapter"],"LI")
  self.assertEqual(p["accepted_lilly_after"]+p["ptolemy_retained"],4040)
  self.assertEqual(p["source_branch"]!="",True)
  self.assertEqual(p["source_and_canonical_pushed_same_commit"],True)
 def test_archive_stored_original_bytes(self):
  r=read("DELIVERY_RECEIPT.json")
  path=Path(r["path"])
  self.assertTrue(path.is_file())
  self.assertEqual(path.stat().st_size,r["archive_bytes"])
  self.assertEqual(sha(path),r["expected_sha256"])
  self.assertEqual(r["observed_sha256"],r["expected_sha256"])
 def test_empirical_boundary_and_prepublication_snapshot(self):
  p=read("PUBLICATION_RECEIPT.json")
  self.assertEqual(p["predictive_validations_added"],0)
  self.assertEqual(p["authenticated_crime_cases"],0)
  self.assertEqual(p["runtime_promotions"],0)
  a=read("ACCEPTANCE.json")
  self.assertFalse(a["canonical_published"])
  self.assertTrue(a["accepted"])
  self.assertTrue(a["printed_p360_line4_erratum_glyph_unresolved"])
  self.assertEqual(read("OWNER_OUTCOME_STATUS.json")["parent_state"],"OPEN")
if __name__=="__main__":unittest.main()
