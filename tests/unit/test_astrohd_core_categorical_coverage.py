from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

from hdmatch.chart.bodygraph import Authority, HDType

ROOT = Path(__file__).parents[2]
COVERAGE_PATH = ROOT / "reference/audits/astrohd_core_categorical_coverage_v1.json"
MATRIX_PATH = ROOT / "reference/research/astrohd_future_core_coverage_candidate_matrix_v1.json"
MAPPING_PATH = ROOT / "mappings/mapping_library_v1.json"
QUESTION_BANK_PATH = ROOT / "reference/core/question_bank_v1.json"

EXPECTED_MAPPING_SHA256 = "3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200"
EXPECTED_QUESTION_BANK_SHA256 = "31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820"
EXPECTED_TYPE_RULE_IDS = {
    "manifestor": [],
    "generator": ["MAP-TYPE-GENERATOR-S02", "MAP-TYPE-GENERATOR-S05"],
    "manifesting_generator": ["MAP-TYPE-GENERATOR-S02", "MAP-TYPE-GENERATOR-S05"],
    "projector": ["MAP-TYPE-PROJECTOR-S03", "MAP-TYPE-PROJECTOR-S04"],
    "reflector": [],
}
EXPECTED_AUTHORITY_RULE_IDS = {
    "emotional_solar_plexus": ["MAP-AUTH-EMOTIONAL-D01", "MAP-AUTH-EMOTIONAL-D03"],
    "sacral": ["MAP-AUTH-SACRAL-D01"],
    "splenic": ["MAP-AUTH-SPLENIC-D01", "MAP-AUTH-SPLENIC-D02"],
    "ego_manifested": [],
    "ego_projected": [],
    "self_projected": [],
    "mental_environmental": [],
    "lunar": [],
}


def _extractor() -> ModuleType:
    path = ROOT / "scripts/extract_astrohd_core_categorical_coverage.py"
    spec = importlib.util.spec_from_file_location("extract_astrohd_core_categorical_coverage", path)
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


def test_engine_type_values_and_current_frozen_paths_match() -> None:
    coverage = _load(COVERAGE_PATH)
    rows = coverage["type_coverage"]

    assert [row["engine_type_value"] for row in rows] == [value.value for value in HDType]
    assert {
        row["engine_type_value"]: row["matching_rule_ids"] for row in rows
    } == EXPECTED_TYPE_RULE_IDS
    for row in rows:
        assert row["matching_rule_count"] == len(row["matching_rule_ids"])
        assert row["has_frozen_type_strategy_path"] is bool(row["matching_rule_ids"])


def test_engine_authority_values_and_current_frozen_paths_match() -> None:
    coverage = _load(COVERAGE_PATH)
    rows = coverage["authority_coverage"]

    assert [row["engine_authority_value"] for row in rows] == [value.value for value in Authority]
    assert {
        row["engine_authority_value"]: row["matching_rule_ids"] for row in rows
    } == EXPECTED_AUTHORITY_RULE_IDS
    for row in rows:
        assert row["matching_rule_count"] == len(row["matching_rule_ids"])
        assert row["has_frozen_authority_path"] is bool(row["matching_rule_ids"])


def test_all_profile_lines_have_expected_frozen_rule_counts() -> None:
    coverage = _load(COVERAGE_PATH)
    rows = coverage["profile_line_coverage"]

    assert {row["profile_line"]: row["matching_rule_count"] for row in rows} == {
        1: 1,
        2: 2,
        3: 2,
        4: 1,
        5: 1,
        6: 2,
    }
    assert all(row["has_frozen_profile_path"] for row in rows)


def test_d01_declared_tokens_without_frozen_disposition_match_exactly() -> None:
    coverage = _load(COVERAGE_PATH)
    disposition = coverage["d01_declared_token_disposition"]

    assert disposition["question_id"] == "D01"
    assert set(disposition["declared_tokens_with_neither_frozen_support_nor_contradiction"]) == {
        "clarity_from_being_in_the_right_place_or_with_the_right_listener",
        "hearing_your_own_words_reveal_the_answer",
        "no_stable_pattern",
    }
    for row in disposition["tokens"]:
        assert row["used_by_any_frozen_support_rule"] is bool(row["support_rule_ids"])
        assert row["used_by_any_frozen_contradiction_rule"] is bool(row["contradiction_rule_ids"])


def test_dependency_summary_reproduces_descriptive_counts() -> None:
    coverage = _load(COVERAGE_PATH)

    assert coverage["dependency_summary"] == {
        "dependency_cluster_count": 7,
        "distinct_frozen_mapped_prompt_count": 23,
        "distinct_frozen_rule_count": 27,
        "interpretation": "descriptive_only_not_independent_sample_counts",
        "observation_group_count": 20,
    }


def test_candidate_matrix_contains_exact_prescribed_targets_and_no_wording() -> None:
    matrix = _load(MATRIX_PATH)
    rows = matrix["targets"]

    assert matrix["status"] == ("draft_research_candidates_not_owner_policy_not_scoring_authority")
    assert [row["target_id"] for row in rows] == [
        "type_strategy.manifestor",
        "type_strategy.reflector",
        "authority.self_projected",
        "authority.mental_environmental",
        "authority.ego_manifested",
        "authority.ego_projected",
        "authority.lunar",
    ]
    assert all(row["current_frozen_path"] == "absent" for row in rows)
    for row in rows:
        assert row["runtime_authorized"] is False
        assert row["mapping_authorized"] is False
        assert row["question_change_authorized"] is False
        assert row["owner_policy"] is False
    assert not {key for key in _all_keys(matrix) if "prompt" in key or "wording" in key}


def test_source_hashes_remain_frozen_and_no_question_count_target_exists() -> None:
    coverage = _load(COVERAGE_PATH)
    matrix = _load(MATRIX_PATH)

    assert _sha256(MAPPING_PATH) == EXPECTED_MAPPING_SHA256
    assert _sha256(QUESTION_BANK_PATH) == EXPECTED_QUESTION_BANK_SHA256
    assert coverage["source"]["mapping_library"]["sha256"] == EXPECTED_MAPPING_SHA256
    assert coverage["source"]["question_bank"]["sha256"] == EXPECTED_QUESTION_BANK_SHA256
    forbidden_count_fields = {
        "required_question_count",
        "target_question_count",
        "recommended_question_count",
        "recommended_count",
    }
    assert forbidden_count_fields.isdisjoint(_all_keys(coverage))
    assert forbidden_count_fields.isdisjoint(_all_keys(matrix))


def test_both_generated_json_artifacts_regenerate_byte_identically(tmp_path: Path) -> None:
    extractor = _extractor()
    coverage_output = tmp_path / COVERAGE_PATH.name
    matrix_output = tmp_path / MATRIX_PATH.name

    extractor.write_artifacts(
        ROOT,
        coverage_output=coverage_output,
        candidate_matrix_output=matrix_output,
    )

    assert coverage_output.read_bytes() == COVERAGE_PATH.read_bytes()
    assert matrix_output.read_bytes() == MATRIX_PATH.read_bytes()
