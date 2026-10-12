"""Selected invariants of documentarily extracted original 1647 Chapter XLVI."""
from pathlib import Path
from datetime import date
import json,hashlib,unittest
B=Path(__file__).resolve().parent
def rd(n):return json.loads((B/n).read_text())
D=rd('RULES.json');R=D['rules'];CASE=rd('CASE_EVIDENCE.json');CHART=rd('CHART_INSCRIPTION.json')
U=rd('UNRESOLVED.json');S=rd('SOURCE_IDENTITY.json');M=rd('SOURCE_IMAGE_MANIFEST.json')
C=rd('COUNTS.json')
def rec(n):return R[n-1770]
def t(n):return rec(n)['source_statement']+' '+' '.join(rec(n)['preconditions'])+' '+' '.join(rec(n)['exceptions_and_evidence_limits'])
class Integrity(unittest.TestCase):
 def test_contiguous_record_numbers(self):
  self.assertEqual([q['id'] for q in R],[f'LI.1647.II.XLVI.R{i}' for i in range(1770,1794)])
 def test_unit_counts(self):
  self.assertEqual((len(R),C['new_documentary_records'],C['lilly_before'],C['lilly_after_if_accepted'],C['combined_if_accepted']),(24,24,1769,1793,2859))
 def test_source_full_original_identity(self):
  self.assertEqual(S['source_full_pdf_sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
  self.assertEqual(M['source_full_pdf_sha256'],S['source_full_pdf_sha256'])
 def test_pages_span_exact(self):
  self.assertEqual({q['source_locator']['pdf_pages'][0] for q in R},{323,324})
  self.assertEqual(S['admitted_pdf_pages'],[323,324])
 def test_source_rasters_have_exact_frozen_hashes(self):
  for v in M['admitted']:
   p=B/v['path'];self.assertEqual(p.stat().st_size,v['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),v['sha256'])
 def test_case_identity(self):
  ids={q['case_id'] for q in R if q['case_id']}
  self.assertEqual(len(ids),1)
  self.assertEqual(C['distinct_historical_cases'],1)
 def test_all_24_are_not_independent_patients(self):
  self.assertTrue(all(not q['case_evidence_countable'] and not q['chart_countable'] for q in R))
 def test_not_runtime_or_clinically_validated(self):
  self.assertTrue(all(q['runtime_status']=='REFERENCE_ONLY_NOT_PROMOTED' and not q['clinical_efficacy_verified'] for q in R))
  self.assertTrue(all(not q['independently_verified_patient_outcome'] and not q['blinded_prospective_prediction'] for q in R))
 def test_readings_not_called_diplomatic_quotations(self):
  self.assertEqual(sum(q['source_statement_type']=='EDITORIAL_DERIVED_ARITHMETIC' for q in R),1);self.assertTrue(all(q['source_statement_type'] in ('EDITORIAL_DERIVED_ARITHMETIC','NORMALIZED_PARAPHRASE_NOT_A_DIPLOMATIC_TRANSCRIPTION') for q in R))
 def test_provenance_localized(self):
  self.assertTrue(all(q['source_sha256']==S['source_full_pdf_sha256'] and q['chapter']=='XLVI' for q in R))
 def test_source_qualifiers_present(self):
  self.assertTrue(all(q['preconditions'] and q['exceptions_and_evidence_limits'] for q in R))
 def test_unresolved_retained(self):
  self.assertEqual(U['retained_count'],len(U['limits']))
  self.assertGreaterEqual(len(U['limits']),24)
 def test_kind_counts_reproduced(self):
  from collections import Counter
  self.assertEqual(dict(Counter(q['source_record_kind'] for q in R)),C['kind_counts'])
 def test_single_source_chart_and_reported_death(self):
  self.assertEqual((CASE['individuals_in_passage'],CASE['original_charts_in_passage']),(1,1))
  self.assertTrue(CASE['author_reported_outcome'])
  self.assertFalse(CASE['independent_outcome_verification'])
 def test_no_reported_prediction_freeze(self):
  self.assertFalse(CASE['documented_prepublication_prediction_freeze'])
  self.assertFalse(CASE['count_as_validated_prediction'])
class SourceConditions(unittest.TestCase):
 def test_chart_inscription_date(self):
  self.assertEqual(CHART['source_weekday_as_printed'],'Die Mercurij')
  self.assertEqual(CHART['source_question_date_text'],'16 Julij 1645')
  self.assertEqual(CHART['source_clock_time'],'7:22 AM:')
 def test_julian_is_inferred(self):
  self.assertTrue(CHART['julian_not_explicit_in_print'])
  self.assertEqual(CHART['inferred_english_julian_date'],'1645-07-16')
  self.assertEqual(CHART['computed_extended_gregorian_equivalent'],'1645-07-26')
  self.assertEqual(date(1645,7,26).strftime('%A'),'Wednesday')
 def test_planetary_hour_not_clock_or_timezone(self):
  self.assertEqual(CHART['source_planetary_hour_glyph'],'♄')
  self.assertTrue(CHART['timezone_unknown'])
  self.assertFalse(CHART['source_location_printed'])
 def test_chart_partial_reading(self):
  self.assertFalse(CHART['chart_all_glyphs_identified'])
 def test_virgo_mars_eighth(self):
  self.assertIn('Virgo',t(1773));self.assertIn('corporeal presence',t(1773))
  self.assertIn('partly',t(1773))
 def test_aquarius_sixth_uncertain_glyph(self):
  s=t(1775).lower()
  self.assertIn('aquarius',s)
  self.assertIn('☋',s);self.assertIn('orientation',s)
 def test_saturn_taurus_fixed(self):
  s=t(1776).lower()
  for x in ('saturn','taurus','fixed','earthy'):self.assertIn(x,s)
 def test_moon_near_mars_not_forced_conjunction(self):
  self.assertIn('proximity',t(1777))
  self.assertIn('not a verified conjunction',t(1777))
 def test_body_symptoms_not_verified(self):
  for n in (1778,1779,1780):
   self.assertEqual(rec(n)['claim_class'],'AUTHOR_MEDICAL_INFERENCE')
 def test_all_which_true_is_source_self_report(self):
  self.assertIn('All which was true',t(1781))
  self.assertFalse(CASE['independent_outcome_verification'])
 def test_initial_survival_window(self):
  self.assertIn('ten or twelve days',t(1783))
  self.assertEqual(rec(1783)['claim_class'],'AUTHOR_REPORTED_PROGNOSIS')
 def test_four_printed_reasons_distinct(self):
  self.assertEqual([rec(n)['source_record_kind'] for n in range(1784,1788)],['reason_one','reason_two','reason_three','reason_four'])
 def test_cauda_leonis_not_dragon_tail(self):
  self.assertIn('Cauda Leonis',t(1786))
  self.assertIn('node glyph',t(1786))
 def test_sextile_square_qualification(self):
  self.assertIn('more properly a square',t(1787))
  self.assertIn('Mercury',t(1787))
  self.assertIn('Jupiter',t(1787))
 def test_death_is_author_reported(self):
  self.assertIn('28th of July',t(1788))
  self.assertEqual(rec(1788)['claim_class'],'AUTHOR_REPORTED_OUTCOME')
 def test_12_days_internal_not_independent(self):
  self.assertEqual((date(1645,7,28)-date(1645,7,16)).days,12)
  self.assertEqual(CASE['calendar_date_difference_days'],12)
  self.assertIn('No contemporaneous prediction freeze',t(1789))
 def test_after_outcome_transits_separate(self):
  for n in (1790,1791,1792):
   self.assertEqual(rec(n)['claim_class'],'AUTHOR_REPORTED_POST_OUTCOME_TIMING')
   self.assertTrue(any('retrospect' in s.lower() or 'after' in s.lower() for s in rec(n)['exceptions_and_evidence_limits']))
 def test_next_crisis_chapter_excluded(self):
  self.assertIn('XLVII',t(1793))
  self.assertIn('not admitted',t(1793))
 def test_parent_no_medical_advice(self):
  self.assertIn('not medical advice',(B/'AUDIT_REPORT.md').read_text().lower())
 def test_rare_source_terms_preserved(self):
  self.assertIn('long-ascension',t(1787))
  self.assertIn('Cauda Leonis',t(1786))
if __name__=='__main__':unittest.main()
