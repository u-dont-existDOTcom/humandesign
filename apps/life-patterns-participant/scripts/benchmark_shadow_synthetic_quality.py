#!/usr/bin/env python3
"""Run privacy-safe synthetic quality checks for shadow clarification triage.

No participant source is read. Cases deliberately isolate one or zero eligible
routes so expected outcomes are interpretable. Output contains only case labels,
route IDs, counts, token counts, and timings.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

from participant.domain import bank, load_instrument, new_state
from participant.shadow_triage import privacy_safe_case_summary, run_shadow_triage

REPO_ROOT = Path(__file__).resolve().parents[3]
WORKER = Path(__file__).resolve().with_name("gpt_review_worker.py")


def load_worker_module():
    spec = importlib.util.spec_from_file_location("gpt_review_worker_synthetic", WORKER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def state_with_targets(instrument: dict, target_ids: set[str], turns: list[dict]) -> dict:
    state = new_state("synthetic-shadow-quality-v1", "gpt-5.6-sol", "xhigh")
    state["consent"] = True
    state["phase"] = "ready"
    state["collection_preferences"]["retrospective_questions_welcome"] = True
    state["addressed_routes"] = {
        route["id"]: {"source_turn_ids": ["synthetic-addressed"]}
        for route in bank(instrument)["questions"]
        if route["id"] not in target_ids
    }
    for index, raw in enumerate(turns, 1):
        state["turns"].append(
            {
                "turn_id": f"syn-{index:02d}",
                "sequence": index,
                "turn_source": "synthetic",
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


def cases(instrument: dict) -> list[tuple[str, dict, str | None]]:
    route = {item["id"]: item for item in bank(instrument)["questions"]}
    return [
        (
            "unresolved_m11",
            state_with_targets(
                instrument,
                {"M11"},
                [
                    {
                        "question_text": (
                            "When plans involve another person, what do you usually do first?"
                        ),
                        "answer_text": (
                            "I usually clarify what each person needs before deciding."
                        ),
                    }
                ],
            ),
            "M11",
        ),
        (
            "redundant_m11",
            state_with_targets(
                instrument,
                {"M11"},
                [
                    {
                        "question_text": (
                            "Suppose a friend says paying for all the ingredients feels "
                            "like too much. What would you say next?"
                        ),
                        "answer_text": (
                            "I would ask what budget works, suggest splitting the ingredient "
                            "cost, and adjust the plan so neither person carries too much."
                        ),
                    }
                ],
            ),
            None,
        ),
        (
            "dependent_prefer_exchange",
            state_with_targets(
                instrument,
                {"PREFER-EXCHANGE"},
                [
                    {
                        "canonical_question_id": "M11",
                        "question_text": route["M11"]["question"],
                        "answer_text": (
                            "I would ask what amount feels manageable and listen to their answer "
                            "before deciding what to do next."
                        ),
                    }
                ],
            ),
            "PREFER-EXCHANGE",
        ),
        (
            "context_missing_prefer_exchange",
            state_with_targets(
                instrument,
                {"PREFER-EXCHANGE"},
                [
                    {
                        "question_text": "What matters when choosing whether to negotiate?",
                        "answer_text": "It depends on the situation.",
                    }
                ],
            ),
            None,
        ),
        (
            "corrected_prefer_exchange",
            state_with_targets(
                instrument,
                {"PREFER-EXCHANGE"},
                [
                    {
                        "question_text": "In a meal-cost discussion, do you keep negotiating?",
                        "answer_text": (
                            "I usually keep negotiating until we find something that works."
                        ),
                    },
                    {
                        "question_text": "Correction",
                        "answer_text": (
                            "Actually, I usually make one counteroffer and then stop if they "
                            "still do not want it."
                        ),
                        "correction_of": "syn-01",
                    },
                ],
            ),
            None,
        ),
        (
            "unsupported_work_recovery_premise",
            state_with_targets(
                instrument,
                {"WORK-RECOVERY"},
                [
                    {
                        "canonical_question_id": "G15",
                        "question_text": route["G15"]["question"],
                        "answer_text": (
                            "At the end of that day I would usually still feel energetic, "
                            "not tired or depleted."
                        ),
                    }
                ],
            ),
            None,
        ),
        (
            "independent_batch_m05_m11",
            state_with_targets(
                instrument,
                {"M05", "M11"},
                [
                    {
                        "question_text": "What is one ordinary thing you notice when plans change?",
                        "answer_text": (
                            "I first notice whether the change affects what I need to do."
                        ),
                    }
                ],
            ),
            "BATCH:M05,M11",
        ),
    ]


def main() -> int:
    worker = load_worker_module()
    with tempfile.TemporaryDirectory(prefix="shadow-synthetic-authority-") as folder:
        instrument = load_instrument(worker.authority_copy(Path(folder)))
        provider = worker.CodexCliProvider()
        output = []
        for index, (label, state, expected_route) in enumerate(cases(instrument), 1):
            result = run_shadow_triage(
                state,
                instrument,
                provider,
                model="gpt-5.6-sol",
                effort="xhigh",
            )
            row = privacy_safe_case_summary(f"case-{index:04d}", state, result)
            row["label"] = label
            row["expected_selected_route_id"] = expected_route
            if isinstance(expected_route, str) and expected_route.startswith("BATCH:"):
                expected = set(expected_route.removeprefix("BATCH:").split(","))
                row["expectation_met"] = expected.issubset(set(row["admitted_route_ids"]))
            else:
                row["expectation_met"] = row["selected_route_id"] == expected_route
            output.append(row)
            print(json.dumps(row, separators=(",", ":")), flush=True)
        print(
            json.dumps(
                {
                    "schema": "life-patterns-shadow-synthetic-quality-v1",
                    "case_count": len(output),
                    "all_expectations_met": all(row["expectation_met"] for row in output),
                    "cases": output,
                },
                separators=(",", ":"),
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
