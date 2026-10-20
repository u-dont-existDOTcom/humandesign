"""Focused, portable document-and-photo tests for original Lilly CLXXX, not predictive success."""
import hashlib
import json
import unittest
from pathlib import Path

B=Path(__file__).resolve().parent; ROOT=B.parents[3]
T=ROOT/'tasks/astro-source-audit-multipass-20261005'
WEST=T/'LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CHINA=ROOT/'tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json'
PREV=T/'batches/B07bb'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))

class OriginalSicknesseServants(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.notes=read(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json')
  c.rules=read(B/'RULES.json');c.accept=read(B/'ACCEPTANCE.json');c.scope=read(B/'TASK_SCOPE.json');c.retrieval=read(B/'SOURCE_IMAGE_1659_754_RETRIEVAL.json')
  c.prior=read(PREV/'ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json');c.west=read(WEST);c.china=read(CHINA)
  c.records=c.notes['records']
 def test_source_1647_full_pdf_sha(self):
  self.assertEqual(self.notes['source_full_original_Wellcome_1647_PDF_sha256'],'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b')
  self.assertEqual(self.notes['source_full_original_Wellcome_1647_PDF_sha256'],self.west['source_sha256'])
 def test_prebatch_exact_accepted_prior(self):
  self.assertEqual(self.west['records_count'],13017)
  self.assertEqual(self.west['batches'][-1]['id'],'B07bb')
  self.assertEqual(self.prior['last_record'],'R13017')
  self.assertEqual(self.west['next']['chapter'],'CLXXX')
  self.assertEqual(self.west['next']['pdf_page'],787)
 def test_chinese_v7_byte_identical(self):
  self.assertEqual(self.china['sum_source_annotations'],355)
  self.assertEqual(sha(CHINA),self.scope['chinese_v7_sha256'])
  self.assertEqual(sha(CHINA),self.accept['Chinese_V7_index_sha256'])
 def test_1647_1659_four_real_page_images(self):
  photos=self.notes['original_photographic_witnesses'];self.assertEqual(set(photos),{'753','754'})
  for folio,pair in photos.items():
   self.assertEqual(set(pair),{'1647','1659'})
   for ed,m in pair.items():
    file=ROOT/m['original_source_repo_relative_file']
    self.assertTrue(file.is_file(),file)
    self.assertEqual(file.stat().st_size,m['bytes'])
    self.assertGreater(m['bytes'],180000)
    self.assertEqual(sha(file),m['sha256'])
    self.assertEqual(m['printed_folio'],int(folio))
    self.assertEqual(m['source_edition'],int(ed))
    self.assertEqual(m['scan_frame'],int(folio)+(34 if ed=='1647' else 29))
 def test_previous_p753_source_image_reuse(self):
  prior=self.prior['two_original_printings_four_page_photo_witnesses']['753'];new=self.notes['original_photographic_witnesses']['753']
  for ed in ('1647','1659'):
   self.assertEqual(prior[ed]['sha256'],new[ed]['sha256'])
   self.assertEqual(new[ed]['reused_from_accepted_batch'],'B07bb')
 def test_p754_1647_preview_image_reuse_not_reextract(self):
  fp=PREV/'evidence/1647_original-788.jpg'
  self.assertEqual(self.notes['original_photographic_witnesses']['754']['1647']['sha256'],sha(fp))
  self.assertEqual(self.notes['original_photographic_witnesses']['754']['1647']['reused_from_accepted_batch'],'B07bb')
 def test_p754_1659_actual_external_scan_frame(self):
  meta=self.notes['original_photographic_witnesses']['754']['1659']
  self.assertEqual(meta['scan_frame'],783)
  self.assertEqual(meta['sha256'],self.retrieval['thumbnail_sha256'])
  self.assertEqual(meta['bytes'],self.retrieval['thumbnail_exact_bytes'])
  self.assertTrue(self.retrieval['original_page_witness_both_editions_inspected'])
  self.assertFalse(self.retrieval['original_djvu_file_sha256_verified'])
 def test_original_chapter_boundaries_not_combined(self):
  self.assertEqual(self.records[0]['role'],'CLXXX_SIXTH_HOUSE_OPEN')
  self.assertEqual(self.records[-1]['role'],'CLXXXI_MARRIAGE_NEXT_BOUNDARY')
  self.assertEqual(self.records[-1]['evidence_layer'],'NEXT_CHAPTER_BOUNDARY')
  self.assertEqual(self.notes['next_chapter'],'CLXXXI')
  self.assertEqual(self.notes['next_first_1647_pdf_frame'],788)
 def test_exact_consecutive_records_no_overlap(self):
  self.assertEqual(len(self.records),27)
  self.assertEqual([x['record_number'] for x in self.records],list(range(13018,13045)))
  self.assertEqual(self.notes['first_R'],'R13018')
  self.assertEqual(self.notes['last_R'],'R13044')
  self.assertEqual(self.notes['next_R'],'R13045')
  self.assertEqual(self.rules['record_count'],27)
 def test_folio_order_and_exact_two_page_span(self):
  self.assertEqual(self.notes['printed_original_folios'],[753,754])
  self.assertEqual(self.notes['original_first_1647_pdf_frames'],[787,788])
  self.assertEqual(self.notes['independently_typeset_original_1659_djvu_frames'],[782,783])
  self.assertEqual([x['original_printed_folio'] for x in self.records],[753]*17+[754]*10)
 def test_source_quotes_and_glosses_explicitly_separated(self):
  for row in self.records:
   self.assertGreaterEqual(len(row['original_1647_short_verbatim_anchor_NOT_full_sentence']),6)
   self.assertGreaterEqual(len(row['historical_gloss_NOT_author_quotation']),20)
   self.assertNotEqual(row['original_1647_short_verbatim_anchor_NOT_full_sentence'],row['historical_gloss_NOT_author_quotation'])
   self.assertFalse(row['original_astrological_glyphs_full_critical_collation_complete'])
 def test_sources_as_historical_not_health_knowledge(self):
  layers={x['evidence_layer'] for x in self.records}
  self.assertIn('UNVERIFIED_HISTORICAL_MEDICAL_CAUSATION',layers)
  self.assertIn('UNVERIFIED_HISTORICAL_MEDICAL_PROGNOSIS',layers)
  self.assertIn('HISTORICAL_PREJUDICIAL_SOCIAL_RULE_NOT_ENDORSED',layers)
  self.assertIn('UNVERIFIED_SERVANT_CHARACTER_PREDICTION',layers)
 def test_health_prejudice_prediction_no_promotion(self):
  self.assertTrue(all(x['previously_known_merchant_case'] for x in self.records))
  self.assertTrue(all(x['medical_diagnosis_treatment_or_social_prejudice_adopted'] is False for x in self.records))
  self.assertTrue(all(x['actual_human_medical_or_servant_observation_independently_verified'] is False for x in self.records))
  self.assertTrue(all(x['independent_actual_person_prediction_result_validated'] is False for x in self.records))
  self.assertTrue(all(x['runtime_model_promoted'] is False for x in self.records))
 def test_source_glosses_not_misused_as_quote(self):
  self.assertTrue(self.notes['source_editable_gloss_separate_from_1647_exact_anchor'])
  self.assertTrue(self.notes['historical_original_symbolic_glyph_collation_not_complete'])
  self.assertTrue(self.notes['full_1659_DjVu_binary_sha256_unverified'])
 def test_no_person_prediction_or_medical_routing(self):
  self.assertEqual(self.notes['actual_human_predictive_validations'],0)
  self.assertEqual(self.notes['runtime_promotions'],0)
  self.assertEqual(self.rules['actual_human_predictive_validations'],0)
  self.assertEqual(self.rules['runtime_model_promotions'],0)
 def test_acceptance_counts_and_sha(self):
  self.assertEqual(self.accept['new_historical_source_only_notes'],27)
  self.assertEqual(self.accept['Lilly_before'],13017)
  self.assertEqual(self.accept['Lilly_after_if_accepted'],13044)
  self.assertEqual(self.accept['Western_after_if_accepted'],14110)
  self.assertEqual(self.accept['Ptolemy_retained'],1066)
  self.assertEqual(self.accept['Chinese_V7_retained'],355)
  self.assertEqual(self.accept['source_notes_sha256'],sha(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json'))
  self.assertEqual(self.accept['rules_sha256'],sha(B/'RULES.json'))
 def test_no_critical_math_or_edition_collation_claim(self):
  self.assertFalse(self.accept['critical_original_astrological_glyph_collation_complete'])
  self.assertFalse(self.accept['clinical_truth_or_independent_merchant_illnesses_verified'])
  self.assertFalse(self.accept['human_servant_observations_validated'])


def individual_record(i):
 def test(self):
  x=self.records[i];self.assertEqual(x['id'],f'R{13018+i}');self.assertEqual(x['record_number'],13018+i)
  self.assertEqual(x,self.rules['rules'][i]);self.assertFalse(x['runtime_model_promoted'])
 return test
for i in range(27):setattr(OriginalSicknesseServants,f'test_original_note_{i+1:02d}',individual_record(i))
if __name__=='__main__':unittest.main()
