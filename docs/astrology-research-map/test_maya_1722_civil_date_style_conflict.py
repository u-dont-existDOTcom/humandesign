#!/usr/bin/env python3
"""Historical European date-style sensitivity: NOT a Mayan natal-day scorer.

For 1722-1723 only, same written day/month/year under a Julian
interpretation corresponds to the Gregorian date eleven days later.
No source date policy is selected from an outcome-match rate.
"""
from datetime import date, timedelta
from pathlib import Path
import json
import unittest
from maya_calendar_reference import reference_calendar_for_date

DIR=Path(__file__).resolve().parent
B04=json.loads((DIR/"MAYA_1722_PRIMARY_FACSIMILE_HAND_READ_B04.json").read_text(encoding="utf-8"))
B06=json.loads((DIR/"MAYA_1722_JULIAN_GREGORIAN_SOURCE_DISCREPANCY_B06.json").read_text(encoding="utf-8"))

def historical_candidates(written_label:date):
    if type(written_label) is not date or written_label.year not in (1722,1723):
        raise ValueError("Only 1722/1723 European date-label counterfactuals are in scope")
    result=[]
    for policy,days in (("AS_GREGORIAN",0),("AS_JULIAN",11)):
        d=written_label+timedelta(days=days)
        a=reference_calendar_for_date(d,correlation=584283)
        result.append((policy,d.isoformat(),a["tzolkin_number"],
                       a["kiche_label_from_practitioner_crosswalk_only"]))
    return tuple(result)

class JulianGregorianHistoricalDescriptorConflictTests(unittest.TestCase):
    def test_1722_first_handwritten_row_sensitive_to_civil_style(self):
        x=historical_candidates(date(1722,5,3))
        self.assertEqual(x[0],("AS_GREGORIAN","1722-05-03",9,"KEJ"))
        self.assertEqual(x[1],("AS_JULIAN","1722-05-14",7,"TIJAX"))

    def test_all_thirty_original_handread_date_rows_under_fixed_correlation(self):
        r=B04["observed_1722_1723_date_rows"]
        self.assertEqual(len(r),30)
        fit={"AS_GREGORIAN":0,"AS_JULIAN":0}
        for witness in r:
            for policy,_,num,name in historical_candidates(date.fromisoformat(witness["gregorian"])):
                fit[policy] += (num,name)==(witness["number"],witness["normalized_kiche"])
        self.assertEqual(fit,{"AS_GREGORIAN":30,"AS_JULIAN":0})
        self.assertEqual(B06["fixed_comparison"]["observed_gregorian_same_label_parity_count"],30)
        self.assertEqual(B06["fixed_comparison"]["observed_julian_same_label_parity_count"],0)

    def test_no_source_policy_promoted_by_better_match(self):
        scope=B06["fixed_comparison"]
        self.assertFalse(scope["source_style_independently_confirmed"])
        self.assertTrue(scope["no_calendar_choice_from_trait_fit"])
        self.assertTrue(B06["boundary"]["prohibit_silent_julian_or_gregorian_policy_promotion"])
        self.assertEqual(B06["boundary"]["untouched_human_predictions"],0)

    def test_structural_52_groups_are_civil_date_style_invariant(self):
        self.assertTrue(B06["fixed_comparison"]["all_52_historical_5_by_52_group_names_independent_of_civil_date_style"])
        self.assertTrue(B06["boundary"]["previous_B04_direct_group_photographs_remain_valid"])

    def test_invalid_outside_scope_dates_and_datetimes_refused(self):
        from datetime import datetime
        for bad in (date(1700,5,3),date(1800,5,3),datetime(1722,5,3),"1722-05-03",None):
            with self.subTest(bad=str(bad)):
                with self.assertRaises(ValueError):
                    historical_candidates(bad)

    def test_historical_source_classes_not_counted_as_independent_oracles(self):
        a=B06["sources"]
        self.assertEqual(len(a),4)
        self.assertEqual({s["id"] for s in a},
                         {"FAMSI_1722_FOLIO","NEWBERRY_LIBRARY_2026_BIBLIOGRAPHY",
                          "GARAY_XOYON_2016","WEEKS_SACHSE_PRAGER_2009_INTRO"})
        self.assertTrue([s for s in a if s["id"]=="NEWBERRY_LIBRARY_2026_BIBLIOGRAPHY"][0]["shares_upenn_famsi_archive_metadata"])
        self.assertEqual(B06["boundary"]["natal_claims_derived_from_calendar_style"],0)

if __name__=="__main__":
    unittest.main()
