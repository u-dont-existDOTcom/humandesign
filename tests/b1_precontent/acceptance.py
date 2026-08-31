"""Exact test-only checks for the 64 B1 pre-content acceptance requirements."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from tests.b1_precontent.validator import (
    ALLOWED_SOURCE,
    FIXTURES,
    ROOT,
    SCHEMA_PATHS,
    ValidationFailure,
    load_fixture,
    load_json,
    validate_access_history,
    validate_record,
)

OWNER_COMMIT = "cc6e8c3c05551c772d788d336994c3996d02ab78"
OWNER_TREE = "11519d876c480b839e24bb6ee109f69c1a6a17a4"
OWNER_SHA = "64fe976c98c2b8ba82d86dc96e4bca2dee596338563dcc10c5934733e98b02af"
CHECKPOINT_9_RULING = "070348adb45ad1d3863ebab68d1bf1eea7439d53"
CHECKPOINT_9_EVIDENCE = "d6af8d472f1a8352b2d710b12aedeb3e904060d0"
CONCEPTION_COMMIT = "496143ed1c04fce8b6f92f010d8f7bd7a11da30c"
SCAN_COMMIT = "1b6f851e5ad3b116d589cf421dbb145d9a2ba3be"
PURPOSE = "b1_independent_construct_precontent_governance"

OWNER_RECORD = ROOT / "docs" / "NATAL_TIME_OWNER_DECISION_B1_20260830.md"
CONCEPTION_MD = (
    ROOT / "docs" / "NATAL_TIME_B1_PRECONTENT_INDEPENDENT_CONCEPTION_SNAPSHOT_20260830.md"
)
CONCEPTION_JSON = (
    ROOT / "state" / "NATAL-TIME-B1-PRECONTENT-INDEPENDENT-CONCEPTION-SNAPSHOT-V1.json"
)
SOURCE_LEDGER = ROOT / "state" / "NATAL-TIME-B1-PRECONTENT-SOURCE-LEDGER-V1.json"
DECISION_LEDGER = ROOT / "state" / "NATAL-TIME-B1-PRECONTENT-METHODS-DECISION-LEDGER-V1.json"
GOVERNANCE = ROOT / "state" / "NATAL-TIME-B1-CONSTRUCT-SOURCE-GOVERNANCE-V1.json"
SCAN_PROTOCOL = ROOT / "state" / "NATAL-TIME-B1-CONSTRUCT-SPECIFIC-SCAN-PROTOCOL-V1.json"
ROLES = ROOT / "state" / "NATAL-TIME-B1-ROLE-ACCESS-MATRIX-V1.json"
FREEZE_GATE = ROOT / "state" / "NATAL-TIME-B1-CONSTRUCT-FREEZE-GATE-V1.json"
MAPPING_FIREWALL = ROOT / "state" / "NATAL-TIME-B1-ASTROHD-MAPPING-FIREWALL-V1.json"
CLAIM_LANES = ROOT / "state" / "NATAL-TIME-B1-CLAIM-LANE-REGISTRY-V1.json"
CHANGE_CONTROL = ROOT / "state" / "NATAL-TIME-B1-POST-FREEZE-CHANGE-CONTROL-V1.json"
THREAT_MODEL = ROOT / "state" / "NATAL-TIME-B1-THREAT-MODEL-V1.json"
UNRESOLVED = ROOT / "state" / "NATAL-TIME-B1-UNRESOLVED-DECISIONS-V1.json"
BASELINE_ATTESTATION = ROOT / "state" / "NATAL-TIME-B1-BASELINE-ATTESTATION-V1.json"
FIXTURE_MANIFEST = ROOT / "state" / "NATAL-TIME-B1-SYNTHETIC-FIXTURE-MANIFEST-V1.json"
ARTIFACT_MANIFEST_V1 = ROOT / "state" / "NATAL-TIME-B1-ARTIFACT-MANIFEST-V1.json"
ARTIFACT_MANIFEST = ROOT / "state" / "NATAL-TIME-B1-ARTIFACT-MANIFEST-V2.json"
ACCEPTANCE_MATRIX = ROOT / "state" / "NATAL-TIME-B1-ACCEPTANCE-MATRIX-V1.json"
CORRECTION_LEDGER = ROOT / "state" / "NATAL-TIME-B1-CORRECTION-LEDGER-V1.json"

VALID_B1_REQUIREMENT_IDS = {f"B1-{index:02d}" for index in range(1, 65)}
TRACEABILITY_ROOT_KEYS = {
    "schema_version",
    "artifact_id",
    "status",
    "active_purpose",
    "provenance",
    "digest_algorithm",
    "supersedes",
    "assignment_semantics",
    "matrix_dependencies",
    "artifacts",
    "artifact_count",
    "self_digest_rule",
}
TRACEABILITY_ARTIFACT_KEYS = {
    "path",
    "sha256",
    "primary_requirement_id",
    "supports_requirement_ids",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def _canonical_json_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _validate_traceability_manifest_data(manifest: dict[str, Any]) -> None:
    """Fail closed unless v2 gives every v1 artifact one primary assignment."""

    assert set(manifest) == TRACEABILITY_ROOT_KEYS
    assert manifest["schema_version"] == "2.0.0"
    assert manifest["artifact_id"] == "natal-time-b1-artifact-manifest-v2"
    assert manifest["status"] == "SUPERSEDING_SINGLE_PRIMARY_TRACEABILITY"
    assert manifest["digest_algorithm"] == "sha256"

    supersedes = manifest["supersedes"]
    assert supersedes == {
        "artifact_id": "natal-time-b1-artifact-manifest-v1",
        "path": "state/NATAL-TIME-B1-ARTIFACT-MANIFEST-V1.json",
        "sha256": _sha256(ARTIFACT_MANIFEST_V1),
    }
    assert "sole controlling assignment" in manifest["assignment_semantics"][
        "primary_requirement_id"
    ]
    assert "non-controlling" in manifest["assignment_semantics"][
        "supports_requirement_ids"
    ]
    dependencies = manifest["matrix_dependencies"]
    assert dependencies == [
        {
            "path": "state/NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json",
            "sha256": _sha256(
                ROOT / "state" / "NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json"
            ),
            "dependency_type": "PROTECTED_BASELINE_BINDING",
        },
        {
            "path": "state/NATAL-TIME-OPTION-B-ARTIFACT-MANIFEST-V1.json",
            "sha256": _sha256(
                ROOT / "state" / "NATAL-TIME-OPTION-B-ARTIFACT-MANIFEST-V1.json"
            ),
            "dependency_type": "ACCEPTED_PRIOR_ARTIFACT_BINDING",
        },
    ]

    artifacts = manifest["artifacts"]
    assert isinstance(artifacts, list)
    assert manifest["artifact_count"] == len(artifacts) == 33

    original = load_json(ARTIFACT_MANIFEST_V1)
    original_paths = [item["path"] for item in original["artifacts"]]
    paths = [item.get("path") for item in artifacts]
    assert len(paths) == len(set(paths))
    assert set(paths) == set(original_paths)

    for item in artifacts:
        assert isinstance(item, dict)
        assert set(item) == TRACEABILITY_ARTIFACT_KEYS
        path = item["path"]
        digest = item["sha256"]
        primary = item["primary_requirement_id"]
        supports = item["supports_requirement_ids"]
        assert isinstance(path, str) and path in original_paths
        assert isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest)
        assert _sha256(ROOT / path) == digest
        assert isinstance(primary, str) and primary in VALID_B1_REQUIREMENT_IDS
        assert isinstance(supports, list)
        assert all(
            isinstance(requirement, str) and requirement in VALID_B1_REQUIREMENT_IDS
            for requirement in supports
        )
        assert len(supports) == len(set(supports))
        assert primary not in supports

    records_by_path = {
        item["path"]: item for item in [*artifacts, *dependencies]
    }
    matrix = load_json(ACCEPTANCE_MATRIX)
    assert matrix["requirement_count"] == 64
    assert [item["requirement_id"] for item in matrix["requirements"]] == [
        f"B1-{index:02d}" for index in range(1, 65)
    ]
    for requirement in matrix["requirements"]:
        record = records_by_path[requirement["artifact"]]
        assert requirement["artifact_digest"] == record["sha256"]


def _expect_failure(
    code: str,
    schema_name: str,
    record: dict[str, Any],
    *,
    source: str = ALLOWED_SOURCE,
) -> None:
    try:
        validate_record(schema_name, record, source=source)
    except ValidationFailure as exc:
        assert exc.code == code, str(exc)
    else:
        raise AssertionError(f"expected controlled rejection {code}")


def _set_nested(record: dict[str, Any], field: str, value: Any) -> None:
    parts = field.split(".")
    target = record
    for part in parts[:-1]:
        nested = target[part]
        assert isinstance(nested, dict)
        target = nested
    target[parts[-1]] = value


def _invalid_case(case_id: str) -> tuple[str, dict[str, Any], str]:
    probes = load_json(FIXTURES / "invalid_probes.json")
    case = next(entry for entry in probes["cases"] if entry["case_id"] == case_id)
    record = copy.deepcopy(load_fixture(case["base_fixture"]))
    mutations = case.get("mutations") or [case["mutation"]]
    for mutation in mutations:
        _set_nested(record, mutation["field"], mutation["value"])
        if mutation.get("also_rehash"):
            digest = hashlib.sha256(
                json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            if "access_ledger_digest" in record:
                record["access_ledger_digest"] = f"sha256:{digest}"
    return case["schema"], record, case["expected_code"]


def _schema_object_nodes(schema: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    if schema.get("type") == "object":
        nodes.append(schema)
    for value in schema.values():
        if isinstance(value, dict):
            nodes.extend(_schema_object_nodes(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    nodes.extend(_schema_object_nodes(item))
    return nodes


def _probe(case_id: str) -> None:
    schema, record, code = _invalid_case(case_id)
    _expect_failure(code, schema, record)


def _roles_by_id() -> dict[str, dict[str, Any]]:
    return {item["role_id"]: item for item in load_json(ROLES)["roles"]}


def _threat_classes() -> set[str]:
    return {item["class"] for item in load_json(THREAT_MODEL)["threats"]}


def check_requirement(requirement_id: str) -> None:
    """Run one authoritative requirement without creating scientific content."""

    governance = load_json(GOVERNANCE)

    if requirement_id == "B1-01":
        assert _git("rev-parse", OWNER_COMMIT) == OWNER_COMMIT
        assert _git("rev-parse", f"{OWNER_COMMIT}^{{tree}}") == OWNER_TREE
        assert _sha256(OWNER_RECORD) == OWNER_SHA
        assert OWNER_RECORD.relative_to(ROOT).as_posix() == (
            "docs/NATAL_TIME_OWNER_DECISION_B1_20260830.md"
        )
        return

    if requirement_id == "B1-02":
        assert _git("merge-base", "--is-ancestor", CHECKPOINT_9_RULING, OWNER_COMMIT) == ""
        return

    if requirement_id == "B1-03":
        text = OWNER_RECORD.read_text(encoding="utf-8")
        plain_text = " ".join(text.replace("**", "").split())
        assert "B1 changes the order" in plain_text
        assert "does not remove" in plain_text and "mapping" in plain_text
        assert load_json(UNRESOLVED)["source_route_selected"] is False
        return

    if requirement_id == "B1-04":
        attestation = load_json(BASELINE_ATTESTATION)
        topology = attestation["topology_and_diff"]
        base = topology["baseline_commit"]
        head = topology["implementation_head"]
        expected_commits = _git("rev-list", "--reverse", f"{base}..{head}").splitlines()
        expected_diff = _git("diff", "--name-status", base, head).splitlines()
        assert topology["ordered_commits"] == expected_commits
        assert topology["name_status_diff"] == expected_diff
        return

    if requirement_id == "B1-05":
        closure = load_json(ROOT / "state" / "NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json")
        binding = closure["protected_core_binding"]
        assert binding["protected_path_count"] == 48
        assert all(_sha256(ROOT / item["path"]) == item["sha256"] for item in binding["records"])
        return

    if requirement_id == "B1-06":
        option_b = load_json(ROOT / "state" / "NATAL-TIME-OPTION-B-ARTIFACT-MANIFEST-V1.json")
        assert all(
            _sha256(ROOT / item["path"]) == item["sha256"] for item in option_b["artifacts"]
        )
        checkpoint_8_paths = [
            "state/NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json",
            "docs/NATAL_TIME_CHECKPOINT7_ACCEPTANCE_20260830.md",
            "docs/NATAL_TIME_OWNER_DECISION_DOSSIER_20260830.md",
        ]
        assert _git("diff", "--name-only", CHECKPOINT_9_EVIDENCE, "--", *checkpoint_8_paths) == ""
        return

    if requirement_id == "B1-07":
        assert _git("merge-base", "--is-ancestor", CONCEPTION_COMMIT, SCAN_COMMIT) == ""
        assert CONCEPTION_COMMIT != SCAN_COMMIT
        for path in (CONCEPTION_MD, CONCEPTION_JSON):
            commits = _git(
                "log", "--diff-filter=A", "--format=%H", "--", str(path.relative_to(ROOT))
            ).splitlines()
            assert commits == [CONCEPTION_COMMIT]
        return

    if requirement_id == "B1-08":
        text = CONCEPTION_MD.read_text(encoding="utf-8") + CONCEPTION_JSON.read_text(
            encoding="utf-8"
        )
        assert not re.search(r"https?://|www\.|10\.[0-9]{4,9}/", text, re.IGNORECASE)
        assert not re.search(
            r"\b(COSMIN|FDA|Registered Reports|Kriegeskorte|NIST|W3C|PROV)\b", text
        )
        return

    if requirement_id == "B1-09":
        snapshot = load_json(CONCEPTION_JSON)
        for field in (
            "problem",
            "independent_first_mechanism",
            "anticipated_contamination_routes",
            "independently_generated_insights",
            "open_question_classes",
        ):
            assert snapshot[field]
        assert snapshot["content_embargo"] and snapshot["access_boundary"]
        return

    if requirement_id == "B1-10":
        snapshot = load_json(CONCEPTION_JSON)
        assert snapshot["construct_content_created"] is False
        assert snapshot["explicit_nonselections"]["construct_or_domain"] == "UNSELECTED"
        assert snapshot["explicit_nonselections"]["measurement_model"] == "UNSELECTED"
        return

    if requirement_id == "B1-11":
        snapshot = load_json(CONCEPTION_JSON)
        assert snapshot["mapping_content_created"] is False
        assert (
            snapshot["explicit_nonselections"][
                "mapping_ontology_feature_hypothesis_model_metric_or_threshold"
            ]
            == "UNSELECTED"
        )
        return

    if requirement_id == "B1-12":
        assert _sha256(CONCEPTION_MD) == (
            "628f806f2dae876a58802113c7a2ef198420f13fc62d24e77ace922e187ce62d"
        )
        assert _sha256(CONCEPTION_JSON) == (
            "0aab29cc1bdfae050581b3c7654603aad5fc8d195ce65a507a5245de8efa754e"
        )
        return

    if requirement_id == "B1-13":
        ledger = load_json(SOURCE_LEDGER)
        assert [item["search_id"] for item in ledger["searches"]] == [
            f"Q{index:02d}" for index in range(1, 21)
        ]
        assert all(item["query"] for item in ledger["searches"])
        assert all(item["version_or_date"] and item["identifier"] for item in ledger["sources"])
        assert ledger["scope"]["eligibility_rule"] and ledger["excluded_results"]
        mapping = load_json(DECISION_LEDGER)["independent_insight_mapping"]
        assert [item["insight_index"] for item in mapping] == list(range(1, 9))
        return

    if requirement_id == "B1-14":
        for path in SCHEMA_PATHS.values():
            for node in _schema_object_nodes(load_json(path)):
                assert node["additionalProperties"] is False
        _probe("B1-INVALID-UNKNOWN-FIELD")
        return

    if requirement_id == "B1-15":
        candidate = load_fixture("candidate_metadata_valid.json")
        validate_record("candidate", candidate)
        assert re.fullmatch(
            r"SYNTH-B1-CANDIDATE-[A-Z0-9]{4,16}", candidate["synthetic_candidate_id"]
        )
        return

    probe_by_requirement = {
        "B1-16": "B1-INVALID-CONSTRUCT-NAME",
        "B1-17": "B1-INVALID-RESPONSE-CONTENT",
        "B1-18": "B1-INVALID-RESPONSE-CONTENT",
        "B1-19": "B1-INVALID-MEASUREMENT-MODEL",
        "B1-20": "B1-INVALID-COEFFICIENT",
        "B1-21": "B1-INVALID-POPULATION",
        "B1-22": "B1-INVALID-CHART-FIELD",
        "B1-23": "B1-INVALID-MAPPING-RULE",
        "B1-24": "B1-INVALID-REHASHED-MAPPING",
    }
    if requirement_id in probe_by_requirement:
        _probe(probe_by_requirement[requirement_id])
        return

    if requirement_id == "B1-25":
        routes = governance["source_route_classes"]
        assert {item["route_class"] for item in routes} == {
            "ESTABLISHED_NON_HD_CONSTRUCT_OR_INSTRUMENT",
            "CHART_BLIND_CONCEPT_ELICITATION",
            "CHART_BLIND_BEHAVIORAL_OR_OBSERVATIONAL_TAXONOMY",
            "CHART_BLIND_PHENOMENOLOGICAL_TAXONOMY",
            "INDEPENDENT_NON_HD_THEORY_DERIVATION",
            "STAGED_INDEPENDENT_HYBRID",
            "UNSELECTED",
        }
        assert all(
            item["selection_status"] in {"UNSELECTED", "ACTIVE_PLACEHOLDER"}
            for item in routes
        )
        return

    if requirement_id == "B1-26":
        selection = governance["route_selection"]
        assert selection["selected_route"] == "UNSELECTED"
        assert selection["preferred_route"] == "NONE"
        assert selection["default_route"] == "NONE"
        assert selection["authorized_route"] == "NONE"
        assert selection["ranking_present"] is False
        return

    if requirement_id == "B1-27":
        required = set(governance["future_source_record_required_metadata"])
        assert {"provenance_digest", "astrohd_exposure_state", "contamination_state"} <= required
        return

    if requirement_id == "B1-28":
        assert governance["eligibility_rules"]["unknown_provenance"] == (
            "FAIL_CLOSED_INELIGIBLE"
        )
        _probe("B1-INVALID-UNKNOWN-PROVENANCE-CLEAN")
        return

    if requirement_id == "B1-29":
        exclusions = set(governance["required_exclusion_states"])
        assert {
            "ASTROHD_SEEDED",
            "CHART_EXPOSED_AUTHOR",
            "MAPPING_BACKSOLVED",
            "PRIOR_INDIVIDUALIZED_FEEDBACK_EXPOSED",
        } <= exclusions
        assert governance["eligibility_rules"]["astrohd_seeded_or_exposed"] == (
            "INELIGIBLE_FOR_CLEAN_B1"
        )
        return

    if requirement_id == "B1-30":
        assert governance["generic_scan_claim_limit"].startswith("NO_CLAIM")
        assert load_json(DECISION_LEDGER)["overlapping_established_instrument_claim"] == (
            "NOT_EVALUATED_CONSTRUCT_SPECIFIC_SCAN_PROHIBITED"
        )
        return

    if requirement_id == "B1-31":
        protocol = load_json(SCAN_PROTOCOL)
        sequence = protocol["prerequisite_sequence"]
        conception_step = (
            "CONSTRUCT_SPECIFIC_CONCEPTION_AND_BOUNDARIES_FROZEN_OUTSIDE_ASTROHD_CONTEXT"
        )
        first_query_step = "FIRST_CONSTRUCT_SPECIFIC_QUERY_MAY_BEGIN_ONLY_AFTER_PRIOR_STEPS"
        assert sequence.index(conception_step) < sequence.index(first_query_step)
        return

    if requirement_id == "B1-32":
        dimensions = set(load_json(SCAN_PROTOCOL)["required_search_dimensions"])
        assert {
            "SYNONYMS_AND_PRIOR_TERMINOLOGY",
            "NEIGHBORING_CONSTRUCTS_AND_REDUNDANCY",
            "EXISTING_QUESTIONNAIRES_AND_SCALES",
            "OBSERVER_REPORTS",
            "BEHAVIORAL_OR_OBJECTIVE_PROXIES_AND_TASKS",
            "VERSION_AND_SUPERSESSION_HISTORY",
            "LICENSING_PERMISSIONS_COST_BURDEN_AND_TOOLING",
            "FAILURE_NONREPLICATION_AND_OTHER_ADVERSE_EVIDENCE",
        } <= dimensions
        return

    if requirement_id == "B1-33":
        protocol = load_json(SCAN_PROTOCOL)
        assert protocol["allowed_terminal_decisions"] == [
            "REUSE",
            "ADAPT",
            "COMPOSE",
            "BOUNDED_COMPARATIVE_EXPERIMENT",
            "DEVELOP_NEW",
        ]
        assert protocol["terminal_decision"] == "UNSELECTED"
        return

    if requirement_id == "B1-34":
        protocol = load_json(SCAN_PROTOCOL)
        assert protocol["status"] == "FUTURE_TEMPLATE_NOT_EXECUTED"
        assert protocol["executed_query_count"] == 0
        assert protocol["construct_content_present"] is False
        return

    if requirement_id == "B1-35":
        assert set(_roles_by_id()) == {
            "ASTROHD_AWARE_GOVERNANCE",
            "CHART_BLIND_AUTHORSHIP",
            "CONSTRUCT_SOURCE_REVIEW",
            "CONTENT_CUSTODY",
            "MEASUREMENT_DEVELOPMENT",
            "RELIABILITY_ANALYSIS",
            "MAPPING",
            "MAPPING_EVALUATION",
            "INCREMENTAL_VALUE_EVALUATION",
            "DATA_AND_ACCESS_CUSTODY",
        }
        return

    if requirement_id == "B1-36":
        context = load_json(ROLES)["astrohd_aware_context"]
        assert set(context["prohibited"]) == {
            "AUTHOR_CONTENT", "EDIT_CONTENT", "SELECT_CONTENT", "RANK_CONTENT",
            "REFINE_CONTENT", "APPROVE_CONTENT",
        }
        return

    if requirement_id == "B1-37":
        denied = set(load_json(ROLES)["future_isolated_model_must_not_receive"])
        assert {
            "ASTROHD_REPOSITORY",
            "ASTROHD_MECHANICS_OR_LABELS",
            "ASTROHD_RESULTS_OR_MAPPING_SUGGESTIONS",
        } <= denied
        return

    if requirement_id == "B1-38":
        roles = load_json(ROLES)
        assert "ASTROHD_MEMORY_OR_RETRIEVAL" in roles["future_isolated_model_must_not_receive"]
        assert "ASTROHD_PROMPT_HISTORY" in roles["future_isolated_model_must_not_receive"]
        assert roles["astrohd_exposed_model_blindness_by_instruction"] == (
            "IMPOSSIBLE_FOR_B1_ELIGIBILITY"
        )
        return

    if requirement_id == "B1-39":
        roles = _roles_by_id()
        assert roles["MAPPING"]["pre_freeze_content_access"] == (
            "DENIED_UNTIL_CONSTRUCT_AND_RELIABILITY_FREEZE"
        )
        assert load_json(ROLES)["mapping_team_pre_freeze_influence"] == "PROHIBITED"
        return

    if requirement_id == "B1-40":
        schema = load_json(SCHEMA_PATHS["access"])
        properties = schema["properties"]
        assert properties["append_only"]["const"] is True
        for field in ("provenance_digest", "previous_event_digest", "access_event_digest"):
            assert "pattern" in properties[field]
        validate_access_history([load_fixture("access_event_valid.json")])
        return

    if requirement_id == "B1-41":
        _probe("B1-INVALID-EXPOSURE-CLEAN")
        return

    if requirement_id == "B1-42":
        _probe("B1-INVALID-ROLE-ERASES-EXPOSURE")
        assert governance["eligibility_rules"]["role_reassignment_after_exposure"] == (
            "DOES_NOT_ERASE_CONTAMINATION"
        )
        return

    if requirement_id == "B1-43":
        first = copy.deepcopy(load_fixture("access_event_valid.json"))
        first["synthetic_actor_id"] = "SYNTH-B1-ACTOR-LINK0001"
        first["synthetic_session_id"] = "SYNTH-B1-SESSION-LINK0001"
        first["synthetic_source_id"] = "SYNTH-B1-SOURCE-LINK0001"
        first["actor_role_id"] = "CHART_BLIND_AUTHORSHIP"
        second = copy.deepcopy(first)
        second["synthetic_access_event_id"] = "SYNTH-B1-EVENT-LINK0002"
        second["event_sequence"] = 1
        second["previous_event_digest"] = first["access_event_digest"]
        second["access_event_digest"] = (
            "sha256:6666666666666666666666666666666666666666666666666666666666666666"
        )
        second["actor_role_id"] = "MAPPING"
        second["astrohd_exposure_state"] = "EXPOSED_CONTAMINATED"
        second["contamination_state"] = "CONTAMINATED_INELIGIBLE"
        validate_access_history([first, second])
        second["contamination_state"] = "CLEAN_SYNTHETIC_METADATA_ONLY"
        try:
            validate_access_history([first, second])
        except ValidationFailure as exc:
            assert exc.code in {
                "B1_EXPOSURE_CONTAMINATION_REQUIRED",
                "B1_PRE_FREEZE_MAPPING_ACCESS",
                "B1_CROSS_ROLE_CONTAMINATION_REQUIRED",
            }
        else:
            raise AssertionError("expected incompatible-role contamination rejection")
        return

    if requirement_id == "B1-44":
        roles = load_json(ROLES)
        assert roles["source_reviewer_mapping_fit_rewrite"] == "PROHIBITED"
        assert _roles_by_id()["CONSTRUCT_SOURCE_REVIEW"]["content_authorship_eligibility"] == (
            "INELIGIBLE_TO_REWRITE_FOR_ASTROHD_FIT"
        )
        return

    if requirement_id == "B1-45":
        roles = load_json(ROLES)
        assert roles["real_assignments_present"] is False
        assert roles["human_access_system_implemented"] is False
        assert roles["participant_workflow_implemented"] is False
        assert all(item["assignment"] == "UNASSIGNED" for item in roles["roles"])
        return

    if requirement_id == "B1-46":
        gate = load_json(FREEZE_GATE)
        assert len(gate["future_required_slots"]) == 10
        assert all(
            item["current_status"] == "UNSET_CONTENT_EMBARGOED"
            for item in gate["future_required_slots"]
        )
        assert gate["content_bearing_values_present"] is False
        return

    if requirement_id == "B1-47":
        rules = load_json(FREEZE_GATE)["eligibility_rules"]
        assert rules["specific_scan_receipt_required"] is True
        assert rules["explicit_source_decision_required"] is True
        assert load_json(FREEZE_GATE)["current_freeze_valid"] is False
        return

    if requirement_id == "B1-48":
        firewall = load_json(MAPPING_FIREWALL)
        assert firewall["gate_rules"]["mapping_gate_before_complete_construct_freeze"] == "CLOSED"
        assert firewall["ordered_stages"][6]["stage_id"] == "SEPARATE_MAPPING_PREREGISTRATION"
        assert firewall["ordered_stages"][6]["current_status"] == "BLOCKED_BY_PRIOR_STAGES"
        return

    if requirement_id == "B1-49":
        rules = load_json(MAPPING_FIREWALL)["gate_rules"]
        assert rules["mapping_hypothesis_identity"] == "FUTURE_SEPARATE_CONTENT_HASH_REQUIRED"
        assert rules["mapping_preregistration_time"] == "AFTER_CONSTRUCT_AND_RELIABILITY_FREEZE"
        return

    if requirement_id == "B1-50":
        assert load_json(MAPPING_FIREWALL)["gate_rules"][
            "mapping_evidence_may_modify_construct_in_place"
        ] is False
        return

    if requirement_id == "B1-51":
        control = load_json(CHANGE_CONTROL)
        assert set(control["controlled_changes_after_mapping_exposure"]) == {
            "RENAME", "MERGE", "SPLIT", "DELETE", "NARROW", "BROADEN", "REDEFINE"
        }
        disposition = control["required_disposition_for_any_controlled_change"]
        assert disposition["new_version"] == "REQUIRED"
        assert disposition["original_version"] == "PRESERVED_IMMUTABLE"
        assert disposition["original_result"] == "PRESERVED_REPORTABLE"
        return

    if requirement_id == "B1-52":
        disposition = load_json(CHANGE_CONTROL)["required_disposition_for_any_controlled_change"]
        assert disposition["new_version_claim_status"] == "EXPLORATORY"
        assert disposition["exposed_evidence_or_components_for_confirmation"] == "INELIGIBLE"
        return

    if requirement_id == "B1-53":
        policy = load_json(CHANGE_CONTROL)["null_result_policy"]
        assert policy["null_weak_unstable_or_nonreplicating_result"] == "PRESERVE_AND_REPORT"
        assert policy["construct_repair_to_rescue_result"] == "PROHIBITED"
        return

    if requirement_id == "B1-54":
        lanes = load_json(CLAIM_LANES)
        assert [item["lane_id"] for item in lanes["lanes"]] == [
            "R_RELIABILITY", "M_MAPPING", "I_INCREMENTAL_VALUE"
        ]
        assert lanes["lane_results_present"] is False
        return

    if requirement_id == "B1-55":
        assert load_json(CLAIM_LANES)["evidence_transfer_rules"]["reliability_to_mapping"] == (
            "PROHIBITED"
        )
        return

    if requirement_id == "B1-56":
        assert load_json(CLAIM_LANES)["evidence_transfer_rules"][
            "mapping_to_incremental_value"
        ] == "PROHIBITED"
        return

    if requirement_id == "B1-57":
        assert load_json(CLAIM_LANES)["ordinary_non_hd_and_null_controls"] == (
            "FUTURE_RESERVED_UNSELECTED_NOT_IMPLEMENTED"
        )
        return

    if requirement_id == "B1-58":
        lanes = load_json(CLAIM_LANES)
        assert lanes["combined_scalar"] == "PROHIBITED"
        assert lanes["combined_confidence"] == "PROHIBITED"
        assert lanes["automatic_progression"] == "PROHIBITED"
        return

    if requirement_id == "B1-59":
        required = {
            "DIRECT_ASTROHD_TERMINOLOGY_LEAKAGE",
            "INDIRECT_SEMANTIC_OR_FAVORED_SOURCE_LEAKAGE",
            "OWNER_PROMPT_OR_EXAMPLE_LEAKAGE",
            "REPOSITORY_ACCESS_LEAKAGE",
            "RETRIEVAL_OR_EMBEDDING_LEAKAGE",
            "PROMPT_HISTORY_OR_MODEL_MEMORY_LEAKAGE",
            "ASTROHD_EXPOSED_MODEL_GENERATION",
            "SOURCE_SELECTION_FOR_MAPPING_LIKELIHOOD",
            "MAPPING_TEAM_INFLUENCE_ON_DEVELOPMENT",
            "SELECTIVE_CONSTRUCT_RETENTION",
            "POST_HOC_RENAME_MERGE_SPLIT_DELETE_OR_REDEFINITION",
            "CONSTRUCT_PROLIFERATION_OR_REDUNDANCY",
            "NAMING_AND_OPERATIONALIZATION_MISMATCH",
            "RELIABILITY_CHERRY_PICKING",
            "MAPPING_CHERRY_PICKING",
            "DISCOVERY_EVIDENCE_REUSED_FOR_CONFIRMATION",
            "CONNECTED_ACTOR_SESSION_SOURCE_OR_EVIDENCE_LEAKAGE",
            "NULL_WEAK_UNSTABLE_OR_NONREPLICATING_RESULT_SUPPRESSION",
            "RELIABILITY_MAPPING_OR_INCREMENTAL_VALUE_LANE_CONFLATION",
            "SYNTHETIC_TO_LIVE_TRANSITION_WITHOUT_NEW_AUTHORITY",
        }
        assert required == _threat_classes()
        return

    if requirement_id == "B1-60":
        manifest = load_json(FIXTURE_MANIFEST)
        assert manifest["content_audit"]["meaningful_construct_content_count"] == 0
        assert manifest["content_audit"]["personal_or_live_record_count"] == 0
        assert manifest["content_audit"]["meaningful_mapping_content_count"] == 0
        for item in manifest["fixtures"]:
            path = ROOT / item["path"]
            assert _sha256(path) == item["sha256"]
            assert "CONSPICUOUSLY_SYNTHETIC_B1_" in path.read_text(encoding="utf-8")
        return

    if requirement_id == "B1-61":
        production_python = list((ROOT / "src").rglob("*.py"))
        assert not any(
            "tests.b1_precontent" in path.read_text(encoding="utf-8")
            or "b1_precontent.validator" in path.read_text(encoding="utf-8")
            for path in production_python
        )
        return

    if requirement_id == "B1-62":
        manifest = load_json(ARTIFACT_MANIFEST)
        _validate_traceability_manifest_data(manifest)
        return

    if requirement_id == "B1-63":
        plan = load_json(BASELINE_ATTESTATION)["exact_head_gate_plan"]
        assert set(plan) == {
            "FULL_TESTS",
            "STRICT_MYPY",
            "CHANGED_FILE_RUFF",
            "PRIVACY_HISTORY_BUILD",
            "PROTECTED_COMPARISON",
            "ACCEPTED_ARTIFACT_COMPARISON",
            "GIT_DIFF_CHECK",
            "CLEAN_INDEX_AND_WORKTREE",
        }
        assert all(value["required"] is True for value in plan.values())
        return

    if requirement_id == "B1-64":
        attestation = load_json(BASELINE_ATTESTATION)
        assert (
            attestation["no_external_action_confirmation"]["all_prohibited_actions_absent"]
            is True
        )
        assert attestation["topology_and_diff"]["name_status_diff"]
        assert load_json(CORRECTION_LEDGER)["open_correction_count"] == 0
        assert load_json(UNRESOLVED)["additional_work_authorized_by_this_register"] is False
        return

    raise AssertionError(f"unknown requirement: {requirement_id}")
