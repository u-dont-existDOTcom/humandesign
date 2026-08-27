#!/usr/bin/env python3
"""Audit how much the current frozen model can discriminate across a century cache."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from hdmatch.evaluation.discrimination import audit_partition, greedy_question_sequence
from hdmatch.runtime.century_cache import load_century_candidate_states, verify_century_cache
from hdmatch.runtime.symbolic_adapter import FrozenSymbolicModel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--mapping", default=Path("mappings/mapping_library_v1.json"), type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = verify_century_cache(args.cache)
    states = load_century_candidate_states(
        args.cache,
        timezone_name="UTC",
        expected_engine_fingerprint=manifest.engine_fingerprint,
    )
    model = FrozenSymbolicModel(args.mapping)

    signature_audit = audit_partition(
        states,
        lambda state: model.scoring_signature(state.chart_features),
    )

    answers_by_signature: dict[object, dict[str, str]] = {}
    answers_by_state: dict[str, dict[str, str]] = {}
    for state in states:
        signature = model.scoring_signature(state.chart_features)
        answers = answers_by_signature.get(signature)
        if answers is None:
            answers = {
                response.question_id: response.answer
                for response in model.oracle_responses(state.chart_features)
            }
            answers_by_signature[signature] = answers
        answers_by_state[state.state_id] = answers

    answer_fingerprint_audit = audit_partition(
        states,
        lambda state: tuple(sorted(answers_by_state[state.state_id].items())),
    )
    greedy_steps = greedy_question_sequence(states, answers_by_state)

    report = {
        "schema_version": "century-discrimination-audit-v1",
        "cache": {
            "cache_version": manifest.cache_version,
            "interval_count": manifest.interval_count,
            "utc_start": manifest.utc_start.isoformat(),
            "utc_end_exclusive": manifest.utc_end_exclusive.isoformat(),
            "engine_fingerprint": manifest.engine_fingerprint,
            "generation_commit": manifest.generation_commit,
        },
        "model": {
            "model_sha256": model.model_sha256,
            "mapping_sha256": model.mapping_sha256,
            "question_bank_sha256": model.question_bank_sha256,
            "model_visible_signature_fields": [
                "type",
                "strategy",
                "authority",
                "profile",
                "defined_centers",
            ],
        },
        "model_visible_signature_partition": asdict(signature_audit),
        "predicted_answer_fingerprint_partition": asdict(answer_fingerprint_audit),
        "greedy_noiseless_question_sequence": [asdict(step) for step in greedy_steps],
        "interpretation": {
            "exact_state_ceiling": (
                "Maximum interval-level top-1 recovery under a noiseless deterministic "
                "fingerprint and an interval-uniform prior, before human response noise."
            ),
            "residual_bits": (
                "Uncertainty about the exact cached interval that remains after observing "
                "the complete deterministic fingerprint."
            ),
            "greedy_sequence": (
                "Questions ordered by incremental interval-uniform entropy under perfect "
                "canonical answers. Zero incremental bits means the question cannot further "
                "split the remaining model-predicted fingerprints."
            ),
        },
    }

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
