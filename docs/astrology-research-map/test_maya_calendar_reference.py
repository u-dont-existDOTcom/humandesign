#!/usr/bin/env python3
"""Small independent regression of source-declared Maya calendar arithmetic."""
from __future__ import annotations
from datetime import date,datetime,timedelta,timezone
import unittest

from maya_calendar_reference import (
    CalendarScopeError, CORRELATIONS, HAAB_MONTHS, YUCATEC_DAYS,
    KICHE_DAY_NAMES_BY_YUCATEC,
    proleptic_gregorian_jdn, reference_calendar_for_date,
)

class SmithsonianSourceExamples(unittest.TestCase):
    def test_smithsonian_2012_12_21_creations_cycle(self):
        a=reference_calendar_for_date(date(2012,12,21),correlation=584283)
        self.assertEqual(a["julian_day_number_integer"],2456283)
        self.assertEqual(a["long_count"],"13.0.0.0.0")
        self.assertEqual((a["tzolkin_number"],a["tzolkin_yucatec_name"]),(4,"AJAW"))
        self.assertEqual((a["haab_day"],a["haab_month"]),(3,"K’ANK’IN"))

    def test_smithsonian_2012_12_20_calendar_example(self):
        a=reference_calendar_for_date(date(2012,12,20))
        self.assertEqual(a["long_count"],"12.19.19.17.19")
        self.assertEqual((a["tzolkin_number"],a["tzolkin_yucatec_name"]),(3,"KAWAK"))
        self.assertEqual((a["haab_day"],a["haab_month"]),(2,"K’ANK’IN"))

    def test_smithsonian_2000_01_01_example(self):
        a=reference_calendar_for_date(date(2000,1,1))
        self.assertEqual(a["julian_day_number_integer"],2451545)
        self.assertEqual(a["long_count"],"12.19.6.15.2")
        self.assertEqual((a["tzolkin_number"],a["tzolkin_yucatec_name"]),(11,"IK’"))
        self.assertEqual((a["haab_day"],a["haab_month"]),(10,"K’ANK’IN"))

    def test_named_day_kiche_crosswalk_only_not_living_count(self):
        self.assertEqual((len(YUCATEC_DAYS),len(KICHE_DAY_NAMES_BY_YUCATEC)),(20,20))
        self.assertEqual((len(set(YUCATEC_DAYS)),len(set(KICHE_DAY_NAMES_BY_YUCATEC))),(20,20))
        i=YUCATEC_DAYS.index("CHUWEN")
        self.assertEqual(KICHE_DAY_NAMES_BY_YUCATEC[i],"B’ATZ’")
        a=reference_calendar_for_date(date(2012,12,21))
        self.assertEqual(a["kiche_label_from_practitioner_crosswalk_only"],"AJPU’")
        self.assertFalse(a["kiche_living_count_epoch_independently_verified"])

    def test_260_day_tzolkin_period_and_365_day_haab_period_are_different(self):
        first=reference_calendar_for_date(date(2020,1,1))
        after260=reference_calendar_for_date(date(2020,1,1)+timedelta(days=260))
        after365=reference_calendar_for_date(date(2020,1,1)+timedelta(days=365))
        self.assertEqual((first["tzolkin_number"],first["tzolkin_yucatec_name"]),
                         (after260["tzolkin_number"],after260["tzolkin_yucatec_name"]))
        self.assertNotEqual((first["haab_day"],first["haab_month"]),
                            (after260["haab_day"],after260["haab_month"]))
        self.assertEqual((first["haab_day"],first["haab_month"]),
                         (after365["haab_day"],after365["haab_month"]))

    def test_18980_day_calendar_round_returns_same_260_and_365_position(self):
        first=reference_calendar_for_date(date(1900,1,1))
        again=reference_calendar_for_date(date(1900,1,1)+timedelta(days=18980))
        self.assertEqual((first["tzolkin_number"],first["tzolkin_yucatec_name"],
                          first["haab_day"],first["haab_month"]),
                         (again["tzolkin_number"],again["tzolkin_yucatec_name"],
                          again["haab_day"],again["haab_month"]))

    def test_GMT_plus_two_remains_named_separate_policy(self):
        a=reference_calendar_for_date(date(2012,12,21),correlation=584283)
        b=reference_calendar_for_date(date(2012,12,21),correlation=584285)
        self.assertNotEqual(a["long_count"],b["long_count"])
        self.assertNotEqual((a["tzolkin_number"],a["tzolkin_yucatec_name"]),
                            (b["tzolkin_number"],b["tzolkin_yucatec_name"]))
        self.assertEqual(CORRELATIONS,(584283,584285))

    def test_month_lists_and_source_Kumku_base_day(self):
        self.assertEqual(len(HAAB_MONTHS),19)
        self.assertEqual(HAAB_MONTHS[17],"KUMK’U")
        self.assertEqual(HAAB_MONTHS[-1],"WAYEB")

    def test_february_29_and_adjacent_date_consistency(self):
        j1=proleptic_gregorian_jdn(date(2000,2,28))
        j2=proleptic_gregorian_jdn(date(2000,2,29))
        j3=proleptic_gregorian_jdn(date(2000,3,1))
        self.assertEqual((j2-j1,j3-j2),(1,1))

    def test_strings_and_datetime_forbidden(self):
        for value in ("2012-12-21",datetime(2012,12,21,0,0),
                      datetime(2012,12,21,12,0,tzinfo=timezone.utc)):
            with self.subTest(value=value):
                with self.assertRaises(CalendarScopeError):
                    reference_calendar_for_date(value)

    def test_other_GMT_or_invalid_argument_rejected(self):
        for x in (0,584284,584280,True,None,"584283"):
            with self.subTest(correlation=x):
                with self.assertRaises(CalendarScopeError):
                    reference_calendar_for_date(date(2012,12,21),correlation=x)

    def test_no_predictive_output_or_unsafe_real_person_chart(self):
        sample=reference_calendar_for_date(date(2012,12,21))
        self.assertFalse(sample["personality_or_fate_prediction_validated"])
        self.assertFalse(sample["eligible_to_score_a_human"])
        self.assertFalse(sample["birth_time_and_local_day_start_handled"])
        self.assertNotIn("personality",sample)
        self.assertNotIn("prediction_score",sample)

if __name__=="__main__":
    unittest.main()
