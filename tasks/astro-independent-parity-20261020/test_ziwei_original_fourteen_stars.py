"""14 source-conditional Zi Wei stars from original mnemonic; no people/early print."""
from __future__ import annotations
import json,hashlib,unittest
from pathlib import Path
from ziwei_original_fourteen_stars import (
    SOURCE_SHA,SOURCE,VERSE,BRANCHES,ZGROUP,FGROUP,
    source_provenance, move, fourteen_star_palaces_given_ziwei,
    fourteen_source_candidate_given_year_life_day,twelve_anchor_configurations
)
HERE=Path(__file__).resolve().parent

class FourteenSourceOnlyStarMechanics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved=json.loads((HERE/'ZIWEI_14_STARS_12_ANCHORS_SOURCE_CONDITIONAL_20261020.json').read_text())
    def test_01_exact_original_source_verses_unique(self):
        raw=SOURCE.read_bytes();s=raw.decode('utf-8')
        self.assertEqual(hashlib.sha256(raw).hexdigest(),SOURCE_SHA)
        self.assertEqual(s.count(VERSE),1)
        self.assertEqual(len(ZGROUP),6)
        self.assertEqual(len(FGROUP),8)
    def test_02_exact_original_verse_byte_SHA_locator(self):
        w=source_provenance();q=w['original_14_star_verse_exact']
        self.assertEqual(q,VERSE)
        self.assertEqual(hashlib.sha256(q.encode()).hexdigest(),w['original_14_star_verse_sha256'])
        self.assertEqual(SOURCE.read_text()[w['verse_start_original_codepoint_offset']:][:len(VERSE)],VERSE)
    def test_03_explicit_14_distinct_principal_star_names(self):
        x=fourteen_star_palaces_given_ziwei('Yin')['all_fourteen_primary_stars_conditional_on_source_palaces']
        self.assertEqual(len(x),14)
        self.assertEqual(set(x),{'ZiWei','TianJi','TaiYang','WuQu','TianTong','LianZhen',
          'TianFu','TaiYin','TanLang','JuMen','TianXiang','TianLiang','QiSha','PoJun'})
    def test_04_all_twelve_possible_ziwei_anchors(self):
        self.assertEqual([x['ziwei_base_branch'] for x in self.saved['all_12_anchor_configurations']],list(BRANCHES))
        self.assertEqual(len(self.saved['all_12_anchor_configurations']),12)
    def test_05_northern_source_ZiWei_series_reverse_and_gaps(self):
        for anchor in BRANCHES:
            x=fourteen_star_palaces_given_ziwei(anchor)['counterclockwise_six_ziwei_group']
            self.assertEqual([x[n] for n in ('ZiWei','TianJi','TaiYang','WuQu','TianTong','LianZhen')],
              [move(anchor,0),move(anchor,-1),move(anchor,-3),move(anchor,-4),move(anchor,-5),move(anchor,-8)])
            # Final 'three empty' instruction closes northern cycle.
            self.assertEqual(move(x['LianZhen'],-4),anchor)
    def test_06_southern_TianFu_series_forward_and_three_gaps(self):
        for anchor in BRANCHES:
            r=fourteen_star_palaces_given_ziwei(anchor)
            j=r['tianfu_base_branch'];x=r['clockwise_eight_tianfu_group']
            self.assertEqual([x[n] for n in ('TianFu','TaiYin','TanLang','JuMen','TianXiang','TianLiang','QiSha','PoJun')],
              [move(j,i) for i in (0,1,2,3,4,5,6,10)])
            self.assertEqual(move(x['QiSha'],4),x['PoJun'])
    def test_07_TianFu_fixed_points_only_Yin_Shen(self):
        x={r['ziwei_base_branch'] for r in self.saved['all_12_anchor_configurations'] if r['ziwei_base_branch']==r['tianfu_base_branch']}
        self.assertEqual(x,{'Yin','Shen'})
    def test_08_sha_po_lang_triplicity_in_each_star_ring(self):
        for a in BRANCHES:
            z=fourteen_star_palaces_given_ziwei(a)['all_fourteen_primary_stars_conditional_on_source_palaces']
            self.assertEqual(move(z['TanLang'],4),z['QiSha'])
            self.assertEqual(move(z['QiSha'],4),z['PoJun'])
            self.assertEqual(move(z['PoJun'],4),z['TanLang'])
    def test_09_source_witness_known_authorial_Jia_Yin_Fire_first_day(self):
        x=fourteen_source_candidate_given_year_life_day('Jia','Yin',1)
        self.assertEqual(x['source_bureau']['effective_bureau_candidate_under_requested_source_policy'],'火六局')
        self.assertEqual(x['conditional_fourteen_stars']['ziwei_base_branch'],'You')
        self.assertEqual(x['conditional_fourteen_stars']['tianfu_base_branch'],'Wei')
        self.assertEqual(x['result_status'],'FOURTEEN_SOURCE_CONDITIONAL_STAR_PALACES_CALCULATED_NOT_NATAL_VALIDATED')
    def test_10_source_You_anchor_major_stars_deterministic(self):
        x=fourteen_star_palaces_given_ziwei('You')['all_fourteen_primary_stars_conditional_on_source_palaces']
        self.assertEqual(x['ZiWei'],'You')
        self.assertEqual(x['TianJi'],'Shen')
        self.assertEqual(x['TaiYang'],'Wu')
        self.assertEqual(x['WuQu'],'Si')
        self.assertEqual(x['TianTong'],'Chen')
        self.assertEqual(x['LianZhen'],'Chou')
        self.assertEqual(x['TianFu'],'Wei')
        self.assertEqual(x['TaiYin'],'Shen')
        self.assertEqual(x['TanLang'],'You')
        self.assertEqual(x['JuMen'],'Xu')
        self.assertEqual(x['TianXiang'],'Hai')
        self.assertEqual(x['TianLiang'],'Zi')
        self.assertEqual(x['QiSha'],'Chou')
        self.assertEqual(x['PoJun'],'Si')
    def test_11_bad_original_source_birth_star_palace_rejected(self):
        for s in ('',None,'紫微','Pisang'):
            with self.assertRaises(ValueError):fourteen_star_palaces_given_ziwei(s)
    def test_12_source_original_na_yin_contradiction_strict_must_not_fill(self):
        x=fourteen_source_candidate_given_year_life_day('Jia','Xu',1)
        self.assertEqual(x['result_status'],'UNRESOLVED_SOURCE_NAYIN_GLYPH_CONFLICT')
        self.assertIsNone(x['conditional_fourteen_stars'])
    def test_13_source_modern_reprint_optional_not_default(self):
        x=fourteen_source_candidate_given_year_life_day('Jia','Xu',1,source_edition_policy='explicit_later_edited_print_candidate')
        self.assertTrue(x['source_bureau']['correction_applied_from_secondary'])
        self.assertIsNotNone(x['conditional_fourteen_stars'])
        self.assertFalse(x['full_historical_birth_chart_parity_verified'])
    def test_14_wood_three_day9_duplicate_fails_to_give_stars(self):
        # Jia year + Xu can become Fire (not Wood); Bing/Hai is the suspect Wood row.
        x=fourteen_source_candidate_given_year_life_day('Bing','Hai',9,source_edition_policy='explicit_later_edited_print_candidate')
        self.assertEqual(x['source_bureau']['effective_bureau_candidate_under_requested_source_policy'],'木三局')
        self.assertEqual(x['result_status'],'UNRESOLVED_ORIGINAL_BUREAU_DAY_TABLE_DUPLICATE_OR_MISSING')
        self.assertIsNone(x['conditional_fourteen_stars'])
    def test_15_metal_four_day30_original_missing(self):
        # Find a yearstem/Life cell that produces Metal strictly from the song.
        from ziwei_nayin_bureau_source import STEMS_ROMAN,BRANCHES_ROMAN,conditional_source_bureau
        candidates=[(y,b) for y in STEMS_ROMAN for b in BRANCHES_ROMAN
             if conditional_source_bureau(y,b).source_conditional_bureau_Chinese=='金四局']
        self.assertGreater(len(candidates),0)
        x=fourteen_source_candidate_given_year_life_day(*candidates[0],30)
        self.assertEqual(x['result_status'],'UNRESOLVED_ORIGINAL_BUREAU_DAY_TABLE_DUPLICATE_OR_MISSING')
        self.assertIsNone(x['conditional_fourteen_stars'])
    def test_16_source_14_star_is_not_full_birth_calendar_engine(self):
        self.assertFalse(self.saved['full_actual_birth_natal_chart_calculation_independently_verified'])
        self.assertFalse(self.saved['birth_year_timezone_lunar_leap_month_and_true_solar_time_parity_verified'])
        self.assertFalse(self.saved['original_source_witness']['source_ancient_Ming_physical_edition_verified'])
    def test_17_replay_saved_all_twelve_anchors(self):
        self.assertEqual(self.saved,json.loads(json.dumps(twelve_anchor_configurations(),ensure_ascii=False)))
    def test_18_zero_actual_person_outcomes(self):
        self.assertEqual(self.saved['past_or_future_real_human_predictions_validated'],0)
        self.assertEqual(self.saved['runtime_promotions'],0)

if __name__=='__main__':
    unittest.main()
