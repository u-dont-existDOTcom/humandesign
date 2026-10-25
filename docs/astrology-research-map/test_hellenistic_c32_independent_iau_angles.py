"""C32 research-only IAU/ERFA vs Swiss angle engine verification.

Synthetic input only. Independent true-equinox geometry never allowed
to overwrite root project's active participant-session prediction model.
"""
from datetime import UTC, datetime
import importlib.util
import json
from pathlib import Path
import unittest

from hellenistic_c32_independent_iau_angle_audit import (
    SYNTHETIC_SEED, CASE_COUNT,
    audit_synthetic, circular_arcseconds,
    eastern_horizon_intersection,
    resolve_civil_time_without_guessing, synthetic_cases,
    erfa_iau06_angles,
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "HELLENISTIC_C32_INDEPENDENT_IAU_ANGLE_PARITY_V1.json"
HAS_ERFA = importlib.util.find_spec("erfa") is not None
HAS_SWISS = importlib.util.find_spec("swisseph") is not None


class TestC32IndependentAngleAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(DATA.read_text(encoding="utf8"))

    def test_no_private_biographical_or_person_prediction_data(self):
        x = self.report
        self.assertEqual(x["scope"],
                         "DETERMINISTIC_SYNTHETIC_ONLY_PRIVATE_CASE_NOT_INCLUDED")
        self.assertFalse(x["human_personal_inputs_included"])
        self.assertEqual(x["human_predictive_validations"], 0)
        self.assertFalse(x["production_runtime_modified"])
        self.assertTrue(x["original_wrong_horizon_code_and_input_receipt_not_available"])
        self.assertTrue(x["cannot_prove_original_program_defect_from_synthetic_parity"])

    def test_deterministic_count_and_dates(self):
        x = list(synthetic_cases())
        self.assertEqual(len(x), CASE_COUNT)
        self.assertEqual(self.report["seed"], SYNTHETIC_SEED)
        self.assertEqual(self.report["count"], CASE_COUNT)
        self.assertEqual(x[0][0], datetime(2000, 1, 1, 12, tzinfo=UTC))
        self.assertEqual(x[-1][0].year,
                         datetime.fromisoformat(self.report["samples"][-1]["utc"]).year)

    def test_eastern_horizon_not_western_antipode(self):
        for row in self.report["samples"]:
            self.assertGreater(row["east_horizon_dot"],0)
            self.assertLess(row["western_east_dot"],0)
            self.assertAlmostEqual(
                circular_arcseconds(row["IAU_asc"],
                                   row["western_intersection_deg"]),
                180*3600,
                delta=1e-8
            )
        self.assertGreater(self.report["min_eastern_point_east_dot"],0)

    def test_two_iau_engines_agree_under_assumed_dut1(self):
        self.assertLess(self.report["max_abs_asc_error_arcseconds"], 0.05)
        self.assertLess(self.report["max_abs_mc_error_arcseconds"], 0.05)
        for row in self.report["samples"]:
            self.assertLess(row["asc_error_arcsec"],0.05)
            self.assertLess(row["mc_error_arcsec"],0.05)

    def test_house_system_invariant_for_angles(self):
        x=self.report
        self.assertLessEqual(x["max_house_system_asc_disagreement_arcseconds"],1e-7)
        self.assertLessEqual(x["max_house_system_mc_disagreement_arcseconds"],1e-7)

    def test_180_degree_wrong_ascendant_changes_source_exposure_group(self):
        from hellenistic_c30_dorotheus_expedition_lot import (
            CAMPAIGN_INDICATOR_SIGNS, ZODIAC)
        opposites={ZODIAC[(ZODIAC.index(name)+6)%12]
                   for name in CAMPAIGN_INDICATOR_SIGNS}
        self.assertEqual(len(opposites),4)
        self.assertTrue(opposites.isdisjoint(CAMPAIGN_INDICATOR_SIGNS))
        # This concerns chart arithmetic ONLY; no military outcome tested.
        self.assertEqual(self.report["human_predictive_validations"],0)

    def test_dut1_is_a_separate_real_source_of_uncertainty(self):
        x=self.report
        self.assertGreater(x["max_abs_DUT1_plusminus_0p9s_asc_shift_arcseconds"],1)
        self.assertGreater(x["max_abs_DUT1_plusminus_0p9s_mc_shift_arcseconds"],1)
        self.assertTrue(x["UT1_UTC_assumed_zero_not_actual_historical_EOP"])
        self.assertTrue(x["not_an_independent_birthplace_timezone_audit"])

    @unittest.skipUnless(HAS_ERFA and HAS_SWISS,
                         "optional ERFA/SWISS environments needed for live replay")
    def test_exact_full_145_synthetic_replay(self):
        self.assertEqual(audit_synthetic(),self.report)

    @unittest.skipUnless(HAS_ERFA, "optional ERFA is needed for live independent geometry")
    def test_iau_requires_timezone_and_admitted_location(self):
        with self.assertRaises(ValueError):
            erfa_iau06_angles(datetime(2000,1,1,12),
                              latitude=20,longitude=-30)
        with self.assertRaises(ValueError):
            erfa_iau06_angles(datetime(2000,1,1,12,tzinfo=UTC),
                              latitude=90,longitude=-30)
        with self.assertRaises(ValueError):
            erfa_iau06_angles(datetime(2000,1,1,12,tzinfo=UTC),
                              latitude=20,longitude=-30,dut1_seconds=float("nan"))

    def test_synthetic_iana_fold_refuses_to_guess(self):
        x=resolve_civil_time_without_guessing(
            datetime(2015,11,1,1,30),iana_timezone="America/New_York")
        self.assertEqual(x["civil_time_status"],"FOLD_AMBIGUOUS")
        self.assertEqual(x["utc_candidates"],
            ["2015-11-01T05:30:00+00:00","2015-11-01T06:30:00+00:00"])
        self.assertFalse(x["automatic_fold_choice_made"])
        self.assertFalse(x["eligible_for_human_prediction"])

    def test_spring_gap_not_normalized_silently(self):
        x=resolve_civil_time_without_guessing(
            datetime(2015,3,8,2,30),iana_timezone="America/New_York")
        self.assertEqual(x["civil_time_status"],"GAP_NONEXISTENT")
        self.assertEqual(x["utc_candidates"],[])

    def test_unambiguous_local_time_unique_utc(self):
        x=resolve_civil_time_without_guessing(
            datetime(2015,2,1,12,0),iana_timezone="America/New_York")
        self.assertEqual(x["civil_time_status"],"UNIQUE")
        self.assertEqual(x["utc_candidates"],["2015-02-01T17:00:00+00:00"])

    def test_local_input_not_permitted_to_hide_timezone(self):
        with self.assertRaises(ValueError):
            resolve_civil_time_without_guessing(
                datetime(2015,2,1,12,tzinfo=UTC),iana_timezone="America/New_York")
        with self.assertRaises(ValueError):
            resolve_civil_time_without_guessing(
                datetime(2015,2,1,12),iana_timezone="Not/A_Valid_Zone")


if __name__=="__main__":
    unittest.main()
