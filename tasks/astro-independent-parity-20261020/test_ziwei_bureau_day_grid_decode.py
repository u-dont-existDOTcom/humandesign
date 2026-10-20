"""Audits original five Zi Wei bureau grid day labels; do not repair gaps."""
import hashlib,json,unittest
from pathlib import Path
from ziwei_bureau_day_grid_decode import (decode_digit,split_row,build_result,SOURCE,ORIGINAL,SOURCE_SHA)
HERE=Path(__file__).resolve().parent

class FiveZiWeiBureauGridLiteralWittnesses(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.saved=json.loads((HERE/'ZIWEI_FIVE_BUREAU_LITERAL_GRID_DECODING_20261020.json').read_text())
  cls.grids={r['original_source_bureau']:r for r in cls.saved['source_original_diagrams_decoded_with_explicit_anomalies']}
  cls.original=json.loads(SOURCE.read_text(encoding='utf-8'))
 def test_01_exact_early_original_transmitted_raw_SHA(self):
  self.assertEqual(hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),SOURCE_SHA)
  self.assertEqual(self.original['whole_raw_original_SHA256'],SOURCE_SHA)
 def test_02_five_original_source_diagrams_unchanged(self):
  self.assertEqual(self.saved['total_source_diagrams'],5)
  self.assertEqual(set(self.grids),{'水二局','木三局','金四局','土五局','火六局'})
  for d in self.original['diagram_reversible_witnesses']:
   text=d['diagram_content'];r=self.grids[d['bureau']]
   self.assertEqual(r['original_grid_utf8_SHA256'],hashlib.sha256(text.encode()).hexdigest())
   self.assertEqual(ORIGINAL.read_text()[d['original_codepoint_start']:d['original_codepoint_end']],text)
 def test_03_exact_vertical_source_glyph_decoding(self):
  self.assertEqual(decode_digit('初','一'),1)
  self.assertEqual(decode_digit('十','一'),11)
  self.assertEqual(decode_digit('廿','三'),23)
  self.assertEqual(decode_digit('三','十'),30)
  self.assertEqual(decode_digit('二','十'),20)
  self.assertEqual(decode_digit('初','十'),10)
  self.assertEqual(decode_digit('十','十'),20)
  self.assertEqual(decode_digit('廿','十'),30)
 def test_04_bad_and_future_compound_glyphs_rejected(self):
  for a,b in [('初','〇'),('卅','一'),('三','一'),('二','二'),('廿','〇')]:
   with self.assertRaises(ValueError):decode_digit(a,b)
 def test_05_grid_cell_delimiters_required(self):
  with self.assertRaisesRegex(ValueError,'boundary'):split_row('初|四|')
  self.assertEqual(split_row('| 初初  |  廿    |'),['初初','廿'])
 def test_06_three_unambiguous_transmitted_source_day_maps(self):
  for bureau in ('水二局','土五局','火六局'):
   r=self.grids[bureau]
   self.assertEqual(r['transmitted_original_label_count'],30)
   self.assertEqual(len(r['day_to_palace_only_when_single_original_label']),30)
   self.assertEqual(r['missing_days_1_to_30'],[])
   self.assertEqual(r['duplicate_original_day_assignments'],{})
   self.assertTrue(r['can_assert_complete_day_placement_from_this_source_only'])
 def test_07_wood_three_original_duplicate_day9(self):
  w=self.grids['木三局']
  self.assertEqual(w['transmitted_original_label_count'],30)
  self.assertEqual(w['duplicate_original_day_assignments'],{'9':['Chen','Yin']})
  self.assertEqual(w['missing_days_1_to_30'],[5])
  self.assertNotIn('9',w['day_to_palace_only_when_single_original_label'])
  self.assertNotIn('5',w['day_to_palace_only_when_single_original_label'])
  self.assertFalse(w['can_assert_complete_day_placement_from_this_source_only'])
 def test_08_wood_three_duplicate_matches_original_raw_cells(self):
  w=self.grids['木三局']
  chen=next(x for x in w['raw_cell_labels_reversible'] if x['palace']=='Chen')
  yin=next(x for x in w['raw_cell_labels_reversible'] if x['palace']=='Yin')
  self.assertEqual((chen['prefix_row'],chen['unit_row']),('初初十','一九一'))
  self.assertEqual((yin['prefix_row'],yin['unit_row']),('初初','三九'))
  self.assertEqual([q['palace_earthly_branch'] for q in w['literal_decoded_day_glyphs'] if q['day']==9],['Chen','Yin'])
 def test_09_metal_four_source_day30_missing(self):
  g=self.grids['金四局']
  self.assertEqual(g['transmitted_original_label_count'],29)
  self.assertEqual(g['missing_days_1_to_30'],[30])
  self.assertEqual(g['duplicate_original_day_assignments'],{})
  self.assertNotIn('30',g['day_to_palace_only_when_single_original_label'])
  self.assertFalse(g['can_assert_complete_day_placement_from_this_source_only'])
 def test_10_metal_other_29_exact_unique_days_preserved(self):
  g=self.grids['金四局']
  self.assertEqual(set(map(int,g['day_to_palace_only_when_single_original_label'])),set(range(1,30)))
  self.assertEqual(len(g['literal_decoded_day_glyphs']),29)
 def test_11_exact_source_incomplete_summary_not_hidden(self):
  self.assertEqual(self.saved['total_missing_day_labels'],2)
  self.assertEqual(self.saved['total_duplicate_day_labels'],1)
  self.assertFalse(self.saved['all_five_grid_day_maps_unique_and_complete'])
 def test_12_exact_report_reproducible(self):self.assertEqual(self.saved,build_result())
 def test_13_not_diplomatic_ancient_source_or_complete_birthchart(self):
  self.assertFalse(self.saved['source_author_original_printing_authenticated'])
  self.assertFalse(self.saved['source_to_birth_calendar_engine_parity_verified'])
  self.assertFalse(self.saved['astronomical_birthhour_month_bureau_mapping_verified'])
 def test_14_source_table_day30_possible_but_not_guaranteed_month(self):
  self.assertEqual(self.grids['水二局']['day_to_palace_only_when_single_original_label']['30'],'Chen')
  self.assertNotIn('30',self.grids['金四局']['day_to_palace_only_when_single_original_label'])
 def test_15_no_real_human_outcomes_or_runtime_promotions(self):
  self.assertEqual(self.saved['empirical_real_person_prediction_validation'],0)
  self.assertEqual(self.saved['runtime_astrology_model_promotions'],0)
if __name__=='__main__':unittest.main()
