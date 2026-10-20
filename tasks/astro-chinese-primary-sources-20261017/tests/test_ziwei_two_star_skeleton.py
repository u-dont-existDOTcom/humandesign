"""Bounded two-star skeleton source checks; source parity is not human accuracy."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ziwei"))
import quan_shu_two_star_skeleton as ts  # noqa: E402
import ziwei_source_mechanics as z  # noqa: E402


class TraditionalPartialNatalSkeleton(unittest.TestCase):
    def test_01_mirror_is_twelve_way_involution(self):
        actual = {s: ts.tian_fu_from_purple(s) for s in z.BRANCHES}
        self.assertEqual(len(set(actual.values())), 12)
        self.assertTrue(all(ts.tian_fu_from_purple(actual[s]) == s for s in z.BRANCHES))
        self.assertEqual(actual["Yin"], "Yin")
        self.assertEqual(actual["Shen"], "Shen")
        self.assertEqual(actual["Chou"], "Mao")
        self.assertEqual(actual["Chen"], "Zi")
        self.assertEqual(actual["Wu"], "Xu")

    def test_02_original_classical_jia_year_first_month_day_one(self):
        r = ts.two_star_from_lunar_inputs("Jia", 1, "Zi", 1)
        self.assertEqual((r.life_palace, r.body_palace), ("Yin", "Yin"))
        self.assertEqual((r.bureau.palace_stem, r.bureau.bureau_number), ("Bing", 6))
        self.assertEqual((r.purple_star.palace, r.tian_fu_palace), ("You", "Wei"))
        self.assertEqual(r.qualified_status, "original_transcription_only")

    def test_03_no_silent_nayin_correction_in_raw_mode(self):
        r = ts.two_star_from_lunar_inputs("Jia", 9, "Zi", 1)
        self.assertEqual(r.life_palace, "Xu")
        self.assertEqual(r.qualified_status, "unresolved_bureau")
        self.assertIsNone(r.purple_star)
        self.assertIsNone(r.tian_fu_palace)
        repaired = ts.two_star_from_lunar_inputs(
            "Jia", 9, "Zi", 1, documented_nayin_emendations=True)
        self.assertEqual(repaired.bureau.bureau_number, 6)
        self.assertEqual(repaired.qualified_status, "qualified_source_variant")

    def test_04_wood_three_day_nine_conflict_is_not_guessed(self):
        r = ts.two_star_from_lunar_inputs("Jia", 3, "Zi", 9)
        self.assertEqual(r.bureau.bureau_number, 3)
        self.assertEqual(r.qualified_status, "unresolved_purple_star")
        self.assertEqual(r.purple_star.source_status, "ambiguous")
        repaired = ts.two_star_from_lunar_inputs(
            "Jia", 3, "Zi", 9, documented_diagram_corrections=True)
        self.assertEqual((repaired.purple_star.palace, repaired.tian_fu_palace),
                         ("Chen", "Zi"))
        self.assertEqual(repaired.qualified_status, "qualified_source_variant")

    def test_05_wood_three_day_five_gap_remains_visible(self):
        r = ts.two_star_from_lunar_inputs("Jia", 3, "Zi", 5)
        self.assertEqual(r.qualified_status, "unresolved_purple_star")
        repaired = ts.two_star_from_lunar_inputs(
            "Jia", 3, "Zi", 5, documented_diagram_corrections=True)
        self.assertEqual(repaired.purple_star.palace, "Yin")
        self.assertEqual(repaired.purple_star.source_status, "modern_collation")

    def test_06_metal_four_day_thirty_not_original_text(self):
        r = ts.two_star_from_lunar_inputs("Jia", 7, "Zi", 30)
        self.assertEqual(r.bureau.bureau_number, 4)
        self.assertEqual(r.purple_star.source_status, "missing")
        repaired = ts.two_star_from_lunar_inputs(
            "Jia", 7, "Zi", 30, documented_diagram_corrections=True)
        self.assertEqual((repaired.purple_star.palace, repaired.tian_fu_palace),
                         ("Hai", "Si"))
        self.assertEqual(repaired.purple_star.source_status, "rule_inference")

    def test_07_explicit_leap_month_convention(self):
        regular = ts.two_star_from_lunar_inputs("Jia", 1, "Zi", 1)
        leap = ts.two_star_from_lunar_inputs("Jia", 1, "Zi", 1, is_leap_month=True)
        self.assertEqual(regular.life_palace, "Yin")
        self.assertEqual(leap.life_palace, "Mao")

    def test_08_unavailable_input_or_out_of_range_fails_closed(self):
        with self.assertRaises(ValueError):
            ts.tian_fu_from_purple("Unknown")
        with self.assertRaises(ValueError):
            ts.two_star_from_lunar_inputs("Jia", 1, "Zi", 31)
        with self.assertRaises(ValueError):
            ts.two_star_from_lunar_inputs("Jia", 0, "Zi", 1)

    def test_09_scope_cannot_be_called_a_full_natal_chart(self):
        self.assertFalse(ts.ENGINE_SCOPE["complete_fourteen_star_chart"])
        self.assertFalse(ts.ENGINE_SCOPE["civil_time_to_chinese_lunar"])
        self.assertEqual(ts.ENGINE_SCOPE["independent_real_human_validations"], 0)
        self.assertEqual(ts.ENGINE_SCOPE["runtime_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
