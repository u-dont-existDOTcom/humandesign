"""C32 pinned observed IERS EOP series: arithmetic, source and leap safety."""
from datetime import UTC,datetime
from pathlib import Path
import importlib.util
import json
import os
import tempfile
import unittest

from hellenistic_c32_iers_observed_eop import (
    SOURCE_FILENAME_SHA256, SOURCE_HEADER_ACTUAL, audit_observed_eop,
    load_pinned_eop, observed_dut1_for_datetime,
)

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"HELLENISTIC_C32_OBSERVED_IERS_EOP_SENSITIVITY_V1.json"
RAW=Path(os.environ.get("C32_IERS_C04_PINNED_FILE","/tmp/c32-eop-c04-mirror.txt"))
ERFA=importlib.util.find_spec("erfa") is not None


class TestC32ObservedIERSSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=json.loads(DATA.read_text(encoding="utf8"))

    def test_source_named_and_exact_version_pinned(self):
        x=self.x
        self.assertEqual(x["raw_IERS_file_sha256"],SOURCE_FILENAME_SHA256)
        self.assertEqual(x["actual_file_header_series"],SOURCE_HEADER_ACTUAL)
        self.assertTrue(x["not_automatically_equivalent_to_20u24_latest"])
        self.assertEqual((x["file_first_day"],x["file_last_day"]),
                         ("1962-01-01","2026-09-15"))
        self.assertEqual(x["file_daily_rows"],23634)

    def test_scope_missing_pre1962_explicit_not_imputed(self):
        x=self.x
        self.assertEqual(x["synthetic_samples_total"],145)
        self.assertEqual(x["IERS_available_synthetic_samples"],140)
        self.assertEqual(len(x["skipped_synthetic_samples"]),5)
        self.assertTrue(all(v["year"] in (1960,1961) for v in x["skipped_synthetic_samples"]))
        self.assertEqual(x["human_predictive_validations"],0)
        self.assertFalse(x["high_stakes_or_human_prediction_certified"])

    def test_recorded_ut1_dut1_gives_independent_parity(self):
        x=self.x
        self.assertLess(x["max_asc_ERFA_vs_Swiss_observed_EOP_arcseconds"],0.05)
        self.assertLess(x["max_mc_ERFA_vs_Swiss_observed_EOP_arcseconds"],0.05)
        self.assertGreater(x["max_asc_actual_EOP_shift_from_assumed0_arcseconds"],1)
        self.assertGreater(x["max_mc_actual_EOP_shift_from_assumed0_arcseconds"],1)

    def test_full_daily_source_rows_embedded_in_each_sample(self):
        for sample in self.x["samples"]:
            a,b=sample["IERS_source_daily_records"]
            self.assertEqual(a["date"],sample["IERS_source_days"][0])
            self.assertEqual(b["date"],sample["IERS_source_days"][1])
            frac=sample["interpolated_UT1_minus_TAI_fraction"]
            recomputed=(
                (1-frac)*(a["dut1_seconds"]-sample["day0_TAI_minus_UTC_seconds"])
                +frac*(b["dut1_seconds"]-sample["day1_TAI_minus_UTC_seconds"])
                +sample["instant_TAI_minus_UTC_seconds"]
            )
            self.assertAlmostEqual(recomputed,sample["IERS_observed_dut1_seconds"],places=11)
            self.assertTrue(sample["no_private_birth_data"])

    def test_unapplied_polar_motion_and_timezone_not_hidden(self):
        x=self.x
        self.assertTrue(x["polar_motion_and_dX_dY_not_implemented"])
        self.assertTrue(x["historical_civil_time_and_birthplace_not_audited"])
        self.assertTrue(x["independent_private_birth_case_not_included"])
        self.assertTrue(all(x["IERS_formal_sigma_max_seconds"]>=0
                            for x in x["samples"]))

    @unittest.skipUnless(RAW.is_file(),"raw pinned public IERS mirror file not present")
    def test_changed_source_file_rejected_fail_closed(self):
        rows=load_pinned_eop(RAW)
        self.assertEqual(len(rows),23634)
        with tempfile.TemporaryDirectory() as temp:
            bad=Path(temp)/"altered.txt"
            data=RAW.read_bytes()
            bad.write_bytes(data[:-1] + (b"0" if data[-1:]!=b"0" else b"1"))
            with self.assertRaises(ValueError):
                load_pinned_eop(bad)

    @unittest.skipUnless(RAW.is_file() and ERFA,
                         "optional pinned EOP source and pyerfa required")
    def test_leap_second_is_not_raw_dut1_linear_interpolation(self):
        rows=load_pinned_eop(RAW)
        mid=observed_dut1_for_datetime(datetime(2016,12,31,12,tzinfo=UTC),rows)
        nextday=observed_dut1_for_datetime(datetime(2017,1,1,0,tzinfo=UTC),rows)
        self.assertTrue(mid["available"])
        self.assertLess(mid["dut1_seconds"],-0.3)
        self.assertGreater(mid["dut1_seconds"],-0.5)
        self.assertAlmostEqual(nextday["dut1_seconds"],0.591287,places=6)
        # A naive interpolation of UT1-UTC across this leap day gives
        # an ~0.5 second artificial offset. UT1-TAI removes that jump.
        before,after=mid["two_original_daily_records"]
        naive=(before["dut1_seconds"]+after["dut1_seconds"])/2
        self.assertGreater(abs(naive-mid["dut1_seconds"]),0.4)

    @unittest.skipUnless(RAW.is_file() and ERFA,
                         "optional pinned EOP source and pyerfa required")
    def test_full_synthetic_observed_eop_replay(self):
        self.assertEqual(audit_observed_eop(RAW),self.x)

if __name__=="__main__":
    unittest.main()
