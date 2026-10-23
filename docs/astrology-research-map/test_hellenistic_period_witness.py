"""Deterministic arithmetic lock for explicitly transcribed Hephaistio II period witnesses.

Only tests printed-number transcription and sums recorded in the source-critical
JSON. Does NOT validate astrology, translation, calendar reconstruction, or
the numerical values as historical originals.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "HEPHAISTIO_II_TIMELORD_NUMERICAL_WITNESS_V1.json"


class TestHephaistioPeriodWitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_base_129_months(self) -> None:
        d = self.data
        self.assertEqual(sum(d["base_months"].values()), 129)
        self.assertEqual(d["chapter29"]["main_declared_months"], 129)
        self.assertEqual(d["chapter29"]["main_calculated_months"], 129)

    def test_first_subdivision_transcription_and_actual_sums(self) -> None:
        observations = self.data["chapter29"]["subdivisions"]
        self.assertEqual(len(observations), 7)
        expected = {
            "Saturn": (900, 913, 13),
            "Jupiter": (360, 365, 5),
            "Mars": (450, 450, 0),
            "Sun": (570, 569, -1),
            "Venus": (240, 243, 3),
            "Mercury": (600, 606, 6),
            "Moon": (750, 764, 14),
        }
        self.assertEqual(set(r["planet"] for r in observations), set(expected))
        for row in observations:
            base, total, delta = expected[row["planet"]]
            self.assertEqual(row["primary_months"] * 30, base)
            self.assertEqual(row["baseline_360_day_calendar_days"], base)
            self.assertEqual(sum(row["quoted_numeric_subperiod_days"].values()), total)
            self.assertEqual(row["subperiod_sum"], total)
            self.assertEqual(row["delta_vs_baseline_360_day_calendar"], delta)
        saturn = next(r for r in observations if r["planet"] == "Saturn")
        self.assertEqual(saturn["quoted_numeric_subperiod_days"]["Mercury"], 150)
        self.assertNotEqual(150, 140)  # The later appended Valens witness differs.

    def test_final_360_365_375_mismatch(self) -> None:
        d = self.data["chapter36"]
        self.assertEqual(d["year_declared_days"], 360)
        self.assertEqual(sum(d["year_primary_table"].values()), 360)
        self.assertEqual(d["year_primary_sum"], 360)
        self.assertEqual(sum(r["day_interval_in_local_subperiod_intro"] for r in d["detailed_subperiods"]), 375)
        self.assertEqual(d["day_interval_intro_sum"], 375)
        self.assertEqual(sum(sum(r["suballocations"].values()) for r in d["detailed_subperiods"]), 365)
        self.assertEqual(d["sum_of_all_listed_suballocations"], 365)
        actual = {r["planet"]: sum(r["suballocations"].values()) for r in d["detailed_subperiods"]}
        self.assertEqual(actual, {
            "Saturn": 86, "Jupiter": 34, "Mars": 42, "Sun": 54,
            "Venus": 21, "Mercury": 57, "Moon": 71,
        })
        self.assertEqual(d["year_primary_table"]["Mercury"], 52)
        self.assertEqual(d["year_primary_table"]["Moon"], 71)
        self.assertNotEqual(d["year_primary_table"]["Mercury"], 57)

    def test_no_human_validation_claim(self) -> None:
        self.assertEqual(self.data["scientific_validation"], "NOT_ATTEMPTED")
        self.assertIn("not_corrected", self.data["scope"])


if __name__ == "__main__":
    unittest.main()
