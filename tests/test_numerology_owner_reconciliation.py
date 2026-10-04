"""Regression checks for concrete reviewer findings; no human-validity claim."""
from datetime import date
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import numerology_owner_comparison as m
import numerology_owner_reconciliation as reviewed
C=m.core();R=reviewed.checks()


class ReviewRegressions(unittest.TestCase):
    def test_36_reduces_to9_not6(self):
        for system in [m.r.CAMPBELL,m.r.JORDAN]:
            v=m.r.tape(m.PARTS,20,system)['essence']
            self.assertEqual((v['raw'],v['root']),(36,9))

    def test_2020_year_and_experience_must_be_concurrent(self):
        early=m.at(date(2020,1,28),C)['jb'];late=m.at(date(2020,1,29),C)['jb']
        self.assertEqual((early['year']['admitted'],late['year']['admitted']),(42,34))
        self.assertEqual({v['number']['admitted'] for v in early['all_entries_at_age']},{29})
        self.assertEqual({v['number']['admitted'] for v in late['all_entries_at_age']},{53})

    def test_jordan_alternate_branch_not_hidden(self):
        for d in [date(2013,3,15),date(2014,1,12)]:
            j=m.at(d,C)['jordan']
            self.assertEqual((j['birth_start']['essence']['raw'],j['display_age_minus_one']['essence']['raw']),(24,22))

    def test_simple_registered_filters_already_select2018(self):
        rows=R['already_registered_simpler_separators']
        self.assertEqual(len(rows),2)
        for row in rows:
            self.assertEqual(row['flagged_years'],[2018])
            self.assertEqual(row['observed_impact_errors'],7)

    def test_root_equality_does_not_discriminate2008(self):
        self.assertEqual(R['root_match_years'],[2008,2018])
        self.assertEqual(R['exact_match_years'],[2018])
        self.assertEqual(R['possible_experience_compounds_within_observed_PY_range'],[34,36,41])

    def test_shift_is_stress_test_not_a_new_source_branch(self):
        self.assertEqual(R['counterfactual_age_plus_one_match_years'],[])
        self.assertEqual(R['shift_status'],'UNSOURCED_ROBUSTNESS_PROBE_NOT_AN_ADMITTED_JB_AGE_BRANCH')

    def test_romantic_annual_language_is_common(self):
        self.assertEqual(R['romance_vocabulary_lower_bound']['count'],15)
        self.assertEqual(R['romance_vocabulary_lower_bound']['denominator'],27)
        self.assertIn(2002,R['romance_vocabulary_lower_bound']['years'])
        self.assertIn(2020,R['romance_vocabulary_lower_bound']['years'])

    def test_both_W_period_branches_reported(self):
        x=R['third_period16_windows_by_W_branch']
        self.assertEqual([v['start'][:4] for v in x['ordinary_W_consonant_sensitivity']],['2001','2010','2019'])
        self.assertEqual([v['start'][:4] for v in x['literal_DW_vowel']],['2005','2014','2023'])

    def test_saved_reconciliation_reproducible(self):
        actual=json.loads((m.OUT/'review_reconciliation_checks.json').read_text())
        self.assertEqual(actual,R)
        actual_t=json.loads((m.OUT/'transparency_controls.json').read_text())
        self.assertEqual(actual_t,reviewed.transparency())


if __name__=='__main__':unittest.main()
