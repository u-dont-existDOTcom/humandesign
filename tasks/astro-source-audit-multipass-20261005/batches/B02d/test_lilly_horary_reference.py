"""Focused reference and counterexample checks for Lilly B02d, not astrology validation."""
import json
from pathlib import Path
import unittest

from lilly_horary_reference import (
    angular_distance, aspect_residual, is_exact_partile, platick_contact,
    source_orb, rays_from, in_nonbeholding_source_table,
    turned_radical_house, declared_horary_house_example,
    solar_separation_claims, printed_strength_row, historical_body_entry
)

ROOT = Path(__file__).resolve().parent
def data(name):
    return json.loads((ROOT/(name+'.json')).read_text())

class OrbTests(unittest.TestCase):
    def test_first_orb_column(self):
        self.assertEqual({p:source_orb(p,'p107_first_column') for p in ('Saturn','Jupiter','Mars','Sun','Venus','Mercury','Moon')},
                         {'Saturn':600,'Jupiter':720,'Mars':450,'Sun':1020,'Venus':480,'Mercury':420,'Moon':750})
    def test_other_authors_column(self):
        self.assertEqual({p:source_orb(p,'p107_other_authors_column') for p in ('Saturn','Jupiter','Mars','Sun','Venus','Mercury','Moon')},
                         {'Saturn':540,'Jupiter':540,'Mars':420,'Sun':900,'Venus':420,'Mercury':420,'Moon':720})
    def test_no_default_and_no_fake_planet(self):
        with self.assertRaises(TypeError): source_orb('Sun')
        with self.assertRaises(ValueError): source_orb('Sun','merged')
        with self.assertRaises(ValueError): source_orb('Uranus','p107_first_column')
    def test_moiety_example_changes_with_profile(self):
        venus = 30*60+10*60
        saturn = 150*60+18*60
        self.assertEqual(aspect_residual(venus,saturn,120),480)
        self.assertTrue(platick_contact(venus,saturn,120,'Venus','Saturn','p107_first_column'))
        self.assertIsNone(platick_contact(venus,saturn,120,'Venus','Saturn','p107_other_authors_column'))
    def test_strict_within_and_outside(self):
        a=0
        self.assertFalse(platick_contact(a,130*60,120,'Saturn','Venus','p107_first_column'))
        self.assertTrue(platick_contact(a,120*60,120,'Saturn','Venus','p107_first_column'))
    def test_exact_partile_is_not_broad_one_degree(self):
        self.assertTrue(is_exact_partile(0,120*60,120))
        self.assertFalse(is_exact_partile(0,120*60+1,120))
        self.assertTrue(is_exact_partile(359*60,179*60,180))
    def test_wrapping_and_bad_coordinates(self):
        self.assertEqual(angular_distance(359*60+59,1),2)
        for a,b in [(-1,0),(21600,0),(0,21600),(0,1.5)]:
            with self.assertRaises(ValueError): angular_distance(a,b)
    def test_reject_synthetic_aspect(self):
        with self.assertRaises(ValueError): aspect_residual(0,30*60,30)


class SignSourceTests(unittest.TestCase):
    def test_rays_aries(self):
        a=rays_from('Aries')
        self.assertEqual(a['dexter'],{60:'Aquarius',90:'Capricorn',120:'Sagittarius'})
        self.assertEqual(a['sinister'],{60:'Gemini',90:'Cancer',120:'Leo'})
        self.assertEqual(a['opposition'],'Libra')
    def test_all_twelve_geometric_table_rows(self):
        signs=data('ASPECT_TABLES')['sign_names']
        self.assertEqual(len(signs),12)
        for idx,sign in enumerate(signs):
            r=rays_from(sign)
            for angle,offset in [(60,2),(90,3),(120,4)]:
                self.assertEqual(r['sinister'][angle],signs[(idx+offset)%12])
                self.assertEqual(r['dexter'][angle],signs[(idx-offset)%12])
            self.assertEqual(r['opposition'],signs[(idx+6)%12])
    def test_literal_nonbeholding_not_completed_by_inference(self):
        self.assertTrue(in_nonbeholding_source_table('Aries','Taurus'))
        self.assertTrue(in_nonbeholding_source_table('Aries','Scorpio'))
        self.assertIsNone(in_nonbeholding_source_table('Aries','Virgo'))
        self.assertIsNone(in_nonbeholding_source_table('Aries','Libra'))
        self.assertEqual(data('ASPECT_TABLES')['raw_directed_entries'],32)
    def test_invalid_sign_rejected(self):
        with self.assertRaises(ValueError): rays_from('Ophiuchus')
        with self.assertRaises(ValueError): in_nonbeholding_source_table('Aries','Ophiuchus')
    def test_turning_complete_twelve_house_rotation(self):
        for origin in range(1,13):
            self.assertEqual([turned_radical_house(origin,i) for i in range(1,13)],
                            [((origin+i-2)%12)+1 for i in range(1,13)])
        with self.assertRaises(ValueError): turned_radical_house(0,1)
    def test_subject_and_asker_not_interchangeable(self):
        partner=declared_horary_house_example('partner')
        self.assertEqual(partner['radical_origin'],7)
        self.assertEqual(partner['relative_houses'],[7,8,9,10,11,12,1,2,3,4,5,6])
        self.assertEqual(declared_horary_house_example('king_as_subject')['radical_origin'],10)
        self.assertEqual(declared_horary_house_example('asker_even_if_king')['radical_origin'],1)
        self.assertEqual(declared_horary_house_example('natal_even_if_king')['radical_origin'],1)
        with self.assertRaises(ValueError): declared_horary_house_example('employee')


class SolarTests(unittest.TestCase):
    def test_literal_zones(self):
        s=solar_separation_claims('Aries','Aries',60)
        self.assertTrue(s['literal_same_sign_combust_8d30'])
        self.assertTrue(s['literal_sun_beams_17d'])
        self.assertFalse(s['literal_cazimi_17arcmin'])
    def test_author_ten_degree_conflict_kept(self):
        s=solar_separation_claims('Aries','Aries',600)
        self.assertFalse(s['literal_same_sign_combust_8d30'])
        self.assertTrue(s['directly_conflicting_10degree_combust_example'])
        self.assertTrue(s['literal_sun_beams_17d'])
    def test_unwritten_intermediate_range_not_treated_as_attested_example(self):
        self.assertFalse(solar_separation_claims('Aries','Aries',540)['directly_conflicting_10degree_combust_example'])
    def test_exact_boundaries_unresolved(self):
        self.assertIsNone(solar_separation_claims('Aries','Aries',17)['literal_cazimi_17arcmin'])
        self.assertIsNone(solar_separation_claims('Aries','Aries',510)['literal_same_sign_combust_8d30'])
        self.assertIsNone(solar_separation_claims('Aries','Taurus',1020)['literal_sun_beams_17d'])
    def test_combust_requires_same_sign_in_literal_definition(self):
        s=solar_separation_claims('Aries','Taurus',100)
        self.assertFalse(s['literal_same_sign_combust_8d30'])
        self.assertTrue(s['literal_sun_beams_17d'])
    def test_no_absolute_angle_as_proxy(self):
        with self.assertRaises(ValueError): solar_separation_claims('Aries','Aries',10801)
        with self.assertRaises(ValueError): solar_separation_claims('Aries','Aries',-1)


class IntegrityTests(unittest.TestCase):
    def test_source_metadata_and_complete_ids(self):
        d=data('RULES')
        self.assertEqual(d['records_count'],176)
        self.assertEqual(d['first_record_number'],392)
        self.assertEqual(d['last_record_number'],567)
        ids=[r['id'] for r in d['records']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(ids[0].endswith('R392') and ids[-1].endswith('R567'))
    def test_source_scoped_and_not_promoted(self):
        d=data('RULES')
        self.assertEqual(set(r['source_locator']['section_key'] for r in d['records']),
                         {'I.XIX','I.XX','I.XXI'})
        for r in d['records']:
            self.assertEqual(r['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertIs(r['independent_evidence_unit'],False)
            self.assertTrue(r['statement_type']=='editor_normalized_paraphrase')
            self.assertTrue(r['source_locator']['pdf_pages'])
            self.assertTrue(all(139<=p<=162 for p in r['source_locator']['pdf_pages']))
    def test_strength_lookup_not_aggregated(self):
        d=data('STRENGTH_ROWS')
        self.assertEqual(len(d['rows']),41)
        self.assertEqual(printed_strength_row('A01')['magnitude'],5)
        self.assertEqual(printed_strength_row('D03')['magnitude'],5)
        self.assertEqual(printed_strength_row('A06')['magnitude'],4)
        self.assertIn('OR',printed_strength_row('E01')['condition'])
        with self.assertRaises(ValueError): printed_strength_row('everything')
    def test_body_table_is_historical_only(self):
        d=data('BODY_TABLE')
        self.assertEqual(len(d['rows']),12)
        self.assertTrue(all(len(v)==7 for v in d['rows'].values()))
        s=historical_body_entry('Cancer','Mars')
        self.assertIn('obscured',s['raw_reading'])
        self.assertTrue(s['not_validated_medical_guidance'])
        with self.assertRaises(ValueError): historical_body_entry('Cancer','Uranus')
    def test_unresolved_not_auto_repaired(self):
        issues=data('UNRESOLVED')['issues']
        self.assertEqual(len(issues),36)
        self.assertEqual(len({r['id'] for r in issues}),36)
        self.assertTrue(any('reception' in r['topic'] for r in issues))
    def test_degree_raw_tokens_preserved(self):
        d=data('DEGREE_TABLE')
        self.assertEqual(len(d['rows']),12)
        self.assertIn('s15',d['rows']['Capricorn']['light_dark_raw'])
        self.assertEqual(d['rows']['Cancer']['lame_deficient'],[9,10,11,12,13,14,15])
    def test_no_deployed_status(self):
        self.assertNotIn('predict',dir(__import__('lilly_horary_reference')))
        self.assertEqual(data('ORB_PROFILES')['author_choice'].startswith('Lilly says'),True)


if __name__=='__main__': unittest.main()
