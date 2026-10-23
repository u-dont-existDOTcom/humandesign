#!/usr/bin/env python3
"""B09 pre-human literature trace, instrument safety and synthetic method tests."""
from __future__ import annotations
from datetime import date
from pathlib import Path
from collections import Counter
import json
import unittest
from maya_b09_synthetic_null_demo import (
    exact_upper_tail_sum_p, run_synthetic_null, source_declared_indices,
)
ROOT=Path(__file__).parent
def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
S=load("MAYA_B09_CHUEN_INDEPENDENT_LEXICAL_SOURCE_COMPARISON_V1.json")
Q=load("MAYA_B09_CHUEN_SOURCE_ALIGNED_BLIND_QUESTIONNAIRE_DRAFT.json")
N=load("MAYA_B09_SYNTHETIC_NULL_MULTI_POLICY_DEMO_V1.json")

class PhilologyAndUnfrozenPilot(unittest.TestCase):
    def test_earlier_independent_semantic_reference_is_not_independent_people(self):
        sources={x["id"]:x for x in S["sources"]}
        t=sources["THOMPSON_1950"]
        self.assertEqual(t["original_research_PDF_SHA256"],
           "690f412479ceb1971e2f741a5d51ee6bdff4918687af8877efad40f63ace4e23")
        self.assertIn("printed page 80",t["bibliographic"])
        self.assertIn("Barrera",t["basis"])
        self.assertFalse(S["independent_reviews"]["single_source_natal_trait_empirically_validated"])
        self.assertFalse(S["independent_reviews"]["Bolles_and_Barrera_independent_human_trait_samples"])

    def test_folkloric_day_and_birth_day_not_automatically_the_same(self):
        kinds={x["id"]:x for x in S["sources"]}
        self.assertIn("NOT a claim",kinds["KNOWLTON_2010"]["difference"])
        self.assertIn("NOT",kinds["BRAAKHUIS_1987_SECONDARY_LEAD"]["source_qualifier"])
        self.assertIn("maker semantic",kinds["STUART_2024_MEN"]["difference"])
        self.assertEqual(S["independent_reviews"]["human_scored_respondents"],0)

    def test_primary_scored_item_includes_paid_and_unpaid(self):
        q=Q["primary_outcome"]
        self.assertEqual(q["ordinal_bins"],[0,1,2,3,4,5])
        self.assertEqual(q["missing"],[6,7])
        self.assertEqual(len(q["items"]),8)
        self.assertIn("paid and unpaid",q["wording_en"])
        self.assertIn("rémunérées ou non",q["wording_fr"])
        self.assertIn("PARTIAL",q["source_equivalence"])

    def test_secondary_measures_not_allowed_to_rescue_primary(self):
        s=Q["secondary_items"]
        self.assertGreaterEqual(len(s),4)
        self.assertTrue(all(x["scored_primary"] is False for x in s))
        self.assertEqual(len({x["id"] for x in s}),len(s))
        self.assertTrue(Q["presentation"]["score_only_primary_outcome"])
        self.assertFalse(Q["lifecycle"]["independent_bilingual_cognitive_test_done"])

    def test_all_human_freeze_and_consent_claims_are_false(self):
        self.assertEqual(Q["stage"],"DRAFT_SEMANTICALLY_IMPROVED_NOT_FROZEN_NO_PARTICIPANTS")
        self.assertTrue(Q["lifecycle"]["no_actual_consent"])
        self.assertTrue(Q["lifecycle"]["no_human_data_stored"])
        self.assertTrue(Q["analysis_draft"]["freeze_sha256_pending"])
        self.assertTrue(Q["analysis_draft"]["feasibility_n60_inadequate_to_validate_effect"])

    def test_exact_subsets_upper_tail_handles_extreme_ties(self):
        self.assertAlmostEqual(exact_upper_tail_sum_p((5,5,0,0),(0,1)),1/6)
        self.assertEqual(exact_upper_tail_sum_p((0,0,0,0),(0,1)),1.0)
        self.assertEqual(exact_upper_tail_sum_p((5,5,0,0),(2,3)),1.0)
        self.assertAlmostEqual(exact_upper_tail_sum_p((5,5,0,0),(0,2)),5/6)

    def test_invalid_or_mismatched_subsets_rejected(self):
        for values,indices in [
          ((0,1,2),(0,0)),((0,1,2),(5,)),((0,6,2),(1,)),
          ((0,True,2),(0,)),((0,1,2),()),((0,1,2),(0,1,2)),
        ]:
          with self.subTest(v=values,i=indices):
            with self.assertRaises(ValueError):
                exact_upper_tail_sum_p(values,indices)

    def test_synthetic_dates_are_60_and_four_nonoverlapping_groups(self):
        a=source_declared_indices(date(2024,1,1),60)
        self.assertEqual(len(a),4)
        self.assertEqual([len(v) for v in a.values()],[3,3,3,3])
        self.assertEqual(len(set(sum((list(x) for x in a.values()),[]))),12)

    def test_seeded_simulation_matches_preserved_snapshot(self):
        x=run_synthetic_null(384,20261023)
        self.assertEqual(x["single_locked_policy_positive_null_count"],20)
        self.assertEqual(x["posthoc_best_of_four_positive_null_count"],55)
        for k in x:
            self.assertEqual(N[k],x[k])
        self.assertGreater(N["posthoc_selected_rate"],N["locked_rate"])
        self.assertTrue(N["no_actual_birthday_or_survey_data"])
        self.assertFalse(N["primary_frozen_human_trial_eligibility"])

if __name__=="__main__":
    unittest.main()
