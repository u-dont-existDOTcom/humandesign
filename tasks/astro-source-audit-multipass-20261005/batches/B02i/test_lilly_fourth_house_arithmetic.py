"""Failure-focused static arithmetic checks; no predictive validation."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import lilly_fourth_house_arithmetic as arithmetic


class SourceCoordinateTests(unittest.TestCase):
    def test_missing_minute_is_rejected_and_omitted_cusps_stay_unknown(self):
        row = {"coordinate": {"sign": "Capricorn", "degree": 18, "minute": None}}
        with self.assertRaisesRegex(ValueError, "Complete source"):
            arithmetic.exact_longitude(row)
        result = arithmetic.reconcile()
        self.assertEqual(result["skipped_incomplete_exact_positions"], ["H04", "H10"])
        self.assertEqual(result["static_longitudes_computed"], 20)
        for key in ("H04", "H10"):
            self.assertIsNone(result["source_positions"][key]["longitude_arcminutes"])
            self.assertIsNone(result["source_positions"][key]["printed_coordinate"]["minute"])

    def test_invalid_complete_coordinate_is_not_misclassified_as_omitted(self):
        for minute in (-1, 60, True, "00"):
            with self.subTest(minute=minute), self.assertRaises(ValueError):
                arithmetic.exact_longitude({"coordinate": {"sign": "Aries", "degree": 1, "minute": minute}})


class CircularGeometryTests(unittest.TestCase):
    def test_wraparound_and_trine_use_the_short_circular_arc(self):
        near_end = arithmetic.GEO.longitude("Pisces", 29, 50)
        near_start = arithmetic.GEO.longitude("Aries", 0, 10)
        trine_partner = arithmetic.GEO.longitude("Cancer", 29, 50)
        self.assertEqual(arithmetic.forward_gap(near_end, near_start), 20)
        self.assertEqual(arithmetic.forward_gap(near_start, near_end), 21580)
        self.assertEqual(arithmetic.GEO.separation(near_end, near_start), 20)
        self.assertEqual(arithmetic.GEO.aspect_residual(near_end, trine_partner, 120), 0)

    def test_half_open_sector_wraps_and_does_not_admit_the_next_cusp(self):
        start = arithmetic.GEO.longitude("Pisces", 20, 0)
        end = arithmetic.GEO.longitude("Aries", 10, 0)
        self.assertTrue(arithmetic.in_forward_half_open_sector(start, start, end))
        self.assertTrue(arithmetic.in_forward_half_open_sector(0, start, end))
        self.assertFalse(arithmetic.in_forward_half_open_sector(end, start, end))
        self.assertFalse(arithmetic.in_forward_half_open_sector(start - 1, start, end))
        with self.assertRaises(ValueError):
            arithmetic.in_forward_half_open_sector(0, 0, 0)

    def test_partial_chart_supports_only_the_specified_h7_geometry(self):
        result = arithmetic.reconcile()
        checks = result["checks"]
        mercury = checks["Mercury_geometric_H07"]
        self.assertTrue(mercury["membership"])
        self.assertFalse(mercury["full_twelve_house_classification_computed"])
        self.assertFalse(mercury["interpretive_cusp_influence_applied"])
        self.assertEqual(checks["Mercury_to_H08"]["forward_distance"]["arcminutes"], 168)
        self.assertEqual(checks["Venus_H07_gap"]["forward_cusp_to_Venus"]["arcminutes"], 50)
        self.assertEqual(checks["fifth_from_seventh"]["radical_house"], 11)


class ChronologicalEndpointTests(unittest.TestCase):
    def test_bargain_and_payment_are_distinct_endpoints(self):
        chronology = arithmetic.reconcile()["checks"]["reported_calendar_intervals"]
        intervals = chronology["intervals"]
        self.assertEqual(intervals["question_to_bargain"]["days"], 25)
        self.assertEqual(intervals["bargain_to_payment_and_sealing"]["days"], 22)
        completion = intervals["question_to_payment_and_sealing"]
        self.assertEqual((completion["days"], completion["weeks"], completion["remaining_days"]), (47, 6, 5))
        self.assertEqual(completion["end_event"], "payment_and_sealing")
        self.assertIsNone(chronology["calendar_system_selected"])
        self.assertFalse(chronology["time_of_day_used"])

    def test_changed_agreement_date_changes_only_its_two_intervals(self):
        chronology = arithmetic.calendar_intervals(
            {"year": 1634, "month": 3, "day": 31},
            {"year": 1634, "month": 5, "day": 10},
            {"year": 1634, "month": 5, "day": 17},
        )["intervals"]
        self.assertEqual(chronology["question_to_bargain"]["days"], 40)
        self.assertEqual(chronology["bargain_to_payment_and_sealing"]["days"], 7)
        self.assertEqual(chronology["question_to_payment_and_sealing"]["days"], 47)

    def test_impossible_date_and_reordered_endpoints_are_rejected(self):
        question = {"year": 1634, "month": 3, "day": 31}
        completion = {"year": 1634, "month": 5, "day": 17}
        for bargain in ({"year": 1634, "month": 4, "day": 31},
                        {"year": 1634, "month": 5, "day": 18},
                        {"year": 1635, "month": 4, "day": 25}):
            with self.subTest(bargain=bargain), self.assertRaises(ValueError):
                arithmetic.calendar_intervals(question, bargain, completion)


class SourceVersusComputedTests(unittest.TestCase):
    def test_fortune_discrepancy_does_not_replace_printed_value(self):
        source_before = arithmetic.SOURCE_TABLE.read_bytes()
        result = arithmetic.reconcile()
        fortune = result["checks"]["Fortune"]
        self.assertEqual(fortune["printed"]["coordinate"], {"sign": "Pisces", "degree": 12, "minute": 27})
        self.assertEqual(fortune["computed"]["coordinate"], {"sign": "Pisces", "degree": 3, "minute": 27})
        self.assertFalse(fortune["printed_matches_computed"])
        self.assertEqual(fortune["shortest_discrepancy"]["arcminutes"], 540)
        self.assertFalse(fortune["printed_coordinate_replaced"])
        self.assertEqual(source_before, arithmetic.SOURCE_TABLE.read_bytes())

    def test_altered_printed_fortune_cannot_tune_the_computation(self):
        raw = json.loads(arithmetic.SOURCE_TABLE.read_text())
        altered = deepcopy(raw)
        point = next(row for row in altered["charts"][0]["bodies_and_points"] if row["body"] == "Fortune")
        point["coordinate"]["minute"] = 28
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "altered_source_fixture.json"
            fixture.write_text(json.dumps(altered))
            result = arithmetic.reconcile(fixture)["checks"]["Fortune"]
        self.assertEqual(result["printed"]["coordinate"]["minute"], 28)
        self.assertEqual(result["computed"]["coordinate"], {"sign": "Pisces", "degree": 3, "minute": 27})
        self.assertEqual(result["shortest_discrepancy"]["arcminutes"], 541)
        self.assertFalse(result["printed_matches_computed"])

    def test_profile_is_required_and_an_alternative_is_not_silently_used(self):
        with self.assertRaises(TypeError):
            arithmetic.compare_fortune(0, 0, 0, 0)
        with self.assertRaises(ValueError):
            arithmetic.compare_fortune(0, 0, 0, 0, profile="reverse_by_night")
        result = arithmetic.reconcile()["checks"]["Fortune"]
        self.assertEqual(result["profile"], "Lilly_XXIII_p143_144_same_by_day_and_night")

    def test_static_results_do_not_rewrite_source_qualitative_claims(self):
        result = arithmetic.reconcile()
        gap = result["checks"]["Sun_Venus_gap"]
        self.assertEqual(gap["shortest_separation"]["arcminutes"], 381)
        self.assertEqual(gap["source_stated_gap"]["value"], 6)
        trine = result["checks"]["Sun_Saturn_trine"]
        self.assertEqual(trine["residual_from_120_degrees"]["arcminutes"], 29)
        self.assertFalse(trine["meaning_of_perfect_resolved"])
        self.assertEqual(result["checks"]["Moon_Mars_gap"]["shortest_separation"]["arcminutes"], 28)
        self.assertFalse(result["ephemeris_computed"])
        self.assertFalse(result["physical_contact_times_computed"])
        self.assertFalse(result["global_orb_classification_computed"])
        self.assertFalse(result["predictive_accuracy_tested"])


if __name__ == "__main__":
    unittest.main()
