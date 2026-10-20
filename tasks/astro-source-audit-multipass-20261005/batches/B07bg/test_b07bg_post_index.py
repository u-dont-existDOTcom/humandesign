"""Original Lilly Honours chapter post source admission, no actual personal tests."""
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-source-audit-multipass-20261005"
INDEX=T/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bg_HONOURS.md"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def h(p):return sha256(p.read_bytes()).hexdigest()

class HonoursAppendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=rd(B/"recovery/LILLY_INDEX_BEFORE_B07bg.json")
        cls.new=rd(INDEX)
        cls.rec=rd(B/"CANONICAL_PREPARE_RECEIPT_20261020.json")
        cls.src=rd(B/"ORIGINAL_1647_1659_HONOURS_SOURCE_V1.json")
        cls.arc=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")

    def test_01_before_after_44_source_notes(self):
        self.assertEqual(self.old["records_count"],13192)
        self.assertEqual(self.new["records_count"],13236)
        self.assertEqual(sum(b["records_count"] for b in self.new["batches"]),13236)
        self.assertEqual(self.new["batches"][-1]["records_count"],44)

    def test_02_all_prior_batch_original_source_data_untouched(self):
        self.assertEqual(self.new["batches"][:-1],self.old["batches"])
        self.assertEqual(self.new["batches"][-1]["id"],"B07bg")
        self.assertEqual(self.new["batches"][-1]["sha256"],h(B/"RULES.json"))

    def test_03_frozen_before_after_original_index_byte_sha(self):
        self.assertEqual(h(B/"recovery/LILLY_INDEX_BEFORE_B07bg.json"),
                         self.rec["old_index_sha256"])
        self.assertEqual(h(INDEX),self.rec["new_index_sha256"])
        self.assertEqual(self.rec["old_index_sha256"],
                         "2bdb66cdf622a1442088b98bcad46376a936520f5d077e00a67688287cf9cba2")

    def test_04_ptolemy_and_root_original_1647_identity_unchanged(self):
        self.assertEqual(self.old["source_id"],self.new["source_id"])
        self.assertEqual(self.old["source_sha256"],self.new["source_sha256"])
        self.assertEqual(self.old["ptolemy_registry"],self.new["ptolemy_registry"])
        self.assertEqual(self.rec["Ptolemy_retained"],1066)

    def test_05_chinese_v7_original_sha_unchanged(self):
        self.assertEqual(h(CHINA),h(B/"recovery/CHINESE_V7_BEFORE_B07bg.json"))
        self.assertEqual(self.rec["Chinese_V7_sha256"],h(CHINA))
        self.assertEqual(self.rec["Chinese_V9_distinct_accepted_lane"],430)

    def test_06_printed_honours_184_and_source_next_literal_183(self):
        last=self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertEqual(last["printed_chapter"],"CLXXXIIII")
        self.assertEqual(last["editorial_ordinal"],184)
        self.assertEqual(last["printed_folios"],[760,761,762])
        self.assertTrue(last["printed_next_Friends_Roman_CLXXXIII_regresses_to_earlier_Travels_label"])
        self.assertEqual(self.new["read_numbered_chapters"],list(range(1,185)))
        self.assertEqual(self.new["read_headed_units_count"],100)

    def test_07_next_friends_source_not_prematurely_counted(self):
        n=self.new["next"]
        self.assertEqual(n["chapter"],"CLXXXIII")
        self.assertEqual(n["printed_page"],762)
        self.assertEqual(n["pdf_page"],796)
        self.assertEqual(n["editorial_source_sequence_ordinal"],185)
        self.assertFalse(n["extracted"])
        self.assertEqual(self.rec["next_R"],"R13237")

    def test_08_exact_original_source_and_rules_sha_44_ids(self):
        self.assertEqual(h(B/"ORIGINAL_1647_1659_HONOURS_SOURCE_V1.json"),
                         self.rec["original_source_notes_sha256"])
        self.assertEqual(h(B/"RULES.json"),self.rec["original_rules_sha256"])
        self.assertEqual([r["id"] for r in self.src["records"]],
                         [f"R{i}" for i in range(13193,13237)])

    def test_09_archive_cold_replay_record_no_external_prediction_claim(self):
        self.assertTrue(self.arc["zip_CRC_check_passed"])
        self.assertTrue(self.arc["all_members_exact_SHA_and_bytes_check_passed"])
        self.assertEqual(self.arc["independent_cold_source_tests_green"],13)
        self.assertEqual(self.arc["member_count"],22)
        self.assertEqual(self.rec["portable_source_archive_sha256"],
                         self.arc["archive_sha256"])

    def test_10_cazimi_repeated_input_not_independent_case(self):
        last=self.new["completed_original_source_units_with_uncertainty"][-1]
        self.assertTrue(last["original_birth_Sun_Venus_Cazimi_reused_from_prior_marriage"])
        self.assertFalse(last["source_epoch_birth_UT_and_cazimi_independent_astronomy_verified"])
        self.assertFalse(last["actual_known_merchant_occupation_reputation_verified"])

    def test_11_current_state_source_chain_preserved(self):
        before=(B/"recovery/CURRENT_BEFORE_B07bg.md").read_text(encoding="utf-8")
        now=CURRENT.read_text(encoding="utf-8")
        self.assertTrue(now.endswith(before))
        title=now.split("## Previous accepted historical checkpoint retained",1)[0]
        self.assertIn("13,236 Lilly",title)
        self.assertIn("R13237",title)
        self.assertTrue(LATEST.is_file())

    def test_12_zero_real_human_predictive_results_and_model_promotions(self):
        self.assertEqual(self.new["empirical_validations"],0)
        self.assertEqual(self.new["runtime_promotions"],0)
        self.assertEqual(self.rec["human_blind_predictive_validation_count"],0)
        self.assertEqual(self.rec["runtime_astrological_promotions"],0)
        self.assertEqual(self.rec["Western_after"],14302)
        self.assertEqual(14302+430,14732)

if __name__=="__main__":unittest.main()
