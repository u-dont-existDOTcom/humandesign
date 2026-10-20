"""All 14 original-principal-star family positions and a modern external example."""

from pathlib import Path
import sys
import unittest
from collections import Counter
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "ziwei"))
import quan_shu_fourteen_stars as stars  # noqa: E402
import ziwei_source_mechanics as z  # noqa: E402


class OriginalFourteenPrincipalStars(unittest.TestCase):
    def test_01_exact_original_couplet_still_matches_source_sha(self):
        stars._verify_original_verse()
        with patch.object(stars, "SOURCE_SHA256", "0" * 64):
            with self.assertRaisesRegex(ValueError, "source changed"):
                stars._verify_original_verse()

    def test_02_six_reverse_eight_forward_full_name_set(self):
        self.assertEqual(len(stars.PURPLE_FAMILY_STEPS), 6)
        self.assertEqual(len(stars.FU_FAMILY_STEPS), 8)
        self.assertEqual(set(stars.PURPLE_FAMILY_STEPS) & set(stars.FU_FAMILY_STEPS), set())
        self.assertEqual(tuple(stars.PURPLE_FAMILY_STEPS.values()), (0, -1, -3, -4, -5, -8))
        self.assertEqual(tuple(stars.FU_FAMILY_STEPS.values()), (0, 1, 2, 3, 4, 5, 6, 10))

    def test_03_all_twelve_anchor_rotations_have_fourteen_stars(self):
        for ziwei in z.BRANCHES:
            layout = stars.fourteen_positions_from_purple(ziwei)
            self.assertEqual(len(layout), 14)
            self.assertTrue(all(house in z.BRANCHES for house in layout.values()))
            self.assertEqual(layout["ZiWei"], ziwei)
            self.assertEqual(layout["TianFu"],
                             stars.tian_fu_from_purple(ziwei))
            self.assertEqual(Counter(layout.values()).total(), 14)

    def test_04_external_published_modern_wu_xu_worked_example(self):
        # Independently published example: https://askziwei.com/blog/en/
        # zi-wei-dou-shu-star-placement-formulas.html
        # This validates the positions of the modern example, not a real natal chart.
        result = stars.fourteen_positions_from_purple("Wu")
        expected = {
            "ZiWei": "Wu", "TianJi": "Si", "TaiYang": "Mao",
            "WuQu": "Yin", "TianTong": "Chou", "LianZhen": "Xu",
            "TianFu": "Xu", "TaiYin": "Hai", "TanLang": "Zi",
            "JuMen": "Chou", "TianXiang": "Yin", "TianLiang": "Mao",
            "QiSha": "Chen", "PoJun": "Shen"
        }
        self.assertEqual(result, expected)

    def test_05_external_modern_mao_chou_example(self):
        # https://www.doushu.ai/star-rules, fully specified anchor example.
        result = stars.fourteen_positions_from_purple("Mao")
        self.assertEqual(result["ZiWei"], "Mao")
        self.assertEqual(result["TianFu"], "Chou")
        self.assertEqual(result["TianJi"], "Yin")
        self.assertEqual(result["TaiYin"], "Yin")
        self.assertEqual(result["PoJun"], "Hai")
        self.assertEqual(result["QiSha"], "Wei")
        self.assertEqual(result["TanLang"], "Mao")

    def test_06_full_fourteen_from_original_skeleton_works(self):
        result = stars.fourteen_from_lunar_inputs("Jia", 1, "Zi", 1)
        self.assertEqual(result.partial_natal.bureau.bureau_number, 6)
        self.assertEqual(result.stars["ZiWei"], "You")
        self.assertEqual(result.stars["TianFu"], "Wei")
        self.assertEqual(len(result.stars), 14)
        self.assertEqual(len(result.placements_by_palace), 12)
        self.assertEqual(sum(map(len, result.placements_by_palace.values())), 14)
        self.assertEqual(result.status, "original_transcription_only")

    def test_07_original_uncertainty_propagates_without_star_invention(self):
        invalid_bureau = stars.fourteen_from_lunar_inputs("Jia", 9, "Zi", 1)
        self.assertIsNone(invalid_bureau.stars)
        self.assertIsNone(invalid_bureau.placements_by_palace)
        self.assertEqual(invalid_bureau.status, "unresolved_bureau")
        ambiguous_day = stars.fourteen_from_lunar_inputs("Jia", 3, "Zi", 9)
        self.assertIsNone(ambiguous_day.stars)
        self.assertEqual(ambiguous_day.status, "unresolved_purple_star")

    def test_08_opted_in_source_variants_remain_qualified(self):
        v = stars.fourteen_from_lunar_inputs(
            "Jia", 3, "Zi", 9, documented_diagram_corrections=True)
        self.assertEqual(len(v.stars), 14)
        self.assertEqual(v.status, "qualified_source_variant")
        q = stars.fourteen_from_lunar_inputs(
            "Jia", 9, "Zi", 1, documented_nayin_emendations=True)
        self.assertEqual(len(q.stars), 14)
        self.assertEqual(q.status, "qualified_source_variant")

    def test_09_invalid_anchors_and_natal_inputs_rejected(self):
        with self.assertRaises(ValueError):
            stars.fourteen_positions_from_purple("NotABranch")
        with self.assertRaises(ValueError):
            stars.fourteen_from_lunar_inputs("Invalid", 1, "Zi", 1)

    def test_10_scope_never_passes_complete_natal_or_empirical_validation(self):
        self.assertTrue(stars.ENGINE_SCOPE["not_full_astrological_natal_chart"])
        self.assertTrue(stars.ENGINE_SCOPE["unverified_actual_civil_birth_calendar_conversion"])
        self.assertFalse(stars.ENGINE_SCOPE["all_minor_and_aux_stars"])
        self.assertFalse(stars.ENGINE_SCOPE["full_four_transformations"])
        self.assertEqual(stars.ENGINE_SCOPE["independently_blinded_real_human_outcomes"], 0)
        self.assertEqual(stars.ENGINE_SCOPE["runtime_forecast_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
