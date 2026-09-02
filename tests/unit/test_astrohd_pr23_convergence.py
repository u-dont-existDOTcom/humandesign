from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).parents[2]
AUDIT_PATH = ROOT / "reference/audits/astrohd_pr23_convergence_v1.json"
BASE_COMMIT = "afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286"
AUDITED_HEAD = "b3da97274c161a31e44cee3ef4159ca0d1d9a0dd"


def _auditor() -> ModuleType:
    path = ROOT / "scripts/audit_astrohd_pr23_convergence.py"
    spec = importlib.util.spec_from_file_location("audit_astrohd_pr23_convergence", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load() -> dict[str, Any]:
    payload = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _source_hashes() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((ROOT / "src/hdmatch").rglob("*.py"))
    }


def _require_bound_git_history() -> None:
    for ref in (BASE_COMMIT, AUDITED_HEAD):
        available = subprocess.run(
            ("git", "cat-file", "-e", f"{ref}^{{commit}}"),
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        if available.returncode != 0:
            pytest.skip(f"shallow checkout does not contain bound audit commit {ref}")


def test_audited_git_boundary_is_exact() -> None:
    audit = _load()

    assert audit["schema_version"] == "astrohd-pr23-convergence-audit-v1"
    assert audit["status"] == "mechanical_final_pr_convergence_audit_no_runtime_effect"
    assert audit["base_commit"] == BASE_COMMIT
    assert audit["audited_head"] == AUDITED_HEAD


def test_changed_file_inventory_reproduces_from_git() -> None:
    _require_bound_git_history()
    auditor = _auditor()

    assert _load()["pr_delta_inventory"] == auditor._pr_delta_inventory(ROOT)


def test_owner_correction_literal_scan_reproduces() -> None:
    _require_bound_git_history()
    auditor = _auditor()
    scan = _load()["owner_correction_remnant_scan"]

    assert scan == auditor._owner_correction_remnant_scan(ROOT)
    assert scan["state_surfaces"]["classification"] == (
        "historical_or_state_records_not_runtime_scan"
    )


def test_production_runtime_symbol_scan_contains_zero_forbidden_identifiers() -> None:
    scan = _load()["runtime_symbol_scan"]

    assert scan["expected_production_runtime_occurrence_count"] == 0
    assert scan["occurrence_count"] == 0
    assert scan["occurrences"] == []


def test_rank_order_and_equality_keys_match_corrected_specification() -> None:
    participant = _load()["rank_semantics"]["participant_backend"]

    assert participant["rank_ordering_key_expressions"] == [
        "-scores[state.state_id].net_rubric_bits",
        "scores[state.state_id].meaningful_contradictions",
        "-scores[state.state_id].detailed_support",
        "-(state.end_utc - state.start_utc).total_seconds()",
        "state.start_utc",
    ]
    assert participant["evidence_tie_key_expressions"] == [
        "round(score.net_rubric_bits, 12)",
        "score.meaningful_contradictions",
        "round(score.detailed_support, 12)",
    ]
    assert participant["core_fit_in_rank_ordering_key"] is False
    assert participant["core_fit_in_evidence_tie_key"] is False
    assert participant["top_net_margin"]["unchanged_from_rank_correction_start"] is True


def test_date_best_state_key_and_other_date_code_match_specification() -> None:
    date = _load()["rank_semantics"]["date_aggregator"]

    assert date["best_state_key_expressions"] == [
        "item.net_rubric_bits",
        "-item.meaningful_contradictions",
        "item.detailed_support",
        "item.state_id",
    ]
    assert date["core_fit_in_best_state_key"] is False
    assert date["date_score_and_midrank_source_unchanged_except_directed_core_fit_removal"] is True


def test_no_core_fit_occurrence_is_in_a_ranking_key_context() -> None:
    inventory = _load()["core_fit_usage_inventory"]

    assert inventory["occurrences"]
    assert inventory["key_context_occurrence_count"] == 0
    assert inventory["key_context_occurrences"] == []


def test_theory_language_feature_has_no_external_production_importer_or_caller() -> None:
    isolation = _load()["theory_language_runtime_isolation"]

    assert isolation["defining_module"] == ("src/hdmatch/evaluation/theory_language_exposure.py")
    assert isolation["public_symbols"]
    assert isolation["importer_count_outside_defining_module"] == 0
    assert isolation["imports_outside_defining_module"] == []
    assert isolation["call_site_count_outside_defining_module"] == 0
    assert isolation["call_sites_outside_defining_module"] == []


def test_seven_future_core_rows_retain_all_authorizations_false() -> None:
    invariant = _load()["future_core_authorization_invariant"]

    assert invariant["row_count"] == 7
    assert invariant["target_ids"] == [
        "authority.ego_manifested",
        "authority.ego_projected",
        "authority.lunar",
        "authority.mental_environmental",
        "authority.self_projected",
        "type_strategy.manifestor",
        "type_strategy.reflector",
    ]
    assert all(
        row["authorization_fields"]
        == {
            "mapping_authorized": False,
            "owner_policy": False,
            "question_change_authorized": False,
            "runtime_authorized": False,
        }
        for row in invariant["rows"]
    )


def test_mapping_and_question_bank_hashes_and_frozen_counts_match() -> None:
    invariant = _load()["mapping_question_bank_invariants"]

    assert invariant["mapping_library"]["sha256"] == (
        "3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200"
    )
    assert invariant["question_bank"]["sha256"] == (
        "31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820"
    )
    assert invariant["mapping_library"]["stored_frozen_mapping_count"] == 27
    assert invariant["distinct_frozen_rule_count"] == 27
    assert invariant["distinct_frozen_mapped_prompt_count"] == 23
    assert invariant["descriptive_only_not_a_completeness_denominator"] is True


def test_historical_audits_retain_hashes_and_generators_fail_closed() -> None:
    invariant = _load()["historical_audit_invariants"]
    hashes = {row["path"]: row["sha256"] for row in invariant["artifacts"]}

    assert hashes == {
        "reference/audits/astrohd_cross_class_core_fit_v1.json": (
            "a113fb53de13f38d5053955975912a1fb194f527c57f610c82d0efc38bc32a70"
        ),
        "reference/audits/astrohd_rank_tiebreak_downstream_v1.json": (
            "c9fb9ee6060c4bbb346c7ac6981a543d3d602a60bb1da83e245cea638a680103"
        ),
    }
    assert len(invariant["generator_results_against_current_source"]) == 2
    assert all(
        row["exception_class"] == "HistoricalAuditSourceMismatch" and row["output_created"] is False
        for row in invariant["generator_results_against_current_source"]
    )


def test_freeze_compatibility_retains_exact_source_commit_binding() -> None:
    binding = _load()["freeze_runtime_binding"]

    assert binding["source_commit_binding"] == {
        "active_runtime_expression": "self.code_commit",
        "frozen_expression": "freeze.code_commit",
        "present": True,
    }
    assert [row["field"] for row in binding["bound_fields"]] == [
        "source commit",
        "chart engine",
        "model version",
        "model bytes",
        "mapping bytes",
        "question bank version",
        "question bank bytes",
    ]


def test_coordination_document_headings_are_recorded_mechanically() -> None:
    rows = _load()["coordination_document_headings"]

    assert [row["path"] for row in rows] == [
        "CURRENT_PLAN.md",
        "docs/36_astrohd_owner_pilot.md",
        "state/CURRENT-STATE.md",
        "state/OWNER-CORRECTION-2026-09-02.md",
    ]
    assert all(row["first_h1"] is not None and len(row["sha256"]) == 64 for row in rows)


def test_generated_json_regenerates_without_modifying_production_source(tmp_path: Path) -> None:
    _require_bound_git_history()
    auditor = _auditor()
    before = _source_hashes()
    output = tmp_path / AUDIT_PATH.name

    auditor.write_audit(ROOT, output=output)

    assert output.read_bytes() == AUDIT_PATH.read_bytes()
    assert _source_hashes() == before
