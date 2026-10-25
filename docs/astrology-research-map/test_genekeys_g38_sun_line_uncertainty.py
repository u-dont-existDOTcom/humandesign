"""G38 source-only Sun/Gene-Key/Line complete-interval uncertainty guards."""
import importlib.util
import json
from decimal import Decimal
from pathlib import Path
import unittest

from genekeys_g38_sun_line_uncertainty import (
    THIS, source_sun_line_enclosure,synthetic_calendar_stability,
    LINE,GATE,ANCHOR,WINDOWS
)

DATA=THIS/"GENEKEYS_G38_SYNTHETIC_NATAL_SUN_LINE_UNCERTAINTY_V1.json"


class TestG38SunLineUncertainty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=json.loads(DATA.read_text(encoding="utf8"))

    def test_rave_mandala_exact_width_and_source_rule_independence(self):
        self.assertEqual(GATE,Decimal("5.625"))
        self.assertEqual(LINE,Decimal("0.9375"))
        self.assertEqual(ANCHOR,Decimal("302"))
        self.assertEqual(WINDOWS,(1,2,6,12,24))
        self.assertFalse(self.x["house_or_prenatal_Design_required_for_natal_Sun_line"])
        self.assertFalse(self.x["Gene_Keys_official_profile_parity_verified"])

    def test_natural_line_boundary_needs_known_birth_clock(self):
        stable=source_sun_line_enclosure(
            center_longitude="302.50",hours_width="1",max_abs_speed_deg_per_day="1.1")
        self.assertTrue(stable["line_stable_IF_speed_bound_and_UTC_interval_complete"])
        uncertain=source_sun_line_enclosure(
            center_longitude="302.92",hours_width="1",max_abs_speed_deg_per_day="1.1")
        self.assertFalse(uncertain["line_stable_IF_speed_bound_and_UTC_interval_complete"])
        self.assertEqual(uncertain["possible_line_numbers"],[1,2])
        self.assertTrue(uncertain["gate_stable_IF_speed_bound_and_UTC_interval_complete"])

    def test_gene_key_boundary_can_change_both_key_and_line(self):
        r=source_sun_line_enclosure(
            center_longitude="301.99",hours_width="2",max_abs_speed_deg_per_day="1.1")
        self.assertFalse(r["gate_stable_IF_speed_bound_and_UTC_interval_complete"])
        self.assertEqual(len(r["possible_gate_numbers"]),2)
        self.assertEqual(r["possible_line_numbers"],[1,6])
        self.assertFalse(r["line_stable_IF_speed_bound_and_UTC_interval_complete"])

    def test_closed_interval_zero_width_boundary_half_open(self):
        x=source_sun_line_enclosure(
            center_longitude="302",hours_width="0",max_abs_speed_deg_per_day="1.1")
        self.assertEqual(x["possible_line_numbers"],[1])
        self.assertTrue(x["gate_and_line_stable_IF_complete"])
        y=source_sun_line_enclosure(
            center_longitude="302",hours_width="1",max_abs_speed_deg_per_day="1.1")
        self.assertFalse(y["gate_stable_IF_speed_bound_and_UTC_interval_complete"])

    def test_duration_day_greater_than_one_line_width_always_conditional_ambiguity(self):
        x=source_sun_line_enclosure(
            center_longitude="310.5",hours_width=24,max_abs_speed_deg_per_day="1.1")
        self.assertEqual(x["conditional_motion_radius_degrees"],"0.55")
        self.assertFalse(x["line_stable_IF_speed_bound_and_UTC_interval_complete"])
        self.assertFalse(x["real_human_claim_admissible"])
        self.assertFalse(x["full_historical_Sun_max_speed_independently_proved"])

    def test_wrap_360_not_silently_meaning_new_mandala_boundary(self):
        r=source_sun_line_enclosure(
            center_longitude="359.99",hours_width="1",
            max_abs_speed_deg_per_day="1.1")
        self.assertIn(r["center_gate"],r["possible_gate_numbers"])
        self.assertIn(r["center_line"],r["possible_line_numbers"])
        self.assertTrue(all(1<=v<=6 for v in r["possible_line_numbers"]))

    def test_missing_or_invalid_inputs_fail(self):
        samples=[
            {"center_longitude":-1,"hours_width":1,"max_abs_speed_deg_per_day":1.1},
            {"center_longitude":360,"hours_width":1,"max_abs_speed_deg_per_day":1.1},
            {"center_longitude":"NaN","hours_width":1,"max_abs_speed_deg_per_day":1.1},
            {"center_longitude":302,"hours_width":49,"max_abs_speed_deg_per_day":1.1},
            {"center_longitude":302,"hours_width":-1,"max_abs_speed_deg_per_day":1.1},
            {"center_longitude":302,"hours_width":1,"max_abs_speed_deg_per_day":-1},
            {"center_longitude":302,"hours_width":1,"max_abs_speed_deg_per_day":"Infinity"},
            {"center_longitude":True,"hours_width":1,"max_abs_speed_deg_per_day":1.1}
        ]
        for v in samples:
            with self.subTest(v=v),self.assertRaises(ValueError):
                source_sun_line_enclosure(**v)

    def test_complete_2020_utc_day_counts_and_no_private_subjects(self):
        r=self.x
        self.assertEqual(len(r["synthetic_midpoints"]),366)
        self.assertTrue(r["zero_real_births_and_zero_human_outcomes"])
        self.assertFalse(r["owner_birth_or_other_person_data_used"])
        self.assertTrue(r["max_speed_not_independently_proved_across_the_actual_human_cohort"])
        counts=r["window_hour_counts"]
        self.assertEqual({k:counts[k]["conditionally_stable_lines"]
                          for k in ("1","2","6","12","24")},
                         {"1":350,"2":329,"6":261,"12":153,"24":0})
        self.assertEqual({k:counts[k]["conditionally_stable_gene_key_numbers"]
                          for k in ("1","2","6","12","24")},
                         {"1":364,"2":362,"6":350,"12":329,"24":293})
        for hours in ("1","2","6","12","24"):
            self.assertEqual(counts[hours]["conditionally_stable_joint_gate_line"],
                             counts[hours]["conditionally_stable_lines"])
            self.assertEqual(counts[hours]["ambiguous_line_midpoints"]+
                             counts[hours]["conditionally_stable_lines"],366)

    def test_reported_2020_UTC_calendar_not_actual_birth_census(self):
        self.assertEqual(self.x["calendar"],
                         "2020_leap_year_366_synthetic_midpoint_instants")
        self.assertTrue(self.x["zero_real_births_and_zero_human_outcomes"])
        self.assertEqual(self.x["Sun_declared_max_speed_deg_day"],1.1)
        self.assertFalse(self.x["house_or_prenatal_Design_required_for_natal_Sun_line"])

    @unittest.skipUnless(importlib.util.find_spec("swisseph"),
                         "real strict Swiss file provider not installed")
    def test_strict_swiss_full_year_replay_when_original_source_files_available(self):
        files=Path("/home/joel/humandesign/data/ephemeris")
        if not (files/"sepl_18.se1").is_file():
            self.skipTest("original authorized local Swiss source missing")
        self.assertEqual(synthetic_calendar_stability(files),self.x)


if __name__=="__main__":
    unittest.main()
