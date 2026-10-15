"""Guard the B02v source-only canonical-index integration before publication.

Historical documentary admission, not an astrology prediction/clinical or
criminal verification. Run against the prepared working branch; publication
requires later nonforce remote push and remote readback.
"""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
def j(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
class CanonicalSourceIndexU75(unittest.TestCase):
 def test_index_records_batch_totals_and_unique(self):
  x=j(IDX)
  self.assertEqual(x["records_count"],2974)
  self.assertEqual(sum(z["records_count"] for z in x["batches"]),2974)
  self.assertEqual(len({z["id"] for z in x["batches"]}),len(x["batches"]))
  self.assertEqual(x["batches"][-2]["id"],"B02u")
  self.assertEqual(x["batches"][-1]["id"],"B02v")
  self.assertEqual(x["batches"][-1]["records_count"],402)
  self.assertEqual(x["batches"][-1]["path"],"batches/B02v/RULES.json")
 def test_source_sha_and_dated_release(self):
  x=j(IDX)
  a=j(B/"ACCEPTANCE.json")
  self.assertEqual(x["source_sha256"],a["original_source_pdf_sha256"])
  self.assertEqual(x["batches"][-1]["sha256"],sha(B/"RULES.json"))
  self.assertEqual(a["rules_sha256"],sha(B/"RULES.json"))
  self.assertEqual(a["unresolved_sha256"],sha(B/"UNRESOLVED.json"))
  self.assertEqual(a["source_order_sha256"],sha(B/"SOURCE_ORDER.json"))
  self.assertEqual(a["uncertainties_retained"],75)
 def test_numbered_chapter_and_precise_next_page(self):
  x=j(IDX)
  self.assertEqual(x["read_numbered_chapters"],list(range(1,51)))
  self.assertEqual(x["next"]["chapter"],"LI")
  self.assertEqual(x["next"]["pdf_page"],400)
  self.assertEqual(x["next"]["printed_page"],366)
  self.assertIn("BELOW",x["next"]["position"])
  self.assertFalse(x["next"]["extracted"])
 def test_historical_only_no_empirical(self):
  x=j(IDX)
  s=j(B/"CLAIM_LEDGER.json")
  self.assertEqual(x["runtime_promotions"],0)
  self.assertEqual(x["empirical_validations"],0)
  self.assertEqual(s["empirical_predictive_outcomes"],0)
  self.assertFalse(s["clinical_or_criminal_uses_authorized"])
  self.assertTrue(j(B/"RULES.json")["documentary_accepted_locally"])
  self.assertEqual(len(j(B/"RULES.json")["rules"]),402)
 def test_state_and_prior_index_preserved(self):
  x=j(IDX)
  self.assertTrue((ROOT/x["current_state"]).is_file())
  old=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02v_CANONICAL_20261015.json"
  self.assertTrue(old.is_file())
  old_j=j(old)
  self.assertEqual(old_j["records_count"],2572)
  self.assertEqual(old_j["batches"][-1]["id"],"B02u")
  self.assertEqual(j(B/"CANONICAL_INTEGRATION_PREPARE_RECEIPT_U75_20261015.json")["previous_index_sha256"],sha(old))
 def test_archive_receipt_and_original_boundary(self):
  r=j(B/"independent_review/DOCUMENTARY_SOURCE_RELEASE_RECEIPT_U75_20261015.json")
  a=j(B/"ACCEPTANCE.json")
  self.assertEqual(r["archive_sha256"],r["destination_sha256"])
  self.assertEqual(r["number_archived_files"],256)
  self.assertEqual(r["number_original_source_images"],21)
  self.assertEqual(sum(v["tests_run"] for v in r["actual_extracted_tests"].values()),109)
  self.assertFalse(a["source_independent_full_diplomatic_transcription_done"])
  self.assertTrue(a["printed_p360_line4_erratum_glyph_unresolved"])
  self.assertEqual(a["next_source"]["chapter"],"LI")
  self.assertIn("BELOW",a["next_source"]["physical_boundary"])
if __name__=="__main__":unittest.main()
