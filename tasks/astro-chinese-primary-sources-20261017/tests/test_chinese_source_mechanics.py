"""Source-only Chinese astrology mechanical tests and research provenance guards."""

import json
import sys
import unittest
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "bazi"))
sys.path.insert(0, str(B / "ziwei"))
import bazi_source_mechanics as bz  # noqa: E402
import ziwei_source_mechanics as zw  # noqa: E402


class ChineseSourceDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((B / "SOURCE_MANIFEST_V1.json").read_text())
        cls.bz = json.loads((B / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json").read_text())
        cls.zw = json.loads((B / "ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json").read_text())

    def test_01_manifest_with_original_book_hashes(self):
        sources = {x["id"]: x for x in self.manifest["sources"]}
        self.assertEqual(len(sources), 7)
        self.assertEqual(
            sources["BZI-S01"]["sha256"],
            "8b40261a8fb4eeacadb19381c91e91208aa3a9de66685407868b2691afb1a6a2",
        )
        self.assertEqual(
            sources["BZI-S02"]["sha256"],
            "9d29d83c94b67b1c887d6a2935ee8361e821bb6216487f9fe86b444a48489e81",
        )

    def test_02_source_first_bazi_no_missing_frozen_ids(self):
        r = self.bz["records"]
        self.assertEqual(self.bz["count"], len(r))
        self.assertEqual([x["id"] for x in r], [f"BZI-R{n:04d}" for n in range(1, len(r) + 1)])
        self.assertGreaterEqual(len(r), 40)

    def test_03_source_first_ziwei_no_missing_frozen_ids(self):
        r = self.zw["records"]
        self.assertEqual(self.zw["count"], len(r))
        self.assertEqual([x["id"] for x in r], [f"ZWD-R{n:04d}" for n in range(1, len(r) + 1)])
        self.assertGreaterEqual(len(r), 20)

    def test_04_every_claim_source_link_and_uncertainty(self):
        source_ids = {x["id"] for x in self.manifest["sources"]}
        for r in self.bz["records"]:
            self.assertIn(r["source"], source_ids)
            self.assertTrue(r["locator"])
            self.assertTrue(r["precondition_or_input"])
            self.assertTrue(r["qualification_or_counterexample"])
            self.assertEqual(r["rule_status"], "SOURCE_ONLY_DOCUMENTED")
            self.assertFalse(r["runtime_promoted"])
        for r in self.zw["records"]:
            self.assertIn(r["source"], source_ids)
            self.assertTrue(r["locator"])
            self.assertTrue(r["original_url"].startswith("https://zh.wikisource.org/"))
            self.assertTrue(r["uncertainty_or_exception"])
            self.assertFalse(r["runtime_promoted"])

    def test_05_no_human_validation_in_all_sources(self):
        self.assertEqual(self.manifest["authoring_contract"]["actual_predictions_verified"], 0)
        self.assertEqual(self.manifest["authoring_contract"]["runtime_promotions"], 0)
        self.assertTrue(
            all(not r["independent_human_accuracy_validated"] for r in self.bz["records"])
        )
        self.assertTrue(
            all(not r["independent_human_prediction_validated"] for r in self.zw["records"])
        )
        self.assertEqual(self.zw["real_human_prediction_validations"], 0)

    def test_06_ziwei_variants_unresolved_never_automatically_selected(self):
        self.assertEqual(len(self.zw["method_variants_not_yet_resolved"]), 5)
        self.assertTrue(
            all(x["chosen"] is None for x in self.zw["method_variants_not_yet_resolved"])
        )

    def test_07_book_publication_differentiated_from_epub(self):
        s = {x["id"]: x for x in self.manifest["sources"]}["BZI-S02"]
        self.assertEqual(s["first_edition_printed"], "2006")
        self.assertTrue(s["epub_metadata_date"].startswith("2018"))

    def test_37_canonical_chinese_index_separate_ids(self):
        index = json.loads((B / "CHINESE_SOURCE_AUDIT_INDEX_V1.json").read_text())
        self.assertEqual(index["sum_source_annotations"], 72)
        self.assertEqual(index["systems"][0]["accepted_source_annotations"], 46)
        self.assertEqual(index["systems"][1]["accepted_source_annotations"], 26)
        self.assertEqual(index["systems"][0]["next_id"], "BZI-R0047")
        self.assertEqual(index["systems"][1]["next_id"], "ZWD-R0027")

    def test_38_no_forecast_model_promotion_in_canonical_index(self):
        index = json.loads((B / "CHINESE_SOURCE_AUDIT_INDEX_V1.json").read_text())
        self.assertEqual(index["independently_validated_real_human_claims"], 0)
        self.assertEqual(index["runtime_promotions"], 0)
        self.assertTrue(all(not s["complete_birth_chart_engine"] for s in index["systems"]))

    def test_08_public_domain_chinese_and_owner_ebook_not_copied(self):
        bad = list(B.rglob("*.epub")) + list(B.rglob("*.pdf"))
        self.assertEqual(bad, [])


class BaziBoundedMechanics(unittest.TestCase):
    def test_09_ten_stems_and_twelve_branches(self):
        self.assertEqual(len(set(bz.STEMS)), 10)
        self.assertEqual(len(set(bz.BRANCHES)), 12)

    def test_10_stem_phase_and_polarity(self):
        self.assertEqual(bz.PHASE_BY_STEM["Jia"], "Wood")
        self.assertEqual(bz.PHASE_BY_STEM["Gui"], "Water")
        self.assertEqual(bz.heavenly_stem_polarity("Jia"), "Yang")
        self.assertEqual(bz.heavenly_stem_polarity("Ding"), "Yin")

    def test_11_hour_branches_exact_clock_boundaries(self):
        self.assertEqual(bz.two_hour_branch(23, 59), "Zi")
        self.assertEqual(bz.two_hour_branch(0, 59), "Zi")
        self.assertEqual(bz.two_hour_branch(1, 0), "Chou")
        self.assertEqual(bz.two_hour_branch(7, 30), "Chen")
        self.assertEqual(bz.two_hour_branch(8, 59), "Chen")
        self.assertEqual(bz.two_hour_branch(16, 30), "Shen")

    def test_12_hours_invalid_fail_closed(self):
        for v in (-1, 24):
            with self.assertRaises(ValueError):
                bz.two_hour_branch(v)
        with self.assertRaises(ValueError):
            bz.two_hour_branch(12, 60)

    def test_13_worked_1967_day_stem_to_hour(self):
        self.assertEqual(bz.hour_pillar_from_day_stem("Yi", 16, 30), ("Jia", "Shen"))

    def test_14_worked_1956_day_stem_to_hour(self):
        self.assertEqual(bz.hour_pillar_from_day_stem("Ren", 9, 30), ("Yi", "Si"))

    def test_15_worked_1940_late_rat_is_not_early_rat(self):
        self.assertEqual(bz.hour_pillar_from_day_stem("Xin", 23, 58), ("Geng", "Zi"))
        self.assertEqual(bz.hour_pillar_from_day_stem("Xin", 0, 58), ("Wu", "Zi"))

    def test_16_late_zi_variant_must_not_be_guessed(self):
        with self.assertRaises(ValueError):
            bz.hour_pillar_from_day_stem("Xin", 23, late_zi_policy="other_school_23_day_start")

    def test_17_forward_reverse_year_sex_convention(self):
        self.assertEqual(bz.traditional_luck_direction("Jia", "M"), "forward")
        self.assertEqual(bz.traditional_luck_direction("Jia", "F"), "reverse")
        self.assertEqual(bz.traditional_luck_direction("Ding", "M"), "reverse")
        self.assertEqual(bz.traditional_luck_direction("Ding", "F"), "forward")
        with self.assertRaises(ValueError):
            bz.traditional_luck_direction("Jia", "unknown")

    def test_18_luck_pillar_2004_book_example(self):
        self.assertEqual(bz.next_luck_pillar("Ji", "Si", "forward", 1), ("Geng", "Wu"))
        self.assertEqual(bz.next_luck_pillar("Ji", "Si", "forward", 2), ("Xin", "Wei"))

    def test_19_luck_pillar_reverse_steps(self):
        self.assertEqual(bz.next_luck_pillar("Xin", "Mao", "reverse", 1), ("Geng", "Yin"))
        self.assertEqual(bz.next_luck_pillar("Xin", "Mao", "reverse", 2), ("Ji", "Chou"))

    def test_20_nearest_solar_term_days_to_year_luck_age(self):
        self.assertEqual(
            [bz.decade_luck_start_age(v) for v in (22, 25, 5, 1)],
            [7, 8, 2, 0],
        )

    def test_21_age_range_bad_input(self):
        with self.assertRaises(ValueError):
            bz.decade_luck_start_age(-1)

    def test_22_five_factor_relative_to_day_master(self):
        expected = {
            "Wood": "Companion",
            "Fire": "Output",
            "Earth": "Wealth",
            "Metal": "Influence",
            "Water": "Resource",
        }
        self.assertEqual({p: bz.five_factor("Jia", p) for p in bz.PHASES}, expected)

    def test_23_four_three_harmony_triplets(self):
        self.assertEqual(bz.san_he_complete("Zi", "Shen", "Chen"), "Water")
        self.assertEqual(bz.san_he_complete("Hai", "Mao", "Wei"), "Wood")
        self.assertEqual(bz.san_he_complete("Yin", "Wu", "Xu"), "Fire")
        self.assertEqual(bz.san_he_complete("Si", "You", "Chou"), "Metal")

    def test_24_no_half_combination_counted_as_full(self):
        self.assertIsNone(bz.san_he_complete("Hai", "Mao"))
        self.assertIsNone(bz.san_he_complete("Hai", "Wei"))

    def test_25_directional_triplet_distinct_from_san_he(self):
        self.assertEqual(bz.san_hui_complete("Yin", "Mao", "Chen"), "Spring")
        self.assertEqual(bz.san_hui_complete("Hai", "Zi", "Chou"), "Winter")
        self.assertIsNone(bz.san_hui_complete("Shen", "Zi", "Chen"))

    def test_26_clear_nonexecuted_calendar_and_natal_prediction_scope(self):
        self.assertFalse(bz.ENGINE_SCOPE["birth_year_month_day_conversion"])
        self.assertFalse(bz.ENGINE_SCOPE["exact_solar_terms"])
        self.assertFalse(bz.ENGINE_SCOPE["fortune_prediction"])
        self.assertEqual(bz.ENGINE_SCOPE["validated_human_predictions"], 0)


class ZiweiBoundedMechanics(unittest.TestCase):
    def test_27_source_year_stem_start_table(self):
        expected = {
            "Jia": "Bing",
            "Ji": "Bing",
            "Yi": "Wu",
            "Geng": "Wu",
            "Bing": "Geng",
            "Xin": "Geng",
            "Ding": "Ren",
            "Ren": "Ren",
            "Wu": "Jia",
            "Gui": "Jia",
        }
        self.assertEqual(zw.YEAR_PAIR_FIRST_YIN_STEM, expected)

    def test_28_first_lunar_month_zi_hour_same_yin_palace(self):
        self.assertEqual(zw.life_and_body_palaces(1, "Zi"), ("Yin", "Yin"))

    def test_29_first_month_chou_hour_mirrored(self):
        self.assertEqual(zw.life_and_body_palaces(1, "Chou"), ("Chou", "Mao"))

    def test_30_first_month_yin_hour_mirrored(self):
        self.assertEqual(zw.life_and_body_palaces(1, "Yin"), ("Zi", "Chen"))

    def test_31_second_month_zi_hour_both_at_mao(self):
        self.assertEqual(zw.life_and_body_palaces(2, "Zi"), ("Mao", "Mao"))

    def test_32_classic_lunar_leap_month_convention_requires_explicit_selection(self):
        self.assertEqual(
            zw.life_and_body_palaces(1, "Zi", is_leap_month=True),
            ("Mao", "Mao"),
        )
        with self.assertRaises(ValueError):
            zw.life_and_body_palaces(1, "Zi", leap_rule="split-at-15")

    def test_33_palace_stems_start_at_yin(self):
        for stem, expected in (
            ("Jia", "Bing"),
            ("Yi", "Wu"),
            ("Bing", "Geng"),
            ("Ding", "Ren"),
            ("Wu", "Jia"),
        ):
            self.assertEqual(zw.palace_stem_from_yin(stem, "Yin"), expected)

    def test_34_year_stem_cycle_across_lunar_palaces(self):
        self.assertEqual(zw.palace_stem_from_yin("Jia", "Mao"), "Ding")
        self.assertEqual(zw.palace_stem_from_yin("Jia", "Chen"), "Wu")

    def test_35_there_are_12_distinct_old_palaces(self):
        self.assertEqual(len(zw.TWELVE_PALACES_OLD_LABELS), 12)
        self.assertEqual(zw.TWELVE_PALACES_OLD_LABELS[2], "Wives/Concubines")
        self.assertEqual(zw.TWELVE_PALACES_OLD_LABELS[3], "Children")

    def test_36_ziwei_not_a_bazi_relabel(self):
        self.assertFalse(zw.ENGINE_SCOPE["gregorian_to_lunar_conversion"])
        self.assertFalse(zw.ENGINE_SCOPE["complete_star_placement"])
        self.assertFalse(zw.ENGINE_SCOPE["four_transformations"])
        self.assertEqual(zw.ENGINE_SCOPE["independent_human_validations"], 0)


if __name__ == "__main__":
    unittest.main()
