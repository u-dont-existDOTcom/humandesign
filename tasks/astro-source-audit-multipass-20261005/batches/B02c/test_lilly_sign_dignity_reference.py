import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import unittest
import lilly_sign_dignity_reference as r

P = r.PROFILE
HERE = Path(__file__).resolve().parent

class GeometryTests(unittest.TestCase):
    def test_saturn_example(self):
        x=Fraction(120)+20+Fraction(35,60)
        self.assertEqual(r.antiscion(x),Fraction(30)+9+Fraction(25,60))
        self.assertEqual(r.contrantiscion(x),Fraction(210)+9+Fraction(25,60))
    def test_sun_example(self): self.assertEqual(r.antiscion(40),140)
    def test_involutions_on_all_arcminutes(self):
        for n in range(21600):
            x=Fraction(n,60)
            self.assertEqual(r.antiscion(r.antiscion(x)),x)
            self.assertEqual(r.contrantiscion(r.contrantiscion(x)),x)
    def test_axes(self):
        for x,y in [(0,180),(90,90),(180,0),(270,270)]: self.assertEqual(r.antiscion(x),y)
    def test_subdegree_preservation(self): self.assertEqual(r.antiscion(Fraction(1,3600)),Fraction(180)-Fraction(1,3600))
    def test_decimal_input(self): self.assertEqual(r.antiscion(20.5),Fraction('159.5'))
    def test_bad_longitudes(self):
        for x in [True,'20',-1,360,float('nan'),float('inf'),None]:
            with self.assertRaises(ValueError):r.antiscion(x)
    def test_borrowing(self): self.assertEqual(r.complement_degree_minute(20,35),(9,25))
    def test_minutes_example(self): self.assertEqual(r.complement_degree_minute(14,17),(15,43))
    def test_zero_minute(self): self.assertEqual(r.complement_degree_minute(14,0),(16,0))
    def test_zero_boundary_literal(self): self.assertEqual(r.complement_degree_minute(0,0),(30,0))
    def test_last_minute(self): self.assertEqual(r.complement_degree_minute(29,59),(0,1))
    def test_bad_sexagesimal(self):
        for d,m in [(30,0),(0,60),(-1,0),(1,True),(1.0,0)]:
            with self.assertRaises(ValueError):r.complement_degree_minute(d,m)

class DignityTests(unittest.TestCase):
    def test_12_well_formed_term_rows(self):
        self.assertEqual(len(r.DATA['terms']),12)
        for rows in r.DATA['terms'].values():
            ends=[n for _,n in rows]
            self.assertEqual(len(rows),5);self.assertEqual(ends[-1],30)
            self.assertTrue(all(a<b for a,b in zip([0]+ends[:-1],ends)))
            self.assertEqual(len({p for p,_ in rows}),5)
    def test_all_360_cells_assigned(self):
        for s in r.SIGNS:
            for n in range(1,31):
                self.assertIn(r.ordinal_term(s,n,profile=P),r.PLANETS)
                self.assertIn(r.ordinal_face(s,n,profile=P),r.PLANETS)
    def test_term_aries_boundary(self):
        self.assertEqual([r.ordinal_term('Aries',n,profile=P) for n in (6,7,14,15,21,22,26,27)],['Jupiter','Venus','Venus','Mercury','Mercury','Mars','Mars','Saturn'])
    def test_table_faces_not_earlier_gap(self):
        self.assertEqual(r.ordinal_face('Aquarius',1,profile=P),'Venus')
        self.assertEqual(r.ordinal_face('Pisces',1,profile=P),'Saturn')
    def test_face_boundaries(self):
        self.assertEqual([r.ordinal_face('Aries',n,profile=P) for n in (1,10,11,20,21,30)],['Mars','Mars','Sun','Sun','Venus','Venus'])
    def test_sagittarius_20_later_witness(self): self.assertEqual(r.ordinal_term('Sagittarius',20,profile=P),'Saturn')
    def test_profile_not_optional(self):
        with self.assertRaises(TypeError):r.ordinal_term('Aries',1)
    def test_wrong_profile(self):
        with self.assertRaises(ValueError):r.ordinal_term('Aries',1,profile='Ptolemy')
    def test_no_silent_coordinate_conversion(self):
        for n in [0,31,1.0,Fraction(1),True]:
            with self.assertRaises(ValueError):r.ordinal_term('Aries',n,profile=P)
    def test_unknown_sign(self):
        with self.assertRaises(ValueError):r.ordinal_face('Unknown',1,profile=P)
    def test_night_sun_aries_example(self):
        x=r.essential_components('Sun','Aries',5,'night',profile=P)
        self.assertEqual(x['components']['exaltation'],4);self.assertEqual(x['components']['triplicity'],0)
    def test_day_sun_aries(self):
        self.assertEqual(r.essential_components('Sun','Aries',5,'day',profile=P)['components']['triplicity'],3)
    def test_night_jupiter_aries(self): self.assertEqual(r.essential_components('Jupiter','Aries',5,'night',profile=P)['components']['triplicity'],3)
    def test_exaltation_not_only_exact_degree(self):
        for n in (1,2,3,29,30):
            self.assertEqual(r.essential_components('Moon','Taurus',n,'day',profile=P)['components']['exaltation'],4)
    def test_water_mars_both(self):
        for s in ('Cancer','Scorpio','Pisces'):
            for t in ('day','night'):
                self.assertEqual(r.essential_components('Mars',s,1,t,profile=P)['components']['triplicity'],3)
    def test_unknown_day_not_night(self):
        for t in (None,False,'unknown'):
            with self.assertRaises(ValueError):r.essential_components('Sun','Aries',1,t,profile=P)
    def test_node_exaltation_separate(self):
        self.assertEqual(r.DATA['exaltations']['Gemini'],['Ascending Node',3])
        with self.assertRaises(ValueError):r.essential_components('Ascending Node','Gemini',3,'day',profile=P)
    def test_sum_scope(self):
        x=r.essential_components('Mercury','Virgo',5,'day',profile=P)
        self.assertEqual(x['positive_essential_sum'],11)
        for k in ['is_outcome_probability','includes_accidental_conditions','includes_debility_penalties','includes_personality_judgment']:self.assertIs(x[k],False)

class AdmissionTests(unittest.TestCase):
    def test_domicile_eligible(self): self.assertIs(r.domicile_analogy_eligible(in_own_domicile=True,retrograde=False,combust=False,afflicted=False),True)
    def test_domicile_blocked(self): self.assertIs(r.domicile_analogy_eligible(in_own_domicile=True,retrograde=False,combust=True,afflicted=False),False)
    def test_unknown_impediment(self): self.assertIsNone(r.domicile_analogy_eligible(in_own_domicile=True,retrograde=None,combust=False,afflicted=False))
    def test_false_antecedent_with_unknown(self):self.assertIs(r.domicile_analogy_eligible(in_own_domicile=False,retrograde=None,combust=None,afflicted=None),False)
    def test_no_integer_booleans(self):
        with self.assertRaises(ValueError):r.exaltation_portrait_eligible(exalted=1,unimpeded=True,angular=True)
    def test_exaltation_angular_required(self):self.assertIs(r.exaltation_portrait_eligible(exalted=True,unimpeded=True,angular=False),False)
    def test_exaltation_all_required(self):self.assertIs(r.exaltation_portrait_eligible(exalted=True,unimpeded=True,angular=True),True)
    def test_exaltation_unknown(self):self.assertIsNone(r.exaltation_portrait_eligible(exalted=True,unimpeded=None,angular=True))
    def test_modality_matches(self):
        for a,b,k in [('Aries','Cancer','movable'),('Taurus','Aquarius','fixed'),('Gemini','Pisces','common')]:
            self.assertEqual(r.modality_pair(a,b)['source_branch'],k)
    def test_modality_mixed_not_matched(self):self.assertFalse(r.modality_pair('Aries','Taurus')['evaluated_as_match'])
    def test_modality_missing(self):self.assertEqual(r.modality_pair(None,'Taurus')['reason'],'missing_input')
    def test_feral_no_invented_half(self):
        self.assertIs(r.feral_sign_status('Leo'),True);self.assertIsNone(r.feral_sign_status('Sagittarius'));self.assertIs(r.feral_sign_status('Aries'),False)
    def test_leo_time(self):self.assertEqual(r.source_time_segment((0,18),(3,6))['elapsed_minutes'],168)
    def test_aquarius_time(self):self.assertEqual(r.source_time_segment((16,4),(17,8))['elapsed_minutes'],64)
    def test_segment_not_complete_sign(self):self.assertFalse(r.source_time_segment((16,4),(17,8))['is_exact_full_sign_rising_time'])
    def test_explicit_time_rollover(self):
        with self.assertRaises(ValueError):r.source_time_segment((23,0),(1,0))
        self.assertEqual(r.source_time_segment((23,0),(1,0),next_day=True)['elapsed_minutes'],120)
    def test_bad_time(self):
        with self.assertRaises(ValueError):r.source_time_segment((24,0),(1,0))

class RecordTests(unittest.TestCase):
    def test_record_coverage_and_ids(self):
        x=json.loads((HERE/'RULES.json').read_text())
        self.assertEqual(x['records_count'],161);self.assertEqual(len(x['records']),161)
        self.assertEqual(len({v['id'] for v in x['records']}),161)
        self.assertTrue(x['records'][0]['id'].endswith('R231'));self.assertTrue(x['records'][-1]['id'].endswith('R391'))
    def test_source_scope_every_record(self):
        for v in json.loads((HERE/'RULES.json').read_text())['records']:
            self.assertFalse(v['independent_evidence_unit']);self.assertEqual(v['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertTrue(v['prerequisites']);self.assertTrue(v['qualifications_and_limits'])
    def test_two_xvi_units(self):
        x=json.loads((HERE/'READING_RECEIPT.json').read_text())
        self.assertEqual([s['label'] for s in x['sections']],['XV','XVI','XVI','XVII','XVIII'])
    def test_all_images_and_no_ocr(self):
        x=json.loads((HERE/'READING_RECEIPT.json').read_text())
        self.assertEqual(x['pdf_pages_images_inspected'],list(range(118,140)));self.assertTrue(x['no_new_ocr'])
    def test_swapped_labels_retained(self):
        rows=json.loads((HERE/'READING_RECEIPT.json').read_text())['pages'];d={x['pdf']:x['observed_label'] for x in rows}
        self.assertEqual(d[128],'95');self.assertEqual(d[129],'94');self.assertEqual(d[121],'17')
    def test_full_catalogue_counts(self):
        self.assertEqual(len(r.CATALOGUE['brief_planet_profiles']),7)
        self.assertEqual(len(r.CATALOGUE['sign_profiles']),12)
        self.assertEqual(len(r.CATALOGUE['colours']['planets']),7)
        self.assertEqual(len(r.CATALOGUE['colours']['signs']),12)
    def test_new_uncertainties(self):self.assertEqual(json.loads((HERE/'UNRESOLVED.json').read_text())['count'],24)
    def test_ambiguous_token_not_discriminator(self):
        j=next(x for x in r.CATALOGUE['brief_planet_profiles'] if x['planet']=='Jupiter')
        self.assertTrue(any('not admitted as an executable' in s for s in j['conditions']))
    def test_mars_missing_branch_preserved(self):
        self.assertNotIn('Jupiter',[x['domicile_lord'] for x in r.CATALOGUE['mars_domicile_branches']])
    def test_source_fixture_hashes(self):
        f=HERE/'COMPARISON_INPUTS.json'
        if not f.exists():self.fail('Comparison fixtures required')
        d=json.loads(f.read_text())
        self.assertEqual(d['earlier_planets_sha256'],'f2addd093777b2c32b1152ee5bdab22a95eefee46987bc7dce5d3514bb41d80b')
    def test_compare_retained_earlier_lists(self):
        d=json.loads((HERE/'COMPARISON_INPUTS.json').read_text());old=deepcopy(d['earlier_enumerations'])
        actual=r.compare_earlier_enumerations(old)
        self.assertEqual(old,d['earlier_enumerations'])
        self.assertEqual(actual['comparison']['terms']['differences_count'],26)
        self.assertEqual(actual['comparison']['terms']['earlier_nonunique_cells'],25)
        self.assertEqual(actual['comparison']['faces']['differences_count'],20)
    def test_robbins_difference_count(self):
        x=json.loads((HERE/'TABLE_COMPARISONS.json').read_text())['robbins_vs_lilly']
        self.assertEqual(x['different_numbered_cells'],66)
        self.assertEqual(x['identical_sign_rows'],['Aries','Cancer','Virgo','Sagittarius','Aquarius'])
    def test_rebuild_is_deterministic(self):
        import subprocess,sys
        names=['RULES.json','PORTRAITS_AND_SIGNS.json','DIGNITY_TABLE_P104.json','ANTISCIA_AND_EXAMPLES.json','READING_RECEIPT.json','UNRESOLVED.json','TEXT_IMAGE_CHECKS.json']
        before={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in names}
        subprocess.run([sys.executable,str(HERE/'build_source_data.py')],check=True,capture_output=True)
        self.assertEqual(before,{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in names})

if __name__=='__main__':unittest.main()
