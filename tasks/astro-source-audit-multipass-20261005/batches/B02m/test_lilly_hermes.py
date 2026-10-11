"""Focused historical source-data checks only. Never interpreted as clinical efficacy."""
import hashlib,json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((ROOT/n).read_text())
rules=load('RULES.json')['rules']
count=load('COUNTS.json')
table=load('REFERENCE_TABLES.json')
source=load('SOURCE_IDENTITY.json')
catalogue=load('MATERIA_MEDICA_TABLES.json')
images=load('SOURCE_IMAGE_MANIFEST.json')
ZOD='Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces'.split()
class RecordIntegrity(unittest.TestCase):
    def test_exact_unique_ids(self):
        self.assertEqual([r['id'].rsplit('R',1)[1] for r in rules],[str(i) for i in range(1651,1703)])
    def test_count_bookkeeping(self):
        self.assertEqual((len(rules),count['cumulative_lilly'],count['combined']),(52,1702,2768))
    def test_source_hash_equals_replayed_manifest(self):
        self.assertEqual(source['sha256'],images['source_pdf_sha256'])
        self.assertEqual(source['sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
    def test_page_continuity(self):
        allpages=set(sum((r['source_locator']['pdf_pages'] for r in rules),[]))
        self.assertEqual(allpages,set(range(302,317)))
    def test_every_record_has_source_locator(self):
        self.assertTrue(all(r['source_locator']['passage_anchor'] and r['source_locator']['pdf_pages'] and r['source_statement'] for r in rules))
    def test_each_page_render_digest(self):
        self.assertEqual(len(images['images']),15)
        for item in images['images']:
            path=ROOT/item['path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),item['sha256'])
    def test_source_presentation_not_runtime(self):
        self.assertTrue(all(r['runtime_status']=='REFERENCE_ONLY_NOT_PROMOTED' and not r['independent_evidence_unit'] for r in rules))
    def test_no_case_or_verified_endpoint(self):
        self.assertTrue(all(r['case_id'] is None and not any(r['case_evidence'].values()) for r in rules))
    def test_exact_boundaries(self):
        self.assertEqual(rules[0]['source_locator']['pdf_pages'],[302])
        self.assertEqual(rules[-1]['source_locator']['pdf_pages'],[316])
        self.assertIn('Aphorismes',load_text('CONTINUE_HANDOFF.md'))
    def test_coverage_no_unmapped_records(self):
        docs=load('SECTION_COVERAGE.json')['sections']
        ids=set(sum((section['related_ids'] for section in docs),[]))
        self.assertEqual(ids,{x['id'] for x in rules})
class Catalogues(unittest.TestCase):
    def test_both_have_full_sign_keys(self):
        self.assertEqual(list(table['saturn']),ZOD)
        self.assertEqual(list(table['mars']),ZOD)
    def test_sign_links_are_disjoint(self):
        self.assertEqual(set(table['saturn'].values()) & set(table['mars'].values()),set())
    def test_saturn_gemini_extra_conditions(self):
        r=next(r for r in rules if r['planetary_afflictor']=='Saturn' and r['sign']=='Gemini')
        self.assertIn('Mars',str(r['exceptions_and_modifiers']))
    def test_mars_virgo_prognosis_exception(self):
        r=next(r for r in rules if r['planetary_afflictor']=='Mars' and r['sign']=='Virgo')
        self.assertIn('benefic',str(r['exceptions_and_modifiers']).lower())
    def test_mars_aquarius_lunar_motion_and_time_limit(self):
        r=next(r for r in rules if r['planetary_afflictor']=='Mars' and r['sign']=='Aquarius')
        self.assertIn('twenty days',r['source_statement'])
        self.assertIn('slow waning',r['source_statement'])
    def test_mars_pisces_waxing_contrasts_aquarius(self):
        r=next(r for r in rules if r['planetary_afflictor']=='Mars' and r['sign']=='Pisces')
        self.assertIn('waxing',r['source_statement'])
    def test_sensory_correspondence(self):
        self.assertEqual(table['printed_senses']['left_eye'],'Moon')
        self.assertEqual(table['printed_senses']['right_eye'],'Sun')
    def test_historical_materia_includes_toxic_warning(self):
        self.assertTrue(any('White Lead' in item for col in catalogue['cooling']['columns'] for item in col))
        self.assertFalse(catalogue['interpretation']['modern_validity'])
    def test_historical_materia_two_multi_column_lists(self):
        self.assertEqual(len(catalogue['cooling']['columns']),3)
        self.assertEqual(len(catalogue['heating']['columns']),3)
    def test_unresolved_ambiguous_authorship(self):
        self.assertGreaterEqual(load('UNRESOLVED.json')['retained_count'],12)

def load_text(name):return (ROOT/name).read_text()

class RecoveryRegressions(unittest.TestCase):
    def r(self,n): return next(x for x in rules if x['id'].endswith('R'+str(n)))
    def test_scorpio_negative_urinary_polarity(self):
        self.assertEqual(self.r(1684)['source_quote_exact']['text'],'no retention of Urine')
        self.assertIn('no retention',self.r(1684)['source_statement'])
        self.assertIn('no retention',' '.join(self.r(1684)['source_details']))
    def test_cooling_rows_not_fused(self):
        rows=catalogue['cooling']['columns'][1]
        self.assertEqual(rows[1:3],['Purcel and','White of an Egge'])
        self.assertIn('Blackberry-Tree',rows)
    def test_opposing_remedy_passages_retained(self):
        self.assertIn('refrigerating',' '.join(self.r(1672)['source_details']))
        self.assertIn('heating',' '.join(self.r(1675)['source_details']))
        self.assertTrue(any(x['id']=='U15' for x in load('UNRESOLVED.json')['limits']))
    def test_speed_states_are_not_silently_equated(self):
        self.assertIn('motion decreasing',' '.join(self.r(1668)['prerequisites']))
        self.assertIn('DECREASING',' '.join(self.r(1700)['source_details']))
        self.assertIn('SWIFT',' '.join(self.r(1701)['source_details']))
    def test_timing_quantifiers_remain_distinct(self):
        self.assertIn('ABOUT THE NINTH',' '.join(self.r(1694)['source_details']))
        self.assertIn('WITHIN THIRTY',' '.join(self.r(1695)['source_details']))
        self.assertIn('TRUE SQUARE',' '.join(self.r(1698)['source_details']))
    def test_every_record_has_exactly_one_primary_section(self):
        ids=[x for section in load('SECTION_COVERAGE.json')['sections'] for x in section['related_ids']]
        self.assertEqual(len(ids),52)
        self.assertEqual(len(set(ids)),52)
    def test_locators_separate_visible_labels_from_sequence(self):
        loc=self.r(1691)['source_locator']
        self.assertEqual(loc['printed_sequence_expected'],[278])
        self.assertIn('279',loc['visible_printed_labels'][0])
        self.assertTrue(all(x['source_locator']['anchor_type'].startswith('locating_phrase') for x in rules))
    def test_complete_detail_and_three_matched_errata(self):
        self.assertTrue(all(x['source_details'] and x['original_draft_record_sha256'] for x in rules))
        self.assertEqual([x['printed_page'] for x in load('TEXTUAL_CHECKS.json')['matched_entries']],[272,274,277])

if __name__=='__main__':unittest.main()
