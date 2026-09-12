from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from hdmatch.evaluation.resolved_development_stack import (
    CODING_MANUAL_REL,
    build_repository_resolved_development_stack,
    file_sha256,
)
from hdmatch.evaluation.resolved_development_stack_v2 import (
    CODING_MANUAL_V2_REL,
    RECURRENCE_POLICY_V2_REL,
    build_repository_resolved_development_stack_v2,
)

ROOT = Path(__file__).resolve().parents[2]
NOW = datetime(2026, 9, 8, 19, 0, tzinfo=UTC)
SOURCE_COMMIT = "f9b11a83706b55ae2539bd9403fa0aa02cdeaa95"


def test_v2_reuses_theory_blind_base_but_rebinds_manual_and_procedure() -> None:
    v1 = build_repository_resolved_development_stack(
        ROOT,
        source_commit=SOURCE_COMMIT,
        released_at_utc=NOW,
    )
    v2 = build_repository_resolved_development_stack_v2(
        ROOT,
        source_commit=SOURCE_COMMIT,
        released_at_utc=NOW,
    )

    assert v2.source == v1.source
    assert v2.compact == v1.compact
    assert v2.resolution == v1.resolution
    assert v2.resolved == v1.resolved
    assert v2.observable_ids == tuple(f"NBM-R{i:02d}" for i in range(1, 23))
    assert v2.coding_manual_sha256 == file_sha256(ROOT / CODING_MANUAL_V2_REL)
    assert v2.coding_manual_sha256 != file_sha256(ROOT / CODING_MANUAL_REL)
    assert v2.recurrence_policy_sha256 == file_sha256(ROOT / RECURRENCE_POLICY_V2_REL)
    assert v2.ontology.payload.coding_procedure_id == "life-patterns-development-coding-manual-v2"
    assert v2.ontology.payload.coding_procedure_sha256 == v2.coding_manual_sha256
    assert v2.procedure.payload.coding_manual_sha256 == v2.coding_manual_sha256
    assert v2.procedure.payload.reconciled_codebook_sha256 == v2.resolved.view_sha256
    assert v2.target_model_information_used_for_revision is False


def test_v2_stack_has_new_content_addresses_without_rewriting_v1() -> None:
    v1 = build_repository_resolved_development_stack(
        ROOT,
        source_commit=SOURCE_COMMIT,
        released_at_utc=NOW,
    )
    v2 = build_repository_resolved_development_stack_v2(
        ROOT,
        source_commit=SOURCE_COMMIT,
        released_at_utc=NOW,
    )

    assert v2.ontology.artifact_id != v1.ontology.artifact_id
    assert v2.ontology.ontology_sha256 != v1.ontology.ontology_sha256
    assert v2.procedure.procedure_id != v1.procedure.procedure_id
    assert v2.procedure.procedure_sha256 != v1.procedure.procedure_sha256
    assert sum(len(row.non_action_values) for row in v2.procedure.payload.observable_extensions) == 28
