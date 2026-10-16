import json,hashlib,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
J=lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
IDX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CUR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03l_CHAPTER_LXVI_COMPLETE.md"
I=J(IDX); R=J(B/"RULES.json"); A=J(B/"ACCEPTANCE.json")
P=J(B/"CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json")
class Integration(unittest.TestCase):
    def test_exact_previous_source_preserved(self):
        older=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03l_CANONICAL.json"
        self.assertEqual(H(older),P["previous_index_sha256"])
        x=J(older)
        self.assertEqual(x["records_count"],3670)
        self.assertEqual(x["batches"][-1]["id"],"B03k")
        self.assertEqual(x["next"]["chapter"],"LXVI")
        self.assertEqual(x["source_sha256"],I["source_sha256"])
    def test_new_source_invariant_and_total(self):
        self.assertEqual(I["records_count"],3746)
        self.assertEqual(sum(b["records_count"] for b in I["batches"]),3746)
        self.assertEqual(I["read_numbered_chapters"],list(range(1,67)))
        self.assertEqual(I["batches"][-1]["id"],"B03l")
        self.assertEqual(I["batches"][-1]["records_count"],76)
        self.assertEqual(I["batches"][-1]["sha256"],H(B/"RULES.json"))
        self.assertEqual([r["record_number"] for r in R["rules"]],list(range(3671,3747)))
    def test_next_chapter_and_original_divider(self):
        self.assertEqual(I["next"]["chapter"],"LXVII")
        self.assertEqual(I["next"]["pdf_page"],438)
        self.assertEqual(I["next"]["printed_page"],404)
        self.assertTrue(all(r["chapter"]=="LXVII_NAVIGATION_ONLY" for r in R["rules"][-2:]))
    def test_chronology_miss_not_reclassified(self):
        self.assertEqual(A["original_literal_surrender_year"],"1644")
        self.assertEqual(A["historically_corrob_surrender_year"],"1643")
        self.assertTrue(A["surrender_three_days_late_as_author_says"])
        self.assertEqual(I["empirical_validations"],0)
        self.assertEqual(I["runtime_promotions"],0)
        self.assertEqual(A["new_empirical_predictions_validated"],0)
    def test_state_and_hash_replay(self):
        self.assertEqual(H(IDX),P["new_index_sha256"])
        self.assertEqual(H(CUR),P["new_current_state_sha256"])
        self.assertEqual(H(LATEST),P["new_latest_state_sha256"])
        z=J(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json")
        self.assertEqual(H(z["download_path"]),P["owner_download_archive_sha256"])
        self.assertEqual(z["extracted_source_tests_passed"],26)
        self.assertEqual(z["extracted_test_exit_code"],0)
        self.assertFalse(P["remote_published"])
if __name__=="__main__":unittest.main(verbosity=2)
