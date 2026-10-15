"""Verify local historical-documentary acceptance candidate, without runtime promotion.
Does not treat the source statements as prediction validation or crime evidence.
"""
from pathlib import Path
import hashlib,json,unittest
B=Path(__file__).resolve().parent
def j(name):return json.loads((B/name).read_text())
def h(name):return hashlib.sha256((B/name).read_bytes()).hexdigest()
A=j("ACCEPTANCE_CANDIDATE.json")
R=j("RULES.json")
U=j("UNRESOLVED.json")
C=j("CLAIM_LEDGER.json")
O=j("SOURCE_ORDER.json")
D=j("RULES_DRAFT.json")
class DocumentaryAdmission(unittest.TestCase):
 def test_accepted_source_is_documentary_only(self):
  self.assertTrue(R["documentary_accepted_locally"])
  self.assertFalse(R["accepted_as_empirical_astro_prediction"])
  self.assertFalse(R["fully_diplomatic_second_reader_completed"])
  self.assertTrue(R["whole_chapter_l_complete_at_documentary_source_level"])
  self.assertEqual(R["status"],"HISTORICAL_SOURCE_DOCUMENTARY_ONLY_ADMITTED_LOCALLY_CANONICAL_PUBLICATION_PENDING")
 def test_contiguous_402_source_units(self):
  self.assertEqual(R["record_count"],402)
  self.assertEqual([x["record_number"] for x in R["rules"]],list(range(2573,2975)))
  self.assertEqual([x["id"] for x in R["rules"]],[x["id"] for x in D["records"]])
  self.assertEqual(R["rules"],D["records"])
 def test_provenance_and_exact_scope(self):
  self.assertEqual(R["source_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
  self.assertEqual(R["source_pages"],list(range(381,401)))
  self.assertEqual(R["errata_original_pdf_page"],888)
  self.assertEqual(R["rules"][-1]["source_record_kind"],"chapter_li_boundary")
  self.assertIn("divider",R["rules"][-1]["source_statement"])
 def test_no_scientific_crime_person_or_clinical_promotion(self):
  self.assertEqual(C["independent_crime_cases"],0)
  self.assertEqual(C["independent_people_identifications"],0)
  self.assertEqual(C["empirical_predictive_outcomes"],0)
  self.assertFalse(C["clinical_or_criminal_uses_authorized"])
  self.assertEqual(C["runtime_promotions"],0)
  for r in R["rules"]:
   self.assertTrue(r["source_witness_only"])
   self.assertFalse(r["case_evidence_countable"])
   self.assertFalse(r["independently_authenticated_outcome"])
   self.assertFalse(r["prospective_blinded_prediction"])
   self.assertFalse(r["clinical_or_criminal_efficacy_verified"])
   self.assertEqual(r["runtime_status"],"REFERENCE_ONLY_NOT_PROMOTED")
 def test_prior_canonical_unchanged_until_publication(self):
  idx=j("RETAINED_LILLY_INDEX_BEFORE.json")
  self.assertEqual(idx["records_count"],2572)
  self.assertEqual(idx["batches"][-1]["id"],"B02u")
  self.assertEqual(idx["next"]["pdf_page"],381)
  self.assertNotIn(50,idx["read_numbered_chapters"])
  self.assertFalse(A["canonical_record_index_updated"])
 def test_source_order_and_cross_page(self):
  self.assertEqual(O["source_order_record_ids"],list(range(2573,2975)))
  self.assertEqual(len(O["sections"]),49)
  self.assertEqual(len(O["source_pages"]),20)
  self.assertEqual(len(O["two_page_locators"]),11)
  self.assertEqual(len([x for x in O["two_page_locators"] if x["page_role"].startswith("LITERAL")]),9)
 def test_three_independent_original_table_transcriptions(self):
  t=j("PRINTED_DIRECTION_TABLES.json")
  self.assertEqual([len(x["rows"]) for x in t["original_table_witnesses"]],[12,12,12])
  self.assertEqual([x["source_pdf_page"] for x in t["original_table_witnesses"]],[398,399,399])
  self.assertNotEqual(t["original_table_witnesses"][1]["rows"],t["original_table_witnesses"][2]["rows"])
  self.assertFalse(A["source_diplomatic_100percent_verbatim_or_independent"])
 def test_original_images_verified_and_glyph_retained(self):
  manifest=j("SOURCE_IMAGE_MANIFEST.json")
  self.assertEqual(len(manifest["images"]),21)
  for x in manifest["images"]:
   self.assertEqual(h(x["path"]),x["sha256"])
  self.assertTrue(j("SOURCE_REPLAY_RECEIPT.json")["all_source_image_renders_replayed_rgb_identical"])
  self.assertFalse(j("ERRATA_COLLATION.json")["candidate_in_scope"][0]["read_word_or_glyph_verified"])
 def test_source_first_finite_pass(self):
  v=j("independent_review/FINITE_HIGH_RISK_SOURCE_PASS_U75_20261015.json")
  self.assertEqual(len(v["inspected_pages"]),10)
  self.assertEqual(v["identified_material_correction"]["issue"],"U75")
  self.assertEqual(v["three_original_direction_tables"]["normalized_table_row_counts"],[12,12,12])
  self.assertEqual(v["decision"],"RECOMMEND_SOURCE_DOCUMENTARY_ONLY_ADMISSION_WITH_RETAINED_UNCERTAINTIES")
 def test_reverse_original_normalized_420(self):
  rev=j("independent_review/REVERSE_SOURCE_COVERAGE_20P_U75_20261015.json")
  self.assertEqual(rev["source_reverse_pages_mapped"],20)
  self.assertEqual(rev["normalized_anchor_count"],420)
  self.assertEqual(rev["distinct_candidate_record_ids_mapped"],402)
  self.assertFalse(rev["original_to_record_exhaustiveness_proved"])
  self.assertEqual(rev["current_source_draft_sha256"],h("RULES_DRAFT.json"))
 def test_source_issues_and_u75_branch(self):
  self.assertEqual(U["retained_count"],75)
  self.assertEqual(U["issues"][-1]["id"],"U75")
  self.assertIn("Moon's domicile applying to the Moon",R["rules"][2769-2573]["source_statement"])
  self.assertFalse(j("RULES_DRAFT.json")["accepted"])
 def test_claims_and_candidate_contents_hashes(self):
  self.assertEqual(A["source_rule_sha256"],h("RULES.json"))
  self.assertEqual(A["source_order_sha256"],h("SOURCE_ORDER.json"))
  self.assertEqual(A["unresolved_sha256"],h("UNRESOLVED.json"))
  self.assertEqual(A["claim_ledger_sha256"],h("CLAIM_LEDGER.json"))
  self.assertTrue(A["accepted_as_documentary_only_locally"])
  self.assertFalse(A["nonforce_published_remote"])
if __name__=="__main__":unittest.main()
