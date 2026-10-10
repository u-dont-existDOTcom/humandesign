"""Inventory, evidence separation and exact arithmetic; not predictive validation."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import lilly_third_house_arithmetic as arithmetic

ROOT=Path(__file__).resolve().parent

def data(name):return json.loads((ROOT/(name+'.json')).read_text())


class SourceIntegrityTests(unittest.TestCase):
    def test_registry_identity_scope_and_nonpromotion(self):
        d=data('RULES');rows=d['rules']
        self.assertEqual(d['records_count'],112)
        self.assertEqual(d['general_records_count'],75)
        self.assertEqual([int(r['id'].rsplit('R',1)[1]) for r in rows],list(range(897,1009)))
        self.assertEqual(len({r['id'] for r in rows}),112)
        for r in rows:
            self.assertEqual(r['source_locator']['source_sha256'],d['source_sha256'])
            self.assertEqual(r['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertFalse(r['independent_evidence_unit'])
            self.assertEqual(r['genre'],'horary')
            self.assertTrue(r['source_locator']['passage_anchor'])

    def test_reading_bounds_and_exact_next_preamble(self):
        receipt=data('READING_RECEIPT');covered=set(receipt['root_original_whole_pages_visually_read_for_extraction'])
        self.assertEqual(covered,set(range(221,236)))
        self.assertEqual(receipt['root_boundary_page_visually_read_not_extracted'],[236])
        self.assertFalse(receipt['new_ocr'])
        for r in data('RULES')['rules']:
            p=r['source_locator']['pdf_pages']
            self.assertTrue(set(p)<=covered)
            self.assertEqual(r['source_locator']['visible_printed_labels'],[str(x-34) for x in p])
        next_unit=data('SECTION_COVERAGE')['next_source_to_extract']
        self.assertEqual((next_unit['pdf_page'],next_unit['printed_page']),(236,202))
        self.assertIn('preamble',next_unit['position'])
        self.assertFalse(next_unit['extracted'])

    def test_context_coverage_and_all_dependency_targets(self):
        rows=data('RULES')['rules'];ids={r['id'] for r in rows}
        a=data('APPLICABILITY_AND_RELATIONS')
        covered=[x for g in a['groups'] for x in g['record_ids']]
        self.assertEqual(set(covered),ids);self.assertEqual(len(covered),len(ids))
        self.assertEqual(len(a['groups']),11)
        for link in a['exception_and_context_links']:
            self.assertIn(link['rule'],ids);self.assertTrue(set(link['must_carry'])<=ids)
        for r in rows:self.assertTrue(set(r.get('dependency_rules',[]))<=ids)
        self.assertIsNone(a['aggregation_algorithm'])
        self.assertIsNone(a['orb_or_cusp_threshold_added'])

    def test_unresolved_references_are_explicit_and_reachable(self):
        d=data('UNRESOLVED');self.assertEqual(d['issues_count'],29)
        rows=data('RULES')['rules'];byid={r['id']:r for r in rows}
        issues={r['id']:r for r in d['issues']}
        self.assertEqual(set(issues),{f'B02h-U{x:02d}' for x in range(1,30)})
        for r in rows:self.assertTrue(set(r['unresolved_ids'])<=set(issues))
        for issue in issues.values():
            self.assertTrue(issue['record_ids'])
            for rid in issue['record_ids']:self.assertIn(issue['id'],byid[rid]['unresolved_ids'])

    def test_case_and_endpoint_dependency_census(self):
        c=data('HISTORICAL_CASES')
        self.assertEqual((c['printed_charts'],c['actual_historical_enquiries'],c['explicit_hypothetical_reuses']),(2,2,1))
        self.assertEqual(c['reported_operational_endpoint_episodes'],2)
        self.assertEqual(len(c['cases']['EX01']['reported_endpoint_episodes']),2)
        self.assertEqual(c['cases']['EX02']['reported_endpoint_episodes'],[])
        self.assertIsNone(c['cases']['EX01']['location_confirmation'])
        self.assertIsNone(c['cases']['EX01']['one_or_two_days_distance_confirmation'])
        self.assertFalse(c['hypothetical']['HY01']['actual_enquiry'])
        self.assertEqual(c['hypothetical']['HY01']['reuses_chart'],'CH02')
        self.assertEqual(c['independent_validation_cases'],0)
        for claim in c['cases']['EX02']['judgements']:self.assertIsNone(claim['separate_confirmed_result'])

    def test_two_eighth_house_references_coexist(self):
        d=data('QUERY_REFERENCES');r=d['absent_relatives']['brother']
        self.assertEqual(r['turned_houses']['8'],10)
        self.assertEqual(r['original_figure_references']['houses']['8'],'death')
        self.assertIsNone(r['frame_precedence'])
        self.assertEqual(d['worked_dual_eighth']['original_eighth_lord'],'Mercury')
        self.assertEqual(d['worked_dual_eighth']['that_lord'],'Mars')
        self.assertEqual(d['current_person_judgements'],0)

    def test_numeric_inventory_keeps_missing_values_and_provenance(self):
        d=data('WORKED_NUMERIC_TABLES')
        rows=[r for c in d['charts'] for k in ['cusps','planets','nodes','lots'] for r in c[k].values()]
        self.assertEqual(len(rows),44)
        self.assertEqual(sum(r['minutes'] is None for r in rows),3)
        self.assertEqual(sum(r['degrees'] is None for r in rows),1)
        for r in rows:self.assertTrue(r['sign_reading_basis'])
        c1,c2=d['charts'];self.assertIsNone(c1['planets']['Jupiter']['sign'])
        self.assertEqual(c1['planets']['Moon']['degrees'],15)
        self.assertEqual(c2['planets']['Sun']['degrees'],1)
        self.assertIsNone(c2['planets']['Venus']['minutes'])

    def test_retained_comparison_companions_resolve(self):
        needed={r for c in data('CROSS_SOURCE_COMPARISONS')['comparisons'] for r in c['retained']}
        retained=data('RETAINED_SOURCE_EXCERPTS')
        self.assertEqual({r['record']['id'] for r in retained['records']},needed)
        self.assertEqual(retained['records_count'],23)
        new={r['id'] for r in data('RULES')['rules']}
        for c in data('CROSS_SOURCE_COMPARISONS')['comparisons']:self.assertTrue(set(c['current'])<=new)
        self.assertTrue(needed.isdisjoint(new))

    def test_source_and_context_regeneration_is_reproducible(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder);b=base/'B02h';b.mkdir();(base/'B02f').mkdir()
            shutil.copyfile(ROOT.parent/'B02f/lilly_presence_ship_reference.py',base/'B02f/lilly_presence_ship_reference.py')
            for p in ['build_source_data.py','integrate_examples.py','build_batch_evidence.py','lilly_third_house_reference.py','WORKED_NUMERIC_TABLES.json','independent_review/examples/CANDIDATE_RULES.json']:
                target=b/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p,target)
            for script in ['integrate_examples.py','build_source_data.py','build_batch_evidence.py']:
                subprocess.run([sys.executable,'-B',str(b/script)],check=True,capture_output=True,text=True)
            for name in ['EXAMPLE_RULES_RECONCILED','RULES','APPLICABILITY_AND_RELATIONS','UNRESOLVED','HISTORICAL_CASES','QUERY_REFERENCES','SECTION_COVERAGE','CROSS_SOURCE_COMPARISONS']:
                self.assertEqual(hashlib.sha256((b/(name+'.json')).read_bytes()).digest(),hashlib.sha256((ROOT/(name+'.json')).read_bytes()).digest(),name)


class ArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result=arithmetic.reconcile()

    def test_saved_arithmetic_is_actual_recalculation(self):
        self.assertEqual(self.result,data('ARITHMETIC_CHECKS'))

    def test_opposite_cusps_and_both_fortune_values(self):
        charts=self.result['charts']
        self.assertTrue(all(x for c in charts.values() for x in c['opposite_cusp_pairs_exact']))
        self.assertEqual(charts['CH01']['Fortune']['computed'],['Capricorn',10,28])
        self.assertEqual(charts['CH02']['Fortune']['computed'],['Scorpio',15,57])
        self.assertTrue(all(c['Fortune']['printed_matches'] for c in charts.values()))

    def test_first_chart_distances_do_not_round_into_prose(self):
        a=self.result['absent_brother']
        self.assertEqual(a['Moon_to_printed_Sun_MC_gap_arcminutes'],599)
        self.assertEqual(a['Venus_Saturn_trine_residual_arcminutes'],20)
        self.assertEqual(a['Venus_to_Capricorn_gap_arcminutes'],67)
        self.assertEqual(a['source_described_degrees_to_ingress'],1)
        self.assertTrue(a['source_qualitative_week_conversion_not_executed'])
        self.assertTrue(a['Sun_MC_shared_printed_entry_not_independent_measurements'])

    def test_jupiter_alternatives_do_not_create_canonical_longitude(self):
        a=self.result['absent_brother']
        self.assertIsNone(a['Jupiter_canonical_longitude'])
        self.assertIsNone(a['Jupiter_canonical_trine_residual'])
        self.assertEqual([(r['degree'],r['sign_if_diagram_sector_is_used'],r['signed_residual_from_trine_arcminutes']) for r in a['Jupiter_conditional_readings']],[(4,'Cancer',634),(14,'Cancer',34),(24,'Gemini',1234)])

    def test_incomplete_positions_fail_closed(self):
        d=data('WORKED_NUMERIC_TABLES');count=0
        for c in d['charts']:
            for kind in ['planets','nodes']:
                for row in c[kind].values():
                    if any(row.get(k) is None for k in ['sign','degrees','minutes']):
                        with self.assertRaises(ValueError):arithmetic.exact_longitude(row)
                        count+=1
        self.assertEqual(count,4)

    def test_cusp_effects_are_separate_from_geometric_sectors(self):
        c=self.result['cambridge'];g=self.result['charts']['CH02']['geometric_houses_from_printed_cusps']
        self.assertEqual([c['Mars_to_MC_gap_arcminutes'],c['Saturn_to_seventh_gap_arcminutes'],c['NorthNode_to_Ascendant_gap_arcminutes']],[260,150,153])
        self.assertEqual([g['Mars'],g['Saturn'],g['NorthNode']],[9,6,12])
        self.assertIsNone(c['cusp_influence_threshold_inferred'])

    def test_second_chart_aspect_residuals_and_conditional_venus_range(self):
        c=self.result['cambridge']
        self.assertEqual(c['Mars_Saturn_square_residual_arcminutes'],17)
        self.assertEqual(c['Moon_Jupiter_sextile_residual_arcminutes'],255)
        self.assertIsNone(c['Moon_Venus_exact_square_gap'])
        self.assertEqual((c['Moon_Venus_conditional_gap_arcminutes']['minimum'],c['Moon_Venus_conditional_gap_arcminutes']['maximum']),(137,196))
        self.assertTrue(c['all_angles_movable'])

    def test_static_checks_do_not_certify_contact_time_or_outcome(self):
        for key in ['physical_contact_times_computed','modern_calendar_resolved','historical_events_independently_verified','predictive_accuracy_tested','source_predictions_replaced_by_arithmetic']:
            self.assertFalse(self.result[key])

if __name__=='__main__':unittest.main()
