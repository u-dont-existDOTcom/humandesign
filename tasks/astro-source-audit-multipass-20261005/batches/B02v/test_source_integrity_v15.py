"""V15 source-only checks for U69 Moon goods page-break and bounded reverse map.

V14 remains immutable for historical U68 archive. Green tests only show
mechanical source consistency and selected image-grounded repairs.
"""
import hashlib,json,unittest
import test_source_integrity_v14 as prev
B=prev.B
P=prev.P
def load(p): return json.loads((B/p).read_text())
def digest(p): return hashlib.sha256((B/p).read_bytes()).hexdigest()
class CurrentV15(prev.CurrentV14):
    def test_unresolved_53_and_unique_ids(self):
        u=load("UNRESOLVED_DRAFT.json")
        self.assertEqual(u["retained_count"],69)
        self.assertEqual(len(u["issues"]),69)
        self.assertEqual(len({x["id"] for x in u["issues"]}),69)
        self.assertEqual([x["id"] for x in u["issues"][-4:]],["U66","U67","U68","U69"])
    def test_second_lord_moon_quality_spans_leaf(self):
        r=P[2714]
        self.assertEqual(r["source_record_kind"],"quality_second_moon_country_beasts")
        self.assertEqual(r["source_locator"]["pdf_pages"],[388,389])
        self.assertEqual(r["source_locator"]["printed_pages"],[354,355])
        self.assertIn("poultry",r["source_statement"])
        self.assertIn("Coun-",r["preconditions"][0])
        self.assertFalse(r["case_evidence_countable"])
    def test_before_u69_source_frozen(self):
        self.assertEqual(digest("recovery/producer_p388_390_before_U69_p354_20261015.json"),
            "03f4f73820d57d296b2264e1e1619608dd536deb521ac6b25cb90a67fbf124e9")
        for p in (388,389):
            src=next(x for x in load("SOURCE_IMAGE_MANIFEST.json")["images"] if x["pdf_page"]==p)
            self.assertEqual(digest(src["path"]),src["sha256"])
    def test_source_order_index_is_a_partition_not_claim_of_completeness(self):
        j=load("SOURCE_ORDER_DRAFT.json")
        self.assertEqual(j["source_page_count"],20)
        self.assertEqual(j["provisional_source_units"],402)
        self.assertEqual(j["editorial_section_marker_count"],49)
        self.assertEqual(sum(x["editorial_record_count"] for x in j["sections"]),402)
        self.assertFalse(j["numbered_chapter_L_completed_and_accepted"])
        a=j["cross_page_source_units"]
        self.assertEqual([x["record"] for x in a],[2579,2597,2631,2632,2633,2714,2737])
        self.assertEqual([x["record"] for x in a if x["page_role"]=="LITERAL_PRINTED_CLAUSE_CONTINUES_OVER_LEAF"],[2579,2597,2633,2714,2737])
        for key,v in j["upstream_sha256"].items():
            self.assertEqual(digest(key),v)
    def test_bounded_402_source_records_review_map_exact(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U69_20261015.json")
        self.assertEqual(j["unique_record_ids_in_bounded_review_evidence"],list(range(2573,2975)))
        self.assertEqual(j["distinct_bounded_review_records"],402)
        self.assertEqual(j["remaining_original_pdf_pages_for_this_specific_scope"],[])
        self.assertEqual(j["records_without_documented_finite_page_specific_check_in_four_review_groups"],[])
        self.assertEqual([x["included_source_record_count"] for x in j["past_review_sets"]],[103,109,64,148])
        self.assertEqual([len(x["records_new_to_prior_groups"]) for x in j["past_review_sets"]],[103,109,43,147])
        self.assertEqual(j["draft_sha256"],digest("RULES_DRAFT.json"))
        self.assertFalse(j["chapter_L_source_complete"])
        self.assertFalse(j["source_independent_fidelity_review_completed"])
    def test_all_review_documents_exist_and_coverage_not_exaggerated(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U69_20261015.json")
        for x in j["past_review_sets"]:
            for path in x["review_evidence_documents"]:self.assertTrue((B/path).is_file(),path)
            self.assertIn("NOT_VERBATIM_FULL_FIDELITY",x["review_level"])
        self.assertEqual(load("COUNTS.json")["accepted_new_documentary_records"],0)
    def test_reverse_printed_p353_clause_map(self):
        j=load("independent_review/REVERSE_SOURCE_TO_RECORD_P387_20261015.json")
        self.assertEqual(j["original_pdf_page"],387)
        self.assertEqual(j["printed_page"],353)
        self.assertEqual(j["records_order"],list(range(2675,2694)))
        self.assertEqual(j["count_source_unit_ids"],19)
        self.assertFalse(j["source_full_completeness_verified"])
        self.assertFalse(j["independent_reviewer"])
if __name__=="__main__":unittest.main()
