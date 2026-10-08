from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
import unittest
import lilly_planet_reference as r

HERE = Path(__file__).resolve().parent

class Tables(unittest.TestCase):
    def test_seven_planets(self):
        self.assertEqual(len(r._data()), 7)
    def test_ordinary_term(self):
        self.assertEqual(r.numbered_degree_candidates('term','Aries',1)['owners'],['Jupiter'])
    def test_gemini_gap_not_repaired(self):
        self.assertEqual(r.numbered_degree_candidates('term','Gemini',21)['status'],'GAP')
    def test_leo_conflict(self):
        self.assertEqual(r.numbered_degree_candidates('term','Leo',1)['owners'],['Saturn','Mercury'])
    def test_virgo_conflict(self):
        self.assertEqual(r.numbered_degree_candidates('term','Virgo',8)['owners'],['Venus','Mercury'])
    def test_leo_and_virgo_gaps(self):
        for sign,d in [('Leo',8),('Virgo',1)]:
            with self.subTest(sign=sign):
                self.assertEqual(r.numbered_degree_candidates('term',sign,d)['owners'],[])
    def test_venus_pisces_face_retained(self):
        self.assertEqual(r.numbered_degree_candidates('face','Pisces',1)['owners'],['Saturn','Venus'])
    def test_aquarius_face_gap(self):
        self.assertEqual(r.numbered_degree_candidates('face','Aquarius',1)['status'],'GAP')
    def test_sun_and_moon_have_no_terms(self):
        for planet in ['Sun','Moon']:
            self.assertEqual(r.planet_record(planet)['raw_terms'],[])
    def test_ordinals_are_not_angles(self):
        for d in [0,31,1.5,True,'1']:
            with self.subTest(d=d), self.assertRaises(ValueError):
                r.numbered_degree_candidates('face','Aries',d)
    def test_invalid_source_identifiers(self):
        with self.assertRaises(ValueError): r.planet_record('Uranus')
        with self.assertRaises(ValueError): r.numbered_degree_candidates('term','ARI',1)
        with self.assertRaises(ValueError): r.numbered_degree_candidates('bound','Aries',1)
    def test_saved_audit_recomputed(self):
        saved=json.loads((HERE/'TABLE_AUDIT.json').read_text())
        for kind,key in [('term','term_anomalies'),('face','face_anomalies')]:
            got=[]
            for sign in r.SIGNS:
                for d in range(1,31):
                    found=r.numbered_degree_candidates(kind,sign,d)
                    if found['status']!='SINGLE':
                        got.append({k:found[k] for k in ['sign','ordinal_degree','owners','status']})
            self.assertEqual(got,saved[key])
    def test_counts_are_source_cells_not_predictions(self):
        s=json.loads((HERE/'TABLE_AUDIT.json').read_text())
        self.assertEqual((s['raw_term_rows'],s['raw_face_rows']),(60,36))
        self.assertEqual((s['term_total_assignments'],s['face_total_assignments']),(359,360))
        self.assertEqual(len(s['term_anomalies']),25)
        self.assertEqual(len(s['face_anomalies']),20)

class Selection(unittest.TestCase):
    def test_explicit_relevance_required(self):
        self.assertEqual(r.conditional_portrait('Jupiter',relevant=None,condition='WELL')['status'],'UNRESOLVED')
    def test_irrelevant_not_applied(self):
        self.assertEqual(r.conditional_portrait('Jupiter',relevant=False,condition='WELL')['branches'],{})
    def test_unknown_not_ill(self):
        self.assertEqual(r.conditional_portrait('Saturn',relevant=True,condition='UNKNOWN')['branches'],{})
    def test_mixed_unresolved_not_averaged(self):
        x=r.conditional_portrait('Mars',relevant=True,condition='MIXED')
        self.assertEqual(set(x['branches']),{'well','ill'})
        self.assertFalse(x['selected_as_prediction'])
    def test_well_mars_not_whitewashed(self):
        x=r.conditional_portrait('Mars',relevant=True,condition='WELL')['branches']['well'].lower()
        self.assertIn('contentious',x)
        self.assertIn('prudent',x)
    def test_well_moon_not_whitewashed(self):
        x=r.conditional_portrait('Moon',relevant=True,condition='WELL')['branches']['well'].lower()
        self.assertIn('timorous',x)
        self.assertIn('peace',x)
    def test_bad_condition_rejected(self):
        with self.assertRaises(ValueError):r.conditional_portrait('Venus',relevant=True,condition='GOOD_PERSON')
        with self.assertRaises(TypeError):r.conditional_portrait('Venus',relevant='yes',condition='WELL')
    def test_own_minor_dignity_true(self):
        self.assertIs(r.minor_dignity_excludes_peregrine(own_term=True,own_face=None),True)
        self.assertIs(r.minor_dignity_excludes_peregrine(own_term=None,own_face=True),True)
    def test_own_minor_dignity_unknown(self):
        self.assertIsNone(r.minor_dignity_excludes_peregrine(own_term=None,own_face=False))
    def test_no_minor_not_full_peregrine_verdict(self):
        self.assertIs(r.minor_dignity_excludes_peregrine(own_term=False,own_face=False),False)
        with self.assertRaises(TypeError):r.minor_dignity_excludes_peregrine(own_term=1,own_face=False)
    def test_mercury_any_aspect_not_gender_conjunction(self):
        x=r.mercury_assimilation('Mars',has_aspect=True)
        self.assertEqual(x['modifier'],'more rash')
        self.assertFalse(x['gender_conjunction_clause_applied'])
    def test_mercury_no_or_unknown_aspect(self):
        self.assertIsNone(r.mercury_assimilation('Sun',has_aspect=None)['modifier'])
        self.assertEqual(r.mercury_assimilation('Sun',has_aspect=False)['status'],'NOT_APPLICABLE')
    def test_mercury_all_six_modifiers(self):
        got=[r.mercury_assimilation(p,has_aspect=True)['modifier'] for p in r.PLANETS if p!='Mercury']
        self.assertEqual(len(set(got)),6)
        with self.assertRaises(ValueError):r.mercury_assimilation('Mercury',has_aspect=True)

class MotionAndCycles(unittest.TestCase):
    def test_slow_strictly_below(self):
        self.assertTrue(r.lunar_slow_analogy(Fraction(13))['equivalent_to_retrograde'])
    def test_exact_threshold_not_below(self):
        self.assertFalse(r.lunar_slow_analogy(r.LUNAR_SLOW_LIMIT)['equivalent_to_retrograde'])
    def test_between_threshold_and_mean(self):
        self.assertLess(r.LUNAR_SLOW_LIMIT,r.LUNAR_MEAN)
        self.assertFalse(r.lunar_slow_analogy((r.LUNAR_SLOW_LIMIT+r.LUNAR_MEAN)/2)['equivalent_to_retrograde'])
    def test_mean_seconds_not_lost(self):
        self.assertEqual(r.LUNAR_MEAN-r.LUNAR_SLOW_LIMIT,Fraction(1,100))
    def test_motion_not_overwritten(self):
        self.assertFalse(r.lunar_slow_analogy(12)['physical_direction_overwritten'])
    def test_unknown_motion(self):
        self.assertIsNone(r.lunar_slow_analogy(None)['equivalent_to_retrograde'])
    def test_invalid_motion(self):
        for v in [-1,float('nan'),float('inf')]:
            with self.subTest(v=v),self.assertRaises(ValueError):r.lunar_slow_analogy(v)
        with self.assertRaises(TypeError):r.lunar_slow_analogy(True)
    def test_orb_no_pair_policy(self):
        for planet,orb in zip(r.PLANETS,[9,9,7,15,7,7,12]):
            with self.subTest(planet=planet):
                x=r.orb_reference(planet)
                self.assertEqual((x['before_degrees'],x['after_degrees']),(orb,orb))
                self.assertEqual(x['pair_aggregation'],'NOT_DETERMINED_HERE')
    def test_four_year_categories_not_one_cycle(self):
        self.assertEqual(r.source_year_numbers('Saturn'),{'greatest':'465','greater':'57','mean':'43 1/2','least':'30'})
    def test_source_mars_age_not_imported(self):
        self.assertIn('41 to 56',r.planet_record('Mars')['age'])
    def test_known_inconsistent_latitude_retained(self):
        x=json.dumps(r.planet_record('Venus')['astronomy'])
        self.assertIn('36',x)
        self.assertIn('2',x)

class NodesAndProvenance(unittest.TestCase):
    def test_head_doctrines_opposed(self):
        self.assertEqual(r.node_reference('Head','malefic',doctrine='reported_ancients')['result'],'evil')
        self.assertEqual(r.node_reference('Head','malefic',doctrine='Lilly_preferred')['result'],'lessen_evil')
    def test_tail_doctrines_opposed(self):
        self.assertEqual(r.node_reference('Tail','malefic',doctrine='reported_ancients')['result'],'good')
        self.assertEqual(r.node_reference('Tail','malefic',doctrine='Lilly_preferred')['result'],'intensify_evil')
    def test_tail_good_not_certain_failure(self):
        x=r.node_reference('Tail','benefic',doctrine='Lilly_preferred')
        self.assertEqual(x['result'],'obstacles_with_conditional_failure')
        self.assertIn('AND',x['tail_benefic_scope'])
    def test_no_numeric_multiplier(self):
        self.assertIsNone(r.node_reference('Tail','malefic',doctrine='Lilly_preferred')['numeric_multiplier'])
    def test_doctrine_explicit(self):
        with self.assertRaises(ValueError):r.node_reference('Head','malefic',doctrine='traditional')
        with self.assertRaises(ValueError):r.node_reference('Node','malefic',doctrine='Lilly_preferred')
    def test_friendship_not_symmetrized(self):
        self.assertIn('Sun',r.planet_record('Saturn')['friends'])
        self.assertIn('Saturn',r.planet_record('Sun')['enemies'])
        self.assertIsNone(r.planet_record('Venus')['friends'])
    def test_records_unique_anchored_not_promoted(self):
        data=json.loads((HERE/'RULES.json').read_text())
        records=data['records']
        self.assertEqual(data['records_count'],len(records))
        self.assertEqual(len(set(x['id'] for x in records)),len(records))
        self.assertEqual(data['independent_predictions_count'],0)
        for x in records:
            self.assertTrue(x['source_locator']['pdf_pages'])
            self.assertEqual(x['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertFalse(x['independent_evidence_unit'])
    def test_later_table_not_full_chapter_read(self):
        data=json.loads((HERE/'TABLE_AUDIT.json').read_text())
        self.assertFalse(data['synoptic_chapter_fully_read'])
    def test_numeric_symbols_not_birth_name_model(self):
        self.assertEqual(r.planet_record('Sun')['numbers'],[1,4])
        self.assertEqual(r.planet_record('Jupiter')['numbers'],[3])
        self.assertEqual(r.planet_record('Saturn')['numbers'],[])

if __name__=='__main__':unittest.main()
