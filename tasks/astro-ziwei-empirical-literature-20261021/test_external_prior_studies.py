"""Negative controls for evidence access, effect-size invention and hypothesis leakage."""

from __future__ import annotations

import unittest
from copy import deepcopy

import audit_external_prior_studies as audit


class AbstractSourceReliabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = audit.read(audit.REG)
        cls.queue = audit.read(audit.QUEUE)
        cls.byid = {x["study_id"]: x for x in cls.data["external_human_studies"]}

    def test_01_seven_sources_and_two_direct_ziwei_studies(self):
        result = audit.evaluate(self.data, self.queue)
        self.assertEqual(result["external_studies_screened"], 7)
        self.assertEqual(result["direct_ZiWei_studies"], 2)
        self.assertEqual(result["HumanDesign_human_predictive_trials"], 0)

    def test_02_2018_n243_three_practitioners_seven_items(self):
        x = self.byid["ZWDS-2018-TEO"]
        self.assertEqual(
            (
                x["sample_n_reported"],
                x["astrology_analyst_n"],
                x["reported_question_items_given_to_astrologers"],
            ),
            (243, 3, 7),
        )

    def test_03_2018_did_not_report_unequivocal_null(self):
        x = self.byid["ZWDS-2018-TEO"]
        self.assertTrue(x["overall_group_result_reported_null"])
        self.assertTrue(x["positive_subgroup_finding_reported"])
        self.assertFalse(x["multiple_testing_adjustment_checked"])

    def test_04_2018_false_subgroup_suppression_is_rejected(self):
        d = deepcopy(self.data)
        item = next(x for x in d["external_human_studies"] if x["study_id"] == "ZWDS-2018-TEO")
        item["positive_subgroup_finding_reported"] = False
        with self.assertRaisesRegex(ValueError, "2018"):
            audit.evaluate(d, self.queue)

    def test_05_2020_reported_smoking_signal_but_N_unknown(self):
        x = self.byid["ZWDS-2020-CHEN"]
        self.assertTrue(x["positive_group_finding_reported"])
        self.assertIsNone(x["sample_n_reported"])
        self.assertFalse(x["effect_size_numeric_available"])
        self.assertTrue(x["cites_2018_ZWDS_TEO_thesis"])

    def test_06_2020_false_sample_size_is_rejected(self):
        d = deepcopy(self.data)
        x = next(x for x in d["external_human_studies"] if x["study_id"] == "ZWDS-2020-CHEN")
        x["sample_n_reported"] = 1000
        with self.assertRaisesRegex(ValueError, "2020"):
            audit.evaluate(d, self.queue)

    def test_07_2020_invented_effect_size_is_rejected(self):
        d = deepcopy(self.data)
        x = next(x for x in d["external_human_studies"] if x["study_id"] == "ZWDS-2020-CHEN")
        x["effect_size_numeric_available"] = True
        with self.assertRaisesRegex(ValueError, "2020"):
            audit.evaluate(d, self.queue)

    def test_08_offcampus_claim_not_equated_with_downloaded_2020_full_text(self):
        record = self.data["source_access_audit"]["TKU_2020"]
        self.assertTrue(record["institutional_page_describes_off_campus_public_use"])
        self.assertIn("ezproxy", record["tested_download_button_redirect_target"])
        self.assertFalse(record["full_original_thesis_file_downloaded"])

    def test_09_original_2018_institutional_copy_request_not_full_access(self):
        record = self.data["source_access_audit"]["CSMU_2018"]
        self.assertEqual(record["institutional_access_control_seen"], "Request a copy")
        self.assertFalse(record["full_original_thesis_file_downloaded"])

    def test_10_false_full_text_access_flag_is_rejected(self):
        d = deepcopy(self.data)
        d["source_access_audit"]["CSMU_2018"]["full_original_thesis_file_downloaded"] = True
        with self.assertRaisesRegex(ValueError, "full-text"):
            audit.evaluate(d, self.queue)

    def test_11_western_studies_not_direct_ziwei_evidence(self):
        direct = [
            x for x in self.data["external_human_studies"] if x["tradition"] == "Zi Wei Dou Shu"
        ]
        self.assertEqual(len(direct), 2)
        self.assertEqual(self.byid["WESTERN-1984-TYSON"]["sample_n_reported"], 15)

    def test_12_carlson_original_short_abstract_numeric_results_not_invented(self):
        x = self.byid["WESTERN-1985-CARLSON"]
        self.assertEqual(x["outcome_direction"], "NOT_VERIFIED_FROM_SHORT_PUBLISHER_ABSTRACT")
        self.assertFalse(x["original_results_quantitatively_extracted"])

    def test_13_preserve_twin_positive_reanalysis_and_disputing_author(self):
        self.assertEqual(
            self.byid["WESTERN-1992-FUZEAU"]["original_author_reported_replies"],
            {"exact": 153, "reverse": 65, "no_difference": 20},
        )
        self.assertTrue(self.byid["WESTERN-1996-ERTEL-DEAN"]["critique_not_uncontested"])
        self.assertFalse(
            self.byid["WESTERN-1996-FUZEAU-REPLY"][
                "claim_that_future_replication_actually_occurred"
            ]
        )

    def test_14_suppressing_original_1996_reply_is_rejected(self):
        d = deepcopy(self.data)
        d["external_human_studies"] = [
            x for x in d["external_human_studies"] if x["study_id"] != "WESTERN-1996-FUZEAU-REPLY"
        ]
        with self.assertRaisesRegex(ValueError, "missing"):
            audit.evaluate(d, self.queue)

    def test_15_invented_prospective_success_in_existing_thesis_rejected(self):
        d = deepcopy(self.data)
        d["external_human_studies"][0][
            "prospective_out_of_sample_chart_prediction_demonstrated"
        ] = True
        with self.assertRaisesRegex(ValueError, "prospective"):
            audit.evaluate(d, self.queue)

    def test_16_human_study_gates_remain_blocked(self):
        p = self.queue["pre_registration_only_after_missing_method_inputs"]
        self.assertFalse(p["human_study_frozen_and_authorized"])
        self.assertEqual(p["project_real_human_predictive_trials_completed"], 0)

    def test_17_missing_thesis_access_queue_rejected(self):
        q = deepcopy(self.queue)
        q["primary_missing_sources"].pop()
        with self.assertRaisesRegex(ValueError, "full-text acquisition"):
            audit.evaluate(self.data, q)

    def test_18_source_report_hashes_and_gate_receipt_build_consistently(self):
        result = audit.emit_receipt()
        self.assertEqual(result["source_registry_SHA256"], audit.hash_file(audit.REG))
        self.assertEqual(result["methods_review_SHA256"], audit.hash_file(audit.REVIEW))
        self.assertEqual(result["evidence"]["direct_ZiWei_studies"], 2)
        self.assertEqual(result["human_astrology_predictive_trials_completed_by_project"], 0)


if __name__ == "__main__":
    unittest.main()
