"""Privacy-safe structural check for completed Life Patterns guided context responses.

Never print or serialize participant free text or distinctive behavior entries.
This is a response-preservation check, not a personality or natal scorer.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

TARGET_ROUTES = (
    "TF1-G01", "TF1-G02", "TF1-G16", "TF1-G23",
    "TF1-M05", "TF1-G20", "TF1-M01", "TF1-M03",
)
ADDED_FIELDS = frozenset({"context_rule", "recent_case", "no_stable_default", "context_skipped"})


def review(previous: dict[str, Any], updated: dict[str, Any]) -> dict[str, Any]:
    if previous.get("schema") != "local_life_patterns_v3_pilot_unsubmitted" or updated.get("schema") != previous["schema"]:
        raise ValueError("Not matching V3 local pilot schema")
    old = previous.get("answers")
    new = updated.get("answers")
    if not isinstance(old, dict) or not isinstance(new, dict) or len(old) != 25 or set(old) != set(new):
        raise ValueError("The original 25 question routes must be preserved")
    if previous.get("unique_behaviors") != updated.get("unique_behaviors"):
        raise ValueError("Distinctive behaviors changed; a separate revision must be tracked")
    if set(TARGET_ROUTES) - set(old):
        raise ValueError("One or more guided target routes were missing")
    for route, old_answer in old.items():
        candidate = new[route]
        if not isinstance(old_answer, dict) or not isinstance(candidate, dict):
            raise ValueError("Question answers must be objects")
        original = {k: value for k, value in candidate.items() if k not in ADDED_FIELDS}
        if original != old_answer:
            raise ValueError("An original question answer or other existing field changed")
        unexpected = set(candidate) - set(old_answer)
        if route not in TARGET_ROUTES and unexpected:
            raise ValueError("Non-target question gained unexpected fields")
        for key in ("context_rule", "recent_case"):
            if key in candidate and not isinstance(candidate[key], str):
                raise ValueError("Context must be verbatim string or absent")
        for key in ("no_stable_default", "context_skipped"):
            if key in candidate and not isinstance(candidate[key], bool):
                raise ValueError("Context switches must be Boolean or absent")
    completed = [
        route for route in TARGET_ROUTES if (
            bool(new[route].get("context_rule", "").strip()) or
            bool(new[route].get("recent_case", "").strip()) or
            new[route].get("no_stable_default") is True or
            new[route].get("context_skipped") is True
        )
    ]
    # Aggregate-only: no user quotes, item-level choices or user-identifying URLs.
    return {
        "schema": "life-patterns-eight-context-completion-aggregate-v1",
        "source_mode": "SAME_PERSON_DEVELOPMENT_NOT_INDEPENDENT_VALIDATION",
        "question_routes_preserved": len(old),
        "target_count": len(TARGET_ROUTES),
        "completed_target_count": len(completed),
        "missing_route_ids": [route for route in TARGET_ROUTES if route not in completed],
        "conditional_rule_count": sum(bool(new[r].get("context_rule", "").strip()) for r in TARGET_ROUTES),
        "concrete_example_count": sum(bool(new[r].get("recent_case", "").strip()) for r in TARGET_ROUTES),
        "no_stable_default_count": sum(new[r].get("no_stable_default") is True for r in TARGET_ROUTES),
        "explicit_skip_count": sum(new[r].get("context_skipped") is True for r in TARGET_ROUTES),
        "original_free_text_and_choices_unchanged": True,
        "unique_behaviors_unchanged": True,
        "selected_count_distribution": dict(sorted(Counter(str(len(q["selected"])) for q in new.values()).items())),
        "participant_count": 1,
        "birth_chart_predictions_tested": 0,
        "private_content_in_output": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous", type=Path, required=True)
    parser.add_argument("--updated", type=Path, required=True)
    parser.add_argument("--aggregate-output", type=Path)
    args = parser.parse_args()
    old = json.loads(args.previous.read_text(encoding="utf-8"))
    new = json.loads(args.updated.read_text(encoding="utf-8"))
    result = review(old, new)
    serialized = json.dumps(result, indent=2) + "\n"
    if args.aggregate_output:
        args.aggregate_output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
