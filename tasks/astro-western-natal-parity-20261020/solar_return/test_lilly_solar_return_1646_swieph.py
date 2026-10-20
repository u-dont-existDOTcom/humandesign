"""Original source 1646 return interpolation vs independently calculated Sun.

Only known native retrospectively discussed by Lilly. Tests demonstrate
calculation reproducibility, original-vs-modern discrepancies, no forecast.
"""

from __future__ import annotations

import json
import sys
import unittest
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import swisseph as swe

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import sun_1646_original_swieph as sol  # noqa: E402

FROZEN=HERE / "LILLY_1646_SOLAR_RETURN_INTERPOLATION_SWIEPH_V1.json"
EPHE=Path("/tmp/hd-western-swe-1616-20261020")
EXTERNAL_EPHE_READY=(
    swe.version=="2.10.03"
    and all((EPHE/f).is_file() for f in ("sepl_12.se1","semo_12.se1"))
)


class Frozen1646OriginalSourceAndTiming(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record=json.loads(FROZEN.read_text())
        cls.comp=cls.record["solar_return_source_modern_comparison"]

    def test_01_original_1647_and_1659_same_folio735_photos_hashes(self):
        literal,witnesses,sha=sol.source_witness()
        self.assertEqual(set(witnesses),set(sol.EXPECTED_SOURCE_KEYS))
        for key,meta in witnesses.items():
            self.assertEqual(meta["sha256"],
                             self.record["source_original_1647_1659_photo_witnesses"][key]["sha256"])
            self.assertGreater(meta["bytes"],100_000)
        self.assertEqual(self.record["original_B07at_source_file_SHA256"],sha)
        self.assertEqual(sha,sha256(sol.SOLAR_SOURCE.read_bytes()).hexdigest())
        self.assertEqual(literal["source_sum_unrounded_time_hms"],[10,8,47])

    def test_02_old_original_interpolation_rows_not_repaired(self):
        lit=self.record["source_original_day_solar_interpolation_values"]
        self.assertEqual(lit["original_natal_longitude_deg_min"],[6,37])
        self.assertEqual(lit["original_ephemeris_noon_deg_min"],[6,12])
        self.assertEqual(lit["remaining_arcminutes"],25)
        self.assertEqual(lit["source_sun_daily_motion_arcminute_arcsecond"],[59,10])
        self.assertEqual(lit["historical_nearby_table_rate_arcminute_arcsecond"],[59,8])
        self.assertEqual(lit["twenty_arcminute_time_hms"],[8,7,2])
        self.assertEqual(lit["five_arcminute_time_hms"],[2,1,45])
        self.assertEqual(lit["source_sum_unrounded_time_hms"],[10,8,47])
        self.assertEqual(lit["printed_later_minute_level_time_hm"],[10,8])
        self.assertEqual(lit["source_westward_meridian_subtract_hm"],[1,7])
        self.assertEqual(lit["house_table_noon_hm"],[12,26])
        self.assertEqual(lit["source_equation_of_time_hm"],[0,16])
        self.assertEqual(lit["source_house_table_final_hm"],[21,43])
        self.assertEqual(self.comp["source_time_addition_seconds"],36527)

    def test_03_original_source_clock_and_UT_projections_not_equated(self):
        self.assertTrue(
            self.comp["source_house_table_final_is_not_a_direct_astronomical_UT_datetime"]
        )
        self.assertTrue(self.comp["nominal_1646_source_clock_UT_equivalence_unverified"])
        self.assertFalse(self.record["original_17th_century_local_UT_and_date_style_resolved"])
        self.assertEqual(self.record["reference_clock_unverified"],
                         "1646-09-19 12h UT is an analytic assumption, "
                         "NOT original Frankfurt clock")

    def test_04_original_vs_modern_Julian_noon_1646_solar_longitude_difference(self):
        self.assertAlmostEqual(self.comp["source_sun_noon_longitude_deg"],186.2,delta=1e-8)
        self.assertAlmostEqual(self.comp["modern_Julian_date_noon_UT_sun_longitude_deg"],
                               186.36618544,delta=2e-6)
        self.assertAlmostEqual(self.comp["modern_Julian_noon_minus_old_ephemeris_noon_arcmin"],
                               9.97112642,delta=0.005)
        self.assertLess(self.comp["modern_Gregorian_date_noon_UT_sun_longitude_deg"],180)
        self.assertGreater(self.comp["modern_Gregorian_date_noon_UT_sun_longitude_deg"],170)

    def test_05_old_Maginus_daily_motion_near_modern_despite_position_difference(self):
        self.assertEqual(self.comp["source_daily_sun_motion_arcmin_arcsec"],[59,10])
        self.assertEqual(self.comp["source_Maginus_nearby_rate_arcmin_arcsec"],[59,8])
        modern_rate=self.comp["modern_noon_Julian_daily_rate_arcmin_arcsecond"]
        self.assertEqual(modern_rate[0],59)
        self.assertAlmostEqual(modern_rate[1],8.1613324,delta=0.005)
        self.assertAlmostEqual(self.comp["source_Maginus_rate_minus_modern_noon_rate_arcsec"],
                               -0.1613324,delta=0.005)
        self.assertAlmostEqual(self.comp["source_daily_motion_minus_modern_noon_rate_arcsec"],
                               1.8386676,delta=0.005)
        self.assertTrue(self.comp["daily_rate_parity_does_not_prove_noon_original_longitude_or_return_clock"])

    def test_06_historic_literal_table_sum_matches_rate_rational_arithmetic(self):
        self.assertEqual(self.comp["source_time_exact_sum_hms"],[10,8,47])
        self.assertEqual(self.comp["source_truncated_clock_hm"],[10,8])
        self.assertLess(
            abs(self.comp["source_time_by_exact_25_over_Maginus_59_08_rate_seconds"]-36527),
            2,
        )
        self.assertEqual(self.comp["source_printed_10h08m47_if_UT_interpreted_as_HHMMSS"],
                         [22,8,47])

    def test_07_two_modern_solar_longitude_targets_have_distinct_exact_roots(self):
        src=self.comp["modern_sun_when_original_source_6deg37_target_crossed"]
        modern=self.comp["modern_sun_when_modern_natal_Julian_1616_target_crossed"]
        self.assertAlmostEqual(src["hours_after_1646_09_19_Julian_noon_assumed_UT"],
                               6.09853765,delta=0.0001)
        self.assertAlmostEqual(modern["hours_after_1646_09_19_Julian_noon_assumed_UT"],
                               8.81257644,delta=0.0001)
        self.assertLess(src["crossing_JD_UT"],modern["crossing_JD_UT"])
        for rec in (src,modern):
            self.assertTrue(rec["returned_swieph"])
            self.assertFalse(rec["returned_moshier"])
            self.assertFalse(rec["historical_observed_return_clock_verified"])
            self.assertEqual(rec["julian_calendar_root_date_time"]["day"],19)
            self.assertEqual(rec["gregorian_calendar_root_date_time"]["day"],29)

    def test_08_original_natal_Sun_is_source_not_modern_natal_target(self):
        self.assertAlmostEqual(self.comp["source_sun_natal_longitude_deg"],186+37/60)
        self.assertAlmostEqual(self.comp["modern_1616_Julian_natal_at_assumed_UT_Sun_longitude_degrees"],
                               186.728146277,delta=0.000002)
        self.assertAlmostEqual(self.comp["modern_crossing_modern_natal_minus_crossing_old_natal_arcminutes"],
                               6.688776,delta=0.002)

    def test_09_every_epoch_ephemeris_flag_actual_SWIEPH_no_Moshier(self):
        self.assertTrue(self.record["every_modern_solar_longitude_actual_swieph"])
        self.assertTrue(self.record["no_moshier_fallback"])
        self.assertEqual(self.record["solar_calculation_flags_request"],
                         swe.FLG_SWIEPH|swe.FLG_SPEED)
        for f in self.record["solar_calculation_return_flags"]:
            self.assertTrue(f&swe.FLG_SWIEPH)
            self.assertFalse(f&swe.FLG_MOSEPH)

    def test_10_source_diagnostic_is_not_actual_human_evidence(self):
        self.assertTrue(self.record["source_known_merchant_retrospective_only"])
        self.assertFalse(self.record["historically_exact_revolution_and_house_timings_authenticated"])
        self.assertFalse(self.record["original_17th_century_local_UT_and_date_style_resolved"])
        self.assertTrue(self.record["retrospective_merchant_study_not_blind"])
        self.assertEqual(self.record["independently_scored_blind_actual_humans"],0)
        self.assertEqual(self.record["runtime_astrology_promotions"],0)
        self.assertEqual(self.record["new_historical_source_annotation_ids"],0)

    def test_11_mismatched_source_photo_sha_fails_closed(self):
        with (
            patch.object(sol, "SOLAR_SOURCE", Path("nonexistent")),
            self.assertRaises(FileNotFoundError),
        ):
            sol.source_witness()

    def test_12_no_unbracketed_solar_root_guess(self):
        with self.assertRaisesRegex(ValueError,"source longitude"):
            sol.crossing_of_target(2322521.0,179.9)
        with self.assertRaisesRegex(ValueError,"source longitude"):
            sol.crossing_of_target(2322521.0,210.1)


@unittest.skipUnless(
    EXTERNAL_EPHE_READY,
    "Exact SWIEPH binaries optional; offline original source checks remain active",
)
class RealSWE1616_1646SunCalculations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen=json.loads(FROZEN.read_text())

    def test_13_full_original_source_and_modern_return_calculation_replay(self):
        actual=sol.compute(EPHE)
        self.assertEqual(actual,self.frozen)

    def test_14_deliberately_Moshier_fallback_raises_and_does_not_return_a_fake_root(self):
        with (
            patch.object(
                sol.swe, "calc_ut",
                return_value=([186.2, 0, 0, 0.985, 0, 0], swe.FLG_MOSEPH | swe.FLG_SPEED),
            ),
            self.assertRaisesRegex(ValueError, "true return flags"),
        ):
            sol.sun_at_jd(2322521.0)

    def test_15_original_crossings_solved_by_swisseph_not_time_fit(self):
        original=self.frozen["solar_return_source_modern_comparison"]
        s=sol.compute(EPHE)["solar_return_source_modern_comparison"]
        self.assertAlmostEqual(
            original["modern_sun_when_original_source_6deg37_target_crossed"]["crossing_JD_UT"],
            s["modern_sun_when_original_source_6deg37_target_crossed"]["crossing_JD_UT"],
            delta=5e-9,
        )
        self.assertAlmostEqual(
            original["modern_sun_when_modern_natal_Julian_1616_target_crossed"]["crossing_JD_UT"],
            s["modern_sun_when_modern_natal_Julian_1616_target_crossed"]["crossing_JD_UT"],
            delta=5e-9,
        )


if __name__=="__main__":
    unittest.main()
