"""Exact 2017 pinned Chinese verse/commentary witnesses; prediction accuracy intentionally unknown."""
import hashlib,json,re,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json';OLD=T/'CHINESE_SOURCE_AUDIT_INDEX_V8.json';read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sha_bytes=lambda b:hashlib.sha256(b).hexdigest()
class DTS13to18Source(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.src=read(B/'BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json');c.w=read(B/'PINNED_DI_TIAN_SUI_13_18_56_ANCHOR_WITNESS_V1.json');c.manifest=read(B/'PINNED_DI_TIAN_SUI_13_18_MANIFEST_V1.json');c.previous=read(OLD);c.scope=read(B/'TASK_SCOPE.json');c.west=read(WEST);c.rows=c.src['record_rows']
 def test_01_original_all_six_chapters_present(self):
  self.assertEqual(set(self.manifest),{'13','14','15','16','17','18'})
  self.assertEqual(set(self.src['source_chapters']),set(self.manifest))
 def test_02_every_source_bytes_SHA_exact(self):
  for sec,meta in self.manifest.items():
   p=B/meta['raw_local_relative'];self.assertTrue(p.is_file());self.assertEqual(p.stat().st_size,meta['exact_utf8_bytes']);self.assertEqual(sha(p),meta['exact_sha256']);self.assertTrue(p.read_text().startswith('{{Novel|滴天髓|'))
 def test_03_canonical_unmodified_chinese_V8_source(self):
  self.assertEqual(sha(OLD),self.scope['Chinese_V8_exact_SHA256'])
  self.assertEqual(self.previous['sum_source_annotations'],374)
  self.assertEqual(self.previous['systems'][0]['next_id'],'BZI-R0155')
  self.assertEqual(self.previous['systems'][1]['next_id'],'ZWD-R0221')
 def test_04_no_overlap_accepted_batch_06(self):
  x=read(T/'batches/ChineseAstro-06/BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json')
  self.assertEqual(x['last_id'],'BZI-R0154');self.assertEqual(x['next_id'],'BZI-R0155')
  self.assertEqual(set(self.manifest).intersection({'04','05','07','08','11','12'}),set())
 def test_05_current_Western_B07bc_retained(self):
  self.assertEqual(self.west['records_count'],13044);self.assertEqual(self.west['batches'][-1]['id'],'B07bc')
  self.assertEqual(sha(WEST),self.scope['Western_B07bc_exact_SHA256'])
 def test_06_verse_plus_commentary_separation(self):
  self.assertEqual(self.src['source_verses'],7);self.assertEqual(self.src['source_commentary_anchor_count'],49)
  self.assertEqual(sum(x['source_layer']=='original_verse' for x in self.rows),7)
  self.assertEqual(sum(x['source_layer']=='transmitted_commentary' for x in self.rows),49)
 def test_07_unbroken_contiguous_ID_sequence(self):
  self.assertEqual(len(self.rows),56);self.assertEqual([r['id'] for r in self.rows],[f'BZI-R{n:04d}' for n in range(155,211)])
  self.assertEqual(self.src['next_id'],'BZI-R0211')
 def test_08_every_quote_exact_orig_word_preserved(self):
  for row in self.rows:
   meta=self.manifest[row['source_chapter'].split('/')[-1]];p=B/meta['raw_local_relative'];text=p.read_text(encoding='utf-8');data=p.read_bytes();q=row['original_chinese_exact_quote'];co=row['original_chinese_character_offset'];bo=row['original_chinese_byte_offset']
   self.assertEqual(text[co:co+len(q)],q);self.assertEqual(len(text[:co].encode()),bo)
   self.assertEqual(data[bo:bo+row['original_chinese_quote_utf8_bytes']],q.encode())
   self.assertEqual(sha_bytes(q.encode()),row['original_chinese_quote_sha256'])
 def test_09_every_original_quote_unique_per_section(self):
  for row in self.rows:
   meta=self.manifest[row['source_chapter'].split('/')[-1]]
   self.assertEqual((B/meta['raw_local_relative']).read_text().count(row['original_chinese_exact_quote']),1)
 def test_10_verse_in_red_markup_not_commentary(self):
  for row in self.rows:
   if row['source_layer']!='original_verse':continue
   m=self.manifest[row['source_chapter'].split('/')[-1]];text=(B/m['raw_local_relative']).read_text()
   self.assertIn('{{color|red|{{+|'+row['original_chinese_exact_quote']+'}}}}',text)
 def test_11_old_ambiguous_odd_glyphs_preserved(self):
  self.assertTrue(any('陰逄午月' in r['original_chinese_exact_quote'] for r in self.rows))
  self.assertTrue(any('東酉南北' in r['original_chinese_exact_quote'] for r in self.rows))
 def test_12_17_Lichun_source_conventions_not_validated_calendar(self):
  rows=[r for r in self.rows if r['source_chapter_section_number']==17]
  self.assertTrue(any('立春後七日前' in r['original_chinese_exact_quote'] for r in rows))
  self.assertTrue(any('八日後十四日前' in r['original_chinese_exact_quote'] for r in rows))
  self.assertTrue(any('十五日後' in r['original_chinese_exact_quote'] for r in rows))
  self.assertTrue(all(not r['old_calendar_or_hidden_stem_time_engine_verified'] for r in rows))
 def test_13_18_subhour_source_fractions_not_calibrated(self):
  rows=[r for r in self.rows if r['source_chapter_section_number']==18]
  self.assertTrue(any('前三刻三分' in r['original_chinese_exact_quote'] for r in rows))
  self.assertTrue(any('後四刻七分' in r['original_chinese_exact_quote'] for r in rows))
  self.assertFalse(self.src['subhour_and_solar_term_old_calendar_engine_independently_validated'])
 def test_14_text_only_nine_in_ten_not_empirical(self):
  rows=[r for r in self.rows if r['source_nine_in_ten_accuracy_claim_without_data']]
  self.assertEqual(len(rows),1);self.assertEqual(rows[0]['original_chinese_exact_quote'],'十有九驗')
  self.assertFalse(self.src['claimed_nine_in_ten_historical_predictions_checked'])
 def test_15_source_sexist_metaphor_not_endorsed(self):
  self.assertTrue(any(x['historical_moral_or_gender_stereotype_not_endorsed'] and '淫賤' in x['original_chinese_exact_quote'] for x in self.rows))
  self.assertTrue(all(not x['real_human_claim_or_prediction_independently_validated'] for x in self.rows))
 def test_16_no_original_early_edition_auth(self):
  self.assertFalse(self.src['early_edition_text_authorship_authenticated']);self.assertFalse(self.src['classical_chinese_expert_commentary_attribution_verified'])
  self.assertTrue(all(not x['original_early_print_authorship_expert_authenticated'] for x in self.rows))
 def test_17_nonexpert_english_gloss_separate(self):
  self.assertTrue(all('NOT' in 'researcher_nonexpert_gloss_NOT_original_translation' and len(x['researcher_nonexpert_gloss_NOT_original_translation'])>15 for x in self.rows))
 def test_18_provenance_receipts_bijective(self):
  self.assertEqual(self.w['quote_count'],56);self.assertEqual(len(self.w['quote_receipts']),56)
  for row,rec in zip(self.rows,self.w['quote_receipts']):
   self.assertEqual(rec['id'],row['id']);self.assertEqual(rec['quote_byte_offset'],row['original_chinese_byte_offset']);self.assertEqual(rec['source_quote_sha256'],row['original_chinese_quote_sha256'])
 def test_19_human_validations_zero(self):
  self.assertEqual(self.src['actual_independent_human_predictions_validated'],0)
  self.assertEqual(self.src['runtime_astrology_promotions'],0)
  self.assertTrue(all(not x['model_runtime_promoted'] for x in self.rows))

def check_row(i):
 def test(self):
  r=self.rows[i];self.assertEqual(r['id'],f'BZI-R{155+i:04d}');self.assertIn(r['source_chapter_section_number'],(13,14,15,16,17,18));self.assertTrue(r['original_chinese_quote_sha256']);self.assertFalse(r['model_runtime_promoted'])
 return test
for i in range(56):setattr(DTS13to18Source,f'test_note_{i+1:02d}',check_row(i))
if __name__=='__main__':unittest.main()
