"""Original-vs-later-edited NaYin glyphs; editorial correction never automatic."""
from __future__ import annotations
import json,hashlib,unittest
from pathlib import Path
from ziwei_secondary_nayin_reading import (
    SECONDARY,PERMITTED_POLICIES,secondary_witness_checked,
    source_bureau_with_explicit_edition_policy,compare_120_modes
)
HERE=Path(__file__).resolve().parent
class TwoEditionsNaYinSourceComparison(unittest.TestCase):
    @classmethod
    def setUpClass(c):
        c.manifest=secondary_witness_checked()
        c.saved=json.loads((HERE/'ZIWEI_SOURCE_STRICT_VS_MODERN_EDITION_120_CANDIDATES_20261020.json').read_text())
    def test_01_modern_pdf_source_is_only_later_print_not_ming(self):
        self.assertFalse(self.manifest['secondary_editing_and_early_original_authorship_verified'])
        self.assertTrue(self.manifest['modern_editor_identity_not_verified_from_title_page'])
        self.assertEqual(self.manifest['PDF_viewer_page_1_based'],80)
        self.assertEqual(self.manifest['secondary_modern_book_printed_folio'],66)
        self.assertEqual(self.manifest['downloaded_full_PDF_bytes'],11640365)
        self.assertEqual(self.manifest['downloaded_full_PDF_SHA256'],
                         '0bbb04a3d274f192f16e1d519fa91f31dc48fab0e440e16ee04109393830cbf8')
    def test_02_original_Wikisource_malformed_glyphs_not_rewritten(self):
        self.assertEqual(self.manifest['readings'][0]['primary_oldid1963110_exact_pair'],'甲戊乙亥')
        self.assertEqual(self.manifest['readings'][1]['primary_oldid1963110_exact_pair'],'戊戌已亥')
    def test_03_modern_secondary_source_readings_exact_and_source_order(self):
        self.assertEqual([x['poem_pair_ordinal'] for x in self.manifest['readings']],[6,18])
        self.assertEqual([x['secondary_edited_print_visually_read_pair'] for x in self.manifest['readings']],
                         ['甲戌乙亥','戊戌己亥'])
    def test_04_bounded_original_photo_excerpts_exact_bytes_and_sha(self):
        for entry in self.manifest['readings']:
            file=HERE/'evidence'/Path(entry['bounded_secondary_excerpt_repo_relative']).name
            self.assertTrue(file.is_file())
            self.assertEqual(file.stat().st_size,entry['excerpt_png_bytes'])
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(),entry['excerpt_png_sha256'])
            self.assertEqual(file.read_bytes()[:8],b'\x89PNG\r\n\x1a\n')
    def test_05_original_strict_default_no_silent_correction(self):
        r=source_bureau_with_explicit_edition_policy('Jia','Xu')
        self.assertIsNone(r['effective_bureau_candidate_under_requested_source_policy'])
        self.assertFalse(r['correction_applied_from_secondary'])
        self.assertFalse(r['original_primary_source_strict_valid'])
    def test_06_opt_in_corrected_fire_source_reading(self):
        r=source_bureau_with_explicit_edition_policy('Jia','Xu',
                edition_policy='explicit_later_edited_print_candidate')
        self.assertEqual(r['effective_bureau_candidate_under_requested_source_policy'],'火六局')
        self.assertEqual(r['evidence_status'],'MODERN_EDITED_SECONDARY_TEXT_SUPPORTS_EMENDATION_NOT_EARLY_ORIGINAL')
        self.assertEqual(r['secondary_evidence_PDF_first_source_page'],80)
        self.assertIsNone(r['primary_original_non_emended_bureau'])
        self.assertTrue(r['correction_applied_from_secondary'])
    def test_07_opt_in_corrected_wood_source_reading(self):
        r=source_bureau_with_explicit_edition_policy('Xin','Hai',
              edition_policy='explicit_later_edited_print_candidate')
        self.assertEqual(r['effective_bureau_candidate_under_requested_source_policy'],'木三局')
        self.assertEqual(r['primary_oldid_original_label'],'戊戌已亥')
        self.assertTrue(r['correction_applied_from_secondary'])
    def test_08_corrected_source_only_four_120_cases(self):
        self.assertEqual(self.saved['secondary_modern_edited_source_alternate_candidates'],4)
        self.assertEqual(self.saved['primary_strict_source_bureau_valid_cases'],116)
        self.assertEqual(self.saved['unresolved_early_Ming_text_authority_cases'],4)
        self.assertEqual({(r['yearstem'],r['life_branch']) for r in self.saved['secondary_changes_four_only']},
                         {('Jia','Xu'),('Ji','Xu'),('Bing','Hai'),('Xin','Hai')})
    def test_09_no_unexplained_corrections_for_116_source_valid(self):
        for p in self.saved['per_candidate_original_vs_second_edition_results']:
            a,b=p['original_primary_strict'],p['secondary_modern_edited_opt_in']
            if a['original_primary_source_strict_valid']:
                self.assertEqual(a['effective_bureau_candidate_under_requested_source_policy'],
                                 b['effective_bureau_candidate_under_requested_source_policy'])
                self.assertFalse(b['correction_applied_from_secondary'])
    def test_10_unknown_source_policy_fails_closed(self):
        with self.assertRaises(ValueError):
            source_bureau_with_explicit_edition_policy('Jia','Xu',edition_policy='always_fix')
    def test_11_no_early_physical_print_critical_collation(self):
        self.assertFalse(self.manifest['independent_expert_manuscript_diplomatic_collation_complete'])
        self.assertFalse(self.manifest['readings'][0]['primary_correction_authenticates_Ming_early_print'])
    def test_12_no_person_forecasts_or_runtime_promotions(self):
        self.assertEqual(self.saved['independent_real_human_predictions_validated'],0)
        self.assertEqual(self.saved['runtime_astrological_promotions'],0)
    def test_13_exact_report_recomputes(self):
        self.assertEqual(self.saved,compare_120_modes())
    def test_14_original_source_files_remain_separate(self):
        self.assertTrue(self.saved['original_pinned_text_and_secondary_editing_kept_separate'])
        self.assertTrue(self.saved['original_reading_stays_default'])
        self.assertTrue(self.manifest['original_website_full_PDF_file_not_committed_to_repo'])

if __name__=='__main__':
    unittest.main()
