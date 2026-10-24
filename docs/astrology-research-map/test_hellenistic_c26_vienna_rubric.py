"""C26 source rubric classification preserves C25's no-inference boundary."""
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
DATA = HERE / "HELIODORUS_C26_VIENNA_RUBRIC_SOURCE_CLASSIFICATION_V1.json"


class TestC26ViennaRubric(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(DATA.read_text(encoding="utf-8"))

    def test_provenance_canvas_precedes_table(self):
        x = self.source["new_original_observation"]
        self.assertEqual((x["folio"],x["canvas_index_zero_based"],x["canvas_number_in_viewer"]),
                         ("205r",416,417))
        self.assertEqual(x["adjacent_folio"],"205v")
        self.assertEqual(len(x["original_study_thumbnail_local_sha256"]),64)

    def test_not_misrepresent_thumbnail_as_full_photo(self):
        x = self.source["new_original_observation"]
        self.assertIn("1600-pixel", x["photo_hash_applies_to"])
        self.assertEqual(x["adjacent_table_original_study_image_sha256"],
                         "6b6e01af7442746186c8b7fef15d0687d53d982681ccebeb4106dc9fdde15748")
        self.assertFalse(self.source["source_images_committed"])

    def test_unblinded_section_read_is_not_critical_edition(self):
        x = self.source["new_original_observation"]
        self.assertEqual(x["reading_type"],"single-reader_nonblind_visual_normalization")
        self.assertIn("τριγωνομοιρι",x["provisional_normalized_Greek"])
        self.assertFalse(x["literal_Greek_letters_verified_by_independent_paleographer"])
        self.assertFalse(x["literal_abbreviations_fully_expanded_and_checked"])

    def test_topic_link_does_not_infer_identical_algorithm(self):
        t = self.source["interpretive_boundary"]
        self.assertEqual(t["class_of_section_is_probably_shared"],"TRIPLICITY_MONOMOIRIAI")
        self.assertFalse(t["exact_rules_identical"])
        self.assertFalse(t["same_exact_30_degree_matrix_proved"])
        self.assertFalse(t["Vienna_1_15_and_16_30_are_day_night_slots_proved"])
        self.assertFalse(t["Florence_2_slots_day_night_identified"])

    def test_no_planet_cell_ever_created_for_vienna(self):
        t = self.source["interpretive_boundary"]
        self.assertEqual(t["Vienna_known_planet_assignments"],0)
        self.assertFalse(t["Vienna_205v_actual_degree_planet_assignments_fully_collated"])
        self.assertFalse(t["independent_blind_paleography_completed"])

    def test_secondary_reviews_not_same_as_boer_text(self):
        x = self.source["published_secondary_context"]
        self.assertIn("persee.fr", x["Charles_Mugler_1963"])
        self.assertIn("persee.fr", x["Alphonse_Dain_1963"])
        self.assertTrue(x["two_commentary_recensional_families_reported"])
        self.assertTrue(x["Boer_actual_critical_figures_uninspected"])
        self.assertFalse(self.source["interpretive_boundary"]["Boer_1962_critical_apparatus_opened"])

    def test_prior_negative_metrics_preserved(self):
        n = self.source["earlier_discrepancies_preserved"]
        self.assertEqual([n["C24_Florence_first_vs_C05_day"], n["C24_Florence_first_vs_C04_editor_D"],
                         n["C24_Florence_second_pair_adjacent_match"], n["C24_Florence_second_vs_C05_night"]],
                         [104,102,120,48])
        self.assertEqual([n["C22_Paulus_family_first_matching_neither_day_candidate"],
                          n["P_Oxy_4277_three_published_positions_matches"],
                          n["P_Oxy_4277_three_published_positions_mismatches"]],[96,1,2])
        self.assertTrue(n["Hephaistio_epitome_IV37_literal_40_derived_140_main_150_kept_distinct"])

    def test_zero_human_validations_or_runtime_changes(self):
        t = self.source["interpretive_boundary"]
        self.assertEqual((t["new_prod_scorer_rules"],t["prospective_blinded_human_validations"]),(0,0))
        self.assertEqual(self.source["main_objective_status"],"OPEN")


if __name__ == "__main__":
    unittest.main()
