"""V14 source-only verification of p366 printed sequence and U68.

Inherits V13 for the U66/U67 p355→356 findings while leaving historical
fixtures unchanged. These tests are NOT independent source completeness.
"""
import hashlib,json,unittest
import test_source_integrity_v13 as old
B=old.B
P=old.P
def load(p):return json.loads((B/p).read_text())
def digest(p):return hashlib.sha256((B/p).read_bytes()).hexdigest()
class CurrentV14(old.CurrentV13):
    def test_unresolved_53_and_unique_ids(self):
        j=load("UNRESOLVED_DRAFT.json")
        self.assertEqual(len(j["issues"]),68)
        self.assertEqual(j["retained_count"],68)
        self.assertEqual(len({x["id"] for x in j["issues"]}),68)
        self.assertEqual([x["id"] for x in j["issues"][-3:]],["U66","U67","U68"])
    def test_p366_printed_sequence_restored(self):
        a=P[2971]
        b=P[2972]
        self.assertEqual(a["source_record_kind"],"other_capture_moon_squares_from_saturn_to_mercury")
        self.assertEqual(b["source_record_kind"],"other_capture_seventh_first")
        self.assertEqual(a["source_locator"]["pdf_pages"],[400])
        self.assertEqual(b["source_locator"]["pdf_pages"],[400])
        self.assertIn("BEFORE",a["source_statement"])
        self.assertIn("After the lunar",b["source_statement"])
        self.assertIn("unresolved",b["source_statement"])
        self.assertFalse(a["case_evidence_countable"])
        self.assertFalse(b["prospective_blinded_prediction"])
    def test_before_U68_source_exact_and_original_page(self):
        self.assertEqual(digest("recovery/producer_p398_400_before_U68_capture_order_20261015.json"),
                         "65da647d9e23ae4524c71071cdb12df56569fa2b0ab5a462fe7c5ccb5d641b19")
        m=load("SOURCE_IMAGE_MANIFEST.json")
        page=next(x for x in m["images"] if x["pdf_page"]==400)
        self.assertEqual(digest(page["path"]),page["sha256"])
    def test_reverse_original_page400_exact_ordinal(self):
        j=load("independent_review/REVERSE_SOURCE_TO_RECORD_P400_20261015.json")
        self.assertEqual(j["printed_page"],366)
        self.assertEqual(j["source_clause_entries"],29)
        self.assertEqual(j["unique_provisional_records"],29)
        self.assertEqual(j["print_sequence_record_ids"],list(range(2946,2975)))
        self.assertEqual([x["record_number"] for x in j["source_to_record"]],list(range(2946,2975)))
        self.assertEqual(j["unmapped_definite_source_clauses"],[])
        self.assertFalse(j["diplomatic_completeness_confirmed"])
        self.assertFalse(j["reviewer_separated_from_producer"])
    def test_bounded_402_source_records_review_map_exact(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U68_20261015.json")
        self.assertEqual(j["distinct_bounded_review_records"],402)
        self.assertEqual(j["unique_record_ids_in_bounded_review_evidence"],list(range(2573,2975)))
        self.assertEqual(j["records_without_documented_finite_page_specific_check_in_four_review_groups"],[])
        self.assertEqual([len(x["records_new_to_prior_groups"]) for x in j["past_review_sets"]],[103,109,43,147])
        self.assertEqual(j["draft_sha256"],digest("RULES_DRAFT.json"))
        self.assertFalse(j["source_independent_fidelity_review_completed"])
        self.assertFalse(j["chapter_L_source_complete"])
    def test_all_review_documents_exist_and_coverage_not_exaggerated(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U68_20261015.json")
        for group in j["past_review_sets"]:
            for p in group["review_evidence_documents"]:self.assertTrue((B/p).is_file(),p)
            self.assertIn("NOT_VERBATIM_FULL_FIDELITY",group["review_level"])
        self.assertFalse(load("RULES_DRAFT.json")["accepted"])
        self.assertEqual(load("COUNTS.json")["accepted_new_documentary_records"],0)
if __name__=="__main__":unittest.main()
