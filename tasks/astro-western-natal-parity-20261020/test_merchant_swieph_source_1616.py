"""Reproducible source and ephemeris audit for Lilly's known 1616 merchant.

Tests verify 1647/1659 *printed source* against one modern mathematical
hypothesis, never a historical birth certificate or predictive success.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import swisseph as swe

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import compute_1616_merchant_swe_parity as m  # noqa: E402

FROZEN = BASE / "MERCHANT_1616_SOURCE_VS_SWISS_TROPICAL_V1.json"
EPHE = Path("/tmp/hd-western-swe-1616-20261020")
EXTERNAL_FILES_READY = (
    all((EPHE / k).is_file() for k in m.EPHE_FILES)
    and swe.version == "2.10.03"
)


class OriginalHistoricalMerchantSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
        cls.orig, cls.original_sha = m.source_original()

    def test_01_original_seven_exact_printed_longitudes_are_preserved(self):
        expected = {
            "Saturn": ("Taurus", 9, 2),
            "Jupiter": ("Sagittarius", 21, 55),
            "Mars": ("Leo", 0, 54),
            "Sun": ("Libra", 6, 37),
            "Venus": ("Libra", 6, 54),
            "Mercury": ("Libra", 3, 34),
            "Moon": ("Gemini", 1, 44),
        }
        self.assertEqual(set(self.orig), set(expected))
        for body, (sign, degree, minute) in expected.items():
            self.assertAlmostEqual(
                self.orig[body],
                m.ZODIAC.index(sign) * 30 + degree + minute / 60,
                delta=1e-10,
            )
            self.assertAlmostEqual(
                self.frozen["source_planet_positions_7"][body],
                self.orig[body],
                delta=0.00000001,
            )

    def test_02_source_witness_and_old_pdf_claim_not_substituted(self):
        self.assertEqual(self.original_sha, self.frozen["original_source_witness_SHA256"])
        self.assertEqual(
            sha256(m.SOURCE_PATH.read_bytes()).hexdigest(),
            self.frozen["original_source_witness_SHA256"],
        )
        self.assertEqual(
            self.frozen["original_Wellcome_whole_original_1647_pdf_SHA256"],
            m.SOURCE_PDF_SHA,
        )
        self.assertEqual(self.frozen["source_printed_birth_year_month_day"], [1616, 9, 19])
        self.assertEqual(self.frozen["source_printed_birth_clock_text"], "2 h. 24. 39 P.M.")
        self.assertEqual(self.frozen["source_printed_latitude_degrees"], 53)
        self.assertFalse(self.frozen["source_birthplace_precise_longitude_independently_known"])
        self.assertFalse(self.frozen["source_birth_clock_UT_or_apparent_local_solar_independently_known"])

    def test_03_all_seventy_frozen_output_flags_have_SWE_actual_not_moshier(self):
        self.assertTrue(self.frozen["calc_requested_swieph"])
        self.assertTrue(self.frozen["calc_returned_swieph_for_all_70_positions"])
        self.assertFalse(self.frozen["calc_any_moshier_fallback"])
        count = 0
        for label in ("julian_original_calendar_hypothesis",
                      "gregorian_original_calendar_hypothesis"):
            hyp = self.frozen[label]
            self.assertEqual(len(hyp["body_reports"]), 7)
            self.assertFalse(hyp["original_clock_was_UT_independently_verified"])
            for body in hyp["body_reports"]:
                self.assertEqual(len(body["time_sensitivity_plus_minus_2h"]), 5)
                for row in body["time_sensitivity_plus_minus_2h"]:
                    count += 1
                    self.assertTrue(row["returned_flags"] & swe.FLG_SWIEPH)
                    self.assertFalse(row["returned_flags"] & swe.FLG_MOSEPH)
                    self.assertTrue(row["actual_SWIEPH"])
                    self.assertFalse(row["actual_MOSEPH_fallback"])
        self.assertEqual(count, 70)

    def test_04_date_hypotheses_not_silently_interchangeable(self):
        jul = self.frozen["julian_original_calendar_hypothesis"]
        gre = self.frozen["gregorian_original_calendar_hypothesis"]
        self.assertEqual((jul["matching_original_zodiac_signs"],
                          gre["matching_original_zodiac_signs"]), (7, 2))
        self.assertEqual(self.frozen["julian_date_written_1616_09_19_as_gregorian_reference"],
                         "1616-09-29")
        self.assertLess(jul["median_abs_arcminute_longitude_residual_at_unverified_UT"],
                        gre["median_abs_arcminute_longitude_residual_at_unverified_UT"])
        self.assertGreater(gre["median_abs_arcminute_longitude_residual_at_unverified_UT"], 500)
        self.assertLess(jul["median_abs_arcminute_longitude_residual_at_unverified_UT"], 10)

    def test_05_signed_residuals_mercury_venus_remain_major_unexplained(self):
        jul = self.frozen["julian_original_calendar_hypothesis"]
        rows = {x["source_body"]: x for x in jul["body_reports"]}
        self.assertAlmostEqual(
            rows["Sun"]["reference_UT_assumption_arcminute_difference"],
            6.68878, delta=0.01
        )
        self.assertAlmostEqual(
            rows["Mercury"]["reference_UT_assumption_arcminute_difference"],
            93.35419, delta=0.01
        )
        self.assertAlmostEqual(
            rows["Venus"]["reference_UT_assumption_arcminute_difference"],
            64.29367, delta=0.01
        )
        self.assertAlmostEqual(
            rows["Moon"]["reference_UT_assumption_arcminute_difference"],
            -1.00358, delta=0.01
        )
        for planet in ("Mercury", "Venus"):
            for entry in rows[planet]["time_sensitivity_plus_minus_2h"]:
                self.assertGreater(entry["difference_vs_1647_printed_arcminutes"], 50)
        self.assertEqual(self.frozen["assumption_sensitivity_hours"], [-2, -1, 0, 1, 2])

    def test_06_reference_clock_is_hypothesis_not_fitted_person(self):
        self.assertEqual(self.frozen["julian_original_calendar_hypothesis"][
            "modern_UT_clock_assumed_HHMMSS"], "14:24:39")
        self.assertTrue(self.frozen["source_author_already_knows_native"])
        for flag in (
            "independently_verified_human_prediction",
            "source_old_new_style_calendar_externally_birth_registered",
            "claimed_independent_original_birth_certificate",
            "independent_natal_house_geometry_reconstruction",
            "independent_historical_ephemeris_exact_natal_parity",
        ):
            self.assertFalse(self.frozen[flag], flag)
        self.assertEqual(self.frozen["real_person_prospective_blind_prediction_count"], 0)
        self.assertEqual(self.frozen["runtime_astrological_promotions"], 0)
        self.assertEqual(self.frozen["historical_source_records_added"], 0)

    def test_07_math_difference_wraps_correctly_and_not_to_sign_only(self):
        self.assertAlmostEqual(m.signed_arcminutes(359.0, 1.0), -120)
        self.assertAlmostEqual(m.signed_arcminutes(1.0, 359.0), 120)
        self.assertAlmostEqual(m.signed_arcminutes(185.0, 185.0), 0)
        self.assertAlmostEqual(m.signed_arcminutes(181.0, 179.0), 120)

    def test_08_source_signs_are_sourced_not_just_anticia_recomputed(self):
        source = json.loads(m.SOURCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(source["all_other_6_antiscions_arithmetically_match"], True)
        self.assertEqual(source["mismatch_original_body"], "Mercury")
        self.assertEqual(source["both_printed_editions_Mercury_antiscion"],
                         ["Pisces", 26, 6])
        self.assertEqual(source["analytic_expected_Mercury_antiscion"],
                         ["Pisces", 26, 26])
        self.assertEqual(source["original_minus_formula_arcminutes"], -20)

    def test_09_invalid_ephemeris_directory_hash_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            td = Path(temp)
            (td / "sepl_12.se1").write_bytes(b"wrong-data")
            (td / "semo_12.se1").write_bytes(b"wrong-data")
            with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
                m.validate_ephe_dir(td)
        with self.assertRaisesRegex(ValueError, "explicit existing absolute"):
            m.validate_ephe_dir(Path("relative/path"))


@unittest.skipUnless(
    EXTERNAL_FILES_READY,
    "Pinned original SWIEPH binaries optional; offline tests remain active",
)
class LiveCheckedSwissEphemerisCalculation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads(FROZEN.read_text(encoding="utf-8"))

    def test_10_physical_files_exact_hash_length_and_original_repo(self):
        source = m.validate_ephe_dir(EPHE)
        self.assertEqual(set(source), set(m.EPHE_FILES))
        for f, witness in source.items():
            self.assertEqual(witness["sha256"], m.EPHE_FILES[f])
            self.assertTrue(witness["bytes"] > 100_000)
            self.assertFalse(witness["released_outside_repo_binary_copied_into_humandesign"])

    def test_11_70_SWIEPH_positions_recompute_exactly_from_separate_binaries(self):
        current = m.compute(EPHE)
        for key in (
            "source_planet_positions_7",
            "calc_library_version",
            "source_printed_birth_clock_text",
            "julian_original_calendar_hypothesis",
            "gregorian_original_calendar_hypothesis",
            "external_official_2026_DE441_ephemeris_file_witnesses",
        ):
            self.assertEqual(current[key], self.frozen[key])
        self.assertEqual(current["calc_library_version"], "2.10.03")

    def test_12_deliberately_forced_non_SWIEPH_flags_fail_closed(self):
        with patch.object(m.swe, "calc_ut", return_value=(
            [1.0, 0, 0, 0, 0, 0], swe.FLG_MOSEPH | swe.FLG_SPEED
        )), self.assertRaisesRegex(ValueError, "SWIEPH requested"):
            m.strict_swieph_body(2311564.10, swe.SUN)

    def test_13_early_historical_JUL_and_GREG_calendar_JDN_separated(self):
        swe.close()
        swe.set_ephe_path(str(EPHE))
        jul = swe.julday(1616, 9, 19, m.REFERENCE_CLOCK_UT_HOURS_ASSUMED, swe.JUL_CAL)
        greg = swe.julday(1616, 9, 19, m.REFERENCE_CLOCK_UT_HOURS_ASSUMED, swe.GREG_CAL)
        self.assertAlmostEqual(jul-greg, 10.0, places=9)
        self.assertAlmostEqual(
            jul,self.frozen["julian_original_calendar_hypothesis"]["julian_day_UT_for_reference_assumption"],
            places=8
        )
        self.assertAlmostEqual(
            greg,self.frozen["gregorian_original_calendar_hypothesis"]["julian_day_UT_for_reference_assumption"],
            places=8
        )


if __name__ == "__main__":
    unittest.main()
