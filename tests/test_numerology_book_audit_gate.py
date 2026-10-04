"""Mutation checks for audit controls. No synthetic receipt is production evidence."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("audit_gate", ROOT / "scripts/numerology_book_audit_verify.py")
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)
DESIGN = json.loads((ROOT / gate.BASE / "empirical_admission_contract.json").read_text())


class EmpiricalAdmissionControls(unittest.TestCase):
    def change(self, key, value):
        data = deepcopy(DESIGN)
        data["constraints"][key] = value
        return gate.validate_design(data)

    def test_actual_design_is_a_valid_nonlaunch_contract(self):
        self.assertEqual(gate.validate_design(DESIGN), [])
        self.assertFalse(DESIGN["launch_ready"])

    def test_unknown_cannot_be_negative(self):
        self.assertIn("EMPIRICAL_CONTROL_VIOLATION: unknown_is_negative", self.change("unknown_is_negative", True))

    def test_personal_year_only_cannot_be_full_decoz(self):
        self.assertIn("EMPIRICAL_CONTROL_VIOLATION: personal_year_only_is_full_decoz", self.change("personal_year_only_is_full_decoz", True))

    def test_false_alarms_and_misses_are_not_discounted(self):
        for key in ("false_positive_cost", "false_negative_cost"):
            with self.subTest(key=key):
                self.assertIn("SYMMETRIC_ERROR_ACCOUNTING_CHANGED", self.change(key, 0.2))
        self.assertIn("SYMMETRIC_ERROR_ACCOUNTING_CHANGED", self.change("false_positive_cost", True))

    def test_post_outcome_branch_selection_rejected(self):
        self.assertTrue(self.change("post_outcome_branch_selection", True))

    def test_averaging_conflicting_authors_rejected(self):
        self.assertTrue(self.change("average_incompatible_outputs", True))

    def test_exposure_duplicate_and_abstention_controls(self):
        for key, value in [("duplicate_event_credit", True), ("abstention_is_negative", True), ("broad_intervals_pay_observed_exposure", False), ("coverage_report_required", False)]:
            with self.subTest(key=key):
                self.assertTrue(self.change(key, value))

    def test_all_chronology_qualities_required(self):
        self.assertTrue(self.change("chronology_quality", ["approximate memory"]))

    def test_claim_of_launched_study_rejected(self):
        data = deepcopy(DESIGN)
        data["study_launched"] = True
        self.assertIn("UNAUTHORIZED_OR_UNESTABLISHED_ACTIVITY: study_launched", gate.validate_design(data))

    def test_open_source_and_operational_prerequisites_cannot_disappear(self):
        for target in ("official_decoz_resources", "campbell_hybrid_scope", "operational_interpretation_freeze"):
            data = deepcopy(DESIGN)
            data["open_launch_prerequisites"] = [x for x in data["open_launch_prerequisites"] if x["id"] != target]
            with self.subTest(target=target):
                self.assertIn("LAUNCH_PREREQUISITES_MISREPRESENTED", gate.validate_design(data))

    def test_2008_cannot_be_promoted_to_major(self):
        data = deepcopy(DESIGN)
        data["owner_2008"]["impact"] = "major"
        self.assertIn("OWNER_2008_CORRECTION_LOST", gate.validate_design(data))

    def test_pending_or_overclaimed_review_is_not_pass(self):
        self.assertIn("CLOSEOUT_REVIEW_DISPOSITION_MISSING", gate.validate_review({"status": "RUNNING"}))
        self.assertIn("INDEPENDENT_REVIEW_SCOPE_OVERCLAIM", gate.validate_review({"status": "CHECKED_NO_MATERIAL_FINDINGS", "review_boundary": "synthetic test only", "full_primary_corpus_independently_certified": True, "unresolved_blocking_findings": []}))


class FrozenArtifactControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        manifest = json.loads((ROOT / gate.BASE / "freeze_manifest.json").read_text())
        names = set(manifest["files"]) | set(gate.BASELINE) | {gate.BASE + "freeze_manifest.json"}
        for name in names:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, path)

    def tearDown(self):
        self.tmp.cleanup()

    def edit_json(self, name, edit):
        path = self.root / gate.BASE / name
        value = json.loads(path.read_text())
        edit(value)
        path.write_text(json.dumps(value))

    def test_actual_frozen_source_artifacts_match(self):
        self.assertEqual(gate.validate_sources(self.root), [])

    def test_changed_v1_is_rejected(self):
        name = next(iter(gate.BASELINE))
        with (self.root / name).open("a") as handle:
            handle.write("\nchanged\n")
        self.assertIn("IMMUTABLE_BLOB_CHANGED: " + name, gate.validate_sources(self.root))

    def test_missing_required_layer_is_not_full_coverage(self):
        self.edit_json("source_coverage.json", lambda d: d["requirement_crosswalk"].pop("relationship_marriage_compatibility"))
        self.assertIn("REQUIRED_DIMENSION_CROSSWALK_INCOMPLETE", gate.validate_sources(self.root))

    def test_missing_book_specification_rejected(self):
        name = gate.BASE + "JORDAN_ROMANCE_NAME_V1.md"
        (self.root / name).unlink()
        self.assertIn("REQUIRED_ARTIFACT_MISSING: " + name, gate.validate_sources(self.root))

    def test_falsely_claimed_campbell_facsimile_rejected(self):
        self.edit_json("source_coverage.json", lambda d: d["books"]["CAMPBELL_YOUR_DAYS_V1"].update(visual_verification="ALL_FACSIMILE_PAGES_VERIFIED"))
        self.assertIn("CAMPBELL_FACSIMILE_LIMIT_LOST", gate.validate_sources(self.root))

    def test_withdrawn_audit_error_stays_withdrawn(self):
        def change(data):
            for entry in data["systems"]["JAVANE_BUNKER_DIVINE_TRIANGLE_V1"]["entries"]:
                if entry["id"] == "JB-A21":
                    entry["status"] = "RETAINED_SOURCE_ISSUE"
        self.edit_json("ambiguities.json", change)
        self.assertIn("WITHDRAWN_AUDIT_ERROR_REINTRODUCED", gate.validate_sources(self.root))

    def test_rebaselining_manifest_cannot_hide_source_change(self):
        name = "JORDAN_ROMANCE_NAME_V1.md"
        path = self.root / gate.BASE / name
        path.write_text("not the source specification")
        self.edit_json("freeze_manifest.json", lambda d: d["files"].update({gate.BASE + name: gate.git_blob(path.read_bytes())}))
        self.assertIn("IMMUTABLE_BLOB_CHANGED: " + gate.BASE + "freeze_manifest.json", gate.validate_sources(self.root))


if __name__ == "__main__":
    unittest.main(verbosity=2)
