"""Chinese V9 canonical append-only after six original BaZi chapters."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017';NEW=T/'CHINESE_SOURCE_AUDIT_INDEX_V9.json';OLD=T/'CHINESE_SOURCE_AUDIT_INDEX_V8.json';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json';read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class ChineseV9PostIndex(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.old=read(B/'recovery/CHINESE_V8_BEFORE_09.json');c.new=read(NEW);c.receipt=read(B/'CANONICAL_PREPARE_RECEIPT_20261020.json');c.src=read(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json');c.release=read(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json')
 def test_01_immutable_prior_v8_bytes(self):
  self.assertEqual(sha(OLD),sha(B/'recovery/CHINESE_V8_BEFORE_09.json'))
  self.assertEqual(self.receipt['old_Chinese_V8_sha256'],sha(OLD))
 def test_02_prior_v7_v6_persist(self):
  self.assertTrue((T/'CHINESE_SOURCE_AUDIT_INDEX_V7.json').is_file());self.assertTrue((T/'CHINESE_SOURCE_AUDIT_INDEX_V6.json').is_file())
 def test_03_count_exact_56_new_bazi(self):
  self.assertEqual(self.old['sum_source_annotations'],374);self.assertEqual(self.new['sum_source_annotations'],430)
  self.assertEqual(self.new['systems'][0]['accepted_source_annotations'],210);self.assertEqual(self.new['systems'][1]['accepted_source_annotations'],220)
 def test_04_no_ziwei_mutation(self):self.assertEqual(self.new['systems'][1],self.old['systems'][1])
 def test_05_append_batch_history(self):
  self.assertEqual(self.new['accepted_batches'][:-1],self.old['accepted_batches'])
  self.assertEqual(self.new['accepted_batches'][-1]['id'],'ChineseAstro-09')
  self.assertEqual(self.new['accepted_batches'][-1]['added_bazi_source_annotations'],56)
 def test_06_chinese_current_index_exact_sha(self):self.assertEqual(self.receipt['new_Chinese_V9_sha256'],sha(NEW))
 def test_07_new_id_contiguous(self):
  self.assertEqual([r['id'] for r in self.src['record_rows']],[f'BZI-R{n:04d}' for n in range(155,211)])
  self.assertEqual(self.src['next_id'],'BZI-R0211');self.assertEqual(self.new['systems'][0]['next_id'],'BZI-R0211')
 def test_08_prior_ziwei_next_same(self):self.assertEqual(self.new['systems'][1]['next_id'],'ZWD-R0221')
 def test_09_unmodified_Western(self):
  self.assertEqual(sha(WEST),sha(B/'recovery/WESTERN_B07bc_BEFORE_09.json'))
  self.assertEqual(read(WEST)['records_count'],13044)
 def test_10_source_SHA_and_witness_manifest(self):
  self.assertEqual(sha(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json'),self.receipt['manifest_sha256'])
  self.assertEqual(sha(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json'),self.receipt['witness_sha256'])
  self.assertEqual(sha(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json'),self.receipt['notes_sha256'])
 def test_11_replayed_75_original_tests_after_portable_archive(self):
  self.assertEqual(self.release['independent_original_quote_tests_replayed'],75)
  self.assertTrue(self.release['member_SHA256_and_exact_bytes_passed'])
  self.assertEqual(self.release['archive_sha256'],self.receipt['archive_sha256'])
 def test_12_source_accuracy_claim_not_tested(self):
  self.assertFalse(self.receipt['claimed_nine_in_ten_source_statement_validated'])
  self.assertFalse(self.src['claimed_nine_in_ten_historical_predictions_checked'])
 def test_13_no_natal_calendar_parity_or_human_validation(self):
  self.assertFalse(self.new['chinese_bazi_solar_term_engine_verified'])
  self.assertFalse(self.new['ziwei_complete_natal_calendar_engine_verified'])
  self.assertEqual(self.new['independently_validated_real_human_claims'],0)
  self.assertEqual(self.new['runtime_promotions'],0)
 def test_14_state_and_next_consistency(self):
  s=(ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md').read_text().split('## Previously accepted source checkpoints retained')[0]
  self.assertIn('210 BaZi + 220 Zi Wei = 430',s)
  self.assertIn('BZI-R0211',s)
  self.assertTrue((ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_09.md').is_file())
if __name__=='__main__':unittest.main()
