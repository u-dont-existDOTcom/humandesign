from __future__ import annotations

import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from hdmatch.util import canonical_json_bytes, sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
PRE_CUSTODY_SOURCE = "daa59b8d84f6f7592303187afb1618791deaa175"
ARTIFACT_PATH = PROJECT_ROOT / "state" / "NATAL-TIME-CHECKPOINT5-ACCEPTANCE-MATRIX.json"


def _load_audit_module() -> ModuleType:
    path = PROJECT_ROOT / "scripts" / "audit_natal_time_checkpoint5_acceptance_matrix.py"
    spec = importlib.util.spec_from_file_location(
        "audit_natal_time_checkpoint5_acceptance_matrix", path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = _load_audit_module()


def _rehash(matrix: dict[str, Any]) -> None:
    payload = dict(matrix)
    payload.pop("matrix_sha256", None)
    matrix["matrix_sha256"] = sha256_json(payload)


def _minimal_matrix() -> dict[str, Any]:
    requirement = "Synthetic structural validator test requirement."
    entry = {
        "requirement_id": "TEST-ONLY",
        "origin": {
            "checkpoint": 5,
            "section": "test",
            "rule_ordinal": "1",
            "source_path": "docs/test.md",
            "source_document_sha256": "1" * 64,
        },
        "requirement": requirement,
        "requirement_sha256": AUDIT._sha256_bytes(requirement.encode("utf-8")),
        "requirement_domain": "test",
        "acceptance_dimensions": {
            "schema": True,
            "access_order": False,
            "metric_semantics": False,
            "provenance": False,
            "privacy": False,
        },
        "test_evidence": {
            "path": "tests/test.py",
            "test_name": "test_only",
            "test_source_blob_oid": "2" * 40,
            "test_source_sha256": "3" * 64,
        },
        "fixture_ids": [],
        "expected_outcome": {
            "kind": "committed_evidence_binding",
            "controlled_code": None,
            "invariants": [],
        },
        "actual_outcome": {
            "verification_state": "committed_evidence_and_test_binding_observed",
            "cases": [],
            "artifact": {
                "path": "state/test.json",
                "git_blob_oid": "4" * 40,
                "file_sha256": "5" * 64,
            },
        },
        "contract_bindings": [],
        "evaluator_binding": {
            "applicability": "not_applicable",
            "evaluator_version_sha256": None,
        },
        "source_binding": {
            "exact_source_commit": "6" * 40,
            "exact_source_tree_oid": "7" * 40,
        },
        "code_bindings": [],
        "custody_dependency": {"required": False, "pending_fields": []},
        "pro_minimum": False,
    }
    matrix: dict[str, Any] = {
        "schema_version": "natal-time-checkpoint5-acceptance-matrix-v1",
        "matrix_status": "finalized_post_custody_synthetic_only",
        "synthetic_only": True,
        "participant_records_accessed": 0,
        "exact_source": {"commit": "6" * 40, "tree_oid": "7" * 40},
        "requirement_sources": [],
        "contract_catalog": {},
        "evaluator_binding": {},
        "bundle_bindings": {
            "hidden_reference_content_included": False,
            "canonical_t_i_digest_included": False,
            "reference_custody_digest_included": False,
        },
        "entry_count": 1,
        "entries": [entry],
        "coverage_summary": {
            "checkpoint_entry_counts": {5: 1},
            "requirement_domain_counts": {"test": 1},
            "acceptance_dimension_counts": {"schema": 1},
            "pro_minimum_requirement_ids": [],
            "pro_minimums_complete": True,
            "pending_field_count": 0,
        },
    }
    _rehash(matrix)
    return matrix


def test_inventory_covers_every_checkpoint_rule_family_and_all_pro_minimums() -> None:
    requirements = AUDIT.REQUIREMENTS
    ids = [item.requirement_id for item in requirements]

    assert len(requirements) == 81
    assert len(ids) == len(set(ids))
    assert {item.checkpoint for item in requirements} == {1, 2, 3, 4, 5}
    assert all(item.dimensions for item in requirements)
    assert all(set(item.dimensions) <= set(AUDIT.DIMENSIONS) for item in requirements)
    assert {
        "CP4-FULL-C",
        "CP4-CANONICAL-REORDER",
        "CP4-REPEATED-STATE-COUNTS",
        "CP5-ACCESS-BINDING-EVERY-VALID",
        "CP5-REHASHED-FORBIDDEN-FIELD",
    } == AUDIT.PRO_MINIMUM_IDS
    assert {
        "evidence_state",
        "engine_identity",
        "replay",
        "study_design",
        "metric_semantics",
        "custody",
        "subset_semantics",
        "reference_domain",
        "schema_closure",
        "privacy",
    } <= {item.domain for item in requirements}


def test_custody_and_reference_fixture_inventory_has_exact_controlled_codes() -> None:
    by_id = {item.requirement_id: item for item in AUDIT.REQUIREMENTS}
    expected_codes = {
        "CP5-EARLY-RAW-BYTE": "early_reference_raw_byte_access",
        "CP5-EARLY-DIGEST": "early_reference_digest_access",
        "CP5-EARLY-METADATA": "early_reference_metadata_access",
        "CP5-EARLY-ALTERNATE-LOADER": "early_reference_alternate_loader_access",
        "CP5-POSTACCESS-T-MUTATION": "t_i_mutated_after_evaluator_access",
        "CP5-DISCONNECTED-DUPLICATE": "duplicate_selected_interval",
        "CP5-MANUFACTURED-SPAN": "manufactured_interval_not_allowed",
        "CP5-REFERENCE-PARTIAL-BEFORE": "reference_domain_partially_incompatible",
        "CP5-REFERENCE-PARTIAL-AFTER": "reference_domain_partially_incompatible",
        "CP5-REFERENCE-PARTIAL-BOTH": "reference_domain_partially_incompatible",
        "CP5-REFERENCE-OUTSIDE": "reference_domain_incompatible",
        "CP5-REFERENCE-ENDPOINT-ONLY": "reference_domain_incompatible",
        "CP5-REFERENCE-MULTIDATE-EXCLUDED": "reference_domain_incompatible",
    }
    assert {
        requirement_id: by_id[requirement_id].expected_code for requirement_id in expected_codes
    } == expected_codes
    assert all(by_id[requirement_id].fixture_ids for requirement_id in expected_codes)
    assert by_id["CP5-REFERENCE-CONTAINED-ONE"].expected_receipt_kind == (
        "descriptive_metric_receipt"
    )
    assert by_id["CP5-REFERENCE-CONTAINED-ADJACENT"].expected_receipt_kind == (
        "descriptive_metric_receipt"
    )
    assert by_id["CP5-REFERENCE-MULTIDATE-INCLUDED"].expected_receipt_kind == (
        "descriptive_metric_receipt"
    )


def test_generation_fails_closed_for_known_pre_custody_source() -> None:
    with pytest.raises(
        AUDIT.AcceptanceMatrixError,
        match="required committed custody/evidence file is missing",
    ):
        AUDIT.build_acceptance_matrix(PROJECT_ROOT, source_commit=PRE_CUSTODY_SOURCE)


def test_structural_validator_accepts_typed_na_and_rejects_pending_or_duplicates() -> None:
    matrix = _minimal_matrix()
    AUDIT.validate_matrix_structure(matrix, required_ids=frozenset({"TEST-ONLY"}))

    pending = deepcopy(matrix)
    pending["entries"][0]["custody_dependency"]["pending_fields"] = ["receipt_sha256"]
    _rehash(pending)
    with pytest.raises(AUDIT.AcceptanceMatrixError, match="pending fields"):
        AUDIT.validate_matrix_structure(pending, required_ids=frozenset({"TEST-ONLY"}))

    duplicated = deepcopy(matrix)
    duplicated["entries"].append(deepcopy(duplicated["entries"][0]))
    duplicated["entry_count"] = 2
    _rehash(duplicated)
    with pytest.raises(AUDIT.AcceptanceMatrixError, match="duplicate requirement IDs"):
        AUDIT.validate_matrix_structure(duplicated, required_ids=frozenset({"TEST-ONLY"}))


def test_structural_validator_rejects_malformed_digest_and_custody_disclosure() -> None:
    matrix = _minimal_matrix()
    case = {
        "fixture_id": "SYNTH-FIXTURE-TEST",
        "controlled_status": "descriptive_metric_receipt",
        "controlled_code": None,
        "expectation_matched": True,
        "digest_evidence": {
            "inference_visible_fixture": {
                "applicability": "applicable",
                "sha256": "not-a-digest",
            },
            "receipt": {"applicability": "applicable", "sha256": "8" * 64},
            "access_state": {"applicability": "not_applicable", "sha256": None},
        },
    }
    matrix["entries"][0]["actual_outcome"]["cases"] = [case]
    _rehash(matrix)
    with pytest.raises(AUDIT.AcceptanceMatrixError, match="applicable digest is malformed"):
        AUDIT.validate_matrix_structure(matrix, required_ids=frozenset({"TEST-ONLY"}))

    disclosed = _minimal_matrix()
    disclosed["bundle_bindings"]["reference_custody_sha256"] = "9" * 64
    _rehash(disclosed)
    with pytest.raises(AUDIT.AcceptanceMatrixError, match="forbidden custody material"):
        AUDIT.validate_matrix_structure(disclosed, required_ids=frozenset({"TEST-ONLY"}))


def test_rehashed_requirement_or_matrix_tamper_fails_closed() -> None:
    matrix = _minimal_matrix()
    matrix["entries"][0]["requirement"] = "Changed after the requirement hash was frozen."
    _rehash(matrix)
    with pytest.raises(AUDIT.AcceptanceMatrixError, match="requirement digest mismatch"):
        AUDIT.validate_matrix_structure(matrix, required_ids=frozenset({"TEST-ONLY"}))

    self_hash = _minimal_matrix()
    self_hash["coverage_summary"]["pending_field_count"] = 1
    with pytest.raises(AUDIT.AcceptanceMatrixError, match="matrix self-hash mismatch"):
        AUDIT.validate_matrix_structure(self_hash, required_ids=frozenset({"TEST-ONLY"}))


def test_saved_matrix_reproduces_from_its_exact_source_commit() -> None:
    saved = json.loads(ARTIFACT_PATH.read_bytes())
    assert saved["entry_count"] == 81
    assert saved["coverage_summary"]["pending_field_count"] == 0
    assert saved["coverage_summary"]["pro_minimums_complete"] is True
    assert ARTIFACT_PATH.read_bytes() == canonical_json_bytes(saved) + b"\n"
    AUDIT.validate_acceptance_matrix(PROJECT_ROOT, saved)
