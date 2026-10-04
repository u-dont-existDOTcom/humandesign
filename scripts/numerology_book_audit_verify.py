#!/usr/bin/env python3
"""Verify the exact audit artifacts, not the truth of numerology or every paraphrase.

Default acceptance also checks Git ordering and executes both task-local test
suites. --working-tree is a pre-commit check, never a remote-publication receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/six-rule-life-timing-20261001"
TASK = "NUMEROLOGY-BOOK-AUDIT-20261004"
FREEZE_COMMIT = "af2cbf287635a682d1cdb36597d5a9c47784743c"
FREEZE_BLOB = "67748cc5a47e3aa552f4c9f40c5102c3a41dfa3b"
BASE = "reference/research/numerology_v2_20261004/"
BASELINE = {
    "reference/research/NUMEROLOGY_METHODOLOGY_AUDIT_V1_20261003.md": "e09a0201eab09078ee8df34204b9a02d90cb45a0",
    "reference/research/numerology_method_registry_v1_20261003.json": "9cf4a28bab2f8c9714c1c01fb503e918b3e29734",
}
SYSTEMS = {"CHEIRO_CHALDEAN_V2", "CAMPBELL_YOUR_DAYS_V1", "JORDAN_ROMANCE_NAME_V1", "JAVANE_BUNKER_DIVINE_TRIANGLE_V1"}
INHERITED = {"CHEIRO_CHALDEAN_V1", "DECOZ_CURRENT_V1"}
DIMENSIONS = {"edition_chapters", "birth_date_hierarchy", "name_roles_changes_activation", "letter_mapping_vowels_normalization", "reduction_compounds_special_numbers", "all_personality_chart_layers", "all_timing_formulas_boundaries_recurrence", "relationship_marriage_compatibility", "event_interpretation_tables", "astrology_tarot_peripherals", "ambiguities_conflicts"}
CHRONOLOGY = ["documentary/contemporaneous", "strongly anchored memory", "approximate memory", "uncertain"]


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load_json(root: Path, name: str, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads((root / name).read_text())
        if not isinstance(value, dict):
            raise ValueError("top level is not an object")
        return value
    except (OSError, ValueError) as exc:
        errors.append(f"INVALID_OR_MISSING_JSON: {name}: {str(exc)[:100]}")
        return {}


def match_file(root: Path, name: str, expected: str, errors: list[str]) -> None:
    try:
        actual = git_blob((root / name).read_bytes())
        if actual != expected:
            errors.append(f"IMMUTABLE_BLOB_CHANGED: {name}")
    except OSError:
        errors.append(f"REQUIRED_ARTIFACT_MISSING: {name}")


def validate_sources(root: Path) -> list[str]:
    errors: list[str] = []
    match_file(root, BASE + "freeze_manifest.json", FREEZE_BLOB, errors)
    manifest = load_json(root, BASE + "freeze_manifest.json", errors)
    for name, expected in {**manifest.get("files", {}), **BASELINE}.items():
        match_file(root, name, expected, errors)
    if set(manifest.get("systems", [])) != SYSTEMS or manifest.get("status") != "FROZEN_WITH_EXPLICIT_SOURCE_BRANCHES":
        errors.append("FREEZE_SYSTEM_SET_OR_STATUS_CHANGED")
    registry = load_json(root, "reference/research/numerology_method_registry_v2_20261004.json", errors)
    if set(registry.get("systems", {})) != SYSTEMS:
        errors.append("REGISTRY_SYSTEM_SET_INCOMPLETE")
    inherited = registry.get("inherited_unchanged", {})
    if set(inherited.get("system_keys", [])) != INHERITED:
        errors.append("INHERITED_SYSTEM_SET_CHANGED")
    coverage = load_json(root, BASE + "source_coverage.json", errors)
    books = coverage.get("books", {})
    if set(books) != SYSTEMS:
        errors.append("FOUR_BOOK_COVERAGE_MISSING")
    for system in SYSTEMS:
        record = books.get(system, {})
        if record.get("full_source_pass") is not True or record.get("front_and_back_matter_read") is not True or record.get("unread_major_sections") != [] or not record.get("numbered_sections") or not record.get("bank_inventory"):
            errors.append(f"INCOMPLETE_DECLARED_SOURCE_COVERAGE: {system}")
        if not re.fullmatch(r"[a-f0-9]{64}", str(record.get("input_sha256", ""))):
            errors.append(f"SOURCE_HASH_MISSING: {system}")
        if record.get("spec_git_blob") != registry.get("systems", {}).get(system, {}).get("spec_git_blob"):
            errors.append(f"SPECIFICATION_CROSSWALK_MISMATCH: {system}")
    if books.get("CAMPBELL_YOUR_DAYS_V1", {}).get("visual_verification") != "NO_SOURCE_IMAGES_IN_UPLOAD":
        errors.append("CAMPBELL_FACSIMILE_LIMIT_LOST")
    crosswalk = coverage.get("requirement_crosswalk", {})
    if set(crosswalk) != DIMENSIONS:
        errors.append("REQUIRED_DIMENSION_CROSSWALK_INCOMPLETE")
    for dimension in DIMENSIONS:
        values = crosswalk.get(dimension, {})
        if set(values) != SYSTEMS or not all(isinstance(v, str) and v.strip() for v in values.values()):
            errors.append(f"SOURCE_LAYER_CROSSWALK_INCOMPLETE: {dimension}")
    ambiguities = load_json(root, BASE + "ambiguities.json", errors)
    entries = [e for value in ambiguities.get("systems", {}).values() for e in value.get("entries", [])]
    ids = [e.get("id") for e in entries]
    if len(ids) != len(set(ids)) or not ids:
        errors.append("AMBIGUITY_IDS_INVALID")
    withdrawn = [e for e in entries if e.get("id") == "JB-A21"]
    if len(withdrawn) != 1 or withdrawn[0].get("status") != "WITHDRAWN_AUDIT_ERROR":
        errors.append("WITHDRAWN_AUDIT_ERROR_REINTRODUCED")
    fixtures = load_json(root, BASE + "formula_fixtures.json", errors)
    cases = fixtures.get("fixtures", [])
    if len(cases) != 75 or len({f.get("id") for f in cases}) != 75 or {f.get("system_id") for f in cases} != SYSTEMS:
        errors.append("SOURCE_FIXTURE_CORPUS_INCOMPLETE")
    rows = fixtures.get("cayce_table", {}).get("rows", [])
    if [r.get("year") for r in rows] != list(range(1877, 1945)):
        errors.append("WORKED_68_YEAR_TABLE_INCOMPLETE")
    return errors


def validate_design(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("source_freeze_commit") != FREEZE_COMMIT or data.get("status") != "DESIGN_COMPLETE_NOT_LAUNCHED":
        errors.append("DESIGN_SOURCE_BOUNDARY_INVALID")
    if set(data.get("principal_arms", [])) != SYSTEMS | {"DECOZ_CURRENT_V1"}:
        errors.append("FULL_AUTHOR_ARM_SET_INCOMPLETE")
    if data.get("relationship_ablation", {}).get("system_id") != "CHEIRO_CHALDEAN_V1":
        errors.append("CHEIRO_V1_ABLATION_LOST")
    for key in ("study_launched", "participant_predictions_created", "owner_history_fit_performed", "launch_ready"):
        if data.get(key) is not False:
            errors.append(f"UNAUTHORIZED_OR_UNESTABLISHED_ACTIVITY: {key}")
    if data.get("operational_manifest") is not None:
        errors.append("UNESTABLISHED_OPERATIONAL_FREEZE")
    controls = data.get("constraints", {})
    expected = {
        "full_relevant_system_per_arm": True, "personal_year_only_is_full_decoz": False,
        "separate_author_outputs": True, "average_incompatible_outputs": False,
        "operational_freeze_before_outcomes": True, "post_outcome_branch_selection": False,
        "unknown_period_label": "UNKNOWN", "unknown_is_negative": False,
        "owner_history_status": "DEVELOPMENT_ONLY", "chronology_quality": CHRONOLOGY,
        "impact_independent_of_numerology": True, "duplicate_event_credit": False,
        "broad_intervals_pay_observed_exposure": True, "abstention_is_negative": False,
        "coverage_report_required": True, "untouched_person_or_prospective_validation": True,
        "person_cluster_split": True, "no_rule_rescue": True, "peripheral_modules_default": "DISABLED",
    }
    for key, value in expected.items():
        if controls.get(key) != value:
            errors.append(f"EMPIRICAL_CONTROL_VIOLATION: {key}")
    costs = [controls.get(k) for k in ("false_positive_cost", "false_negative_cost", "true_positive_reward")]
    if any(type(v) not in (int, float) for v in costs) or costs != [1, 1, 1]:
        errors.append("SYMMETRIC_ERROR_ACCOUNTING_CHANGED")
    if data.get("owner_2008", {}).get("impact") != "moderate_not_top_major" or data.get("owner_2008", {}).get("chronology_quality") != "approximate memory":
        errors.append("OWNER_2008_CORRECTION_LOST")
    prerequisites = {p.get("id"): p for p in data.get("open_launch_prerequisites", [])}
    required = {"official_decoz_resources", "campbell_hybrid_scope", "operational_interpretation_freeze", "independent_implementation_review", "cohort_observation_and_privacy", "endpoints_and_precision", "sealed_execution_release"}
    if set(prerequisites) != required or any(p.get("status") != "OPEN" or not p.get("requires") for p in prerequisites.values()):
        errors.append("LAUNCH_PREREQUISITES_MISREPRESENTED")
    return errors


def validate_review(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("status") not in {"CHECKED_WITH_RECONCILIATION", "CHECKED_NO_MATERIAL_FINDINGS", "UNAVAILABLE_SCOPE_EXPLICIT"}:
        errors.append("CLOSEOUT_REVIEW_DISPOSITION_MISSING")
    if not data.get("review_boundary") or data.get("full_primary_corpus_independently_certified") is not False:
        errors.append("INDEPENDENT_REVIEW_SCOPE_OVERCLAIM")
    if data.get("unresolved_blocking_findings") != []:
        errors.append("UNRESOLVED_BLOCKING_REVIEW_FINDING")
    return errors


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True, check=False)


def validate_history(root: Path) -> list[str]:
    errors: list[str] = []
    if git(root, "merge-base", "--is-ancestor", FREEZE_COMMIT, "HEAD").returncode:
        errors.append("SOURCE_FREEZE_NOT_ANCESTOR")
    for path in [BASE + "EMPIRICAL_COMPARISON_DESIGN.md", BASE + "empirical_admission_contract.json"]:
        commits = git(root, "log", "--diff-filter=A", "--format=%H", "--", path).stdout.splitlines()
        if not commits:
            errors.append(f"DESIGN_NOT_COMMITTED: {path}")
        elif commits[-1] == FREEZE_COMMIT or git(root, "merge-base", "--is-ancestor", FREEZE_COMMIT, commits[-1]).returncode:
            errors.append(f"DESIGN_NOT_AFTER_SOURCE_FREEZE: {path}")
    return errors


def validate_task(root: Path, preflight: bool, working_tree: bool) -> list[str]:
    errors: list[str] = []
    lock = load_json(root, "tasks/ACTIVE-TASK.json", errors)
    if git(root, "branch", "--show-current").stdout.strip() != BRANCH or lock.get("requiredBranch") != BRANCH or lock.get("taskId") != TASK or lock.get("exclusive") is not True:
        errors.append("TASK_BRANCH_IDENTITY_MISMATCH")
    for path, expected in BASELINE.items():
        match_file(root, path, expected, errors)
    if preflight:
        return errors
    errors.extend(validate_sources(root))
    design = load_json(root, BASE + "empirical_admission_contract.json", errors)
    errors.extend(validate_design(design))
    for name in ["EMPIRICAL_COMPARISON_DESIGN.md", "AUDIT_COMPLETION_REPORT.md", "closeout_claim_ledger.json", "closeout_review_receipt.json"]:
        if not (root / BASE / name).is_file():
            errors.append(f"REQUIRED_ARTIFACT_MISSING: {name}")
    review = load_json(root, BASE + "closeout_review_receipt.json", errors)
    errors.extend(validate_review(review))
    policy = (root / "docs/24_numerology_methodology_policy.md").read_text()
    if any(system not in policy for system in SYSTEMS | INHERITED) or any(term not in policy for term in ("UNKNOWN", "DEVELOPMENT", "Duality", "No rule creep", "chronology")):
        errors.append("POLICY_CONTROL_REFERENCE_MISSING")
    old_path = "experiments/astrohd/chaldean_life_event_retrodiagnostic_20261003.json"
    historical = load_json(root, old_path, errors)
    if historical.get("periodicity_labels", {}).get("2008", {}).get("impact") != "moderate_not_top_major":
        errors.append("HISTORICAL_2008_LABEL_WRONG")
    annotation = historical.get("historical_snapshot_annotation", {})
    if annotation.get("new_fit_performed") is not False or annotation.get("background_counts_are_observed_negatives") is not False or annotation.get("specificity_claim_admissible") is not False:
        errors.append("HISTORICAL_UNKNOWN_NEGATIVES_MISREPRESENTED")
    original = git(root, "show", f"{FREEZE_COMMIT}:{old_path}")
    if original.returncode == 0:
        prior = json.loads(original.stdout)
        for key in ("event_years", "coarse_year_root_result", "birth_year_periodicity", "known_periodicity_hit"):
            if historical.get(key) != prior.get(key):
                errors.append(f"HISTORICAL_RESULTS_REWRITTEN: {key}")
    else:
        errors.append("HISTORICAL_BASELINE_UNAVAILABLE")
    if not working_tree:
        errors.extend(validate_history(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    flags = parser.add_mutually_exclusive_group()
    flags.add_argument("--preflight", action="store_true")
    flags.add_argument("--working-tree", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate_task(ROOT, args.preflight, args.working_tree)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [f"ACCEPTANCE_INPUT_ERROR: {type(exc).__name__}: {str(exc)[:180]}"]
    test_result: dict[str, Any] = {"status": "NOT_RUN_PREFLIGHT"}
    if not args.preflight:
        run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_numerology_book_*.py"], cwd=ROOT, capture_output=True, text=True, check=False)
        test_result = {"status": "PASS" if run.returncode == 0 else "FAIL", "output": (run.stdout + run.stderr).strip()}
        if run.returncode:
            errors.append("TASK_TESTS_FAILED")
    report = {"task": TASK, "mode": "preflight" if args.preflight else "working_tree_precommit" if args.working_tree else "committed_artifact_acceptance", "status": "FAIL" if errors else "PASS", "head": git(ROOT, "rev-parse", "HEAD").stdout.strip(), "source_freeze_commit": FREEZE_COMMIT, "findings": errors, "tests": test_result, "mechanical_scope": "artifact identity, declared coverage, immutable baselines, protocol controls and source arithmetic", "semantic_completeness_certified_by_this_script": False, "predictive_validity_tested": False, "study_launch_ready": False, "remote_publication_verified_by_this_script": False}
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
