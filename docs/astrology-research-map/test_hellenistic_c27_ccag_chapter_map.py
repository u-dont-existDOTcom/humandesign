"""C27 CCAG chapter titles and witnessed boundaries remain source-typed, not predictive rules."""
import json
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
SOURCE=HERE/"HELIODORUS_C27_CCAG_CHAPTER_BOUNDARIES_V1.json"

class TestC27HistoricalCatalogueBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_two_scans_not_ocr_only(self):
        s=self.data["printed_catalogues"]
        self.assertEqual(len(s),2)
        self.assertEqual({r["short"] for r in s},{"CCAG_VI","CCAG_I"})
        self.assertTrue(all(r["printed_page_directly_visually_read"] for r in s))
        self.assertTrue(all(r["OCR_standalone_not_authority"] for r in s))
        self.assertTrue(all(len(r["pdf_sha256"])==64 for r in s))

    def test_correct_printed_vs_pdf_page_references(self):
        s={x["short"]:x for x in self.data["printed_catalogues"]}
        self.assertEqual((s["CCAG_VI"]["printed_page"],s["CCAG_VI"]["pdf_page_one_based"]),(27,45))
        self.assertEqual((s["CCAG_I"]["printed_page"],s["CCAG_I"]["pdf_page_one_based"]),(27,17))
        self.assertEqual(s["CCAG_I"]["pdf_page_contains_two_printed_pages"],[26,27])

    def test_vienna_actual_chapter_numbers_and_folio(self):
        v=self.data["catalogue_witnesses"]["vienna"]
        self.assertEqual((v["chapter_trigon"]["number_arabic"],v["chapter_trigon"]["last_folio"]),(34,"205v"))
        self.assertEqual((v["chapter_next"]["number_arabic"],v["chapter_next"]["last_folio"]),(35,"209"))
        self.assertIn("μονομοιρίας",v["chapter_trigon"]["title"])
        self.assertIn("ἀναγκαίας",v["chapter_next"]["title"])

    def test_florence_distinct_primary_heading_figure_and_next(self):
        f=self.data["catalogue_witnesses"]["florence"]
        self.assertEqual([f["chapter_trigon"]["folio"],f["figure"]["folio"],f["chapter_next"]["folio"]],
                         ["202v","204v","205"])
        self.assertIn("τριγωνικῶν",f["figure"]["caption"])
        self.assertIn("ἀναγκαστικῆς",f["chapter_next"]["title"])
        self.assertTrue(f["chapter_next"]["distinct_next_chapter_not_column_gloss"])

    def test_c26_early_reading_not_silently_replaced_by_catalogue(self):
        v=self.data["catalogue_witnesses"]["vienna"]
        self.assertNotEqual(v["photo_205r"]["c26_red_rubric_preliminary"],
                            v["chapter_trigon"]["catalogue_terminal_words"])
        self.assertFalse(v["photo_205r"]["rubric_exact_same_as_catalogue_terminal"])

    def test_two_regions_of_same_vienna_not_independent(self):
        x=self.data["catalogue_witnesses"]["vienna"]["earlier_catalogued_passage"]
        self.assertEqual(x["folio"],"159–159v")
        self.assertEqual(x["catalogue_printed_page"],2)
        self.assertEqual(x["study_canvases_checked"],[324,325,326])
        self.assertFalse(x["actual_table_photo_confirmed"])
        self.assertFalse(x["independent_manuscript"])

    def test_catalogue_headers_do_not_certify_night_positions(self):
        c=self.data["consequence"]
        self.assertTrue(c["trigon_monomoiria_source_topic_both_attested"])
        self.assertTrue(c["next_chapter_semantics_distinct_from_figure"])
        self.assertFalse(c["can_infer_Florence_slots_are_day_night_from_catalogue"])
        self.assertFalse(c["can_infer_Vienna_15_15_subcolumns_are_day_night_from_catalogue"])
        self.assertFalse(c["exact_ancient_algorithm_reconstructed"])
        self.assertFalse(c["Boers_1962_actual_apparatus_read"])

    def test_scientific_none_and_frozen_negative_controls(self):
        n=self.data["frozen_previous_results"]
        c=self.data["consequence"]
        self.assertEqual([n["C24_first_vs_C05_day"],n["C24_first_vs_C04_corrected"],
                         n["C24_second_adjacent_swap_consistency"],n["C24_second_vs_C05_night"]],[104,102,120,48])
        self.assertEqual([n["C22_older_source_neither_C04_nor_C05_day"],
                          n["P_Oxy4277_matches"],n["P_Oxy4277_nonmatches"]],[96,1,2])
        self.assertEqual((c["predictive_human_validations"],c["production_scoring_promotions"]),(0,0))
        self.assertEqual(self.data["main_objective_status"],"OPEN")

if __name__=="__main__":
    unittest.main()
