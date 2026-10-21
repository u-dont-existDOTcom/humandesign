#!/usr/bin/env python3
"""Development-only independently reversible BaZi four-pillar source parity tests."""
from __future__ import annotations
from datetime import datetime,timezone,timedelta
from hashlib import sha256
from pathlib import Path
import json,unittest
from unittest.mock import patch

from dual_witness_bazi_fourpillars import (
    WitnessError,PILLARS,POLICY,PINNED_DEPENDENCIES,
    compare_fictional_reference_clock,sxtwl_fourpillars,lunar_python_fourpillars
)
from run_fictional_fourpillars_parity import (
    B,ROOT,OUTPUT,SOURCE_INDEX,SOURCE_INDEX_SHA,LIB_HOME,
    YEARS,BOUNDARY_DATES,TIME_OFFSETS,SEED,original_synthetic_samples,run,source_sha_roster
)

EXPECTED_REPORT_SHA="bf67f3a45078676a0ccf45c26b2296b1b7c7ec0249f1a434034885c57c8ee78e"
EXPECTED_INDEX_SHA="6e46e87ca2019945301b1f47f8d3ee91bd58c1a89461912d50bace74bc9543de"

def sha(b:bytes)->str:return sha256(b).hexdigest()

class BaZiJieQiSourceParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=OUTPUT.read_bytes()
        if sha(raw)!=EXPECTED_REPORT_SHA:
            raise ValueError("Frozen source development report bytes changed")
        cls.result=json.loads(raw.decode("utf-8"))

    def test_original_accepted_chinese_index_immutability(self):
        self.assertEqual(sha(SOURCE_INDEX.read_bytes()),EXPECTED_INDEX_SHA)
        i=json.loads(SOURCE_INDEX.read_text(encoding="utf-8"))
        self.assertEqual(i["sum_source_annotations"],1289)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in i["systems"]],
                         [(230,"BZI-R0231"),(1059,"ZWD-R1060")])
        self.assertEqual(i["independently_validated_real_human_claims"],0)

    def test_result_sha_and_516_fictional_clocks(self):
        self.assertEqual(sha(OUTPUT.read_bytes()),EXPECTED_REPORT_SHA)
        r=self.result
        self.assertEqual((len(r["ordinary_synthetic_cases"]),len(r["precise_transition_boundary_cases"])),(480,36))
        self.assertEqual(r["synthetic_clock_seed"],20261021)
        self.assertEqual((len(YEARS),len(BOUNDARY_DATES),len(TIME_OFFSETS)),(12,6,6))

    def test_exact_pin_two_different_versions_and_file_hashes(self):
        self.assertEqual(self.result["source_pinned_versions"],{"lunar-python":"1.4.8","sxtwl":"2.0.7"})
        actual=source_sha_roster()
        self.assertEqual(actual,self.result["source_library_files_SHA256_bytes"])
        self.assertGreaterEqual(len(actual),6)
        self.assertIn("_sxtwl.cpython-312-x86_64-linux-gnu.so",actual)

    def test_not_equivalent_to_original_print_or_correct_birth_chart(self):
        self.assertFalse(self.result["independently_authenticated_old_printed_BaZi_method"])
        self.assertTrue(self.result["synthetic_parity_does_not_establish_real_world_correctness"])
        self.assertEqual((self.result["actual_human_birth_inputs"],
                          self.result["independent_real_human_blind_accuracy_studies"],
                          self.result["astrology_runtime_rule_promotions"]),(0,0,0))
        self.assertEqual(POLICY["scope"],"FICTIONAL_PRECISE_REFERENCE_CLOCK_FIXED_UTC_PLUS_08_ONLY")
        self.assertEqual(POLICY["timezone_conversion_or_historical_tzif"],"NOT IMPLEMENTED")

    def test_ordinary_eight_raw_sxtwl_date_only_misses_retained(self):
        self.assertEqual(self.result["naive_sxtwl_day_level_mismatches"],8)
        misses=self.result["original_naive_jieqi_day_mismatch_cases"]
        self.assertEqual(len(misses),8)
        self.assertTrue(all(row["fictional_clock"].endswith(":30:00") for row in misses))
        self.assertEqual(len({row["fictional_clock"] for row in misses}),8)
        self.assertIn("2023-02-04T06:30:00",{row["fictional_clock"] for row in misses})

    def test_correction_eliminates_all_480_ordinary_library_differences(self):
        self.assertEqual(self.result["corrected_sxtwl_vs_lunar_python_mismatches"],0)
        self.assertTrue(all(row["agrees"] for row in self.result["ordinary_synthetic_cases"]))
        self.assertTrue(all(set(row["corrected_sxtwl_pillars"])==set(PILLARS)
                            for row in self.result["ordinary_synthetic_cases"]))
        self.assertTrue(all(row["corrected_sxtwl_pillars"]==row["independent_lunar_python_pillars"]
                            for row in self.result["ordinary_synthetic_cases"]))

    def test_actual_36_boundary_clock_statuses_preserved(self):
        b=self.result["precise_transition_boundary_cases"]
        self.assertEqual((len(b),sum(bool(row["different_pillars"]) for row in b)),(36,4))
        self.assertEqual(sum(x["status"]=="ABSTAIN_DIFFERENT_GANZHI_WITNESSES" for x in b),4)
        self.assertEqual({r["relative_to_sxtwl_Jie_seconds"] for r in b},set(TIME_OFFSETS))
        self.assertEqual(len({x["Jie_date"] for x in self.result["boundary_transition_switch_moments"]}),6)

    def test_exact_four_disagreeing_source_boundary_instants(self):
        wrong={row["fictional_clock"]:row for row in self.result["precise_transition_disagreements"]}
        self.assertEqual(set(wrong),{
            "2023-02-04T10:42:21","2026-01-05T16:22:54",
            "2026-02-04T04:01:52","2057-08-07T07:33:10"})
        self.assertEqual(wrong["2026-02-04T04:01:52"]["different_pillars"],["year","month"])
        self.assertEqual(wrong["2057-08-07T07:33:10"]["different_pillars"],["month"])
        self.assertTrue(all(x["relative_to_sxtwl_Jie_seconds"]==1 for x in wrong.values()))

    def test_six_lunar_python_vs_sxtwl_Jie_switch_offsets(self):
        got=[x["relative_switch_offset_seconds"] for x in self.result["boundary_transition_switch_moments"]]
        want=[12.143829,16.647186,16.607216,-0.093262,50.396576,-0.080078]
        for a,b in zip(got,want):
            self.assertAlmostEqual(a,b,places=3)
        self.assertEqual(len(got),6)

    def test_original_two_library_2026_term_disagreement_is_abstain(self):
        r=compare_fictional_reference_clock(datetime(2026,2,4,4,1,52))
        self.assertEqual(r["status"],"ABSTAIN_DIFFERENT_GANZHI_WITNESSES")
        self.assertEqual(r["difference_components"],["year","month"])
        self.assertEqual(r["source_sxtwl"]["pillars"]["year"],"丙午")
        self.assertEqual(r["source_lunar_python"]["pillars"]["year"],"乙巳")
        self.assertFalse(r["production_natal_chart_ready"])

    def test_on_2026_term_both_libraries_agree_before_and_after(self):
        for t in (datetime(2026,2,4,3,0),datetime(2026,2,4,5,0)):
            with self.subTest(t=t):
                r=compare_fictional_reference_clock(t)
                self.assertEqual(r["status"],"AGREE_ENGINEERING_ONLY")
                self.assertEqual(r["difference_components"],[])
                self.assertFalse(r["production_natal_chart_ready"])

    def test_unadjusted_day_early_2026_term_is_wrong_to_second_oracle(self):
        t=datetime(2026,2,4,3,0,0)
        naive=sxtwl_fourpillars(t,day_transition_correction=False)
        fixed=sxtwl_fourpillars(t,day_transition_correction=True)
        other=lunar_python_fourpillars(t)
        self.assertNotEqual(naive["pillars"]["year"],other["pillars"]["year"])
        self.assertEqual(fixed["pillars"],other["pillars"])
        self.assertTrue(fixed["sxtwl_lookup_corrected_to_previous_day"])

    def test_timezone_aware_or_birth_site_not_accepted(self):
        with self.assertRaises(WitnessError):
            compare_fictional_reference_clock(datetime(2026,2,4,4,0,tzinfo=timezone.utc))
        with self.assertRaises(WitnessError):
            compare_fictional_reference_clock("2026-02-04T04:00:00")

    def test_fractions_and_year_outside_study_range_rejected(self):
        for t in (datetime(2026,2,4,4,1,51,500000),datetime(1900,12,31),
                  datetime(2101,1,1)):
            with self.subTest(t=t):
                with self.assertRaises(WitnessError):
                    compare_fictional_reference_clock(t)

    def test_broken_external_dependency_version_rejected(self):
        with patch("dual_witness_bazi_fourpillars.version",return_value="0.0.0"):
            with self.assertRaises(WitnessError):
                compare_fictional_reference_clock(datetime(2026,2,4,4,0))

    def test_missing_library_route_fails_closed(self):
        with patch("dual_witness_bazi_fourpillars._import_witnesses",
                   side_effect=WitnessError("DELIBERATE_TEST_NO_LIBRARIES")):
            with self.assertRaisesRegex(WitnessError,"DELIBERATE_TEST_NO_LIBRARIES"):
                compare_fictional_reference_clock(datetime(2026,2,4,4,0))

    def test_mutated_source_witness_fails_model_agreement(self):
        ref=datetime(2026,2,4,5,0)
        baseline=sxtwl_fourpillars(ref)
        corrupted=dict(baseline)
        vals=dict(corrupted["pillars"])
        vals["month"]="INVALID_MOCK_MONTH"
        corrupted["pillars"]=vals
        with patch("dual_witness_bazi_fourpillars.sxtwl_fourpillars",return_value=corrupted):
            report=compare_fictional_reference_clock(ref)
            self.assertEqual(report["status"],"ABSTAIN_DIFFERENT_GANZHI_WITNESSES")
            self.assertEqual(report["difference_components"],["month"])

    def test_generator_reproduces_identical_source_report_sha(self):
        regenerated=run()
        # The report is serialized as indent 2, unicode exact and final newline.
        packed=json.dumps(regenerated,ensure_ascii=False,indent=2)+"\n"
        self.assertEqual(sha(packed.encode("utf-8")),EXPECTED_REPORT_SHA)

if __name__=="__main__":
    unittest.main()
