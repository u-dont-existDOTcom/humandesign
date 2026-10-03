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
# Blind Claude Opus and Sonnet adjudicators disagreed on whether this generic
# coordination answer leaves enough information gain to justify M11. Do not
# tune the shadow model to an assistant-authored expected label.
DISPUTED_EXPECTATION_LABELS = {"unresolved_m11"}


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
        (
            "mixed_m05_and_prefer_exchange",
            state_with_targets(
                instrument,
                {"M05", "PREFER-EXCHANGE"},
                [
                    {
                        "canonical_question_id": "M11",
                        "question_text": route["M11"]["question"],
                        "answer_text": (
                            "I would ask what amount feels manageable and listen to their "
                            "answer before deciding what to do next."
                        ),
                    },
                    {
                        "question_text": "How do you react to ordinary schedule changes?",
                        "answer_text": (
                            "I usually check what changed before deciding whether it matters."
                        ),
                    },
                ],
            ),
            "BATCH:M05,PREFER-EXCHANGE",
        ),
        (
            "mixed_review_ready",
            state_with_targets(
                instrument,
                {"M05", "M11", "WORK-RECOVERY"},
                [
                    {
                        "question_text": (
                            "On a route I know well, if the driver takes a road that route "
                            "normally never uses, what would I make of it?"
                        ),
                        "answer_text": (
                            "I would think there is probably a detour or traffic issue and "
                            "look for more information before assuming danger."
                        ),
                    },
                    {
                        "question_text": (
                            "If a friend says paying for all meal ingredients is too much, "
                            "what would I say?"
                        ),
                        "answer_text": (
                            "I would ask their budget and suggest a split or cheaper meal so "
                            "the plan works for both of us."
                        ),
                    },
                    {
                        "canonical_question_id": "G15",
                        "question_text": route["G15"]["question"],
                        "answer_text": (
                            "I would usually still feel energetic, not tired or depleted."
                        ),
                    },
                ],
            ),
            None,
        ),
        (
            "explicit_unknown_prefer_exchange",
            state_with_targets(
                instrument,
                {"M11", "PREFER-EXCHANGE"},
                [
                    {
                        "canonical_question_id": "M11",
                        "question_text": route["M11"]["question"],
                        "answer_text": (
                            "I would ask what budget works and try another arrangement. "
                            "Whether I keep negotiating after that depends on the situation, "
                            "but I cannot say yet what makes me keep going versus stop."
                        ),
                    }
                ],
            ),
            None,
        ),
        (
            "mixed_correction_leaves_m05",
            state_with_targets(
                instrument,
                {"M05", "M11"},
                [
                    {
                        "question_text": (
                            "If a friend says the ingredient cost is too much, what would I do?"
                        ),
                        "answer_text": "I would probably insist that the original split is fair.",
                    },
                    {
                        "question_text": "Correction",
                        "answer_text": (
                            "Actually I would ask what they can afford and renegotiate the "
                            "split rather than insist."
                        ),
                        "correction_of": "syn-01",
                    },
                    {
                        "question_text": "What do I notice when a plan changes?",
                        "answer_text": "Mostly whether I need to adjust my timing.",
                    },
                ],
            ),
            "M05",
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
                expectation_met = expected.issubset(set(row["admitted_route_ids"]))
            else:
                expectation_met = row["selected_route_id"] == expected_route
            row["expectation_status"] = (
                "disputed"
                if label in DISPUTED_EXPECTATION_LABELS
                else "met"
                if expectation_met
                else "failed"
            )
            output.append(row)
            print(json.dumps(row, separators=(",", ":")), flush=True)
        print(
            json.dumps(
                {
                    "schema": "life-patterns-shadow-synthetic-quality-v1",
                    "case_count": len(output),
                    "disputed_expectation_count": sum(
                        row["expectation_status"] == "disputed" for row in output
                    ),
                    "all_non_disputed_expectations_met": all(
                        row["expectation_status"] in {"met", "disputed"}
                        for row in output
                    ),
                    "cases": output,
                },
                separators=(",", ":"),
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
