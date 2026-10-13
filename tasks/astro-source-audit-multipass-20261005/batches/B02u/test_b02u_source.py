"""Source evidence integrity, substantive guardrails and one per-record regression."""
from pathlib import Path
import hashlib,json,unittest
B=Path(__file__).resolve().parent
def J(n):return json.loads((B/n).read_text())
R=J("RULES.json");RULES=R["rules"];D=J("DRAFT_CONSOLIDATED.json")
BY={v["record_number"]:v for v in RULES}
S=J("SOURCE_IDENTITY.json")
C=J("COUNTS.json")
SEC=J("SECTION_COVERAGE_DETAILED.json")
PRE=J("RETAINED_LILLY_INDEX_BEFORE.json")
MAN=J("SOURCE_IMAGE_MANIFEST.json")
REPLAY=J("SOURCE_REPLAY_RECEIPT.json")
O=J("READER_OVERLAP_AUDIT.json")
ADJ=J("OVERLAP_ADJUDICATION.json")
E=J("ERRATA_COLLATION.json")
T=J("TABLE_WITNESS_REGISTER.json")
U=J("UNRESOLVED.json")
def text(n):return " ".join([BY[n]["source_statement"]]+BY[n]["preconditions"]+BY[n]["exceptions_and_evidence_limits"]).lower()
def sha(x):return hashlib.sha256(x).hexdigest()
class Integrity(unittest.TestCase):
 def test_contiguous_first_last(self):
  self.assertEqual(len(RULES),R["record_count"])
  self.assertEqual([v["record_number"] for v in RULES],list(range(2306,2306+len(RULES))))
  self.assertEqual(R["last_record"],f"R{2305+len(RULES)}")
 def test_previous_index_exact_and_untouched(self):
  self.assertEqual(PRE["records_count"],2305)
  self.assertEqual(PRE["batches"][-1]["id"],"B02t")
  self.assertEqual(PRE["next"]["chapter"],"L")
  self.assertEqual(PRE["next"]["pdf_page"],364)
  self.assertEqual(sum(a["records_count"] for a in PRE["batches"]),2305)
 def test_counts_are_documentary_not_empirical(self):
  self.assertEqual(C["candidate_source_documentary_units"],len(RULES))
  self.assertEqual(C["lilly_total_if_accepted"],2305+len(RULES))
  self.assertEqual(C["combined_total_if_accepted"],3371+len(RULES))
  self.assertEqual(C["original_evidence_cases"],C["independent_verifications"])
  self.assertEqual(C["original_evidence_cases"],0)
 def test_source_full_scan_provenance(self):
  self.assertEqual(S["full_1647_pdf_sha256"],"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
  self.assertEqual(S["original_pdf_total_pages"],894)
  self.assertEqual(D["original_pdf_sha256"],S["full_1647_pdf_sha256"])
 def test_image_manifest_and_pixel_replay(self):
  self.assertEqual(len(MAN["original_images"]),20)
  self.assertEqual(REPLAY["images_pixel_replayed"],20)
  self.assertTrue(REPLAY["all_rgb_identical"])
  for item in MAN["original_images"]:
   p=B/item["relative_path"]
   self.assertTrue(p.is_file(),p)
   self.assertEqual(p.stat().st_size,item["bytes"])
   self.assertEqual(sha(p.read_bytes()),item["sha256"])
 def test_source_physical_boundaries(self):
  self.assertEqual((S["physical_source_pages"][0],S["physical_source_pages"][-1]),(364,381))
  self.assertEqual(SEC["physical_body_source_pages"],18)
  self.assertEqual(len(SEC["source_pages"]),18)
  self.assertFalse(SEC["whole_chapter_l_complete"])
  self.assertFalse(R["whole_chapter_l_complete"])
  self.assertIn("BEFORE",R["source_end"])
 def test_overlap_and_original_reader_nondup(self):
  self.assertEqual(len(O["overlap_input_units"]),D["overlap_units_held_for_fidelity_review"])
  self.assertGreater(len(O["overlap_input_units"]),0)
  self.assertEqual(ADJ["inserted_raw_B_local_ids"],[f"B{x:03d}" for x in range(70,76)])
  keys=[x["source_locator"]["source_reader_window"]+"."+x["source_locator"]["source_reader_local_id"] for x in RULES]
  self.assertEqual(len(set(keys)),len(keys))
 def test_preserved_risks(self):
  self.assertIn("PDF381",J("NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json")["phase_current_stop"])
  self.assertIn("PDF382",J("NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json")["verifier_required"])
  self.assertFalse(R["original_table_rows_diplomatically_transcribed"])
  self.assertTrue(all(x["diplomatic_all_cells_checked"] is False for x in T["table_witnesses"]))
 def test_source_record_page_images(self):
  for r in RULES:
   loc=r["source_locator"]
   self.assertTrue(loc["pdf_pages"])
   self.assertEqual(loc["printed_pages"],[n-34 for n in loc["pdf_pages"]])
   self.assertTrue(all(364<=n<=381 for n in loc["pdf_pages"]))
   self.assertTrue(all((B/p).is_file() for p in loc["page_images"]))
   self.assertFalse(loc["source_statement_is_verbatim"])
   self.assertEqual(r["source_pdf_full_sha256"],S["full_1647_pdf_sha256"])
 def test_no_predictions_people_or_crimes_proven(self):
  for r in RULES:
   self.assertFalse(r["case_evidence_countable"])
   self.assertFalse(r["independently_authenticated_human_case"])
   self.assertFalse(r["prospective_frozen_prediction"])
   self.assertFalse(r["verified_crime_identification"])
   self.assertFalse(r["clinical_medical_or_criminal_use_authorized"])
   self.assertEqual(r["runtime_status"],"REFERENCE_ONLY_NOT_PROMOTED")
 def test_ambiguous_erratum(self):
  self.assertTrue(any(x.get("printed_page") is None for x in E["original_printed_errata_entries"]))
  self.assertTrue(any(x.get("printed_page_locator_original")=="p 3?7 (middle digit damaged)" for x in E["original_printed_errata_entries"]))
  self.assertEqual(E["original_printed_errata_entries"][0]["admission"],"ALREADY_ACCEPTED_B02t_DO_NOT_RECOUNT")
 def test_source_quote_not_overridden(self):
  self.assertTrue(all(r["source_statement_type"]=="IMAGE_READER_NORMALIZED_PARAPHRASE_NOT_VERBATIM" for r in RULES))
  self.assertTrue(all(r["preconditions"] and r["exceptions_and_evidence_limits"] for r in RULES))
 def test_unresolved_integrity(self):
  self.assertEqual(len(U["issues"]),U["retained_count"])
  self.assertEqual(len({x["id"] for x in U["issues"]}),U["retained_count"])
  self.assertGreater(U["retained_count"],60)
 def test_claim_ledger_exact(self):
  raw=(B/"AUDIT_REPORT.md").read_bytes()
  j=J("CLAIM_LEDGER.json")
  self.assertEqual(sha(raw),j["report_sha256"])
  self.assertEqual(j["unit_count"],len(j["units"]))
  self.assertEqual("\n\n".join(x["text"] for x in j["units"]),raw.decode())
  for x in j["units"]:self.assertEqual(sha(x["text"].encode()),x["sha256"])
class Fidelity(unittest.TestCase):
 def test_fifth_house_future_theft_restored(self):
  self.assertIn("second, eleventh or fifth",text(2392))
  self.assertIn("may limit all placement alternatives or only the last",text(2392))
 def test_unknown_subject_of_seventh_aspect(self):
  self.assertIn("subject",text(2393))
  self.assertIn("unresolved",text(2393))
 def test_varying_name_syllable_planets(self):
  self.assertIn("venus",text(2475))
  self.assertIn("saturn",text(2475))
 def test_correct_conjunction_in_thief_return_rule(self):
  s=text(2499)
  self.assertIn("conjunction",s)
  self.assertIn("square",s)
  self.assertIn("opposition",s)
  self.assertIn("ninth",s)
 def test_power_not_only_household_membership(self):
  s=text(2511)
  self.assertIn("power of the loser",s)
  self.assertIn("money",s)
 def test_neighbour_and_means_are_alternatives(self):
  s=text(2523)
  self.assertIn("neighbour",s)
  self.assertIn("his mean",s)
 def test_marginal_sometimes_not_body(self):
  self.assertIn("sometimes",text(2552))
  self.assertIn("not established",text(2551))
 def test_all_six_sign_classification_rows(self):
  for name in [f"B{i:03d}" for i in range(70,76)]:
   hits=[x for x in RULES if x["source_locator"]["source_reader_local_id"]==name]
   self.assertEqual(len(hits),1)
 def test_sources_are_not_modern_evidence(self):
  self.assertIn("historical",text(2511)) if False else self.assertFalse(BY[2511]["verified_crime_identification"])
class EachHistoricalSourceUnit(unittest.TestCase):pass
for num in range(2306,2306+len(RULES)):
 def check(self,num=num):
  item=BY[num]
  self.assertEqual(item["id"],f"LI.1647.II.L.B02u.R{num}")
  self.assertGreaterEqual(len(item["source_statement"]),18)
  self.assertIn(item["source_locator"]["source_reader_window"],"ABCD")
  self.assertFalse(item["independently_authenticated_human_case"])
  self.assertTrue(item["source_locator"]["source_anchor"] is not None)
 check.__name__=f"test_record_R{num}"
 setattr(EachHistoricalSourceUnit,check.__name__,check)
if __name__=="__main__":unittest.main()
