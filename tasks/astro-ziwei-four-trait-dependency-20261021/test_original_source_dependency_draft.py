"""Original Zi Wei four human construct lexeme-dependence and toy coverage tests.

All source claim mappings are historical, tentative and NOT approved for
human personality or illness prediction.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import build_original_source_dependency_draft as draft

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
DOC = B / "FOUR_ZIWEI_SOURCE_CONSTRUCT_DEPENDENCY_DRAFT_V1.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data):
    return sha256(data).hexdigest()


class SourceBoundFourConstructDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read(DOC)
        cls.claims = cls.data["all_11_old_chinese_phrase_to_construct_source_dependency_claims"]
        cls.edges = cls.data["five_original_source_claim_dependency_edges"]
        cls.toy = cls.data["comparative_toy_model_structural_coverage"]
        cls.counts = cls.toy["synthetic_chart_option_state_counts"]

    def test_01_accepted_original_source_lexical_colocation_and_readiness_SHA(self):
        self.assertEqual(sha(draft.L.read_bytes()), draft.LEX_SHA)
        self.assertEqual(sha(draft.C.read_bytes()), draft.COL_SHA)
        self.assertEqual(sha(draft.READY.read_bytes()), draft.READY_SHA)
        self.assertEqual(self.data["source_11_narrow_lexemes_report_SHA256"], draft.LEX_SHA)
        self.assertEqual(
            self.data["source_15_same_palace_grade_clauses_report_SHA256"], draft.COL_SHA
        )

    def test_02_original_historical_source_not_pretended_as_empirical_humans(self):
        self.assertEqual(self.data["actual_real_person_birth_and_response_records"], 0)
        self.assertEqual(self.data["actual_human_predictive_accuracy_trials"], 0)
        self.assertEqual(self.data["production_astrological_rules_promoted"], 0)
        self.assertFalse(self.data["real_human_preregistration_completed"])
        self.assertFalse(self.data["source_frozen_primary_human_prediction_model_selected"])

    def test_03_exact_eleven_source_context_claims_from_old_Chinese(self):
        expected = {
            (x["verbatim_narrow_Chinese_phrase"], x["original_occurrence_source_star"])
            for x in read(draft.L)["verbatim_behavior_related_lexical_source_witnesses"]
        }
        self.assertEqual({(x["source_phrase"], x["source_star"]) for x in self.claims}, expected)
        self.assertEqual(len(self.claims), 11)
        self.assertTrue(all(x["psycho_behavioral_effect_magnitude"] is None for x in self.claims))

    def test_04_original_four_early_source_behavior_constructs_preliminary(self):
        source = self.data["four_preliminary_behavioral_construct_definitions"]
        self.assertEqual(
            {k: v["main_star_source_intro"] for k, v in source.items()},
            {
                "decision_commitment": ["WuQu"],
                "contentious_disagreement": ["LianZhen"],
                "voluntary_helping": ["TianLiang"],
                "competitive_striving": ["PoJun"],
            },
        )
        self.assertTrue(
            all(not v["psychometrically_validated_outcome_selected"] for v in source.values())
        )

    def test_05_TaiYang_helping_exact_original_phrase_alternative_source_star(self):
        self.assertEqual(
            self.data["tentative_TaiYang_helping_extension_for_source_overlap_only"],
            ["TaiYang", "TianLiang"],
        )
        other = [r for r in self.claims if r["source_phrase"] == "好济施"]
        self.assertEqual({x["source_star"] for x in other}, {"TaiYang", "TianLiang"})
        self.assertEqual(
            {x["tentative_behavioral_construct"] for x in other}, {"voluntary_helping"}
        )
        self.assertEqual(
            {x["old_accepted_source_annotation_id"] for x in other}, {"ZWD-R0263", "ZWD-R0464"}
        )

    def test_06_YouBi_reverse_lexical_order_not_automatically_validated_helping(self):
        y = next(r for r in self.claims if r["source_phrase"] == "好施济")
        self.assertEqual(y["source_star"], "YouBi")
        self.assertEqual(
            y["tentative_behavioral_construct"], "RELATED_GIVING_WORDING_NOT_EQUIVALENT_YET"
        )
        self.assertEqual(y["required_feature_engine_status"], "AUXILIARY_PLACEMENT_NOT_VERIFIED")
        self.assertFalse(y["tentative_behavior_construct_wording_equivalence_validated"])

    def test_07_WenQu_conditional_decisiveness_needs_other_stars_favourable_house(self):
        r = next(r for r in self.claims if r["source_star"] == "WenQu")
        self.assertEqual(
            r["original_source_context_class"], "AUXILIARY_CONDITIONAL_CO_PRESENT_STARS"
        )
        self.assertEqual(r["required_feature_engine_status"], "AUXILIARY_PLACEMENT_NOT_VERIFIED")
        self.assertFalse(r["this_draft_claim_may_be_used_as_scored_human_prediction"])

    def test_08_raw_only_QingYang_still_not_full_accepted_source_note(self):
        raw = [r for r in self.claims if r["source_star"] == "QingYang"]
        self.assertEqual(len(raw), 2)
        self.assertTrue(all(x["old_accepted_source_annotation_id"] is None for x in raw))
        self.assertTrue(
            all(
                x["required_feature_engine_status"] == "AUXILIARY_PLACEMENT_NOT_VERIFIED"
                for x in raw
            )
        )

    def test_09_medical_violence_claims_not_repackaged_as_competition_psychology(self):
        claims = {(x["source_phrase"], x["source_star"]): x for x in self.claims}
        self.assertEqual(
            claims[("争斗疾病", "PoJun")]["tentative_behavioral_construct"],
            "HISTORICAL_FIGHTING_AND_ILLNESS_NOT_QUESTIONNAIRE_TARGET",
        )
        self.assertEqual(
            claims[("好勇斗狠", "QingYang")]["tentative_behavioral_construct"],
            "HISTORICAL_AGGRESSION_NOT_COMPETITION_TARGET",
        )
        self.assertTrue(
            self.data[
                "clinical_fate_gender_moral_stereotypes_excluded_from_modern_human_prediction"
            ]
        )

    def test_10_all_source_claims_no_behavior_calibration_or_scored_promotion(self):
        for r in self.claims:
            self.assertIsNone(r["psycho_behavioral_effect_magnitude"])
            self.assertFalse(r["source_testable_human_hypothesis_frozen"])
            self.assertFalse(r["is_independent_questionnaire_predictive_score"])
            self.assertFalse(r["this_draft_claim_may_be_used_as_scored_human_prediction"])

    def test_11_five_source_dependency_edges_include_same_exact_wording(self):
        self.assertEqual(len(self.edges), 5)
        edge = next(
            x for x in self.edges if x["source_dependency_type"] == "EXACT_IDENTICAL_CHINESE_PHRASE"
        )
        self.assertEqual(
            {edge["left_original_star"], edge["right_original_star"]}, {"TaiYang", "TianLiang"}
        )
        self.assertEqual(edge["tentative_shared_construct"], "voluntary_helping")
        self.assertFalse(edge["probabilities_may_be_added_as_independent_model_hits"])

    def test_12_distinct_lexical_overlap_and_conditional_source_edges_not_false_correlations(self):
        self.assertEqual(
            {e["source_dependency_type"] for e in self.edges},
            {
                "EXACT_IDENTICAL_CHINESE_PHRASE",
                "SHARED_LEXICAL_ROOT_ONLY",
                "EXPLICIT_AUXILIARY_CONDITIONAL",
                "ADVERSE_MULTI_STAR_CLUSTER_NOT_SIMPLE_PAIR",
            },
        )
        self.assertTrue(
            all(not x["human_trait_correlation_or_effect_size_quantified"] for x in self.edges)
        )

    def test_13_312_vendor_rows_not_independent_human_chart_or_312_unique(self):
        self.assertEqual(self.data["source_312_synthetic_oracle_SHA256"], draft.ORACLE_SHA)
        self.assertEqual(self.toy["synthetic_chart_option_state_counts"]["synthetic_states"], 120)
        self.assertEqual(len(self.toy["all_120_pinned_source_14_main_star_toy_states"]), 120)
        self.assertTrue(self.toy["sampled_dates_not_population_birth_time_prevalence"])
        self.assertTrue(self.toy["user_or_Hale_inspected_outcomes_not_included"])

    def test_14_narrow_sole_star_mechanically_agreed_10_not_tradition(self):
        self.assertEqual(self.counts["strict_sole_star_and_all_vendor_agreement"], 10)
        self.assertTrue(
            self.data[
                "model_A_strict_mechanics_are_NOT_assumed_original_traditional_conjunction_requirement"
            ]
        )
        self.assertFalse(self.data["source_frozen_primary_human_prediction_model_selected"])

    def test_15_initial_four_main_star_source_presence_34_vs_unselected(self):
        self.assertEqual(self.counts["initial_four_main_star_presence"], 34)
        self.assertEqual(self.counts["old_selected_star_with_other_principal_present"], 22)
        self.assertTrue(
            self.data[
                "two_hypothesis_models_A_strict_B_presence_are_ALTERNATIVES_not_copre_registered_primary"
            ]
        )

    def test_16_broader_five_star_source_lexeme_presence_42_extra_eight(self):
        self.assertEqual(self.counts["extended_five_main_star_presence"], 42)
        self.assertEqual(self.counts["new_states_due_sole_TaiYang_extension"], 8)
        self.assertEqual(
            self.counts["extended_five_main_star_presence"]
            - self.counts["initial_four_main_star_presence"],
            8,
        )
        self.assertTrue(
            self.data[
                "model_Bplus_TaiYang_helping_expansion_NOT_test_or_select_after_viewing_human_responses"
            ]
        )

    def test_17_two_same_helping_main_stars_must_count_one_target(self):
        self.assertEqual(self.counts["two_helping_stars_TaiYang_and_TianLiang"], 2)
        self.assertTrue(
            self.data["source_lexical_occurrences_not_statistically_independent_predictions"]
        )
        for r in self.toy["all_120_pinned_source_14_main_star_toy_states"]:
            if {"TaiYang", "TianLiang"} <= set(r["Life_palace_original_main_stars"]):
                self.assertEqual(
                    r["distinct_tentative_behavior_constructs_deDuplicated"], ["voluntary_helping"]
                )

    def test_18_four_target_constructs_not_many_lexical_phrases(self):
        self.assertEqual(
            [self.counts["number_of_constructs_" + str(k)] for k in (0, 1, 2)], [78, 39, 3]
        )
        self.assertEqual(self.counts["two_distinct_target_constructs"], 3)
        self.assertEqual(sum(self.counts["number_of_constructs_" + str(k)] for k in (0, 1, 2)), 120)

    def test_19_historical_grade_ranks_not_modern_behavioral_weights(self):
        self.assertEqual(
            self.data["unverified_benefic_malefic_year_stem_qualifier_source_rule_count"], 15
        )
        self.assertTrue(
            self.data["source_grade_rank_wealth_conditions_not_transferable_to_personality_weights"]
        )
        self.assertTrue(
            self.data["model_B_has_no_verified_interactions_or_psychological_calibration"]
        )

    def test_20_all_ten_true_human_readiness_gates_remain_blocked(self):
        gates = self.data["all_real_human_pilot_readiness_gate_statuses"]
        self.assertEqual(len(gates), 10)
        self.assertEqual(self.data["number_of_human_ready_gates"], 0)
        self.assertTrue(
            all(x["blocking"] and x["status"] in ("unresolved", "owner_gate") for x in gates)
        )
        self.assertFalse(self.data["matched_decoys_and_non_astrology_baseline_approved"])
        self.assertFalse(self.data["questionnaire_selected_or_calibrated_for_actual_people"])

    def test_21_changed_source_SHA_or_removed_accepted_lexical_note_fails(self):
        with (
            patch.object(draft, "LEX_SHA", "0" * 64),
            self.assertRaisesRegex(ValueError, "source or readiness document SHA drift"),
        ):
            draft.get_data()

    def test_22_raw_QingYang_source_claim_cannot_be_promoted_to_main_star(self):
        broken = deepcopy(draft.CLASSES)
        val = broken[("果决", "QingYang")]
        broken[("果决", "QingYang")] = (val[0], val[1], "MAIN_STAR_POSITION_CALCULABLE")
        with (
            patch.object(draft, "CLASSES", broken),
            self.assertRaisesRegex(ValueError, "unaccepted original auxiliary"),
        ):
            draft.source_claims(read(draft.L))

    def test_23_forged_vendor_synthetic_oracle_source_SHA_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            data = Path(d) / "original.json"
            data.write_text('{"synthetic_cases":312}')
            with (
                patch.object(draft, "COLD_ORACLE", data),
                self.assertRaisesRegex(ValueError, "SHA incorrect"),
            ):
                draft.oracle_source()

    def test_24_full_draft_recomputes_exact_and_does_not_add_human_accuracy(self):
        self.assertEqual(draft.build(), self.data)
        self.assertEqual(self.data["actual_human_predictive_accuracy_trials"], 0)
        self.assertEqual(self.data["production_astrological_rules_promoted"], 0)


if __name__ == "__main__":
    unittest.main()
