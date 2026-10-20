"""Guarded after-append index, original two-edition Children single-folio only."""
import json
from hashlib import sha256
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07be_CHILDREN.md"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"

def read(p):return json.loads(p.read_text(encoding="utf-8"))
def digest(p):return sha256(p.read_bytes()).hexdigest()

class OriginalChildrenAppendAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=read(B/"recovery/LILLY_INDEX_BEFORE_B07be.json")
        cls.after=read(INDEX)
        cls.rec=read(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.src=read(B/"ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json")
        cls.accept=read(B/"ACCEPTANCE.json")
        cls.release=read(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_exact_one_time_source_record_count(self):
        self.assertEqual((self.before["records_count"],self.after["records_count"]),
                         (13101,13131))
        self.assertEqual(sum(x["records_count"] for x in self.after["batches"]),13131)
        self.assertEqual(self.after["batches"][-1]["records_count"],30)
        self.assertEqual(self.after["batches"][-1]["id"],"B07be")

    def test_02_all_prior_canonical_historical_batches_untouched(self):
        self.assertEqual(self.before["batches"],self.after["batches"][:-1])
        self.assertEqual(self.after["batches"][-1]["sha256"],
                         digest(B/"RULES.json"))

    def test_03_original_index_before_and_after_sha_exact(self):
        self.assertEqual(digest(B/"recovery/LILLY_INDEX_BEFORE_B07be.json"),
                         self.rec["old_index_sha256"])
        self.assertEqual(digest(INDEX),self.rec["new_index_sha256"])
        self.assertEqual(self.rec["old_index_sha256"],
                         "ad395b0f6ffa49cf412dffc0abc1c4fd0cc418de3b41bbc4b0b690571e6bcfc3")

    def test_04_source_sha_and_ptolemy_persistence(self):
        self.assertEqual(self.before["source_sha256"],self.after["source_sha256"])
        self.assertEqual(self.before["ptolemy_registry"],self.after["ptolemy_registry"])
        self.assertEqual(self.rec["Ptolemy_retained"],1066)

    def test_05_distinct_Chinese_V7_unmodified(self):
        self.assertEqual(digest(CHINA),digest(B/"recovery/CHINESE_V7_BEFORE_B07be.json"))
        self.assertEqual(read(CHINA)["sum_source_annotations"],355)
        self.assertEqual(self.rec["Chinese_V9_distinct_accepted_branch"],430)

    def test_06_ordered_source_chapters_182_no_repeated_marriage(self):
        self.assertEqual(self.before["read_numbered_chapters"],list(range(1,182)))
        self.assertEqual(self.after["read_numbered_chapters"],list(range(1,183)))
        self.assertEqual(self.after["read_headed_units_count"],98)
        self.assertEqual(self.after["partial_numbered_chapters"],[])

    def test_07_original_children_chapter_one_folio_not_travels(self):
        last=self.after["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["printed_chapter"],"CLXXXII")
        self.assertEqual(last["children_substantive_original_folios"],[757])
        self.assertEqual(last["next_travels_source_heading_original_folio"],758)
        self.assertTrue(last["original_no_issue_negative_overridden_by_positive_children"])
        self.assertTrue(last["original_four_children_are_tentative_not_undisputed_final_count"])
        self.assertFalse(last["original_Astro_glyphs_complete_expert_critical_edition"])

    def test_08_next_original_travels_chapter_immutable_frontier(self):
        n=self.after["next"]
        self.assertEqual(n["chapter"],"CLXXXIII")
        self.assertEqual(n["pdf_page"],792)
        self.assertEqual(n["printed_page"],758)
        self.assertFalse(n["extracted"])
        self.assertEqual(self.rec["next_R"],"R13132")

    def test_09_original_source_SHA_30_nonduplicate_record_IDs(self):
        self.assertEqual(digest(B/"ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json"),
                         self.rec["original_source_notes_sha256"])
        self.assertEqual(digest(B/"RULES.json"),self.rec["original_rules_sha256"])
        self.assertEqual([r["id"] for r in self.src["records"]],
                         [f"R{i}" for i in range(13102,13132)])

    def test_10_cold_archival_package_source_SHA_and_tests(self):
        self.assertTrue(self.release["ZIP_CRC_verified"])
        self.assertTrue(self.release["exact_member_SHA256_and_bytes_verified"])
        self.assertEqual(self.release["source_member_count"],15)
        self.assertEqual(self.rec["portable_archive_sha256"],self.release["archive_SHA256"])
        self.assertEqual(self.rec["independent_cold_offline_tests"],14)

    def test_11_source_cannot_be_reinterpreted_medical_reproduction_proof(self):
        last=self.after["completed_original_source_units_with_uncertainty"][-1]
        self.assertTrue(last["real_merchant_children_count_birth_certificates_unverified"])
        self.assertTrue(last["medical_or_child_health_accuracy_unverified"])
        self.assertEqual(last["blind_real_human_predictive_tests"],0)
        self.assertEqual(last["runtime_astrological_promotions"],0)

    def test_12_previous_state_history_byte_exact_suffix(self):
        previous=(B/"recovery/CURRENT_BEFORE_B07be.md").read_text(encoding="utf-8")
        current=CURRENT.read_text(encoding="utf-8")
        self.assertTrue(current.endswith(previous))
        self.assertIn("13,131 Lilly",current.split(
            "## Previous accepted historical checkpoint retained",1)[0])
        self.assertTrue(LATEST.is_file())
        self.assertIn("CLXXXII",LATEST.read_text(encoding="utf-8"))

    def test_13_empirical_predictions_and_runtime_untouched(self):
        self.assertEqual(self.after["empirical_validations"],0)
        self.assertEqual(self.after["runtime_promotions"],0)
        self.assertEqual(self.rec["genuine_human_forecasts_validated"],0)
        self.assertEqual(self.rec["astrology_runtime_promotions"],0)

    def test_14_overall_combined_branch_counts_not_claimed_integrated(self):
        self.assertEqual(self.rec["Western_after"],13131+1066)
        self.assertEqual(self.rec["Chinese_V9_distinct_accepted_branch"],210+220)
        self.assertEqual(13131+1066+210+220,14627)

if __name__=="__main__":
    unittest.main()
