"""Source-locked NaYin five-phase bureau audit (not human predictive validation)."""

from collections import Counter
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "ziwei"))
import quan_shu_vol2_nayin_bureau as n  # noqa: E402
import ziwei_source_mechanics as z  # noqa: E402


class NaYinSourceAndMechanicalParity(unittest.TestCase):
    def test_01_exact_original_poem_and_two_malformed_witnesses(self):
        tokens = n.original_couplets()
        self.assertEqual(len(tokens), 30)
        self.assertEqual(len(set(tokens)), 30)
        self.assertIn("甲戊乙亥山头火", tokens)
        self.assertIn("戊戌已亥平地木", tokens)
        self.assertNotIn("甲戌乙亥山头火", tokens)
        self.assertNotIn("戊戌己亥平地木", tokens)

    def test_02_source_hash_fails_closed(self):
        with patch.object(n, "SOURCE_SHA256", "0" * 64):
            with self.assertRaisesRegex(ValueError, "SHA256 changed"):
                n.original_couplets()

    def test_03_unmodified_original_has_58_of_60_pillars(self):
        raw = n.table()
        self.assertEqual(len(raw), 58)
        self.assertNotIn(("甲", "戌"), raw)
        self.assertNotIn(("己", "亥"), raw)
        self.assertEqual({status for _, _, status in raw.values()}, {"direct"})

    def test_04_documented_corrections_complete_60_pillars(self):
        m = n.table(documented_emendations=True)
        self.assertEqual(len(m), 60)
        self.assertEqual(m[("甲", "戌")], ("Fire", 6, "emended_later_witness"))
        self.assertEqual(m[("己", "亥")], ("Wood", 3, "emended_later_witness"))
        self.assertEqual(sum(x[2] == "emended_later_witness" for x in m.values()), 2)
        self.assertEqual(sum(x[2] == "direct" for x in m.values()), 58)

    def test_05_unmodified_120_year_palace_paths_leave_exactly_four_unresolved(self):
        rows = [n.life_palace_bureau(y, b) for y in z.STEMS for b in z.BRANCHES]
        self.assertEqual(len(rows), 120)
        self.assertEqual(sum(r.source_status == "direct" for r in rows), 116)
        unresolved = [r for r in rows if r.source_status == "unresolved_source"]
        self.assertEqual(len(unresolved), 4)
        self.assertTrue(all(r.phase is None and r.bureau_number is None for r in unresolved))
        self.assertEqual({(r.palace_stem, r.life_palace) for r in unresolved},
                         {("Jia", "Xu"), ("Ji", "Hai")})

    def test_06_documented_emendations_resolve_four_paths_not_overwrite_raw_source(self):
        rows = [n.life_palace_bureau(y, b, documented_emendations=True)
                for y in z.STEMS for b in z.BRANCHES]
        self.assertEqual(sum(r.phase is not None for r in rows), 120)
        self.assertEqual(sum(r.source_status == "emended_later_witness" for r in rows), 4)
        self.assertEqual(sum(r.source_status == "direct" for r in rows), 116)
        self.assertIn("甲戊乙亥山头火", n.original_couplets())
        self.assertIn("戊戌已亥平地木", n.original_couplets())

    def test_07_every_pillar_occurs_twice_over_ten_year_stems_twelve_palaces(self):
        labels = Counter(
            (z.palace_stem_from_yin(y, b), b)
            for y in z.STEMS for b in z.BRANCHES
        )
        self.assertEqual(len(labels), 60)
        self.assertEqual(set(labels.values()), {2})

    def test_08_original_worked_example_jia_year_yin_is_fire_six(self):
        r = n.life_palace_bureau("Jia", "Yin")
        self.assertEqual((r.palace_stem, r.phase, r.bureau_number, r.source_status),
                         ("Bing", "Fire", 6, "direct"))
        self.assertEqual(z.life_and_body_palaces(1, "Zi"), ("Yin", "Yin"))
        self.assertEqual(n.life_palace_bureau("Ji", "Yin").bureau_number, 6)

    def test_09_five_distinct_bureaus_directly_present(self):
        m = n.table()
        self.assertEqual({p[1] for p in m.values()}, {2, 3, 4, 5, 6})
        self.assertEqual({p[0] for p in m.values()},
                         {"Water", "Wood", "Metal", "Earth", "Fire"})

    def test_10_invalid_convention_inputs_fail_closed(self):
        for inputs in (("Ji", "Invalid"), ("Invalid", "Yin"), ("甲", "寅")):
            with self.assertRaises(ValueError):
                n.life_palace_bureau(*inputs)

    def test_11_source_scope_is_not_full_natal_or_predictive_validation(self):
        self.assertFalse(n.ENGINE_SCOPE["lunar_calendar_converted"])
        self.assertFalse(n.ENGINE_SCOPE["14_star_chart_parity_verified"])
        self.assertFalse(n.ENGINE_SCOPE["independent_original_imprint_authentication"])
        self.assertEqual(n.ENGINE_SCOPE["human_predictive_tests"], 0)
        self.assertEqual(n.ENGINE_SCOPE["runtime_promotions"], 0)
        self.assertEqual(n.ENGINE_SCOPE["uncorrected_year_stem_palace_paths"], 116)
        self.assertEqual(n.ENGINE_SCOPE["documented_emendation_year_stem_palace_paths"], 120)

    def test_12_only_explicit_source_couplets_ever_emended(self):
        self.assertEqual(set(n.DOCUMENTED_EMENDATIONS), {"甲戊乙亥山头火", "戊戌已亥平地木"})
        for original, emended in n.DOCUMENTED_EMENDATIONS.items():
            self.assertEqual(len(original), len(emended))
            self.assertEqual(sum(a != b for a, b in zip(original, emended)), 1)
            self.assertIn(emended[-1], n.PHASE_TO_BUREAU)
        self.assertGreaterEqual(len(n.COLLATION_URLS), 2)


if __name__ == "__main__":
    unittest.main()
