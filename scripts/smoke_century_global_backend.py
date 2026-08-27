#!/usr/bin/env python3
"""Smoke the real participant backend against a verified century cache.

This deliberately uses a neutral synthetic UTC birth fixture and *zero behavioral
answers*.  It therefore exercises cache verification/loading, the frozen mapping
library, pre-answer candidate-universe binding, and global discrimination without
using or exposing a real person's answer key.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.participant.century_backend import CenturyCapableParticipantBackend
from hdmatch.participant.models import RankScope, ResolvedBirth


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris", required=True)
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--question-bank", required=True)
    parser.add_argument("--century-cache", required=True)
    parser.add_argument("--code-commit", default="smoke")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    backend = CenturyCapableParticipantBackend(
        ephemeris_path=args.ephemeris,
        mapping_path=args.mapping,
        question_bank_path=args.question_bank,
        century_cache_dir=args.century_cache,
        code_commit=args.code_commit,
    )
    initialized = time.perf_counter()

    birth_utc = datetime(1990, 1, 1, 12, 0, tzinfo=UTC)
    birth = ResolvedBirth(
        supplied_local=datetime(1990, 1, 1, 12, 0),
        birthplace="UTC synthetic smoke fixture",
        iana_timezone="UTC",
        fold=0,
        birth_utc=birth_utc,
        utc_offset_seconds=0,
        tzdb_version="synthetic-smoke",
        pre_standard_time_uncertain=False,
    )
    freeze = backend.build_prediction_freeze(
        session_id="HD-00000000000000000000000000000000",
        birth=birth,
        ranking_scope=RankScope.CENTURY_GLOBAL,
        created_at_utc=datetime.now(UTC),
    )
    frozen = time.perf_counter()

    if freeze.ranking_scope is not RankScope.CENTURY_GLOBAL:
        raise RuntimeError("global smoke freeze did not preserve century_global scope")
    if freeze.candidate_universe_state_count < 250_000:
        raise RuntimeError(
            "global smoke loaded implausibly small candidate universe: "
            f"{freeze.candidate_universe_state_count}"
        )
    if not (
        freeze.candidate_universe_utc_start <= birth_utc < freeze.candidate_universe_utc_end_exclusive
    ):
        raise RuntimeError("synthetic birth is outside frozen century universe")
    if len(freeze.candidate_universe_sha256) != 64:
        raise RuntimeError("candidate universe digest is not SHA-256 shaped")

    loaded_states = backend._century_universe_cache.get("UTC")
    if loaded_states is None:
        raise RuntimeError("century universe was not cached after successful freeze")
    model_visible_signature_count = len(
        {
            backend.model.scoring_signature(state.chart_features)
            for state in loaded_states
        }
    )

    diagnostics = backend.discrimination(freeze=freeze, responses=())
    discriminated = time.perf_counter()
    if diagnostics.candidate_state_count != freeze.candidate_universe_state_count:
        raise RuntimeError(
            "discrimination candidate count changed after freeze: "
            f"{diagnostics.candidate_state_count} != {freeze.candidate_universe_state_count}"
        )
    if diagnostics.top_state_tie_count != freeze.candidate_universe_state_count:
        raise RuntimeError(
            "zero behavioral evidence must leave every candidate state evidence-tied: "
            f"{diagnostics.top_state_tie_count} != {freeze.candidate_universe_state_count}"
        )

    report = {
        "schema_version": "century-global-backend-smoke-v2",
        "fixture": "synthetic-utc-1990-01-01T12:00:00Z",
        "ranking_scope": freeze.ranking_scope.value,
        "candidate_state_count": freeze.candidate_universe_state_count,
        "model_visible_signature_count": model_visible_signature_count,
        "candidate_universe_sha256": freeze.candidate_universe_sha256,
        "candidate_universe_utc_start": freeze.candidate_universe_utc_start.isoformat(),
        "candidate_universe_utc_end_exclusive": (
            freeze.candidate_universe_utc_end_exclusive.isoformat()
        ),
        "candidate_universe_timezone": freeze.candidate_universe_timezone,
        "frozen_prediction_dimension_count": len(freeze.dimensions),
        "top_state_tie_count_zero_answers": diagnostics.top_state_tie_count,
        "top_margin_rubric_bits_zero_answers": diagnostics.top_margin_rubric_bits,
        "timing_seconds": {
            "backend_init": initialized - started,
            "freeze_including_cache_verify_load_and_digest": frozen - initialized,
            "zero_answer_discrimination": discriminated - frozen,
            "total": discriminated - started,
        },
    }
    rendered = json.dumps(report, sort_keys=True, indent=2)
    print(rendered, flush=True)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
