"""Post-admission 1647/1659 original Lilly CLXXXI Marriage immutable append tests.

These assert documentary intake and zero actual empirical predictions.
Older B07bc post-index tests deliberately require the OLD last chapter and
are only applicable to its frozen accepted branch, NOT this new source index.
"""
from __future__ import annotations
import json
from pathlib import Path
from hashlib import sha256
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bd_MARRIAGE.md"

def rd(p):
    return json.loads(p.read_text(encoding="utf-8"))

def sh(p):
    return sha256(p.read_bytes()).hexdigest()

class B07bdMarriageAppendAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=rd(B/"recovery/LILLY_INDEX_BEFORE_B07bd.json")
        cls.new=rd(INDEX)
        cls.src=rd(B/"ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json")
        cls.rule=rd(B/"RULES.json")
        cls.acc=rd(B/"ACCEPTANCE.json")
        cls.rec=rd(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.release=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_canonical_old_and_new_index_exact_count(self):
        self.assertEqual(self.old["records_count"],13044)
        self.assertEqual(self.new["records_count"],13101)
        self.assertEqual(len(self.src["all_source_records"]),57)
        self.assertEqual(sum(b["records_count"] for b in self.new["batches"]),13101)

    def test_02_append_only_old_historical_batches_untouched(self):
        self.assertEqual(self.new["batches"][:-1],self.old["batches"])
        self.assertEqual(self.new["batches"][-1]["id"],"B07bd")
        self.assertEqual(self.new["batches"][-1]["records_count"],57)
        self.assertEqual(self.new["batches"][-1]["sha256"],sh(B/"RULES.json"))

    def test_03_before_sha_was_recorded_by_guard(self):
        self.assertEqual(
            sh(B/"recovery/LILLY_INDEX_BEFORE_B07bd.json"),self.rec["old_index_sha256"])
        self.assertEqual(sh(INDEX),self.rec["new_index_sha256"])
        self.assertEqual(self.rec["old_index_sha256"],
                         "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8")

    def test_04_preserved_source_root_and_Ptolemy(self):
        self.assertEqual(self.old["source_sha256"],self.new["source_sha256"])
        self.assertEqual(self.old["ptolemy_registry"],self.new["ptolemy_registry"])
        self.assertEqual(self.old["source_id"],self.new["source_id"])
        self.assertEqual(self.rec["Ptolemy_retained"],1066)

    def test_05_chinese_V7_original_bytes_unchanged(self):
        self.assertEqual(sh(CHINA),sh(B/"recovery/CHINESE_V7_BEFORE_B07bd.json"))
        self.assertEqual(sh(CHINA),self.rec["Chinese_V7_sha256"])
        self.assertEqual(rd(CHINA)["sum_source_annotations"],355)

    def test_06_181_original_numbered_units_without_accidental_repeat(self):
        self.assertEqual(self.old["read_numbered_chapters"],list(range(1,181)))
        self.assertEqual(self.new["read_numbered_chapters"],list(range(1,182)))
        self.assertEqual(self.new["partial_numbered_chapters"],[])
        self.assertEqual((self.old["read_headed_units_count"],self.new["read_headed_units_count"]),
                         (96,97))

    def test_07_original_marriage_4_physical_folios_and_children_divider(self):
        last=self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["printed_chapter"],"CLXXXI")
        self.assertEqual(last["printed_folios"],[754,755,756,757])
        self.assertTrue(last["physical_source_span_covered"])
        self.assertFalse(last["verified_real_merchant_marital_history"])
        self.assertTrue(last["original_marriage_predictions_known_to_author_and_not_blind"])

    def test_08_next_child_chapter_is_not_prematurely_counted(self):
        n=self.new["next"]
        self.assertEqual(n["chapter"],"CLXXXII")
        self.assertEqual(n["pdf_page"],791)
        self.assertEqual(n["printed_page"],757)
        self.assertFalse(n["extracted"])
        self.assertTrue(n["boundary_image_read"])
        self.assertEqual(self.rec["next_R"],"R13102")

    def test_09_original_marriage_57_source_note_SHA_frozen(self):
        self.assertEqual(sh(B/"ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json"),
                         self.rec["source_notes_sha256"])
        self.assertEqual(sh(B/"RULES.json"),self.rec["rules_sha256"])
        self.assertEqual(self.src["all_source_records"],self.rule["rules"])
        self.assertEqual([r["id"] for r in self.rule["rules"]],
                         [f"R{i}" for i in range(13045,13102)])

    def test_10_independently_extracted_19_tests_portable_archive_SHA(self):
        self.assertEqual(self.rec["portable_offline_tests_passed"],17)
        self.assertEqual(self.rec["portable_optional_swieph_skipped"],2)
        self.assertEqual(self.release["independently_extracted_standalone_original_tests_executed"],19)
        self.assertEqual(self.release["ZIP_member_count"],26)
        self.assertTrue(self.release["ZIP_CRC_verified"])
        self.assertTrue(self.release["member_SHA256_and_bytes_verified"])
        self.assertEqual(self.release["archive_sha256"],self.rec["archive_sha256"])

    def test_11_original_cazimi_discrepancy_not_taken_as_verified_wedding_history(self):
        last=self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertTrue(last["original_venus_cazimi_at_17arcmin_source"])
        self.assertTrue(last["modern_Sun_Venus_separation_far_beyond_17arcmin_under_hypothetical_UT"])
        self.assertFalse(last["original_meridian_historical_UT_and_birthplace_verified"])
        self.assertFalse(last["verified_real_merchant_marital_history"])

    def test_12_no_human_predictions_or_runtime_promotions(self):
        self.assertEqual(self.new["empirical_validations"],0)
        self.assertEqual(self.new["runtime_promotions"],0)
        self.assertEqual(self.rec["real_human_predictive_validations"],0)
        self.assertEqual(self.rec["runtime_astrological_promotions"],0)
        self.assertEqual(self.src["independent_prospective_human_predictive_tests"],0)

    def test_13_current_state_prepended_without_old_text_loss(self):
        old=(B/"recovery/CURRENT_BEFORE_B07bd.md").read_text(encoding="utf-8")
        cur=CURR.read_text(encoding="utf-8")
        self.assertTrue(cur.endswith(old))
        new=cur.split("## Previous accepted historical checkpoint retained",1)[0]
        self.assertIn("13,101 Lilly",new)
        self.assertIn("R13102",new)
        self.assertIn("CLXXXII",new)
        self.assertTrue(LATEST.is_file())
        self.assertIn("Cazimi",LATEST.read_text())

    def test_14_chinese_v9_count_separate_not_silently_merged(self):
        self.assertEqual(self.rec["separate_Chinese_V7_retained"],355)
        self.assertEqual(self.rec["separate_Chinese_V9_source_total_in_other_branch"],430)
        self.assertEqual(self.new["records_count"]+self.rec["Ptolemy_retained"],14167)
        self.assertEqual(14167+430,14597)

if __name__=="__main__":
    unittest.main()
