"""Only structural/source-reference regression checks; NO clinical or predictive validity."""
from pathlib import Path
import json,hashlib,unittest
P=Path(__file__).resolve().parent
def read(name):return json.loads((P/name).read_text())
RULES=read('RULES.json')['rules']
C=read('COUNTS.json')
I=read('APHORISM_INDEX.json')
U=read('UNRESOLVED.json')
S=read('SOURCE_IDENTITY.json')
M=read('SOURCE_IMAGE_MANIFEST.json')
def by(n):return RULES[n-1]
def text(n):return by(n)['source_statement']+' '+' '.join(by(n)['prerequisites'])+' '+' '.join(by(n)['exceptions_and_modifiers'])
class RecordIntegrity(unittest.TestCase):
 def test_unique_consecutive_ids(self):
  self.assertEqual([r['id'] for r in RULES],[f'LI.1647.II.XLIV.R{i}' for i in range(1703,1746)])
 def test_exact_numbering(self):
  self.assertEqual([r['source_aphorism_number'] for r in RULES],list(range(1,44)))
 def test_counts(self):
  self.assertEqual((len(RULES),C['previous_lilly'],C['cumulative_lilly_if_accepted'],C['combined_if_accepted']),(43,1702,1745,2811))
 def test_source_identity(self):
  self.assertEqual(S['sha256'],M['source_pdf_sha256'])
  self.assertEqual(S['sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
 def test_source_page_coverage(self):
  self.assertEqual(set(p for r in RULES for p in r['source_locator']['pdf_pages']),set(range(316,321)))
 def test_cross_page_entries(self):
  for n,pages in [(9,[316,317]),(30,[318,319]),(42,[319,320])]:
   self.assertEqual(by(n)['source_locator']['pdf_pages'],pages)
 def test_index_and_records_match(self):
  self.assertEqual([(x['number'],x['id']) for x in I['entries']],[(r['source_aphorism_number'],r['id']) for r in RULES])
 def test_original_png_digest_integrity(self):
  self.assertEqual(len(M['images']),5)
  for entry in M['images']:
   path=P/entry['path']
   self.assertTrue(path.is_file())
   self.assertEqual(path.stat().st_size,entry['bytes'])
   self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),entry['sha256'])
 def test_locator_context(self):
  self.assertTrue(all(r['source_locator']['source_id']==S['source_id'] and r['source_locator']['chapter']=='XLIV' and r['source_locator']['book']=='II' for r in RULES))
 def test_every_record_has_prerequisites_and_qualifiers(self):
  self.assertTrue(all(r['prerequisites'] and r['exceptions_and_modifiers'] and r['source_statement'] for r in RULES))
 def test_none_promoted_to_runtime(self):
  self.assertTrue(all(r['source_interpretation_status']=='REFERENCE_ONLY_NOT_PROMOTED' and not r['clinical_or_predictive_validity'] and not r['independent_evidence_unit'] for r in RULES))
 def test_none_presented_as_patient_case(self):
  self.assertTrue(all(r['case_id'] is None and not any(r['case_evidence'].values()) for r in RULES))
 def test_exact_coverage_index(self):
  coverage=read('SECTION_COVERAGE.json')['coverage']
  self.assertEqual([x['aphorism'] for x in coverage],list(range(1,44)))
  self.assertEqual([x['record'] for x in coverage],[r['id'] for r in RULES])
 def test_no_misattributed_quote(self):
  self.assertTrue(all('not declared diplomatic quotation' in r['source_locator']['anchor_type'] for r in RULES))
 def test_historical_genre(self):
  self.assertTrue(all(r['source_genre']=='historical horary/medical astrology; unvalidated' for r in RULES))
 def test_counts_per_kind(self):
  from collections import Counter
  self.assertEqual(dict(Counter(r['kind'] for r in RULES)),C['kind_counts'])
class ConditionalGuards(unittest.TestCase):
 def test_physician_distinct_from_medicine(self):
  self.assertIn('seventh',text(3).lower());self.assertIn('tenth',text(3).lower())
 def test_hour_of_first_visit_vs_beginning_cure(self):
  self.assertIn('FIRST physician visit',text(5))
  self.assertIn('FIRST begins cure',text(6))
  self.assertIn('FIRST physician visit',text(7))
 def test_urine_consent_alternatives_retained(self):
  self.assertIn('whether the querent came with consent or not',text(8))
  self.assertIn('OR consent',text(9))
  self.assertIn('eleventh',text(9))
 def test_both_luminaries_condition(self):
  self.assertIn('BOTH',text(11))
  self.assertIn('both versus either',text(12).lower())
 def test_malefic_reception_exception(self):
  self.assertIn('reception',text(13).lower())
 def test_two_significators_uncertain(self):
  self.assertIn('two of these Significators',text(14))
 def test_aphorism15_doubt_not_certainty(self):
  self.assertIn('doubtfull',text(15))
 def test_eighth_reception_not_necessarily_mutual(self):
  self.assertIn('without reciprocal reception',text(17))
 def test_aphorism18_unprinted_tenth_not_completed(self):
  self.assertIn('The tenth is not listed',text(18))
 def test_aphorism19_odd_negative_literal_retained(self):
  self.assertIn('great fear of recovery',text(19))
  self.assertNotIn('fear of death',by(19)['source_statement'])
 def test_aphorism20_moon_speed_light_aspects_and_reception(self):
  s=text(20).lower()
  for word in ('swift','increasing in light','sextile','trine','reception'):self.assertIn(word,s)
 def test_aphorism23_application_to_conjunction(self):
  self.assertIn('CONJUNCTION',text(23))
 def test_aphorism25_station_and_combustion_separate(self):
  self.assertIn('stationary',text(25));self.assertIn('Combustion',text(25))
 def test_body_spirits_animals_not_diagnosis(self):
  for w in ('body','spirits'):self.assertIn(w,text(27).lower())
  self.assertIn('Animals',text(28))
  self.assertIn('no psychiatric diagnosis',text(28).lower())
 def test_house_lists_exact(self):
  for n in [29]:
   for x in ['ninth','eleventh','tenth','seventh','fourth','twelfth','eighth']:
    self.assertIn(x,text(n).lower())
 def test_natal_overlay_explicit(self):
  for n in [32,33,34]:
   self.assertTrue('natal' in text(n).lower() or 'nativity' in text(n).lower())
  self.assertIn('therein',text(33).lower());self.assertIn('thither',text(33).lower())
  self.assertIn('Revolution',text(34))
 def test_illness_money_is_separate_endpoint(self):
  self.assertIn('expensive',text(35))
 def test_sun_exception(self):
  self.assertIn('Jupiter',text(38))
  self.assertIn('Sun',text(38))
 def test_patient_blame_not_reified(self):
  self.assertIn('not evidence of actual behaviour',text(40))
 def test_waxing_and_waning_distinct_from_speed(self):
  self.assertIn('waxing',text(43).lower())
  self.assertIn('waning',text(43).lower())
  self.assertIn('speed',text(43))
 def test_18_retained_uncertainties(self):
  self.assertEqual(U['retained_count'],len(U['limits']))
  self.assertGreaterEqual(len(U['limits']),18)
 def test_four_original_errata_are_bounded(self):
  e=read('ERRATA_COLLATION.json')['entries']
  self.assertEqual([(x['printed_page'],x['printed_line']) for x in e],[(284,'14'),(284,'37'),(285,'4'),(285,'11')])
  self.assertTrue(all(x['status'] and x['aphorism'] in (23,30,31,33) for x in e))
 def test_report_source_only(self):
  report=(P/'AUDIT_REPORT.md').read_text()
  self.assertIn('predictive',report.lower())
  self.assertIn('R1703',report)
  self.assertIn('Chapter XLV',report)
if __name__=='__main__':unittest.main()
