"""Check independent source constants, explicit branches, and anti-silent-import cases."""
import importlib.util
import json
from datetime import date
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ref',ROOT/'scripts/numerology_book_reference.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
DATA=json.loads((ROOT/'reference/research/numerology_v2_20261004/formula_fixtures.json').read_text())

def field(value,path):
    if path=='$': return value
    for part in path.split('.'):
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value

class SourceArithmetic(unittest.TestCase):
    def test_source_fixtures(self):
        for f in DATA['fixtures']:
            with self.subTest(fixture=f['id']):
                args=dict(f['arguments'])
                if 'born' in args: args['born']=date.fromisoformat(args['born'])
                actual=getattr(r,f['operation'])(**args)
                for path,expected in f['expected_paths'].items(): self.assertEqual(field(actual,path),expected,path)
    def test_complete_cayce_table(self):
        for row in DATA['cayce_table']['rows']:
            with self.subTest(year=row['year']):
                self.assertEqual(r.jb_year(date(1877,3,18),row['year'])['admitted'],row['personal_year'])
                p=r.jb_periods(date(1877,3,18),row['year'],44,12)
                self.assertEqual([v['admitted'] for v in p],[row['period1'],row['period2'],row['period3']])
    def test_expected_coverage(self):
        self.assertEqual({f['system_id'] for f in DATA['fixtures']},r.SYSTEMS)
        self.assertEqual([x['year'] for x in DATA['cayce_table']['rows']],list(range(1877,1945)))
    def test_master_disagreements_are_not_averaged(self):
        self.assertEqual([r.result(22,s)['value'] for s in [r.CHEIRO,r.JORDAN,r.CAMPBELL,r.JB]],[4,4,22,22])
        self.assertEqual([r.result(44,s)['value'] for s in [r.CHEIRO,r.JORDAN,r.CAMPBELL,r.JB]],[8,8,8,44])
    def test_life_lesson_full_units_not_partwise(self):
        d=date(1940,11,12)
        self.assertEqual(r.date_number(d,r.JB)['raw'],37)
        self.assertEqual(r.date_number(d,r.JORDAN)['result']['raw'],10)
    def test_no_silent_phonetic_mask(self):
        for s in (r.CAMPBELL,r.JB):
            with self.assertRaises(ValueError):r.name_number(['Mary'],s,selection='vowels')
        with self.assertRaises(ValueError):r.name_number(['Mary'],r.JORDAN,masks=['CVCV'],selection='vowels')
    def test_jordan_no_vowel_is_not_fabricated(self):
        n=r.name_number(['Lynn'],r.JORDAN,selection='vowels')
        self.assertFalse(n['interpretation_available']);self.assertEqual(n['result']['value'],0)
    def test_distinct_planes_not_same_numeric_groups(self):
        self.assertEqual(r.planes(['C'],r.CAMPBELL)['planes']['intuitive'],1)
        self.assertEqual(r.planes(['C'],r.JORDAN)['counts']['emotional'],1)
    def test_declared_campbell_master_duration_branches(self):
        with self.assertRaises(ValueError):r.pinnacle_marks(11,r.CAMPBELL)
        self.assertEqual(r.pinnacle_marks(11,r.CAMPBELL,'literal'),[25,34,43])
        self.assertEqual(r.pinnacle_marks(11,r.CAMPBELL,'root'),[34,43,52])
    def test_eight_challenge_scope(self):
        self.assertEqual(r.challenges(1,9,2,r.CAMPBELL),[8,7,1])
        for m in range(1,10):
            for d in range(1,10):
                for y in range(1,10):
                    a,b,c=r.challenges(m,d,y,r.CAMPBELL)
                    if c==8:self.assertEqual({a,b},{0,8})
    def test_rc_not_eight_year_toggle(self):
        self.assertEqual([r.jordan_race_consciousness(a) for a in range(27,32)],[1,3,5,7,9])
        for a in range(90):self.assertEqual(r.jordan_race_consciousness(a),r.jordan_race_consciousness(a+9))
    def test_campbell_1910_2009_claim_is_correct(self):
        self.assertEqual([y for y in range(1910,2010) if r.reduction(y,(11,22))[-1]==11],[1910,2009])
    def test_tapes_not_a_jb_triangle(self):
        with self.assertRaises(ValueError):r.tape(['Ada','Wynn','Lunt'],35,r.JB)
        t=r.jb_triangle(['Ada','Wynn'],date(1940,11,12))
        self.assertTrue(all(x['interval'][1]-x['interval'][0]==9 for x in t['lines']))
        self.assertEqual(t['lines'][3]['ordinal'],23)
    def test_duplicate_major_ages_not_six_events(self):
        line=r.jb_triangle(['Ada','Wynn'],date(1940,11,12))['lines'][0]
        self.assertEqual(len(line['major']),6)
        self.assertEqual(len({x['age'] for x in line['major']}),4)
    def test_triangle_minor_sort_not_operation_order(self):
        line=r.jb_triangle(['Ada','Wynn'],date(1940,11,12))['lines'][3]
        self.assertEqual([x['age'] for x in line['minor']],[31,32])
        self.assertEqual([x['number']['raw'] for x in line['minor']],[97,35])
    def test_all_letters_in_both_plane_tables(self):
        letters=list(r.ALPHABET)
        c=r.planes(letters,r.CAMPBELL)
        self.assertEqual(sum(c['planes'].values()),26)
        self.assertEqual(sum(c['classes'].values()),26)
        self.assertEqual(sum(r.planes(letters,r.JORDAN)['counts'].values()),26)
    def test_input_uncertainty_not_normalized_away(self):
        for p in [['Jean-Luc'],['Hâle'],['Mr Smith'],['Groß'],['ı'],['']]:
            with self.assertRaises(ValueError):r.tokens(p)
    def test_jordan_interval_three_not_harmonic(self):
        x=r.jordan_balance_intervals({'heart':3,'destiny':6,'birth_force':7,'reality':4})
        self.assertEqual(x[0]['difference'],3);self.assertEqual(x[0]['category'],'strain')
    def test_jb_compound_root_is_not_enough(self):
        self.assertEqual(r.jb_power(41,37)['admitted'],78)
        self.assertNotEqual(r.jb_power(5,1)['admitted'],78)
    def test_no_unsupported_imports(self):
        for s in (r.JB,r.CHEIRO):
            with self.assertRaises(ValueError):r.pinnacles(3,5,1990,s)
            with self.assertRaises(ValueError):r.challenges(3,5,1990,s)
    def test_phase_ranges_not_implicit_prediction(self):
        c=r.campbell_cycle_candidates(date(1732,2,22),28)
        self.assertIsNone(c['exact_lunar_return']);self.assertIsNone(c['exact_in_year_boundary'])
    def test_ambiguous_campbell_branches_require_selection(self):
        with self.assertRaises(ValueError):r.name_number(["Kirk"],r.CAMPBELL)
        with self.assertRaises(ValueError):r.date_number(date(1732,2,22),r.CAMPBELL)
    def test_invalid_numeric_inputs_rejected(self):
        for x in [True,-1,None,1.2,'11']:
            with self.assertRaises(ValueError):r.digit_sum(x)

if __name__=='__main__':unittest.main(verbosity=2)
