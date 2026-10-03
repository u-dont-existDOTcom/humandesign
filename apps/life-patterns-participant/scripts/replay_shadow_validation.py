#!/usr/bin/env python3
"""Replay frozen synthetic shadow-triage validation cases.

This development-only runner never touches Railway or live participant state.
It prints route-level/timing metadata only; source text remains in synthetic fixtures.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from pathlib import Path

from participant.domain import bank, load_instrument, new_state
from participant.shadow_triage import privacy_safe_case_summary, run_shadow_triage

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[3]
WORKER = HERE.with_name("gpt_review_worker.py")


def _worker():
    spec = importlib.util.spec_from_file_location("shadow_validation_worker", WORKER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _state(case: dict, instrument: dict, model: str, effort: str) -> dict:
    state = new_state("shadow-validation", model, effort)
    state.update(consent=True, phase="ready")
    state["collection_preferences"]["retrospective_questions_welcome"] = True
    target = set(case["route_ids"])
    state["addressed_routes"] = {
        route["id"]: {"source_turn_ids": ["synthetic-addressed"]}
        for route in bank(instrument)["questions"]
        if route["id"] not in target
    }
    for index, raw in enumerate(case["turns"], 1):
        state["turns"].append(
            {
                "turn_id": f"{case['case_id']}-turn-{index:02d}",
                "sequence": index,
                "turn_source": "synthetic_validation",
                "turn_role": "behavioral",
                "canonical_question_id": raw.get("canonical_question_id"),
                "question_wording_status": "synthetic",
                "question_text": raw["question_text"],
                "answer_text": raw["answer_text"],
                "correction_of": raw.get("correction_of"),
                "conditions": [],
                "corrections": [],
                "process_feedback": [],
                "antecedent_turn_ids": [],
            }
        )
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("expected", type=Path)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--effort", default="xhigh")
    args = parser.parse_args()

    case_doc = json.loads(args.cases.read_text(encoding="utf-8"))
    expected_doc = json.loads(args.expected.read_text(encoding="utf-8"))
    expected = {item["case_id"]: item for item in expected_doc["cases"]}
    worker = _worker()

    results = []
    with tempfile.TemporaryDirectory(prefix="shadow-validation-authority-") as folder:
        instrument = load_instrument(worker.authority_copy(Path(folder)))
        provider = worker.CodexCliProvider()
        for case in case_doc["cases"]:
            state = _state(case, instrument, args.model, args.effort)
            result = run_shadow_triage(
                state,
                instrument,
                provider,
                model=args.model,
                effort=args.effort,
            )
            row = privacy_safe_case_summary(case["case_id"], state, result)
            target = expected[case["case_id"]]
            actual_decision = (
                "review_ready"
                if row["shadow_outcome"] == "review_ready"
                else "clarification_needed"
                if row["shadow_outcome"] == "clarification_recommended"
                else "no_admitted_candidate"
            )
            route_ok = (
                target["route_id"] is None
                or target["route_id"] in row["admitted_route_ids"]
            )
            passed = actual_decision == target["decision"] and route_ok
            results.append(
                {
                    "case_id": case["case_id"],
                    "expected_decision": target["decision"],
                    "expected_route_id": target["route_id"],
                    "actual_decision": actual_decision,
                    "admitted_route_ids": row["admitted_route_ids"],
                    "passed": passed,
                    "semantic_duration_seconds": row["semantic_duration_seconds"],
                }
            )
            print(json.dumps(results[-1], separators=(",", ":")), flush=True)

    receipt = {
        "schema": "life-patterns-shadow-triage-validation-receipt-v1",
        "case_count": len(results),
        "passed_count": sum(item["passed"] for item in results),
        "all_passed": all(item["passed"] for item in results),
        "cases": results,
    }
    print("RECEIPT " + json.dumps(receipt, separators=(",", ":")))
    return 0 if receipt["all_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
