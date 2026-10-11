"""Independent source-review regressions. Textual conditions, NOT clinical or model validity."""
import unittest
from test_lilly_aphorisms import by,read
def clause(n):return by(n)['source_statement']+' '+' '.join(by(n)['prerequisites'])+' '+' '.join(by(n)['exceptions_and_modifiers'])
class OpusReviewRegression(unittest.TestCase):
 def test_physician_saturn_hour_patient_is_subject(self):
  self.assertIn('his Patient shall either be long sick',clause(5))
  self.assertIn('may continue patient or shift to physician',clause(5))
 def test_aphorism4_30_fixed_source_disagreement(self):
  self.assertIn('moveable signs',clause(4).lower())
  self.assertIn('quick',clause(4).lower())
  self.assertIn('moveable signs',clause(30).lower())
  self.assertIn('vary',clause(30).lower())
  self.assertIn('Aphorism30',clause(4))
 def test_aphorism13_printed_parallel_negative(self):
  self.assertIn('destroyeth not',clause(13))
  self.assertIn('profit',clause(13))
  self.assertIn('stated categorically',by(13)['source_statement'])
 def test_aphorism18_physician_modal_and_exact_house_list(self):
  self.assertIn('may justly feare',clause(18))
  self.assertNotIn('prescribed',by(18)['source_statement'])
  self.assertIn('eighth seventh',clause(18))
 def test_aphorism33_material_erratum_local_trigger(self):
  s=clause(33).lower()
  for p in ('therein','thither','at both','in that place'):self.assertIn(p,s)
  self.assertEqual(by(33)['witness_variants']['1647_body'],'and both times there happens to be an Infortune')
  self.assertIn('therein',by(33)['witness_variants']['errata_corrected_reading'])
 def test_aphorism43_illness_onset_and_mars_modifiers(self):
  s=clause(43).lower()
  self.assertIn('beware in the beginning',s)
  self.assertIn('joint necessity versus individually aggravating',s)
  self.assertTrue(by(43)['original_source_wording_uncertain'])
 def test_urine_with_and_without_consent_overlap_not_erased(self):
  self.assertIn('whether the querent came with consent or not',clause(8))
  self.assertIn('If \'no Urine or consent\' in #9 means either is absent',clause(9))
  self.assertIn('if it means neither',clause(9))
  self.assertTrue(by(9)['original_source_wording_uncertain'])
 def test_ambiguous_luminaries_at_12_not_false_both(self):
  self.assertIn('both versus either',clause(12).lower())
  self.assertTrue(by(12)['original_source_wording_uncertain'])
 def test_aphorism20_and23_ambiguities_remain(self):
  for n in (20,23,34):self.assertTrue(by(n)['original_source_wording_uncertain'])
  self.assertIn('unresolved',clause(23).lower())
 def test_four_errata_citations_have_appropriate_status(self):
  e=read('ERRATA_COLLATION.json')['entries']
  self.assertEqual(len(e),4)
  self.assertEqual({x['aphorism'] for x in e},{23,30,31,33})
  for x in e:self.assertEqual(x['applied_to_normalized_record'],x['aphorism'] in (30,31,33))
  self.assertIn('ERRATUM_THEREIN',e[-1]['status'])
 def test_index_and_record_uncertainty_agree(self):
  index=read('APHORISM_INDEX.json')['entries']
  for v in index:
   self.assertEqual(v['textual_uncertainty'],by(v['number'])['original_source_wording_uncertain'])
 def test_evidence_layers_never_promote_as_applied_rules(self):
  for n in (8,9,33,40):
   r=by(n)
   self.assertFalse(r['evidence_assurance']['medical_efficacy'])
   self.assertFalse(r['evidence_assurance']['empirical_prediction_validation'])
   self.assertNotIn('qualifier_layers',r)
   self.assertIn('source_vs_editorial_disposition',r)
if __name__=='__main__':unittest.main()
