"""C21 direct Greek clause / sect-light scope, source-only regressions.

These tests are exact reproducible interpretation controls; they do not
prove that the modern online text reproduces Boer's printed apparatus,
an ancient author's autograph, or astrology's human predictive validity.
"""
import unittest

from paulus_c21_luminary_scope import (
    greek_source_witness,
    chapter5_by_sign_ruler,
    chapter32_sect_light_ruler,
    source_scope_audit,
)
from paulus_trigon_narrative_c05 import (
    narrative_one_cycle, printed_diurnal_difference_summary
)
from paulus_monomoiria_source_c04 import edited_day_degree_ruler


class TestDirectGreekScopeC21(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=greek_source_witness()
        cls.a=source_scope_audit()
        cls.clauses={x["id"]:x for x in cls.w["clauses"]}

    def test_exact_Eulogikon_markdown_and_html_provenance(self):
        s=self.w["source"]
        self.assertIn("paul-alexandria-astrology-sum-aa.md",s["markdown"])
        self.assertEqual(s["markdown_bytes"],181883)
        self.assertEqual(s["markdown_SHA256"],"78b9da9d8fdf9187c969ebb4cd3b46151f9831d8e68d238274962f0e8696a263")
        self.assertEqual(s["html_bytes"],245014)
        self.assertFalse(s["modern_editorial_base_verified_as_Boer_1958"])
        self.assertFalse(s["primary_papyrological_artifact"])

    def test_literal_short_clauses_separate_from_interpretation(self):
        self.assertEqual(len(self.clauses),4)
        self.assertEqual(self.clauses["C21-C5-FRACTION"]["short_exact"],
                         "καὶ τὰ λεπτὰ ὡς μοῖραν μίαν")
        self.assertEqual(self.clauses["C21-C32-FACTION"]["short_exact"],
                         "τὰς μοίρας τοῦ αἱρετικοῦ φωτὸς")
        self.assertEqual(self.clauses["C21-C32-NODUP"]["short_exact"],
                         "μὴ διδοὺς ἐκ δευτέρου")
        self.assertTrue(all(c["status"]=="EXACT_DIGITAL_GREEK_WORDING"
                            for c in self.clauses.values()))

    def test_chapter5_sign_start_fraction_stays_in_first_interval(self):
        self.assertEqual(chapter5_by_sign_ruler("Libra",0,0),"Venus")
        self.assertEqual(chapter5_by_sign_ruler("Libra",0,59),"Venus")
        self.assertEqual(chapter5_by_sign_ruler("Libra",2,35),"Moon")
        self.assertEqual(chapter5_by_sign_ruler("Libra",9,35),"Moon")

    def test_chapter32_is_light_of_sect_not_generic_natal_point(self):
        self.assertEqual(chapter32_sect_light_ruler(
            sect="day",luminary="Sun",light_sign="Aries",ordinal_degree=1),"Sun")
        self.assertEqual(chapter32_sect_light_ruler(
            sect="night",luminary="Moon",light_sign="Aries",ordinal_degree=1),"Jupiter")
        self.assertEqual(chapter32_sect_light_ruler(
            sect="night",luminary="Moon",light_sign="Cancer",ordinal_degree=1),"Mars")

    def test_reject_opposite_or_arbitrary_luminary(self):
        for sect,lumi in [("day","Moon"),("night","Sun"),
                          ("day","Mars"),("night","Ascendant")]:
            with self.assertRaises(ValueError):
                chapter32_sect_light_ruler(
                    sect=sect,luminary=lumi,light_sign="Aries",ordinal_degree=1
                )

    def test_sect_and_ordinal_boundary_fail_closed(self):
        for sect in ("unknown","twilight","DAY",""):
            with self.assertRaises(ValueError):
                chapter32_sect_light_ruler(
                    sect=sect,luminary="Sun",light_sign="Aries",ordinal_degree=1
                )
        for ordinal in (0,31,True,1.5,"2"):
            with self.assertRaises(ValueError):
                chapter32_sect_light_ruler(
                    sect="day",luminary="Sun",light_sign="Aries",ordinal_degree=ordinal
                )

    def test_narrative_skips_repeated_venus_until_seven_unique(self):
        for sect in ("day","night"):
            for tri in ("fire","earth","air","water"):
                sequence=narrative_one_cycle(tri,sect)
                self.assertEqual(len(sequence),7)
                self.assertEqual(len(set(sequence)),7)
                self.assertEqual(sequence.count("Venus"),1)

    def test_exact_disputed_water_degree8_remains_three_witnesses(self):
        # Only a source-table comparison: C21 Greek narrative (if sect Sun
        # in Cancer), Greenbaum's day table, and Munich literal MS reading.
        self.assertEqual(chapter32_sect_light_ruler(
            sect="day",luminary="Sun",light_sign="Cancer",ordinal_degree=8),"Venus")
        self.assertEqual(edited_day_degree_ruler("Cancer",8,sect="day"),"Mars")
        self.assertEqual(self.w["missing_digital_table_rows"]["C04_to_C05_printed_disagreements"],34)

    def test_missing_online_cells_do_not_make_missing_ancient_table(self):
        m=self.w["missing_digital_table_rows"]
        self.assertIn("DIGITAL_MARKDOWN_RENDITION_ONLY",m["absence_scope"])
        self.assertFalse(self.a["digital_online_diagram_has_transcribed_120_planet_cells"])
        self.assertFalse(self.w["source"]["modern_editorial_base_verified_as_Boer_1958"])

    def test_chapter33_variants_are_alternatives_not_accumulator(self):
        ch=self.w["chapter33"]
        self.assertTrue(ch["source_compares_multiple_alternative_procedures"])
        self.assertTrue(ch["does_not_certify_Ascendant_degree_of_Berlin_21347"])
        self.assertTrue(ch["does_not_prove_Egyptian_Saturn_term_in_Berlin_ink"])

    def test_C05_Historical_negative_cases_stay_preserved(self):
        self.assertEqual(printed_diurnal_difference_summary()["total_differing_cells"],34)
        self.assertEqual(self.a["Oxford_4277_matches_retained"],1)
        self.assertEqual(self.w["source_model_bindings"]["C05_P_Oxy_4277_historical_nonmatches"],2)

    def test_no_production_promotion_blinded_human_results(self):
        a=self.w["admission"]
        self.assertFalse(a["source_renders_full_Boer_1958_Greek_apparatus"])
        self.assertFalse(a["repeated_eight_slot_120_cell_chart_can_replace_Greek_prose"])
        self.assertFalse(a["production_scorer_modified"])
        self.assertFalse(a["cross_tradition_map_modified"])
        self.assertEqual(a["human_predictive_validations"],0)
        self.assertFalse(a["gansten_purchased_ebook_extracted"])


if __name__=="__main__":
    unittest.main()
