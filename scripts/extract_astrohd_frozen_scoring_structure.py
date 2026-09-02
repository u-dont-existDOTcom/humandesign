#!/usr/bin/env python3
"""Generate descriptive-only AstroHD scoring-structure audit artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAPPING_LIBRARY_PATH = Path("mappings/mapping_library_v1.json")
QUESTION_BANK_PATH = Path("reference/core/question_bank_v1.json")
PRIOR_MAPPING_AUDIT_PATH = Path("reference/audits/astrohd_frozen_rule_prompt_mapping_v1.json")
SCORING_STRUCTURE_OUTPUT_PATH = Path("reference/audits/astrohd_frozen_scoring_structure_v1.json")
QUESTION_STATUS_OUTPUT_PATH = Path("reference/audits/astrohd_question_mapping_status_v1.json")


JsonObject = dict[str, Any]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json_object(path: Path) -> JsonObject:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return payload


def render_json(payload: JsonObject) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _core_weight(structural_class: str, core_weights: JsonObject) -> Any:
    if structural_class in core_weights:
        return core_weights[structural_class]
    plural_key = f"{structural_class}s"
    return core_weights.get(plural_key)


def _source_metadata(repository_root: Path) -> JsonObject:
    mapping_path = repository_root / MAPPING_LIBRARY_PATH
    question_path = repository_root / QUESTION_BANK_PATH
    return {
        "mapping_library": {
            "path": MAPPING_LIBRARY_PATH.as_posix(),
            "sha256": sha256_file(mapping_path),
        },
        "prior_mechanical_mapping_audit_path": PRIOR_MAPPING_AUDIT_PATH.as_posix(),
        "question_bank": {
            "path": QUESTION_BANK_PATH.as_posix(),
            "sha256": sha256_file(question_path),
        },
    }


def build_frozen_scoring_structure(
    mapping_library: JsonObject,
    question_bank: JsonObject,
    prior_mapping_audit: JsonObject,
    *,
    source: JsonObject,
) -> JsonObject:
    mappings = mapping_library["mappings"]
    questions = question_bank["questions"]
    answer_specs = mapping_library["answer_specs"]
    if not isinstance(mappings, list) or not isinstance(questions, list):
        raise ValueError("mapping and question collections must be lists")
    if not isinstance(answer_specs, list):
        raise ValueError("answer_specs must be a list")

    frozen = sorted(
        (mapping for mapping in mappings if mapping.get("status") == "frozen"),
        key=lambda mapping: mapping["mapping_id"],
    )
    question_by_id = {question["id"]: question for question in questions}
    answer_spec_by_question = {spec["question_id"]: spec for spec in answer_specs}
    frozen_prompt_ids = sorted(
        {question_id for mapping in frozen for question_id in mapping["question_ids"]}
    )

    if len(frozen) != 27 or len(frozen_prompt_ids) != 23:
        raise ValueError(
            "frozen mapping invariant mismatch: "
            f"{len(frozen)} rules / {len(frozen_prompt_ids)} prompts"
        )
    if any(question_id not in question_by_id for question_id in frozen_prompt_ids):
        raise ValueError("a frozen mapping references an unknown question")
    if any(question_id not in answer_spec_by_question for question_id in frozen_prompt_ids):
        raise ValueError("a frozen-mapped question lacks an answer specification")

    prior_rule_ids = {row["rule_identifier"] for row in prior_mapping_audit["rules"]}
    prior_prompt_ids = {row["prompt_identifier"] for row in prior_mapping_audit["prompts"]}
    frozen_rule_ids = {mapping["mapping_id"] for mapping in frozen}
    if frozen_rule_ids != prior_rule_ids or set(frozen_prompt_ids) != prior_prompt_ids:
        raise ValueError("frozen mapping sets do not match the prior mechanical audit")

    core_weights = mapping_library["constants"]["core_weights"]
    structural_classes: list[JsonObject] = []
    for structural_class in sorted({mapping["structural_class"] for mapping in frozen}):
        class_mappings = [
            mapping for mapping in frozen if mapping["structural_class"] == structural_class
        ]
        class_prompt_ids = sorted(
            {question_id for mapping in class_mappings for question_id in mapping["question_ids"]}
        )
        structural_classes.append(
            {
                "core_weight": _core_weight(structural_class, core_weights),
                "dependency_clusters": sorted(
                    {mapping["dependency_cluster"] for mapping in class_mappings}
                ),
                "observation_ids": sorted(
                    {mapping["observation_id"] for mapping in class_mappings}
                ),
                "prompt_count": len(class_prompt_ids),
                "prompt_ids": class_prompt_ids,
                "rule_count": len(class_mappings),
                "rule_ids": sorted(mapping["mapping_id"] for mapping in class_mappings),
                "structural_class": structural_class,
            }
        )

    frozen_rules: list[JsonObject] = []
    for mapping in frozen:
        contradiction = mapping.get("contradiction_rule")
        row: JsonObject = {
            "chart_feature_predicate": mapping["chart_feature_predicate"],
            "dependency_cluster": mapping["dependency_cluster"],
            "has_explicit_contradiction_rule": contradiction is not None,
            "mapping_directness": mapping["mapping_directness"],
            "mapping_directness_class": mapping["mapping_directness_class"],
            "mapping_id": mapping["mapping_id"],
            "observation_id": mapping["observation_id"],
            "predicted_response": {
                "canonical_answer_token": mapping["predicted_response"]["canonical_answer_token"],
                "support_answer_tokens": sorted(
                    mapping["predicted_response"]["support_answer_tokens"]
                ),
            },
            "question_ids": sorted(mapping["question_ids"]),
            "structural_class": mapping["structural_class"],
            "structural_salience": mapping["structural_salience"],
        }
        if contradiction is not None:
            row["contradiction_rule"] = {
                "answer_tokens": sorted(contradiction["answer_tokens"]),
                "severity": contradiction["severity"],
            }
        frozen_rules.append(row)

    mapped_prompts: list[JsonObject] = []
    for question_id in frozen_prompt_ids:
        question = question_by_id[question_id]
        prompt_mappings = [mapping for mapping in frozen if question_id in mapping["question_ids"]]
        answer_spec = answer_spec_by_question[question_id]
        declared_tokens = sorted(option["token"] for option in answer_spec["options"])
        support_tokens = sorted(
            {
                token
                for mapping in prompt_mappings
                for token in mapping["predicted_response"]["support_answer_tokens"]
            }
        )
        contradiction_tokens = sorted(
            {
                token
                for mapping in prompt_mappings
                for token in (mapping.get("contradiction_rule") or {}).get("answer_tokens", [])
            }
        )
        structural_class_ids = sorted({mapping["structural_class"] for mapping in prompt_mappings})
        dependency_cluster_ids = sorted(
            {mapping["dependency_cluster"] for mapping in prompt_mappings}
        )
        observation_ids = sorted({mapping["observation_id"] for mapping in prompt_mappings})
        rule_ids = sorted(mapping["mapping_id"] for mapping in prompt_mappings)
        mapped_prompts.append(
            {
                "behavioral_constructs": sorted(question["behavioral_constructs"]),
                "declared_answer_token_count": len(declared_tokens),
                "declared_answer_tokens": declared_tokens,
                "dependency_cluster_count": len(dependency_cluster_ids),
                "dependency_clusters": dependency_cluster_ids,
                "domain": question["domain"],
                "explicit_contradiction_token_count": len(contradiction_tokens),
                "explicit_contradiction_tokens": contradiction_tokens,
                "frozen_support_token_count": len(support_tokens),
                "frozen_support_tokens": support_tokens,
                "minimum_evidence": question["minimum_evidence"],
                "observation_count": len(observation_ids),
                "observation_ids": observation_ids,
                "phase": question["phase"],
                "question_id": question_id,
                "response_format": question["response_format"],
                "rule_count": len(rule_ids),
                "rule_ids": rule_ids,
                "structural_class_count": len(structural_class_ids),
                "structural_classes": structural_class_ids,
                "unmapped_answer_policy": answer_spec["unmapped_answer_policy"],
            }
        )

    dependency_groups: list[JsonObject] = []
    for cluster_id in sorted({mapping["dependency_cluster"] for mapping in frozen}):
        group = [mapping for mapping in frozen if mapping["dependency_cluster"] == cluster_id]
        rule_ids = sorted(mapping["mapping_id"] for mapping in group)
        prompt_ids = sorted(
            {question_id for mapping in group for question_id in mapping["question_ids"]}
        )
        observation_ids = sorted({mapping["observation_id"] for mapping in group})
        dependency_groups.append(
            {
                "cluster_id": cluster_id,
                "observation_count": len(observation_ids),
                "observation_ids": observation_ids,
                "prompt_count": len(prompt_ids),
                "prompt_ids": prompt_ids,
                "rule_count": len(rule_ids),
                "rule_ids": rule_ids,
            }
        )

    observation_groups: list[JsonObject] = []
    for observation_id in sorted({mapping["observation_id"] for mapping in frozen}):
        group = [mapping for mapping in frozen if mapping["observation_id"] == observation_id]
        rule_ids = sorted(mapping["mapping_id"] for mapping in group)
        prompt_ids = sorted(
            {question_id for mapping in group for question_id in mapping["question_ids"]}
        )
        observation_groups.append(
            {
                "observation_id": observation_id,
                "prompt_count": len(prompt_ids),
                "prompt_ids": prompt_ids,
                "rule_count": len(rule_ids),
                "rule_ids": rule_ids,
            }
        )

    return {
        "dependency_cluster_groups": dependency_groups,
        "frozen_rules": frozen_rules,
        "frozen_summary": {
            "distinct_frozen_mapped_prompt_count": len(frozen_prompt_ids),
            "distinct_frozen_rule_count": len(frozen),
        },
        "mapped_prompts": mapped_prompts,
        "observation_groups": observation_groups,
        "schema_version": "astrohd-frozen-scoring-structure-v1",
        "source": source,
        "status": "mechanical_audit_descriptive_only_no_runtime_effect",
        "structural_classes": structural_classes,
    }


def build_question_mapping_status(
    mapping_library: JsonObject,
    question_bank: JsonObject,
    *,
    source: JsonObject,
) -> JsonObject:
    mappings = mapping_library["mappings"]
    questions = question_bank["questions"]
    if not isinstance(mappings, list) or not isinstance(questions, list):
        raise ValueError("mapping and question collections must be lists")

    references_by_question: dict[str, list[JsonObject]] = defaultdict(list)
    question_ids = {question["id"] for question in questions}
    for mapping in mappings:
        for question_id in mapping["question_ids"]:
            if question_id not in question_ids:
                raise ValueError(f"mapping references unknown question: {question_id}")
            references_by_question[question_id].append(
                {
                    "dependency_cluster": mapping.get("dependency_cluster"),
                    "mapping_id": mapping["mapping_id"],
                    "observation_id": mapping.get("observation_id"),
                    "status": mapping["status"],
                    "structural_class": mapping.get("structural_class"),
                    "unresolved_reason": mapping.get("unresolved_reason"),
                }
            )

    rows: list[JsonObject] = []
    for question in sorted(questions, key=lambda row: row["id"]):
        references = sorted(
            references_by_question[question["id"]], key=lambda row: row["mapping_id"]
        )
        statuses = {reference["status"] for reference in references}
        rows.append(
            {
                "behavioral_constructs": sorted(question["behavioral_constructs"]),
                "domain": question["domain"],
                "has_empirical_only_mapping": "empirical_only" in statuses,
                "has_frozen_mapping": "frozen" in statuses,
                "has_unresolved_mapping": "unresolved" in statuses,
                "mapping_references": references,
                "minimum_evidence": question["minimum_evidence"],
                "phase": question["phase"],
                "question_id": question["id"],
            }
        )

    phase_counts = Counter(question["phase"] for question in questions)
    return {
        "interpretation": "descriptive_only_not_a_completeness_denominator",
        "questions": rows,
        "schema_version": "astrohd-question-mapping-status-v1",
        "source": source,
        "status": "mechanical_audit_descriptive_only_no_runtime_effect",
        "summary": {
            "question_count": len(rows),
            "question_count_by_phase": dict(sorted(phase_counts.items())),
            "question_count_with_empirical_only_mapping": sum(
                row["has_empirical_only_mapping"] for row in rows
            ),
            "question_count_with_frozen_mapping": sum(row["has_frozen_mapping"] for row in rows),
            "question_count_with_unresolved_mapping": sum(
                row["has_unresolved_mapping"] for row in rows
            ),
        },
    }


def generate_audits(
    repository_root: Path = ROOT,
) -> tuple[JsonObject, JsonObject]:
    mapping_library = load_json_object(repository_root / MAPPING_LIBRARY_PATH)
    question_bank = load_json_object(repository_root / QUESTION_BANK_PATH)
    prior_mapping_audit = load_json_object(repository_root / PRIOR_MAPPING_AUDIT_PATH)
    source = _source_metadata(repository_root)
    scoring_structure = build_frozen_scoring_structure(
        mapping_library,
        question_bank,
        prior_mapping_audit,
        source=source,
    )
    question_status = build_question_mapping_status(
        mapping_library,
        question_bank,
        source=source,
    )
    return scoring_structure, question_status


def write_audits(
    repository_root: Path = ROOT,
    *,
    scoring_output: Path | None = None,
    question_status_output: Path | None = None,
) -> tuple[Path, Path]:
    scoring_structure, question_status = generate_audits(repository_root)
    scoring_path = scoring_output or repository_root / SCORING_STRUCTURE_OUTPUT_PATH
    status_path = question_status_output or repository_root / QUESTION_STATUS_OUTPUT_PATH
    scoring_path.write_bytes(render_json(scoring_structure))
    status_path.write_bytes(render_json(question_status))
    return scoring_path, status_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    arguments = parser.parse_args()
    scoring_path, status_path = write_audits(arguments.repository_root.resolve())
    scoring_structure = load_json_object(scoring_path)
    question_status = load_json_object(status_path)
    print(
        json.dumps(
            {
                "distinct_frozen_mapped_prompt_count": scoring_structure["frozen_summary"][
                    "distinct_frozen_mapped_prompt_count"
                ],
                "distinct_frozen_rule_count": scoring_structure["frozen_summary"][
                    "distinct_frozen_rule_count"
                ],
                "question_count": question_status["summary"]["question_count"],
                "question_mapping_status_output": status_path.relative_to(
                    arguments.repository_root.resolve()
                ).as_posix(),
                "scoring_structure_output": scoring_path.relative_to(
                    arguments.repository_root.resolve()
                ).as_posix(),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
