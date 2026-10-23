#!/usr/bin/env python3
"""B10 original-source craft measurement scope and anonymous coder fixture tests."""
import json
from pathlib import Path
import unittest
from maya_b10_occupation_coder_preflight import (
    CodingScopeError, CORE_ISCO_08, classify_occupation_candidate
)

ROOT=Path(__file__).resolve().parent
def data(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
C=data("MAYA_B10_ESTABLISHED_CRAFT_MEASURES_AND_DECISION_MATRIX.json")
F=data("MAYA_B10_ANONYMOUS_CODING_FIXTURES_V1.json")
B09=data("MAYA_B09_CHUEN_SOURCE_ALIGNED_BLIND_QUESTIONNAIRE_DRAFT.json")

class SourceCraftMeasureTests(unittest.TestCase):
    def test_prior_art_is_real_and_does_not_masquerade_as_validated_human_effect(self):
        urls={p["id"]:p["source_url"] for p in C["independent_prior_work"]}
        self.assertIn("ilo.org",urls["ILO_ISCO_08"])
        self.assertIn("bls.gov",urls["BLS_ATUS"])
        self.assertIn("PMC5891557",urls["COSMIN_2018"])
        self.assertIn("unstats.un.org",urls["UN_TIME_USE"])
        self.assertEqual(C["hard_limits"]["human_confirmatory_predictions_scored"],0)

    def test_preexisting_B09_annual_hours_is_not_silently_promoted(self):
        a=C["candidate_primary_options"]
        self.assertEqual([o["id"] for o in a],[
          "C1_SKILLED_CRAFT_OCCUPATION","C2_PAID_PLUS_UNPAID_MAKING_FREQUENCY",
          "C3_ANNUAL_CRAFT_HOURS","C4_SEVEN_DAY_DIARY_CHECK"])
        self.assertIn("B09_PRIMARY_DRAFT",a[2]["preoutcome_status"])
        self.assertTrue(all(x["primary_statistic_selected"] is False for x in a))
        self.assertTrue(B09["lifecycle"]["no_frozen_respondent_prediction"])

    def test_chosen_investigator_specific_ISCO_subset_is_exact(self):
        expected={"7115","7314","7317","7318","7522","7531","7533"}
        self.assertEqual(CORE_ISCO_08,expected)
        self.assertEqual({r["code"] for r in C["source_narrow_ISCO_08_candidate_codes"]},expected)
        self.assertTrue(all(len(x["label"])>10 for x in C["source_narrow_ISCO_08_candidate_codes"]))

    def test_all_13_hypothetical_fixtures_reproduce_expected_decision(self):
        cases=F["cases"]
        self.assertEqual(len(cases),13)
        self.assertEqual(len({x["id"] for x in cases}),13)
        for case in cases:
            with self.subTest(case=case["id"]):
                got=classify_occupation_candidate(case["supplied_manual_code_metadata"])
                self.assertEqual(got["status"],case["expected_output_status"])
                self.assertIs(got["narrow_ISCO_candidate_core_role"],case["expected_narrow_core_role"])
                self.assertFalse(got["birth_data_read"])
                self.assertFalse(got["validated_natal_prediction"])

    def test_common_confusions_excluded_from_candidate_core(self):
        cases={f["id"]:f for f in F["cases"]}
        for id in ["retail_noncraft","industrial_operator","digital_artist","food_prep"]:
            got=classify_occupation_candidate(cases[id]["supplied_manual_code_metadata"])
            self.assertIs(got["narrow_ISCO_candidate_core_role"],False)
        self.assertIs(classify_occupation_candidate(cases["unpaid_weaver"]["supplied_manual_code_metadata"])
                      ["narrow_ISCO_candidate_core_role"],None)

    def test_unreviewed_or_uncertain_work_does_not_count_as_noncraft_failure(self):
        cases={f["id"]:f for f in F["cases"]}
        for id in ["uncertain_code","unrecorded_job","unpaid_weaver","apprentice_carpentry"]:
            got=classify_occupation_candidate(cases[id]["supplied_manual_code_metadata"])
            self.assertIn("ABSTAIN",got["status"])
            self.assertIsNone(got["narrow_ISCO_candidate_core_role"])

    def test_coder_refuses_sensitive_personal_fields_or_implicit_identifiers(self):
        base={"isco_unit_code":"7115","code_verification":"verified","role_scope":"paid_work"}
        for extra,val in [("name","Example"),("dob","1999-01-01"),("birthplace","Anywhere"),("birth_day","CHUWEN"),("craft_hours",100)]:
            with self.subTest(extra=extra), self.assertRaises(CodingScopeError):
                classify_occupation_candidate({**base,extra:val})

    def test_invalid_code_or_misrepresented_verified_absence_rejected(self):
        bads=[
          {"isco_unit_code":"73","code_verification":"verified","role_scope":"paid_work"},
          {"isco_unit_code":"UNAVAILABLE","code_verification":"verified","role_scope":"paid_work"},
          {"isco_unit_code":"731X","code_verification":"verified","role_scope":"paid_work"},
          {"isco_unit_code":7318,"code_verification":"verified","role_scope":"paid_work"},
          {"isco_unit_code":"7318","code_verification":"yes","role_scope":"paid_work"},
          {"isco_unit_code":"7318","code_verification":"verified","role_scope":"unknown"},
          None,
        ]
        for r in bads:
            with self.subTest(arg=str(r)),self.assertRaises(CodingScopeError):
                classify_occupation_candidate(r)

    def test_mutant_machine_operator_promoted_to_weaver_would_change_result(self):
        case=next(x for x in F["cases"] if x["id"]=="industrial_operator")
        result=classify_occupation_candidate(case["supplied_manual_code_metadata"])
        wrong=classify_occupation_candidate({
            **case["supplied_manual_code_metadata"],"isco_unit_code":"7318"})
        self.assertIs(result["narrow_ISCO_candidate_core_role"],False)
        self.assertIs(wrong["narrow_ISCO_candidate_core_role"],True)
        # This documents why a *human blinded occupation coder* is needed,
        # not that automatic code lookup can detect a false initial code.

    def test_work_paid_and_leisure_crafts_are_not_conflated(self):
        source=next(x for x in C["independent_prior_work"] if x["id"]=="BLS_ATUS")
        self.assertIn("120309",source["reference_category"])
        self.assertIn("leisure-only",source["limits"])
        self.assertTrue(C["measurement_review_protocol"]["no_real_birth_data_during_cognitive_validation"])
        self.assertTrue(C["hard_limits"]["no_ISCO_occupation_codes_automatically_from_pseudonymous_free_text"])
        self.assertFalse(C["hard_limits"]["frozen_primary_outcome_choice"])
        self.assertEqual(F["counters"],{"actual_humans":0,"real_births":0,"craft_human_outcomes":0,"natal_validations":0})

if __name__=="__main__":
    unittest.main()
