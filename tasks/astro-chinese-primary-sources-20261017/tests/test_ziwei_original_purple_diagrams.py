"""Original Zi Wei bureau-day diagrams versus separate division rule.

This validates a bounded deterministic interpretation of transmitted tables,
not an astronomical birth calendar, a 14-star chart, or human prediction.
"""

from collections import Counter
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "ziwei"))
import quan_shu_vol2_nayin_bureau as ny  # noqa: E402
import quan_shu_vol2_purple_star as ps  # noqa: E402
import ziwei_source_mechanics as zw  # noqa: E402


class SourceDiagramParity(unittest.TestCase):
    def test_01_original_source_diagrams_are_all_five_sha_pinned(self):
        raw = ps.original_bureau_diagrams()
        self.assertEqual(set(raw), {2, 3, 4, 5, 6})
        self.assertEqual({bureau: len(days) for bureau, days in raw.items()},
                         {2: 30, 3: 29, 4: 29, 5: 30, 6: 30})

    def test_02_original_day_labels_and_the_exact_three_problem_cases(self):
        raw = ps.original_bureau_diagrams()
        self.assertEqual(sum(sum(map(len, t.values())) for t in raw.values()), 149)
        self.assertEqual(raw[3][9], ("Chen", "Yin"))
        self.assertNotIn(5, raw[3])
        self.assertNotIn(30, raw[4])
        self.assertEqual(ps.purple_palace_by_diagram(3, 9).source_status, "ambiguous")
        self.assertEqual(ps.purple_palace_by_diagram(3, 5).source_status, "missing")
        self.assertEqual(ps.purple_palace_by_diagram(4, 30).source_status, "missing")

    def test_03_147_unambiguous_source_readings_all_match_separate_rule(self):
        rows = [ps.purple_palace_by_diagram(b, d) for b in range(2, 7) for d in range(1, 31)]
        self.assertEqual(len(rows), 150)
        counts = Counter(r.source_status for r in rows)
        self.assertEqual(counts, {"direct": 147, "missing": 2, "ambiguous": 1})
        for r in rows:
            if r.source_status == "direct":
                self.assertEqual(r.palace, ps.purple_palace_by_division(r.bureau, r.lunar_day))

    def test_04_independent_remainder_arithmetic_reproduces_original_worked_example(self):
        self.assertEqual(ps.purple_palace_by_division(6, 1), "You")
        self.assertEqual(ps.purple_palace_by_division(2, 1), "Chou")
        self.assertEqual(ps.purple_palace_by_division(2, 2), "Yin")
        self.assertEqual(ps.purple_palace_by_division(3, 1), "Chen")
        self.assertEqual(ps.purple_palace_by_division(3, 5), "Yin")
        self.assertEqual(ps.purple_palace_by_division(3, 9), "Chen")
        self.assertEqual(ps.purple_palace_by_division(4, 30), "Hai")

    def test_05_emended_diagrams_cover_all_150_and_keep_three_distinct_statuses(self):
        corrected = ps.corrected_bureau_diagrams()
        self.assertTrue(all(len(m) == 30 for m in corrected.values()))
        rows = [ps.purple_palace_by_diagram(b, d, documented_corrections=True)
                for b in range(2, 7) for d in range(1, 31)]
        self.assertEqual(Counter(r.source_status for r in rows),
                         {"direct": 147, "modern_collation": 1,
                          "ambiguity_resolved": 1, "rule_inference": 1})
        self.assertTrue(all(r.palace == ps.purple_palace_by_division(r.bureau, r.lunar_day)
                            for r in rows))

    def test_06_original_transmitted_text_still_has_duplicated_and_missing_entries(self):
        self.assertEqual(ps.original_bureau_diagrams()[3][9], ("Chen", "Yin"))
        self.assertNotIn(5, ps.original_bureau_diagrams()[3])
        self.assertNotIn(30, ps.original_bureau_diagrams()[4])

    def test_07_invalid_natal_inputs_fail_closed(self):
        for b, d in ((0, 1), (1, 1), (7, 1), (6, 0), (6, 31),
                     (2, "1"), (True, 1), (3, 1.0)):
            with self.assertRaises(ValueError):
                ps.purple_palace_by_diagram(b, d)
            with self.assertRaises(ValueError):
                ps.purple_palace_by_division(b, d)

    def test_08_frozen_source_changed_fails_closed(self):
        with patch.object(ps, "SOURCE_SHA256", "0" * 64):
            with self.assertRaisesRegex(ValueError, "SHA256"):
                ps.original_bureau_diagrams()

    def test_09_3600_source_paths_preserve_all_unresolved_cases(self):
        cases = []
        for year in zw.STEMS:
            for life in zw.BRANCHES:
                bureau = ny.life_palace_bureau(year, life)
                for day in range(1, 31):
                    if bureau.bureau_number is None:
                        cases.append("unresolved_bureau")
                    else:
                        cases.append(ps.purple_palace_by_diagram(bureau.bureau_number, day).source_status)
        self.assertEqual(len(cases), 3600)
        self.assertEqual(Counter(cases),
                         {"direct": 3412, "unresolved_bureau": 120, "missing": 46, "ambiguous": 22})

    def test_10_opted_in_variants_cover_3600_without_promoting_to_natal_validation(self):
        for year in zw.STEMS:
            for life in zw.BRANCHES:
                bureau = ny.life_palace_bureau(year, life, documented_emendations=True)
                self.assertIsNotNone(bureau.bureau_number)
                for day in range(1, 31):
                    pos = ps.purple_palace_by_diagram(
                        bureau.bureau_number, day, documented_corrections=True)
                    self.assertEqual(pos.palace, ps.purple_palace_by_division(bureau.bureau_number, day))

    def test_11_explicit_nonpredictive_scope(self):
        self.assertFalse(ps.ENGINE_SCOPE["civil_to_lunar_conversion"])
        self.assertFalse(ps.ENGINE_SCOPE["14_principal_star_full_layout"])
        self.assertEqual(ps.ENGINE_SCOPE["real_human_predictive_validations"], 0)
        self.assertEqual(ps.ENGINE_SCOPE["runtime_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
