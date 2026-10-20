"""Chinese V8 append-only and older original evidence immutability, no predictions."""
import hashlib,json,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017'
NEW=T/'CHINESE_SOURCE_AUDIT_INDEX_V8.json';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
class ChineseV8AppendOnly(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.old=read(B/'recovery/CHINESE_V7_BEFORE_08.json');c.new=read(NEW);c.receipt=read(B/'CANONICAL_PREPARE_RECEIPT_20261020.json');c.source=read(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json');c.release=read(B/'SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json')
 def test_01_old_index_unchanged_SHA(self):self.assertEqual(sha(B/'recovery/CHINESE_V7_BEFORE_08.json'),self.receipt['V7_index_exact_sha256'])
 def test_02_count_exact(self):
  self.assertEqual(self.old['sum_source_annotations'],355);self.assertEqual(self.new['sum_source_annotations'],374)
  self.assertEqual(self.new['systems'][1]['accepted_source_annotations'],220)
  self.assertEqual(self.new['systems'][0]['accepted_source_annotations'],154)
 def test_03_accepted_batches_append_only(self):
  self.assertEqual(self.new['accepted_batches'][:-1],self.old['accepted_batches'])
  self.assertEqual(self.new['accepted_batches'][-1]['id'],'ChineseAstro-08')
  self.assertEqual(self.new['accepted_batches'][-1]['added_ziwei_source_annotations'],19)
 def test_04_all_BaZi_unchanged(self):self.assertEqual(self.new['systems'][0],self.old['systems'][0])
 def test_05_index_source_hash(self):self.assertEqual(sha(NEW),self.receipt['V8_index_exact_sha256'])
 def test_06_last_ZiWei_and_BaZi_next(self):
  self.assertEqual(self.new['systems'][1]['next_id'],'ZWD-R0221');self.assertEqual(self.new['systems'][0]['next_id'],'BZI-R0155')
 def test_07_exact_pinned_source_metadata(self):
  self.assertEqual(self.new['prior_index_sha256'],sha(B/'recovery/CHINESE_V7_BEFORE_08.json'))
  self.assertEqual(self.new['accepted_batches'][-1]['source_original_full_oldid'],1963110)
 def test_08_source_witness_sha_preserved(self):
  self.assertEqual(self.receipt['source_witness_sha256'],sha(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json'))
  self.assertEqual(self.new['accepted_batches'][-1]['rules_sha256'],sha(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json'))
 def test_09_original_19_note_ids(self):
  self.assertEqual([r['id'] for r in self.source['record_rows']],[f'ZWD-R{n:04d}' for n in range(202,221)])
 def test_10_original_Western_B07bc_exact_bytes_unchanged(self):
  self.assertEqual(sha(WEST),sha(B/'recovery/WESTERN_B07bc_BEFORE_08.json'))
  self.assertEqual(read(WEST)['records_count'],13044)
 def test_11_38_portable_archive_tests_verified(self):
  self.assertEqual(self.release['independent_extraction_test_replay'],38)
  self.assertTrue(self.release['members_SHA256_and_exact_bytes_verified'])
  self.assertEqual(self.release['archive_sha256'],self.receipt['portable_archive_sha256'])
 def test_12_no_independent_human_predictions(self):
  self.assertEqual(self.new['independently_validated_real_human_claims'],0)
  self.assertEqual(self.new['runtime_promotions'],0)
 def test_13_no_calendar_or_star_engine_promoted(self):
  self.assertFalse(self.new['ziwei_complete_natal_calendar_engine_verified'])
  self.assertFalse(self.new['chinese_bazi_solar_term_engine_verified'])
 def test_14_state_has_same_count_and_next(self):
  cur=(ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md').read_text().split('## Previous accepted historical checkpoint')[0]
  self.assertIn('154 BaZi + 220 Zi Wei = 374',cur)
  self.assertIn('ZWD-R0221',cur)
  self.assertTrue((ROOT/'state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261020_08.md').is_file())
if __name__=='__main__':unittest.main()
