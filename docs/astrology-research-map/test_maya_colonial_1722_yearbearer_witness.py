#!/usr/bin/env python3
"""Colonial K'iche' yearbearer source-table checks: NOT empirical natal claims."""
import json
from pathlib import Path
from datetime import date, timedelta
import unittest
from maya_calendar_reference import reference_calendar_for_date

SRC=json.loads(Path(__file__).with_name(
  "MAYA_1722_COLONIAL_KICHE_YEARBEARER_WITNESS_V1.json").read_text(encoding="utf-8"))

class ColonialKiche1722YearbearerChecks(unittest.TestCase):
    def test_copy_and_modern_edition_are_same_original_lineage(self):
        a=SRC["primary_source_trace"]
        self.assertEqual(a["manuscript_origin_year"],1722)
        self.assertEqual(a["holding"],"University of Pennsylvania Library, Berendt-Brinton Linguistic Collection, Ms. Coll. 700 Item 58")
        self.assertIn("1877",a["transmission"])
        self.assertFalse(SRC["evidence_scope"]["original_script_1722_fully_read"])
        self.assertTrue(SRC["scholarly_reading"]["source_independence"])

    def test_1722_day_label_weekday_and_classic_lowland_haab(self):
        a=SRC["first_civil_date_anchor"]
        d=date.fromisoformat(a["date"])
        self.assertEqual(d.strftime("%A"),a["calendar_weekday"])
        c=reference_calendar_for_date(d,correlation=584283)
        self.assertEqual((c["tzolkin_number"],c["kiche_label_from_practitioner_crosswalk_only"],
                          c["tzolkin_yucatec_name"]), (9,"KEJ","MANIK’"))
        self.assertEqual((c["haab_day"],c["haab_month"]),(5,"K’AYAB"))
        self.assertEqual(a["origin"].split(",")[0].split(" printed p.")[0],"2016 government work")

    def test_1722_lowland_haab_at_exactly_plus_40_days(self):
        d=date(1722,5,3)
        next_day=d+timedelta(days=40)
        c=reference_calendar_for_date(next_day)
        self.assertEqual(next_day.isoformat(),"1722-06-12")
        self.assertEqual((c["haab_day"],c["haab_month"]),(0,"POP"))
        self.assertTrue(SRC["first_civil_date_anchor"]["forty_day_offset_is_2016_author_model"])

    def test_all_nine_2016_gov_source_rows_match_declared_GMT_584283_math(self):
        records=SRC["later_source_table_date_rows"]
        self.assertEqual(len(records),9)
        self.assertEqual(len({r["civil"] for r in records}),8)
        for r in records:
            with self.subTest(date=r["civil"],community=r["community"]):
                c=reference_calendar_for_date(date.fromisoformat(r["civil"]))
                self.assertEqual((c["tzolkin_number"],c["kiche_label_from_practitioner_crosswalk_only"]),
                                 (r["reported"],r["sign"]))
                self.assertEqual((c["haab_day"],c["haab_month"]),
                                 (r["printed_haab_day"],r["printed_haab_month"]))

    def test_plus_one_mutant_is_not_the_same_1722_civil_label(self):
        original=reference_calendar_for_date(date(1722,5,3))
        shifted=reference_calendar_for_date(date(1722,5,4))
        self.assertNotEqual((original["tzolkin_number"],original["tzolkin_yucatec_name"]),
                            (shifted["tzolkin_number"],shifted["tzolkin_yucatec_name"]))

    def test_alternative_GMT_is_not_a_silent_source_replacement(self):
        d=date(1722,5,3)
        a=reference_calendar_for_date(d,correlation=584283)
        b=reference_calendar_for_date(d,correlation=584285)
        self.assertEqual((a["tzolkin_number"],a["kiche_label_from_practitioner_crosswalk_only"]),(9,"KEJ"))
        self.assertNotEqual((b["tzolkin_number"],b["kiche_label_from_practitioner_crosswalk_only"]),
                            (a["tzolkin_number"],a["kiche_label_from_practitioner_crosswalk_only"]))

    def test_no_human_claim_from_calendar_source(self):
        x=SRC["evidence_scope"]
        self.assertFalse(x["are_all_rows_independent"])
        self.assertFalse(x["community_natal_birth_clock_verified"])
        self.assertEqual(x["untouched_human_predictive_validations"],0)
        self.assertEqual(x["production_model_promotions"],0)
        self.assertFalse(SRC["first_civil_date_anchor"]["source_sign_and_solar_pair_independence"]=="INDEPENDENT_CONFIRMATION")

if __name__=="__main__":
    unittest.main()
