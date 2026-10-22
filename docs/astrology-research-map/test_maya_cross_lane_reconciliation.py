#!/usr/bin/env python3
"""Assert source/clock/claim/human evidence remain separated across accepted lanes."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,re,unittest
from reconcile_accepted_maya_lanes import build,HERE,ROOT,OUT,LEDGER,ALL_PROVENANCE,PARENTS

def load(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return sha256(p.read_bytes()).hexdigest()

class ReconciledMayaEvidence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cover=load(OUT);cls.ledger=load(LEDGER)
  cls.owner=load(ROOT/"tasks/astro-maya-comparative-map-20261022/MAYA_LOCAL_SOURCE_INVENTORY_V1.json")
  cls.practitioner=load(HERE/"MAYA_FIRST_SOURCE_WITNESS_V1.json")
  cls.folio=load(ROOT/"tasks/astro-maya-dresden-facsimile-page24-20261022/DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json")
  cls.crosswalk=load(ROOT/"tasks/astro-multitradition-source-coverage-20261022/TRADITION_CONSTRUCT_AND_SURVEY_CROSSWALK_V1.json")
  cls.calendar_claim=load(HERE/"CLAIM_TRACE_EXAMPLE_MAYA_E_V1.json")

 def test_deterministic_rebuild_exact_two_json_sha(self):
  original=(sha(OUT),sha(LEDGER))
  build()
  self.assertEqual((sha(OUT),sha(LEDGER)),original)
  self.assertEqual(original,("1a99626ac5af6de94cda71745b28b0cfe02014f2ec8bef477206102decb1b8a6","474fd7557be4973771fb70e7001cb8014d96d68f1f4e7dc80a11e2f15a1e8d3e"))

 def test_original_parent_descriptive_map_not_rewritten(self):
  v1=HERE/"TRADITION_COVERAGE_V1.json"
  self.assertEqual(self.cover["prior_inventory_sha256"],sha(v1))
  p=load(v1)
  self.assertEqual(len(p["traditional_systems"]),16)
  self.assertEqual(len(self.cover["traditional_systems"]),16)
  self.assertEqual([x["id"] for x in self.cover["traditional_systems"]],[x["id"] for x in p["traditional_systems"]])

 def test_single_map_and_referenced_links(self):
  readme=(HERE/"README.md").read_text(encoding="utf-8")
  self.assertIn("OWNER_GUIDE_MAYA_BOOKS_SYSTEMS_AND_RESEARCH_MAP_20261022.md",readme)
  self.assertIn("TRADITION_COVERAGE_RECONCILED_V2.json",readme)
  self.assertIn("RECONCILED_SOURCE_TO_TEST_EVIDENCE_V1.json",readme)
  self.assertEqual(self.ledger["one_canonical_living_overview_diagram"],"docs/astrology-research-map/WORKFLOW.mmd")
  self.assertFalse(self.ledger["other_parallel_Mermaid_diagrams_copied_into_canonical_tree"])
  for x in ("WORKFLOW.mmd","SOURCE_TO_TEST_GATES.mmd","TRADITION_DEPENDENCIES.mmd"):
   self.assertTrue((HERE/x).read_text(encoding="utf-8").startswith("flowchart "))
  self.assertFalse((HERE/"MULTITRADITION_SOURCE_TO_TEST_MAP.md").exists())

 def test_all_sibling_source_hash_provenance_bounded(self):
  self.assertEqual(self.ledger["source_lane_git_heads"],PARENTS)
  witnesses=self.ledger["source_files_sha256_and_bytes"]
  self.assertEqual(len(witnesses),13)
  self.assertEqual(len(ALL_PROVENANCE),13)
  for p in ALL_PROVENANCE:
   proof=witnesses[p.relative_to(ROOT).as_posix()]
   self.assertEqual((proof["sha256"],proof["bytes"]),(sha(p),p.stat().st_size))
   self.assertEqual(proof["evidence_layer"],"SOURCE_OR_METHOD_DOCUMENTATION_NOT_HUMAN_SUCCESS")

 def test_four_owner_maya_nonfiction_books_and_excluded_novel(self):
  self.assertEqual(len(self.owner["input_sources"]),5)
  self.assertEqual(self.owner["research_sources_usable_for_next_reading"],4)
  self.assertEqual(self.owner["fiction_omitted_from_original_sources"],1)
  names=[x["title"] for x in self.owner["input_sources"]]
  self.assertTrue(any("Time and the Highland Maya" in n for n in names))
  self.assertTrue(any("The Madrid Codex" in n for n in names))
  self.assertTrue(any("Skywatchers" in n for n in names))
  self.assertTrue(any("Calendrical Calculations" in n for n in names))
  self.assertTrue(any("Doomsday Match" in n for n in names))
  self.assertEqual(self.cover["owner_maya_book_inventory"]["fully_read_books"],0)

 def test_maya_living_practitioner_names_and_person_claims_not_predictive(self):
  self.assertEqual(len(self.practitioner["day_name_crosswalk_only"]),20)
  self.assertEqual(len(self.practitioner["observed_primary_claims_development_only"]),7)
  maya=next(x for x in self.cover["traditional_systems"] if x["id"]=="MAYA-LIVING")
  self.assertFalse(maya["accepted_evidence"]["Kiche_living_daycount_epoch_independently_verified"])
  self.assertEqual(maya["accepted_evidence"]["personality_claims_in_runtime"],0)
  self.assertEqual(self.ledger["living_Kiche_source_person_claims_held_as_exploratory"],7)

 def test_maya_claim_trace_does_not_qualify_for_human_trial(self):
  x=self.calendar_claim
  self.assertEqual(x["claim_id"],"MAYA-CAND-001")
  self.assertFalse(x["readiness"]["frozen_before_outcomes"])
  self.assertEqual(x["human_evidence"]["validated_predictive_successes"],0)
  self.assertEqual(x["human_evidence"]["untouched_test_participants"],0)
  self.assertFalse(self.cover["historical_original_source_promotion"]["Maya_original_person_trait_prediction_frozen"])

 def test_original_dresden_facsimile_seen_not_deciphered(self):
  self.assertEqual(len(self.folio["source_witnesses"]),2)
  self.assertTrue(all(x["direct_visual_notes"] and len(x["render_sha256"])==64 and x["rendered_width"]>0 and x["rendered_height"]>0 for x in self.folio["source_witnesses"]))
  self.assertEqual(self.folio["independently_transcribed_Maya_hieroglyph_signs"],0)
  doc=next(x for x in self.cover["traditional_systems"] if x["id"]=="MAYA-CODEX")
  self.assertEqual(doc["accepted_evidence"]["visualized_facsimile_folio_count"],2)
  self.assertFalse(doc["accepted_evidence"]["original_surviving_codex_pages_authenticated_against_facsimiles"])
  self.assertEqual(doc["accepted_evidence"]["derived_person_specific_Maya_natal_predictions"],0)

 def test_six_hd_existing_domains_and_14_unscored_non_hd_categories(self):
  self.assertEqual(len(self.crosswalk["existing_Human_Design_domain_ids"]),6)
  self.assertEqual(len(self.crosswalk["crosswalk"]),20)
  self.assertEqual(len([x for x in self.crosswalk["crosswalk"] if x["id"].startswith("HD-EXISTING-")]),6)
  self.assertEqual(len([x for x in self.crosswalk["crosswalk"] if not x["id"].startswith("HD-EXISTING-")]),14)
  self.assertEqual(self.crosswalk["cross_tradition_hypotheses_active_in_runtime"],0)
  self.assertEqual(self.cover["current_claim_class_crosswalk"]["cross_tradition_scored_claims_promoted"],0)

 def test_correlation_variants_not_universal_kiche_epoch(self):
  self.assertEqual(self.ledger["Maya_lowland_calendar_GMT_correlation_choices"],[584283,584285])
  self.assertFalse(self.ledger["independent_Kiche_daycount_anchor_verified"])
  self.assertIn("Living_Kiche_Chol_Qij_daykeeping",self.ledger["Maya_tradition_region_layers"])
  self.assertIn("Modern_Dreamspell_not_ancient_primary",self.ledger["Maya_tradition_region_layers"])

 def test_human_blind_nulls_are_zero_every_layer(self):
  self.assertEqual(self.ledger["actual_independently_blinded_human_predictive_validations"],0)
  self.assertEqual(self.ledger["astrology_rule_promotions"],0)
  self.assertFalse(self.ledger["main_runtime_changes"])
  self.assertEqual(self.cover["project_empirical_state"]["real_human_blind_pred_successes"],0)
  self.assertEqual(self.owner["real_human_blinded_predictive_validations"],0)

 def test_mutation_two_witnesses_to_validated_human_is_rejected(self):
  mutated=deepcopy(self.ledger)
  mutated["actual_independently_blinded_human_predictive_validations"]=2
  mutated["astrology_rule_promotions"]=2
  valid=lambda d:d["actual_independently_blinded_human_predictive_validations"]==0 and d["astrology_rule_promotions"]==0
  self.assertTrue(valid(self.ledger))
  self.assertFalse(valid(mutated))

 def test_mutation_maya_study_to_unverified_epoch_is_not_scored(self):
  mutated=deepcopy(self.cover)
  native=next(x for x in mutated["traditional_systems"] if x["id"]=="MAYA-LIVING")
  native["accepted_evidence"]["Kiche_living_daycount_epoch_independently_verified"]=True
  valid=lambda d: all(not x["accepted_evidence"]["Kiche_living_daycount_epoch_independently_verified"]
    for x in d["traditional_systems"] if x["id"]=="MAYA-LIVING")
  self.assertTrue(valid(self.cover))
  self.assertFalse(valid(mutated))

if __name__=="__main__":unittest.main()
