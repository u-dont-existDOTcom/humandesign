"""Original 1647 against independently typeset 1659 Naibod table images."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class CrossEditionPrint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = load(B / "NAIBOD_1647_VS_1659_SOURCE_COMPARISON_V1.json")
        cls.t = load(B / "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json")
        cls.original = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.degree = {r["equatorial_degrees"]: r for r in cls.t["degree_rows"]}
        cls.minute = {r["equatorial_arcminutes_as_printed"]: r for r in cls.t["minute_rows"]}
        cls.rows = {(r["kind"], r["row"]): r for r in cls.c["comparisons"]}

    def test_two_distinct_original_prints(self):
        self.assertEqual(self.c["first_edition"]["year"], 1647)
        self.assertEqual(self.c["second_edition"]["year"], 1659)
        self.assertIn("commons.wikimedia.org", self.c["second_edition"]["commons_file"])
        self.assertIn("1647", self.c["first_edition"]["source"])

    def test_original_1647_degree_image_hash(self):
        r = self.c["first_edition"]["degrees"]
        self.assertEqual(sha(B / r["file"]), r["sha256"])
        self.assertEqual(r["sha256"], self.original["photos"]["747"]["sha256"])

    def test_original_1647_minute_image_hash(self):
        r = self.c["first_edition"]["minutes"]
        self.assertEqual(sha(B / r["file"]), r["sha256"])
        self.assertEqual(r["sha256"], self.original["photos"]["748"]["sha256"])

    def test_second_edition_degree_print_hash(self):
        r = self.c["second_edition"]["degree_table"]
        self.assertEqual(r["djvu_scan_page"], 742)
        self.assertEqual(sha(B / r["file"]), r["sha256"])
        self.assertEqual(
            r["sha256"], "3f72ee094906122f1ab2b09762b4875b24e04b96cb7d04d5dba614d93946cb82"
        )

    def test_second_edition_minute_print_hash(self):
        r = self.c["second_edition"]["minute_table"]
        self.assertEqual(r["djvu_scan_page"], 743)
        self.assertEqual(sha(B / r["file"]), r["sha256"])
        self.assertEqual(
            r["sha256"], "36dfa3326c3ddab8e5ca78d5c30e47c43d6de66fd198fc1c7769ee1558358b85"
        )

    def test_printed_degree_69_both_carry(self):
        r = self.rows["degree", 69]
        self.assertEqual(r["1647"], [70, 4, 3])
        self.assertEqual(r["1659"], [70, 4, 3])
        self.assertEqual(r["secondary_flattened_year"], 69)
        self.assertTrue(self.degree[69]["visual_source_conflict_with_secondary_year"])

    def test_original_degree_80_24h_not_cleared(self):
        r = self.rows["degree", 80]
        self.assertEqual(r["1647"], [81, 62, 24])
        self.assertEqual(r["1659"], [81, 62, 24])
        self.assertEqual(self.degree[80]["printed_1647_hours"], 24)

    def test_original_degree_90_both_year_91(self):
        r = self.rows["degree", 90]
        self.assertEqual(r["1647"], [91, 116, 13])
        self.assertEqual(r["1659"], [91, 116, 13])
        self.assertEqual(r["secondary_flattened_year"], 90)

    def test_first_minute_discrepancy_remains_unresolved(self):
        r = self.rows["minute", 1]
        self.assertIsNone(r["1647"])
        self.assertEqual(r["1647_glyph_candidates"], [5, 6])
        self.assertEqual(r["1659"], [6, 4])
        self.assertEqual(self.minute[1]["original_photo_day_ambiguity"], [5, 6])

    def test_minute_8_persistent_likely_error(self):
        r = self.rows["minute", 8]
        self.assertEqual(r["1647"], [44, 10])
        self.assertEqual(r["1659"], [44, 10])
        self.assertEqual(r["status"], "PERSISTENT_PROBABLE_COMPOSITOR_ERROR")

    def test_original_minute_27_not_invented(self):
        r = self.rows["minute", 27]
        self.assertIsNone(r["1647"])
        self.assertIsNone(r["1659"])
        self.assertNotIn(27, self.minute)

    def test_minute_44_variant_old_vs_second(self):
        r = self.rows["minute", 44]
        self.assertEqual(r["1647"], [271, 8])
        self.assertEqual(r["1659"], [271, 18])
        self.assertEqual(r["secondary"], [271, 8])
        self.assertEqual(self.minute[44]["secondary_hours"], 8)
        self.assertEqual(r["status"], "SECOND_EDITION_CHANGES_PRINTED_HOUR")

    def test_minute_55_used_in_historical_example(self):
        self.assertEqual(self.rows["minute", 55]["1647"], [339, 17])
        self.assertEqual(self.rows["minute", 55]["1659"], [339, 17])

    def test_sixty_vs_degree_one_persistent_problem(self):
        r = self.rows["minute", 60]
        self.assertEqual(r["1647"], r["1659"])
        self.assertEqual(r["1647"], [374, 14])
        self.assertEqual(r["status"], "PERSISTENT_60_MINUTE_BOUNDARY_DISCREPANCY")

    def test_cross_edition_is_not_claim_of_exhaustiveness(self):
        self.assertFalse(self.c["full_1659_source_table_digit_corpus_checked"])
        self.assertFalse(self.c["full_1647_source_table_digit_corpus_checked"])
        self.assertTrue(
            self.c["first_edition_documentary_values_never_overwritten_from_later_edition"]
        )

    def test_no_forecast_or_canonical_promotion(self):
        self.assertFalse(self.c["historical_algorithm_martial_natal_accuracy_validated"])
        self.assertEqual(self.c["independent_real_human_predictions_validated"], 0)
        self.assertEqual(self.c["runtime_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
