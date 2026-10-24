"""C22 source-reconciliation regression, no human predictive evaluation."""
import unittest

from paulus_c22_120cell_source_comparison import (
    compare_all_120, provenance, CATEGORIES
)
from paulus_monomoiria_source_c04 import edited_day_degree_ruler
from paulus_trigon_narrative_c05 import narrative_degree_ruler
from paulus_c15_three_manuscript_comparison import three_manuscript_comparison


class TestFullPaulusSourceReconciliationC22(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=provenance()
        cls.a=compare_all_120()
        cls.rows={(r["trigon"],r["ordinal_degree"]):r for r in cls.a["rows"]}

    def test_local_owner_translation_scan_identity_and_extent(self):
        p=self.p["source_groups"]["greenbaum_English_printed"]
        self.assertEqual(p["pdf_page_count"],93)
        self.assertEqual(p["local_pdf_sha256"],"dffa2a86e2a8c13135b1fc9e68b798224a25464e617fa221a7551b5be08b605a")
        self.assertIn("page 77",p["last_scanned_leaf"])
        self.assertTrue(p["no_publisher_scan_of_Boer_1958_apparatus_in_this_pass"])
        self.assertFalse(p["photo_redistributed"])

    def test_English_page_references_and_layer_maintained(self):
        p=self.p["source_groups"]["greenbaum_English_printed"]["inspected_pages"]
        self.assertEqual([(x["pdf_page"],x["printed_page"]) for x in p],
                         [(82,66),(83,67),(84,68),(85,69),(86,70)])
        self.assertIn("EDITORIAL_RECONSTRUCTION",p[1]["source_layer"])
        self.assertIn("TRANSLATOR_COMMENTARY",p[0]["source_layer"])

    def test_four_triplicities_printed_visual_spot_checks(self):
        spec=self.p["source_groups"]["greenbaum_English_printed"]["p67_visual_sample_cells"]
        signs={"fire":"Aries","earth":"Taurus","air":"Gemini","water":"Cancer"}
        for t,cells in spec.items():
            for degree,planet in cells:
                self.assertEqual(edited_day_degree_ruler(signs[t],degree,sect="day"),planet)

    def test_full_120_disjoint_exhaustive_partition(self):
        a=self.a
        self.assertEqual(a["physical_photo_candidate_positions"],120)
        self.assertEqual(a["category_counts"],{
            "both":12,"narrative_only":11,"greenbaum_only":1,"neither":96})
        self.assertEqual(set(a["category_counts"]),set(CATEGORIES))
        self.assertEqual(sum(a["category_counts"].values()),120)

    def test_complete_per_trigon_partition(self):
        expected={
            "fire":{"both":6,"narrative_only":0,"greenbaum_only":0,"neither":24},
            "earth":{"both":4,"narrative_only":0,"greenbaum_only":0,"neither":26},
            "air":{"both":2,"narrative_only":4,"greenbaum_only":1,"neither":23},
            "water":{"both":0,"narrative_only":7,"greenbaum_only":0,"neither":23},
        }
        self.assertEqual(self.a["category_per_trigon"],expected)
        self.assertTrue(all(sum(b.values())==30 for b in expected.values()))

    def test_day_narrative_vs_photo_23_of_120_not_34_of_120(self):
        self.assertEqual(self.a["manuscript_vs_narrative_day_matches"],23)
        self.assertEqual(self.a["manuscript_vs_greenbaum_day_matches"],13)
        self.assertEqual(sum(r["category"] in ("both","narrative_only") for r in self.a["rows"]),23)
        self.assertEqual(sum(r["category"] in ("both","greenbaum_only") for r in self.a["rows"]),13)

    def test_nocturnal_diagnostic_does_not_rescue_manuscript_globally(self):
        self.assertEqual(self.a["manuscript_vs_narrative_night_matches"],13)
        self.assertFalse(self.a["manuscript_explicit_day_night_rubric_certified"])
        self.assertEqual(self.rows["fire",1]["narrative_day"],"Sun")
        self.assertEqual(self.rows["fire",1]["narrative_night_diagnostic"],"Jupiter")

    def test_34_previous_trouble_cells_are_only_subset(self):
        self.assertEqual(self.a["previously_disputed_34"],
                         {"total":34,"narrative_only":11,"greenbaum_only":1,"neither":22})
        self.assertEqual(self.a["previously_agreed_day_sources_86"],
                         {"total":86,"manuscript_agrees_both":12,"manuscript_disagrees_both":74})
        self.assertEqual(34+86,120)

    def test_Cancer_8_three_distinct_witness_readings(self):
        row=self.rows["water",8]
        self.assertEqual((row["manuscript_label"],row["narrative_day"],row["greenbaum_printed_day"]),
                         ("Mercury","Venus","Mars"))
        self.assertEqual(row["category"],"neither")

    def test_original_Munich_unknown_remains_unfilled(self):
        self.assertEqual(self.a["Munich_readable_compared"],119)
        self.assertIsNone(self.rows["earth",28]["manuscript_Munich_label"])
        self.assertEqual(self.rows["earth",28]["manuscript_Florence_label"],"Mars")
        self.assertEqual(self.rows["earth",28]["manuscript_label"],"Mars")

    def test_transcription_and_stemma_not_inadvertently_canonized(self):
        s=self.p["source_groups"]["physical_manuscript_family"]
        self.assertTrue(s["three_separate_photo_sources_recorded"])
        self.assertFalse(s["textual_stemmatic_independence_verified"])
        self.assertFalse(s["independent_blinded_paleographic_retranscription_done"])
        self.assertTrue(s["same_research_context_and_previous_sequences_were_known_when_later_witnesses_deciphered"])
        self.assertFalse(self.a["Boer_1958_Greek_critical_table_apparatus_inspected"])

    def test_negative_papyrus_and_production_boundaries_survive(self):
        q=self.p["unresolved"]
        self.assertFalse(q["P_Oxy_4277_Greek_labels_independently_redeciphered"])
        self.assertEqual((q["unchanged_C05_papyrus_matches"],q["unchanged_C05_papyrus_failures"]),(1,2))
        self.assertFalse(q["scorer_changed"])
        self.assertFalse(q["cross_tradition_map_changed"])
        self.assertEqual(self.a["human_predictive_validations"],0)
        self.assertFalse(self.a["production_rule_promoted"])


if __name__=="__main__":
    unittest.main()
