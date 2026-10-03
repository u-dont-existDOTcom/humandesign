#!/usr/bin/env python3
"""Run the fast clarification triage in shadow mode on a local source record.

The script never mutates Railway state and prints no participant text. It is a
research/development benchmark; the legacy review remains authoritative.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from pathlib import Path

from participant.domain import load_instrument, new_state
from participant.gap_triage import (
    GAP_ADMISSION_PROMPT,
    GAP_TRIAGE_PROMPT,
    GapAdmission,
    GapTriage,
    admitted_candidates,
    make_admission_context,
    make_triage_context,
    validate_admission,
    validate_triage,
)
from participant.store import canonical

HERE = Path(__file__).resolve()
WORKER = HERE.with_name("gpt_review_worker.py")


def load_worker_module():
    spec = importlib.util.spec_from_file_location("gpt_review_worker_shadow", WORKER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def source_state(record: dict) -> dict:
    state = new_state("gap-shadow", "openai-gpt-56-sol", "xhigh")
    state.update(session_id="shadow", revision=0, consent=True, phase="ready")
    state["collection_preferences"]["retrospective_questions_welcome"] = True
    for index, raw in enumerate(record.get("turns") or [], 1):
        if not isinstance(raw, dict):
            continue
        state["turns"].append(
            {
                "turn_id": str(raw.get("turn_id") or f"shadow-{index:04d}"),
                "sequence": index,
                "turn_source": "shadow-source",
                "turn_role": raw.get("turn_role", "behavioral"),
                "canonical_question_id": raw.get("canonical_question_id"),
                "question_wording_status": raw.get(
                    "question_wording_status", "received_edited_or_unverified"
                ),
                "question_text": raw.get("question_text"),
                "answer_text": raw.get("answer_text"),
                "correction_of": raw.get("correction_of"),
                "conditions": raw.get("conditions") or [],
                "corrections": raw.get("corrections") or [],
                "process_feedback": raw.get("process_feedback") or [],
            }
        )
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_json", type=Path)
    parser.add_argument("--model", default="openai-gpt-56-sol")
    parser.add_argument("--effort", default="xhigh")
    args = parser.parse_args()

    record = json.loads(args.source_json.read_text(encoding="utf-8"))
    state = source_state(record)
    worker = load_worker_module()

    with tempfile.TemporaryDirectory(prefix="gap-triage-authority-") as folder:
        instrument = load_instrument(worker.authority_copy(Path(folder)))
        provider = worker.CodexCliProvider()
        triage_context = make_triage_context(state, instrument)
        triage, triage_call = provider.call(
            GAP_TRIAGE_PROMPT,
            triage_context,
            GapTriage,
            args.model,
            args.effort,
        )
        validate_triage(triage, state, instrument)

        admission_context = make_admission_context(state, instrument, triage)
        admission, admission_call = provider.call(
            GAP_ADMISSION_PROMPT,
            admission_context,
            GapAdmission,
            args.model,
            args.effort,
        )
        validate_admission(admission, triage, state, instrument)
        kept = admitted_candidates(triage, admission)

    print(
        json.dumps(
            {
                "schema": "life-patterns-gap-triage-shadow-result-v1",
                "source_turn_count": len(state["turns"]),
                "triage_context_chars": len(canonical(triage_context)),
                "admission_context_chars": len(canonical(admission_context)),
                "triage_decision": triage.decision,
                "proposed_route_ids": [item.route_id for item in triage.candidates],
                "approved_route_ids": [item.route_id for item in kept],
                "missed_material_route_id": (
                    admission.missed_material_gap.route_id
                    if admission.missed_material_gap is not None
                    else None
                ),
                "review_ready_supported": admission.review_ready_supported,
                "calls": [
                    {
                        key: call.get(key)
                        for key in (
                            "stage",
                            "duration_seconds",
                            "prompt_tokens",
                            "completion_tokens",
                            "reasoning_effort",
                            "requested_model",
                            "provider",
                        )
                    }
                    for call in (triage_call, admission_call)
                ],
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
