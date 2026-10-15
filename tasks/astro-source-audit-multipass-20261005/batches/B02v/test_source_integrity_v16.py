"""V16 source-only checks for printed352 U70 outside-house limitation.

Inherits current relevant V15 checks, leaving earlier snapshot tests unchanged.
This suite cannot prove empirical astrology or full original omission freedom.
"""
import hashlib,json,unittest
import test_source_integrity_v15 as prev
B=prev.B
P=prev.P
def load(p):return json.loads((B/p).read_text())
def digest(p):return hashlib.sha256((B/p).read_bytes()).hexdigest()
class CurrentV16(prev.CurrentV15):
    def test_unresolved_53_and_unique_ids(self):
        u=load("UNRESOLVED_DRAFT.json")
        self.assertEqual(u["retained_count"],70)
        self.assertEqual(len(u["issues"]),70)
        self.assertEqual(len({x["id"] for x in u["issues"]}),70)
        self.assertEqual([x["id"] for x in u["issues"][-5:]],["U66","U67","U68","U69","U70"])
    def test_printed_p352_outside_house_margin_scoped(self):
        r=P[2670]
        self.assertEqual(r["source_record_kind"],"goods_outside_house_element_cardinal_points")
        self.assertEqual(r["source_locator"]["pdf_pages"],[386])
        self.assertIn("OUTSIDE the house",r["source_statement"])
        self.assertIn("outside the house",r["preconditions"][0])
        self.assertIn("fiery/east",r["source_statement"])
        self.assertFalse(r["case_evidence_countable"])
        for n in (2667,2668,2669):
            self.assertNotIn("outside the house",P[n]["source_statement"].lower())
    def test_exact_before_U70_source_and_image(self):
        self.assertEqual(digest("recovery/producer_p385_387_before_U70_p352_20261015.json"),
           "6ad66feabd81eb3a93841be51af434ccd3782806f2c7896fecf66672c955ca3a")
        im=next(x for x in load("SOURCE_IMAGE_MANIFEST.json")["images"] if x["pdf_page"]==386)
        self.assertEqual(digest(im["path"]),im["sha256"])
    def test_reverse_p354_source_map(self):
        j=load("independent_review/REVERSE_SOURCE_TO_RECORD_P388_20261015.json")
        self.assertEqual(j["original_pdf_page"],388)
        self.assertEqual(j["record_count"],21)
        self.assertEqual([x["record_number"] for x in j["source_to_record"]],list(range(2694,2715)))
        self.assertIn("U69",j["material_finding"])
        self.assertFalse(j["source_omission_proof"])
        self.assertFalse(j["independent_full_fidelity"])
    def test_bounded_402_source_records_review_map_exact(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U70_20261015.json")
        self.assertEqual(j["distinct_bounded_review_records"],402)
        self.assertEqual(j["unique_record_ids_in_bounded_review_evidence"],list(range(2573,2975)))
        self.assertEqual(j["records_without_documented_finite_page_specific_check_in_four_review_groups"],[])
        self.assertEqual(j["remaining_original_pdf_pages_for_this_specific_scope"],[])
        self.assertEqual([x["included_source_record_count"] for x in j["past_review_sets"]],[103,109,64,148])
        self.assertEqual([len(x["records_new_to_prior_groups"]) for x in j["past_review_sets"]],[103,109,43,147])
        self.assertEqual(j["draft_sha256"],digest("RULES_DRAFT.json"))
        self.assertFalse(j["source_independent_fidelity_review_completed"])
        self.assertFalse(j["chapter_L_source_complete"])
    def test_all_review_documents_exist_and_coverage_not_exaggerated(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U70_20261015.json")
        for g in j["past_review_sets"]:
            for doc in g["review_evidence_documents"]:self.assertTrue((B/doc).is_file(),doc)
            self.assertIn("NOT_VERBATIM_FULL_FIDELITY",g["review_level"])
        self.assertEqual(load("COUNTS.json")["accepted_new_documentary_records"],0)
    def test_p389_reverse_map_revised_for_page_seam(self):
        j=load("independent_review/REVERSE_SOURCE_TO_RECORD_P389_U70_20261015.json")
        self.assertEqual(j["source_phrase_count"],28)
        self.assertEqual(j["mapped_unique_record_count"],24)
        self.assertEqual(j["mapped_provisional_record_numbers"],list(range(2714,2738)))
        self.assertEqual(j["source_to_record"][0]["record_numbers"],[2714])
        self.assertEqual(j["supersedes_map_sha256"],"3f4715da0a02ccdfbe28a12dbcfc9506217175f3cef1852e0a032ee56422ab51")
        self.assertFalse(j["diplomatic_character_for_character_completeness_certified"])
if __name__=="__main__":unittest.main()
