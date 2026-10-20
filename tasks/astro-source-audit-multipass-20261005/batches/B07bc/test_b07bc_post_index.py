"""Post-admission regression: CLXXX is historical-only, append-only, never a prediction."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-source-audit-multipass-20261005'
INDEX=T/'LILLY_SOURCE_EXTRACTION_INDEX_V1.json';CHINA=ROOT/'tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class CLXXXPostIndex(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.old=read(B/'recovery/LILLY_INDEX_BEFORE_B07bc.json');c.new=read(INDEX);c.source=read(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json');c.rules=read(B/'RULES.json');c.accept=read(B/'ACCEPTANCE.json');c.canonical=read(B/'CANONICAL_PREPARE_RECEIPT_20261020.json');c.release=read(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json')
 def test_01_append_exact_records(self):
  self.assertEqual(self.old['records_count'],13017);self.assertEqual(self.new['records_count'],13044)
  self.assertEqual(sum(x['records_count'] for x in self.new['batches']),13044)
 def test_02_all_prior_batches_bytewise_equal_in_memory(self):
  self.assertEqual(self.new['batches'][:-1],self.old['batches'])
  self.assertEqual(self.new['batches'][-1]['id'],'B07bc')
  self.assertEqual(self.new['batches'][-1]['sha256'],sha(B/'RULES.json'))
 def test_03_old_index_frozen_exact_hash(self):
  self.assertEqual(sha(B/'recovery/LILLY_INDEX_BEFORE_B07bc.json'),self.canonical['old_index_sha256'])
 def test_04_original_source_root_unchanged(self):
  self.assertEqual(self.old['source_sha256'],self.new['source_sha256'])
  self.assertEqual(self.old['ptolemy_registry'],self.new['ptolemy_registry'])
 def test_05_chinese_v7_bytes_unchanged(self):
  self.assertEqual(sha(CHINA),sha(B/'recovery/CHINESE_V7_BEFORE_B07bc.json'))
  self.assertEqual(read(CHINA)['sum_source_annotations'],355)
 def test_06_physical_CLXXX_number_covered(self):
  self.assertEqual(self.new['read_numbered_chapters'],list(range(1,181)))
  self.assertEqual(self.new['read_headed_units_count'],96)
  self.assertEqual(self.new['partial_numbered_chapters'],[])
  self.assertEqual(self.new['completed_original_source_units_with_uncertainty'][-1]['printed_chapter'],'CLXXX')
 def test_07_original_printed_Marriage_next(self):
  n=self.new['next'];self.assertEqual(n['chapter'],'CLXXXI')
  self.assertEqual(n['pdf_page'],788);self.assertEqual(n['printed_page'],754)
  self.assertFalse(n['extracted']);self.assertEqual(self.canonical['next_R'],'R13045')
 def test_08_new_source_exact_SHA_and_27_notes(self):
  self.assertEqual(sha(B/'ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json'),self.canonical['source_notes_sha256'])
  self.assertEqual(len(self.source['records']),27)
  self.assertEqual([r['id'] for r in self.rules['rules']],[f'R{n}' for n in range(13018,13045)])
 def test_09_portable_archive_44_replays(self):
  self.assertEqual(self.release['independently_extracted_test_replays'],44)
  self.assertTrue(self.release['member_SHA256_and_bytes_verified'])
  self.assertEqual(self.release['archive_sha256'],self.canonical['archive_sha256'])
 def test_10_no_medical_truth_or_social_character_accuracy(self):
  last=self.new['completed_original_source_units_with_uncertainty'][-1]
  self.assertFalse(last['historical_merchant_medical_outcomes_independently_verified'])
  self.assertFalse(last['historical_servant_behavior_independently_verified'])
  self.assertFalse(last['source_expert_diplomatic_collation_complete'])
 def test_11_zero_actual_human_predictions_or_model_promotions(self):
  self.assertEqual(self.new['empirical_validations'],0);self.assertEqual(self.new['runtime_promotions'],0)
  self.assertEqual(self.canonical['independent_human_predictions_validated'],0)
  self.assertEqual(self.canonical['runtime_promotions'],0)
 def test_12_current_state_has_next_and_exact_count(self):
  s=(ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md').read_text()
  self.assertIn('13,044 Lilly',s.split('## Previous accepted historical checkpoint')[0]);self.assertIn('R13045',s.split('## Previous accepted historical checkpoint')[0])
  self.assertTrue((ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bc_SICKNESSE_SERVANTS.md').is_file())
if __name__=='__main__':unittest.main()
