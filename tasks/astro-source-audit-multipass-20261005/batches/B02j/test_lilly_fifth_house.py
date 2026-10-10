"""Focused tests of transcription integrity and bounded arithmetic, not astrology."""
import copy
import json
from pathlib import Path
import unittest
from fractions import Fraction

import lilly_fifth_house_reference as r

HERE = Path(__file__).resolve().parent
TABLES = json.loads((HERE / 'WORKED_NUMERIC_TABLES.json').read_text())


class BoundedArithmeticTests(unittest.TestCase):
    def test_zodiac_wrap_and_negative_projection(self):
        self.assertEqual(r.zodiac(-1), {'sign':'Pisces','degree':29,'minute':59})
        self.assertEqual(r.zodiac(21600), {'sign':'Aries','degree':0,'minute':0})

    def test_missing_minute_cannot_be_zero_filled(self):
        with self.assertRaises(r.SourceInputError):
            r.longitude('Aries',11,None)

    def test_invalid_sign_or_precision_rejected(self):
        for args in [('Unknown',2,0), ('Aries',30,0), ('Aries',2,60), ('Aries',2.0,0), ('Aries',True,0)]:
            with self.subTest(args=args), self.assertRaises(r.SourceInputError):
                r.longitude(*args)

    def test_children_formula_is_same_day_and_night(self):
        # A synthetic wrap case catches reversal, wrong projection and sect switching.
        asc, mars, jup = r.longitude('Pisces',29,50), r.longitude('Aries',1,0), r.longitude('Taurus',2,20)
        expected = r.longitude('Taurus',1,10)
        for sect in ('day','night'):
            self.assertEqual(r.part_of_children(asc,mars,jup,sect), expected)

    def test_children_formula_requires_declared_sect(self):
        with self.assertRaises(r.SourceInputError):
            r.part_of_children(0,0,0,'unrecorded')

    def test_first_chart_fortune_matches_conditional_reading(self):
        receipt = r.comparison_receipt(TABLES)
        self.assertTrue(receipt['first_fortune']['matches'])
        self.assertEqual(receipt['first_fortune']['result'], {'sign':'Sagittarius','degree':3,'minute':8})
        self.assertTrue(receipt['first_fortune']['conditional_on_declared_inferred_signs'])

    def test_first_chart_children_part_matches_conditional_reading(self):
        receipt = r.comparison_receipt(TABLES)
        self.assertEqual(receipt['first_part_of_children']['result'], {'sign':'Libra','degree':20,'minute':16})
        self.assertTrue(receipt['first_part_of_children']['matches'])
        self.assertTrue(receipt['first_part_of_children']['conditional_on_declared_inferred_signs'])

    def test_second_chart_fortune_uses_figure_sun(self):
        receipt = r.comparison_receipt(TABLES)
        self.assertEqual(receipt['second_fortune']['result'], {'sign':'Taurus','degree':20,'minute':48})
        self.assertTrue(receipt['second_fortune']['matches'])

    def test_solar_alternative_does_not_silently_replace_figure(self):
        changed = copy.deepcopy(TABLES)
        for point in changed['figures'][1]['points']:
            if point['label'] == 'Sun':
                point['minute'] = 48
        receipt = r.comparison_receipt(changed)
        self.assertFalse(receipt['second_fortune']['matches'])
        self.assertEqual(receipt['second_fortune']['result']['minute'],52)
        self.assertEqual(r.comparison_receipt(TABLES)['question_sun_vs_reported_perfect_square_mismatch_minutes'],4)

    def test_opposite_cusp_mismatch_is_preserved(self):
        self.assertEqual(r.comparison_receipt(TABLES)['first_opposite_cusp_mismatch_minutes'],10)

    def test_moon_square_gap_uses_correct_ray(self):
        sat, moon = r.longitude('Aries',24,37), r.longitude('Capricorn',9,50)
        self.assertEqual(r.remaining_to_aspect(moon,sat,90,-1), 14*60+47)
        self.assertNotEqual(r.remaining_to_aspect(moon,sat,90,1), 14*60+47)
        for values in [(0,600,90,True),(0,None,90,1)]:
            with self.assertRaises(r.SourceInputError):
                r.remaining_to_aspect(*values)

    def test_mercury_conjunction_gap_and_difference(self):
        receipt = r.comparison_receipt(TABLES)
        self.assertEqual(receipt['mercury_to_saturn_conjunction_arc_minutes'],13*60+37)
        self.assertEqual(receipt['difference_minutes'],70)

    def test_local_delivery_conversion_preserves_fraction(self):
        value = r.timing_conversion(887,'XLIII_delivery_example','static_longitude_gap')
        self.assertEqual(value, {'quantity':Fraction(887,60),'unit':'week'})

    def test_direction_day_scale_is_different_method(self):
        value = r.timing_conversion(887,'XL_Part_of_Children_direction','ascensional_direction_arc')
        self.assertEqual(value, {'quantity':Fraction(887,60),'unit':'day'})

    def test_no_automatic_exchange_of_arc_types(self):
        for method,measure in [('XLIII_delivery_example','ascensional_direction_arc'),('XL_Part_of_Children_direction','static_longitude_gap'),('universal','static_longitude_gap')]:
            with self.subTest(method=method,measure=measure), self.assertRaises(r.SourceInputError):
                r.timing_conversion(887,method,measure)

    def test_reported_delivery_same_calendar_interval(self):
        receipt = r.comparison_receipt(TABLES)
        self.assertEqual(receipt['same_calendar_question_to_birth_days'],95)
        self.assertEqual(divmod(95,7),(13,4))
        self.assertEqual(receipt['reported_delivery_days_before_fourteen_week_point'],3)

    def test_date_helper_does_not_claim_calendar_conversion(self):
        with self.assertRaises(r.SourceInputError):
            r.same_calendar_days((1645,12,31),(1646,1,1))
        with self.assertRaises(r.SourceInputError):
            r.same_calendar_days((1700,2,28),(1700,3,1))

    def test_cusp_virtue_distances_remain_separate_from_vote(self):
        receipt = r.comparison_receipt(TABLES)
        self.assertEqual(receipt['moon_forward_to_fifth_cusp_minutes'],251)
        self.assertEqual(receipt['saturn_forward_to_ninth_cusp_minutes'],43)
        self.assertLess(receipt['moon_forward_to_fifth_cusp_minutes'],300)
        self.assertLess(receipt['saturn_forward_to_ninth_cusp_minutes'],300)


class SourceModelBoundaryTests(unittest.TestCase):
    def test_only_printed_house_year_mappings_are_supplied(self):
        self.assertEqual([r.house_year(h) for h in (1,2,10,7,4)], [1,2,3,4,5])
        self.assertTrue(all(r.house_year(h) is None for h in (3,5,6,8,9,11,12)))

    def test_gestation_alternatives_not_outcome_selected(self):
        self.assertEqual(r.gestation_alternatives('trine')['values'],[5,3])
        self.assertEqual(r.gestation_alternatives('sextile')['values'],[2,6])

    def test_gestation_ordinal_and_elapsed_language_preserved(self):
        self.assertEqual(r.gestation_alternatives('square')['basis'],'ordinal_month_of_conception')
        self.assertEqual(r.gestation_alternatives('opposition')['basis'],'months_already_conceived')

    def test_printed_twelve_votes_count_eight_four(self):
        self.assertEqual(len(TABLES['testimonies']),12)
        self.assertEqual(r.tally(TABLES['testimonies']), {'male':8,'female':4})

    def test_repeated_bodies_do_not_become_independent_observations(self):
        groups = r.dependency_groups(TABLES['testimonies'],planetary_bodies={'Moon','Mercury','Saturn','Jupiter'})
        self.assertEqual(groups['Saturn'],['M2','M3','M5'])
        self.assertEqual(groups['Mercury'],['F4','M1','M8'])
        self.assertEqual(groups['Jupiter'],['M6','M7'])

    def test_dependency_identification_requires_body_vocabulary(self):
        with self.assertRaises(r.SourceInputError):
            r.dependency_groups(TABLES['testimonies'],planetary_bodies=[])

    def test_votes_need_unique_ids_and_dependency_inputs(self):
        for rows in [[TABLES['testimonies'][0]]*2,[{'id':'X','direction':'male','dependencies':[]}],[{'id':'X','direction':'male','dependencies':'Moon'}]]:
            with self.assertRaises(r.SourceInputError):
                r.tally(rows)
        with self.assertRaises(r.SourceInputError):
            r.dependency_groups([{'id':'X','direction':'male','dependencies':'Moon'}], planetary_bodies={'Moon'})

    def test_full_hour_chain_sensitivity_yields_tie_without_editing_source(self):
        before = copy.deepcopy(TABLES['testimonies'])
        answer = r.sensitivity_tally(before,{'M6':'female','M7':'female'},interpretation='Counterfactual Moon hour and its Capricorn sign')
        self.assertEqual(answer['tally'],{'male':6,'female':6})
        self.assertFalse(answer['source_repaired'])
        self.assertEqual(before,TABLES['testimonies'])
        self.assertEqual(r.tally(before),{'male':8,'female':4})

    def test_sensitivity_requires_label_and_known_rows(self):
        for changes,label in [({'M6':'female'},''),({'NEW':'female'},'counterfactual')]:
            with self.assertRaises(r.SourceInputError):
                r.sensitivity_tally(TABLES['testimonies'],changes,interpretation=label)

    def test_missing_figure_minutes_and_later_table_are_distinct(self):
        mercury = next(x for x in TABLES['figures'][1]['points'] if x['label']=='Mercury')
        self.assertIsNone(mercury['minute'])
        with self.assertRaises(r.SourceInputError):
            r.read_coordinate(mercury)
        self.assertEqual(mercury['arithmetic_table_value']['minute'],0)
        self.assertEqual(TABLES['delivery_table']['mercury'],['Aries',11,0])

    def test_chart_and_testimony_hour_conflict_not_repaired(self):
        second = TABLES['figures'][1]
        self.assertEqual(second['hour_lord_printed'],'Moon')
        self.assertEqual(second['hour_lord_in_testimony_table'],'Jupiter')

    def test_coordinate_inventory_and_all_complete_values_valid(self):
        entries = [x for figure in TABLES['figures'] for key in ('cusps','points') for x in figure[key]]
        self.assertEqual(len(entries),TABLES['coordinate_entry_count'])
        self.assertEqual(len(entries),45)
        missing = [x for x in entries if x['minute'] is None]
        self.assertEqual([x['label'] for x in missing],['Mercury'])
        for row in entries:
            if row['minute'] is not None:
                self.assertEqual(r.zodiac(r.read_coordinate(row)),{k:row[k] for k in ('sign','degree','minute')})

    def test_case_inventory_does_not_inflate_marks_or_transits(self):
        cases = json.loads((HERE/'HISTORICAL_CASES.json').read_text())
        self.assertEqual((cases['case_count'],cases['dated_enquiries'],cases['printed_charts']),(2,2,2))
        self.assertEqual(cases['cases'][0]['bodily_mark_count'],5)
        self.assertTrue(all(not x['independently_verified'] for x in cases['cases']))

    def test_reference_results_make_no_ephemeris_or_accuracy_claim(self):
        receipt = r.comparison_receipt(TABLES)
        self.assertFalse(receipt['historical_ephemeris_computed'])
        self.assertFalse(receipt['accuracy_evaluated'])


class SourceLedgerIntegrityTests(unittest.TestCase):
    def test_canonical_records_unique_contiguous_and_counted(self):
        data = json.loads((HERE/'RULES.json').read_text())
        ids = [x['id'] for x in data['rules']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),data['records_count'])
        self.assertEqual([int(x.rsplit('R',1)[1]) for x in ids],list(range(1157,1157+len(ids))))
        self.assertEqual(data['general_records_count']+data['worked_example_records_count'],len(ids))

    def test_every_record_has_source_anchor_logic_and_reference_scope(self):
        data = json.loads((HERE/'RULES.json').read_text())
        for record in data['rules']:
            self.assertTrue(record['source_locator']['passage_anchor'],record['id'])
            self.assertTrue(record['prerequisites'],record['id'])
            self.assertTrue(all(256 <= p <= 276 for p in record['source_locator']['pdf_pages']),record['id'])
            self.assertEqual(record['runtime_status'],'REFERENCE_ONLY_NOT_PROMOTED')
            self.assertFalse(record['independent_evidence_unit'])

    def test_issue_references_resolve_without_dropping_open_limits(self):
        records = json.loads((HERE/'RULES.json').read_text())['rules']
        issues = json.loads((HERE/'UNRESOLVED.json').read_text())['issues']
        ids = {x['id'] for x in issues}
        self.assertEqual(len(ids),len(issues))
        for record in records:
            self.assertTrue(set(record['unresolved_ids']) <= ids,record['id'])

    def test_coverage_and_boundary_do_not_claim_sixth_house_extraction(self):
        coverage = json.loads((HERE/'SECTION_COVERAGE.json').read_text())
        self.assertEqual(coverage['admitted_pdf_pages'],list(range(256,277)))
        self.assertEqual(coverage['next']['pdf_page'],277)
        self.assertEqual(coverage['next']['printed_page'],243)
        self.assertFalse(coverage['next']['extracted'])
        self.assertEqual(coverage['numbered_chapters'],['XXXIX','XL','XLI','XLII','XLIII'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
