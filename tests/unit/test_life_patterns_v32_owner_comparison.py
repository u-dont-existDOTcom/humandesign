"""Offline V3.2 revision, source-integrity and no-chart-leak tests."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "tasks/life-patterns-v32-owner-comparison-20261015"
REV = (
    ROOT
    / "tasks/life-patterns-guided-eight-assessment-20261015/V3_2_COGNITIVE_QUESTION_CANDIDATES.json"
)
BANK = ROOT / "tasks/life-patterns-idiographic-20261010/tendency-first-v3-scaffold-development.json"


def module(filename):
    spec = importlib.util.spec_from_file_location(filename.stem, str(filename))
    obj = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(obj)
    return obj


class V32Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = module(HERE / "build_v32_pilot.py")
        cls.compare = module(HERE / "compare_private_owner.py")
        cls.bank = json.loads(BANK.read_text())
        cls.revisions = json.loads(REV.read_text())

    def test_artifact_reproducible(self):
        self.assertEqual(
            self.builder.build(), (HERE / "LIFE_PATTERNS_V32_OFFLINE_PILOT.html").read_bytes()
        )

    def test_revisions_scored_neither_here_nor_live(self):
        self.assertEqual(len(self.revisions["items"]), 8)
        self.assertTrue(
            all(
                q["planning_targets"] == [] and q["automatic_chart_scoring"] is False
                for q in self.bank["questions"]
            )
        )
        self.assertIn("DEVELOPMENT_ONLY", self.revisions["status"])
        self.assertEqual({q["id"] for q in self.revisions["items"]}, set(self.compare.ROUTES))
        for q in self.revisions["items"]:
            self.assertTrue(q["candidate_question"])
            self.assertTrue(q["abstain_if"])
        self.assertTrue(
            all("birth" not in q["candidate_question"].lower() for q in self.revisions["items"])
        )

    def sample_sources(self):
        answers = {
            q["id"]: {
                "selected": [q["example_answer_paths"][0]],
                "other": "synthetic",
                "skip": False,
                "unsure": False,
            }
            for q in self.bank["questions"]
        }
        original = {
            "schema": self.compare.SCHEMA,
            "answers": answers,
            "unique_behaviors": [{"behavior": str(i)} for i in range(3)],
        }
        updated = json.loads(json.dumps(original))
        for route in self.compare.ROUTES[:6]:
            updated["answers"][route]["context_rule"] = "Synthetic conditional information"
        for route in self.compare.ROUTES[4:]:
            updated["answers"][route]["recent_case"] = "Synthetic recent example"
        cross = {
            "rows": [
                {
                    "question_id": q["id"],
                    "old_route_id": q["source_route_id"],
                    "old_direct_equivalence": i < 24,
                    "category": "compatible_narrow",
                    "scope_analysis": "Neutral comparison",
                    "historical_sources": [],
                }
                for i, q in enumerate(self.bank["questions"])
            ]
        }
        return original, updated, cross

    def test_provenance_and_non_incremental_chart_status(self):
        old, new, cross = self.sample_sources()
        baseline = self.compare.FROZEN_RESULT.read_text()
        receipt, rows = self.compare.summarize(old, new, cross, self.bank, self.revisions, baseline)
        self.assertEqual(receipt["v3_original_question_count"], 25)
        self.assertEqual(receipt["v3_context_guided_routes_complete"], 8)
        self.assertEqual(receipt["guided_distinct_conditional_rules"], 6)
        self.assertEqual(receipt["guided_distinct_recent_cases"], 4)
        self.assertEqual(receipt["historical_direct_mapped_routes"], 24)
        self.assertEqual(receipt["v32_newly_admitted_chart_features"], 0)
        self.assertFalse(receipt["new_birth_date_search_executed"])
        self.assertEqual(len(rows), 25)
        # Completely different development prose cannot modify a scoring result.
        for route in self.compare.ROUTES:
            new["answers"][route]["context_rule"] = "A different synthetic behavior"
        other, _ = self.compare.summarize(old, new, cross, self.bank, self.revisions, baseline)
        self.assertEqual(
            other["birth_date_found_by_new_v32_answers"],
            receipt["birth_date_found_by_new_v32_answers"],
        )

    def test_changed_old_source_rejected(self):
        old, new, cross = self.sample_sources()
        new["answers"]["TF1-G01"]["selected"] = []
        with self.assertRaisesRegex(ValueError, "Original answer changed"):
            self.compare.summarize(
                old, new, cross, self.bank, self.revisions, self.compare.FROZEN_RESULT.read_text()
            )

    def test_public_receipt_bounded(self):
        receipt = json.loads((HERE / "AGGREGATE_SOURCE_RESULT.json").read_text())
        self.assertEqual(receipt["v32_newly_admitted_chart_features"], 0)
        self.assertEqual(receipt["owner_private_text_in_repo"], False)
        self.assertNotIn("source_answers", receipt)
        self.assertNotIn("birth_date", receipt)


if __name__ == "__main__":
    unittest.main()
