from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pytest

from tests.p1_adjudication.validator import (
    ALLOWED_SOURCE,
    ValidationFailure,
    load_fixture,
    validate_record,
)
from tests.s6_h1_prehuman.acceptance import run_all_requirements as run_checkpoint11

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"
DOCS = ROOT / "docs"
FIXTURES = ROOT / "tests" / "fixtures" / "p1_adjudication"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_checkpoint11_authority_and_accepted_artifacts_are_exact() -> None:
    expected = {
        "NATAL-TIME-OWNER-P1-RATIFICATION-SOURCE-EPOCH6-20260831.json": (
            "2faee461ba44273c267edd0c106be2cd46377e820098ce6b3047bbcf477a6efa"
        ),
        "NATAL-TIME-P1-PROPOSAL-TEXT-EPOCH6-20260831.txt": (
            "664c875137f7d671685db0df074429cfc0a243a78d549f7ee1143af8eacb5a00"
        ),
        "NATAL-TIME-OWNER-SOURCE-RECEIPT-EPOCH6-V1.json": (
            "4eb5600e9f46f07c35546f65e5dd6ed15438a3683ffa87590f81b808edaac3ff"
        ),
        "NATAL-TIME-OWNER-OUTCOME-EPOCH6-V1.json": (
            "e6b4608a4849fa3acde1ab71db8026af55a04b21070529c6d5bc8eb20cbf8001"
        ),
        "NATAL-TIME-S6-H1-PRIOR-EXPOSURE-POLICY-AUTHORITY-V1.json": (
            "5334ffd43189747a475592c59afcd173c66e14a0e8a39b1928b9dcae8b484e17"
        ),
        "NATAL-TIME-S6-H1-CHECKPOINT11-PRO-RULING-V5.json": (
            "2cae4899eb7b31e913552d2ec6ba0f2c73427b8eeec0be9d3281d65f3d1c2c5c"
        ),
    }
    for name, digest in expected.items():
        assert sha256(STATE / name) == digest
    assert len(run_checkpoint11()) == 60


def test_conception_is_frozen_and_precedes_scan() -> None:
    document = DOCS / "NATAL_TIME_P1_ADJUDICATION_PREMETHOD_CONCEPTION_20260831.md"
    conception = STATE / "NATAL-TIME-P1-ADJUDICATION-PREMETHOD-CONCEPTION-V1.json"
    assert sha256(document) == "40e32809fa8f882394414aa6e412ec6f90f5eed3392395fd1f3da34475c3d8b1"
    assert sha256(conception) == "91a3421fa7241d08478a8705a1a964170da242558ec8ed603d2db08b078ab799"
    ledger = load_json(STATE / "NATAL-TIME-P1-ADJUDICATION-SOURCE-LEDGER-V1.json")
    assert ledger["conception_commit"] == "7d914af30bfe4c4817692067f8e4471f3c3e3987"
    assert ledger["scan_started_after_conception_commit"] is True
    text = document.read_text(encoding="utf-8")
    assert "http://" not in text and "https://" not in text and "doi.org" not in text
    for source_name in ("ICMJE", "FDA", "EMA", "ORI", "NIST", "GRRAS"):
        assert source_name not in text
    state = load_json(conception)
    assert state["search_count_at_freeze"] == 0
    assert state["selected_option_ids"] == []
    assert not any(state["prohibited_content_flags"].values())


def test_source_ledger_has_exact_ordered_queries_and_no_forbidden_search() -> None:
    ledger = load_json(STATE / "NATAL-TIME-P1-ADJUDICATION-SOURCE-LEDGER-V1.json")
    assert ledger["query_count"] == 24 == len(ledger["queries"])
    assert [item["sequence"] for item in ledger["queries"]] == list(range(1, 25))
    assert {item["date"] for item in ledger["queries"]} == {"2026-08-31"}
    assert all(item["query"].strip() == item["query"] for item in ledger["queries"])
    query_text = "\n".join(item["query"] for item in ledger["queries"]).lower()
    for prohibited in ("astrohd", "human design", "birth chart", "relationship chart"):
        assert prohibited not in query_text
    assert ledger["construct_specific_search_count"] == 0
    assert ledger["mapping_search_count"] == 0
    assert ledger["included_source_count"] == 24
    assert ledger["excluded_source_count"] == 4
    assert all(item["eligibility_decision"] for item in ledger["sources"])
    assert all(item["reason"] for item in ledger["sources"])


def test_method_families_have_exactly_one_classification_and_no_selection() -> None:
    ledger = load_json(STATE / "NATAL-TIME-P1-ADJUDICATION-METHODS-DECISION-LEDGER-V1.json")
    families = ledger["families"]
    assert ledger["method_family_count"] == len(families) == 18
    assert len({item["method_family_id"] for item in families}) == len(families)
    allowed = set(ledger["allowed_classifications"])
    assert all(item["classification"] in allowed for item in families)
    assert all(isinstance(item["classification"], str) for item in families)
    assert ledger["selected_method_family_ids"] == []
    assert ledger["selected_evidence_threshold"] is None
    assert ledger["selected_adjudication_procedure"] is None
    assert ledger["selected_author_configuration"] is None
    assert ledger["selected_adjudicator_configuration"] is None


def _assert_all_object_schemas_closed(schema: dict[str, Any]) -> None:
    if schema.get("type") == "object":
        assert schema.get("additionalProperties") is False
    for key in ("properties",):
        for nested in schema.get(key, {}).values():
            _assert_all_object_schemas_closed(nested)
    if "items" in schema:
        _assert_all_object_schemas_closed(schema["items"])
    for nested in schema.get("oneOf", []):
        _assert_all_object_schemas_closed(nested)


def test_evidence_schema_is_closed_and_separates_required_dimensions() -> None:
    schema = load_json(STATE / "NATAL-TIME-P1-EVIDENCE-CLASSIFICATION-SCHEMA-V1.json")
    _assert_all_object_schemas_closed(schema)
    properties = schema["properties"]
    for field in (
        "exposure_provenance",
        "familiarity",
        "self_concept_integration_state",
        "intentional_derivation_risk_state",
        "evidence_completeness_state",
        "evidence_conflict_state",
        "process_state",
        "substantive_outcome",
        "role_access_state",
    ):
        assert field in properties
    nondispositive = set(properties["non_dispositive_metadata_classes"]["items"]["enum"])
    assert nondispositive == {
        "BELIEF",
        "SKEPTICISM",
        "MISMATCH",
        "PERCEIVED_ACCURACY",
        "CURIOSITY",
        "USEFULNESS",
        "PRODUCT_INTEREST",
    }


@pytest.mark.parametrize(
    "fixture_name", ["valid_incomplete.json", "valid_adjudication_pending.json"]
)
def test_synthetic_fixtures_validate(fixture_name: str) -> None:
    validate_record(load_fixture(fixture_name))


def _mutated_probe(probe: dict[str, Any]) -> tuple[dict[str, Any], str]:
    record = copy.deepcopy(load_fixture("valid_incomplete.json"))
    mutation = probe["mutation"]
    source = ALLOWED_SOURCE
    if mutation in {"UNKNOWN_FIELD", "PROHIBITED_FIELD"}:
        record[probe["field"]] = "SYNTHETIC_PROBE"
    elif mutation in {"PROHIBITED_VALUE", "PERSONAL_VALUE", "ENUM_ESCAPE"}:
        record[probe["field"]] = probe["value"]
    elif mutation in {"REAL_PERSON_TRUE", "HUMAN_ACTION_TRUE"}:
        record[probe["field"]] = True
    elif mutation == "EMPTY_PROVENANCE":
        record["exposure_provenance"] = []
    elif mutation == "DUPLICATE_PROVENANCE":
        record["exposure_provenance"] = ["UNKNOWN", "UNKNOWN"]
    elif mutation == "NON_SYNTHETIC_SOURCE":
        source = "UNCONTROLLED_INPUT"
    else:
        raise AssertionError(mutation)
    return record, source


@pytest.mark.parametrize(
    "probe",
    load_json(FIXTURES / "invalid_probes.json")["probes"],
    ids=lambda probe: probe["probe_id"],
)
def test_prohibited_or_non_synthetic_metadata_fails_closed(probe: dict[str, Any]) -> None:
    record, source = _mutated_probe(probe)
    with pytest.raises(ValidationFailure):
        validate_record(record, source=source)


def test_validator_has_no_human_classification_algorithm_or_production_import() -> None:
    validator_path = ROOT / "tests" / "p1_adjudication" / "validator.py"
    validator_text = validator_path.read_text(encoding="utf-8")
    assert "def classify" not in validator_text
    assert "def decide" not in validator_text
    assert "substantive_outcome" not in validator_text
    assert "tests.p1_adjudication" not in "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in (ROOT / "src").rglob("*.py")
    )


def test_role_access_matrix_has_six_distinct_roles_and_firewalls() -> None:
    matrix = load_json(STATE / "NATAL-TIME-P1-BLIND-ADJUDICATION-ROLE-ACCESS-MATRIX-V1.json")
    assert {role["role_id"] for role in matrix["roles"]} == {
        "ELIGIBILITY_EVIDENCE_CUSTODIAN",
        "BLIND_ELIGIBILITY_ADJUDICATOR",
        "CLEAN_H1_AUTHOR",
        "PROTECTED_CONTENT_CUSTODIAN",
        "RELIABILITY_EVALUATOR",
        "LATER_MAPPING_EVALUATOR",
    }
    assert matrix["real_person_assignments"] == []
    assert matrix["current_access_grants"] == []
    assert not any(
        matrix["access_invariants"][key]
        for key in (
            "requires_blind_adjudication_can_receive_clean_author_access_without_future_receipt",
            "ineligible_clean_h1_author_can_receive_prefreeze_author_access",
            "unknown_or_conflicting_evidence_can_receive_clean_author_access",
            "eligible_status_alone_grants_assignment",
            "target_domain_exposed_model_repository_conversation_or_retrieval_context_can_author",
            "recusal_or_replacement_erases_prior_access",
            "later_mapping_can_influence_prefreeze_author_work",
        )
    )


def test_state_machine_preserves_history_without_algorithm() -> None:
    machine = load_json(STATE / "NATAL-TIME-P1-EVIDENCE-DECISION-STATE-MACHINE-V1.json")
    guards = set(machine["structural_guards"])
    assert "CONFLICT_CANNOT_BE_CLEARED_WITHOUT_A_NEW_RECORDED_EVENT" in guards
    assert "DISAGREEMENT_REMAINS_VISIBLE_AFTER_RESOLUTION" in guards
    assert "RECUSAL_AND_REPLACEMENT_PRESERVE_PRIOR_EXPOSURE_AND_ACCESS" in guards
    assert "A_SUBSTANTIVE_OUTCOME_DOES_NOT_CREATE_ACCESS" in guards
    assert machine["transition_algorithm_present"] is False
    assert machine["decision_algorithm_present"] is False


def test_author_configuration_registry_is_neutral_and_complete() -> None:
    registry = load_json(STATE / "NATAL-TIME-P1-AUTHOR-CONFIGURATION-REGISTRY-V1.json")
    assert [item["option_id"] for item in registry["options"]] == [
        "AUTHOR-CONFIG-SINGLE",
        "AUTHOR-CONFIG-INDEPENDENT-PAIR",
        "AUTHOR-CONFIG-INDEPENDENT-PANEL",
    ]
    for option in registry["options"]:
        assert set(option["adjudication_variants"]) == {
            "SEPARATE_ADJUDICATION",
            "SHARED_ADJUDICATION",
        }
        for tradeoff in ("contamination", "independence", "cost", "burden", "feasibility"):
            assert option[f"{tradeoff}_tradeoff"]
        assert option["operational_author_count"] is None
        assert option["selected"] is False
    for flag in (
        "recommendation_present",
        "ranking_present",
        "default_present",
        "implied_authorization_present",
        "author_count_selected",
        "adjudicator_count_selected",
        "population_selected",
        "language_selected",
        "geography_selected",
        "recruitment_selected",
        "burden_selected",
        "compensation_selected",
        "budget_selected",
        "timeline_selected",
    ):
        assert registry[flag] is False


def test_owner_dossier_and_unresolved_register_do_not_preselect() -> None:
    register = load_json(STATE / "NATAL-TIME-P1-UNRESOLVED-DECISIONS-V1.json")
    assert register["decision_count"] == len(register["decisions"]) == 20
    assert all(item["status"] == "UNSELECTED" for item in register["decisions"])
    assert register["selected_decision_ids"] == []
    assert register["owner_decision_required_now"] is False
    assert register["owner_decision_required_before_human_facing_design_or_activity"] is True
    dossier = (DOCS / "NATAL_TIME_P1_ADJUDICATION_OWNER_DOSSIER_20260831.md").read_text(
        encoding="utf-8"
    )
    assert "None is recommended" in dossier
    assert "No owner choice is required at this checkpoint" in dossier


def test_acceptance_matrix_is_exactly_ordered_48_rows() -> None:
    matrix = load_json(STATE / "NATAL-TIME-P1-ADJUDICATION-ACCEPTANCE-MATRIX-V1.json")
    expected = [f"P1A-{index:02d}" for index in range(1, 49)]
    assert matrix["requirement_count"] == len(matrix["requirements"]) == 48
    assert [item["requirement_id"] for item in matrix["requirements"]] == expected
    assert all(item["status"].startswith("PASS") for item in matrix["requirements"])


def test_manifest_hashes_every_artifact_with_one_primary_requirement() -> None:
    manifest = load_json(STATE / "NATAL-TIME-P1-ADJUDICATION-ARTIFACT-MANIFEST-V1.json")
    paths = [item["path"] for item in manifest["artifacts"]]
    assert len(paths) == len(set(paths)) == manifest["artifact_count"]
    for item in manifest["artifacts"]:
        assert re.fullmatch(r"P1A-[0-4][0-9]", item["primary_requirement_id"])
        assert item["primary_requirement_id"] <= "P1A-48"
        assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
        assert sha256(ROOT / item["path"]) == item["sha256"]
    assert manifest["selected_method_or_configuration"] is False
    assert manifest["root_completion"] is False
    assert manifest["release_permission"] is False


def test_reconciliation_and_assurance_planes_remain_separate() -> None:
    reconciliation = load_json(
        STATE / "NATAL-TIME-P1-ADJUDICATION-OBJECTIVE-RECONCILIATION-V1.json"
    )
    assurance = load_json(STATE / "NATAL-TIME-P1-ADJUDICATION-ASSURANCE-PLANES-V1.json")
    assert reconciliation["worker_to_contract_alignment"].startswith("GREEN")
    assert reconciliation["contract_to_owner_alignment"] == "PARTIAL_ROOT_OPEN"
    assert reconciliation["completion_claim"] == "WORKING"
    assert reconciliation["parent_outcome"] == "OPEN"
    assert assurance["operational_alignment"]["state"].startswith("PASS")
    assert assurance["scientific_adequacy"]["state"] == "WARN"
    assert assurance["release_adequacy"]["state"] == "NOT_APPLICABLE"
    assert assurance["release_adequacy"]["release_permission"] is False


def test_no_prohibited_action_or_production_source_delta_claim() -> None:
    ledger = load_json(STATE / "NATAL-TIME-P1-ADJUDICATION-EXECUTION-LEDGER-V1.json")
    assert not any(ledger["prohibited_actions"].values())
    assert ledger["completion_claim"] == "WORKING"
    assert ledger["parent_outcome"] == "OPEN"
    assert ledger["root_completion"] is False
    assert ledger["release_permission"] is False
