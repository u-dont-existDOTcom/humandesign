from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.resolved_development_stack import (
    CODING_MANUAL_REL,
    RESOLUTION_ARTIFACT_RECONSTRUCTION_AT_UTC,
    build_repository_resolved_development_stack,
    file_sha256,
)


NOW = datetime(2026, 9, 6, 21, 0, tzinfo=UTC)


def test_real_repository_stack_binds_exact_resolved_measurement_chain() -> None:
    stack = build_repository_resolved_development_stack(
        Path("."),
        source_commit="abcdef0123456789",
        released_at_utc=NOW,
    )
    assert stack.resolved.payload.original_subcode_count == 206
    assert stack.resolved.payload.resolved_subcode_count == 208
    assert stack.resolved.payload.non_action_count == 28
    assert stack.resolved.payload.not_non_action_count == 180
    assert stack.observable_ids == tuple(f"NBM-R{index:02d}" for index in range(1, 23))
    assert stack.procedure.payload.reconciled_codebook_sha256 == stack.resolved.view_sha256
    assert stack.procedure.payload.coding_manual_sha256 == stack.coding_manual_sha256
    assert stack.ontology.payload.coding_procedure_sha256 == stack.coding_manual_sha256
    assert stack.coding_manual_sha256 == file_sha256(CODING_MANUAL_REL)
    assert sum(
        len(row.non_action_values) for row in stack.procedure.payload.observable_extensions
    ) == 28


def test_reconstruction_is_deterministic_for_same_release_inputs() -> None:
    kwargs = dict(
        repo_root=Path("."),
        source_commit="abcdef0123456789",
        released_at_utc=NOW,
    )
    first = build_repository_resolved_development_stack(**kwargs)
    second = build_repository_resolved_development_stack(**kwargs)
    assert first.source == second.source
    assert first.resolution == second.resolution
    assert first.resolved == second.resolved
    assert first.ontology == second.ontology
    assert first.procedure == second.procedure


def test_reconstruction_timestamp_is_explicitly_not_current_run_time() -> None:
    stack = build_repository_resolved_development_stack(
        Path("."),
        source_commit="abcdef0123456789",
        released_at_utc=NOW,
    )
    assert stack.resolution.payload.created_at_utc == RESOLUTION_ARTIFACT_RECONSTRUCTION_AT_UTC
    assert stack.ontology.payload.released_at_utc == NOW
    assert stack.procedure.payload.created_at_utc == NOW


def test_stack_rejects_unpinned_short_source_ref() -> None:
    with pytest.raises(ValueError, match="source commit"):
        build_repository_resolved_development_stack(
            Path("."),
            source_commit="main",
            released_at_utc=NOW,
        )
