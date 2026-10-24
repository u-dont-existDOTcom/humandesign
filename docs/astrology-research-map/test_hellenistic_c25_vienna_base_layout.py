"""C25 structural primary-source audit; no guessed planetary values.

Original photograph can substantiate an apparent 15+15 degree numbering,
but cannot alone certify astrology's efficacy or the 1962 Greek edition.
"""
import unittest
from heliodorus_c25_vienna_layout_audit import (
    vienna_source, inspected_degree_number_pairs, bounded_layout_reconciliation
)


class TestViennaACommentaryC25(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=vienna_source()
        cls.a=bounded_layout_reconciliation()
        cls.photo=cls.src["primary_original_manuscript"]

    def test_Official_Austrian_Library_manuscript(self):
        self.assertIn("phil. gr. 115",self.photo["shelfmark"])
        self.assertIn("1182CE33",self.photo["public_iiif_manifest"])
        self.assertEqual(self.photo["manifest_canvas_count"],468)

    def test_original_canvas_418_folio205v_and_resized_hash(self):
        self.assertEqual(self.photo["located_folio"],"205v")
        self.assertEqual((self.photo["located_canvas_index_zero_based"],
                          self.photo["located_canvas_number_in_viewer"]),(417,418))
        self.assertEqual(self.photo["source_full_photographic_dimensions"],[4192,6562])
        self.assertEqual(self.photo["actual_study_image_dimensions"],[2600,4070])
        self.assertTrue(self.photo["study_image_is_resized_not_entire_original_bytes"])
        self.assertEqual(self.photo["study_image_bytes"],1533303)
        self.assertEqual(self.photo["study_image_sha256"],
                         "6b6e01af7442746186c8b7fef15d0687d53d982681ccebeb4106dc9fdde15748")
        self.assertFalse(self.photo["photos_in_repository"])

    def test_125_thumbnails_and_flanking_pages_verified(self):
        x=self.photo["scan_range"]
        self.assertEqual((x["canvas_indices_zero_based_start"],
                          x["canvas_indices_zero_based_end"]),(325,449))
        self.assertEqual((x["total_canvas_images_fetched_as_thumbnails"],
                          x["download_failures"],x["contact_sheets_visually_examined"]),(125,0,6))
        self.assertEqual(self.photo["page_before"]["folio"],"205r")
        self.assertEqual(self.photo["page_after"]["folio"],"206r")

    def test_readable_number_examples_first_to_fifteenth_and_16_to_30(self):
        self.assertEqual(
            [(r["row"],r["left_number"],r["right_number"])
             for r in inspected_degree_number_pairs()],
            [(1,1,16),(2,2,17),(3,3,18),(14,14,29),(15,15,30)]
        )
        self.assertEqual(self.a["degree_pair_examples_passing_15_offset_diagnostic"],5)
        self.assertFalse(self.a["Vienna_num_pair_semantics_proved"])

    def test_layout_is_distinct_from_Florence_two_glyph_slots(self):
        chart=self.src["table_literal_visual_observations"]
        self.assertTrue(chart["two_numbered_degree_subcolumns_per_row_provisional"])
        self.assertEqual(chart["numbered_rows_per_group_provisionally"],15)
        self.assertTrue(chart["another_adjacent_Aries_marked_section_visible"])
        self.assertFalse(chart["auxiliary_Aries_section_function_known"])
        self.assertFalse(self.a["older_Florence_and_Vienna_are_same_day_night_scheme_proved"])
        self.assertEqual(self.a["later_Florence_24h_double_planet_slots"],240)

    def test_no_Vienna_planetary_glyphs_imputed(self):
        self.assertEqual(self.src["table_literal_visual_observations"]["planetary_glyphs_at_degree_level_independently_read"],0)
        self.assertFalse(self.a["source_complete_30x4_planetary_cells_transcribed"])
        self.assertFalse(self.a["Vienna_has_day_night_pairs_proved"])
        self.assertFalse(self.src["remainder"]["check_Boer_1962_printed_chapter_and_manuscript_sigla"] is False)

    def test_date_discrepancy_preserved_not_artificially_resolved(self):
        x=self.src["date_and_genealogy_uncertainty"]
        self.assertEqual(x["ONB_iiif_catalogue_dating"],"1200")
        self.assertIn("1111–1169",x["Pinakes_catalogue_estimate"])
        self.assertIn("1241",x["ONB_iiif_catalogue_explanatory_note"])
        self.assertFalse(x["date_disagreement_resolved"])
        self.assertTrue(x["do_not_silently_choose_earliest"])

    def test_Boer_main_Vienna_witness_does_not_mean_edition_read(self):
        x=self.src["textual_work_attribution"]
        self.assertIn("Boer",x["Boer_editorial_edition"])
        self.assertIn("1963",x["contemporary_review"])
        self.assertFalse(x["Boer_1962_actual_Greek_edition_pages_seen"])
        self.assertFalse(x["commentary_author_Heliodorus_personally_proven"])

    def test_subject_identification_requires_original_greek_not_chart_shape(self):
        q=self.src["table_literal_visual_observations"]
        self.assertFalse(q["same_subject_as_Florence_mononomoiria_chart_certified_from_own_Greek"])
        self.assertFalse(q["Vienna_table_exact_Greek_heading_read"])
        self.assertTrue(q["tentative_15_plus_15_layout_not_planetary_rules"])
        self.assertTrue(self.src["remainder"]["prove_table_subject_before_comparing_glyphs"])

    def test_previous_historical_negatives_and_zero_humans(self):
        self.assertEqual(self.a["C05_P_Oxy_matches_retained"],1)
        self.assertFalse(self.a["C24_source_numbers_overwritten"])
        self.assertFalse(self.a["scoring_rule_promoted"])
        self.assertEqual(self.a["human_predictive_validations"],0)
        self.assertFalse(self.src["remainder"]["Gansten_purchased_Kindle_edition_extracted"])


if __name__=="__main__":
    unittest.main()
