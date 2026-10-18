"""Provisional 1647 Naibod degree/minute table with explicit print conflicts.

Numeric source text is a derivative transcription aid; authority remains the
original first-edition photo. These tests check data integrity, not astrology.
"""

import hashlib
import json
import unittest
from pathlib import Path

from lilly_1647_direction_time_mechanics import OldTabularTime, naibod_recombine

B = Path(__file__).resolve().parent


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class HistoricNaibodTables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = j(B / "NAIBOD_SOURCE_TABLES_1647_PROVISIONAL_V1.json")
        cls.win = j(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.d = {r["equatorial_degrees"]: r for r in cls.t["degree_rows"]}
        cls.m = {r["equatorial_arcminutes_as_printed"]: r for r in cls.t["minute_rows"]}

    def test_complete_degree_coverage(self):
        self.assertEqual(len(self.d), 90)
        self.assertEqual(list(self.d), list(range(1, 91)))
        self.assertEqual(self.t["degree_rows_count"], 90)

    def test_missing_minute_27_kept_missing(self):
        self.assertEqual(self.t["missing_source_minute_labels"], [27])
        self.assertEqual(len(self.m), 59)
        self.assertEqual(list(self.m), [n for n in range(1, 61) if n != 27])
        self.assertNotIn(27, self.m)

    def test_original_table_photo_sha(self):
        for key, frame in (
            ("first_edition_degree_photo_sha256", 747),
            ("first_edition_minute_photo_sha256", 748),
        ):
            pic = B / self.win["photos"][str(frame)]["file"]
            self.assertEqual(sha(pic), self.t[key])
            self.assertEqual(pic.stat().st_size, self.win["photos"][str(frame)]["bytes"])

    def test_1647_full_pdf_same_witness(self):
        self.assertEqual(self.t["first_edition_pdf_sha256"], self.win["full_source_pdf_sha256"])

    def test_original_degree_1(self):
        r = self.d[1]
        self.assertEqual(
            (r["printed_1647_years"], r["printed_1647_days"], r["printed_1647_hours"]), (1, 5, 8)
        )

    def test_source_naibod_degree_11(self):
        r = self.d[11]
        self.assertEqual(
            (r["printed_1647_years"], r["printed_1647_days"], r["printed_1647_hours"]), (11, 58, 21)
        )

    def test_source_naibod_degree_19(self):
        r = self.d[19]
        self.assertEqual(
            (r["printed_1647_years"], r["printed_1647_days"], r["printed_1647_hours"]),
            (19, 101, 17),
        )

    def test_original_degree_68_boundary(self):
        r = self.d[68]
        self.assertEqual(
            (r["printed_1647_years"], r["printed_1647_days"], r["printed_1647_hours"]), (68, 364, 0)
        )

    def test_original_degree_69_normalization_vs_transcriber(self):
        r = self.d[69]
        self.assertEqual(
            (r["printed_1647_years"], r["printed_1647_days"], r["printed_1647_hours"]), (70, 4, 3)
        )
        self.assertEqual(r["secondary_transcript_years"], 69)
        self.assertTrue(r["visual_source_conflict_with_secondary_year"])

    def test_years_69_to_90_original_visual_not_secondary(self):
        self.assertEqual(
            [r["printed_1647_years"] for r in self.d.values() if r["equatorial_degrees"] >= 69],
            list(range(70, 92)),
        )
        self.assertEqual(
            sum(r["visual_source_conflict_with_secondary_year"] for r in self.d.values()),
            22,
        )

    def test_last_original_degree_90(self):
        r = self.d[90]
        self.assertEqual(
            (r["printed_1647_years"], r["printed_1647_days"], r["printed_1647_hours"]),
            (91, 116, 13),
        )

    def test_first_minute_source_ambiguity_retained(self):
        r = self.m[1]
        self.assertEqual((r["secondary_days"], r["secondary_hours"]), (6, 4))
        self.assertEqual(r["original_photo_day_ambiguity"], [5, 6])
        self.assertFalse(r["usable_without_source_reconciliation_for_timing"])

    def test_printed_minute_8_is_not_inferred_49(self):
        r = self.m[8]
        self.assertEqual((r["secondary_days"], r["secondary_hours"]), (44, 10))
        self.assertNotEqual(r["secondary_days"], 49)
        self.assertFalse(r["usable_without_source_reconciliation_for_timing"])

    def test_source_row_26_to_28_missing_one_label(self):
        self.assertEqual((self.m[26]["secondary_days"], self.m[26]["secondary_hours"]), (160, 14))
        self.assertEqual((self.m[28]["secondary_days"], self.m[28]["secondary_hours"]), (166, 18))
        self.assertNotIn(27, self.m)

    def test_source_29_and_30_compromised_sequence(self):
        self.assertEqual((self.m[29]["secondary_days"], self.m[29]["secondary_hours"]), (172, 23))
        self.assertEqual((self.m[30]["secondary_days"], self.m[30]["secondary_hours"]), (179, 3))
        self.assertFalse(self.m[29]["usable_without_source_reconciliation_for_timing"])

    def test_source_minute_44_hour(self):
        r = self.m[44]
        self.assertEqual((r["secondary_days"], r["secondary_hours"]), (271, 8))
        self.assertEqual((self.m[43]["secondary_days"], self.m[43]["secondary_hours"]), (265, 14))
        self.assertEqual((self.m[45]["secondary_days"], self.m[45]["secondary_hours"]), (277, 23))
        self.assertFalse(r["usable_without_source_reconciliation_for_timing"])

    def test_original_minute_55(self):
        self.assertEqual((self.m[55]["secondary_days"], self.m[55]["secondary_hours"]), (339, 17))

    def test_original_minute_52(self):
        self.assertEqual((self.m[52]["secondary_days"], self.m[52]["secondary_hours"]), (321, 4))

    def test_original_minute_60_source_boundary(self):
        self.assertEqual((self.m[59]["secondary_days"], self.m[59]["secondary_hours"]), (364, 10))
        self.assertEqual((self.m[60]["secondary_days"], self.m[60]["secondary_hours"]), (374, 14))
        self.assertFalse(self.m[60]["usable_without_source_reconciliation_for_timing"])

    def test_degree_one_and_minute_sixty_disagree(self):
        a = self.d[1]
        degree_one_hours = (a["printed_1647_years"] * 365 + a["printed_1647_days"]) * 24 + a[
            "printed_1647_hours"
        ]
        m = self.m[60]
        minute_60_hours = m["secondary_days"] * 24 + m["secondary_hours"]
        self.assertEqual(minute_60_hours - degree_one_hours, 4 * 24 + 6)

    def test_source_degree_80_hour24_not_normalized_away(self):
        r = self.d[80]
        self.assertEqual((r["printed_1647_days"], r["printed_1647_hours"]), (62, 24))

    def test_original_naibod_terms_replay(self):
        a, b = self.d[11], self.m[55]
        self.assertEqual(
            naibod_recombine(
                OldTabularTime(
                    a["printed_1647_years"], a["printed_1647_days"], a["printed_1647_hours"]
                ),
                OldTabularTime(0, b["secondary_days"], b["secondary_hours"]),
            ),
            OldTabularTime(12, 33, 14),
        )

    def test_original_naibod_opposition_replay(self):
        a, b = self.d[19], self.m[52]
        self.assertEqual(
            naibod_recombine(
                OldTabularTime(
                    a["printed_1647_years"], a["printed_1647_days"], a["printed_1647_hours"]
                ),
                OldTabularTime(0, b["secondary_days"], b["secondary_hours"]),
            ),
            OldTabularTime(20, 57, 21),
        )

    def test_not_entire_original_transcription_verified(self):
        self.assertFalse(self.t["all_minute_rows_unambiguous"])
        self.assertFalse(self.t["all_degree_years_crosschecked_expert"])
        self.assertFalse(self.t["full_astrological_birth_chart_engine_verified"])
        self.assertFalse(self.t["minute_degree_0_row_applicable"])

    def test_no_human_or_runtime_promotion(self):
        self.assertEqual(self.t["independent_person_outcome_validation_count"], 0)
        self.assertEqual(self.t["runtime_promotions"], 0)
        self.assertTrue(
            all(not r["arithmetic_or_personal_prediction_validated"] for r in self.d.values())
        )
        self.assertTrue(all(not r["human_event_prediction_validated"] for r in self.m.values()))

    def test_provenance_not_only_secondary_text(self):
        self.assertTrue(self.t["modern_text_transcription_aid_url"].startswith("https://"))
        self.assertEqual(len(self.t["frozen_secondary_degree_section_sha256"]), 64)
        self.assertEqual(len(self.t["frozen_secondary_minute_section_sha256"]), 64)
        self.assertIn("original", self.t["original_source"].lower())


if __name__ == "__main__":
    unittest.main()
