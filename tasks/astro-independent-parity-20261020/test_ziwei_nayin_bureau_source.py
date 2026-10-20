"""Original NaYin song word-level witness with uncorrected transmitted glyphs."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

from ziwei_nayin_bureau_source import (
    conditional_source_bureau, read_source_poem, source_conditional_120,
    ORIGINAL, ORIGINAL_SHA, EXPECTED_LITERAL_ANOMALIES,
)
from ziwei_original_bureau_candidate import candidate_given_bureau_day
from ziwei_tianfu_relative import tianfu_from_ziwei
HERE = Path(__file__).resolve().parent

class NaYinOriginalSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes=json.loads((HERE/'ZIWEI_ORIGINAL_NAYIN_120_CONDITIONALS_20261020.json').read_text())
        cls.poem=read_source_poem()
        cls.records=cls.notes['conditional_year_stem_plus_life_palace_lookup']
    def test_01_source_immutable_revision(self):
        import hashlib
        self.assertEqual(hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(), ORIGINAL_SHA)
        self.assertIn('纳音甲子歌误要熟读',ORIGINAL.read_text())
    def test_02_30_original_verses_pairs_exact(self):
        self.assertEqual(len(self.poem),30)
        self.assertEqual(self.poem[0]['original_phrase_exact'],'甲子乙丑海中金')
        self.assertEqual(self.poem[1]['original_phrase_exact'],'丙寅丁卯炉中火')
        self.assertEqual(self.poem[-1]['original_phrase_exact'],'壬戌癸亥大海水')
    def test_03_two_printed_label_errors_never_corrected_silently(self):
        bad=[r for r in self.poem if not r['both_original_labels_match_generated_60_cycle']]
        self.assertEqual([(r['poem_pair_ordinal'],r['original_written_stem_branch_pair']) for r in bad],
            [(6,'甲戊乙亥'),(18,'戊戌已亥')])
        self.assertEqual(set(EXPECTED_LITERAL_ANOMALIES),{6,18})
    def test_04_normal_cycle_58_other_pair_labels_are_exact(self):
        self.assertEqual(sum(r['both_original_labels_match_generated_60_cycle'] for r in self.poem),28)
        self.assertEqual(sum(len(r['literal_mismatches_with_60_cycle']) for r in self.poem),2)
    def test_05_original_Jia_Yin_to_Fire_six_bureau(self):
        r=conditional_source_bureau('Jia','Yin')
        self.assertEqual(r.derived_source_palace_sexagenary_name,'丙寅')
        self.assertEqual(r.original_nayin_source_chinese_verse,'丙寅丁卯炉中火')
        self.assertEqual(r.source_conditional_bureau_Chinese,'火六局')
        self.assertTrue(r.original_source_glyph_permitted_for_queried_natal_pillar)
    def test_06_full_authorial_worked_example_Jia_Yin_Fire_day1_You(self):
        r=conditional_source_bureau('Jia','Yin')
        star=candidate_given_bureau_day(r.source_conditional_bureau_Chinese,1)
        self.assertEqual(star.literal_ziwei_branch_if_single_source_label,'You')
        self.assertEqual(star.derived_tianfu_branch_if_single_ziwei_label,tianfu_from_ziwei('You'))
    def test_07_independent_modern_commentary_example_Geng_Chou(self):
        r=conditional_source_bureau('Geng','Chou')
        self.assertEqual(r.derived_source_palace_sexagenary_name,'己丑')
        self.assertEqual(r.source_conditional_bureau_Chinese,'火六局')
        self.assertIn('霹雳火',r.original_nayin_source_chinese_verse)
    def test_08_total_120_conditional_year_life_cells(self):
        self.assertEqual(len(self.records),120)
        self.assertEqual(len({(r['source_input_birth_year_stem'],r['source_input_life_palace_branch']) for r in self.records}),120)
    def test_09_116_valid_not_120(self):
        ok=[r for r in self.records if r['original_source_glyph_permitted_for_queried_natal_pillar']]
        self.assertEqual(len(ok),116)
        self.assertEqual(self.notes['conditional_source_status_counts']['EXACT_TRANSMITTED_NAYIN_SOURCE_LABEL_NOT_BIRTH_CHART_VALIDATION'],116)
    def test_10_no_guess_at_transmitted_甲戊(self):
        for y in ('Jia','Ji'):
            r=conditional_source_bureau(y,'Xu')
            self.assertEqual(r.derived_source_palace_sexagenary_name,'甲戌')
            self.assertEqual(r.glyph_that_prevents_strict_source_acceptance,'甲戊')
            self.assertEqual(r.derived_cycle_name_if_source_were_emended_not_adopted,'甲戌')
            self.assertIsNone(r.source_conditional_bureau_Chinese)
    def test_11_no_guess_at_transmitted_已亥(self):
        for y in ('Bing','Xin'):
            r=conditional_source_bureau(y,'Hai')
            self.assertEqual(r.derived_source_palace_sexagenary_name,'己亥')
            self.assertEqual(r.glyph_that_prevents_strict_source_acceptance,'已亥')
            self.assertIsNone(r.source_conditional_element_Chinese)
            self.assertIsNone(r.source_conditional_bureau_Chinese)
    def test_12_all_four_unresolved_not_excluded_from_report(self):
        missing={(r['source_input_birth_year_stem'],r['source_input_life_palace_branch']) for r in self.records if r['source_conditional_bureau_Chinese'] is None}
        self.assertEqual(missing,{('Jia','Xu'),('Ji','Xu'),('Bing','Hai'),('Xin','Hai')})
    def test_13_names_and_stems_reject_unknown_inputs(self):
        for stem,branch in [('', 'Yin'),('Jia','Dragon'),('甲','Yin'),('Jia','寅'),(None,'Yin')]:
            with self.assertRaises(ValueError):
                conditional_source_bureau(stem,branch)
    def test_14_original_poem_source_byte_glyph_sha_reversibility(self):
        s=ORIGINAL.read_text()
        import hashlib
        for row in self.poem:
            phrase=row['original_phrase_exact'];cp=row['original_phrase_source_character_offset']
            self.assertEqual(s[cp:cp+len(phrase)],phrase)
            self.assertEqual(hashlib.sha256(phrase.encode()).hexdigest(),row['original_phrase_UTF8_SHA256'])
    def test_15_no_independent_ancient_printing_verified(self):
        self.assertFalse(self.notes['independent_early_classical_paper_source_witness'])
        self.assertFalse(self.notes['verified_Gregorian_to_lunar_and_birthyear_convention'])
    def test_16_no_human_validation_or_model_promotion(self):
        self.assertFalse(self.notes['complete_birth_natal_fourteen_stars_and_timing_verified'])
        self.assertEqual(self.notes['real_person_predictions_validated'],0)
        self.assertEqual(self.notes['runtime_promotions'],0)
    def test_17_report_matches_exact_recomputation(self):
        self.assertEqual(self.notes,source_conditional_120())
    def test_18_no_state_omission_or_automatic_source_normalization(self):
        self.assertTrue(self.notes['source_odd_glyphs_not_silently_emended'])
        self.assertEqual(self.notes['conditional_source_status_counts']['UNRESOLVED_ORIGINAL_NAYIN_GLYPH_CONFLICT_NO_BUREAU_ASSIGNED'],4)

if __name__ == '__main__':
    unittest.main()
