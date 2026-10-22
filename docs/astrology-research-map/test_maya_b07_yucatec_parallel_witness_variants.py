#!/usr/bin/env python3
"""Historical Yucatec natal copy-variant consistency, not a personality test."""
import json
from pathlib import Path
from collections import Counter
import unittest
from maya_calendar_reference import YUCATEC_DAYS

BASE=Path(__file__).resolve().parent
S=json.loads((BASE/"MAYA_B07_YUCATEC_ARTISAN_WITNESS_VARIANTS.json").read_text(encoding="utf-8"))
P=json.loads((BASE/"MAYA_B07_YUCATEC_NATAL_SOURCE_PROVENANCE_V1.json").read_text(encoding="utf-8"))
D=json.loads((BASE/"MAYA_B07_ARTISAN_BLIND_STUDY_DRAFT_V1.json").read_text(encoding="utf-8"))

class YucatecManuscriptVariants(unittest.TestCase):
    def test_three_named_days_five_source_columns_exact(self):
        self.assertEqual([r["canonical_yucatec"] for r in S["entries"]],["CHUWEN","MEN","KAB’AN"])
        self.assertTrue(set(r["canonical_yucatec"] for r in S["entries"]).issubset(set(YUCATEC_DAYS)))
        self.assertEqual(len(S["entries"]),3)
        for r in S["entries"]:
            self.assertEqual(len(r["witness_variants"]),5)
            self.assertEqual(len(set(v["id"] for v in r["witness_variants"])),5)
            self.assertTrue(all(v["source_locus"].startswith("parallel") for v in r["witness_variants"]))

    def test_three_kaua_loci_not_three_independent_texts(self):
        self.assertEqual(S["independent_manuscript_ancestors_count_max"],3)
        self.assertTrue(S["flags"]["multiple_Kaua_loci_same_ancestral_source"])
        for r in S["entries"]:
            self.assertEqual(sum(v["id"].startswith("KAUA_") for v in r["witness_variants"]),3)
            self.assertEqual(sum(v["id"]=="CHAN_CAH_1_4" for v in r["witness_variants"]),1)
            self.assertEqual(sum(v["id"]=="PEREZ_94_95" for v in r["witness_variants"]),1)

    def test_chuen_has_specific_making_wording_in_kaua_variants(self):
        x={r["canonical_yucatec"]:r for r in S["entries"]}
        ch=x["CHUWEN"]
        self.assertTrue(ch["first_human_trial_candidate"])
        self.assertTrue(any("woodwork" in v["domain"] for v in ch["witness_variants"]))
        self.assertEqual(sum("weaving" in v["domain"] for v in ch["witness_variants"]),2)
        self.assertFalse(ch["source_to_modern_behavior_equivalence_verified"])

    def test_caban_carpentry_single_long_kaua_passage_only(self):
        x={r["canonical_yucatec"]:r for r in S["entries"]}
        c=x["KAB’AN"]
        locations=[v["id"] for v in c["witness_variants"] if "woodwork" in v["domain"]]
        self.assertEqual(locations,["KAUA_11_12"])
        self.assertFalse(c["first_human_trial_candidate"])
        self.assertFalse(x["MEN"]["first_human_trial_candidate"])

    def test_editor_english_world_directions_are_later_inference(self):
        self.assertTrue(P["classification"]["directional_day_attributions"].startswith("Editor"))
        self.assertIn("bracketed world-directions", " ".join(S["provenance_warnings"]))
        self.assertTrue(S["flags"]["original_Chan_Cah_fragment_source_not_complete_natal_cycle_in_every_witness"])

    def test_no_person_character_validation_from_transcription_or_synthetic_tests(self):
        self.assertEqual(S["results"]["historical_personal_outcomes"],0)
        self.assertEqual(S["results"]["scored_untouched_human_participants"],0)
        self.assertEqual(S["results"]["validated_natal_effects"],0)
        self.assertEqual(P["nonpromotion"]["actual_untouched_human_natal_validations"],0)
        self.assertEqual(D["counters"]["frozen_questionnaire_versions"],0)
        self.assertEqual(D["status"],"PRE_REGISTRATION_DRAFT_NOT_FROZEN_NOT_RUNNING")

    def test_original_parallel_and_translation_hashes_exact(self):
        self.assertEqual(S["source_original"]["original_pdf_sha256"],P["sources"][1]["sha256"])
        self.assertEqual(S["source_english"]["original_pdf_sha256"],P["sources"][0]["sha256"])
        self.assertEqual(S["source_original"]["original_pdf_pages"],[38,39,40,41])
        self.assertEqual(S["source_english"]["pdf_pages"],[20,21,22,23,24])

    def test_composite_three_day_group_not_an_authorized_primary_result(self):
        self.assertEqual(D["primary"]["canonical_yucatec_day"],"CHUWEN")
        self.assertTrue(D["exploratory_not_primary"]["is_investigator_generated_group_not_in_original_source"])
        self.assertTrue(D["exploratory_not_primary"]["not_usable_to_rescue_failed_single_CHUWEN_result"])
        self.assertEqual(P["source_fidelity_positive_candidates"][0]["test_eligibility"],"UNFROZEN_POTENTIAL_PRIMARY")

if __name__=="__main__":
    unittest.main()
