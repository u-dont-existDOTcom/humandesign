import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda x:json.loads(Path(x).read_text(encoding="utf-8"))
H=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
I=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03z_CHAPTER_LXXX_COMPLETE.md"
IDX=J(I);R=J(B/"RULES.json")
P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Integration(unittest.TestCase):
 def test_exact_parent_index_preserved(self):
  before=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03z_CANONICAL.json"
  self.assertEqual(H(before),P["previous_index_sha256"])
  prev=J(before)
  self.assertEqual(prev["records_count"],4549)
  self.assertEqual(prev["batches"][-1]["id"],"B03y")
  self.assertEqual(prev["batches"],IDX["batches"][:-1])
 def test_contiguous_source_index_and_exact_rows(self):
  self.assertEqual(IDX["records_count"],4631)
  self.assertEqual(sum(x["records_count"] for x in IDX["batches"]),4631)
  self.assertEqual(IDX["read_numbered_chapters"],list(range(1,81)))
  self.assertEqual(IDX["batches"][-1]["id"],"B03z")
  self.assertEqual(IDX["batches"][-1]["sha256"],H(B/"RULES.json"))
  self.assertEqual([r["record_number"] for r in R["rules"]],list(range(4550,4632)))
 def test_next_chapter_and_empirical_isolation(self):
  self.assertEqual(IDX["next"]["chapter"],"LXXXI")
  self.assertEqual(IDX["next"]["pdf_page"],476)
  self.assertEqual(IDX["empirical_validations"],0)
  self.assertEqual(IDX["runtime_promotions"],0)
  self.assertEqual(R["independently_verified_political_events"],0)
  self.assertTrue(R["historical_status_quo_reform_qualification_retained"])
 def test_local_state_archive_provenance(self):
  self.assertEqual(H(I),P["new_index_sha256"])
  self.assertEqual(H(CUR),P["current_state_sha256"])
  self.assertEqual(H(LATEST),P["latest_state_sha256"])
  ziprec=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
  self.assertEqual(H(ziprec["owner_download_path"]),P["owner_archive_sha256"])
  self.assertEqual(ziprec["extracted_tests_passed"],19)
  self.assertFalse(P["remote_published"])
if __name__=="__main__":unittest.main(verbosity=2)
