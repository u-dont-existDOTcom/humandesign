"""Structural and source-clause regression tests; not clinical or predictive validation."""
from pathlib import Path
import json,hashlib,unittest
B=Path(__file__).resolve().parent
def load(n):return json.loads((B/n).read_text())
D=load('RULES.json');R=D['rules'];C=load('COUNTS.json');P=load('CASE_EVIDENCE.json')
K=load('CHART_INSCRIPTION.json');S=load('SOURCE_IDENTITY.json');I=load('SOURCE_IMAGE_MANIFEST.json')
A=load('SECTION_COVERAGE.json');U=load('UNRESOLVED.json')
def record(i):return R[i-1746]
def body(i):
 r=record(i);return ' '.join([r['source_statement']]+r['preconditions']+r['exceptions_and_evidence_limits']).lower()
class Structure(unittest.TestCase):
 def test_24_continuous_record_ids(self):
  self.assertEqual([r['id'] for r in R],[f'LI.1647.II.XLV.R{i}' for i in range(1746,1770)])
 def test_source_counts(self):
  self.assertEqual((len(R),C['prior_lilly'],C['cumulative_lilly_if_accepted'],C['combined_if_accepted']),(24,1745,1769,2835))
 def test_one_person_and_one_chart(self):
  self.assertEqual((P['number_of_individuals_reported'],P['printed_query_chart_count']), (1,1))
  self.assertEqual(C['historical_cases_reported'],1)
 def test_case_group_single(self):
  self.assertEqual(len({r['case_id'] for r in R}),1)
  self.assertEqual(len({r['case_independence_group'] for r in R}),1)
 def test_historical_source_identity(self):
  self.assertEqual(S['sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
  self.assertEqual(S['full_original_bytes'],141842963)
 def test_all_source_identity_matching(self):
  self.assertTrue(all(r['source_sha256']==S['sha256'] and r['source_id']==S['source_id'] for r in R))
 def test_book_and_chapter(self):
  self.assertTrue(all(r['book']=='II' and r['chapter']=='XLV' for r in R))
 def test_png_bytes_verified(self):
  self.assertEqual(len(I['images']),3)
  for x in I['images']:
   p=B/x['filename'];self.assertTrue(p.is_file())
   self.assertEqual(p.stat().st_size,x['bytes'])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['sha256'])
 def test_admitted_pages_only(self):
  self.assertEqual(S['admitted_pdf_pages'],[320,321,322])
  self.assertEqual(S['next_heading_boundary_pdf_page'],323)
 def test_section_index_matches_records(self):
  self.assertEqual([x['id'] for x in A['source_records']],[r['id'] for r in R])
  for i,r in enumerate(R):self.assertEqual(r['source_locator']['pdf_pages'],A['source_records'][i]['pdf_pages'])
 def test_next_chapter_excluded(self):
  self.assertEqual(A['following_boundary']['chapter'],'XLVI')
  self.assertEqual(record(1769)['kind'],'chapter_boundary_and_case_identity')
 def test_all_claims_have_source_qualifiers(self):
  self.assertTrue(all(r['source_statement'] and r['preconditions'] and r['exceptions_and_evidence_limits'] for r in R))
 def test_20_unresolved(self):
  self.assertEqual(U['retained_count'],len(U['issues']))
  self.assertGreaterEqual(U['retained_count'],20)
 def test_no_verbatim_transcript_claim(self):
  self.assertTrue(all(r['source_statement_class']=='NORMALIZED_PARAPHRASE_NOT_DIPLOMATIC_TRANSCRIPTION' for r in R))
 def test_no_runtimes(self):
  self.assertTrue(all(r['runtime_status']=='REFERENCE_ONLY_NOT_PROMOTED' and not r['source_ruleset_implementation_ready'] for r in R))
 def test_no_independent_patient_outcomes(self):
  self.assertFalse(P['outcome_independently_verified'])
  self.assertTrue(all(not r['independent_patient_outcome_verified'] for r in R))
 def test_no_blinded_prospective_successes(self):
  self.assertFalse(P['documented_prediction_freeze_before_outcome'])
  self.assertTrue(all(not r['blinded_prospective_prediction'] for r in R))
 def test_no_clinical_efficacy(self):
  self.assertFalse(P['direct_causal_or_medical_efficacy_evidence'])
  self.assertTrue(all(not r['clinical_efficacy_verified'] for r in R))
class SourceConditionGuards(unittest.TestCase):
 def test_correct_jupiter_day_glyph(self):
  self.assertEqual(K['source_weekday_glyph'],'♃')
  self.assertEqual(K['source_day_of_month'],8)
  self.assertIn('not numeral 24',body(1746))
 def test_date_calendar_context(self):
  self.assertEqual(P['inferred_julian_question_date'],'1645-05-08')
  self.assertEqual(K['proleptic_gregorian_equivalent'],'1645-05-18')
 def test_wrong_prior_date_is_superseded(self):
  self.assertIn('24 May',K['earlier_erroneous_transcription'])
  self.assertIn('not 24 May 1645',(B/'CHAPTER_XLV_DATE_CORRECTION.md').read_text())
 def test_no_modern_timezone(self):
  self.assertTrue(P['clock_time_zone_unresolved'])
  self.assertIsNone(K['time_zone_source'])
 def test_chart_not_modern_ephemeris(self):
  self.assertFalse(K['diagram_full_degree_transcription_complete'])
  self.assertFalse(P['chart_reproduction_from_modern_ephemeris'])
 def test_scropio_and_chele(self):
  self.assertIn('scorpio',body(1748));self.assertIn('chelæ',body(1748))
 def test_saturn_fall_in_sixth(self):
  self.assertIn('saturn',body(1749));self.assertIn('sixth',body(1749));self.assertIn('fall',body(1749))
 def test_body_reference_head_breast_heart(self):
  for i,w in [(1750,'head'),(1751,'breast'),(1752,'heart')]:self.assertIn(w,body(i))
 def test_prior_square_cancer_vs_current_leo(self):
  self.assertIn('leo',body(1752))
  self.assertIn('cancer',body(1753));self.assertIn('at that time',body(1753))
 def test_melancholy_primary_and_choler_secondary(self):
  self.assertIn('principal',body(1755));self.assertIn('secondary',body(1757))
 def test_patient_symptoms_not_independent_cases(self):
  self.assertIn('head',body(1759));self.assertIn('red gravels',body(1763))
  self.assertEqual(record(1759)['case_id'],record(1763)['case_id'])
 def test_historical_physic_not_medical_advice(self):
  self.assertIn('hot',body(1764));self.assertIn('moist',body(1764))
  self.assertFalse(record(1764)['clinical_efficacy_verified'])
 def test_death_14_august_is_author_report(self):
  self.assertIn('fourteenth of august',body(1765))
  self.assertFalse(P['outcome_independently_verified'])
 def test_duration_is_separate_inference(self):
  self.assertIn('fixed',body(1766));self.assertIn('fixed',body(1767))
  self.assertIn('antiscion',body(1768))
 def test_report_marks_unverified_medical_and_prediction(self):
  text=(B/'AUDIT_REPORT.md').read_text().lower()
  self.assertIn('no independently authenticated patient record',text)
  self.assertIn('source-only',text)
if __name__=='__main__':unittest.main()
