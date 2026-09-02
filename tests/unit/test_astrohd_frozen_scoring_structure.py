from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).parents[2]
MAPPING_PATH = ROOT / "mappings/mapping_library_v1.json"
QUESTION_BANK_PATH = ROOT / "reference/core/question_bank_v1.json"
PRIOR_AUDIT_PATH = ROOT / "reference/audits/astrohd_frozen_rule_prompt_mapping_v1.json"
STRUCTURE_PATH = ROOT / "reference/audits/astrohd_frozen_scoring_structure_v1.json"
STATUS_PATH = ROOT / "reference/audits/astrohd_question_mapping_status_v1.json"

PROHIBITED_INTERPRETIVE_FIELDS = {
    "coverage_gap",
    "coverage_adequate",
    "coverage_inadequate",
    "needs_new_question",
    "recommended_question",
    "recommended_mapping",
    "discriminative_value",
    "reliability_judgment",
    "respondent_burden_judgment",
    "leakage_risk_judgment",
    "construct_missing",
    "questionnaire_complete",
    "questionnaire_incomplete",
    "required_question_count",
    "target_question_count",
    "recommended_count",
}


def _extractor() -> ModuleType:
    path = ROOT / "scripts/extract_astrohd_frozen_scoring_structure.py"
    spec = importlib.util.spec_from_file_location("extract_astrohd_frozen_scoring_structure", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for child in value.values() for key in _all_keys(child)}
    if isinstance(value, list):
        return {key for child in value for key in _all_keys(child)}
    return set()


def test_frozen_sets_exactly_match_prior_mechanical_audit() -> None:
    structure = _load(STRUCTURE_PATH)
    prior = _load(PRIOR_AUDIT_PATH)

    assert structure["frozen_summary"] == {
        "distinct_frozen_mapped_prompt_count": 23,
        "distinct_frozen_rule_count": 27,
    }
    assert {row["mapping_id"] for row in structure["frozen_rules"]} == {
        row["rule_identifier"] for row in prior["rules"]
    }
    assert {row["question_id"] for row in structure["mapped_prompts"]} == {
        row["prompt_identifier"] for row in prior["prompts"]
    }


def test_sources_and_frozen_rows_reproduce_current_source_bytes() -> None:
    structure = _load(STRUCTURE_PATH)
    library = _load(MAPPING_PATH)
    bank = _load(QUESTION_BANK_PATH)
    source = structure["source"]

    assert source["mapping_library"] == {
        "path": "mappings/mapping_library_v1.json",
        "sha256": _sha256(MAPPING_PATH),
    }
    assert source["question_bank"] == {
        "path": "reference/core/question_bank_v1.json",
        "sha256": _sha256(QUESTION_BANK_PATH),
    }
    assert source["prior_mechanical_mapping_audit_path"] == (
        "reference/audits/astrohd_frozen_rule_prompt_mapping_v1.json"
    )

    frozen_by_id = {
        mapping["mapping_id"]: mapping
        for mapping in library["mappings"]
        if mapping["status"] == "frozen"
    }
    assert len(structure["frozen_rules"]) == len(frozen_by_id) == 27
    for row in structure["frozen_rules"]:
        source_mapping = frozen_by_id[row["mapping_id"]]
        assert row["question_ids"] == sorted(source_mapping["question_ids"])
        assert row["structural_class"] == source_mapping["structural_class"]
        assert row["dependency_cluster"] == source_mapping["dependency_cluster"]
        assert row["observation_id"] == source_mapping["observation_id"]
        assert row["mapping_directness"] == source_mapping["mapping_directness"]
        assert row["mapping_directness_class"] == source_mapping["mapping_directness_class"]
        assert row["structural_salience"] == source_mapping["structural_salience"]
        assert row["chart_feature_predicate"] == source_mapping["chart_feature_predicate"]
        assert row["predicted_response"] == {
            "canonical_answer_token": source_mapping["predicted_response"][
                "canonical_answer_token"
            ],
            "support_answer_tokens": sorted(
                source_mapping["predicted_response"]["support_answer_tokens"]
            ),
        }
        contradiction = source_mapping.get("contradiction_rule")
        assert row["has_explicit_contradiction_rule"] is (contradiction is not None)
        if contradiction is None:
            assert "contradiction_rule" not in row
        else:
            assert row["contradiction_rule"] == {
                "answer_tokens": sorted(contradiction["answer_tokens"]),
                "severity": contradiction["severity"],
            }

    question_by_id = {question["id"]: question for question in bank["questions"]}
    answer_spec_by_id = {
        answer_spec["question_id"]: answer_spec for answer_spec in library["answer_specs"]
    }
    for row in structure["mapped_prompts"]:
        question = question_by_id[row["question_id"]]
        source_mappings = [
            mapping
            for mapping in frozen_by_id.values()
            if row["question_id"] in mapping["question_ids"]
        ]
        declared_tokens = sorted(
            option["token"] for option in answer_spec_by_id[row["question_id"]]["options"]
        )
        support_tokens = sorted(
            {
                token
                for mapping in source_mappings
                for token in mapping["predicted_response"]["support_answer_tokens"]
            }
        )
        contradiction_tokens = sorted(
            {
                token
                for mapping in source_mappings
                for token in (mapping.get("contradiction_rule") or {}).get("answer_tokens", [])
            }
        )
        assert row["phase"] == question["phase"]
        assert row["domain"] == question["domain"]
        assert row["response_format"] == question["response_format"]
        assert row["minimum_evidence"] == question["minimum_evidence"]
        assert row["behavioral_constructs"] == sorted(question["behavioral_constructs"])
        assert row["rule_ids"] == sorted(mapping["mapping_id"] for mapping in source_mappings)
        assert row["structural_classes"] == sorted(
            {mapping["structural_class"] for mapping in source_mappings}
        )
        assert row["dependency_clusters"] == sorted(
            {mapping["dependency_cluster"] for mapping in source_mappings}
        )
        assert row["observation_ids"] == sorted(
            {mapping["observation_id"] for mapping in source_mappings}
        )
        assert row["declared_answer_tokens"] == declared_tokens
        assert row["declared_answer_token_count"] == len(declared_tokens)
        assert row["frozen_support_tokens"] == support_tokens
        assert row["frozen_support_token_count"] == len(support_tokens)
        assert row["explicit_contradiction_tokens"] == contradiction_tokens
        assert row["explicit_contradiction_token_count"] == len(contradiction_tokens)
        assert (
            row["unmapped_answer_policy"]
            == answer_spec_by_id[row["question_id"]]["unmapped_answer_policy"]
        )

    class_rows = {row["structural_class"]: row for row in structure["structural_classes"]}
    assert set(class_rows) == {mapping["structural_class"] for mapping in frozen_by_id.values()}
    for structural_class, row in class_rows.items():
        source_mappings = [
            mapping
            for mapping in frozen_by_id.values()
            if mapping["structural_class"] == structural_class
        ]
        assert row["rule_ids"] == sorted(mapping["mapping_id"] for mapping in source_mappings)
        assert row["rule_count"] == len(source_mappings)


def test_dependency_and_observation_groups_are_exactly_reconstructible() -> None:
    structure = _load(STRUCTURE_PATH)
    library = _load(MAPPING_PATH)
    frozen = [mapping for mapping in library["mappings"] if mapping["status"] == "frozen"]

    for row in structure["dependency_cluster_groups"]:
        source_rows = [
            mapping for mapping in frozen if mapping["dependency_cluster"] == row["cluster_id"]
        ]
        expected_rules = sorted(mapping["mapping_id"] for mapping in source_rows)
        expected_prompts = sorted(
            {question_id for mapping in source_rows for question_id in mapping["question_ids"]}
        )
        expected_observations = sorted({mapping["observation_id"] for mapping in source_rows})
        assert row["rule_ids"] == expected_rules
        assert row["prompt_ids"] == expected_prompts
        assert row["observation_ids"] == expected_observations
        assert row["rule_count"] == len(expected_rules)
        assert row["prompt_count"] == len(expected_prompts)
        assert row["observation_count"] == len(expected_observations)

    for row in structure["observation_groups"]:
        source_rows = [
            mapping for mapping in frozen if mapping["observation_id"] == row["observation_id"]
        ]
        expected_rules = sorted(mapping["mapping_id"] for mapping in source_rows)
        expected_prompts = sorted(
            {question_id for mapping in source_rows for question_id in mapping["question_ids"]}
        )
        assert row["rule_ids"] == expected_rules
        assert row["prompt_ids"] == expected_prompts
        assert row["rule_count"] == len(expected_rules)
        assert row["prompt_count"] == len(expected_prompts)


def test_question_status_inventory_is_complete_and_status_mechanical() -> None:
    status = _load(STATUS_PATH)
    library = _load(MAPPING_PATH)
    bank = _load(QUESTION_BANK_PATH)
    rows = status["questions"]

    assert status["interpretation"] == "descriptive_only_not_a_completeness_denominator"
    assert len(rows) == len(bank["questions"]) == 81
    assert len({row["question_id"] for row in rows}) == len(rows)
    assert {row["question_id"] for row in rows} == {
        question["id"] for question in bank["questions"]
    }

    mapping_by_id = {mapping["mapping_id"]: mapping for mapping in library["mappings"]}
    for row in rows:
        expected = sorted(
            (
                mapping
                for mapping in library["mappings"]
                if row["question_id"] in mapping["question_ids"]
            ),
            key=lambda mapping: mapping["mapping_id"],
        )
        assert [reference["mapping_id"] for reference in row["mapping_references"]] == [
            mapping["mapping_id"] for mapping in expected
        ]
        statuses = {mapping["status"] for mapping in expected}
        assert row["has_frozen_mapping"] is ("frozen" in statuses)
        assert row["has_empirical_only_mapping"] is ("empirical_only" in statuses)
        assert row["has_unresolved_mapping"] is ("unresolved" in statuses)
        for reference in row["mapping_references"]:
            source_mapping = mapping_by_id[reference["mapping_id"]]
            assert row["question_id"] in source_mapping["question_ids"]
            assert reference == {
                "dependency_cluster": source_mapping.get("dependency_cluster"),
                "mapping_id": source_mapping["mapping_id"],
                "observation_id": source_mapping.get("observation_id"),
                "status": source_mapping["status"],
                "structural_class": source_mapping.get("structural_class"),
                "unresolved_reason": source_mapping.get("unresolved_reason"),
            }


def test_output_ordering_is_deterministic_and_contains_no_interpretive_fields() -> None:
    structure = _load(STRUCTURE_PATH)
    status = _load(STATUS_PATH)

    assert [row["mapping_id"] for row in structure["frozen_rules"]] == sorted(
        row["mapping_id"] for row in structure["frozen_rules"]
    )
    assert [row["question_id"] for row in structure["mapped_prompts"]] == sorted(
        row["question_id"] for row in structure["mapped_prompts"]
    )
    assert [row["cluster_id"] for row in structure["dependency_cluster_groups"]] == sorted(
        row["cluster_id"] for row in structure["dependency_cluster_groups"]
    )
    assert [row["observation_id"] for row in structure["observation_groups"]] == sorted(
        row["observation_id"] for row in structure["observation_groups"]
    )
    assert [row["question_id"] for row in status["questions"]] == sorted(
        row["question_id"] for row in status["questions"]
    )
    assert PROHIBITED_INTERPRETIVE_FIELDS.isdisjoint(_all_keys(structure))
    assert PROHIBITED_INTERPRETIVE_FIELDS.isdisjoint(_all_keys(status))


def test_regeneration_is_byte_identical(tmp_path: Path) -> None:
    extractor = _extractor()
    scoring_output = tmp_path / STRUCTURE_PATH.name
    status_output = tmp_path / STATUS_PATH.name

    extractor.write_audits(
        ROOT,
        scoring_output=scoring_output,
        question_status_output=status_output,
    )

    assert scoring_output.read_bytes() == STRUCTURE_PATH.read_bytes()
    assert status_output.read_bytes() == STATUS_PATH.read_bytes()
