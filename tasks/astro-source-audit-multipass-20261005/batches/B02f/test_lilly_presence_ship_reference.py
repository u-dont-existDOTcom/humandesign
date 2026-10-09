"""Bounded source/reference checks. Passing tests do not validate astrology."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

import lilly_presence_ship_reference as ref

ROOT = Path(__file__).resolve().parent


def data(name):
    return json.loads((ROOT / (name + '.json')).read_text())


class QueryFrameTests(unittest.TestCase):
    def test_question_changes_unrelated_person_role(self):
        self.assertEqual(ref.person_house_reference('at_home', 'unrelated_familiar')['radical_house'], 7)
        self.assertEqual(ref.person_house_reference('general_absent', 'unrelated')['radical_house'], 1)

    def test_actual_relative_roles(self):
        for relation, house in {'father':4, 'mother':10, 'child':5, 'sibling':3, 'neighbour':3}.items():
            self.assertEqual(ref.person_house_reference('at_home', relation)['radical_house'], house)

    def test_unknown_frame_or_role_not_filled(self):
        for args in [('natal','unrelated'), ('at_home','employee'), ('general_absent','father')]:
            with self.assertRaises(ValueError):
                ref.person_house_reference(*args)

    def test_presence_three_categories(self):
        self.assertEqual(ref.presence_category_reference('angular')['houses'], [1,4,7,10])
        self.assertEqual(ref.presence_category_reference('succedent')['claim'], 'not far from home')
        self.assertEqual(ref.presence_category_reference('cadent')['claim'], 'far from home')
        with self.assertRaises(ValueError):
            ref.presence_category_reference('unknown')

    def test_turned_spouse_and_child_sixths(self):
        self.assertEqual(ref.turned_house(7,6), 12)
        self.assertEqual(ref.turned_house(5,6), 10)
        self.assertEqual(ref.turned_house(12,2), 1)
        for args in [(0,6),(7,13),(True,6)]:
            with self.assertRaises(ValueError):
                ref.turned_house(*args)

    def test_beyond_five_degree_negative_example(self):
        self.assertTrue(ref.beyond_cusp_window(301))
        self.assertTrue(ref.beyond_cusp_window(500))
        self.assertIsNone(ref.beyond_cusp_window(300))
        self.assertIsNone(ref.beyond_cusp_window(299))
        self.assertIsNone(ref.beyond_cusp_window(0))
        with self.assertRaises(ValueError):
            ref.beyond_cusp_window(-1)

    def test_returned_reference_is_defensive_copy(self):
        obj = ref.presence_category_reference('angular')
        obj['houses'].append(12)
        self.assertEqual(ref.presence_category_reference('angular')['houses'], [1,4,7,10])


class TimingTests(unittest.TestCase):
    def test_symbolic_units_source_profile(self):
        for modality,unit in [('moveable','days'),('common','weeks'),('fixed','months')]:
            result = ref.news_symbolic_interval(600, modality, profile=ref.NEWS_PROFILE)
            self.assertEqual(result['quantity'], '10')
            self.assertEqual(result['unit'], unit)
            self.assertFalse(result['civil_date_computed'])
            self.assertFalse(result['is_forecast'])

    def test_fraction_not_rounded_to_integer(self):
        result = ref.news_symbolic_interval(442,'common',profile=ref.NEWS_PROFILE)
        self.assertEqual(result['quantity'], '221/30')
        self.assertEqual(result['unit'], 'weeks')

    def test_no_implicit_timing_profile(self):
        with self.assertRaises(TypeError):
            ref.news_symbolic_interval(60,'common')
        with self.assertRaises(ValueError):
            ref.news_symbolic_interval(60,'common',profile='generic_Lilly')
        with self.assertRaises(ValueError):
            ref.news_symbolic_interval(60,'mixed',profile=ref.NEWS_PROFILE)
        with self.assertRaises(ValueError):
            ref.news_symbolic_interval(-60,'common',profile=ref.NEWS_PROFILE)

    def test_hypothetical_example_options_not_auto_selected(self):
        options = ref.hypothetical_news_options()
        self.assertEqual(options, {'ordinary_report':'about ten weeks','known_nearby':'ten days'})
        options['ordinary_report'] = 'ten years'
        self.assertEqual(ref.hypothetical_news_options()['ordinary_report'], 'about ten weeks')

    def test_square_comparison_keeps_geometry(self):
        source = ref.square_equivalence_reference()
        self.assertEqual(source['geometric_angle_degrees'], 90)
        self.assertEqual(source['interpretive_comparison'], 'trine')
        self.assertFalse(source['equivalence_is_geometric'])
        self.assertIsNone(source['strength_multiplier'])
        self.assertEqual(ref.aspect_residual(ref.longitude('Cancer',17,0), ref.longitude('Libra',27,0), 90), 600)
        self.assertEqual(ref.aspect_residual(ref.longitude('Cancer',17,0), ref.longitude('Libra',27,0), 120), 1200)

    def test_letter_anchor_not_physical_delivery(self):
        result = ref.question_clock_reference('letter')
        self.assertIn('intention perceived',result['selected_anchor_description'])
        self.assertIn('not mere delivery',result['selected_anchor_description'])
        self.assertFalse(result['actual_timestamp_chosen'])
        self.assertIsNone(result['modern_interface_mapping'])

    def test_event_and_request_clocks_distinct(self):
        self.assertIn('event time',ref.question_clock_reference('sudden_event')['selected_anchor_description'])
        self.assertIn('propounded',ref.question_clock_reference('spoken_request')['selected_anchor_description'])
        self.assertIn('impartiality',ref.question_clock_reference('self_question')['selected_anchor_description'])
        with self.assertRaises(ValueError):
            ref.question_clock_reference('chatgpt_backend_restart')


class GeometryTests(unittest.TestCase):
    def test_all_arcminute_coordinate_roundtrips(self):
        for value in range(ref.CIRCLE):
            self.assertEqual(ref.longitude(*ref.as_sign(value)), value)

    def test_invalid_coordinates_and_missing_minutes(self):
        for args in [('Leo',30,0),('Leo',1,60),('Leo',1,None),('Aries',True,0),('wrong',0,0)]:
            with self.assertRaises(ValueError):
                ref.longitude(*args)
        for value in [-1,21600,True,1.0]:
            with self.assertRaises(ValueError):
                ref.as_sign(value)

    def test_antiscion_involution_and_wrap(self):
        for value in [0,1,5400,10800,16049,21599]:
            self.assertEqual(ref.antiscion(ref.antiscion(value)), value)
        self.assertEqual(ref.separation(21599,1),2)

    def test_mars_antiscion_from_printed_chart(self):
        result = ref.worked_arithmetic()
        self.assertEqual(result['ship_mars_antiscion'], ('Cancer',10,34))
        self.assertEqual(result['ship_mars_antiscion_to_ascendant_arcminutes'], 59)
        self.assertNotEqual(result['ship_mars_antiscion_to_ascendant_arcminutes'],0)

    def test_moon_trines_static_not_ephemeris(self):
        result = ref.worked_arithmetic()
        self.assertEqual(result['ship_moon_mercury_trine_residual_arcminutes'],21)
        self.assertEqual(result['ship_moon_sun_trine_residual_arcminutes'],65)
        self.assertFalse(result['physical_contact_times_computed'])
        self.assertFalse(result['historical_calendar_resolved'])

    def test_jupiter_unsupplied_minute_remains_unknown(self):
        case = data('HISTORICAL_CASES')['cases']['surviving_ship_1644']
        self.assertIsNone(case['degree_only_position']['Jupiter'][2])
        self.assertIsNone(ref.worked_arithmetic()['jupiter_exact_antiscion'])
        with self.assertRaises(ValueError):
            ref.longitude(*case['degree_only_position']['Jupiter'])

    def test_mother_case_fortune_reproduced(self):
        result = ref.worked_arithmetic()
        self.assertEqual(result['mother_case_fortune'], ('Gemini',15,3))
        self.assertTrue(result['printed_fortune_matches'])
        self.assertFalse(result['predictive_validation'])

    def test_fortune_requires_source_profile(self):
        with self.assertRaises(TypeError):
            ref.fortune(1,2,3)
        with self.assertRaises(ValueError):
            ref.fortune(1,2,3,profile='automatic_night_reversal')
        self.assertEqual(ref.fortune(5,2,10,profile=ref.FORTUNE_PROFILE),21597)

    def test_invalid_aspect_rejected(self):
        with self.assertRaises(ValueError):
            ref.aspect_residual(0,60,45)
        with self.assertRaises(ValueError):
            ref.aspect_residual(-1,60,90)


class RecordTests(unittest.TestCase):
    def test_sequential_records_and_scope(self):
        d = data('RULES')
        self.assertEqual(d['records_count'],107)
        self.assertEqual(d['first_record_number'],668)
        self.assertEqual(d['last_record_number'],774)
        self.assertEqual([int(r['id'].rsplit('R',1)[1]) for r in d['records']], list(range(668,775)))
        self.assertEqual(set(r['source_locator']['section_key'] for r in d['records']), {'II.XXIV','II.XXV','II.XXVI'})
        for r in d['records']:
            self.assertFalse(r['independent_evidence_unit'])
            self.assertEqual(r['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertTrue(all(181<=p<=201 for p in r['source_locator']['pdf_pages']))

    def test_all_twelve_ship_correspondences(self):
        self.assertEqual(len(data('SHIP_PARTS')['parts']),12)
        self.assertEqual(ref.ship_part_reference('Sagittarius')['source_description'],'mariners themselves')
        self.assertEqual(ref.ship_part_reference('Aquarius')['source_description'],'master or captain')
        self.assertFalse(ref.ship_part_reference('Pisces')['modern_safety_guidance'])
        with self.assertRaises(ValueError):
            ref.ship_part_reference('unknown')

    def test_role_overlap_not_independent_counts(self):
        overlap = ref.ship_role_dependencies('Moon')
        self.assertTrue(overlap['planetary_roles_share_body'])
        self.assertEqual(overlap['distinct_named_planets'],['Moon'])
        self.assertIsNone(overlap['independent_evidence_count'])
        self.assertFalse(ref.ship_role_dependencies('Saturn')['planetary_roles_share_body'])
        with self.assertRaises(ValueError):
            ref.ship_role_dependencies('Uranus')

    def test_cases_not_inflated_by_teaching_reuse(self):
        cases = data('HISTORICAL_CASES')['cases']
        self.assertEqual(len(cases),3)
        self.assertEqual(len(cases['mother_son_1638']['hypothetical_reuses']),4)
        self.assertTrue(all(c['partial_chart'] for c in cases.values()))
        self.assertTrue(all(not c['independent_validation'] for c in cases.values()))

    def test_all_twenty_eight_issues_preserved(self):
        issues = data('UNRESOLVED')['issues']
        self.assertEqual(len(issues),28)
        self.assertEqual(len({x['id'] for x in issues}),28)
        self.assertTrue(any(x['topic']=='ship_parts_polarity' for x in issues))
        self.assertTrue(any(x['topic']=='mark_gender_asymmetry' for x in issues))

    def test_mars_dignity_and_return_without_loss_not_erased(self):
        rows = data('RULES')['records']
        dignity = [x for x in rows if x['title']=='Departing ship: Saturn and qualified Mars damage'][0]
        self.assertIn('essential dignity',dignity['source_statement'])
        self.assertIn('grave damage',dignity['source_statement'])
        returned = [x for x in rows if x['title']=='Ship: return can be without loss'][0]
        self.assertIn('return without loss',returned['source_statement'])

    def test_fixed_house_and_sign_mark_channels(self):
        d = data('BODY_MARK_REFERENCE')
        self.assertEqual(len(d['input_roles']),5)
        self.assertEqual(d['house_body_explicit']['1'],'face')
        self.assertFalse(d['clinical_use'])

    def test_deterministic_data_regeneration(self):
        names = ['RULES','QUERY_FRAMES','SHIP_PARTS','BODY_MARK_REFERENCE','HISTORICAL_CASES','TIMING_REFERENCES','UNRESOLVED']
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)/'build_source_data.py'
            shutil.copyfile(ROOT/'build_source_data.py',target)
            subprocess.run([sys.executable,str(target)],check=True,capture_output=True,text=True)
            for name in names:
                expected = (ROOT/(name+'.json')).read_bytes()
                actual = (Path(folder)/(name+'.json')).read_bytes()
                self.assertEqual(hashlib.sha256(actual).digest(),hashlib.sha256(expected).digest())


if __name__ == '__main__':
    unittest.main()
