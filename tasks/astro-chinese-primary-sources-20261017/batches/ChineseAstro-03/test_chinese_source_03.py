"""Pinned raw Chinese section/quote integrity and bounded auxiliary placement tests."""

import hashlib
import json
import sys
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parents[1]
sys.path.insert(0, str(P / "ziwei"))
import quan_shu_vol2_aux_placements as aux  # noqa: E402
import quan_shu_vol2_placements as original  # noqa: E402


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class ChineseSource03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.note = j(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
        cls.witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
        cls.previous = j(P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json")
        cls.base = j(P / "batches/ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json")

    def test_pinned_exact_revision_source_witness(self):
        self.assertEqual(self.note["wikisource_revision_id"], 1963110)
        self.assertEqual(self.witness["pinned_wikisource_revision_id"], 1963110)
        self.assertEqual(self.note["raw_source_sha256"], self.witness["raw_source_sha256"])
        self.assertEqual(self.witness["raw_source_bytes"], 106736)
        self.assertEqual(self.witness["short_exact_chinese_anchor_matches"], 45)

    def test_no_existing_source_ids_repeated(self):
        self.assertEqual(self.previous["sum_source_annotations"], 97)
        self.assertEqual(self.previous["systems"][1]["accepted_source_annotations"], 51)
        self.assertEqual(self.previous["systems"][1]["next_id"], "ZWD-R0052")
        self.assertEqual(self.base["records"][-1]["id"], "ZWD-R0051")
        self.assertEqual(
            [r["id"] for r in self.note["records"]], [f"ZWD-R{x:04d}" for x in range(52, 97)]
        )
        self.assertEqual(self.note["next_id"], "ZWD-R0097")
        self.assertEqual(
            set(r["id"] for r in self.base["records"]) & set(r["id"] for r in self.note["records"]),
            set(),
        )

    def test_original_source_section_and_quote_hashes(self):
        for record, proof in zip(self.note["records"], self.witness["anchors"], strict=True):
            self.assertEqual(record["id"], proof["id"])
            self.assertEqual(record["original_chinese_anchor"], proof["original_chinese_anchor"])
            self.assertEqual(record["locator"].split(":", 1)[1], proof["original_source_section"])
            self.assertEqual(record["raw_revision_anchor_char_offset"], proof["anchor_char_offset"])
            self.assertEqual(
                record["raw_revision_anchor_utf8_sha256"],
                hashlib.sha256(record["original_chinese_anchor"].encode()).hexdigest(),
            )
            self.assertGreaterEqual(
                proof["anchor_char_offset"], proof["source_section_char_offset"]
            )

    def test_flagged_no_genuine_human_validation(self):
        for r in self.note["records"]:
            self.assertTrue(r["original_revision_quote_match_confirmed"])
            self.assertEqual(r["rule_status"], "SOURCE_ONLY_DOCUMENTED")
            self.assertFalse(r["independently_validated_real_person_accuracy"])
            self.assertFalse(r["runtime_promoted"])
            self.assertFalse(r["full_birth_calendar_engine_verified"])
            self.assertTrue(r["historical_source_meaning"])
            self.assertTrue(r["source_precondition"])
            self.assertTrue(r["uncertainty_or_exception"])

    def test_source_not_Ming_diplomatic_manuscript_claim(self):
        self.assertFalse(self.note["author_attribution_verified"])
        self.assertFalse(self.note["source_is_complete_original_diplomatic_edition"])
        self.assertFalse(self.witness["complete_chinese_edition_diplomatic_collation"])
        self.assertFalse(self.witness["independent_classical_Chinese_expert_translation_verified"])

    def test_chinese_CJK_not_converted_to_traditional_in_raw_anchor(self):
        self.assertTrue(any("诰" in r["locator"] for r in self.note["records"]))
        self.assertTrue(any("从" in r["original_chinese_anchor"] for r in self.note["records"]))
        self.assertEqual(self.note["count"], 45)

    def test_natal_not_current_taisui_rule_distinguished(self):
        kinds = {r["rule_or_section_type"] for r in self.note["records"]}
        self.assertIn("jieshen_natal", kinds)
        self.assertIn("tiande_annual", kinds)
        self.assertIn("yuede_annual", kinds)
        self.assertIn("doujun_month", kinds)
        self.assertIn("doujun_hour", kinds)

    def test_gender_old_text_not_modern_user_claim(self):
        status = aux.method_limits()
        self.assertFalse(status["historical_sex_coded_rules_are_modern_gender_claims"])
        self.assertFalse(status["natal_14_main_stars_full_layout_verified"])
        self.assertFalse(status["calendar_chinese_new_year_leap_month_verified"])
        self.assertFalse(status["birth_hour_late_zi_and_true_solar_time_resolved"])

    def test_original_fengge_separate_from_longchi(self):
        self.assertEqual(original.long_chi("Zi"), "Chen")
        self.assertEqual(aux.feng_ge("Zi"), "Xu")
        self.assertEqual(aux.feng_ge("Chou"), "You")

    def test_original_taifu_fenggao_independent_birth_hour(self):
        self.assertEqual(aux.tai_fu("Zi"), "Wu")
        self.assertEqual(aux.tai_fu("Chou"), "Wei")
        self.assertEqual(aux.feng_gao("Zi"), "Yin")
        self.assertEqual(aux.feng_gao("Chou"), "Mao")

    def test_taifu_fenggao_all_twelve_unique_positions(self):
        self.assertEqual(len(set(aux.tai_fu(b) for b in aux.BRANCHES)), 12)
        self.assertEqual(len(set(aux.feng_gao(b) for b in aux.BRANCHES)), 12)
        self.assertEqual(len(set(aux.feng_ge(b) for b in aux.BRANCHES)), 12)

    def test_hongluan_opposite_tianxi_all_years(self):
        for b in aux.BRANCHES:
            self.assertEqual(aux.tian_xi(b), aux.move(aux.hong_luan(b), 6))
        self.assertEqual(aux.hong_luan("Zi"), "Mao")
        self.assertEqual(aux.tian_xi("Zi"), "You")

    def test_changsheng_five_bureaux(self):
        self.assertEqual(
            {b: aux.changsheng(b, "ChangSheng", "male") for b in aux.BUREAU_BASE},
            {"fire": "Yin", "wood": "Hai", "water": "Shen", "metal": "Si", "earth": "Shen"},
        )

    def test_changsheng_source_gender_direction(self):
        self.assertEqual(aux.changsheng("fire", "MuYu", "male"), "Mao")
        self.assertEqual(aux.changsheng("fire", "MuYu", "female"), "Chou")
        self.assertEqual(len(aux.CHANGSHENG_STAGES), 12)

    def test_four_annual_stars_relation(self):
        for b in aux.BRANCHES:
            r = aux.annual_sang_diao_bai_guan(b)
            self.assertEqual(r["SangMen"], aux.move(b, 2))
            self.assertEqual(r["DiaoKe"], aux.move(b, -2))
            self.assertEqual(r["BaiHu"], aux.move(r["SangMen"], 6))
            self.assertEqual(r["GuanFu"], aux.move(r["DiaoKe"], 6))

    def test_doujun_two_stages_not_shortcut(self):
        self.assertEqual(aux.dou_jun("Zi", 1, "Zi"), "Zi")
        self.assertEqual(aux.dou_jun("Zi", 2, "Zi"), "Hai")
        self.assertEqual(aux.dou_jun("Zi", 2, "Chou"), "Zi")
        self.assertEqual(aux.dou_jun("Mao", 2, "Zi"), "Yin")

    def test_year_natal_vs_annual_deity_starts(self):
        self.assertEqual(aux.tian_de("Zi"), "You")
        self.assertEqual(aux.yue_de("Zi"), "Zi")
        self.assertEqual(aux.jie_shen("Zi"), "Xu")
        self.assertEqual(aux.tian_de("Chou"), "Xu")
        self.assertEqual(aux.jie_shen("Chou"), "You")

    def test_jie_lu_five_two_stem_pairs(self):
        self.assertEqual(len(aux.JIE_LU_KONG), 10)
        self.assertEqual(aux.jie_lu_kong("Jia"), aux.jie_lu_kong("Ji"))
        self.assertEqual(aux.jie_lu_kong("Jia"), ("Shen", "You"))
        self.assertEqual(aux.jie_lu_kong("Wu"), ("Zi", "Chou"))
        self.assertEqual(aux.jie_lu_kong("Gui"), ("Zi", "Chou"))

    def test_xun_all_six_sets(self):
        self.assertEqual(aux.xun_kong("Zi"), ("Xu", "Hai"))
        self.assertEqual(aux.xun_kong("Yin"), ("Zi", "Chou"))
        self.assertEqual(aux.xun_kong("Chen"), ("Yin", "Mao"))
        self.assertEqual(aux.xun_kong("Wu"), ("Chen", "Si"))
        self.assertEqual(aux.xun_kong("Shen"), ("Wu", "Wei"))
        self.assertEqual(aux.xun_kong("Xu"), ("Shen", "You"))

    def test_xiaoxian_four_birth_year_trines(self):
        self.assertEqual(len(aux.XIAO_XIAN_START), 12)
        for t, start in (
            (("Yin", "Wu", "Xu"), "Chen"),
            (("Shen", "Zi", "Chen"), "Xu"),
            (("Si", "You", "Chou"), "Wei"),
            (("Hai", "Mao", "Wei"), "Chou"),
        ):
            self.assertEqual([aux.xiao_xian_start(b) for b in t], [start] * 3)

    def test_xun_does_not_accept_arbitrary_branch(self):
        with self.assertRaises(ValueError):
            aux.xun_kong("Chou")
        with self.assertRaises(ValueError):
            aux.xun_kong("Hai")

    def test_fail_closed_calendar_inputs(self):
        for bad in (0, 13, True, None, 1.5):
            with self.assertRaises(ValueError):
                aux.dou_jun("Zi", bad, "Zi")
        with self.assertRaises(ValueError):
            aux.dou_jun("Zi", 1, "SOME_INVALID")
        with self.assertRaises(ValueError):
            aux.changsheng("fire", "Unrecognized", "male")
        with self.assertRaises(ValueError):
            aux.changsheng("light", "ChangSheng", "male")
        with self.assertRaises(ValueError):
            aux.changsheng("fire", "MuYu", "nonbinary")

    def test_independent_zero_validation(self):
        self.assertEqual(self.note["independent_human_prediction_validations"], 0)
        self.assertEqual(self.note["runtime_promotions"], 0)
        self.assertEqual(aux.method_limits()["runtime_prediction_promotions"], 0)


def make_quoted_anchor_test(i):
    def test(self):
        row = self.note["records"][i]
        proof = self.witness["anchors"][i]
        self.assertEqual(row["id"], f"ZWD-R{i + 52:04d}")
        self.assertEqual(row["original_chinese_anchor"], proof["original_chinese_anchor"])
        self.assertGreaterEqual(len(row["original_chinese_anchor"]), 5)
        self.assertTrue(row["original_revision_quote_match_confirmed"])
        self.assertFalse(row["runtime_promoted"])

    return test


for n in range(45):
    setattr(ChineseSource03, f"test_source_anchor_{n + 52:04d}", make_quoted_anchor_test(n))


if __name__ == "__main__":
    unittest.main()
