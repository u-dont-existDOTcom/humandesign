"""B07bf post-append invariants after original first/second edition Travels."""
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/"tasks/astro-source-audit-multipass-20261005"
INDEX=TASK/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURR=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bf_TRAVELS.md"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return sha256(p.read_bytes()).hexdigest()

class PostIndexTravels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=rd(B/"recovery/LILLY_INDEX_BEFORE_B07bf.json")
        cls.after=rd(INDEX)
        cls.rec=rd(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.source=rd(B/"ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json")
        cls.release=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_61_record_append_to_13192(self):
        self.assertEqual(self.before["records_count"],13131)
        self.assertEqual(self.after["records_count"],13192)
        self.assertEqual(sum(b["records_count"] for b in self.after["batches"]),13192)
        self.assertEqual(self.after["batches"][-1]["records_count"],61)

    def test_02_parent_batch_exact_untouched(self):
        self.assertEqual(self.after["batches"][:-1],self.before["batches"])
        self.assertEqual(self.after["batches"][-1]["id"],"B07bf")
        self.assertEqual(self.after["batches"][-1]["sha256"],sha(B/"RULES.json"))

    def test_03_before_and_after_index_exact_hash(self):
        self.assertEqual(sha(B/"recovery/LILLY_INDEX_BEFORE_B07bf.json"),
                         self.rec["old_index_SHA256"])
        self.assertEqual(sha(INDEX),self.rec["new_index_SHA256"])
        self.assertEqual(self.rec["old_index_SHA256"],
                         "7212bd8aa75ff1ba5f6e30c0d21c55d60d9ac46101e7c8251035793ad587ff5c")

    def test_04_original_root_source_and_ptolemy_unchanged(self):
        self.assertEqual(self.before["source_sha256"],self.after["source_sha256"])
        self.assertEqual(self.before["ptolemy_registry"],self.after["ptolemy_registry"])
        self.assertEqual(self.rec["Ptolemy_retained"],1066)

    def test_05_original_chinese_source_sha_untouched(self):
        self.assertEqual(sha(CHINA),sha(B/"recovery/CHINESE_V7_BEFORE_B07bf.json"))
        self.assertEqual(self.rec["Chinese_V9_accepted_in_separate_branch"],430)
        self.assertEqual(self.rec["Chinese_V7_source_SHA256"],sha(CHINA))

    def test_06_printed_183_original_chapters_plus_distinct_184_next(self):
        self.assertEqual(self.before["read_numbered_chapters"],list(range(1,183)))
        self.assertEqual(self.after["read_numbered_chapters"],list(range(1,184)))
        self.assertEqual(self.after["read_headed_units_count"],99)
        self.assertEqual(self.after["partial_numbered_chapters"],[])
        self.assertEqual(self.after["next"]["chapter"],"CLXXXIIII")
        self.assertEqual(self.after["next"]["editorial_source_sequence_ordinal"],184)

    def test_07_original_travels_start_end_and_next_divider(self):
        last=self.after["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["printed_folios"],[758,759,760])
        self.assertEqual(last["historical_start"],"R13132")
        self.assertEqual(last["historical_end"],"R13192")
        self.assertEqual(last["next_chapter_printed_Roman"],"CLXXXIIII")
        self.assertEqual(self.after["next"]["printed_page"],760)
        self.assertEqual(self.after["next"]["pdf_page"],794)
        self.assertFalse(self.after["next"]["extracted"])

    def test_08_exact_source_and_RULES_SHA_and_all_ids(self):
        self.assertEqual(sha(B/"ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json"),
                         self.rec["original_source_SHA256"])
        self.assertEqual(sha(B/"RULES.json"),self.rec["original_rules_SHA256"])
        self.assertEqual([r["id"] for r in self.source["records"]],
                         [f"R{i}" for i in range(13132,13193)])

    def test_09_cold_zip_source_SHA_proof_not_unobserved_forecast(self):
        self.assertTrue(self.release["zip_CRC_verified"])
        self.assertTrue(self.release["all_portable_members_independently_SHA_checked"])
        self.assertEqual(self.release["fresh_cold_extraction_source_tests_green"],11)
        self.assertEqual(self.rec["portable_source_archive_SHA256"],
                         self.release["archive_sha256"])
        self.assertEqual(self.release["source_member_count"],20)

    def test_10_leakage_is_explicit_and_not_human_success(self):
        last=self.after["completed_original_source_units_with_uncertainty"][-1]
        self.assertTrue(last["author_past_voyages_already_disclosed_prior_to_rule_interpretation"])
        self.assertFalse(last["authentic_real_merchant_past_voyages_independently_verified"])
        self.assertEqual(last["actual_real_human_predictive_test_count"],0)
        self.assertEqual(self.after["empirical_validations"],0)
        self.assertEqual(self.after["runtime_promotions"],0)

    def test_11_current_state_contains_latest_and_old_text_exact(self):
        old=(B/"recovery/CURRENT_BEFORE_B07bf.md").read_text(encoding="utf-8")
        new=CURR.read_text(encoding="utf-8")
        self.assertTrue(new.endswith(old))
        title=new.split("## Previous accepted historical checkpoint retained",1)[0]
        self.assertIn("13,192 Lilly",title)
        self.assertIn("R13193",title)
        self.assertTrue(LATEST.is_file())
        self.assertIn("CLXXXIII",LATEST.read_text(encoding="utf-8"))

    def test_12_original_counts_are_historical_only_not_predictive_accuracies(self):
        self.assertEqual(self.rec["Lilly_after"],13192)
        self.assertEqual(self.rec["Western_after"],14258)
        self.assertEqual(14258+self.rec["Chinese_V9_accepted_in_separate_branch"],14688)
        self.assertEqual(self.rec["real_human_predictive_validations"],0)
        self.assertEqual(self.rec["astrological_rules_promoted"],0)

if __name__=="__main__":unittest.main()
