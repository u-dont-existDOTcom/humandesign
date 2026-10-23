"""C11 exact printed-edition comparison + authentic but uncollated Munich MS.
Green unit tests check edited-source arithmetic and admissibility, NOT ancient
astrology accuracy nor actual blinded human predictive validity.
"""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DOC=json.loads((ROOT/"HEPHAISTIO_C11_MAIN_EPITOME_AND_MUNICH_MANUSCRIPT_WITNESS_V1.json").read_text(encoding="utf-8"))
C10=json.loads((ROOT/"HEPHAISTIO_C10_EPITOME_IV37_SOURCE_QUESTION_REGISTER_V1.json").read_text(encoding="utf-8"))

class TestHephaistioC11SourceEvidence(unittest.TestCase):
    def setUp(self):
        self.rows={row["parent"]:row for row in DOC["periods"]}

    def test_corrected_πγ_83_not_false_positive_πν_130(self):
        s=DOC["critical_new_readings"]["c10_sun_correction"]
        self.assertEqual((s["c10_bad_literal"],s["c11_editted_epitome_literal"]),(130,83))
        self.assertEqual((s["old_c10_sum"],s["new_c11_sum"]),(578,531))
        self.assertEqual(s["greek_printed_number"],"πγ")
        self.assertTrue(s["false_green_test_repaired"])
        self.assertFalse(s["biography_fitting"])

    def test_c10_supersession_applied_to_original_fixture(self):
        sun=C10["parent_periods"]["Sun"]
        self.assertEqual(sun["edited_printed_values_by_recipient"],[104,52,64,83,30,80,118])
        self.assertEqual((sun["possible_sum_days"],sun["possible_delta_vs_30day_months"]),([531],[-39]))
        self.assertIn("false-green",C10["supersession"]["c11_corrected_source_literal"])

    def test_seven_original_main_and_epitome_printed_vectors(self):
        main={
            "Saturn":[210,84,105,133,57,150,175],
            "Jupiter":[85,34,42,54,22,57,71],
            "Mars":[105,42,52,66,28,70,87],
            "Sun":[130,52,64,83,35,87,118],
            "Venus":[57,22,28,36,15,38,47],
            "Mercury":[141,56,70,90,36,96,117],
            "Moon":[177,71,87,115,47,119,148]}
        epi={
            "Saturn":[210,84,105,133,57,40,105],
            "Jupiter":[85,34,42,54,22,57,71],
            "Mars":[105,52,52,66,28,70,87],
            "Sun":[104,52,64,83,30,80,118],
            "Venus":[57,22,28,36,15,38,17],
            "Mercury":[141,57,70,90,36,96,117],
            "Moon":[177,71,87,None,47,119,148]}
        self.assertEqual(set(self.rows),set(main))
        for p in main:
            self.assertEqual(self.rows[p]["main_1973_printed"],main[p],p)
            self.assertEqual(self.rows[p]["epitome_1974_printed"],epi[p],p)

    def test_literal_sums_must_follow_values_not_test_fixtures(self):
        expected_main={"Saturn":914,"Jupiter":365,"Mars":450,"Sun":569,"Venus":243,"Mercury":606,"Moon":764}
        expected_epi={"Saturn":[734],"Jupiter":[365],"Mars":[460],"Sun":[531],"Venus":[213],"Mercury":[607],"Moon":[764,794]}
        for p,row in self.rows.items():
            self.assertEqual(row["main_sum"],sum(row["main_1973_printed"]),p)
            self.assertEqual(row["main_sum"],expected_main[p],p)
            ev=sum(v for v in row["epitome_1974_printed"] if v is not None)
            if p=="Moon":
                self.assertEqual(row["epitome_sum_candidates"],[ev+115,ev+145])
            else:
                self.assertEqual(row["epitome_sum_candidates"],[ev])
            self.assertEqual(row["epitome_sum_candidates"],expected_epi[p],p)

    def test_venus_direction_preserved_not_conflated(self):
        v=DOC["critical_new_readings"]["venus_direction_recheck"]
        self.assertEqual((v["epitome_value"],v["main_value"]),(36,36))
        self.assertEqual(v["sun_parent_venus_recipient_main_value"],35)
        self.assertEqual((self.rows["Venus"]["epitome_sum_candidates"],self.rows["Venus"]["main_sum"]),([213],243))
        self.assertEqual(C10["parent_periods"]["Venus"]["possible_sum_days"],[213])

    def test_mars_witnesses_not_based_on_closure(self):
        m=DOC["critical_new_readings"]["mars_recensional_difference"]
        self.assertEqual((m["epitome"],m["main"]),(52,42))
        self.assertEqual((m["epitome_sum"],m["main_sum"]),(460,450))
        self.assertFalse(m["independent_ancient_manuscript_collation"])

    def test_literal_40_derived_140_main_150(self):
        s=DOC["critical_new_readings"]["saturn_critical"]
        self.assertEqual((s["epitome_literal"],s["epitome_approx_derived"],s["main_literal"]),(40,140,150))
        self.assertNotEqual(s["epitome_literal"],s["epitome_approx_derived"])

    def test_moon_glyph_and_historical_papyrus_still_open(self):
        m=DOC["critical_new_readings"]["moon_sun"]
        self.assertEqual(m["epitome_ambiguous"],[115,145])
        self.assertIsNone(self.rows["Moon"]["epitome_1974_printed"][3])
        self.assertEqual(self.rows["Moon"]["epitome_sum_candidates"],[764,794])
        self.assertFalse(DOC["other_open"]["oxyrhynchus_4277_original_image_inspected"])

    def test_actual_munich_photo_new_but_no_invented_120cell_collation(self):
        m=DOC["sources"]["munich"]
        f=DOC["munich_figure"]
        self.assertEqual(m["shelfmark"],"Cod. graec. 170")
        self.assertIn("00081",m["iiif_image_uri"])
        self.assertEqual(f["column_heading_signs"],["Aries","Taurus","Gemini","Cancer"])
        self.assertEqual(len(f["visually_read_first_degree"]),4)
        self.assertTrue(all("PROVISIONAL" in v["confidence"] or "TENTATIVE" in v["confidence"] for v in f["visually_read_first_degree"]))
        self.assertFalse(f["full_120_cell_glyph_decipherment_complete"])
        self.assertFalse(f["day_night_sect_identified"])
        self.assertEqual(f["adjacent_manuscript_pages_visually_opened"],[64,66])
        self.assertEqual(f["adjacent_bsb_iiif_images_visually_opened"],[80,82])
        self.assertEqual(f["first_degree_assignments_admitted_for_34_cell_comparison"],0)
        self.assertFalse(f["image_redistributed"])

    def test_source_books_and_human_data_not_promoted(self):
        c=DOC["controls"]
        self.assertEqual(c["human_predictive_validations"],0)
        for k in ("production_scorer_changed","cross_tradition_map_changed","gansten_kindle_extracted","original_books_redistributed","biographical_fitting"):
            self.assertFalse(c[k],k)
        self.assertEqual(DOC["other_open"]["paulus_disputed_cells_before"],34)
        self.assertEqual(DOC["other_open"]["paulus_disputed_cells_resolved_in_c11"],0)

if __name__=="__main__":
    unittest.main()
