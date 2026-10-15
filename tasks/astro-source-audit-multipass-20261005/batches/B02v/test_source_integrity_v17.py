"""U74 source-only checks for four new physical page seams and qualifiers.

Historical snapshot fixtures remain unchanged. This suite tests exact source
locators, preserved bytes and bounded maps, not independently complete text.
"""
import hashlib,json,unittest
import test_source_integrity_v16 as prev
B=prev.B
P=prev.P
def load(x):return json.loads((B/x).read_text())
def digest(x):return hashlib.sha256((B/x).read_bytes()).hexdigest()
class CurrentV17(prev.CurrentV16):
    def test_unresolved_53_and_unique_ids(self):
        u=load("UNRESOLVED_DRAFT.json")
        self.assertEqual(u["retained_count"],74)
        self.assertEqual(len(u["issues"]),74)
        self.assertEqual(len({x["id"] for x in u["issues"]}),74)
        self.assertEqual([x["id"] for x in u["issues"][-4:]],["U71","U72","U73","U74"])
    def test_original_p351_p353_physical_source_continuations(self):
        for record,expect in [(2655,[385,386]),(2674,[386,387])]:
            self.assertEqual(P[record]["source_locator"]["pdf_pages"],expect)
        self.assertIn("LEO",P[2674]["source_statement"])
        self.assertIn("Venus",P[2674]["preconditions"][0])
        self.assertFalse(P[2674]["case_evidence_countable"])
    def test_quoted_haly_not_lilly(self):
        a=P[2674]
        b=P[2675]
        self.assertEqual(a["source_record_kind"],"reported_haly_leo_venus_example_start")
        self.assertEqual(b["source_record_kind"],"reported_haly_leo_venus_bed")
        self.assertIn("Haly",a["source_statement"])
        self.assertIn("Haly",b["source_statement"])
        self.assertIn("LEO",a["source_statement"])
        self.assertIn("Leo",b["source_statement"])
        self.assertEqual(a["source_locator"]["pdf_pages"],[386,387])
        self.assertEqual(b["source_locator"]["pdf_pages"],[387])
    def test_original_p357_p359_source_continuations_and_soft_modifier(self):
        self.assertEqual(P[2770]["source_locator"]["pdf_pages"],[391,392])
        self.assertIn("all these signify recovery",P[2770]["source_statement"])
        self.assertEqual(P[2793]["source_locator"]["pdf_pages"],[392,393])
        self.assertEqual(P[2794]["source_record_kind"],"second_exaltation_especially_other_testimony")
        self.assertIn("ESPECIALLY",P[2794]["source_statement"])
        self.assertIn("not another independent",P[2794]["source_statement"])
        self.assertIn("IF PRESENT",P[2794]["preconditions"][0])
        self.assertFalse(P[2794]["prospective_blinded_prediction"])
    def test_prior_producers_frozen_exact(self):
        expected={
        "recovery/producer_p385_387_before_U71_U72_20261015.json":"a963f7bb71f51da0021134d7c45f189ce8f2b201f202b02e77cb9ec003597a91",
        "recovery/producer_p391_392_pre_U73_U74_20261015.json":"93846bf7990d590f28431498bcbd8b88747fc31dcd16d5faeeba2602b1fac4de",
        "recovery/producer_p393_395_pre_U73_U74_20261015.json":"0b248e902436b3f764b8087d600e03c0d00379b6ef789fd130bd09bf4ec31b6a"}
        for name,hash in expected.items():self.assertEqual(digest(name),hash)
    def test_source_order_index_is_a_partition_not_claim_of_completeness(self):
        j=load("SOURCE_ORDER_DRAFT.json")
        self.assertEqual(len(j["cross_page_source_units"]),11)
        self.assertEqual([x["record"] for x in j["cross_page_source_units"]],[2579,2597,2631,2632,2633,2655,2674,2714,2737,2770,2793])
        self.assertEqual(len([x for x in j["cross_page_source_units"] if x["page_role"]=="LITERAL_PRINTED_CLAUSE_CONTINUES_OVER_LEAF"]),9)
        self.assertEqual(j["provisional_source_units"],402)
        self.assertFalse(j["numbered_chapter_L_completed_and_accepted"])
        for name,expected in j["upstream_sha256"].items():self.assertEqual(digest(name),expected)
    def test_reverse_coverage_14_of_20_pages(self):
        j=load("independent_review/REVERSE_SOURCE_COVERAGE_U74_20261015.json")
        self.assertEqual(j["source_bounded_reverse_page_count"],14)
        self.assertEqual(j["source_anchor_count"],289)
        self.assertEqual(j["distinct_provisional_records_reverse_mapped"],272)
        self.assertEqual(j["records_not_yet_reverse_mapped"],list(range(2816,2946)))
        self.assertEqual(j["remaining_reverse_page_ids"],list(range(394,400)))
        self.assertEqual(len(j["repeat_page_reference_ids"]),11)
        self.assertFalse(j["source_reverse_completeness_proved"])
        self.assertFalse(j["source_independent_reviewer"])
    def test_new_reverse_maps_source_image_identity(self):
        j=load("independent_review/REVERSE_SOURCE_COVERAGE_U74_20261015.json")
        im={x["pdf_page"]:x for x in load("SOURCE_IMAGE_MANIFEST.json")["images"]}
        for e in j["source_pages"]:
            self.assertEqual(digest(e["map_path"]),e["map_sha256"])
            self.assertEqual(digest(im[e["original_pdf_page"]]["path"]),im[e["original_pdf_page"]]["sha256"])
            self.assertTrue(all(n in P for n in e["record_ids"]))
    def test_bounded_402_source_records_review_map_exact(self):
        j=load("independent_review/REVIEW_COVERAGE_CONSERVATIVE_U74_20261015.json")
        self.assertEqual(j["distinct_bounded_review_records"],402)
        self.assertEqual([x["included_source_record_count"] for x in j["past_review_sets"]],[103,109,65,149])
        self.assertEqual([len(x["records_new_to_prior_groups"]) for x in j["past_review_sets"]],[103,109,43,147])
        self.assertEqual(j["draft_sha256"],digest("RULES_DRAFT.json"))
        for group in j["past_review_sets"]:
            for doc in group["review_evidence_documents"]:
                self.assertTrue((B/doc).is_file(),doc)
        self.assertFalse(j["source_independent_fidelity_review_completed"])
        self.assertFalse(j["chapter_L_source_complete"])
    def test_all_review_documents_exist_and_coverage_not_exaggerated(self):
        j=load("independent_review/REVERSE_SOURCE_COVERAGE_U74_20261015.json")
        self.assertEqual(len(j["source_pages"]),14)
        self.assertEqual(len(j["distinct_reverse_mapped_record_ids"]),272)
        self.assertEqual(load("COUNTS.json")["accepted_new_documentary_records"],0)
if __name__=="__main__":unittest.main()
