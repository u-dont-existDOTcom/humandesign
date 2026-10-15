"""V12 source-only checks for U65 and conservative 402/402 page review coverage.

Proves source-image identities and actual reviewed record-ID coverage, NOT
independent historical text completeness or real predictive validity.
"""
import hashlib,json,unittest
import test_source_integrity_v11 as previous
B=previous.B
P=previous.P

class CurrentV12(previous.CurrentV11):
    def test_unresolved_53_and_unique_ids(self):
        j=json.loads((B/"UNRESOLVED_DRAFT.json").read_text())
        self.assertEqual(len(j["issues"]),65)
        self.assertEqual(j["retained_count"],65)
        self.assertEqual(len({x["id"] for x in j["issues"]}),65)
        self.assertEqual([x["id"] for x in j["issues"][-5:]],["U61","U62","U63","U64","U65"])
    def test_p366_non_capture_aspect_not_only_house(self):
        r=P[2948]
        q=P[2949]
        self.assertEqual(r["source_record_kind"],"not_taken_lord7_aspects_venus_jupiter_eleven_friends")
        self.assertEqual(q["source_record_kind"],"not_taken_lord7_aspects_benefic_third_strangers")
        self.assertIn("seventh lord aspects",r["source_statement"])
        self.assertIn("precondition",r["source_statement"])
        self.assertIn("seventh-lord/benefic aspect",q["source_statement"])
        self.assertIn("elliptical",q["source_statement"])
        self.assertEqual(r["source_locator"]["pdf_pages"],[400])
        self.assertEqual(q["source_locator"]["pdf_pages"],[400])
        self.assertFalse(r["case_evidence_countable"])
        self.assertFalse(q["prospective_blinded_prediction"])
    def test_original_before_u65_bytes(self):
        f=B/"recovery/producer_p398_400_pre_U65_20261015.json"
        self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),"1bd3fa93a7ad49c15aba88d5f5e1102a7d8dc299fc69f44a30cea6b401bf042f")
        manifest=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
        image=next(x for x in manifest["images"] if x["pdf_page"]==400)
        self.assertEqual(hashlib.sha256((B/image["path"]).read_bytes()).hexdigest(),image["sha256"])
    def test_bounded_402_source_records_review_map_exact(self):
        j=json.loads((B/"independent_review/REVIEW_COVERAGE_CONSERVATIVE_U65_20261015.json").read_text())
        self.assertEqual(j["distinct_bounded_review_records"],402)
        self.assertEqual(j["unique_record_ids_in_bounded_review_evidence"],list(range(2573,2975)))
        self.assertEqual(len(j["records_without_documented_finite_page_specific_check_in_four_review_groups"]),0)
        self.assertEqual(j["remaining_original_pdf_pages_for_this_specific_scope"],[])
        self.assertEqual([r["included_source_record_count"] for r in j["past_review_sets"]],[103,109,64,147])
        self.assertEqual([len(r["records_new_to_prior_groups"]) for r in j["past_review_sets"]],[103,109,43,147])
        self.assertEqual(j["draft_sha256"],hashlib.sha256((B/"RULES_DRAFT.json").read_bytes()).hexdigest())
        self.assertFalse(j["source_independent_fidelity_review_completed"])
        self.assertFalse(j["chapter_L_source_complete"])
    def test_all_review_documents_exist_and_coverage_not_exaggerated(self):
        j=json.loads((B/"independent_review/REVIEW_COVERAGE_CONSERVATIVE_U65_20261015.json").read_text())
        for grp in j["past_review_sets"]:
            for doc in grp["review_evidence_documents"]:
                self.assertTrue((B/doc).is_file(),doc)
            self.assertIn("NOT_VERBATIM_FULL_FIDELITY",grp["review_level"])
        s=json.loads((B/"COUNTS.json").read_text())
        self.assertEqual(s["accepted_lilly_before"],2572)
        self.assertEqual(s["accepted_new_documentary_records"],0)
if __name__=="__main__":unittest.main()
