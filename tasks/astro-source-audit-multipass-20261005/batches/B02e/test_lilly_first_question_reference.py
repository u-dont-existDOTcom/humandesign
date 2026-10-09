"""Bounded source-reference tests. No empirical astrology validation."""
import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import unittest
import sys
from lilly_first_question_reference import (
    zodiac,decompose,fortune_position,angular_residual,house_age_bounds,
    phase_mnemonic,fortune_table_row,literal_quadrant_for_house,
    can_cast_to_fortune,exact_case_calculations,SIGNS)
ROOT=Path(__file__).resolve().parent

def data(name):
    return json.loads((ROOT/(name+'.json')).read_text())

class PositionTests(unittest.TestCase):
    def test_complete_sign_minute_roundtrip(self):
        for sign in SIGNS:
            for d,m in [(0,0),(0,1),(12,34),(29,59)]:
                self.assertEqual(decompose(zodiac(sign,d,m)),(sign,d,m))
    def test_bad_coordinates_rejected(self):
        for args in [('Aries',30,0),('Aries',-1,0),('Taurus',1,60),('Aries',True,0),('Ophiuchus',0,0)]:
            with self.assertRaises(ValueError):zodiac(*args)
        for pos in (-1,21600,0.5,True):
            with self.assertRaises(ValueError):decompose(pos)
    def test_fortune_worked_example(self):
        asc=zodiac('Leo',23,27);sun=zodiac('Aries',4,18);moon=zodiac('Virgo',21,18)
        p=fortune_position(asc,sun,moon,sect='day',profile='lilly_same_day_night')
        self.assertEqual(p,18627)
        self.assertEqual(decompose(p),('Aquarius',10,27))
        self.assertEqual((moon-sun)%21600,10020)
    def test_selected_fortune_method_does_not_reverse_at_night(self):
        args=(zodiac('Leo',23,27),zodiac('Aries',4,18),zodiac('Virgo',21,18))
        self.assertEqual(fortune_position(*args,sect='day',profile='lilly_same_day_night'),
                         fortune_position(*args,sect='night',profile='lilly_same_day_night'))
    def test_reported_reversal_is_explicit_alternative(self):
        a,s,m=1200,600,5400
        day=fortune_position(a,s,m,sect='day',profile='reported_nocturnal_reverse')
        night=fortune_position(a,s,m,sect='night',profile='reported_nocturnal_reverse')
        self.assertEqual(day,6000);self.assertEqual(night,18000)
        self.assertNotEqual(day,night)
    def test_fortune_no_implicit_profile_or_sect(self):
        with self.assertRaises(TypeError):fortune_position(0,0,0,sect='day')
        with self.assertRaises(ValueError):fortune_position(0,0,0,sect='day',profile='best_fit')
        with self.assertRaises(ValueError):fortune_position(0,0,0,sect='unknown',profile='lilly_same_day_night')
    def test_fortune_borrow_and_wrap(self):
        self.assertEqual(fortune_position(21590,21599,0,sect='night',profile='lilly_same_day_night'),21591)
        self.assertEqual(fortune_position(21599,0,1,sect='day',profile='lilly_same_day_night'),0)
    def test_static_aspect_residual_not_opposition_raw_difference(self):
        self.assertEqual(angular_residual(zodiac('Virgo',21,18),zodiac('Pisces',28,40),180),442)
        self.assertEqual(angular_residual(21599,1,0),2)
        with self.assertRaises(ValueError):angular_residual(0,1800,30)

class CaseTests(unittest.TestCase):
    def test_five_exact_static_intervals(self):
        d=exact_case_calculations()
        expected={'sun_beyond_ninth_cusp_arcminutes':130,
          'moon_mercury_opposition_residual_arcminutes':381,
          'moon_jupiter_trine_residual_arcminutes':186,
          'sun_to_aries_end_arcminutes':1542,
          'moon_mars_opposition_residual_arcminutes':442}
        self.assertEqual({k:d[k] for k in expected},expected)
    def test_no_invented_mean_or_chosen_calendar(self):
        d=exact_case_calculations()
        self.assertIsNone(d['moon_mars_mean_formula'])
        self.assertEqual(d['moon_mars_author_result_years'],'about three years and three quarters')
        self.assertEqual(d['moon_mars_other_stated_option_years'],'221/30')
        self.assertIs(d['physical_contact_times_computed'],False)
        self.assertIs(d['historical_calendar_resolved'],False)
        self.assertIs(d['personal_forecast'],False)
    def test_source_rounding_kept_separate(self):
        d=data('TIMING_CASES')
        by_id={r['id']:r for r in d['case_intervals']}
        self.assertEqual(by_id['T3']['exact_arcminutes'],186)
        self.assertIn('almost/about three',by_id['T3']['author_timing'])
        self.assertEqual(by_id['T4']['exact_arcminutes'],1542)
        self.assertIn('about26',by_id['T4']['author_timing'])
    def test_partial_chart_and_corrected_venus_glyph(self):
        d=data('CASE_REFERENCE')
        self.assertEqual(d['verified_positions']['Venus'],['Taurus',16,7])
        self.assertEqual(d['verified_positions']['Jupiter'],['Taurus',24,24])
        self.assertEqual(d['printed_heading']['day_raw'],'24.14. martij')
        self.assertIn('UNRESOLVED',d['printed_heading']['calendar_resolution'])
        self.assertTrue(any('not a complete' in t for t in d['limits']))
    def test_default_and_alternate_house_scales(self):
        self.assertEqual(house_age_bounds(12,years_per_house=5)['bounds_years'],[0,5])
        self.assertEqual(house_age_bounds(8,years_per_house=5)['bounds_years'],[20,25])
        self.assertEqual(house_age_bounds(1,years_per_house=5)['bounds_years'],[55,60])
        self.assertEqual(house_age_bounds(8,years_per_house=6)['bounds_years'],[24,30])
        self.assertEqual(house_age_bounds(1,years_per_house=6)['bounds_years'],[66,72])
    def test_scale_selection_and_boundaries_not_silently_resolved(self):
        d=house_age_bounds(8,years_per_house=6)
        self.assertIs(d['selection_not_determined'],True)
        self.assertEqual(d['boundary_inclusion'],'UNRESOLVED')
        with self.assertRaises(TypeError):house_age_bounds(8)
        for h,scale in [(0,5),(13,6),(1,7),(True,5)]:
            with self.assertRaises(ValueError):house_age_bounds(h,years_per_house=scale)
    def test_quadrants_are_literal_source_house_groups(self):
        self.assertEqual(literal_quadrant_for_house(10)['houses'],[12,11,10])
        self.assertEqual(literal_quadrant_for_house(9)['direction'],'South verging West')
        self.assertEqual(literal_quadrant_for_house(1)['direction'],'North inclining East')
        seen=[h for row in data('DIRECTIONAL_QUARTERS') for h in row['houses']]
        self.assertEqual(sorted(seen),list(range(1,13)))
        with self.assertRaises(ValueError):literal_quadrant_for_house(0)

class FortuneTableTests(unittest.TestCase):
    def test_four_exact_phase_mnemonics(self):
        for angle,h in [(0,1),(5400,4),(10800,7),(16200,10)]:
            row=phase_mnemonic(angle)
            self.assertEqual(row['source_exact_house'],h)
            self.assertIsNone(row['actual_house_from_cusps'])
            self.assertIsNone(row['source_interval_houses'])
    def test_intermediate_phases_not_actual_house_computation(self):
        for angle,hs in [(1,[1,2,3]),(6000,[4,5,6]),(12000,[7,8,9]),(21599,[10,11,12])]:
            row=phase_mnemonic(angle)
            self.assertEqual(row['source_interval_houses'],hs)
            self.assertIsNone(row['source_exact_house'])
            self.assertIsNone(row['actual_house_from_cusps'])
            self.assertEqual(row['status'],'SOURCE_MNEMONIC_NOT_HOUSE_ENGINE')
    def test_all_28_unique_strength_rows(self):
        d=data('FORTUNE_TABLE')
        self.assertEqual(len(d['rows']),28)
        self.assertEqual(len({r['id'] for r in d['rows']}),28)
        self.assertEqual(d['row_aggregation'],'UNSPECIFIED_NO_AUTOMATIC_NET_SCORE')
    def test_neutral_is_explicit_not_missing(self):
        r=fortune_table_row('N01')
        self.assertEqual(r['condition'],['Aries'])
        self.assertEqual(r['category'],'sign_neutral')
        self.assertEqual(r['magnitude'],0)
    def test_virgo_requires_terms_not_automatic_positive(self):
        r=fortune_table_row('S04')
        self.assertEqual(r['condition'],['Virgo'])
        self.assertIn('Only if',r['qualification'])
        self.assertIn('terms',r['qualification'])
    def test_fortune_table_not_planet_strength_table(self):
        self.assertEqual(fortune_table_row('A04')['magnitude'],3)
        self.assertEqual(fortune_table_row('D08')['magnitude'],4)
        self.assertEqual(fortune_table_row('D09')['magnitude'],4)
    def test_fixed_star_raw_positions_and_ocr_correction(self):
        self.assertEqual(fortune_table_row('F01')['condition'],['Regulus','Leo',24,34])
        self.assertEqual(fortune_table_row('F02')['condition'],['Spica Virginis','Libra',18,33])
        self.assertEqual(fortune_table_row('D10')['condition'],['Caput Algol','Taurus',20,54])
    def test_fortune_receives_does_not_cast_rays(self):
        self.assertIs(can_cast_to_fortune('Fortune'),False)
        for p in ('Saturn','Jupiter','Mars','Sun','Venus','Mercury','Moon'):
            self.assertIs(can_cast_to_fortune(p),True)
        with self.assertRaises(ValueError):can_cast_to_fortune('Uranus')
    def test_reference_rows_are_defensively_copied(self):
        row=fortune_table_row('S01');row['condition'].append('Aries')
        self.assertEqual(fortune_table_row('S01')['condition'],['Taurus','Pisces'])
        with self.assertRaises(ValueError):fortune_table_row('total_score')

class RecordTests(unittest.TestCase):
    def test_100_records_sequential_unique_ids(self):
        d=data('RULES');self.assertEqual(d['records_count'],100)
        self.assertEqual((d['first_record_number'],d['last_record_number']),(568,667))
        n=[int(r['id'].rsplit('R',1)[1]) for r in d['records']]
        self.assertEqual(n,list(range(568,668)))
        self.assertEqual(len({r['id'] for r in d['records']}),100)
    def test_source_scope_and_provenance(self):
        for r in data('RULES')['records']:
            loc=r['source_locator']
            self.assertEqual(loc['book'],'II')
            self.assertIn(loc['section_key'],('II.XXII','II.XXIII'))
            self.assertTrue(all(163<=p<=180 for p in loc['pdf_pages']))
            self.assertEqual(loc['source_sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
            self.assertEqual(r['statement_type'],'editor_normalized_paraphrase')
    def test_no_promotions_or_independence_inflation(self):
        for r in data('RULES')['records']:
            self.assertEqual(r['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertIs(r['independent_evidence_unit'],False)
        self.assertIs(data('FORTUNE_TABLE')['no_person_inference'],True)
    def test_all_25_issues_kept(self):
        issues=data('UNRESOLVED')['issues']
        self.assertEqual(len(issues),25)
        self.assertEqual(len({r['id'] for r in issues}),25)
        self.assertTrue({'timing_mean','functional_benefic','hindsight_exposure','author_admission'}.issubset({r['topic'] for r in issues}))
    def test_stated_death_caution_not_erased(self):
        rows={r['title']:r for r in data('RULES')['records']}
        r=rows['More testimony does not remove date caution']
        self.assertIn('absolute time of death',r['source_statement'])
        self.assertIn('not death',rows['Other-house misfortune is explicitly not death']['source_statement'])
    def test_deterministic_regeneration(self):
        names=['RULES','CASE_REFERENCE','TIMING_CASES','FORTUNE_TABLE','DIRECTIONAL_QUARTERS','STAR_NATURE_CATALOGUE','UNRESOLVED']
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'build_source_data.py';p.write_bytes((ROOT/'build_source_data.py').read_bytes())
            subprocess.run([sys.executable,str(p)],check=True,capture_output=True,text=True)
            for name in names:
                a=(ROOT/(name+'.json')).read_bytes();b=(Path(tmp)/(name+'.json')).read_bytes()
                self.assertEqual(hashlib.sha256(a).digest(),hashlib.sha256(b).digest())

if __name__=='__main__':unittest.main()
