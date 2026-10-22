#!/usr/bin/env python3
"""Fictional SWIEPH solar term source-compare checks, not human astrology evaluation."""
from __future__ import annotations
from datetime import datetime,timezone,timedelta
from hashlib import sha256
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from calculate_swieph_fourth_oracle import (
    B,ROOT,THIRD,PIN,OUTPUT,DATA,BINARY,THIRD_SHA,SEPL_SHA,SEMO_SHA,BINARY_SHA,
    SOURCE_FLAG,FourthSourceError,sha,rd,source_swisseph,
    solar_apparent_geocentric_lon,difference,crossing,run
)

EXPECTED_SHA="7826f65e9dbff6142064a356c55c61a0ba659d423490bb59775dd0f563dd7e0d"
ACCEPTED_CHINESE=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V30.json"
V30_SHA="6e46e87ca2019945301b1f47f8d3ee91bd58c1a89461912d50bace74bc9543de"
EXPECTED_CLOCKS={
    "2023-02-04T10:42:21","2026-01-05T16:22:54",
    "2026-02-04T04:01:52","2057-08-07T07:33:10","2057-08-07T07:34:09"
}
EXPECTED_SWIEPH_MINUS_MOSHIER={
    "2023-02-04":0.640513,
    "2026-01-05":0.470568,
    "2026-02-04":0.171877,
    "1912-12-07":-0.403617,
    "2057-08-07":-0.540088,
    "1965-12-07":0.730636
}

class SourcePinnedSWIEPHFourth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=rd(OUTPUT)
        cls.third=rd(THIRD)
        cls.manifest=rd(PIN)

    def test_original_accepted_historical_source_registry_unchanged(self):
        self.assertEqual(sha(ACCEPTED_CHINESE.read_bytes()),V30_SHA)
        index=rd(ACCEPTED_CHINESE)
        self.assertEqual((index["sum_source_annotations"],index["systems"][0]["accepted_source_annotations"],
                          index["systems"][1]["accepted_source_annotations"]),(1289,230,1059))
        self.assertEqual((index["independently_validated_real_human_claims"],index["runtime_promotions"]),(0,0))

    def test_exact_parent_moshier_report_sha_unchanged(self):
        self.assertEqual(sha(THIRD.read_bytes()),THIRD_SHA)
        self.assertEqual((len(self.third["precise_JieQi_dates"]),len(self.third["original_36_boundary_synthetic_comparisons"])),(6,36))
        self.assertEqual(self.report["parent_third_source_report_SHA256"],THIRD_SHA)

    def test_fourth_report_original_sha_and_fixed_case_universe(self):
        self.assertEqual(sha(OUTPUT.read_bytes()),EXPECTED_SHA)
        self.assertEqual((len(self.report["six_term_swieph_apparent_geocentric_Sun_crossings"]),
                          len(self.report["all_original_36_fictional_fixed_UTC8_clock_comparisons"])),(6,36))
        self.assertEqual(self.report["status"],"ENGINEERING_COMPARISON_ONLY_NOT_REAL_CHINESE_BIRTH_CHART_VALIDATION")

    def test_compressed_original_source_ephemeris_file_sha_and_bytes(self):
        self.assertEqual((DATA/"sepl_18.se1").stat().st_size,484061)
        self.assertEqual(sha((DATA/"sepl_18.se1").read_bytes()),SEPL_SHA)
        self.assertEqual((DATA/"semo_18.se1").stat().st_size,1304771)
        self.assertEqual(sha((DATA/"semo_18.se1").read_bytes()),SEMO_SHA)
        source_manifest=rd(DATA/"swisseph_ephemeris_manifest.json")
        self.assertEqual(source_manifest["source_commit"],"3fd0f956d73898b91cc4f67cf18b21af656d1342")

    def test_swieph_wrapper_binary_loaded_and_returned_flags(self):
        swe=source_swisseph()
        self.assertEqual(Path(swe.__file__).resolve(),BINARY.resolve())
        self.assertEqual(sha(BINARY.read_bytes()),BINARY_SHA)
        self.assertEqual(swe.FLG_SWIEPH|swe.FLG_SPEED,258)
        self.assertEqual(SOURCE_FLAG,258)
        p,ret,_=solar_apparent_geocentric_lon(datetime(2057,8,7,7,34),swe)
        self.assertEqual(ret,258)
        self.assertGreater(p,134.999)

    def test_root_model_returns_swieph_not_moshier_flags(self):
        self.assertTrue(self.report["source_Swiss_EPHE_return_flags_258_required"])
        self.assertTrue(self.report["source_Swiss_prior_Moshier_flag_260_is_distinct"])
        for row in self.report["six_term_swieph_apparent_geocentric_Sun_crossings"]:
            self.assertEqual(row["returned_ephemeris_flags"],258)
            self.assertEqual(row["root_bracket_precision_seconds"],.002)

    def test_all_six_original_jieqi_dates_and_exact_angles(self):
        expected=list(self.manifest["original_6_dates"])
        self.assertEqual(expected,["2023-02-04","2026-01-05","2026-02-04","1912-12-07","2057-08-07","1965-12-07"])
        rows=self.report["six_term_swieph_apparent_geocentric_Sun_crossings"]
        self.assertEqual([r["JieQi_reference_date"] for r in rows],expected)
        for row in rows:
            self.assertEqual(row["angle_target_degrees"],self.manifest["original_6_dates"][row["JieQi_reference_date"]])
            self.assertAlmostEqual(row["geocentric_apparent_tropical_sun_longitude_degrees"],row["angle_target_degrees"],delta=.0000002)

    def test_third_vs_fourth_all_six_crossings_within_one_second(self):
        for row in self.report["six_term_swieph_apparent_geocentric_Sun_crossings"]:
            day=row["JieQi_reference_date"]
            self.assertAlmostEqual(row["SWIEPH_minus_Moshier_seconds"],EXPECTED_SWIEPH_MINUS_MOSHIER[day],delta=.002)
            self.assertLess(abs(row["SWIEPH_minus_Moshier_seconds"]),.8)

    def test_original_all_36_clock_identities_preserved(self):
        old=[r["fictional_reference_clock"] for r in self.third["original_36_boundary_synthetic_comparisons"]]
        new=[r["original_fictional_fixed_UTC8_reference_clock"] for r in self.report["all_original_36_fictional_fixed_UTC8_clock_comparisons"]]
        self.assertEqual(old,new)
        self.assertEqual(len(set(new)),36)

    def test_cumulative_5_nonunanimous_31_agree(self):
        self.assertEqual((self.report["all_four_nonunanimity_count"],self.report["all_four_unanimity_count"]),(5,31))
        rows=self.report["all_four_nonunanimity_clocks"]
        self.assertEqual(len(rows),5)
        self.assertEqual({r["original_fictional_fixed_UTC8_reference_clock"] for r in rows},EXPECTED_CLOCKS)
        self.assertTrue(all(x["status"].startswith("ABSTAIN_") for x in rows))

    def test_new_2057_two_calendar_agreement_vs_kernel(self):
        rows=self.report["new_two_calendar_consensus_against_SWIEPH_clocks"]
        self.assertEqual(len(rows),1)
        sample=rows[0]
        self.assertEqual(sample["original_fictional_fixed_UTC8_reference_clock"],"2057-08-07T07:34:09")
        self.assertEqual(sample["original_sxtwl_reported_year_month"],sample["original_lunar_python_reported_year_month"])
        self.assertFalse(sample["source_sxtwl_matches_swieph"])
        self.assertFalse(sample["source_lunar_python_matches_swieph"])
        self.assertFalse(sample["source_swieph_sun_crossed_target"])
        self.assertLess(sample["source_swieph_sun_minus_target_arcseconds"],0)

    def test_2057_solar_crossing_and_lunar_library_second(self):
        row=next(x for x in self.report["six_term_swieph_apparent_geocentric_Sun_crossings"] if x["JieQi_reference_date"]=="2057-08-07")
        self.assertEqual(row["SWIEPH_term_reference_clock"][:19],"2057-08-07T07:34:10")
        self.assertLess(row["lunar_python_minus_SWIEPH_seconds"],-10.0)
        self.assertGreater(row["lunar_python_minus_SWIEPH_seconds"],-11.0)

    def test_other_five_lunar_switches_within_one_second_of_swieph(self):
        for row in self.report["six_term_swieph_apparent_geocentric_Sun_crossings"]:
            if row["JieQi_reference_date"]!="2057-08-07":
                self.assertLess(abs(row["lunar_python_minus_SWIEPH_seconds"]),1.0)

    def test_kernel_solar_term_root_low_and_high_signs(self):
        swe=source_swisseph()
        for row in self.report["six_term_swieph_apparent_geocentric_Sun_crossings"]:
            t=datetime.fromisoformat(row["SWIEPH_term_reference_clock"])
            target=row["angle_target_degrees"]
            with self.subTest(day=row["JieQi_reference_date"]):
                self.assertLess(difference(t-timedelta(minutes=3),target,swe),0)
                self.assertGreater(difference(t+timedelta(minutes=3),target,swe),0)

    def test_refuse_fake_real_birth_timezone(self):
        swe=source_swisseph()
        with self.assertRaises(FourthSourceError):
            solar_apparent_geocentric_lon(datetime(2026,2,4,4,2,tzinfo=timezone.utc),swe)
        with self.assertRaises(FourthSourceError):
            solar_apparent_geocentric_lon("birthtime 4:02am",swe)

    def test_refuse_unselected_solar_target(self):
        swe=source_swisseph()
        with self.assertRaises(FourthSourceError):
            crossing(datetime(2026,2,4,4,0),270,swe)

    def test_mocked_wrong_return_flags_rejected(self):
        swe=source_swisseph()
        real=swe.calc_ut
        def wrong(*args,**kwargs):
            coordinates,ret,warn=real(*args,**kwargs)
            return coordinates,260,warn
        with patch.object(swe,"calc_ut",side_effect=wrong):
            with self.assertRaises(FourthSourceError):
                solar_apparent_geocentric_lon(datetime(2026,2,4,4,2),swe)

    def test_manifest_mutation_fails_closed(self):
        with patch("calculate_swieph_fourth_oracle.SEPL_SHA","0"*64):
            with self.assertRaises(FourthSourceError):
                source_swisseph()

    def test_third_report_mutation_fails_closed(self):
        with patch("calculate_swieph_fourth_oracle.THIRD_SHA","f"*64):
            with self.assertRaises(FourthSourceError):
                run()

    def test_report_recomputation_exact_hash(self):
        doc=run()
        buffer=(json.dumps(doc,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
        self.assertEqual(sha(buffer),EXPECTED_SHA)

    def test_no_ancient_printed_edition_or_human_predictions(self):
        self.assertFalse(self.report["historical_Chinese_original_printed_source_independently_verified"])
        self.assertEqual((self.report["human_birth_input_records"],
                          self.report["real_blinded_human_predictive_validations"],
                          self.report["runtime_astrology_rule_promotions"]),(0,0,0))


if __name__=="__main__":
    unittest.main()
