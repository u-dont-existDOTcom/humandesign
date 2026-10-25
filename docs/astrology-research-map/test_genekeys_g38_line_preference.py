"""G38 six-Line preference prototype, 120 entirely synthetic subjects."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path
import unittest
from collections import Counter

from genekeys_g38_synthetic_line_preference import (
    BANK,CONTRACT,SOURCE,SOURCE_PIN,SOURCE_STYLES,PERMUTATIONS,
    PERSON_COUNT,SCHEMAS,MOCK_POPULATION_STYLE_WEIGHTS,ROOT,
    fake_freeze,fake_responses,score_mock,check_packet,
    verified_source_locked_freeze,validate_sources,messages_from_bank,
    synthetic_independent_style_choice,canonical,digest,write_once,
)

PRE=ROOT/"GENEKEYS_G38_SYNTHETIC_PREANSWER_V1.json"
RESP=ROOT/"GENEKEYS_G38_SYNTHETIC_MOCK_CHOICES_V1.json"
SCORE=ROOT/"GENEKEYS_G38_SYNTHETIC_SCORE_V1.json"


class TestG38LineStyleResearchOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=json.loads(PRE.read_text(encoding="utf8"))
        cls.o=json.loads(RESP.read_text(encoding="utf8"))
        cls.sc=json.loads(SCORE.read_text(encoding="utf8"))
        cls.fb=check_packet(cls.f,SCHEMAS[0])
        cls.ob=check_packet(cls.o,SCHEMAS[1])
        cls.sb=check_packet(cls.sc,SCHEMAS[2])

    def test_source_registry_hash_and_exact_original_short_line_phrases(self):
        src,bank,contract=validate_sources()
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_PIN)
        self.assertEqual(len(src["verified_six_line_interpersonal_styles"]),6)
        self.assertEqual([bank["style_map"][str(i)]["source_phrase"] for i in range(1,7)],
              [s["brief_official_responds_best_to"] for s
               in src["verified_six_line_interpersonal_styles"]])
        self.assertEqual(contract["branch"]["natal_sphere_choice_is"],
            "ASSISTANT_ANALYST_DESIGN_CHOICE_NOT_PUBLISHER_PRESCRIPTION")

    def test_four_scenarios_six_style_messages_share_all_core_facts(self):
        _src,b,_=validate_sources()
        messages=messages_from_bank(b)
        self.assertEqual(len(messages),4)
        for task,entry in messages.items():
            self.assertEqual(len(entry["messages"]),6)
            for style,text in entry["messages"].items():
                self.assertEqual(style in range(1,7),True)
                for fact in entry["facts"]:
                    self.assertEqual(text.count(fact),1)

    def test_line1_really_longest_line5_really_shortest_source_style_proxy(self):
        _src,bank,_=validate_sources()
        tasks=messages_from_bank(bank)
        self.assertTrue(bank["stimulus_development_length_fix_before_publication"])
        for task in tasks.values():
            lengths={k:len(t.split()) for k,t in task["messages"].items()}
            self.assertEqual(max(lengths,key=lengths.get),1)
            self.assertEqual(min(lengths,key=lengths.get),5)
            self.assertGreater(lengths[1]-lengths[5],20)
        self.assertFalse(bank["independent_manipulation_checks_performed"])

    def test_source_phrases_not_misrepresented_as_author_original_message_scripts(self):
        bank=json.loads(BANK.read_text(encoding="utf8"))
        self.assertTrue(bank["analyst_authored_six_style_proxies_not_original_Rudd_messages"])
        self.assertFalse(bank["independent_manipulation_checks_performed"])
        self.assertFalse(bank["readability_content_equivalence_peer_review_performed"])
        self.assertEqual(len(bank["source_literal_to_experiment_divergences"]),6)
        self.assertIn("romance",bank["source_literal_to_experiment_divergences"][3].lower())

    def test_120_subjects_four_repeated_choices_and_balanced_line_within_strata(self):
        self.assertEqual(self.fb["participant_count"],PERSON_COUNT)
        self.assertEqual(len(self.fb["synthetic_participants"]),PERSON_COUNT)
        self.assertEqual(self.fb["trials_per_person"],4)
        group={}
        all_orders=set()
        for p in self.fb["synthetic_participants"]:
            grp=p["synthetic_cohort_stratum"]
            group.setdefault(grp,Counter())[p["SYNTHETIC_chart_line_not_actual_astro"]]+=1
            self.assertTrue(p["synthetic_participant_id"].startswith("ONLY-SYNTHETIC-G38-"))
            self.assertEqual(len(p["trials"]),4)
            for t in p["trials"]:
                self.assertEqual(set(t["displayed_styles_in_order"]),set(range(1,7)))
                self.assertEqual(len(t["messages_displayed_in_order"]),6)
                all_orders.add(tuple(t["displayed_styles_in_order"]))
        self.assertEqual(set(group),{f"MOCK-GROUP-{i}" for i in range(1,5)})
        self.assertTrue(all(c=={i:5 for i in range(1,7)} for c in group.values()))
        self.assertGreater(len(all_orders),50)

    def test_canonical_freeze_and_fake_response_and_score_reproduce(self):
        self.assertEqual(fake_freeze(),self.f)
        self.assertEqual(fake_responses(self.f),self.o)
        self.assertEqual(score_mock(self.f,self.o),self.sc)
        self.assertEqual(self.f["sha256"],
          "8ad17bee6a67df5be0130ea06357ca9dfd4c84cbb97562b88b03de7e72de7ba2")
        self.assertEqual(self.o["sha256"],
          "42b483904cdfe2745eb3ddf769a32428d28903f2e3d09fef4e207b777032b071")
        self.assertEqual(self.sc["sha256"],
          "2a2d4f816cfee75dbe1bee885378ef5b7d8dd70b29a131838768d62d853a7d7a")

    def test_unmatched_source_line_is_not_a_prediction_of_trauma_or_low_virtue(self):
        self.assertTrue(self.fb["same_chart_CANNOT_add_information_beyond_full_HD_natal_input"])
        self.assertTrue(self.fb["original_G37_publisher_sphere_choice_undetermined"])
        self.assertTrue(self.fb["natal_Sun_sphere_line_is_analyst_chosen"])
        self.assertTrue(self.sb["SOURCE_DEFINED_HYPOTHESIS_NOT_AUTHOR_QUANTIFIED"])
        self.assertTrue(self.sb["not_a_human_GeneKeys_utility_or_predictivity_measure"])

    def test_mock_line_independent_response_generator_uses_no_personal_chart(self):
        pid="ONLY-SYNTHETIC-G38-042"
        for scenario in ("map","drawing","garden","history"):
            x=synthetic_independent_style_choice(pid,scenario)
            self.assertIn(x,range(1,7))
        self.assertTrue(self.ob["responses_generated_independently_of_fake_natal_line"])
        self.assertTrue(self.ob["response_generator_has_unequal_general_style_popularity"])
        self.assertEqual(sum(MOCK_POPULATION_STYLE_WEIGHTS),1.0)

    def test_g38_control_of_unequal_stimulus_appeal_and_person_clustering(self):
        self.assertEqual(self.sb["synthetic_task_choices_total"],480)
        self.assertEqual(self.sb["matched_line_hits_across_all_synthetic_tasks"],76)
        self.assertEqual(self.sb["matched_preference_fraction_mock"],76/480)
        self.assertAlmostEqual(self.sb["nonastrology_popularity_baseline_fraction_mock"],1/6)
        self.assertEqual(self.sb["perm_count"],PERMUTATIONS)
        self.assertTrue(self.sb["perm_whole_person_line_labels"])
        self.assertEqual(self.sb["person_level_null_one_sided_p_MOCK_ONLY"],.7115)
        self.assertGreater(self.sb["population_style_preference_rates_mock"]["5"],.25)
        self.assertLess(self.sb["population_style_preference_rates_mock"]["1"],.10)
        self.assertTrue(self.sb["mock_unadjusted_uniform_one_sixth_is_NOT_appropriate_null"])

    def test_immutable_source_model_disallows_rehashed_line_swap(self):
        changed=copy.deepcopy(self.f)
        changed["body"]["synthetic_participants"][0]["SYNTHETIC_chart_line_not_actual_astro"]=6
        changed["sha256"]=digest(changed["body"])
        check_packet(changed,SCHEMAS[0])
        with self.assertRaises(ValueError):
            verified_source_locked_freeze(changed)
        with self.assertRaises(ValueError):
            score_mock(changed,self.o)

    def test_rehashing_changed_bank_or_contract_analyst_choice_fails(self):
        for column in ("stimulus_bank_file_SHA256","study_contract_file_SHA256"):
            altered=copy.deepcopy(self.f)
            altered["body"][column]="0"*64
            altered["sha256"]=digest(altered["body"])
            with self.subTest(column=column),self.assertRaises(ValueError):
                fake_responses(altered)

    def test_self_hash_changed_mock_answer_rejected(self):
        x=copy.deepcopy(self.o)
        x["body"]["response_rows"][0]["selected_visible_position_1to6"]=7
        with self.assertRaises(ValueError):
            score_mock(self.f,x)
        # Even validly rehashed now fails value-validation.
        x["sha256"]=digest(x["body"])
        with self.assertRaises(ValueError):
            score_mock(self.f,x)

    def test_invalid_selected_position_and_bool_rejected(self):
        for bad in (0,7,True,"1",None):
            x=copy.deepcopy(self.o)
            x["body"]["response_rows"][0]["selected_visible_position_1to6"]=bad
            x["sha256"]=digest(x["body"])
            with self.subTest(bad=bad),self.assertRaises(ValueError):
                score_mock(self.f,x)

    def test_missing_or_duplicate_or_unknown_mock_answer_rejected(self):
        bad=copy.deepcopy(self.o)
        bad["body"]["response_rows"].pop()
        bad["sha256"]=digest(bad["body"])
        with self.assertRaises(ValueError):
            score_mock(self.f,bad)
        bad=copy.deepcopy(self.o)
        bad["body"]["response_rows"][-1]=copy.deepcopy(bad["body"]["response_rows"][0])
        bad["sha256"]=digest(bad["body"])
        with self.assertRaises(ValueError):
            score_mock(self.f,bad)
        bad=copy.deepcopy(self.o)
        bad["body"]["response_rows"][0]["synthetic_participant_id"]="UNKNOWN"
        bad["sha256"]=digest(bad["body"])
        with self.assertRaises(ValueError):
            score_mock(self.f,bad)

    def test_binding_response_to_different_frozen_version_rejected(self):
        bad=copy.deepcopy(self.o)
        bad["body"]["pre_answer_frozen_packet_sha256"]="0"*64
        bad["sha256"]=digest(bad["body"])
        with self.assertRaises(ValueError):
            score_mock(self.f,bad)

    def test_cannot_relabel_real_participant_record_as_synthetic(self):
        bad=copy.deepcopy(self.o)
        bad["body"]["response_rows"][0]["no_actual_person_answered"]=False
        bad["sha256"]=digest(bad["body"])
        with self.assertRaises(ValueError):
            score_mock(self.f,bad)
        bad=copy.deepcopy(self.f)
        bad["body"]["synthetic_only"]=False
        bad["sha256"]=digest(bad["body"])
        with self.assertRaises(ValueError):
            fake_responses(bad)

    def test_exclusive_file_write_prevents_freeze_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"synthetic_freeze.json"
            write_once(p,self.f)
            saved=p.read_bytes()
            with self.assertRaises(FileExistsError):
                write_once(p,self.f)
            self.assertEqual(saved,p.read_bytes())

    def test_frozen_model_is_not_complete_official_GeneKeys_profile(self):
        contract=json.loads(CONTRACT.read_text(encoding="utf8"))
        self.assertFalse(contract["branch"]["official_full_profile_calculator_parity_established"])
        self.assertTrue(contract["proposed_primary_test"]["same_chart_CANNOT_add_information_beyond_full_HD_natal_input"]
                        if "same_chart_CANNOT_add_information_beyond_full_HD_natal_input"
                           in contract["proposed_primary_test"] else
                        contract["proposed_primary_test"]["unavoidable_hd_shared_input"].startswith("Gene Keys"))
        self.assertFalse(contract["current_result"]["pre_registered"])
        self.assertFalse(contract["current_result"]["actual_consent_collect"])
        self.assertFalse(contract["current_result"]["real_person_outcomes"])
        self.assertEqual(contract["current_result"]["human_predictive_validations"],0)

    def test_missing_real_person_custody_and_human_irreversibility_unclaimed(self):
        self.assertFalse(self.fb["real_consent_or_communication_administered"])
        self.assertFalse(self.fb["rehearsal_is_NOT_externally_timestamped"] is False)
        self.assertFalse(self.sb["production_scorer_modified"])
        self.assertEqual(self.sb["truly_blinded_human_validation_count"],0)


if __name__=="__main__":
    unittest.main()
