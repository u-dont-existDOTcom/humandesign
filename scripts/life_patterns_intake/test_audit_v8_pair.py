"""Synthetic-only checks for the read-only intake audit; no participant data."""
import copy
from pathlib import Path
import tempfile
import unittest

from audit_v8_pair import BASE_SCHEMA, REPAIR_SCHEMA, audit, load


def fixture():
    base = {
        "schema_version": BASE_SCHEMA,
        "record_status": "complete_after_pattern_review",
        "pattern_claims": [{
            "pattern_id": "PAT-TEST", "support_state": "multiple_episodes",
            "supporting_episode_ids": ["EP-A", "EP-B"],
            "supporting_series_report_ids": ["SER-A"], "counterexample_episode_ids": [],
            "source_turn_ids": ["T1"]}],
        "series_reports": [{"series_id": "SER-A", "source_turn_ids": ["T1"]}],
        "episodes": [{"episode_id": key, "linked_pattern_ids": ["PAT-TEST"],
                      "source_turn_ids": ["T1"]} for key in ("EP-A", "EP-B")],
        "transcript_source_provenance": {"source_turn_index": {"T1": "SYNTHETIC"}}
    }
    repair = {
        "schema_version": REPAIR_SCHEMA, "original_schema_version": BASE_SCHEMA,
        "original_record_status": base["record_status"],
        "question_log": [{"question_id": "Q1", "target_pattern_id": "PAT-TEST",
                          "response_reference": "R1"}],
        "repair_responses": [{"response_id": "R1", "exact_text": "SYNTHETIC"},
                             {"response_id": "R2", "exact_text": "yes"}],
        "recovered_transcript_turns": [{"recovered_turn_id": "RC1", "original_local_id": "T1"}],
        "participant_confirmed_account_changes": [{"target_pattern_id": "PAT-TEST",
            "review_reference": "REV1", "approval_reference": "R2"}],
        "post_review_added_evidence": [{"added_evidence_id": "EV1", "target_pattern_id": "PAT-TEST",
            "source_reference": "R1", "evidence_type": "concrete_episode"}],
        "proposed_metadata_corrections": [], "outstanding_issues": [],
        "review_record": {"review_id": "REV1", "participant_response_reference": "R2",
                          "participant_response": "yes"}
    }
    return base, repair


class AuditTests(unittest.TestCase):
    def test_valid_pair_is_not_mutated(self):
        base, repair = fixture()
        before = copy.deepcopy((base, repair))
        self.assertTrue(audit(base, repair)["structural_check_passed"])
        self.assertEqual((base, repair), before)

    def test_wrong_schema(self):
        base, repair = fixture()
        repair["original_schema_version"] = "wrong"
        self.assertFalse(audit(base, repair)["structural_check_passed"])

    def test_unresolved_source(self):
        base, repair = fixture()
        repair["post_review_added_evidence"][0]["source_reference"] = "ABSENT"
        self.assertFalse(audit(base, repair)["structural_check_passed"])

    def test_duplicate_ids(self):
        base, repair = fixture()
        repair["repair_responses"].append(copy.deepcopy(repair["repair_responses"][0]))
        self.assertFalse(audit(base, repair)["structural_check_passed"])

    def test_unknown_changed_pattern(self):
        base, repair = fixture()
        repair["participant_confirmed_account_changes"][0]["target_pattern_id"] = "ABSENT"
        self.assertFalse(audit(base, repair)["structural_check_passed"])

    def test_missing_review_link(self):
        base, repair = fixture()
        repair["participant_confirmed_account_changes"][0]["review_reference"] = "ABSENT"
        self.assertFalse(audit(base, repair)["structural_check_passed"])

    def test_approval_text_mismatch(self):
        base, repair = fixture()
        repair["review_record"]["participant_response"] = "not the same text"
        self.assertFalse(audit(base, repair)["structural_check_passed"])

    def test_question_budget(self):
        base, repair = fixture()
        repair["question_log"] = [{"question_id": f"Q{i}", "target_pattern_id": "PAT-TEST",
                                  "response_reference": "R1"} for i in range(5)]
        self.assertFalse(audit(base, repair)["structural_check_passed"])

    def test_label_mismatch_is_flagged_not_rewritten(self):
        base, repair = fixture()
        base["pattern_claims"][0]["supporting_episode_ids"] = ["EP-A"]
        result = audit(base, repair)
        self.assertTrue(result["structural_check_passed"])
        self.assertEqual(len(result["original_support_label_findings"]), 1)
        self.assertEqual(base["pattern_claims"][0]["support_state"], "multiple_episodes")

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            path.write_text('{"x":1,"x":2}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load(path)

    def test_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            path.write_text('{"x":NaN}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load(path)


if __name__ == "__main__":
    unittest.main()
