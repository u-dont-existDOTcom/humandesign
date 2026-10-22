#!/usr/bin/env python3
"""Third ephemeris synthetic-only source parity regression, including negatives.

This test suite does NOT validate BaZi on real humans or independently authenticate
any traditional printed original. Moshier is a third numerical software witness.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from hashlib import sha256
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from solve_third_moshier_solar_term import (
    B, ROOT, PREVIOUS, OUTPUT, PIN, SWE_BIN, PREV_SHA, BIN_SHA, TERMS,
    SourceMismatch, sha, _astro_module,
    tropical_geocentric_apparent_sun, angular_error_degrees, crossing, run
)

FIXTURE_SHA="48d9b068797c4ef2209761c4d94532d035e26205b48c8f3cfb250c61722d06b1"
PARENT_V30_INDEX=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V30.json"
PARENT_V30_SHA="6e46e87ca2019945301b1f47f8d3ee91bd58c1a89461912d50bace74bc9543de"
CLOCKS_EXPECTED={
    "2023-02-04T10:42:21",
    "2026-01-05T16:22:54",
    "2026-02-04T04:01:52",
    "2057-08-07T07:33:10",
    "2057-08-07T07:34:09",
}
THIRD_VS_SXTWL_OFFSETS={
    "2023-02-04":11.666323,
    "2026-01-05":15.9330,
    "2026-02-04":16.6582,
    "1912-12-07":0.3384,
    "2057-08-07":61.527,
    "1965-12-07":-0.1808,
}


class ThreeWayJieQi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(OUTPUT.read_text(encoding="utf-8"))
        cls.parent=json.loads(PREVIOUS.read_text(encoding="utf-8"))
        cls.manifest=json.loads(PIN.read_text(encoding="utf-8"))

    def test_report_binary_exact_hash(self):
        self.assertEqual(sha(OUTPUT.read_bytes()),FIXTURE_SHA)
        self.assertEqual(self.report["status"],"DEVELOPMENT_ONLY_NOT_AUTHORITY_FOR_HISTORICAL_BIRTH_CHARTS")

    def test_prior_two_source_516_case_fixture_untouched(self):
        self.assertEqual(sha(PREVIOUS.read_bytes()),PREV_SHA)
        self.assertEqual((len(self.parent["ordinary_synthetic_cases"]),
                          len(self.parent["precise_transition_boundary_cases"])),(480,36))
        self.assertEqual((self.parent["naive_sxtwl_day_level_mismatches"],
                          self.parent["corrected_sxtwl_vs_lunar_python_mismatches"],
                          len(self.parent["precise_transition_disagreements"])),(8,0,4))

    def test_accepted_chinese_source_index_no_change(self):
        self.assertEqual(sha(PARENT_V30_INDEX.read_bytes()),PARENT_V30_SHA)
        old=json.loads(PARENT_V30_INDEX.read_text(encoding="utf-8"))
        self.assertEqual(old["sum_source_annotations"],1289)
        self.assertEqual([s["accepted_source_annotations"] for s in old["systems"]],[230,1059])
        self.assertEqual((old["independently_validated_real_human_claims"],old["runtime_promotions"]),(0,0))

    def test_moshier_binary_pinned_hash_bytes_versions_and_loaded_path(self):
        swe=_astro_module()
        self.assertEqual((SWE_BIN.stat().st_size,sha(SWE_BIN.read_bytes())),(2391504,BIN_SHA))
        self.assertEqual(swe.version,"2.10.03")
        self.assertEqual(Path(swe.__file__).resolve(),SWE_BIN.resolve())
        self.assertEqual((self.manifest["dependency_version"],
                          self.manifest["source_binary_sha256"]),("2.10.3.6",BIN_SHA))
        self.assertFalse(self.manifest["real_human_predictive_validations"])

    def test_only_predeclared_six_term_targets(self):
        self.assertEqual(list(TERMS),["2023-02-04","2026-01-05","2026-02-04",
                                      "1912-12-07","2057-08-07","1965-12-07"])
        self.assertEqual(len(self.report["precise_JieQi_dates"]),6)
        self.assertEqual(self.report["source_solar_term_targets"],TERMS)

    def test_synthetic_36_boundary_original_inputs_same_order(self):
        prev=[x["fictional_clock"] for x in self.parent["precise_transition_boundary_cases"]]
        current=[x["fictional_reference_clock"] for x in self.report["original_36_boundary_synthetic_comparisons"]]
        self.assertEqual(prev,current)
        self.assertEqual(len(current),36)
        self.assertEqual(len(set(current)),36)

    def test_all_unanimity_and_nonunanimity_records_accounted_for(self):
        allrows=self.report["original_36_boundary_synthetic_comparisons"]
        nonunanimous=[x for x in allrows if x["status"]!="THREE_AGREE_NUMERICAL_ONLY"]
        self.assertEqual(len(nonunanimous),5)
        self.assertEqual({x["fictional_reference_clock"] for x in nonunanimous},CLOCKS_EXPECTED)
        self.assertEqual(len([x for x in allrows if x["status"]=="THREE_AGREE_NUMERICAL_ONLY"]),31)
        self.assertEqual(nonunanimous,self.report["all_three_model_nonunanimity_samples"])

    def test_original_four_two_library_conflicts_always_abstain(self):
        previous={x["fictional_clock"] for x in self.parent["precise_transition_disagreements"]}
        self.assertEqual(len(previous),4)
        this={x["fictional_reference_clock"] for x in self.report["all_three_model_nonunanimity_samples"]}
        self.assertTrue(previous.issubset(this))
        for row in self.report["all_three_model_nonunanimity_samples"]:
            self.assertTrue(row["status"].startswith("ABSTAIN_"))

    def test_new_unanimous_two_libraries_disagree_with_third(self):
        extra=[x for x in self.report["all_three_model_nonunanimity_samples"]
               if x["status"]=="ABSTAIN_TWO_WITNESSES_AGREE_AGAINST_THIRD"]
        self.assertEqual(len(extra),1)
        a=extra[0]
        self.assertEqual(a["fictional_reference_clock"],"2057-08-07T07:34:09")
        self.assertEqual(a["source_sxtwl_year_month"],a["source_lunar_python_year_month"])
        self.assertFalse(a["third_source_crossed_target"])
        self.assertFalse(a["source_sxtwl_matches_numerical_ephemeris"])
        self.assertFalse(a["source_lunar_python_matches_numerical_ephemeris"])
        self.assertEqual(self.report["two_calendar_libraries_agree_but_Moshier_diff_count"],1)

    def test_six_source_root_flags_and_angles(self):
        for row in self.report["precise_JieQi_dates"]:
            with self.subTest(day=row["JieQi_date"]):
                self.assertEqual(row["ephemeris_actual_flags"],260)
                self.assertEqual(row["solar_target_longitude_degrees"],TERMS[row["JieQi_date"]])
                self.assertAlmostEqual(row["model_solar_longitude_at_root_degrees"],
                                       TERMS[row["JieQi_date"]],delta=0.0000002)
                self.assertLess(row["model_root_iterations"],60)
                self.assertLess(row["model_root_max_halfwidth_seconds"],0.003)

    def test_moshier_not_vendor_swisseph_ephemeris_files(self):
        self.assertTrue(self.report["Moshier_implementation_not_JPL_ephemeris_files"])
        self.assertEqual(self.report["source_solar_positions_flags"],
                         "FLG_MOSEPH | FLG_SPEED, retflags 260")
        self.assertEqual(self.report["source_time_conversion"],
                         "original fixed UTC+8 reference clock minus 8h => UT Julian day => Swiss calc_ut")

    def test_root_times_against_observed_approximate_offsets(self):
        for row in self.report["precise_JieQi_dates"]:
            day=row["JieQi_date"]
            d=row["Moshier_minus_sxtwl_seconds"]
            self.assertAlmostEqual(d,THIRD_VS_SXTWL_OFFSETS[day],delta=0.005)

    def test_moshier_and_lunar_agree_at_five_of_six_to_within_one_second(self):
        residuals={x["JieQi_date"]:x["lunar_python_first_changed_second_minus_Moshier_seconds"]
                   for x in self.report["precise_JieQi_dates"]}
        for name,d in residuals.items():
            if name=="2057-08-07":
                self.assertLess(d,-10.0)
                self.assertGreater(d,-12.5)
            else:
                self.assertLess(abs(d),1.0)

    def test_solar_term_crossing_before_and_after_signs(self):
        swe=_astro_module()
        for row in self.report["precise_JieQi_dates"]:
            t=datetime.fromisoformat(row["source_third_clock"])
            target=row["solar_target_longitude_degrees"]
            with self.subTest(day=row["JieQi_date"]):
                self.assertLess(angular_error_degrees(t-timedelta(minutes=5),target,swe),0)
                self.assertGreater(angular_error_degrees(t+timedelta(minutes=5),target,swe),0)

    def test_untrusted_named_real_birth_timezone_rejected(self):
        swe=_astro_module()
        when=datetime(2026,2,4,4,2,tzinfo=timezone.utc)
        with self.assertRaises(SourceMismatch):
            tropical_geocentric_apparent_sun(when,swe)
        with self.assertRaises(SourceMismatch):
            tropical_geocentric_apparent_sun("2026-02-04 04:02 UTC",swe)

    def test_invalid_preselected_term_rejected(self):
        swe=_astro_module()
        with self.assertRaises(SourceMismatch):
            crossing(datetime(2026,2,4,4,0),300,swe)

    def test_package_version_mismatch_fail_closed(self):
        with patch("solve_third_moshier_solar_term.version",return_value="0.0.0"):
            with self.assertRaises(SourceMismatch):
                _astro_module()

    def test_binary_hash_mutation_fail_closed(self):
        with patch("solve_third_moshier_solar_term.BIN_SHA","0"*64):
            with self.assertRaises(SourceMismatch):
                _astro_module()

    def test_wrong_requested_or_returned_flags_rejected(self):
        swe=_astro_module()
        real=swe.calc_ut
        def corrupt(*args,**kwargs):
            coords,flags,message=real(*args,**kwargs)
            return coords,flags-256,message
        with patch.object(swe,"calc_ut",side_effect=corrupt):
            with self.assertRaises(SourceMismatch):
                tropical_geocentric_apparent_sun(datetime(2026,2,4,4,2),swe)

    def test_previous_report_hash_mutation_fail_closed(self):
        with patch("solve_third_moshier_solar_term.PREV_SHA","f"*64):
            with self.assertRaises(SourceMismatch):
                run()

    def test_case_by_case_recompute_matches_original_sha(self):
        replay=run()
        packed=json.dumps(replay,ensure_ascii=False,indent=2)+"\n"
        self.assertEqual(sha(packed.encode("utf-8")),FIXTURE_SHA)

    def test_no_human_or_runtime_predictions(self):
        self.assertEqual((self.report["human_birth_data_records"],
                          self.report["human_blind_predictive_accuracy_validated"],
                          self.report["runtime_astrology_rule_promotions"]),(0,0,0))
        self.assertFalse(self.report["independent_ancient_printed_BaZi_school_certified"])
        self.assertTrue(self.report["unresolved_2057_one_or_more_model_errors"])


if __name__=="__main__":
    unittest.main()
