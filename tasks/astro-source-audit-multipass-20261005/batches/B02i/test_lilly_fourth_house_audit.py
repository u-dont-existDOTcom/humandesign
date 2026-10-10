"""Admission checks for source provenance, full record inventory and case units."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parent


def read(name): return json.loads((ROOT/name).read_text())


class SourceAdmissionTests(unittest.TestCase):
    def test_source_ids_are_contiguous_and_all_admitted_pages_have_records(self):
        records = read('RULES.json')['rules']
        self.assertEqual([int(r['id'].rsplit('R',1)[1]) for r in records], list(range(1009,1157)))
        self.assertEqual(len(records), len({r['id'] for r in records}))
        pages = {p for r in records for p in r['source_locator']['pdf_pages']}
        self.assertEqual(pages, set(range(236,257)))
        self.assertTrue(all(r['source_locator']['passage_anchor'] for r in records))
        self.assertTrue(all(not r['independent_evidence_unit'] for r in records))

    def test_source_first_notes_retain_all_three_frozen_hashes(self):
        expected = {
            'source_a':'a969e9e3f75124b0d869608c432a05db7b59fae4751bb46ee940815726edb979',
            'source_b':'93dadb60d8acdae63ed259ce6bc43aee84e71f16e5944fa0f70ed108c54df373',
            'worked_chart':'d718c9195068047fb7dd12e78d321e9a2049fa3273a96f1a8eb21d1dea93ed1e'}
        for folder,digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT/'independent_review'/folder/'SOURCE_FIRST_NOTES.md').read_bytes()).hexdigest(),digest)

    def test_every_raw_candidate_survives_in_source_fields(self):
        records = {r['local_id']:r for r in read('RULES.json')['rules']}
        groups = [('source_a','records','local_id'),('source_b','rules','local_id'),('worked_chart','candidates','id')]
        total = 0
        for folder,key,idkey in groups:
            for raw in read(f'independent_review/{folder}/CANDIDATE_RULES.json')[key]:
                self.assertEqual(records[raw[idkey]]['source_fields'],raw)
                total += 1
        self.assertEqual(total,len(records))

    def test_issue_links_resolve_and_resolved_readings_are_counted_separately(self):
        rules = read('RULES.json')['rules']; issues = read('UNRESOLVED.json')
        ids = {r['id'] for r in rules}; issue_ids = {r['id'] for r in issues['issues']}
        self.assertEqual(issues['issues_count'],len(issue_ids))
        self.assertEqual(issues['resolved_readings_count'],len(issues['resolved_readings']))
        for row in issues['issues']+issues['resolved_readings']:
            self.assertTrue(set(row['record_ids']) <= ids)
        for row in rules: self.assertTrue(set(row['unresolved_ids']) <= issue_ids)

    def test_numeric_table_preserves_frozen_copy_and_omissions(self):
        self.assertEqual((ROOT/'WORKED_NUMERIC_TABLES.json').read_bytes(),
                         (ROOT/'independent_review/worked_chart/NUMERIC_TABLES.json').read_bytes())
        chart = read('WORKED_NUMERIC_TABLES.json')['charts'][0]
        self.assertEqual(chart['entry_count'],22)
        self.assertEqual(len(chart['house_cusps'])+len(chart['bodies_and_points']),22)
        self.assertEqual([r['house'] for r in chart['house_cusps'] if r['coordinate']['minute'] is None],[4,10])
        self.assertTrue(all(not r['sign_printed_adjacent'] for r in chart['bodies_and_points']))

    def test_one_enquiry_is_not_multiplied_by_episodes_or_body_marks(self):
        cases = read('HISTORICAL_CASES.json')
        self.assertEqual(cases['dated_enquiry_count'],1)
        self.assertEqual(cases['printed_chart_count'],1)
        self.assertEqual(cases['independently_verified_outcome_count'],0)
        case = cases['cases'][0]
        self.assertEqual(len(case['body_mark_records']),5)
        self.assertTrue(all(r['independent_case'] is False for r in case['episodes']))
        self.assertTrue(all(r['record_ids'] for r in cases['unspecified_experience_accounts']))

    def test_declared_whole_span_includes_top256_and_stops_before_fifth_house(self):
        receipt = read('READING_RECEIPT.json'); coverage = read('SECTION_COVERAGE.json')
        self.assertEqual(receipt['root_original_whole_pages_visually_read_for_extraction'],list(range(236,256)))
        self.assertIn('256',receipt['root_partial_page_visually_read_for_extraction'])
        self.assertIn('Fifth-house',coverage['boundary']['next'])
        self.assertTrue(all(r['record_ids'] for r in coverage['page_coverage']))

    def test_reference_export_matches_implementation_and_comparisons_resolve(self):
        import lilly_fourth_house_reference as reference
        self.assertEqual(read('QUERY_REFERENCES.json'),reference.reference_inventory())
        retained = read('RETAINED_SOURCE_EXCERPTS.json')
        for comparison in read('CROSS_SOURCE_COMPARISONS.json')['comparisons']:
            for item in comparison['earlier_records']:
                value = retained
                for token in item['excerpt_pointer'].strip('/').split('/'):
                    value = value[int(token)] if isinstance(value,list) else value[token]
                self.assertEqual(value['id'],item['record_id'])


if __name__ == '__main__': unittest.main()
