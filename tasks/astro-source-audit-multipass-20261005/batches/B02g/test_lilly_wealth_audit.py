"""Source integrity and printed arithmetic, not tests of predictive accuracy."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import lilly_wealth_case_arithmetic as arithmetic
import lilly_wealth_reference as reference

ROOT = Path(__file__).resolve().parent

def data(name):
    return json.loads((ROOT / (name + '.json')).read_text())

class SourceIntegrityTests(unittest.TestCase):
    def test_record_identity_scope_and_nonpromotion(self):
        d=data('RULES')
        self.assertEqual(d['records_count'],122)
        self.assertEqual([int(r['id'].rsplit('R',1)[1]) for r in d['rules']],list(range(775,897)))
        self.assertEqual(len({r['id'] for r in d['rules']}),122)
        for row in d['rules']:
            self.assertFalse(row['independent_evidence_unit'])
            self.assertEqual(row['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertEqual(row['genre'],'horary')
            self.assertEqual(row['source_locator']['source_sha256'],d['source_sha256'])

    def test_page_anchors_preserve_visible_folio_anomaly(self):
        labels={r['pdf_page']:r['visible_folio'] for r in data('READING_RECEIPT')['page_labels']}
        self.assertEqual({p:labels[p] for p in [204,205,208,209]},{204:'174',205:'175',208:'170',209:'171'})
        for r in data('RULES')['rules']:
            loc=r['source_locator']
            self.assertTrue(loc['passage_anchor'])
            self.assertTrue(all(201<=p<=221 for p in loc['pdf_pages']))
            self.assertEqual(loc['visible_printed_labels'],[labels[p] for p in loc['pdf_pages']])

    def test_complete_context_and_valid_exception_links(self):
        ids={r['id'] for r in data('RULES')['rules']}
        d=data('APPLICABILITY_AND_RELATIONS')
        covered=[rid for g in d['groups'] for rid in g['record_ids']]
        self.assertEqual(set(covered),ids)
        self.assertEqual(len(covered),len(ids))
        for edge in d['exception_links']:
            self.assertIn(edge['rule'],ids)
            self.assertTrue(set(edge['must_carry'])<=ids)
        for issue in data('UNRESOLVED')['issues']:
            self.assertTrue(set(issue['record_ids'])<=ids)
        self.assertEqual(data('UNRESOLVED')['issues_count'],32)

    def test_one_case_preserves_unconfirmed_endpoints(self):
        cases=data('HISTORICAL_CASES')['cases']
        self.assertEqual(len(cases),1)
        c=cases['tradesman_1634']
        self.assertEqual(c['independent_validation_cases'],0)
        rows={r['endpoint']:r for r in c['outcome_records']}
        self.assertIn('money and land',rows['wife_money_and_land']['reported_result'])
        self.assertIsNone(rows['about_1640_trade_reputation_friends']['reported_result'])
        self.assertIsNone(rows['lasting_competence']['reported_result'])
        self.assertFalse(c['full_lifetime_observation'])
        self.assertFalse(c['original_prediction_freeze_available'])

    def test_frames_match_reference_and_turned_money(self):
        for name,d in data('QUERY_FRAMES').items():
            if not isinstance(d,dict):continue
            actual=reference.query_frame(name)
            for key in ['querent_house','querent_money_house','counterparty_house','counterparty_money_house']:
                self.assertEqual(actual[key],d[key])
            if actual['counterparty_house']:
                self.assertEqual(arithmetic.GEO.turned_house(actual['counterparty_house'],2),actual['counterparty_money_house'])

    def test_house_timing_profile_retains_undefined_override(self):
        d=data('TIMING_REFERENCES')
        for pair,unit in d['house_pair_units'].items():
            a,b=pair.split('|')
            out=reference.wealth_symbolic_interval(387,a,b,profile=d['house_pair_profile'])
            self.assertEqual(out['interval'],'129/20')
            self.assertEqual(out['unit'],unit)
            self.assertFalse(out['civil_dates_computed'])
        self.assertIsNone(d['long_business_threshold'])
        self.assertIsNone(d['ascendant_cusp_complete_modality_table'])

    def test_reader_disagreement_and_next_boundary_retained(self):
        self.assertEqual(data('WORKED_NUMERIC_TABLES')['chart']['time_minute_options'],[0,6])
        self.assertEqual(data('READING_RECEIPT')['root_actually_viewed_pdf_pages'],list(range(201,222)))
        n=data('SECTION_COVERAGE')['next_source_to_extract']
        self.assertEqual(n['pdf_page'],221)
        self.assertIn('preamble',n['position'])

    def test_receiving_direction_and_point_semantics(self):
        rows={int(r['id'].rsplit('R',1)[1]):r for r in data('RULES')['rules']}
        self.assertIn('receiving',rows[821]['title'])
        self.assertIn('receiving',rows[830]['title'])
        self.assertIn('at the hour of the question',rows[836]['source_statement'])
        self.assertIn('exceptions',rows[837]['source_statement'])
        self.assertIn('unimpeded benefic planet',rows[888]['source_statement'])
        self.assertFalse(data('APPLICABILITY_AND_RELATIONS')['point_semantics']['Fortune_and_nodes_emit_rays'])

    def test_deterministic_data_regeneration(self):
        with tempfile.TemporaryDirectory() as folder:
            tmp=Path(folder)
            for name in ['build_source_data.py','build_batch_evidence.py','XXVIII_EXTRACTED.json']:
                shutil.copyfile(ROOT/name,tmp/name)
            for script in ['build_source_data.py','build_batch_evidence.py']:
                subprocess.run([sys.executable,str(tmp/script)],check=True,capture_output=True,text=True)
            for name in ['RULES','QUERY_FRAMES','TIMING_REFERENCES','HISTORICAL_CASES','UNRESOLVED','APPLICABILITY_AND_RELATIONS','CROSS_SOURCE_COMPARISONS','SECTION_COVERAGE','READING_RECEIPT']:
                self.assertEqual(hashlib.sha256((tmp/(name+'.json')).read_bytes()).digest(),hashlib.sha256((ROOT/(name+'.json')).read_bytes()).digest(),name)

class PrintedArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=arithmetic.reconcile()

    def test_all_antiscion_and_contra_pairs_reproduce(self):
        self.assertEqual(len(self.result['antiscia']),7)
        self.assertTrue(all(r['printed_antiscion_matches'] and r['printed_contra_antiscion_matches'] for r in self.result['antiscia']))
        self.assertEqual(self.result['exact_antiscion_hits_on_transcribed_points_or_cusps'],[])

    def test_strength_components_and_fortune_net(self):
        expected={'Saturn':-8,'Jupiter':20,'Mars':9,'Sun':8,'Venus':18,'Mercury':13,'Moon':5}
        self.assertEqual({r['body']:r['computed_net'] for r in self.result['strengths']},expected)
        self.assertTrue(all(r['printed_components_and_net_match'] for r in self.result['strengths']))
        self.assertEqual(self.result['fortune']['computed_strength_net'],-2)

    def test_fortune_and_timing_distances(self):
        self.assertEqual(self.result['fortune']['computed'],['Scorpio',0,10])
        self.assertTrue(self.result['fortune']['printed_matches'])
        self.assertEqual(self.result['distances_arcminutes']['Mars_to_Ascendant'],119)
        self.assertEqual(self.result['distances_arcminutes']['Moon_to_Venus'],387)
        self.assertFalse(self.result['physical_contact_times_computed'])
        self.assertFalse(self.result['historical_calendar_resolved'])

    def test_cusp_exception_has_no_replacement_cutoff(self):
        f=self.result['source_cusp_assignment']['Fortune']
        self.assertEqual(f['gap_to_second_cusp_arcminutes'],385)
        self.assertEqual((f['geometric_house_between_printed_cusps'],f['source_attributed_house']),(1,2))
        self.assertIsNone(f['general_replacement_threshold'])
        self.assertEqual(self.result['distances_arcminutes']['Venus_to_eleventh_cusp'],61)

    def test_near_contact_and_square_geometry(self):
        self.assertEqual(self.result['distances_arcminutes']['Saturn_contra_antiscion_to_Jupiter'],170)
        self.assertEqual(self.result['aspect_residuals_arcminutes']['Jupiter_square_Ascendant'],198)
        self.assertEqual(self.result['aspect_residuals_arcminutes']['Jupiter_square_Mars'],79)
        self.assertIn('without minutes',self.result['fixed_star_limits']['Spica'])

    def test_four_swift_entries_and_five_claim(self):
        s=self.result['swift_count']
        self.assertEqual(s['swift_bodies'],['Jupiter','Mars','Venus','Mercury'])
        self.assertEqual(s['slow_bodies'],['Saturn','Sun','Moon'])
        self.assertEqual(s['later_source_claim'],5)
        self.assertFalse(s['consistent'])
        m=self.result['mean_motion_comparisons']
        self.assertEqual((m['Mars']['daily_arcseconds'],m['Mars']['source_mean_arcseconds']),(2100,1887))
        self.assertEqual(m['Jupiter']['source_mean_arcseconds'],299)

    def test_arithmetic_output_and_exact_motion_units(self):
        self.assertEqual(data('ARITHMETIC_CHECKS'),self.result)
        self.assertEqual(arithmetic._motion_arcseconds('1d13m'),4380)
        self.assertEqual(arithmetic._motion_arcseconds('0d04m59s'),299)
        for bad in ['1d','1d60m','0d10m60s','1.2d10m']:
            with self.assertRaises(ValueError):arithmetic._motion_arcseconds(bad)

if __name__=='__main__':
    unittest.main()
