"""Build the recurrence-corrected Life Patterns development measurement stack.

This is additive. The historical v1 development stack remains reproducible and unchanged.
The v2 stack reuses the same theory-blind reconciled behavioral source/non-action resolution,
but binds a new development coding manual and the explicit recurrence-evidence policy before any
human or automated labels exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .neutral_measurement import OntologyReleaseArtifact
from .non_action_resolution import (
    CompactNonActionClassification,
    NonActionAmbiguityResolutionArtifact,
    ResolvedCodebookViewArtifactV2,
)
from .reconciled_codebook_source import ReconciledCodebookSourceArtifact
from .reconciled_ontology import build_development_ontology_from_resolved_view
from .resolved_coding_procedure import build_structured_procedure_from_resolved_view
from .resolved_development_stack import (
    ResolvedDevelopmentStack,
    build_repository_resolved_development_stack,
    file_sha256,
)
from .structured_annotation_v2 import StructuredCodingProcedureArtifactV2

CODING_MANUAL_V2_REL = Path("state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md")
RECURRENCE_POLICY_V2_REL = Path(
    "docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md"
)


@dataclass(frozen=True)
class ResolvedDevelopmentStackV2:
    source: ReconciledCodebookSourceArtifact
    compact: CompactNonActionClassification
    resolution: NonActionAmbiguityResolutionArtifact
    resolved: ResolvedCodebookViewArtifactV2
    ontology: OntologyReleaseArtifact
    procedure: StructuredCodingProcedureArtifactV2
    coding_manual_sha256: str
    recurrence_policy_sha256: str
    aggregation_policy_sha256: str
    theory_policy_sha256: str
    observable_ids: tuple[str, ...]
    supersedes_development_stack_version: str = "v1"
    target_model_information_used_for_revision: bool = False


def build_repository_resolved_development_stack_v2(
    repo_root: str | Path,
    *,
    source_commit: str,
    released_at_utc: datetime,
) -> ResolvedDevelopmentStackV2:
    """Rebind the frozen theory-blind base to recurrence-corrected development semantics."""

    root = Path(repo_root)
    base: ResolvedDevelopmentStack = build_repository_resolved_development_stack(
        root,
        source_commit=source_commit,
        released_at_utc=released_at_utc,
    )
    manual_path = root / CODING_MANUAL_V2_REL
    recurrence_path = root / RECURRENCE_POLICY_V2_REL
    missing = [
        str(path.relative_to(root))
        for path in (manual_path, recurrence_path)
        if not path.is_file()
    ]
    if missing:
        raise ValueError("recurrence-corrected development stack is missing: " + ", ".join(missing))

    coding_manual_sha256 = file_sha256(manual_path)
    recurrence_policy_sha256 = file_sha256(recurrence_path)
    ontology = build_development_ontology_from_resolved_view(
        base.source,
        base.resolved,
        ontology_id="life-patterns-theory-blind-resolved-development-v3",
        ontology_version="v3.0.0",
        coding_manual_id="life-patterns-development-coding-manual-v2",
        coding_manual_sha256=coding_manual_sha256,
        aggregation_policy_id="life-patterns-neutral-measurement-bridge",
        aggregation_policy_sha256=base.aggregation_policy_sha256,
        theory_contamination_policy_id="life-patterns-theory-blind-content-authority-policy",
        theory_contamination_policy_sha256=base.theory_policy_sha256,
        source_commit=source_commit.strip(),
        released_at_utc=released_at_utc,
    )
    procedure = build_structured_procedure_from_resolved_view(
        source=base.source,
        resolved=base.resolved,
        ontology=ontology,
        coding_manual_sha256=coding_manual_sha256,
        created_at_utc=released_at_utc,
    )
    observable_ids = tuple(row.observable_id for row in ontology.payload.observables)
    expected = tuple(f"NBM-R{index:02d}" for index in range(1, 23))
    if observable_ids != expected:
        raise ValueError("v2 development stack does not contain exact NBM-R01..NBM-R22 order")
    if procedure.payload.reconciled_codebook_sha256 != base.resolved.view_sha256:
        raise ValueError("v2 procedure does not bind frozen resolved codebook view")
    if procedure.payload.coding_manual_sha256 != coding_manual_sha256:
        raise ValueError("v2 procedure does not bind recurrence-corrected coding manual")
    if (
        ontology.payload.coding_procedure_id != "life-patterns-development-coding-manual-v2"
        or ontology.payload.coding_procedure_sha256 != coding_manual_sha256
    ):
        raise ValueError("v2 ontology does not bind recurrence-corrected coding manual")
    if sum(len(row.non_action_values) for row in procedure.payload.observable_extensions) != 28:
        raise ValueError("v2 procedure does not preserve exact 28-value non-action registry")

    return ResolvedDevelopmentStackV2(
        source=base.source,
        compact=base.compact,
        resolution=base.resolution,
        resolved=base.resolved,
        ontology=ontology,
        procedure=procedure,
        coding_manual_sha256=coding_manual_sha256,
        recurrence_policy_sha256=recurrence_policy_sha256,
        aggregation_policy_sha256=base.aggregation_policy_sha256,
        theory_policy_sha256=base.theory_policy_sha256,
        observable_ids=observable_ids,
    )
