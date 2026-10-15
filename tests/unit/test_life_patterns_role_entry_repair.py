"""Role-entry questionnaire regression tests: no scoring leakage or source overwrites."""

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-role-entry-repair-20261015"
PRIOR = ROOT / "tasks/life-patterns-v32-owner-comparison-20261015"
FROZEN = ROOT / "tasks/scenario-owner-recovery-calibration-20260923"


def load_source_module(file):
    spec = importlib.util.spec_from_file_location(file.stem, file)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class RoleEntryRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_source_module(TASK / "build_v33_role_entry.py")
        cls.protocol = json.loads((TASK / "ROLE_ENTRY_MEASUREMENT_V1.json").read_text())
        cls.generated = (TASK / "LIFE_PATTERNS_V33_ROLE_ENTRY_OFFLINE_PILOT.html").read_text()

    def test_generated_html_is_byte_exact(self):
        self.assertEqual(self.builder.build().decode(), self.generated)

    def test_original_banks_and_revision_data_present(self):
        match = re.search(
            r'<script id="pilot-data" type="application/json">(.*?)</script>', self.generated, re.S
        )
        self.assertIsNotNone(match)
        d = json.loads(match.group(1))
        self.assertEqual(len(d["questions"]), 25)
        self.assertEqual(len(d["v32"]["items"]), 8)
        self.assertEqual(len(d["role_probe"]["allowed_origins"]), 7)
        self.assertEqual(len(d["role_probe"]["pattern_choices"]), 6)
        self.assertEqual(d["role_probe"]["status"], "DEVELOPMENT_ONLY_NOT_SCORED")
        self.assertTrue(all(q.get("automatic_chart_scoring") is False for q in d["questions"]))

    def test_role_entry_not_equal_acceptance_or_offer(self):
        self.assertIn("Offering help", self.protocol["role_definition"])
        self.assertIn("If you become responsible", self.protocol["prompt"])
        self.assertIn(
            "normally", self.protocol["source_gap"].lower()
        ) if "normally" in self.protocol["source_gap"].lower() else self.assertIn(
            "typical", self.protocol["source_gap"].lower()
        )
        self.assertIn("context-dependent", self.protocol["coding_rule"])
        self.assertIn("No natal features", self.protocol["participant_scope"])

    def test_no_answer_key_in_participant_prompt(self):
        words = " ".join(
            str(self.protocol[key])
            for key in ("prompt", "role_definition", "overall_question", "neutral_followup")
        )
        self.assertNotRegex(
            words.lower(), r"lilly|astrology|birth date|1985|venus|recognition_entry|positive vote"
        )
        self.assertNotIn("astrohd_v15_behavioral_bridge", self.generated)

    def test_new_schema_is_separate_and_prior_schema_compatible(self):
        s = self.generated
        for schema in [
            "local_life_patterns_v3_2_pilot_unsubmitted",
            "local_life_patterns_v3_3_pilot_unsubmitted",
            "local_life_patterns_v3_pilot_unsubmitted",
        ]:
            self.assertIn(schema, s)
        self.assertIn("role_entry_review:state.roleEntry", s)
        self.assertIn("v3_2_answers:state.v32", s)
        self.assertIn("roleHasData(state.roleEntry)", s)
        self.assertIn("state.roleEntry=parsed.roleEntry", s)
        self.assertIn("role-short", s)
        self.assertIn("role-details", s)
        self.assertIn("roleRecord.summary", s)
        self.assertIn("roleFocus()", s)

    def test_corrected_reference_scoped(self):
        receipt = json.loads((PRIOR / "AGGREGATE_SOURCE_RESULT.json").read_text())
        accepted = json.loads(
            (FROZEN / "ASTROHD-V14-EXACT-CENTURY-RESULT-20260925.json").read_text()
        )
        self.assertEqual(receipt["accepted_reference_model"], "astrohd-v14-v1.4d")
        self.assertTrue(receipt["accepted_reference_recorded_instant_joint_first"])
        self.assertEqual(receipt["accepted_reference_tied_minute_count"], accepted["maximum_count"])
        self.assertEqual(
            receipt["accepted_reference_unique_maximum_date"], accepted["maximum_dates"][0]
        )
        self.assertFalse(receipt["new_birth_date_search_executed"])
        self.assertNotIn("prior_frozen_v43_exact_recorded_interval_rank", receipt)
        self.assertTrue(
            (PRIOR / "compare_private_owner.py")
            .read_text()
            .count("ASTROHD-V14-EXACT-CENTURY-RECEIPT-20260925.md")
            == 1
        )


if __name__ == "__main__":
    unittest.main()
