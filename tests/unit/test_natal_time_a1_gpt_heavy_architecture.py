from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest

from tests.a1_gpt_heavy.validator import (
    ValidationFailure,
    load_fixture,
    validate_record,
)

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"
DOCS = ROOT / "docs"
FIXTURES = ROOT / "tests" / "fixtures" / "a1_gpt_heavy"
CORRECTED_BASELINE = "497bfed7c554c52dc3b22b2548b41fef844c84a9"
CONCEPTION_COMMIT = "5091d16fd22e78ed2147b4de839bbd8e99e00e0c"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def test_owner_source_and_corrected_baseline_are_exact() -> None:
    source = load_json(STATE / "NATAL-TIME-OWNER-A1-GPT-HEAVY-SOURCE-EPOCH8-20260831.json")
    exact = source["message_text_exact"].encode("utf-8")
    assert len(exact) == source["message_byte_length"] == 56
    assert exact.hex() == source["message_utf8_hex"]
    assert hashlib.sha256(exact).hexdigest() == source["message_sha256"]
    assert (
        source["message_sha256"]
        == "97ce6179532c73e9668a5cff47b41006f49a536cf76e449084f3834847d28e59"
    )
    contract = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-GOVERNANCE-CONTRACT-V1.json")
    assert contract["owner_source"]["eligibility_verdict"] == "NOT_MADE"
    reconciliation = load_json(
        STATE / "NATAL-TIME-A1-GPT-HEAVY-OBJECTIVE-RECONCILIATION-EPOCH8-V1.json"
    )
    assert reconciliation["corrected_baseline"]["head"] == CORRECTED_BASELINE
    assert (
        reconciliation["corrected_baseline"]["tree"] == "9e4777142c7e08f605b4e50b848d1ca985b5ac70"
    )


def test_conception_is_frozen_and_precedes_all_scan_work() -> None:
    document = DOCS / "NATAL_TIME_A1_GPT_HEAVY_PREELICITATION_CONCEPTION_20260831.md"
    state = STATE / "NATAL-TIME-A1-GPT-HEAVY-PREELICITATION-CONCEPTION-V1.json"
    assert sha256(document) == "05cbce1ae583d9a188bfc0f11d1d8d97741c97f83007e9a82ff1d91e4e178a96"
    assert sha256(state) == "05117102b5b88b3041657d3bfe25885b0c77231484e3dfe8ce772eab81f212f3"
    ledger = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-SOURCE-LEDGER-V1.json")
    assert ledger["conception_commit"] == CONCEPTION_COMMIT
    assert ledger["scan_started_after_conception_commit"] is True
    assert git("merge-base", "--is-ancestor", CONCEPTION_COMMIT, "HEAD") == ""
    text = document.read_text(encoding="utf-8")
    for prohibited in ("http://", "https://", "doi.org", "NIST", "W3C", "CRediT", "COREQ", "SRQR"):
        assert prohibited not in text


def test_methods_scan_is_bounded_exact_and_classified_once() -> None:
    sources = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-SOURCE-LEDGER-V1.json")
    assert sources["query_count"] == len(sources["queries"]) == 24
    assert [item["sequence"] for item in sources["queries"]] == list(range(1, 25))
    assert {item["date"] for item in sources["queries"]} == {"2026-08-31"}
    query_text = "\n".join(item["query"] for item in sources["queries"]).lower()
    for prohibited in ("astrohd", "human design", "birth chart", "relationship chart"):
        assert prohibited not in query_text
    assert sources["construct_specific_search_count"] == 0
    assert sources["instrument_specific_search_count"] == 0
    assert sources["mapping_search_count"] == 0
    assert sources["included_source_count"] == 18
    assert sources["excluded_source_count"] == 5
    assert sources["askrigor"]["forum_signal"]["state"] == "NOT_TRIGGERED"
    assert sources["askrigor"]["full_text_audit"]["segments_retrieved"] == 89
    assert sources["askrigor"]["full_text_audit"]["segments_total"] == 89

    methods = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-METHODS-DECISION-LEDGER-V1.json")
    families = methods["families"]
    assert methods["method_family_count"] == len(families) == 19
    assert len({item["method_family_id"] for item in families}) == len(families)
    assert all(item["classification"] in methods["allowed_classifications"] for item in families)
    assert methods["one_classification_per_family"] is True
    assert methods["selected_method_family_ids"] == []
    for field in (
        "selected_model",
        "selected_provider",
        "selected_model_version",
        "selected_prompt",
        "selected_evidence_standard",
        "selected_threshold",
        "selected_reconciliation_rule",
        "selected_human_procedure",
    ):
        assert methods[field] is None


def _object_nodes(schema: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    if schema.get("type") == "object":
        nodes.append(schema)
    for value in schema.values():
        if isinstance(value, dict):
            nodes.extend(_object_nodes(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    nodes.extend(_object_nodes(item))
    return nodes


def test_custody_schema_is_closed_and_content_free() -> None:
    schema = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-CUSTODY-SCHEMA-V1.json")
    assert all(node.get("additionalProperties") is False for node in _object_nodes(schema))
    prohibited = set(schema["x-prohibited-field-names"])
    for field in (
        "question",
        "prompt",
        "content",
        "construct",
        "instrument",
        "chart",
        "relationship",
        "mapping_result",
        "eligibility_outcome",
    ):
        assert field in prohibited
    record = load_fixture("valid_complete_metadata.json")
    assert record["real_person_record"] is False
    assert record["human_facing_content_present"] is False
    assert record["semantic_content_present"] is False
    assert record["eligibility_outcome_present"] is False
    assert record["selected_configuration_present"] is False
    validate_record(record)


def _set_path(record: dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    target: Any = record
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    final = parts[-1]
    if isinstance(target, list):
        target[int(final)] = value
    else:
        target[final] = value


@pytest.mark.parametrize(
    "case",
    load_json(FIXTURES / "hostile_cases.json")["cases"],
    ids=lambda case: case["case_id"],
)
def test_hostile_synthetic_cases_fail_closed(case: dict[str, Any]) -> None:
    record = copy.deepcopy(load_fixture("valid_complete_metadata.json"))
    _set_path(record, case["path"], case["value"])
    with pytest.raises(ValidationFailure) as error:
        validate_record(record)
    assert error.value.code == case["expected_code"], str(error.value)


def test_roles_contexts_and_owner_author_events_are_distinct() -> None:
    matrix = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-ROLE-ACCESS-MATRIX-V1.json")
    assert {item["role_id"] for item in matrix["roles"]} == {
        "ASTROHD_AWARE_GOVERNANCE_GPT",
        "ISOLATED_GPT_ADJUDICATION_RUN",
        "GPT_ADJUDICATION_RECONCILIATION",
        "ISOLATED_CHART_BLIND_CONTENT_SUPPORT_GPT",
        "JOEL_AUTHOR",
        "JOEL_OWNER",
    }
    assert matrix["real_person_assignments"] == []
    assert matrix["current_access_grants"] == []
    assert not any(matrix["access_invariants"].values())
    conflict = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-OWNER-AUTHOR-CONFLICT-CONTRACT-V1.json")
    assert conflict["events_interchangeable"] is False
    assert conflict["owner_event_can_satisfy_semantic_acceptance"] is False
    assert conflict["author_event_can_override_gpt_adjudication"] is False
    assert (
        conflict["lack_of_hd_interpretation_knowledge"]["eligibility_effect"] == "NON_DISPOSITIVE"
    )
    assert conflict["single_author_limit"]["cross_author_robustness_claim_allowed"] is False


def test_adjudication_topology_separates_runs_models_and_reconciliation() -> None:
    topology = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-ADJUDICATION-TOPOLOGY-V1.json")
    assert len(topology["initial_run_slots"]) == 2
    assert {item["slot_id"] for item in topology["initial_run_slots"]} == {
        "GPT_INITIAL_RUN_SLOT_A",
        "GPT_INITIAL_RUN_SLOT_B",
    }
    assert all(
        item["peer_unsealed_access_allowed"] is False for item in topology["initial_run_slots"]
    )
    assert topology["reconciliation_slot"]["initial_outputs_immutable"] is True
    assert topology["reconciliation_slot"]["disagreement_must_remain_visible"] is True
    assert topology["same_model_multiple_runs_claim"] == "INDEPENDENT_RUNS_NOT_INDEPENDENT_MODELS"
    assert topology["independent_model_claim_allowed"] is False
    assert topology["real_adjudication_executed"] is False


def test_two_freeze_guards_cover_human_origin_and_postfreeze_history() -> None:
    machine = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-TWO-FREEZE-STATE-MACHINE-V1.json")
    guards = set(machine["structural_guards"])
    for guard in (
        "GPT_SEMANTIC_TRANSFORMATION_REQUIRES_RAW_FREEZE",
        "ORIGINAL_SOURCE_CANNOT_BE_REPLACED_BY_TRANSCRIPT_OR_DERIVATIVE",
        "NEAR_DUPLICATE_FLAG_IS_NON_BINDING",
        "SYNTHESIS_PRESERVES_CONFLICT_AND_UNRESOLVED_MATERIAL",
        "CLEAN_FREEZE_REQUIRES_JOEL_FINAL_FIDELITY_ATTESTATION",
        "PREFREEZE_PROTECTED_EXPOSURE_FORCES_CONTAMINATED_FAIL_CLOSED",
        "POSTFREEZE_REVISION_CANNOT_OVERWRITE_CLEAN_FREEZE",
    ):
        assert guard in guards
    assert machine["freeze_order"] == [
        "RAW_HUMAN_ORIGIN_FREEZE",
        "CLEAN_CONCEPTION_FREEZE",
        "PROTECTED_MAPPING_ACCESS",
    ]
    assert machine["transition_algorithm_present"] is False
    assert machine["real_transition_executed"] is False


def test_validator_is_test_only_and_absent_from_production_imports() -> None:
    validator_text = (ROOT / "tests/a1_gpt_heavy/validator.py").read_text(encoding="utf-8")
    assert "def classify" not in validator_text
    assert "def decide" not in validator_text
    production = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in (ROOT / "src").rglob("*.py")
    )
    assert "tests.a1_gpt_heavy" not in production
    assert (
        git("diff", "--name-only", CORRECTED_BASELINE, "--", "src", "web", "alembic", "migrations")
        == ""
    )


def test_exact_48_row_matrix_and_manifest_hashes() -> None:
    matrix = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-ACCEPTANCE-MATRIX-V1.json")
    assert matrix["requirement_count"] == len(matrix["requirements"]) == 48
    assert [item["requirement_id"] for item in matrix["requirements"]] == [
        f"A1G-{index:02d}" for index in range(1, 49)
    ]
    assert all(item["status"].startswith("PASS") for item in matrix["requirements"])
    manifest = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-ARTIFACT-MANIFEST-V1.json")
    paths = [item["path"] for item in manifest["artifacts"]]
    assert len(paths) == len(set(paths)) == manifest["artifact_count"]
    for item in manifest["artifacts"]:
        assert re.fullmatch(r"A1G-[0-4][0-9]", item["primary_requirement_id"])
        assert "A1G-01" <= item["primary_requirement_id"] <= "A1G-48"
        assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
        assert sha256(ROOT / item["path"]) == item["sha256"]
    assert manifest["production_source_diff_empty"] is True
    assert manifest["root_completion"] is False
    assert manifest["release_permission"] is False


def test_reconciliation_assurance_and_execution_boundaries_are_separate() -> None:
    reconciliation = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-OBJECTIVE-RECONCILIATION-V1.json")
    assurance = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-ASSURANCE-PLANES-V1.json")
    execution = load_json(STATE / "NATAL-TIME-A1-GPT-HEAVY-EXECUTION-LEDGER-V1.json")
    assert reconciliation["worker_to_contract_alignment"] == "GREEN"
    assert reconciliation["contract_to_owner_alignment"] == "PARTIAL_ROOT_OPEN"
    assert reconciliation["completion_claim"] == "WORKING"
    assert reconciliation["parent_outcome"] == "OPEN"
    assert assurance["operational_alignment"]["state"] == "PASS"
    assert assurance["scientific_adequacy"]["state"] == "WARN"
    assert assurance["release_adequacy"]["state"] == "NOT_APPLICABLE"
    assert assurance["release_adequacy"]["release_permission"] is False
    assert not any(execution["prohibited_actions"].values())
    assert execution["root_completion"] is False
    assert execution["release_permission"] is False
