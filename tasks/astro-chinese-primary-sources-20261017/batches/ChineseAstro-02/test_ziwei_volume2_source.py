"""Offline original-source witness and independent bounded placement tests."""

import hashlib
import json
import sys
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parents[1]
sys.path.insert(0, str(P / "ziwei"))
import quan_shu_vol2_placements as zw  # noqa: E402


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


class TextWitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.part = load(B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json")
        cls.witness = load(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")

    def test_witness_pinned(self):
        self.assertEqual(self.part["wikisource_revision_id"], 1963110)
        self.assertEqual(self.witness["wikisource_revision_id"], 1963110)
        self.assertEqual(self.part["raw_source_sha256"], self.witness["wikitext_sha256"])
        self.assertEqual(self.witness["wikitext_bytes"], 106736)
        self.assertEqual(self.witness["unmatched"], [])

    def test_source_split_not_conflated(self):
        self.assertEqual(self.part["count"], 25)
        self.assertEqual(self.part["next_id"], "ZWD-R0052")
        base = load(P / "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json")
        self.assertEqual(len(base["records"]), 26)
        self.assertEqual(base["records"][-1]["id"], "ZWD-R0026")
        self.assertEqual(
            [r["id"] for r in self.part["records"]], [f"ZWD-R{n:04d}" for n in range(27, 52)]
        )
        self.assertEqual(
            set(x["id"] for x in base["records"]) & set(x["id"] for x in self.part["records"]),
            set(),
        )

    def test_source_anchor_verified_and_not_prediction(self):
        for row in self.part["records"]:
            self.assertTrue(row["original_revision_quote_match_confirmed"])
            self.assertFalse(row["independently_validated_real_person_accuracy"])
            self.assertFalse(row["runtime_promoted"])
            self.assertFalse(row["full_chart_engine_verified"])
            self.assertTrue(row["historical_source_meaning"])
            self.assertTrue(row["uncertainty_or_exception"])
            self.assertTrue(row["source_precondition"])
            self.assertEqual(row["rule_status"], "SOURCE_ONLY_DOCUMENTED")
        self.assertFalse(self.part["source_complete_line_collation"])
        self.assertEqual(self.witness["accepted_quote_count"], 25)

    def test_no_sensitive_or_model_promotion(self):
        self.assertEqual(self.part["independent_human_prediction_validations"], 0)
        self.assertEqual(self.part["runtime_promotions"], 0)
        self.assertFalse(self.witness["independent_expert_translation_validation"])
        self.assertFalse(self.witness["human_astrological_validation"])

    def test_legacy_bazi_not_rewritten(self):
        bz = load(P / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json")
        self.assertEqual((bz["count"], bz["records"][-1]["id"]), (46, "BZI-R0046"))

    def test_method_fail_closed(self):
        status = zw.declared_method_status()
        self.assertEqual(status["source_revision"], 1963110)
        self.assertFalse(status["complete_birth_chart_engine"])
        self.assertFalse(status["leap_lunar_month_variant_resolved"])
        self.assertFalse(status["individual_human_prediction_validated"])

    def test_all_chinese_anchors_have_proper_provenance(self):
        for row in self.part["records"]:
            self.assertTrue(row["locator"].startswith("卷二:"))
            self.assertTrue(row["original_chinese_anchor"])
            self.assertEqual(row["source"], "ZWDS-CLASSIC-01")
            self.assertEqual(row["source_revision_id"], 1963110)
            self.assertTrue(row["display_transliterated_traditional_anchor"])

    def test_no_publishing_copyright_bytes(self):
        self.assertEqual(list(P.rglob("*.epub")), [])
        self.assertEqual(list(P.rglob("*.pdf")), [])

    def test_index_v2_when_ready(self):
        path = P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json"
        self.assertTrue(path.is_file())
        index = load(path)
        self.assertEqual(index["sum_source_annotations"], 97)
        self.assertEqual(index["systems"][0]["accepted_source_annotations"], 46)
        self.assertEqual(index["systems"][1]["accepted_source_annotations"], 51)
        self.assertEqual(index["systems"][1]["next_id"], "ZWD-R0052")
        self.assertEqual(index["independently_validated_real_human_claims"], 0)

    def test_original_rules_protected(self):
        index = load(P / "CHINESE_SOURCE_AUDIT_INDEX_V1.json")
        self.assertEqual(index["sum_source_annotations"], 72)
        self.assertEqual(index["systems"][1]["accepted_source_annotations"], 26)
        self.assertEqual(index["systems"][1]["next_id"], "ZWD-R0027")

    def test_witness_hash_matches_accepted_index(self):
        index = load(P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json")
        accepted = index["accepted_batches"][-1]
        self.assertEqual(accepted["id"], "ChineseAstro-02")
        self.assertEqual(
            accepted["witness_sha256"],
            hashlib.sha256((B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json").read_bytes()).hexdigest(),
        )
        self.assertEqual(
            accepted["rules_sha256"],
            hashlib.sha256(
                (B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json").read_bytes()
            ).hexdigest(),
        )


class PlacementExamples(unittest.TestCase):
    def test_wenchang_and_wenqu_hour_two(self):
        self.assertEqual((zw.wen_chang("Zi"), zw.wen_qu("Zi")), ("Xu", "Chen"))
        self.assertEqual((zw.wen_chang("Chou"), zw.wen_qu("Chou")), ("You", "Si"))

    def test_hour_star_paths_12_separate(self):
        a = [zw.wen_chang(h) for h in zw.BRANCHES]
        b = [zw.wen_qu(h) for h in zw.BRANCHES]
        self.assertEqual(len(set(a)), 12)
        self.assertEqual(len(set(b)), 12)
        self.assertEqual(a[:3], ["Xu", "You", "Shen"])
        self.assertEqual(b[:3], ["Chen", "Si", "Wu"])

    def test_zuofu_youbi_month(self):
        self.assertEqual((zw.zuo_fu(1), zw.you_bi(1)), ("Chen", "Xu"))
        self.assertEqual((zw.zuo_fu(2), zw.you_bi(2)), ("Si", "You"))

    def test_no_implicit_leap_month(self):
        for m in (0, 13, -1, True, None, 1.5):
            with self.assertRaises(ValueError):
                zw.zuo_fu(m)

    def test_tianxing_tianyao(self):
        self.assertEqual((zw.tian_xing(1), zw.tian_yao(1)), ("You", "Chou"))
        self.assertEqual((zw.tian_xing(2), zw.tian_yao(2)), ("Xu", "Yin"))

    def test_dijie_tiankong_late_hour(self):
        self.assertEqual((zw.di_jie("Zi"), zw.tian_kong("Zi")), ("Hai", "Hai"))
        self.assertEqual((zw.di_jie("Chou"), zw.tian_kong("Chou")), ("Zi", "Xu"))
        self.assertEqual((zw.di_jie("Wu"), zw.tian_kong("Wu")), ("Si", "Si"))

    def test_lucun_all_stems(self):
        expected = ["Yin", "Mao", "Si", "Wu", "Si", "Wu", "Shen", "You", "Hai", "Zi"]
        self.assertEqual([zw.lu_cun(s) for s in zw.STEMS], expected)

    def test_lucun_adjacent_guigolden(self):
        self.assertEqual(zw.lu_cun("Gui"), "Zi")
        self.assertEqual(zw.qing_yang_and_tuo_luo("Gui"), ("Chou", "Hai"))

    def test_other_stems_symmetric(self):
        for stem in zw.STEMS:
            forward, backward = zw.qing_yang_and_tuo_luo(stem)
            self.assertEqual(forward, zw.move(zw.lu_cun(stem), 1))
            self.assertEqual(backward, zw.move(zw.lu_cun(stem), -1))

    def test_tianma_four_trines(self):
        self.assertEqual([zw.tian_ma(b) for b in ("Yin", "Wu", "Xu")], ["Shen"] * 3)
        self.assertEqual([zw.tian_ma(b) for b in ("Shen", "Zi", "Chen")], ["Yin"] * 3)
        self.assertEqual([zw.tian_ma(b) for b in ("Si", "You", "Chou")], ["Hai"] * 3)
        self.assertEqual([zw.tian_ma(b) for b in ("Hai", "Mao", "Wei")], ["Si"] * 3)

    def test_santai_bazuo_first_day(self):
        self.assertEqual((zw.san_tai(1, 1), zw.ba_zuo(1, 1)), ("Chen", "Xu"))
        self.assertEqual((zw.san_tai(2, 1), zw.ba_zuo(2, 1)), ("Si", "You"))

    def test_santai_bazuo_day_two(self):
        self.assertEqual((zw.san_tai(1, 2), zw.ba_zuo(1, 2)), ("Si", "You"))

    def test_bad_lunar_days(self):
        for day in (0, -1, 31, None, True, 3.14):
            with self.assertRaises(ValueError):
                zw.ba_zuo(1, day)

    def test_year_ku_xu(self):
        self.assertEqual((zw.tian_ku("Zi"), zw.tian_xu("Zi")), ("Wu", "Wu"))
        self.assertEqual((zw.tian_ku("Chou"), zw.tian_xu("Chou")), ("Si", "Wei"))

    def test_longchi(self):
        self.assertEqual(zw.long_chi("Zi"), "Chen")
        self.assertEqual(zw.long_chi("Chou"), "Si")

    def test_associates_illness_pieces_not_inferences(self):
        self.assertEqual(zw.natal_palace("Yin", "Life"), "Yin")
        self.assertEqual(zw.natal_palace("Yin", "Siblings"), "Chou")
        self.assertEqual(zw.tian_shang_and_tian_shi("Yin"), ("Wei", "You"))

    def test_4transform_jia_only(self):
        self.assertEqual(zw.jia_four_transformations(), ("LianZhen", "PoJun", "WuQu", "TaiYang"))

    def test_fail_closed_inputs(self):
        for fn in (zw.wen_chang, zw.tian_kong, zw.tian_ma, zw.tian_ku):
            with self.assertRaises(ValueError):
                fn("NoSuchBranch")
        with self.assertRaises(ValueError):
            zw.lu_cun("NoSuchStem")
        with self.assertRaises(ValueError):
            zw.natal_palace("Zi", "Danger")
        with self.assertRaises(ValueError):
            zw.move("Zi", True)


def add_anchor_test(i):
    def test(self):
        row = self.part["records"][i]
        self.assertEqual(row["id"], f"ZWD-R{27 + i:04d}")
        self.assertTrue(row["original_revision_quote_match_confirmed"])
        self.assertGreaterEqual(len(row["original_chinese_anchor"]), 3)

    return test


for i in range(25):
    setattr(TextWitness, f"test_original_chinese_anchor_{27 + i:04d}", add_anchor_test(i))


if __name__ == "__main__":
    unittest.main()
