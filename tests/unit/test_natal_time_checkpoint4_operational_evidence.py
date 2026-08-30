from __future__ import annotations

import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from types import ModuleType

import pytest

from hdmatch.util import canonical_json_bytes, sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
ARTIFACT_PATH = PROJECT_ROOT / "state/NATAL-TIME-CHECKPOINT4-OPERATIONAL-EVIDENCE.json"


def _load_audit_module() -> ModuleType:
    path = PROJECT_ROOT / "scripts" / "audit_natal_time_checkpoint4_operational_evidence.py"
    spec = importlib.util.spec_from_file_location(
        "audit_natal_time_checkpoint4_operational_evidence", path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = _load_audit_module()


@pytest.fixture(scope="module")
def evidence() -> dict[str, object]:
    return AUDIT.build_operational_evidence(PROJECT_ROOT)


def test_operational_evidence_reproduces_and_is_non_scientific(
    evidence: dict[str, object],
) -> None:
    saved = json.loads(ARTIFACT_PATH.read_bytes())
    assert saved == evidence
    assert ARTIFACT_PATH.read_bytes() == canonical_json_bytes(evidence) + b"\n"
    unhashed = deepcopy(evidence)
    embedded = unhashed.pop("artifact_sha256")
    assert embedded == sha256_json(unhashed)
    classification = evidence["classification"]
    assert classification == {
        "operational_diagnostics_only": True,
        "scientific_identity_input": False,
        "scientific_result_input": False,
        "performance_guarantee": False,
        "deployment_or_railway_observation": False,
    }
    AUDIT.validate_operational_evidence(PROJECT_ROOT, saved)


def test_durable_write_span_is_only_an_observable_lower_bound(
    evidence: dict[str, object],
) -> None:
    diagnostics = evidence["durable_write_diagnostics"]
    assert len(diagnostics["observations"]) == 10
    assert diagnostics["observed_inode_birth_span_nanoseconds"] == 1_126_967_377_817
    assert diagnostics["observable_lower_bound_span_nanoseconds"] == 1_126_942_930_551
    assert diagnostics["observable_lower_bound_span_seconds"] == "1126.942930551"
    assert diagnostics["observable_lower_bound_span_iso8601"] == "PT18M46.942930551S"
    limits = " ".join(diagnostics["limits"])
    assert "not end-to-end" in limits
    assert "performance guarantee" in limits
    assert any("No end-to-end replay duration" in item for item in evidence["claim_limits"])


def test_lint_scopes_are_git_derived_and_legacy_debt_is_separate(
    evidence: dict[str, object],
) -> None:
    lint = evidence["changed_file_lint"]
    scopes = {item["scope_id"]: item for item in lint["path_scopes"]}
    assert set(scopes) == {"checkpoint4_evaluated_diff", "phase0_closure_diff"}
    assert scopes["checkpoint4_evaluated_diff"]["lint_changed_path_count"] == 7
    assert scopes["phase0_closure_diff"]["lint_changed_path_count"] == 7
    for scope in scopes.values():
        assert scope["observed_exit_code"] == 0
        assert scope["observed_stdout"] == "All checks passed!"
        assert scope["ruff_argv"] == [
            ".venv/bin/ruff",
            "check",
            *scope["lint_changed_paths"],
        ]
    baseline = lint["legacy_repo_wide_baseline"]
    assert baseline["observed_exit_code"] == 1
    assert baseline["observed_violation_count"] == 1812
    assert lint["phase1_paths_included"] is False
    assert "checkpoint 5" in lint["phase1_recording_boundary"]


def test_validator_rejects_rehashed_tamper(evidence: dict[str, object]) -> None:
    tampered = deepcopy(evidence)
    tampered["changed_file_lint"]["legacy_repo_wide_baseline"][
        "observed_violation_count"
    ] = 0
    tampered["artifact_sha256"] = sha256_json(
        {key: value for key, value in tampered.items() if key != "artifact_sha256"}
    )
    with pytest.raises(AUDIT.OperationalEvidenceError, match="does not reproduce exactly"):
        AUDIT.validate_operational_evidence(PROJECT_ROOT, tampered)
