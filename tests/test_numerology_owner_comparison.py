"""Verify owner-development arithmetic and limited claims, not predictive truth."""
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import numerology_owner_comparison as m
import numerology_owner_context_checks as context
import numerology_owner_ancillary as ancillary
r=m.r
C=m.core()
D=m.diagnostics(C)
P=context.check()


class OwnerSourceArithmetic(unittest.TestCase):
    def test_exact_six_component_name(self):
        self.assertEqual(m.PARTS,['JOEL','EDWARD','SANE','TODD','DANIEL','ROSENBLUM'])
        self.assertEqual(sum(map(len,m.PARTS)),33)
        self.assertEqual(m.ROLES,['JOEL','EDWARDSANETODDDANIEL','ROSENBLUM'])

    def test_distinct_generating_compounds(self):
        self.assertEqual([C[m.DECOZ]['names'][k]['result']['raw'] for k in ['all','vowels','consonants']],[37,40,42])
        self.assertEqual([C[r.JORDAN]['names'][k]['result']['raw'] for k in ['all','vowels','consonants']],[28,31,24])
        self.assertEqual([C[m.DECOZ]['names'][k]['result']['root'] for k in ['all','vowels','consonants']],[1,4,6])

    def test_jb_W_branches_preserved_not_selected_for_fit(self):
        b=C[r.JB]['branches']
        self.assertEqual([b['literal_DW_vowel'][k]['result']['raw'] for k in ['vowels','consonants']],[63,73])
        self.assertEqual([b['ordinary_W_consonant_sensitivity'][k]['result']['raw'] for k in ['vowels','consonants']],[58,78])
        self.assertEqual(C[r.JB]['life_lesson']['admitted'],53)

    def test_triangle_ordinals_and_squares(self):
        t=C[r.JB]['triangle']
        self.assertEqual([x['letter'] for x in t['lines']],list('JOELEDWAR'))
        self.assertEqual([x['raw'] for x in t['squares']],[31,50,65])

    def test_2018_double41_is_minor_not_major(self):
        v=m.at(date(2018,7,1),C)['jb']
        self.assertEqual(v['year']['admitted'],41)
        self.assertEqual(v['active_major'],[])
        self.assertTrue(any(x['age']==33 and x['number']['admitted']==41 for x in v['active_minor']))

    def test_2013_january_does_not_borrow_age28(self):
        early=m.at(date(2013,1,12),C);late=m.at(date(2013,3,15),C)
        self.assertEqual(early['completed_age'],27)
        self.assertEqual(early['decoz']['essence']['root'],9)
        self.assertEqual(early['jb']['year']['admitted'],35)
        self.assertEqual(early['jb']['all_entries_at_age'],[])
        self.assertEqual(late['decoz']['essence']['root'],7)
        self.assertTrue(any(v['number']['admitted']==53 for v in late['jb']['all_entries_at_age']))

    def test_birth_is_before_2014_birthday(self):
        v=m.at(date(2014,1,12),C)
        self.assertEqual(v['completed_age'],28)
        self.assertEqual(v['jb']['year']['admitted'],36)
        self.assertEqual(v['jordan']['birth_start']['essence']['raw'],24)
        self.assertEqual(v['jordan']['display_age_minus_one']['essence']['raw'],22)

    def test_2026_uncertain_day_keeps_both_years(self):
        a=m.at(date(2026,1,28),C);b=m.at(date(2026,1,29),C)
        self.assertEqual((a['jb']['year']['admitted'],b['jb']['year']['admitted']),(39,40))
        self.assertEqual((a['completed_age'],b['completed_age']),(40,41))
        for x in [a,b]:self.assertTrue(any(v['number']['admitted']==50 for v in x['jb']['active_major']))

    def test_period16_is_not_unique_to_2014(self):
        self.assertEqual([v['start'] for v in P['literal_JB_third_period_16_windows']],['2005-09-29','2014-09-29','2023-09-29'])
        self.assertEqual(m.at(date(2014,9,28),C)['jb']['period_branches']['literal_DW_vowel']['admitted'],15)
        self.assertEqual(m.at(date(2014,9,29),C)['jb']['period_branches']['literal_DW_vowel']['admitted'],16)

    def test_long_cycle_and_ancillary_chart(self):
        x=ancillary.additional()
        self.assertEqual([p['root'] for p in x[m.DECOZ]['pinnacles']],[3,7,1,6])
        self.assertEqual(x['common_input_counts']['missing_digits'],[7,8])
        self.assertEqual(x[r.JORDAN]['security_root'],6)
        self.assertFalse(x[r.CAMPBELL]['squared_key_birthday'])


class ScopeAndErrorAccounting(unittest.TestCase):
    def test_36_definitions_22_distinct_predictions(self):
        self.assertEqual(len(D['results']),36)
        self.assertEqual(len({tuple(x['flagged_years']) for x in D['results']}),22)

    def test_unknowns_not_charged_as_false_positives(self):
        self.assertTrue(D['unlabelled_years_are_unknown'])
        for v in D['results']:
            self.assertTrue(set(v['lower_impact_false_flags']) <= {2008,2022})
            self.assertEqual(v['observed_impact_errors'],len(v['major_year_misses'])+len(v['lower_impact_false_flags']))
            self.assertFalse(set(v['unknown_flagged_years']) & {2008,2022})

    def test_union_adds_hit_and_error_not_better_total(self):
        a={v['adapter_id']:v for v in D['results']}
        one=a['CHEIRO_YEAR_HARMONY'];union=a['CHEIRO_YEAR_HARMONY__OR__LEGACY_WESTERN_CHANGE_SET']
        self.assertEqual((len(one['major_year_hits']),len(union['major_year_hits'])),(6,7))
        self.assertEqual((one['observed_impact_errors'],union['observed_impact_errors']),(3,3))
        self.assertEqual((one['coverage_years'],union['coverage_years']),(12,15))

    def test_no_coarse_candidate_beats_three_errors(self):
        self.assertEqual(min(x['observed_impact_errors'] for x in D['results']),3)
        self.assertTrue(all(2010 in x['major_year_misses'] for x in D['results']))

    def test_trivial_baseline_exposes_selected_labels(self):
        always_flag_errors=len(D['explicit_lower_impact_event_years'])
        self.assertEqual(always_flag_errors,2)
        self.assertLess(always_flag_errors,min(x['observed_impact_errors'] for x in D['results']))

    def test_new_filters_do_not_identify_unique_combination(self):
        self.assertEqual({tuple(x['years']) for x in P['hypotheses'].values()},{(2018,)})
        self.assertEqual(P['double5_years'],[2009,2018])
        self.assertEqual(P['status'],'POST_RESULT_HYPOTHESIS_NOT_VALIDATION')

    def test_2008_not_upgraded_and_2029_not_scored(self):
        e={v['id']:v for v in m.EVENTS}
        self.assertEqual(e['relationship_rupture_2008']['impact'],'moderate')
        self.assertEqual(e['mother_loss']['impact'],'low')
        self.assertNotIn(2029,D['calendar_years'])
        self.assertIsNone(P['future_2029_not_scored']['observed_outcome'])

    def test_frozen_source_payloads_unchanged(self):
        manifest=json.loads((ROOT/'reference/research/numerology_v2_20261004/freeze_manifest.json').read_text())
        for path,digest in {**manifest['files'],**manifest['immutable_baseline_files']}.items():
            data=(ROOT/path).read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            with self.subTest(path=path):self.assertEqual(actual,digest)

    def test_event_chronology_quality_not_documentary_from_precision(self):
        permitted={'documentary/contemporaneous','strongly anchored memory','approximate memory','uncertain'}
        self.assertTrue(all(e['quality'] in permitted for e in m.EVENTS))
        self.assertTrue(all(e['quality']!='documentary/contemporaneous' for e in m.EVENTS))


if __name__=='__main__':unittest.main(verbosity=2)
