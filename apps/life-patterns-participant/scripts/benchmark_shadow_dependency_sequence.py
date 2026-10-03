#!/usr/bin/env python3
"""Synthetic two-step check that dependent follow-ups are not batched prematurely."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from benchmark_shadow_synthetic_quality import load_worker_module
from participant.domain import bank, load_instrument, new_state
from participant.shadow_triage import privacy_safe_case_summary, run_shadow_triage


def base_state(instrument: dict) -> dict:
    state = new_state("synthetic-shadow-dependency-v1", "gpt-5.6-sol", "xhigh")
    state["consent"] = True
    state["phase"] = "ready"
    state["collection_preferences"]["retrospective_questions_welcome"] = True
    targets = {"M11", "PREFER-EXCHANGE"}
    state["addressed_routes"] = {
        route["id"]: {"source_turn_ids": ["synthetic-addressed"]}
        for route in bank(instrument)["questions"]
        if route["id"] not in targets
    }
    return state


def main() -> int:
    worker = load_worker_module()
    with tempfile.TemporaryDirectory(prefix="shadow-dependent-sequence-") as folder:
        instrument = load_instrument(worker.authority_copy(Path(folder) / "authority"))
        route = {item["id"]: item for item in bank(instrument)["questions"]}
        provider = worker.CodexCliProvider()
        state = base_state(instrument)

        first = run_shadow_triage(
            state,
            instrument,
            provider,
            model="gpt-5.6-sol",
            effort="xhigh",
        )
        first_summary = privacy_safe_case_summary("step-0001", state, first)

        state["turns"].append(
            {
                "turn_id": "syn-m11-answer",
                "sequence": 1,
                "turn_source": "synthetic",
                "turn_role": "behavioral",
                "canonical_question_id": "M11",
                "question_wording_status": "synthetic",
                "question_text": route["M11"]["question"],
                "answer_text": (
                    "I would ask what amount feels manageable and listen to their answer "
                    "before deciding what to do next."
                ),
                "correction_of": None,
                "conditions": [],
                "corrections": [],
                "process_feedback": [],
                "antecedent_turn_ids": [],
            }
        )
        state["addressed_routes"]["M11"] = {"source_turn_ids": ["syn-m11-answer"]}

        second = run_shadow_triage(
            state,
            instrument,
            provider,
            model="gpt-5.6-sol",
            effort="xhigh",
        )
        second_summary = privacy_safe_case_summary("step-0002", state, second)

        result = {
            "schema": "life-patterns-shadow-dependent-sequence-v1",
            "first_selected_route_id": first_summary["selected_route_id"],
            "first_eligible_route_count": first_summary["eligible_route_count"],
            "second_selected_route_id": second_summary["selected_route_id"],
            "second_eligible_route_count": second_summary["eligible_route_count"],
            "expectation_met": (
                first_summary["selected_route_id"] == "M11"
                and second_summary["selected_route_id"] == "PREFER-EXCHANGE"
            ),
            "first_semantic_duration_seconds": first_summary["semantic_duration_seconds"],
            "second_semantic_duration_seconds": second_summary["semantic_duration_seconds"],
        }
        print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
