"""Golden examples and scope/boundary regressions, not predictive validation."""
import json
from fractions import Fraction as F
from pathlib import Path
import unittest
import lilly_foundation_reference as ref

HERE=Path(__file__).parent
CASES=json.loads((HERE/'CALCULATION_CASES.json').read_text())
RULES=json.loads((HERE/'RULES.json').read_text())

def cusps(case='first_figure'):
    return ref.complete_opposite_cusps({int(h):ref.longitude(*v) for h,v in CASES[case]['cusps'].items()})

class GeometryTests(unittest.TestCase):
    def test_source_longitude_and_sextile(self):
        self.assertEqual(ref.longitude('Gemini',10),70)
        self.assertEqual(ref.aspect_point(70,60),130)
        self.assertEqual(ref.aspect_point(70,60,'leading'),10)
    def test_opposition_roundtrip(self):
        for v in [0,1,179,180,359,F(999,60)]:
            with self.subTest(v=v): self.assertEqual(ref.opposite(ref.opposite(v)),v)
    def test_shortest_wrap(self):
        self.assertEqual(ref.shortest_separation(359,1),2)
    def test_coordinate_bounds(self):
        for args in [('Other',1),('Aries',30),('Aries',0,60),('Aries',0,0,60)]:
            with self.subTest(args=args), self.assertRaises(ValueError): ref.longitude(*args)
    def test_bool_float_rejected(self):
        for v in [True,False,1.0,float('nan')]:
            with self.subTest(v=v),self.assertRaises(TypeError):ref.exact(v)
    def test_ordinary_vs_recognition_angles(self):
        rows=ref.TABLES['aspects']
        self.assertEqual([r['degrees'] for r in rows if r['source_role']=='ordinary'],[0,60,90,120,180])
        self.assertEqual([r['degrees'] for r in rows if r['source_role']!='ordinary'],[30,72,108,144,150])
        with self.assertRaises(ValueError):ref.aspect_point(5,45)
    def test_rounding_branches(self):
        self.assertEqual(ref.solar_degree_for_table('Capricorn',26,39)['longitude'],297)
        self.assertEqual(ref.solar_degree_for_table('Aquarius',7,29)['longitude'],307)
        self.assertIsNone(ref.solar_degree_for_table('Aquarius',7,30)['longitude'])
        self.assertEqual(ref.solar_degree_for_table('Pisces',29,59)['longitude'],0)
    def test_first_cusp_reproduction(self):
        c=cusps()
        self.assertEqual(c[4],ref.longitude('Leo',19))
        self.assertEqual(c[8],ref.longitude('Capricorn',17,10))
        for h in range(1,7):self.assertEqual(c[h+6],ref.opposite(c[h]))
    def test_first_physical_planets(self):
        case=CASES['first_figure'];c=cusps()
        for planet,h in case['physical_house_expectations'].items():
            with self.subTest(planet=planet):self.assertEqual(ref.physical_house(ref.longitude(*case['noon_planets'][planet]),c),h)
    def test_cusp_virtue_not_physical_rewrite(self):
        result=ref.cusp_virtue_reference(ref.longitude('Capricorn',13,55),cusps())
        self.assertEqual(result['physical_house'],7)
        self.assertEqual(result['candidate_virtue_house'],8)
        self.assertEqual(result['nearest_distance_degrees'],F(13,4))
        self.assertIn('PENDING',result['status'])
    def test_exact_five_unresolved(self):
        c=cusps();r=ref.cusp_virtue_reference(c[8]-5,c)
        self.assertEqual(r['physical_house'],7)
        self.assertIsNone(r['candidate_virtue_house'])
        self.assertIn('EXACT_FIVE',r['status'])
    def test_tie_unresolved(self):
        c={i:30*(i-1) for i in range(1,13)}
        self.assertIn('TIE',ref.cusp_virtue_reference(15,c)['status'])
    def test_cusp_boundary_enters_house(self):
        c=cusps()
        for h in c:self.assertEqual(ref.physical_house(c[h],c),h)
    def test_malformed_cusps_rejected(self):
        with self.assertRaises(ValueError):ref.complete_opposite_cusps({1:F(0)})
        c=cusps();c[2]=c[1]
        with self.assertRaises(ValueError):ref.physical_house(1,c)
    def test_second_cusps_allow_repeated_sign(self):
        c=cusps('second_figure')
        self.assertEqual(c[12]//30,c[1]//30)
        self.assertEqual(c[7],ref.longitude('Aries',21,3))

class TimeTests(unittest.TestCase):
    def test_noon_to_next_day(self):
        self.assertEqual(ref.clock_from_noon(840),{'civil_day_offset':1,'hour':2,'minute':F(0)})
        self.assertEqual(ref.clock_from_noon(1260)['hour'],9)
    def test_zero_next_noon_and_negative(self):
        self.assertEqual(ref.clock_from_noon(0)['hour'],12)
        self.assertEqual(ref.clock_from_noon(1440)['civil_day_offset'],1)
        self.assertEqual(ref.clock_from_noon(-780)['civil_day_offset'],-1)
    def test_morning_previous_origin(self):
        self.assertEqual(ref.noon_origin_for_clock(9,45),{'noon_date_offset':-1,'elapsed_minutes':1305})
        self.assertEqual(ref.noon_origin_for_clock(12,0),{'noon_date_offset':0,'elapsed_minutes':0})
    def test_three_time_sums(self):
        for args,expected in [((1196,90),1286),((1242,680),482),((1278,1305),1143)]:
            with self.subTest(args=args):self.assertEqual(ref.add_table_time(*args)['wrapped_minutes'],expected)
    def test_time_bad_bounds(self):
        for args in [(24,0),(1,60),(-1,0)]:
            with self.assertRaises(ValueError):ref.noon_origin_for_clock(*args)
        with self.assertRaises(ValueError):ref.add_table_time(1440,0)
    def test_meridian_signs(self):
        self.assertEqual(ref.meridian_position_elapsed(90,50),140)
        self.assertEqual(ref.meridian_event_time(840,50),790)
        self.assertEqual(ref.clock_from_noon(790),{'civil_day_offset':1,'hour':1,'minute':F(10)})
    def test_event_date_crossing_preserved(self):
        self.assertEqual(ref.meridian_event_time(20,50),-30)
        self.assertEqual(ref.clock_from_noon(-30)['hour'],11)
    def test_short_daily_direction_guard(self):
        self.assertEqual(ref.daily_arcminutes(359,1,'direct'),120)
        self.assertEqual(ref.daily_arcminutes(1,359,'retrograde'),-120)
        with self.assertRaises(ValueError):ref.daily_arcminutes(359,1,'retrograde')
        with self.assertRaises(ValueError):ref.daily_arcminutes(1,1,'unknown')
    def test_source_and_exact_sun(self):
        start=ref.longitude('Capricorn',26,39)
        full=ref.linear_advance(start,61,140)
        source=ref.longitude('Capricorn',26,44,4)
        self.assertEqual((full-source)*3600,F(311,6))
        self.assertEqual(full,ref.longitude('Capricorn',26,44,F(335,6)))
    def test_source_and_exact_moon(self):
        start=ref.longitude('Capricorn',20,54)
        full=ref.linear_advance(start,727,140)
        source=ref.longitude('Capricorn',21,54)
        self.assertEqual(full,ref.longitude('Capricorn',22,4,F(245,6)))
        self.assertEqual((full-source)*3600,F(3845,6))
    def test_negative_advance(self):
        self.assertEqual(ref.linear_advance(ref.longitude('Gemini',27,40),-6,1440),ref.longitude('Gemini',27,34))

class SourceScopeTests(unittest.TestCase):
    def test_record_inventory(self):
        self.assertEqual(RULES['records_count'],len(RULES['records']))
        self.assertEqual(len({r['id'] for r in RULES['records']}),len(RULES['records']))
        self.assertEqual(RULES['independent_predictions_count'],0)
        for r in RULES['records']:
            self.assertTrue(r['source_locator']['pdf_pages'])
            self.assertTrue(r['prerequisites'])
            self.assertEqual(r['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
    def test_coordinate_context(self):
        self.assertEqual(ref.annotation('D','latitude_direction'),'descending latitude')
        self.assertEqual(ref.annotation('D','longitudinal_motion'),'direct')
        with self.assertRaises(ValueError):ref.annotation('D','unknown')
    def test_distinct_house_roles(self):
        h=ref.house_reference(1)
        self.assertEqual(h['natural_cosignificator_planet'],'Saturn')
        self.assertEqual(h['joy'],'Mercury')
        self.assertTrue(h['not_equivalent_to_cusp_ruler'])
    def test_house_return_is_not_shared_mutable_state(self):
        h=ref.house_reference(1);h['joy']='Sun'
        self.assertEqual(ref.house_reference(1)['joy'],'Mercury')
    def test_all_twelve_house_records(self):
        self.assertEqual([r['house'] for r in ref.TABLES['houses']],list(range(1,13)))
        for row in ref.TABLES['houses']:
            self.assertIn(row['source_rule_id'],{r['id'] for r in RULES['records']})
    def test_rank_keeps_equality_requirement(self):
        self.assertIsNone(ref.compare_house_strength(1,10,equally_dignified=None)['stronger_house'])
        self.assertEqual(ref.compare_house_strength(1,10,equally_dignified=True)['stronger_house'],1)
        self.assertEqual(ref.compare_house_strength(9,2,equally_dignified=True)['stronger_house'],9)
        self.assertIsNone(ref.compare_house_strength(4,4,equally_dignified=True)['stronger_house'])
    def test_physician_fixture_image_verified(self):
        self.assertIn('Mars and Venus',ref.house_reference(6)['conditional_clauses'])
    def test_noon_examples_not_current_natal_chart(self):
        self.assertTrue(CASES['first_figure']['not_actual_event_time_chart'])
        self.assertIn('not Swiss',CASES['source_vs_exact_linear']['scope'])
    def test_source_calculation_not_validation(self):
        self.assertIn('NOT_PREDICTIVELY_VALIDATED',ref.STATUS)
    def test_native_scopes_not_silent_current_diagnoses(self):
        for r in RULES['records']:
            self.assertFalse(r['independent_evidence_unit'])
        self.assertEqual({r['source_locator']['chapter'] for r in RULES['records'] if r['source_locator']['book']=='I'},set(range(1,8)))

# One independent golden test per source table row / daily example, not one new prediction.
for row in ref.TABLES['hourly_motion_table']:
    def test_row(self,row=row):
        actual=ref.hourly_arcseconds(row['daily_arcminutes'])
        displayed=60*row['hourly_arcminutes']+row['arcseconds']+F(row['thirds'],60)
        self.assertEqual(actual,displayed)
    setattr(TimeTests,f'test_hourly_table_row_{row["daily_arcminutes"]:02}',test_row)
for row in CASES['daily_motion']:
    def test_daily(self,row=row):
        self.assertEqual(ref.daily_arcminutes(ref.longitude(*row['earlier']),ref.longitude(*row['later']),row['direction']),row['expected_signed_arcminutes'])
    setattr(TimeTests,f'test_daily_example_{row["body"].lower()}',test_daily)
if __name__=='__main__':unittest.main(verbosity=2)
