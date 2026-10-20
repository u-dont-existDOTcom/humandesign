"""Exact original Chinese Wikitext oldid1963110 provenance; no horoscope or human validation."""
import hashlib,json,re,unittest
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[3];T=ROOT/'tasks/astro-chinese-primary-sources-20261017';WEST=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json';RAW=T/'batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt';PREV=T/'batches/ChineseAstro-07/ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json';OLD=T/'CHINESE_SOURCE_AUDIT_INDEX_V7.json';read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sha_bytes=lambda x:hashlib.sha256(x).hexdigest()
class ChineseV8ExactOriginal(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.rules=read(B/'ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json');c.witness=read(B/'SOURCE_1963110_POSTBUREAU_WITNESS_V1.json');c.prior=read(PREV);c.v7=read(OLD);c.scope=read(B/'TASK_SCOPE.json');c.west=read(WEST);c.raw=RAW.read_text(encoding='utf-8');c.records=c.rules['record_rows']
 def test_01_full_source_SHA_and_bytes(self):
  self.assertEqual(sha(RAW),'1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72');self.assertEqual(RAW.stat().st_size,106736)
  self.assertEqual(self.rules['original_raw_full_SHA256'],sha(RAW))
 def test_02_exact_unmodified_prior_V7(self):
  self.assertEqual(sha(OLD),self.scope['Chinese_V7_sha256']);self.assertEqual(self.v7['sum_source_annotations'],355)
  self.assertEqual(self.v7['systems'][0]['accepted_source_annotations'],154);self.assertEqual(self.v7['systems'][1]['accepted_source_annotations'],201)
  self.assertEqual(self.v7['accepted_batches'][-1]['id'],'ChineseAstro-07')
 def test_03_previous_original_witness_not_overlapping(self):
  self.assertEqual(self.prior['last_id'],'ZWD-R0201');self.assertEqual(self.prior['next_id'],'ZWD-R0202')
  self.assertEqual(self.prior['original_text_segment_absolute_end_codepoint'],12080)
  self.assertEqual(self.rules['original_excerpt_absolute_start_character'],12085)
 def test_04_four_diagrams_in_order(self):
  self.assertEqual(self.rules['diagram_count'],4)
  self.assertEqual([x['source_diagram_role'] for x in self.records[:4]],['TIANFU_REFERENCE_STAR_PALACE_DIAGRAM','TIANSHANG_TIANSHI_YEAR_LIMIT_RISK_DIAGRAM','LU_QUAN_KE_JI_TRANSFORMATIONS_DIAGRAM','TWELVE_BRANCH_SEVEN_GRADE_STAR_CONDITIONS_TABLE'])
 def test_05_original_nowiki_segment_exact_match(self):
  start=self.rules['original_excerpt_absolute_start_character'];end=self.rules['original_excerpt_absolute_end_character_exclusive']
  p=B/'SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt'
  self.assertEqual(self.raw[start:end],p.read_text(encoding='utf-8'));self.assertEqual(sha(p),self.rules['original_excerpt_sha256'])
  self.assertEqual(sha(p),self.witness['original_exact_excerpt_SHA256'])
 def test_06_diagram_excerpt_hashes(self):
  text=(B/'SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt').read_text(encoding='utf-8');part=text.split('<nowiki>',1)[1].split('</nowiki>',1)[0];chunks=re.split(r'\n\s*\n',part);self.assertEqual(len(chunks),4)
  for i,t in enumerate(chunks):
   self.assertEqual(t,self.records[i]['source_original_exact_quote'])
   self.assertEqual(sha_bytes(t.encode()),self.witness['original_four_unparsed_diagram_UTF8_SHA256'][i])
 def test_07_original_byte_offsets_exact_roundtrip(self):
  for r in self.records:
   quote=r['source_original_exact_quote'];co=r['source_original_absolute_character_offset'];byte=r['source_original_absolute_utf8_byte_offset']
   self.assertEqual(self.raw[co:co+len(quote)],quote)
   self.assertEqual(len(self.raw[:co].encode()),byte)
   self.assertEqual(RAW.read_bytes()[byte:byte+r['source_quote_utf8_bytes']],quote.encode())
   self.assertEqual(sha_bytes(quote.encode()),r['source_quote_utf8_sha256'])
 def test_08_original_quotes_are_unique_in_fragment(self):
  seg=(B/'SOURCE_1963110_POSTBUREAU_DIAGRAMS_RAW_EXCERPT.txt').read_text()
  for r in self.records[:-1]:self.assertEqual(seg.count(r['source_original_exact_quote']),1)
 def test_09_19_new_Ids_contiguous(self):
  self.assertEqual(len(self.records),19);self.assertEqual([x['id'] for x in self.records],[f'ZWD-R{i:04d}' for i in range(202,221)])
  self.assertEqual(self.rules['first_id'],'ZWD-R0202');self.assertEqual(self.rules['last_id'],'ZWD-R0220');self.assertEqual(self.rules['next_id'],'ZWD-R0221')
 def test_10_table_has_12_earthly_branches(self):
  self.assertEqual([x['earthly_branch'] for x in self.records if x['source_type']=='source_historical_branch_star_grade_row'],list('子丑寅卯辰巳午未申酉戌亥'))
 def test_11_original_table_7_columns_declared_historical(self):
  self.assertEqual(self.records[5]['source_type'],'source_historical_seven_grade_taxonomy')
  self.assertEqual(self.records[5]['source_original_exact_quote'],'|   |庙       |旺       |得地     |利益     |平和     |不得地   |落陷     |')
  for r in self.records[6:18]:self.assertEqual(len(r['grade_columns']),7)
 def test_12_no_claim_verified_premodern_woodblock(self):
  self.assertFalse(self.rules['early_original_woodblock_edition_authenticated'])
  self.assertTrue(all(not x['original_source_physical_early_edition_authenticated'] for x in self.records))
 def test_13_no_calendar_chart_parity(self):
  self.assertFalse(self.rules['traditional_ziwei_complete_calendar_and_chart_engine_verified'])
  self.assertFalse(self.rules['original_source_star_name_abbreviations_fully_collated'])
  self.assertTrue(all(not x['historic_table_symbol_cell_or_calendar_engine_validated'] for x in self.records))
 def test_14_no_high_stakes_human_predictions(self):
  self.assertEqual(self.rules['independent_real_human_predictions_validated'],0)
  self.assertEqual(self.rules['runtime_promotions'],0)
  self.assertTrue(all(not x['independent_human_forecast_or_outcome_validated'] and not x['runtime_model_promoted'] for x in self.records))
 def test_15_last_record_is_next_section_only(self):
  self.assertEqual(self.records[-1]['source_original_exact_quote'],'===一 命宫===')
  self.assertEqual(self.records[-1]['source_type'],'NEXT_SECTION_BOUNDARY')
 def test_16_prebatch_western_index_still_B07bc(self):
  self.assertEqual(self.west['records_count'],13044)
  self.assertEqual(self.west['batches'][-1]['id'],'B07bc')
  self.assertEqual(self.west['empirical_validations'],0)
 def test_17_quote_witness_IDs_and_offsets(self):
  self.assertEqual(len(self.witness['exact_source_quotes']),19)
  for i,x in enumerate(self.witness['exact_source_quotes']):
   self.assertEqual(x['id'],self.records[i]['id'])
   self.assertEqual(x['source_codepoint_offset'],self.records[i]['source_original_absolute_character_offset'])
   self.assertEqual(x['quote_sha256'],self.records[i]['source_quote_utf8_sha256'])
 def test_18_old_headed_mortality_diagram_not_outcome(self):
  self.assertIn('凡岁限行到此星必死',self.records[1]['source_original_exact_quote'])
  self.assertFalse(self.rules['historic_year_limit_mortality_forecast_validated'])
 def test_19_source_does_not_complete_full_Ziwei_II(self):
  self.assertEqual(self.rules['next_section'],'===一 命宫===')
  self.assertFalse(self.rules['original_source_star_name_abbreviations_fully_collated'])

def verify_note(i):
 def test(self):
  x=self.records[i];self.assertEqual(x['id'],f'ZWD-R{202+i:04d}');self.assertEqual(x['source_original_full_oldid'],1963110);self.assertTrue(x['historical_research_gloss_NOT_quotation'])
  self.assertFalse(x['runtime_model_promoted'])
 return test
for i in range(19):setattr(ChineseV8ExactOriginal,f'test_original_note_{i+1:02d}',verify_note(i))
if __name__=='__main__':unittest.main()
