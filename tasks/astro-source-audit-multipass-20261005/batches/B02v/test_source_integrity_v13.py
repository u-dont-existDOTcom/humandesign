"""V13 source-only checks for U66–U67 and printed page355→356 reverse audit.

Historical original-page evidence only. No independent word-for-word audit,
actual stolen-property case, or empirical predictive validation is implied.
Earlier V12 fixture remains intact for the U65 snapshot.
"""
import hashlib,json,unittest
import test_source_integrity_v12 as old
B=old.B
P=old.P
def file(name):return json.loads((B/name).read_text())
def digest(name):return hashlib.sha256((B/name).read_bytes()).hexdigest()

class CurrentV13(old.CurrentV12):
    def test_unresolved_53_and_unique_ids(self):
        j=file("UNRESOLVED_DRAFT.json")
        self.assertEqual(j["retained_count"],67)
        self.assertEqual(len(j["issues"]),67)
        self.assertEqual(len({x["id"] for x in j["issues"]}),67)
        self.assertEqual([x["id"] for x in j["issues"][-2:]],["U66","U67"])
    def test_sun_to_ruler_and_rulers_to_sun_both_retained(self):
        r=P[2735]
        self.assertEqual(r["source_record_kind"],"sun_house_ruler_application_bidirectional_textual_ambiguity")
        self.assertIn("Sun applying to the lord",r["source_statement"])
        self.assertIn("applying TO the Sun",r["source_statement"])
        self.assertIn("goods will be found",r["source_statement"])
        self.assertIn("direction",r["exceptions_and_evidence_limits"][0])
        self.assertEqual(r["source_locator"]["pdf_pages"],[389])
        self.assertFalse(r["case_evidence_countable"])
    def test_opening_p355_consequent_p356_cross_leaf(self):
        r=P[2737]
        self.assertEqual(r["source_record_kind"],"recover_first_to_lord_of_lost")
        self.assertEqual(r["source_locator"]["pdf_pages"],[389,390])
        self.assertEqual(r["source_locator"]["printed_pages"],[355,356])
        self.assertIn("unto the Lord of the Ascendant",r["source_statement"])
        self.assertIn("recovered",r["source_statement"])
        self.assertFalse(r["prospective_blinded_prediction"])
    def test_exact_originals_and_sources(self):
        self.assertEqual(digest("recovery/producer_p388_390_before_U66_p355_20261015.json"),
         "fce4b68c4397e1e27b8c9ca6278a65143a56bb17bc15e95388865253bad3f04d")
        self.assertEqual(digest("recovery/producer_p388_390_before_U67_20261015.json"),
         "8a7662cc709c540ec61008ba23c92c01c5f81cdac9adb2a5af9fe381c483d439")
        for p in [389,390]:
            e=next(x for x in file("SOURCE_IMAGE_MANIFEST.json")["images"] if x["pdf_page"]==p)
            self.assertEqual(digest(e["path"]),e["sha256"])
    def test_reverse_p389_literal_clause_coverage(self):
        j=file("independent_review/REVERSE_SOURCE_TO_RECORD_P389_20261015.json")
        self.assertEqual(j["printed_page"],355)
        self.assertEqual(j["source_phrase_count"],27)
        self.assertEqual(j["mapped_unique_record_count"],23)
        self.assertEqual(j["mapped_provisional_record_numbers"],list(range(2715,2738)))
        self.assertEqual(len(j["source_to_record"]),27)
        self.assertEqual(j["unmapped_definite_source_clauses"],[])
        self.assertTrue(all(x["record_numbers"][0] in P for x in j["source_to_record"]))
        self.assertFalse(j["independent_blinded_reviewer"])
        self.assertFalse(j["diplomatic_character_for_character_completeness_certified"])
    def test_source_order_index_is_a_partition_not_claim_of_completeness(self):
        j=file("SOURCE_ORDER_DRAFT.json")
        self.assertEqual(j["provisional_source_units"],402)
        self.assertEqual(j["source_page_count"],20)
        self.assertEqual(j["editorial_section_marker_count"],49)
        self.assertEqual(j["sections"][-1]["end_record"],2974)
        self.assertFalse(j["numbered_chapter_L_completed_and_accepted"])
        crosses=j["cross_page_source_units"]
        self.assertEqual(len(crosses),6)
        self.assertEqual([x["record"] for x in crosses],[2579,2597,2631,2632,2633,2737])
        self.assertEqual([x["record"] for x in crosses if x["page_role"]=="LITERAL_PRINTED_CLAUSE_CONTINUES_OVER_LEAF"],[2579,2597,2633,2737])
        for name,d in j["upstream_sha256"].items():self.assertEqual(digest(name),d)
    def test_bounded_402_source_records_review_map_exact(self):
        j=file("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U67_20261015.json")
        self.assertEqual(j["distinct_bounded_review_records"],402)
        self.assertEqual(j["unique_record_ids_in_bounded_review_evidence"],list(range(2573,2975)))
        self.assertEqual(j["records_without_documented_finite_page_specific_check_in_four_review_groups"],[])
        self.assertEqual(j["remaining_original_pdf_pages_for_this_specific_scope"],[])
        self.assertEqual([x["included_source_record_count"] for x in j["past_review_sets"]],[103,109,64,147])
        self.assertEqual(j["draft_sha256"],digest("RULES_DRAFT.json"))
        self.assertFalse(j["source_independent_fidelity_review_completed"])
        self.assertFalse(j["chapter_L_source_complete"])
    def test_all_review_documents_exist_and_coverage_not_exaggerated(self):
        j=file("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U67_20261015.json")
        for g in j["past_review_sets"]:
            for p in g["review_evidence_documents"]:self.assertTrue((B/p).is_file(),p)
            self.assertIn("NOT_VERBATIM_FULL_FIDELITY",g["review_level"])
        self.assertEqual(file("COUNTS.json")["accepted_new_documentary_records"],0)
        self.assertFalse(file("RULES_DRAFT.json")["accepted"])
if __name__=="__main__":unittest.main()
