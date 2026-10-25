#!/usr/bin/env python3
"""Generate the mechanical AstroHD core-categorical coverage audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from hdmatch.chart.bodygraph import Authority, HDType
from hdmatch.model.mapping_library import ChartPredicate

ROOT = Path(__file__).resolve().parents[1]
BODYGRAPH_PATH = Path("src/hdmatch/chart/bodygraph.py")
MAPPING_LIBRARY_PATH = Path("mappings/mapping_library_v1.json")
QUESTION_BANK_PATH = Path("reference/core/question_bank_v1.json")
SCORING_STRUCTURE_PATH = Path("reference/audits/astrohd_frozen_scoring_structure_v1.json")
COVERAGE_OUTPUT_PATH = Path("reference/audits/astrohd_core_categorical_coverage_v1.json")
CANDIDATE_MATRIX_OUTPUT_PATH = Path(
    "reference/research/astrohd_future_core_coverage_candidate_matrix_v1.json"
)

JsonObject = dict[str, Any]

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
EXPECTED_PROFILE_RULE_COUNTS = {1: 1, 2: 2, 3: 2, 4: 1, 5: 1, 6: 2}
EXPECTED_D01_NEITHER_TOKENS = {
    "clarity_from_being_in_the_right_place_or_with_the_right_listener",
    "hearing_your_own_words_reveal_the_answer",
    "no_stable_pattern",
}


def load_json_object(path: Path) -> JsonObject:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return payload


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_json(payload: JsonObject) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _source_metadata(repository_root: Path) -> JsonObject:
    return {
        "bodygraph": {
            "path": BODYGRAPH_PATH.as_posix(),
            "sha256": sha256_file(repository_root / BODYGRAPH_PATH),
        },
        "mapping_library": {
            "path": MAPPING_LIBRARY_PATH.as_posix(),
            "sha256": sha256_file(repository_root / MAPPING_LIBRARY_PATH),
        },
        "question_bank": {
            "path": QUESTION_BANK_PATH.as_posix(),
            "sha256": sha256_file(repository_root / QUESTION_BANK_PATH),
        },
        "scoring_structure_audit": {
            "path": SCORING_STRUCTURE_PATH.as_posix(),
            "sha256": sha256_file(repository_root / SCORING_STRUCTURE_PATH),
        },
    }


def _matching_mappings(
    frozen_mappings: list[JsonObject],
    *,
    structural_class: str,
    chart: JsonObject,
) -> list[JsonObject]:
    return sorted(
        (
            mapping
            for mapping in frozen_mappings
            if mapping["structural_class"] == structural_class
            and ChartPredicate.model_validate(mapping["chart_feature_predicate"]).matches(chart)
        ),
        key=lambda mapping: mapping["mapping_id"],
    )


def _coverage_details(mappings: list[JsonObject]) -> JsonObject:
    return {
        "dependency_clusters": sorted({mapping["dependency_cluster"] for mapping in mappings}),
        "matching_rule_count": len(mappings),
        "matching_rule_ids": [mapping["mapping_id"] for mapping in mappings],
        "observation_ids": sorted({mapping["observation_id"] for mapping in mappings}),
        "prompt_ids": sorted(
            {question_id for mapping in mappings for question_id in mapping["question_ids"]}
        ),
    }


def build_core_categorical_coverage(
    mapping_library: JsonObject,
    scoring_structure: JsonObject,
    *,
    source: JsonObject,
) -> JsonObject:
    frozen_mappings = sorted(
        (mapping for mapping in mapping_library["mappings"] if mapping["status"] == "frozen"),
        key=lambda mapping: mapping["mapping_id"],
    )

    type_coverage: list[JsonObject] = []
    for hd_type in HDType:
        mappings = _matching_mappings(
            frozen_mappings,
            structural_class="type_strategy",
            chart={"type": hd_type.value},
        )
        details = _coverage_details(mappings)
        details.update(
            {
                "engine_type_value": hd_type.value,
                "has_frozen_type_strategy_path": bool(mappings),
            }
        )
        type_coverage.append(details)

    authority_coverage: list[JsonObject] = []
    for authority in Authority:
        mappings = _matching_mappings(
            frozen_mappings,
            structural_class="authority",
            chart={"authority": authority.value},
        )
        details = _coverage_details(mappings)
        details.update(
            {
                "engine_authority_value": authority.value,
                "has_frozen_authority_path": bool(mappings),
            }
        )
        authority_coverage.append(details)

    profile_line_coverage: list[JsonObject] = []
    for line in range(1, 7):
        mappings = _matching_mappings(
            frozen_mappings,
            structural_class="profile",
            chart={"profile": str(line)},
        )
        details = _coverage_details(mappings)
        details.update(
            {
                "has_frozen_profile_path": bool(mappings),
                "profile_line": line,
            }
        )
        profile_line_coverage.append(details)

    answer_spec = next(
        spec for spec in mapping_library["answer_specs"] if spec["question_id"] == "D01"
    )
    d01_mappings = [mapping for mapping in frozen_mappings if "D01" in mapping["question_ids"]]
    token_disposition: list[JsonObject] = []
    for option in sorted(answer_spec["options"], key=lambda row: row["token"]):
        token = option["token"]
        support_rule_ids = sorted(
            mapping["mapping_id"]
            for mapping in d01_mappings
            if token in mapping["predicted_response"]["support_answer_tokens"]
        )
        contradiction_rule_ids = sorted(
            mapping["mapping_id"]
            for mapping in d01_mappings
            if token in (mapping.get("contradiction_rule") or {}).get("answer_tokens", [])
        )
        token_disposition.append(
            {
                "answer_token": token,
                "contradiction_rule_ids": contradiction_rule_ids,
                "support_rule_ids": support_rule_ids,
                "used_by_any_frozen_contradiction_rule": bool(contradiction_rule_ids),
                "used_by_any_frozen_support_rule": bool(support_rule_ids),
            }
        )
    neither_tokens = sorted(
        row["answer_token"]
        for row in token_disposition
        if not row["used_by_any_frozen_support_rule"]
        and not row["used_by_any_frozen_contradiction_rule"]
    )

    observed_type_rules = {
        row["engine_type_value"]: row["matching_rule_ids"] for row in type_coverage
    }
    observed_authority_rules = {
        row["engine_authority_value"]: row["matching_rule_ids"] for row in authority_coverage
    }
    observed_profile_counts = {
        row["profile_line"]: row["matching_rule_count"] for row in profile_line_coverage
    }
    if observed_type_rules != EXPECTED_TYPE_RULE_IDS:
        raise ValueError(
            f"type coverage mismatch: expected {EXPECTED_TYPE_RULE_IDS}, "
            f"observed {observed_type_rules}"
        )
    if observed_authority_rules != EXPECTED_AUTHORITY_RULE_IDS:
        raise ValueError(
            f"authority coverage mismatch: expected {EXPECTED_AUTHORITY_RULE_IDS}, "
            f"observed {observed_authority_rules}"
        )
    if observed_profile_counts != EXPECTED_PROFILE_RULE_COUNTS:
        raise ValueError(
            f"profile coverage mismatch: expected {EXPECTED_PROFILE_RULE_COUNTS}, "
            f"observed {observed_profile_counts}"
        )
    if set(neither_tokens) != EXPECTED_D01_NEITHER_TOKENS:
        raise ValueError(
            f"D01 token mismatch: expected {sorted(EXPECTED_D01_NEITHER_TOKENS)}, "
            f"observed {neither_tokens}"
        )

    dependency_summary = {
        "dependency_cluster_count": len(scoring_structure["dependency_cluster_groups"]),
        "distinct_frozen_mapped_prompt_count": scoring_structure["frozen_summary"][
            "distinct_frozen_mapped_prompt_count"
        ],
        "distinct_frozen_rule_count": scoring_structure["frozen_summary"][
            "distinct_frozen_rule_count"
        ],
        "interpretation": "descriptive_only_not_independent_sample_counts",
        "observation_group_count": len(scoring_structure["observation_groups"]),
    }
    expected_dependency_summary = {
        "dependency_cluster_count": 7,
        "distinct_frozen_mapped_prompt_count": 23,
        "distinct_frozen_rule_count": 27,
        "interpretation": "descriptive_only_not_independent_sample_counts",
        "observation_group_count": 20,
    }
    if dependency_summary != expected_dependency_summary:
        raise ValueError(
            f"dependency summary mismatch: expected {expected_dependency_summary}, "
            f"observed {dependency_summary}"
        )

    return {
        "authority_coverage": authority_coverage,
        "d01_declared_token_disposition": {
            "declared_tokens_with_neither_frozen_support_nor_contradiction": neither_tokens,
            "question_id": "D01",
            "tokens": token_disposition,
        },
        "dependency_summary": dependency_summary,
        "profile_line_coverage": profile_line_coverage,
        "schema_version": "astrohd-core-categorical-coverage-v1",
        "source": source,
        "status": "mechanical_audit_descriptive_only_no_runtime_effect",
        "type_coverage": type_coverage,
    }


def build_future_core_candidate_matrix() -> JsonObject:
    common_authorizations = {
        "mapping_authorized": False,
        "owner_policy": False,
        "question_change_authorized": False,
        "runtime_authorized": False,
    }
    targets: list[JsonObject] = [
        {
            "current_frozen_path": "absent",
            "disposition": (
                "existing_probe_is_partial_because_it_measures_initiation_outcome_"
                "not_informing_before_action"
            ),
            "existing_candidate_question_ids": ["S01"],
            "future_action_class": "extra_high_pro_design_required",
            "target_id": "type_strategy.manifestor",
        },
        {
            "current_frozen_path": "absent",
            "disposition": "no_direct_existing_full_lunar_cycle_strategy_probe_identified",
            "existing_direct_full_lunar_cycle_probe_ids": [],
            "future_action_class": "extra_high_pro_design_required",
            "target_id": "type_strategy.reflector",
        },
        {
            "current_frozen_path": "absent",
            "disposition": (
                "strong_reuse_candidate_but_self_heard_speech_is_not_unique_to_this_authority"
            ),
            "existing_candidate_question_ids": ["D01", "D04"],
            "future_action_class": "source_backed_mapping_design_required",
            "relevant_existing_d01_token": "hearing_your_own_words_reveal_the_answer",
            "target_id": "authority.self_projected",
        },
        {
            "current_frozen_path": "absent",
            "disposition": "strong_existing_probe_reuse_candidate",
            "existing_candidate_question_ids": ["D01", "D05"],
            "future_action_class": "source_backed_mapping_design_required",
            "relevant_existing_d01_token": (
                "clarity_from_being_in_the_right_place_or_with_the_right_listener"
            ),
            "target_id": "authority.mental_environmental",
        },
        {
            "current_frozen_path": "absent",
            "disposition": "existing_material_is_partial_and_overlaps_other_verbal_authorities",
            "existing_candidate_question_ids": ["D04", "D06"],
            "future_action_class": "extra_high_pro_discrimination_design_required",
            "target_id": "authority.ego_manifested",
        },
        {
            "current_frozen_path": "absent",
            "disposition": (
                "existing_material_is_partial_and_does_not_by_itself_establish_an_authority_mapping"
            ),
            "existing_candidate_question_ids": ["D06", "S04"],
            "future_action_class": "extra_high_pro_discrimination_design_required",
            "target_id": "authority.ego_projected",
        },
        {
            "current_frozen_path": "absent",
            "dependency_note": (
                "future_lunar_authority_and_reflector_strategy_evidence_must_not_be_double_counted"
            ),
            "disposition": "no_direct_existing_full_lunar_cycle_authority_probe_identified",
            "existing_direct_full_lunar_cycle_probe_ids": [],
            "future_action_class": "extra_high_pro_design_required",
            "target_id": "authority.lunar",
        },
    ]
    for target in targets:
        target.update(common_authorizations)
    return {
        "schema_version": "astrohd-future-core-coverage-candidate-matrix-v1",
        "status": "draft_research_candidates_not_owner_policy_not_scoring_authority",
        "targets": targets,
    }


def generate_artifacts(repository_root: Path = ROOT) -> tuple[JsonObject, JsonObject]:
    mapping_library = load_json_object(repository_root / MAPPING_LIBRARY_PATH)
    scoring_structure = load_json_object(repository_root / SCORING_STRUCTURE_PATH)
    source = _source_metadata(repository_root)
    coverage = build_core_categorical_coverage(
        mapping_library,
        scoring_structure,
        source=source,
    )
    candidate_matrix = build_future_core_candidate_matrix()
    return coverage, candidate_matrix


def write_artifacts(
    repository_root: Path = ROOT,
    *,
    coverage_output: Path | None = None,
    candidate_matrix_output: Path | None = None,
) -> tuple[Path, Path]:
    coverage, candidate_matrix = generate_artifacts(repository_root)
    coverage_path = coverage_output or repository_root / COVERAGE_OUTPUT_PATH
    matrix_path = candidate_matrix_output or repository_root / CANDIDATE_MATRIX_OUTPUT_PATH
    coverage_path.write_bytes(render_json(coverage))
    matrix_path.write_bytes(render_json(candidate_matrix))
    return coverage_path, matrix_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    arguments = parser.parse_args()
    repository_root = arguments.repository_root.resolve()
    coverage_path, matrix_path = write_artifacts(repository_root)
    coverage = load_json_object(coverage_path)
    print(
        json.dumps(
            {
                "authority_values": len(coverage["authority_coverage"]),
                "candidate_targets": len(load_json_object(matrix_path)["targets"]),
                "coverage_output": coverage_path.relative_to(repository_root).as_posix(),
                "profile_lines": len(coverage["profile_line_coverage"]),
                "type_values": len(coverage["type_coverage"]),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
