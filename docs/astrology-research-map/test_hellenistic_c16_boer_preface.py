"""C16: reproducible editorial-hypothesis and manuscript genealogy boundaries.

Correct unit tests do not certify OCR or resurrect lost ancient autographs.
"""
import unittest

from paulus_boer_preface_lineage_c16 import preface_record, source_lineage_assessment


class TestBoerPrefaceC16(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=preface_record()
        cls.a=source_lineage_assessment()
        cls.observations={x["id"]:x for x in cls.r["observations"]}

    def test_exact_editor_and_ocr_provenance(self):
        source=self.r["source"]
        self.assertEqual(source["author_editor"],"Emilie Boer")
        self.assertEqual(source["edition_year"],1958)
        self.assertIn("PRAEFATIO",source["consulted_part"])
        self.assertFalse(source["source_page_image_seen"])
        self.assertFalse(source["source_pdf_examined"])
        self.assertIn("NOISY",source["OCR_quality"])

    def test_previously_physically_inspected_codices_in_edition_list(self):
        mss=self.observations["B1958-02"]["witnesses"]
        self.assertEqual(len(mss),3)
        self.assertEqual(
            sorted(x["shelfmark"] for x in mss),
            ["Laurentianus gr. 28.7","Monacensis gr. 170","Vaticanus gr. 1444"])
        self.assertEqual(self.a["three_physical_codices_observed"],3)

    def test_one_archetype_is_probability_not_established_fact(self):
        item=self.observations["B1958-01"]
        self.assertEqual(item["kind"],"EDITORIAL_HYPOTHESIS")
        self.assertIn("verisimile",item["literal_scope"])
        self.assertTrue(self.a["editorial_one_mutilated_archetype_is_hypothesis"])
        self.assertFalse(self.a["editorial_conjecture_is_authenticated_textual_stemma"])
        self.assertEqual(self.a["independent_genealogical_manuscript_families_proven"],0)

    def test_three_manuscript_numerical_agreement_is_not_three_ancient_authorities(self):
        self.assertEqual(
            (self.a["vatican_florence_source_positions_equal"],
             self.a["vatican_munich_readable_positions_equal"]),(120,119))
        self.assertFalse(self.a["ancient_paulus_algorithm_identified"])

    def test_early_14th_century_Z_editorial_preference(self):
        z=self.observations["B1958-03"]
        self.assertEqual(z["siglum"],"Z")
        self.assertEqual(z["shelfmark"],"Parisinus gr. 2506")
        self.assertEqual(z["Boer_date"],"early 14th century")
        self.assertIn("utilior Z",z["Boer_short_quote"])
        self.assertFalse(z["original_image_of_Z_inspected_this_batch"])

    def test_dating_conflict_not_silently_erased(self):
        z=self.observations["B1958-03"]
        self.assertIn("13th-century",z["dates_noted_in_previous_research"])
        self.assertEqual(z["Boer_date"],"early 14th century")
        self.assertEqual(self.a["textual_witness_date_discrepancy_preserved"],z["dates_noted_in_previous_research"])

    def test_Y_Paris_2425_valued_but_not_guaranteed(self):
        y=self.observations["B1958-04"]
        self.assertEqual((y["siglum"],y["shelfmark"]),("Y","Parisinus gr. 2425"))
        self.assertEqual(y["Boer_date"],"15th century")
        self.assertFalse(y["original_image_of_Y_inspected_this_batch"])

    def test_chapter32_editorial_note_low_OCR_confidence(self):
        ch=self.observations["B1958-05"]
        self.assertIn("λβ",ch["greek_section"])
        self.assertIn("non Heliodori",ch["Latin_parenthesis_short_quote"])
        self.assertIn("LOW",ch["confidence"])
        self.assertFalse(ch["Heliodorus_attribution_resolved_globally"])

    def test_vetted_apparatus_and_original_papyrus_still_open(self):
        gaps=self.r["source_gaps"]
        self.assertFalse(gaps["Boer_1958_full_text_diagram_apparatus_visually_examined"])
        self.assertFalse(gaps["Boer_1962_original_diagram_visually_examined"])
        self.assertFalse(gaps["P_Oxy_4277_original_full_image_seen"])
        self.assertFalse(gaps["ms_legend_greek_day_night_certified"])

    def test_2013_or_biographical_fit_not_entered(self):
        release=self.r["publication"]
        self.assertFalse(release["blind_biographical_fit"])
        self.assertFalse(release["production_model_changed"])
        self.assertEqual(release["untouched_human_predictive_validations"],0)
        self.assertFalse(self.a["production_scorer_modified"])

    def test_no_unverified_original_scan_or_pdf_promoted(self):
        s=self.r["source"]
        self.assertTrue(s["source_web_reference"].startswith("turn"))
        self.assertFalse(s["source_page_image_seen"])
        self.assertFalse(s["source_pdf_examined"])
        self.assertFalse(self.r["publication"]["images_or_purchased_book_redistributed"])


if __name__=="__main__":
    unittest.main()
