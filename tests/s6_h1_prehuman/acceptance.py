"""Exact test-only checks for the 60 S6/H1 pre-human acceptance requirements."""

from __future__ import annotations

import copy
import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from tests.s6_h1_prehuman.validator import (
    ALLOWED_SOURCE,
    FIXTURES,
    ROOT,
    SCHEMA_PATHS,
    ValidationFailure,
    load_fixture,
    load_json,
    validate_record,
)

ACCEPTED_CHECKPOINT_10 = "f588af40f107d23430808665175e65b133400d4e"
CONCEPTION_COMMIT = "a2f990f343f1ff8a14171043c15d43b5efe06b73"
VALID_IDS = {f"S6H1-{index:02d}" for index in range(1, 61)}

P = {
    "source_alignment": ROOT / "state/NATAL-TIME-S6-H1-SOURCE-ALIGNMENT-ATTESTATION-V1.json",
    "workflow": ROOT / "state/NATAL-TIME-S6-H1-WORKFLOW-CONTRACT-V1.json",
    "roles": ROOT / "state/NATAL-TIME-S6-H1-ROLE-ACCESS-MATRIX-V1.json",
    "screening": ROOT / "state/NATAL-TIME-S6-H1-SCREENING-METADATA-SCHEMA-V1.json",
    "isolation": ROOT / "state/NATAL-TIME-S6-H1-ISOLATION-PROVENANCE-SCHEMA-V1.json",
    "escrow": ROOT / "state/NATAL-TIME-S6-H1-CONTENT-ESCROW-CONTRACT-V1.json",
    "machine": ROOT / "state/NATAL-TIME-S6-H1-CONCEPTION-SEARCH-STATE-MACHINE-V1.json",
    "threats": ROOT / "state/NATAL-TIME-S6-H1-THREAT-MODEL-V1.json",
    "unresolved": ROOT / "state/NATAL-TIME-S6-H1-UNRESOLVED-DECISIONS-V1.json",
    "reconciliation": ROOT / "state/NATAL-TIME-S6-H1-OBJECTIVE-RECONCILIATION-V1.json",
    "assurance": ROOT / "state/NATAL-TIME-S6-H1-ASSURANCE-PLANES-V1.json",
    "conception": ROOT / "state/NATAL-TIME-S6-H1-PREHUMAN-INDEPENDENT-CONCEPTION-V1.json",
    "sources": ROOT / "state/NATAL-TIME-S6-H1-PREHUMAN-SOURCE-LEDGER-V1.json",
    "methods": ROOT / "state/NATAL-TIME-S6-H1-PREHUMAN-METHODS-DECISION-LEDGER-V1.json",
    "execution": ROOT / "state/NATAL-TIME-S6-H1-EXECUTION-LEDGER-V1.json",
    "matrix": ROOT / "state/NATAL-TIME-S6-H1-ACCEPTANCE-MATRIX-V1.json",
    "manifest": ROOT / "state/NATAL-TIME-S6-H1-ARTIFACT-MANIFEST-V2.json",
    "dossier": ROOT / "docs/NATAL_TIME_S6_H1_PREHUMAN_OWNER_DOSSIER_20260830.md",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout.strip()


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


def _set_nested(record: dict[str, Any], field: str, value: Any) -> None:
    parts = field.split(".")
    target = record
    for part in parts[:-1]:
        nested = target[part]
        assert isinstance(nested, dict)
        target = nested
    target[parts[-1]] = value


def _invalid_probe(case_id: str) -> None:
    probes = load_json(FIXTURES / "invalid_probes.json")
    case = next(item for item in probes["cases"] if item["case_id"] == case_id)
    record = copy.deepcopy(load_fixture(case["base_fixture"]))
    for mutation in case.get("mutations", [case.get("mutation")]):
        assert mutation is not None
        _set_nested(record, mutation["field"], mutation["value"])
    try:
        validate_record(case["schema"], record)
    except ValidationFailure as exc:
        assert exc.code == case["expected_code"], str(exc)
    else:
        raise AssertionError(f"expected controlled rejection for {case_id}")


def _roles() -> dict[str, dict[str, Any]]:
    return {item["role_id"]: item for item in load_json(P["roles"])["roles"]}


def _decision_categories() -> dict[str, str]:
    return {
        item["decision_id"]: item["category"] for item in load_json(P["unresolved"])["decisions"]
    }


def _protected_checkpoint_paths() -> list[str]:
    tracked = _git("ls-tree", "-r", "--name-only", ACCEPTED_CHECKPOINT_10).splitlines()
    prefixes = (
        "docs/NATAL_TIME_CHECKPOINT8_",
        "docs/NATAL_TIME_OPTION_B_",
        "docs/NATAL_TIME_B1_",
        "docs/PRO_SUPERVISION_CHECKPOINT_8_",
        "docs/PRO_SUPERVISION_CHECKPOINT_9_",
        "docs/PRO_SUPERVISION_OPTION_B_",
        "docs/PRO_SUPERVISION_B1_",
        "state/NATAL-TIME-CHECKPOINT8-",
        "state/NATAL-TIME-OPTION-B-",
        "state/NATAL-TIME-B1-",
    )
    return [path for path in tracked if path.startswith(prefixes)]


def check_requirement(requirement_id: str) -> None:
    """Run one authoritative requirement without human, content, or mapping action."""

    assert requirement_id in VALID_IDS
    number = int(requirement_id.split("-")[1])
    source = load_json(P["source_alignment"])
    workflow = load_json(P["workflow"])
    roles = _roles()
    machine = load_json(P["machine"])
    unresolved = load_json(P["unresolved"])
    execution = load_json(P["execution"])

    if number == 1:
        assert source["owner_source"] == {
            "owner_request_id": "OR-ASTROHD-RELATIONSHIP-CONTINUATION-20260830",
            "owner_outcome_id": "OO-ASTROHD-RELATIONSHIP-CONTINUATION",
            "epoch": 4,
            "canonical_locator": "state/NATAL-TIME-OWNER-OUTCOME-SOURCE-EPOCH4-20260830.md",
            "sha256": "2bc3b243f67411907799c9b382dccd9552220a67cfe20d0429949868123db735",
            "receipt_id": "osr-astrohd-relationship-20260830-epoch4-v1",
            "receipt_path": "state/NATAL-TIME-OWNER-SOURCE-RECEIPT-EPOCH4-V1.json",
            "receipt_sha256": "ddc542e03079fba0a06577500dd98a13f7784e13d5ea56130676525611427e47",
        }
    elif number == 2:
        assert source["acquisition_mode"] == "WORKER_COPIED"
    elif number == 3:
        assert source["receipt_capability"] == "INTEGRITY_ONLY"
    elif number == 4:
        assert source["contract_to_captured_source_alignment"] == "MATCH"
    elif number == 5:
        assert source["independent_source_comparison"] == "NOT_INDEPENDENT"
    elif number == 6:
        assert source["contract_to_owner_alignment"] == "PARTIAL"
    elif number == 7:
        reconciliation = load_json(P["reconciliation"])
        assert reconciliation["requirement_count"] == 13
        assert [item["owner_requirement_id"] for item in reconciliation["requirements"]] == [
            f"RO-{index:02d}" for index in range(1, 14)
        ]
    elif number == 8:
        assert source["completion_claim"] == "WORKING"
        assert source["parent_outcome_open"] is True
        assert source["root_terminalization_allowed"] is False
    elif number == 9:
        conception = load_json(P["conception"])
        sources = load_json(P["sources"])
        assert conception["status"] == "FROZEN_PRE_SEARCH"
        assert sources["independent_conception_commit"] == CONCEPTION_COMMIT
        assert _git("merge-base", "--is-ancestor", CONCEPTION_COMMIT, "HEAD") == ""
    elif number == 10:
        conception = load_json(P["conception"])
        assert all(
            conception[field] is False
            for field in (
                "external_citations_present",
                "framework_or_source_names_present",
                "urls_present",
                "human_candidates_present",
            )
        )
    elif number == 11:
        conception = load_json(P["conception"])
        assert all(
            conception[field] is False
            for field in (
                "screening_questions_present",
                "construct_examples_present",
                "source_choices_present",
                "mapping_hypotheses_present",
            )
        )
    elif number == 12:
        ledger = load_json(P["sources"])
        assert len(ledger["queries"]) == 20
        assert len(ledger["sources"]) >= 12
        assert ledger["excluded_results"]
        assert all(item["version_or_date"] for item in ledger["sources"])
    elif number == 13:
        assert len(load_json(P["sources"])["scope"]) == 12
    elif number == 14:
        methods = load_json(P["methods"])
        allowed = set(methods["allowed_classifications"])
        assert allowed == {
            "REUSE_DIRECTLY",
            "ADAPT",
            "COMPOSE",
            "BASELINE_OR_DIAGNOSTIC_ONLY",
            "INCOMPATIBLE",
            "UNRESOLVED",
            "REQUIRES_PRO_REVIEW",
            "REQUIRES_OWNER_DECISION",
        }
        assert all(item["classification"] in allowed for item in methods["decisions"])
    elif number == 15:
        queries = "\n".join(item["query"].lower() for item in load_json(P["sources"])["queries"])
        assert not any(
            term in queries
            for term in (
                "astrohd",
                "human design",
                "construct candidate",
                "mapping ontology",
                "mapping method",
            )
        )
    elif number == 16:
        assert set(roles) == {
            "OWNER",
            "GOVERNANCE_SUPERVISOR",
            "SCREENING_ADMINISTRATOR",
            "CHART_BLIND_HUMAN_CONCEPT_AUTHOR",
            "SOURCE_SEARCH_WORKER",
            "MEASUREMENT_REVIEWER",
            "CONTENT_CUSTODIAN",
            "RELIABILITY_EVALUATOR",
            "MAPPING_WORKER",
            "INDEPENDENT_EVALUATOR",
        }
    elif number == 17:
        assert load_json(P["roles"])["real_person_assignments"] == []
    elif number == 18:
        eligibility = load_json(P["roles"])["content_author_eligibility"]
        assert (
            eligibility[
                "astrohd_exposed_person_context_conversation_repository_model_session_eligible"
            ]
            is False
        )
        assert eligibility["current_context_eligible"] is False
    elif number == 19:
        eligibility = load_json(P["roles"])["content_author_eligibility"]
        assert eligibility["human_only"] is True
        assert eligibility["model_or_model_session_eligible"] is False
    elif number == 20:
        assert "S6_ORDER_CANNOT_BE_BYPASSED" in workflow["invariants"]
        assert (
            "CONSTRUCT_SPECIFIC_SEARCH_REQUIRES_PRIOR_HUMAN_CONCEPTION_FREEZE"
            in machine["non_bypass_rules"]
        )
    elif number == 21:
        separated = {tuple(pair) for pair in workflow["logical_role_separations"]}
        assert ("CHART_BLIND_HUMAN_CONCEPT_AUTHOR", "SOURCE_SEARCH_WORKER") in separated
        assert ("CHART_BLIND_HUMAN_CONCEPT_AUTHOR", "MEASUREMENT_REVIEWER") in separated
        assert ("CHART_BLIND_HUMAN_CONCEPT_AUTHOR", "CONTENT_CUSTODIAN") in separated
        assert ("CHART_BLIND_HUMAN_CONCEPT_AUTHOR", "RELIABILITY_EVALUATOR") in separated
        assert ("CHART_BLIND_HUMAN_CONCEPT_AUTHOR", "MAPPING_WORKER") in separated
    elif number == 22:
        assert roles["MEASUREMENT_REVIEWER"]["content_revision"] == "FORBIDDEN_SILENT_CHANGE"
    elif number == 23:
        assert roles["MAPPING_WORKER"]["prefreeze_content_access"] == "FORBIDDEN"
        assert machine["mapping_lane_state"] == "CLOSED_NOT_AUTHORIZED"
    elif number == 24:
        role_data = load_json(P["roles"])
        assert role_data["assignment_history"].startswith("APPEND_ONLY")
        assert role_data["access_history"].startswith("APPEND_ONLY")
        assert role_data["exposure_history"].startswith("APPEND_ONLY")
    elif number == 25:
        conflicts = set(load_json(P["roles"])["conflict_classes"])
        assert {
            "PERSON_ROLE_CONFLICT",
            "TEAM_CONNECTION_CONFLICT",
            "SESSION_EXPOSURE_CONFLICT",
            "SOURCE_EXPOSURE_CONFLICT",
            "CONNECTED_EVIDENCE_CONFLICT",
        } <= conflicts
    elif number == 26:
        for path in SCHEMA_PATHS.values():
            assert all(
                node.get("additionalProperties") is False for node in _object_nodes(load_json(path))
            )
    elif number == 27:
        screening = load_json(P["screening"])
        isolation = load_json(P["isolation"])
        assert screening["properties"]["synthetic_candidate_id"]["pattern"].startswith("^SYN-")
        assert isolation["properties"]["synthetic_isolation_id"]["pattern"].startswith("^SYN-")
        _invalid_probe("real_like_candidate_id")
    elif number == 28:
        fields = set(load_json(P["screening"])["properties"]["exposure_states"]["required"])
        assert fields == {
            "human_design",
            "astrohd",
            "astrology",
            "repository",
            "conversation",
            "mapping",
            "owner",
            "individualized_feedback",
        }
    elif number == 29:
        _invalid_probe("unknown_exposure_not_closed")
        _invalid_probe("contamination_not_ineligible")
    elif number == 30:
        assert (
            load_json(P["sources"])["nonselection_confirmation"]["screening_threshold_or_exception"]
            == "UNSELECTED"
        )
        assert unresolved["selection_count"] == 0
    elif number == 31:
        _invalid_probe("prohibited_human_field")
        dossier = P["dossier"].read_text(encoding="utf-8")
        assert "contains no screening question" in dossier
    elif number == 32:
        prohibited = execution["prohibited_action_record"]
        assert (
            prohibited[
                "human_identification_contact_screening_recruitment_compensation_assignment_enrollment"
            ]
            is False
        )
    elif number == 33:
        required = set(load_json(P["isolation"])["required"])
        assert {"environment", "session", "tool", "retrieval", "actor", "access"} <= required
    elif number == 34:
        _invalid_probe("isolation_with_unknown_session")
        assert "IGNORE_INSTRUCTION_SUBSTITUTED_FOR_ISOLATION" in {
            item["class"] for item in load_json(P["threats"])["threats"]
        }
    elif number == 35:
        _invalid_probe("model_authorship_true")
        assert load_fixture("isolation_valid.json")["model_content_authorship_allowed"] is False
    elif number == 36:
        assert execution["external_mutations"] == []
        assert execution["human_records"] == []
    elif number == 37:
        escrow = load_json(P["escrow"])
        assert escrow["current_repository_content_bearing_bytes_allowed"] is False
        assert escrow["astrohd_exposed_surface_prefreeze_content_allowed"] is False
    elif number == 38:
        escrow = load_json(P["escrow"])
        assert set(escrow["permitted_repository_fields"]) == {
            "opaque_synthetic_id",
            "status",
            "sha256_content_digest",
            "provenance_receipt",
            "append_only_access_event",
            "append_only_custody_event",
            "freeze_receipt",
        }
        assert {"construct_text", "item", "prompt", "mapping_hypothesis"} <= set(
            escrow["prohibited_repository_fields"]
        )
    elif number == 39:
        assert roles["MAPPING_WORKER"]["prefreeze_content_access"] == "FORBIDDEN"
        assert roles["OWNER"]["prefreeze_content_access"] == "FORBIDDEN"
        assert roles["GOVERNANCE_SUPERVISOR"]["prefreeze_content_access"] == "FORBIDDEN"
    elif number == 40:
        escrow = load_json(P["escrow"])
        assert (
            "EVERY_ACCESS_AND_CUSTODY_EVENT_IS_APPEND_ONLY_HASH_LINKED_AND_ROLE_ATTRIBUTED"
            in escrow["future_custody_invariants"]
        )
        assert {"content_digest", "previous_event_digest", "event_digest"} <= set(
            escrow["closed_synthetic_event_shape"]["allowed_keys"]
        )
    elif number == 41:
        future = machine["future_unopened_ordered_states"]
        assert future.index("FUTURE_HUMAN_CONCEPTION_FROZEN") < future.index(
            "FUTURE_CONSTRUCT_SPECIFIC_SEARCH_PROTOCOL_FROZEN"
        )
    elif number == 42:
        assert (
            "LATER_SEARCH_CREATES_A_LINKED_EVIDENCE_PACKAGE_NOT_AN_IN_PLACE_EDIT"
            in machine["non_bypass_rules"]
        )
    elif number == 43:
        hard_stops = {
            item["before"]
            for item in machine["stops"]
            if item["status"] == "HARD_STOP_CURRENT_CHILD"
        }
        assert {
            "FUTURE_HUMAN_SCREENING_AUTHORIZED",
            "FUTURE_HUMAN_CONCEPTION_AUTHORED",
            "FUTURE_CONSTRUCT_SPECIFIC_SEARCH_PROTOCOL_FROZEN",
        } <= hard_stops
    elif number == 44:
        assert machine["mapping_lane_state"] == "CLOSED_NOT_AUTHORIZED"
        assert (
            "FUTURE_ASTROHD_MAPPING_QUESTION_SEPARATELY_FROZEN"
            in machine["future_unopened_ordered_states"]
        )
    elif number == 45:
        assert (
            "NULL_WEAK_UNSTABLE_OR_NONREPLICATING_MAPPING_PRESERVES_THE_ORIGINAL_AND_DOES_NOT_AUTHORIZE_REPAIR"
            in machine["non_bypass_rules"]
        )
    elif number == 46:
        assert len(unresolved["decisions"]) == 15
        assert P["dossier"].exists()
    elif number == 47:
        assert unresolved["selection_count"] == 0
        assert {item["status"] for item in unresolved["decisions"]} == {"UNSELECTED"}
    elif number == 48:
        assert all(
            unresolved[field] is False
            for field in (
                "recommendation_present",
                "ranking_present",
                "default_present",
                "preselection_present",
            )
        )
    elif number == 49:
        category = _decision_categories()["OD-04"]
        assert all(
            word in category
            for word in (
                "population",
                "geography",
                "language",
                "age",
                "literacy",
                "accessibility",
                "intended_use",
            )
        )
    elif number == 50:
        categories = _decision_categories()
        assert "recruitment" in categories["OD-05"]
        assert all(
            word in categories["OD-06"]
            for word in ("compensation", "budget", "staffing", "timeline")
        )
        assert "burden" in categories["OD-07"]
    elif number == 51:
        categories = _decision_categories()
        assert all(
            word in categories["OD-12"]
            for word in ("failure", "retry", "replacement", "termination")
        )
        assert "construct_specific_search" in categories["OD-13"]
        assert "reliability" in categories["OD-14"]
        assert "AstroHD_mapping" in categories["OD-15"]
    elif number == 52:
        assert unresolved["implied_human_authorization_present"] is False
        assert "supplies no recommendation" in P["dossier"].read_text(encoding="utf-8")
    elif number == 53:
        matrix = load_json(P["matrix"])
        assert matrix["requirement_count"] == 60
        assert [item["requirement_id"] for item in matrix["requirements"]] == [
            f"S6H1-{index:02d}" for index in range(1, 61)
        ]
    elif number == 54:
        manifest = load_json(P["manifest"])
        assert manifest["digest_algorithm"] == "sha256"
        v1_path = ROOT / manifest["supersedes"]["path"]
        assert _sha256(v1_path) == manifest["supersedes"]["sha256"]
        inherited = load_json(v1_path)["artifacts"]
        replacements = {item["path"]: item for item in manifest["changed_or_added_artifacts"]}
        artifacts = [replacements.pop(item["path"], item) for item in inherited]
        artifacts.extend(replacements.values())
        assert manifest["artifact_count"] == len(artifacts)
        assert len({item["path"] for item in artifacts}) == manifest["artifact_count"]
        for item in artifacts:
            assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
            assert item["primary_requirement_id"] in VALID_IDS
            assert _sha256(ROOT / item["path"]) == item["sha256"]
    elif number == 55:
        validate_record("screening", load_fixture("screening_valid.json"), source=ALLOWED_SOURCE)
        validate_record("isolation", load_fixture("isolation_valid.json"), source=ALLOWED_SOURCE)
        _invalid_probe("unknown_field")
        _invalid_probe("retrieval_source_nonzero")
        production_imports = [
            path
            for path in (ROOT / "src").rglob("*.py")
            if "s6_h1_prehuman" in path.read_text(encoding="utf-8")
        ]
        assert production_imports == []
    elif number == 56:
        paths = _protected_checkpoint_paths()
        assert paths
        for path in paths:
            assert (ROOT / path).read_bytes() == subprocess.run(
                ["git", "show", f"{ACCEPTED_CHECKPOINT_10}:{path}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
    elif number == 57:
        matrix = load_json(P["matrix"])
        row = matrix["requirements"][56]
        assert row["requirement_id"] == "S6H1-57"
        assert row["status"] == "PASS_AT_EXACT_HEAD"
        assert _git("diff", "--check") == ""
        assert _git("diff", "--name-only", ACCEPTED_CHECKPOINT_10, "--", "src") == ""
    elif number == 58:
        browser = execution["browser_operation"]
        assert browser["generic_research_mode"] == "HEADLESS_DEFAULT"
        assert browser["dedicated_secondary_workspace_reused"] is True
        assert browser["unnecessary_new_visible_windows_opened"] is False
    elif number == 59:
        assert len(execution["corrected_commands"]) >= 2
        assert execution["external_mutations"] == []
        assert set(execution["prohibited_action_record"].values()) == {False}
    elif number == 60:
        assurance = load_json(P["assurance"])
        assert assurance["worker_to_contract_alignment"] == "GREEN"
        assert assurance["contract_to_owner_alignment"] == "PARTIAL"
        assert assurance["completion_claim"]["type"] == "WORKING"
        assert assurance["completion_claim"]["parent_outcome"] == "OPEN"
        assert assurance["operational_alignment"]["status"] == "PASS"
        assert assurance["scientific_adequacy"]["status"] == "WARN"
        assert assurance["release_adequacy"]["status"] == "NOT_APPLICABLE"
        assert assurance["release_adequacy"]["release_permission"] is False


def run_all_requirements() -> list[str]:
    """Run all 60 ordered checks and return the passing IDs."""

    passing: list[str] = []
    for index in range(1, 61):
        requirement_id = f"S6H1-{index:02d}"
        check_requirement(requirement_id)
        passing.append(requirement_id)
    return passing
