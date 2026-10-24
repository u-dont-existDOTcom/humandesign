"""C28: Distinct physical Vienna codices, not fake source contradictions."""
import json
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
DATA=HERE/"HELIODORUS_C28_KROLL_CODEX_IDENTITY_V1.json"
OLD=HERE/"HELIODORUS_C27_CCAG_CHAPTER_BOUNDARIES_V1.json"

class TestC28CodexIdentity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=json.loads(DATA.read_text(encoding="utf8"))
        cls.old=json.loads(OLD.read_text(encoding="utf8"))

    def test_kroll_printed_covers_separately_verified_pages(self):
        x=self.src["catalogue"]
        self.assertEqual(x["printed_pages_examined"],[1,2,16,27])
        self.assertEqual(x["pdf_pages_one_based"],[19,20,34,45])
        self.assertEqual(len(x["pdf_sha256"]),64)
        self.assertTrue(x["photo_and_text_read_directly"])

    def test_first_codex_108_owns_f159_table_reference(self):
        x=self.src["codex_108"]
        self.assertEqual(x["catalogue_item"],1)
        self.assertIn("gr.108",x["shelfmark"])
        self.assertEqual((x["page_start"],x["page_end"]),(1,16))
        self.assertEqual(x["trigon_folio"],"159-159v")
        self.assertIn("tabula f. 159v",x["ending_note"])

    def test_second_codex_115_owns_f205_table(self):
        x=self.src["codex_115"]
        self.assertEqual(x["catalogue_item"],2)
        self.assertIn("gr.115",x["shelfmark"])
        self.assertEqual((x["page_start"],x["page_end"]),(16,27))
        self.assertEqual(x["trigon_entry_page"],27)
        self.assertEqual((x["trigon_chapter"],x["trigon_folio"]),(34,"205v"))

    def test_old_c27_really_misattributed_p2_to_115(self):
        earlier=self.old["catalogue_witnesses"]["vienna"]
        self.assertIn("gr.115",earlier["shelfmark"])
        self.assertEqual(earlier["earlier_catalogued_passage"]["catalogue_printed_page"],2)
        self.assertEqual(self.src["correction"]["corrected_witness"],"phil. gr.108")

    def test_source_mutation_is_supersession_not_rewrite(self):
        x=self.src["correction"]
        self.assertTrue(x["prior_artifact_retained"])
        self.assertEqual(x["error_type"],"CROSS_CODEX_CONFLATION")
        self.assertTrue(x["catalogue_f159_v_photo_paradox_resolved"])

    def test_cannot_verify_108_from_115_photos(self):
        a=self.src["codex_108"];b=self.src["codex_115"]
        self.assertFalse(a["original_photo_read"])
        self.assertEqual(a["planetary_cells_verified"],0)
        self.assertTrue(b["photos_of_115_do_not_verify_108"])
        self.assertEqual(b["official_manuscript_IIIF_canvas"],417)

    def test_original_editorial_crossref_not_algorithm(self):
        s=self.src["scientific_gates"]
        self.assertTrue(s["Kroll_cross_reference_to_Florence_is_editorial"])
        self.assertTrue(s["physical_witnesses_distinct"])
        self.assertFalse(s["independent_rule_proved"])
        self.assertFalse(s["Boer_1962_apparatus_opened"])
        self.assertFalse(s["day_night_slots_proved"])

    def test_parent_owner_outcome_still_open_zero_humans(self):
        self.assertEqual(self.src["root_goal_status"],"OPEN")
        self.assertEqual(self.src["scientific_gates"]["human_predictive_validations"],0)
        self.assertEqual(self.src["scientific_gates"]["production_scoring_changes"],0)

if __name__=="__main__":
    unittest.main()
