"""Exact construct-neutral checks for the 72 Option B acceptance requirements."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from tests.option_b.validator import (
    ALLOWED_SOURCE,
    CONTRACT_PATH,
    FIXTURES,
    ROOT,
    SCHEMA_PATHS,
    ValidationFailure,
    load_fixture,
    load_json,
    validate_record,
)

OWNER_SHA = "c24bb062bd90466f0be1a5be03211c8933e80bc1b4eaeee9509d5856bea02fc4"
CHECKPOINT_8 = "63bfb78909a97eb5b8b31efe55e065a6f78973a2"
CONCEPTION_COMMIT = "aaec2fecad74a1dfc9fa6fa7ec75d90a77f9c1fd"
SCAN_COMMIT = "98b829e812c4cf2fdff7e02f00fa39ce137e6872"
PURPOSE = "measurement_reliability_prerequisite_screen"

CONCEPTION_MD = ROOT / "docs" / "NATAL_TIME_OPTION_B_INDEPENDENT_CONCEPTION_SNAPSHOT_20260830.md"
CONCEPTION_JSON = ROOT / "state" / "NATAL-TIME-OPTION-B-INDEPENDENT-CONCEPTION-SNAPSHOT-V1.json"
SOURCE_LEDGER = ROOT / "state" / "NATAL-TIME-OPTION-B-SOURCE-LEDGER-V1.json"
DECISION_LEDGER = ROOT / "state" / "NATAL-TIME-OPTION-B-METHODS-DECISION-LEDGER-V1.json"
THREAT_MODEL = ROOT / "state" / "NATAL-TIME-MEASUREMENT-RELIABILITY-THREAT-MODEL-V1.json"
UNRESOLVED = ROOT / "state" / "NATAL-TIME-OPTION-B-UNRESOLVED-DECISIONS-V1.json"
FIXTURE_MANIFEST = ROOT / "state" / "NATAL-TIME-OPTION-B-SYNTHETIC-FIXTURE-MANIFEST-V1.json"
ARTIFACT_MANIFEST = ROOT / "state" / "NATAL-TIME-OPTION-B-ARTIFACT-MANIFEST-V1.json"
ACCEPTANCE_MATRIX = ROOT / "state" / "NATAL-TIME-OPTION-B-ACCEPTANCE-MATRIX-V1.json"
PRO_RULING = ROOT / "docs" / "PRO_SUPERVISION_OPTION_B_CONTRACT_20260830.md"

SUBSTANTIVE_JSON = [
    CONCEPTION_JSON,
    SOURCE_LEDGER,
    DECISION_LEDGER,
    CONTRACT_PATH,
    *SCHEMA_PATHS.values(),
    THREAT_MODEL,
    UNRESOLVED,
    FIXTURE_MANIFEST,
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _expect_failure(
    code: str, schema_name: str, record: dict[str, Any], *, source: str = ALLOWED_SOURCE
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
            record["response_bundle_digest"] = f"sha256:{digest}"
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


def _all_schema_property_names() -> set[str]:
    names: set[str] = set()
    for path in SCHEMA_PATHS.values():
        schema = load_json(path)
        for node in _schema_object_nodes(schema):
            names.update(node.get("properties", {}))
    return names


def _threat_classes() -> set[str]:
    return {item["class"] for item in load_json(THREAT_MODEL)["threats"]}


def check_requirement(requirement_id: str) -> None:
    """Run one authoritative Pro requirement without making an empirical choice."""

    contract = load_json(CONTRACT_PATH)

    if requirement_id == "OB-01":
        assert _git("merge-base", "--is-ancestor", CONCEPTION_COMMIT, SCAN_COMMIT) == ""
        assert CONCEPTION_COMMIT != SCAN_COMMIT
        return

    if requirement_id == "OB-02":
        text = CONCEPTION_MD.read_text(encoding="utf-8") + CONCEPTION_JSON.read_text(
            encoding="utf-8"
        )
        assert not re.search(r"https?://|www\.|10\.[0-9]{4,9}/", text, re.IGNORECASE)
        assert not re.search(r"\b(COSMIN|GRRAS|WCAG|AERA|NCME|Forer|Cronbach)\b", text)
        snapshot = load_json(CONCEPTION_JSON)
        assert set(snapshot["explicit_nonselections"].values()) == {"UNSELECTED"}
        return

    if requirement_id == "OB-03":
        assert (
            _sha256(CONCEPTION_MD)
            == "4a9d579e4dddf773eb7532ae725cc610662396806870a4235f1d7e5cccf5cf7e"
        )
        assert (
            _sha256(CONCEPTION_JSON)
            == "d8b1692283271c2195a802d48e4b71307371424b075ff69ab502db51ca5d3ba8"
        )
        return

    if requirement_id == "OB-04":
        mapping = load_json(DECISION_LEDGER)["independent_insight_mapping"]
        assert [item["insight_index"] for item in mapping] == list(range(1, 9))
        assert {item["post_scan_status"] for item in mapping} <= {
            "REUSED",
            "ADAPTED",
            "SUPERSEDED",
            "STILL_NOVEL",
        }
        return

    if requirement_id == "OB-05":
        ledger = load_json(SOURCE_LEDGER)
        assert ledger["search_date"] == "2026-08-30"
        assert [item["search_id"] for item in ledger["searches"]] == [
            f"Q{index:02d}" for index in range(1, 25)
        ]
        assert all(item["query"] for item in ledger["searches"])
        assert all(item["version_or_date"] and item["identifier"] for item in ledger["sources"])
        assert ledger["scope"]["eligibility_rule"] and ledger["scope"]["stopping_rule"]
        return

    if requirement_id == "OB-06":
        queries = [item["query"].lower() for item in load_json(SOURCE_LEDGER)["searches"]]
        assert all("human design" not in query for query in queries)
        assert any("reliability" in query and "human design" not in query for query in queries)
        return

    if requirement_id == "OB-07":
        changed = _git("diff", "--name-only", f"{CONCEPTION_COMMIT}..HEAD").splitlines()
        assert not any(path.lower().endswith(".pdf") for path in changed)
        assert (
            "copyrighted_full_text_corpus_storage" in load_json(SOURCE_LEDGER)["scope"]["excluded"]
        )
        return

    if requirement_id == "OB-08":
        assert contract["active_purpose"] == PURPOSE
        for path in SUBSTANTIVE_JSON:
            artifact = load_json(path)
            purpose = artifact.get("active_purpose") or artifact.get("x-provenance", {}).get(
                "active_purpose"
            )
            assert purpose == PURPOSE
        return

    if requirement_id == "OB-09":
        for path in SCHEMA_PATHS.values():
            for node in _schema_object_nodes(load_json(path)):
                assert node["additionalProperties"] is False
        return

    if requirement_id == "OB-10":
        for case_id in (
            "SYNTH-INVALID-CONSTRUCT-FIELD",
            "SYNTH-INVALID-CHART-FIELD",
            "SYNTH-INVALID-REFERENCE-SET-FIELD",
            "SYNTH-INVALID-SCORE-FIELD",
            "SYNTH-INVALID-THRESHOLD-FIELD",
            "SYNTH-INVALID-CODING-CATEGORY",
            "SYNTH-INVALID-RESPONSE-CONTENT",
        ):
            schema, record, code = _invalid_case(case_id)
            _expect_failure(code, schema, record)
        return

    if requirement_id == "OB-11":
        schema, record, code = _invalid_case("SYNTH-INVALID-REHASHED-CONSTRUCT")
        _expect_failure(code, schema, record)
        return

    if requirement_id == "OB-12":
        for path in SUBSTANTIVE_JSON:
            artifact = load_json(path)
            provenance = artifact.get("provenance") or artifact.get("x-provenance")
            assert provenance["owner_record_sha256"] == OWNER_SHA
            assert provenance["checkpoint_8_accepted_head"] == CHECKPOINT_8
        return

    if requirement_id == "OB-13":
        versioning = contract["versioning_and_supersession"]
        assert versioning["immutability"] == "REQUIRED_AFTER_COMMIT"
        assert versioning["correction_mode"] == "NEW_SUPERSEDING_ARTIFACT_WITH_EXPLICIT_LINEAGE"
        return

    if requirement_id == "OB-14":
        administration = load_fixture("administration_valid.json")
        coding = load_fixture("coding_valid.json")
        assert administration["synthetic_participant_id"].startswith("SYNTH-P-")
        assert administration["synthetic_component_id"].startswith("SYNTH-CC-")
        assert coding["synthetic_coder_id"].startswith("SYNTH-CODER-")
        return

    if requirement_id == "OB-15":
        audit = load_json(FIXTURE_MANIFEST)["content_audit"]
        zero_fields = [
            key
            for key in audit
            if key.endswith("_count") and key != "prohibited_field_name_probe_count"
        ]
        assert all(audit[key] == 0 for key in zero_fields)
        raw = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURES.glob("*.json"))
        assert "@" not in raw
        assert not re.search(r'"(?:email|phone|name)"\s*:', raw, re.IGNORECASE)
        assert not re.search(r"\b(?:19|20)[0-9]{2}-[01][0-9]-[0-3][0-9]\b", raw)
        return

    if requirement_id == "OB-16":
        forbidden = {
            "chart",
            "T_i",
            "C_i",
            "S_i",
            "candidate_interval",
            "compatibility",
            "relationship_evidence",
        }
        assert _all_schema_property_names().isdisjoint(forbidden)
        return

    if requirement_id == "OB-17":
        _expect_failure(
            "OB_NON_SYNTHETIC_INPUT",
            "administration",
            {"record_class": "PRODUCTION_RECORD_SENTINEL"},
            source="PRODUCTION_OR_PRIVATE_RECORD",
        )
        return

    if requirement_id == "OB-18":
        boundary = load_json(FIXTURE_MANIFEST)["identity_boundary"]
        assert boundary["deterministic_live_or_private_linkage"] == "PROHIBITED_AND_ABSENT"
        assert boundary["live_or_private_source"] == "NONE"
        return

    if requirement_id == "OB-19":
        needles = [path.name for path in SCHEMA_PATHS.values()] + ["tests.option_b.validator"]
        for source in (ROOT / "src").rglob("*.py"):
            text = source.read_text(encoding="utf-8")
            assert all(needle not in text for needle in needles)
        return

    if requirement_id == "OB-20":
        families = {
            item["family"] for item in contract["permitted_future_measurement_property_families"]
        }
        assert {"RELATIVE_RELIABILITY", "AGREEMENT", "MEASUREMENT_ERROR"} <= families
        return

    if requirement_id == "OB-21":
        assert contract["global_reliability_scalar"] == "PROHIBITED"
        return

    if requirement_id == "OB-22":
        assert contract["preferred_default_coefficient"] == "NONE"
        return

    if requirement_id == "OB-23":
        assert contract["numeric_acceptance_threshold"] == "NONE"
        assert contract["verbal_quality_band"] == "NONE"
        return

    if requirement_id == "OB-24":
        plan = load_fixture("property_plan_valid.json")["test_retest_eligibility"]
        assert set(plan) == {
            "construct_temporal_ontology",
            "expected_stability_evidence",
            "recall_risk",
            "interim_events",
            "administration_condition_equivalence",
            "proposed_interval_rationale",
        }
        return

    if requirement_id == "OB-25":
        schema = load_json(SCHEMA_PATHS["property_plan"])
        statuses = schema["properties"]["status"]["enum"]
        assert "EXECUTABLE" not in statuses
        assert set(
            load_fixture("property_plan_valid.json")["test_retest_eligibility"].values()
        ) == {"UNRESOLVED"}
        return

    if requirement_id == "OB-26":
        family = next(
            item
            for item in contract["permitted_future_measurement_property_families"]
            if item["family"] == "INTER_RATER"
        )
        assert {"INDEPENDENT_CODING", "NO_PRIOR_CODE_VISIBILITY"} <= set(family["preconditions"])
        return

    if requirement_id == "OB-27":
        eligibility = load_fixture("property_plan_valid.json")["internal_consistency_eligibility"]
        assert eligibility == {
            "reflective_model_status": "UNSELECTED",
            "structural_validity_status": "UNSELECTED",
            "status": "INELIGIBLE",
        }
        return

    if requirement_id == "OB-28":
        assert contract["semantic_guards"]["correlation_only_satisfies_agreement"] is False
        return

    if requirement_id == "OB-29":
        assert set(contract["future_estimate_reserved_slots"]) == {
            "POINT_ESTIMATE",
            "UNCERTAINTY_INTERVAL",
            "MEASUREMENT_ERROR",
            "SAMPLE_AND_CONTEXT_DESCRIPTION",
            "ASSUMPTIONS",
        }
        assert contract["future_estimate_slot_status"] == "PROHIBITED_UNTIL_LATER_APPROVED_CONTRACT"
        return

    if requirement_id == "OB-30":
        guards = contract["semantic_guards"]
        assert guards["reliability_may_populate_validity"] is False
        assert guards["reliability_may_populate_rectification"] is False
        return

    if requirement_id == "OB-31":
        schema, record, code = _invalid_case("SYNTH-INVALID-PRIOR-CODE-CLEAN")
        _expect_failure(code, schema, record)
        return

    if requirement_id == "OB-32":
        schema, record, code = _invalid_case("SYNTH-INVALID-ADJUDICATION-REWRITE")
        _expect_failure(code, schema, record)
        return

    if requirement_id == "OB-33":
        rules = contract["role_and_access_boundaries"]["rules"]
        assert (
            "DEVELOPMENT_ADJUDICATION_CANNOT_BECOME_LOCKED_GROUND_TRUTH_WITHOUT_LATER_FREEZE"
            in rules
        )
        return

    if requirement_id == "OB-34":
        states = contract["contamination_states"]
        for marker in (
            "PRIOR_RESPONSE",
            "PRIOR_CODE",
            "CHART_OR_LABEL",
            "INDIVIDUALIZED_FEEDBACK",
            "REFERENCE_TIME",
        ):
            assert any(marker in state for state in states)
        return

    if requirement_id == "OB-35":
        semantics = contract["contamination_semantics"]
        assert semantics["clean_estimate_eligibility"].startswith(
            "CONTAMINATED_OBSERVATIONS_PROHIBITED"
        )
        assert semantics["silent_repair"] == "PROHIBITED"
        return

    if requirement_id == "OB-36":
        versioning = contract["versioning_and_supersession"]
        assert versioning["coding_protocol_change"] == "NEW_VERSION_AND_NO_UNQUALIFIED_POOLING"
        return

    if requirement_id == "OB-37":
        assert {
            "ITEM_MISSING",
            "OCCASION_MISSING",
            "DROPOUT",
            "REFUSAL",
            "TECHNICAL_FAILURE",
            "ACCESSIBILITY_FAILURE",
            "STRUCTURAL_NOT_APPLICABLE",
            "UNKNOWN_REASON",
        } <= set(contract["missingness_classes"])
        return

    if requirement_id == "OB-38":
        assert contract["missingness_semantics"]["value_conversion"] == "PROHIBITED"
        return

    if requirement_id == "OB-39":
        semantics = contract["missingness_semantics"]
        assert semantics["reason_provenance"] == "REQUIRED"
        assert semantics["denominator_provenance"] == "REQUIRED"
        return

    if requirement_id == "OB-40":
        assert contract["missingness_semantics"]["complete_case_default"] == "PROHIBITED"
        return

    if requirement_id == "OB-41":
        semantics = contract["missingness_semantics"]
        assert {
            semantics[key] for key in ("imputation", "weighting", "deletion", "sensitivity_method")
        } == {"UNSELECTED"}
        return

    if requirement_id == "OB-42":
        assert (
            contract["missingness_semantics"]["missing_retest_classification"]
            == "NEITHER_AGREEMENT_DISAGREEMENT_NOR_ABSTENTION"
        )
        return

    if requirement_id == "OB-43":
        assert "PLANNED_MISSING" in contract["missingness_classes"]
        assert contract["missingness_semantics"]["planned_vs_unplanned"] == "DISTINCT"
        return

    if requirement_id == "OB-44":
        assert "ATTRITION_CONDITIONED_ON_PRIOR_RESPONSE_OR_FEEDBACK" in _threat_classes()
        return

    if requirement_id == "OB-45":
        classes = _threat_classes()
        expected_fragments = (
            "ACQUIESCENCE",
            "EXTREME_RESPONDING",
            "MIDPOINT_RESPONDING",
            "STRAIGHTLINING",
            "SOCIAL_DESIRABILITY",
            "DEMAND_CHARACTERISTICS",
            "EXPECTANCY",
            "FAMILIARITY",
            "POSITIVE_VALENCE",
            "AUTHORITY",
            "PERSONAL_VALIDATION",
        )
        assert all(any(fragment in item for item in classes) for fragment in expected_fragments)
        return

    if requirement_id == "OB-46":
        assert contract["semantic_guards"]["reverse_wording_is_default_remedy"] is False
        return

    if requirement_id == "OB-47":
        assert contract["feedback_order_rule"].startswith(
            "NO_INDIVIDUALIZED_CHART_OR_PERSONALITY_FEEDBACK"
        )
        return

    if requirement_id == "OB-48":
        audit = load_json(FIXTURE_MANIFEST)["content_audit"]
        assert audit["item_or_prompt_content_count"] == 0
        assert audit["response_option_content_count"] == 0
        return

    if requirement_id == "OB-49":
        assert (
            contract["semantic_guards"]["stable_barnum_acceptance_is_construct_reliability"]
            is False
        )
        return

    if requirement_id == "OB-50":
        assert (
            contract["semantic_guards"]["response_style_adjustment_may_merge_with_target"] is False
        )
        return

    if requirement_id == "OB-51":
        required = set(load_json(SCHEMA_PATHS["administration"])["required"])
        assert {
            "language_version_id",
            "mode_version_id",
            "form_version_id",
            "accommodation_version_id",
        } <= required
        return

    if requirement_id == "OB-52":
        assert set(contract["equivalence_and_pooling"].values()) == {"BLOCKED_UNRESOLVED"}
        return

    if requirement_id == "OB-53":
        assert contract["versioning_and_supersession"]["language_change"] == "NEW_VERSION_REQUIRED"
        return

    if requirement_id == "OB-54":
        assert contract["equivalence_and_pooling"]["cross_group"] == "BLOCKED_UNRESOLVED"
        return

    if requirement_id == "OB-55":
        assert contract["semantic_guards"]["accessibility_metadata_may_silently_exclude"] is False
        return

    if requirement_id == "OB-56":
        assert (
            contract["semantic_guards"][
                "accommodation_variation_is_automatically_participant_error"
            ]
            is False
        )
        assert any(
            item["facet"] == "ACCESSIBILITY_OR_ACCOMMODATION_VERSION"
            for item in contract["replication_facet_registry"]
        )
        return

    if requirement_id == "OB-57":
        boundary = contract["accessibility_boundary"]
        assert boundary["future_target"] == "WCAG_2_2_AA"
        assert boundary["conformance_claim"] == "NONE"
        assert set(boundary["required_future_evaluation"]) == {
            "AUTOMATED",
            "HUMAN",
            "COGNITIVE_ACCESSIBILITY",
        }
        return

    if requirement_id == "OB-58":
        changed = _git("diff", "--name-only", f"{SCAN_COMMIT}..HEAD").splitlines()
        assert not any(path.startswith(("src/", "static/", "templates/")) for path in changed)
        assert contract["accessibility_boundary"]["interface_implemented"] is False
        return

    if requirement_id == "OB-59":
        boundary = contract["connected_component_boundary"]
        assert boundary["multiple_future_data_roles_per_component"] == "PROHIBITED"
        assert {
            "SYNTHETIC_PERSON",
            "SYNTHETIC_ALIAS",
            "SYNTHETIC_REPEAT_PARTICIPATION",
            "SYNTHETIC_PARTNER",
            "SYNTHETIC_HOUSEHOLD_MEMBER",
            "SYNTHETIC_TRANSITIVE_COMPONENT",
        } <= set(boundary["entity_classes"])
        return

    if requirement_id == "OB-60":
        edges = set(contract["connected_component_boundary"]["edge_classes"])
        assert {
            "SYNTHETIC_SHARED_RECRUITER_EDGE",
            "SYNTHETIC_SHARED_SOURCE_EDGE",
            "SYNTHETIC_SHARED_CUSTODIAN_EDGE",
            "SYNTHETIC_SHARED_CODER_EDGE",
        } <= edges
        return

    if requirement_id == "OB-61":
        assert (
            contract["connected_component_boundary"]["role_reassignment_after_exposure"]
            == "APPEND_CONTAMINATION_DO_NOT_REWRITE_HISTORY"
        )
        return

    if requirement_id == "OB-62":
        boundary = contract["connected_component_boundary"]
        assert boundary["split_algorithm"] == "NOT_IMPLEMENTED"
        assert boundary["cohort_allocation"] == "NOT_IMPLEMENTED"
        return

    if requirement_id == "OB-63":
        assert contract["connected_component_boundary"]["live_relationship_source"] == "PROHIBITED"
        return

    if requirement_id == "OB-64":
        manifest = load_json(ARTIFACT_MANIFEST)
        for record in manifest["artifacts"]:
            assert _sha256(ROOT / record["path"]) == record["sha256"]
        return

    if requirement_id == "OB-65":
        paths = [
            CONCEPTION_JSON,
            SOURCE_LEDGER,
            CONTRACT_PATH,
            SCHEMA_PATHS["administration"],
            THREAT_MODEL,
            UNRESOLVED,
            ROOT / "tests" / "option_b" / "validator.py",
            ACCEPTANCE_MATRIX,
        ]
        for path in paths:
            commits = _git(
                "log", "--diff-filter=A", "--format=%H", "--", str(path.relative_to(ROOT))
            ).splitlines()
            assert len(commits) == 1 and re.fullmatch(r"[0-9a-f]{40}", commits[0])
        return

    if requirement_id == "OB-66":
        closure = load_json(ROOT / "state" / "NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json")
        binding = closure["protected_core_binding"]
        assert binding["protected_path_count"] == 48
        assert all(_sha256(ROOT / item["path"]) == item["sha256"] for item in binding["records"])
        return

    if requirement_id == "OB-67":
        paths = [
            "state/NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json",
            "docs/NATAL_TIME_CHECKPOINT7_ACCEPTANCE_20260830.md",
            "docs/NATAL_TIME_OWNER_DECISION_DOSSIER_20260830.md",
        ]
        assert _git("diff", "--name-only", CHECKPOINT_8, "--", *paths) == ""
        return

    if requirement_id == "OB-68":
        text = PRO_RULING.read_text(encoding="utf-8")
        for gate in (
            "Full tests",
            "strict mypy",
            "changed-file Ruff",
            "privacy/history/build",
            "git diff --check",
            "clean index",
            "clean worktree",
        ):
            assert gate in text
        return

    if requirement_id == "OB-69":
        assert "b7660b8c9bcf52cbb14bc5442c13a3a8635aad32" in PRO_RULING.read_text(encoding="utf-8")
        return

    if requirement_id == "OB-70":
        assert "PUSH_MERGE_DEPLOY_OR_PUBLISH" in contract["prohibited_operations"]
        assert load_json(UNRESOLVED)["additional_work_authorized_by_this_register"] is False
        return

    if requirement_id == "OB-71":
        operations = set(contract["prohibited_operations"])
        assert "READ_PARTICIPANT_DOCUMENTARY_RELATIONSHIP_OR_SECRET_DATA" in operations
        assert "ACCEPT_LIVE_OR_PRIVATE_RECORD" in operations
        return

    if requirement_id == "OB-72":
        decisions = load_json(DECISION_LEDGER)
        plan = load_fixture("property_plan_valid.json")
        assert decisions["final_method_selected"] is False
        assert plan["status"] == "UNSELECTED"
        assert plan["replication_facet_class"] == "UNSELECTED"
        assert plan["observation_data_class"] == "UNSELECTED"
        assert plan["intended_use_class"] == "UNSELECTED"
        assert plan["candidate_estimand_family_list"] == []
        assert contract["human_work_authorized"] is False
        assert contract["rectification_authorized"] is False
        return

    raise AssertionError(f"unknown requirement: {requirement_id}")
