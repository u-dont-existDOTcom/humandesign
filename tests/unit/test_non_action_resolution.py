from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.non_action_resolution import (
    NonActionAmbiguityResolutionPayload,
    build_ambiguity_resolution_artifact,
    build_resolved_codebook_view_v2,
    compact_classification_errors,
    load_compact_non_action_classification,
    parse_ambiguity_resolution_jsonl,
)
from hdmatch.evaluation.reconciled_codebook_source import parse_reconciled_codebook_file
from hdmatch.experiments.canonical import sha256_json

CODEBOOK_PATH = Path(
    "state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md"
)
COMPACT_PATH = Path("state/LIFE-PATTERNS-NON-ACTION-CLASSIFICATION-COMPACT-v1-2026-09-04.json")
RESOLUTION_PATH = Path(
    "state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-NORMALIZED-v1-2026-09-04.jsonl"
)
RAW_RESOLUTION_PATH = Path(
    "state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-RAW-v1-2026-09-04.jsonl.txt"
)
PROMPT_PATH = Path(
    "state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-PROMPT-v1-2026-09-04.txt"
)
NOW = datetime(2026, 9, 4, 14, 48, tzinfo=UTC)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact():
    source = parse_reconciled_codebook_file(CODEBOOK_PATH)
    compact = load_compact_non_action_classification(COMPACT_PATH)
    decisions = parse_ambiguity_resolution_jsonl(RESOLUTION_PATH.read_bytes())
    payload = NonActionAmbiguityResolutionPayload(
        reconciled_source_artifact_id=source.artifact_id,
        reconciled_source_sha256=source.artifact_sha256,
        compact_classification_sha256=sha256_json(compact),
        resolution_prompt_sha256=_sha(PROMPT_PATH),
        raw_output_sha256=_sha(RAW_RESOLUTION_PATH),
        normalized_output_sha256=_sha(RESOLUTION_PATH),
        author_kind="ai",
        author_or_model_identity="THEORY-BLIND-CLEAN-CHAT",
        author_or_model_version="USER-SUPPLIED-OUTPUT; MODEL VERSION NOT RECORDED",
        decisions=decisions,
        created_at_utc=NOW,
    )
    return source, compact, build_ambiguity_resolution_artifact(
        payload,
        source=source,
        compact=compact,
    )


def test_compact_first_pass_matches_exact_frozen_source() -> None:
    source = parse_reconciled_codebook_file(CODEBOOK_PATH)
    compact = load_compact_non_action_classification(COMPACT_PATH)
    assert compact_classification_errors(compact, source=source) == ()
    assert compact.counts == {
        "non_action": 24,
        "not_non_action": 174,
        "ambiguous": 8,
        "total": 206,
    }


def test_real_theory_blind_resolution_covers_exactly_eight_ambiguities() -> None:
    source, compact, artifact = _artifact()
    assert len(artifact.payload.decisions) == 8
    assert {row.original_subcode_id for row in artifact.payload.decisions} == set(
        compact.ambiguous_ids
    )
    assert all(row.resolution != "exclude" for row in artifact.payload.decisions)
    assert sum(row.resolution == "split" for row in artifact.payload.decisions) == 2
    assert sum(row.resolution == "clarify_without_split" for row in artifact.payload.decisions) == 6

    resolved = build_resolved_codebook_view_v2(
        source=source,
        compact=compact,
        resolution=artifact,
    )
    assert resolved.payload.original_subcode_count == 206
    assert resolved.payload.resolved_subcode_count == 208
    assert resolved.payload.non_action_count == 28
    assert resolved.payload.not_non_action_count == 180

    by_id = {
        row.subcode_id: row
        for observable in resolved.payload.observables
        for row in observable.subcodes
    }
    assert "R07-a" not in by_id
    assert by_id["R07-a1"].classification == "not_non_action"
    assert by_id["R07-a2"].classification == "non_action"
    assert "R16-d" not in by_id
    assert by_id["R16-d1"].classification == "not_non_action"
    assert by_id["R16-d2"].classification == "non_action"
    assert by_id["R11-I6"].classification == "not_non_action"
    assert by_id["R15-h"].classification == "not_non_action"
    assert by_id["R17-g"].classification == "non_action"
    assert by_id["R19-e"].classification == "not_non_action"
    assert by_id["R20-g"].classification == "not_non_action"
    assert by_id["R21-i"].classification == "non_action"


def test_resolution_rejects_missing_blind_decision() -> None:
    source = parse_reconciled_codebook_file(CODEBOOK_PATH)
    compact = load_compact_non_action_classification(COMPACT_PATH)
    decisions = parse_ambiguity_resolution_jsonl(RESOLUTION_PATH.read_bytes())[:-1]
    payload = NonActionAmbiguityResolutionPayload(
        reconciled_source_artifact_id=source.artifact_id,
        reconciled_source_sha256=source.artifact_sha256,
        compact_classification_sha256=sha256_json(compact),
        resolution_prompt_sha256=_sha(PROMPT_PATH),
        raw_output_sha256=_sha(RAW_RESOLUTION_PATH),
        normalized_output_sha256=_sha(RESOLUTION_PATH),
        author_kind="ai",
        author_or_model_identity="SYNTHETIC-MISSING-DECISION-TEST",
        decisions=decisions,
        created_at_utc=NOW,
    )
    with pytest.raises(ValueError, match="exactly the originally ambiguous"):
        build_ambiguity_resolution_artifact(payload, source=source, compact=compact)
