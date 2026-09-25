#!/usr/bin/env python3
"""Extract frozen rule-to-prompt relationships without interpreting coverage."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from hdmatch.model.mapping_library import load_mapping_library

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DISTINCT_RULE_COUNT = 27
EXPECTED_DISTINCT_MAPPED_PROMPT_COUNT = 23


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mapping-library",
        type=Path,
        default=Path("mappings/mapping_library_v1.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reference/audits/astrohd_frozen_rule_prompt_mapping_v1.json"),
    )
    return parser.parse_args()


def build_extract(mapping_library_path: Path) -> dict[str, Any]:
    library = load_mapping_library(mapping_library_path)
    rules = [
        {
            "rule_identifier": mapping.mapping_id,
            "mapped_prompt_count": len(set(mapping.question_ids)),
            "mapped_prompt_identifiers": sorted(set(mapping.question_ids)),
        }
        for mapping in sorted(library.frozen_mappings, key=lambda item: item.mapping_id)
    ]
    prompt_to_rules: dict[str, list[str]] = defaultdict(list)
    for rule in rules:
        for prompt_identifier in rule["mapped_prompt_identifiers"]:
            prompt_to_rules[prompt_identifier].append(rule["rule_identifier"])
    prompts = [
        {
            "prompt_identifier": prompt_identifier,
            "mapped_rule_count": len(rule_identifiers),
            "mapped_rule_identifiers": sorted(rule_identifiers),
        }
        for prompt_identifier, rule_identifiers in sorted(prompt_to_rules.items())
    ]
    distinct_rule_count = len({rule["rule_identifier"] for rule in rules})
    distinct_mapped_prompt_count = len(prompt_to_rules)
    return {
        "schema_version": "astrohd-frozen-rule-prompt-mapping-extract-v1",
        "source": {
            "path": _display_path(mapping_library_path),
            "sha256": hashlib.sha256(mapping_library_path.read_bytes()).hexdigest(),
            "status_filter": "frozen",
        },
        "distinct_rule_count": distinct_rule_count,
        "distinct_mapped_prompt_count": distinct_mapped_prompt_count,
        "rules": rules,
        "prompts": prompts,
        "prompts_shared_by_multiple_rules": [
            prompt for prompt in prompts if prompt["mapped_rule_count"] > 1
        ],
        "rules_mapped_to_multiple_prompts": [
            rule for rule in rules if rule["mapped_prompt_count"] > 1
        ],
        "acceptance": {
            "expected_distinct_rule_count": EXPECTED_DISTINCT_RULE_COUNT,
            "expected_distinct_mapped_prompt_count": (EXPECTED_DISTINCT_MAPPED_PROMPT_COUNT),
            "counts_match": (
                distinct_rule_count == EXPECTED_DISTINCT_RULE_COUNT
                and distinct_mapped_prompt_count == EXPECTED_DISTINCT_MAPPED_PROMPT_COUNT
            ),
        },
    }


def write_extract(report: dict[str, Any], output_path: Path) -> None:
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def main() -> None:
    args = parse_args()
    report = build_extract(args.mapping_library)
    write_extract(report, args.output)
    print(
        json.dumps(
            {
                "source": report["source"]["path"],
                "distinct_rule_count": report["distinct_rule_count"],
                "distinct_mapped_prompt_count": report["distinct_mapped_prompt_count"],
                "counts_match": report["acceptance"]["counts_match"],
            },
            sort_keys=True,
        )
    )
    if not report["acceptance"]["counts_match"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
