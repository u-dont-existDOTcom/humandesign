"""Image-first A1/A2/B/C/D source fidelity guards: historical print, not forecast validation."""
from pathlib import Path
import json,unittest,hashlib
B=Path(__file__).resolve().parent
R={x["record_number"]:x for x in json.loads((B/"RULES.json").read_text())["rules"]}
def t(n):return " ".join([R[n]["source_statement"]]+R[n]["preconditions"]+R[n]["exceptions_and_evidence_limits"]).lower()
class SourceOriginalCorrections(unittest.TestCase):
 def test_hour_not_fourth_lord_radicality(self):
  self.assertIn("hour",t(2319));self.assertIn("seventh",t(2319))
  self.assertNotIn("lord of fourth",R[2319]["source_statement"].lower())
 def test_suspicion_condition_is_separate(self):
  self.assertIn("fidelity",t(2572))
  self.assertIn("chief",t(2572))
  self.assertNotIn("hour-lord identity",R[2572]["source_statement"])
 def test_correct_historical_margin_word(self):
  self.assertIn("consentanious",t(2322))
  self.assertIn("consonant",t(2322))
  self.assertIn("not",t(2322))
 def test_discovery_not_guaranteed_recovery(self):
  self.assertIn("discovery",t(2327))
  self.assertIn("hope",t(2327))
  self.assertIn("not equivalent",t(2327))
 def test_original_page_turn_his_lord_antecedent(self):
  self.assertEqual(R[2330]["source_locator"]["pdf_pages"],[365,366])
  self.assertIn("antecedent",t(2330))
 def test_unequal_glyph_readings_unresolved(self):
  self.assertIn("opposition",t(2338))
  self.assertIn("conjunction",t(2338))
  self.assertIn("second house",t(2338))
  self.assertIn("unresolved",t(2338))
 def test_sun_second_lord_in_tenth(self):
  self.assertIn("tenth",t(2339))
  self.assertIn("sun",t(2339))
  self.assertIn("no invented sextile",t(2339))
 def test_venus_in_tenth_sign_tenth_moon_opposite(self):
  s=t(2343)
  for x in ("venus","tenth","moon","opposition"):self.assertIn(x,s)
  self.assertIn("tenth sign",s)
 def test_other_jest_rule_moon_opposes(self):
  self.assertIn("opposes",t(2345))
  self.assertIn("twelfth",t(2345))
  self.assertIn("sextile",t(2345))
 def test_scant_not_soon(self):
  self.assertIn("scant",t(2347))
  self.assertIn("scarcely",t(2347))
 def test_fifth_house_returned(self):
  self.assertIn("fifth",t(2392))
  self.assertIn("eleventh",t(2392))
  self.assertIn("second",t(2392))
 def test_no_self_aspect_in_future_theft(self):
  s=t(2393)
  self.assertIn("actor",s)
  self.assertIn("not securely",s)
 def test_name_venus_second_glyph(self):
  self.assertIn("venus",t(2475))
  self.assertIn("saturn",t(2475))
 def test_moon_ninth_conjunction_not_sextile(self):
  s=R[2499]["source_statement"].lower()
  self.assertIn("conjunction",s)
  self.assertIn("square",s)
  self.assertIn("opposition",s)
  self.assertNotIn("sextile",s)
 def test_second_house_power_not_membership(self):
  self.assertIn("power of the loser",t(2511))
  self.assertIn("money",t(2511))
 def test_neighbor_actor_or_means(self):
  self.assertIn("neighbor",t(2523))
  self.assertIn("or his mean",t(2523))
 def test_margin_not_retrofit_body(self):
  self.assertIn("reach",t(2551))
  self.assertIn("not established",t(2551))
  self.assertIn("sometimes",t(2552))
 def test_original_section_scope_pdf381(self):
  x=json.loads((B/"NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json").read_text())
  self.assertIn("BEFORE",x["phase_current_stop"])
  self.assertIn("house",x["unextracted_next_phase_sections_pdf381"][0].lower())
  self.assertIn("door",str(x).lower())
 def test_handwritten_annotations_not_print(self):
  x=json.loads((B/"ORIGINAL_MARGINALIA_REGISTER.json").read_text())
  self.assertTrue(x["not_new_aphorisms_or_human_cases"])
  self.assertEqual(len(x["items"]),8)
 def test_corrupted_errata_unresolved(self):
  x=json.loads((B/"ERRATA_COLLATION.json").read_text())
  self.assertTrue(any(z.get("printed_page") is None for z in x["original_printed_errata_entries"]))
  self.assertTrue(x["p330_instruction_belongs_to_prior_accepted_batch"])
 def test_append_only_id_source_order(self):
  ids=json.loads((B/"SOURCE_ORDER.json").read_text())["source_order_record_ids"]
  self.assertEqual(ids[ids.index(2319)+1],2572)
  self.assertEqual(len(ids),len(set(ids)))
 def test_two_table_images_without_diplomatic_pretence(self):
  x=json.loads((B/"TABLE_WITNESS_REGISTER.json").read_text())
  self.assertEqual(len(x["table_witnesses"]),2)
  self.assertTrue(all(not q["diplomatic_all_cells_checked"] for q in x["table_witnesses"]))
 def test_completed_independent_review_receipts(self):
  for window in ("A1","A2","B","C","D"):
   x=json.loads((B/"independent_review"/f"OPUS_{window}_INITIAL.json").read_text())
   self.assertEqual(x.get("status",x.get("verdict")),"FINDS_ERROR")
 def test_records_not_empirically_validated(self):
  self.assertEqual(len(R),267)
  self.assertTrue(all(not x["verified_crime_identification"] and
                      not x["prospective_frozen_prediction"] and
                      not x["independently_authenticated_human_case"] for x in R.values()))
if __name__=="__main__":unittest.main()
