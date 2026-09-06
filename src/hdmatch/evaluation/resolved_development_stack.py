"""Rebuild the repository's exact resolved Life Patterns development measurement stack.

The substantive chain is fixed repository state: reconciled v1 codebook, compact theory-blind
non-action classification, normalized theory-blind ambiguity amendment, resolved view, resolved
development ontology, and Structured Annotation V2 procedure.  This helper removes duplicated
test-only reconstruction logic and gives private development-corpus preparation one fail-closed
entry point.

The ambiguity-resolution artifact timestamp below is a software reconstruction timestamp already
used by the repository's real-fixture tests.  It is not represented as the original chat's
message timestamp.  The preserved raw/normalized hashes and model-identity limitation remain the
actual provenance-bearing fields.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.experiments.canonical import sha256_json

from .neutral_measurement import OntologyReleaseArtifact
from .non_action_resolution import (
    CompactNonActionClassification,
    NonActionAmbiguityResolutionArtifact,
    NonActionAmbiguityResolutionPayload,
    ResolvedCodebookViewArtifactV2,
    build_ambiguity_resolution_artifact,
    build_resolved_codebook_view_v2,
    load_compact_non_action_classification,
    parse_ambiguity_resolution_jsonl,
)
from .reconciled_codebook_source import (
    ReconciledCodebookSourceArtifact,
    parse_reconciled_codebook_file,
)
from .reconciled_ontology import build_development_ontology_from_resolved_view
from .resolved_coding_procedure import build_structured_procedure_from_resolved_view
from .structured_annotation_v2 import StructuredCodingProcedureArtifactV2

CODEBOOK_REL = Path(
    "state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md"
)
COMPACT_REL = Path("state/LIFE-PATTERNS-NON-ACTION-CLASSIFICATION-COMPACT-v1-2026-09-04.json")
RESOLUTION_REL = Path(
    "state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-NORMALIZED-v1-2026-09-04.jsonl"
)
RAW_RESOLUTION_REL = Path(
    "state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-RAW-v1-2026-09-04.jsonl.txt"
)
RESOLUTION_PROMPT_REL = Path(
    "state/LIFE-PATTERNS-NON-ACTION-AMBIGUITY-RESOLUTION-PROMPT-v1-2026-09-04.txt"
)
CODER_PROMPT_REL = Path("state/LIFE-PATTERNS-AUTOMATED-CODING-PROMPT-v3-2026-09-04.txt")
AGGREGATION_POLICY_REL = Path("docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_BRIDGE_SPEC.md")
THEORY_POLICY_REL = Path("docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md")

RESOLUTION_ARTIFACT_RECONSTRUCTION_AT_UTC = datetime(2026, 9, 4, 14, 48, tzinfo=UTC)


@dataclass(frozen=True)
class ResolvedDevelopmentStack:
    source: ReconciledCodebookSourceArtifact
    compact: CompactNonActionClassification
    resolution: NonActionAmbiguityResolutionArtifact
    resolved: ResolvedCodebookViewArtifactV2
    ontology: OntologyReleaseArtifact
    procedure: StructuredCodingProcedureArtifactV2
    coder_prompt_sha256: str
    aggregation_policy_sha256: str
    theory_policy_sha256: str
    observable_ids: tuple[str, ...]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_repository_resolved_development_stack(
    repo_root: str | Path,
    *,
    source_commit: str,
    released_at_utc: datetime,
) -> ResolvedDevelopmentStack:
    root = Path(repo_root)
    if len(source_commit.strip()) < 7:
        raise ValueError("source commit must be a pinned commit or sufficiently specific ref")

    codebook_path = root / CODEBOOK_REL
    compact_path = root / COMPACT_REL
    resolution_path = root / RESOLUTION_REL
    raw_resolution_path = root / RAW_RESOLUTION_REL
    resolution_prompt_path = root / RESOLUTION_PROMPT_REL
    coder_prompt_path = root / CODER_PROMPT_REL
    aggregation_policy_path = root / AGGREGATION_POLICY_REL
    theory_policy_path = root / THEORY_POLICY_REL
    required = (
        codebook_path,
        compact_path,
        resolution_path,
        raw_resolution_path,
        resolution_prompt_path,
        coder_prompt_path,
        aggregation_policy_path,
        theory_policy_path,
    )
    missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
    if missing:
        raise ValueError("resolved development stack is missing repository inputs: " + ", ".join(missing))

    source = parse_reconciled_codebook_file(codebook_path)
    compact = load_compact_non_action_classification(compact_path)
    decisions = parse_ambiguity_resolution_jsonl(resolution_path.read_bytes())
    resolution_payload = NonActionAmbiguityResolutionPayload(
        reconciled_source_artifact_id=source.artifact_id,
        reconciled_source_sha256=source.artifact_sha256,
        compact_classification_sha256=sha256_json(compact),
        resolution_prompt_sha256=file_sha256(resolution_prompt_path),
        raw_output_sha256=file_sha256(raw_resolution_path),
        normalized_output_sha256=file_sha256(resolution_path),
        author_kind="ai",
        author_or_model_identity="THEORY-BLIND-CLEAN-CHAT",
        author_or_model_version="USER-SUPPLIED-OUTPUT; MODEL VERSION NOT RECORDED",
        decisions=decisions,
        created_at_utc=RESOLUTION_ARTIFACT_RECONSTRUCTION_AT_UTC,
    )
    resolution = build_ambiguity_resolution_artifact(
        resolution_payload,
        source=source,
        compact=compact,
    )
    resolved = build_resolved_codebook_view_v2(
        source=source,
        compact=compact,
        resolution=resolution,
    )

    coder_prompt_sha256 = file_sha256(coder_prompt_path)
    aggregation_policy_sha256 = file_sha256(aggregation_policy_path)
    theory_policy_sha256 = file_sha256(theory_policy_path)
    ontology = build_development_ontology_from_resolved_view(
        source,
        resolved,
        ontology_id="life-patterns-theory-blind-resolved-development-v2",
        ontology_version="v2.0.0",
        coding_manual_id="life-patterns-automated-coding-prompt-v3",
        coding_manual_sha256=coder_prompt_sha256,
        aggregation_policy_id="life-patterns-neutral-measurement-bridge",
        aggregation_policy_sha256=aggregation_policy_sha256,
        theory_contamination_policy_id="life-patterns-theory-blind-content-authority-policy",
        theory_contamination_policy_sha256=theory_policy_sha256,
        source_commit=source_commit.strip(),
        released_at_utc=released_at_utc,
    )
    procedure = build_structured_procedure_from_resolved_view(
        source=source,
        resolved=resolved,
        ontology=ontology,
        coding_manual_sha256=coder_prompt_sha256,
        created_at_utc=released_at_utc,
    )
    observable_ids = tuple(row.observable_id for row in ontology.payload.observables)
    expected = tuple(f"NBM-R{index:02d}" for index in range(1, 23))
    if observable_ids != expected:
        raise ValueError("resolved development stack does not contain exact NBM-R01..NBM-R22 order")
    if procedure.payload.reconciled_codebook_sha256 != resolved.view_sha256:
        raise ValueError("resolved procedure does not bind resolved codebook view")
    if sum(len(row.non_action_values) for row in procedure.payload.observable_extensions) != 28:
        raise ValueError("resolved procedure does not contain the exact 28-value non-action registry")

    return ResolvedDevelopmentStack(
        source=source,
        compact=compact,
        resolution=resolution,
        resolved=resolved,
        ontology=ontology,
        procedure=procedure,
        coder_prompt_sha256=coder_prompt_sha256,
        aggregation_policy_sha256=aggregation_policy_sha256,
        theory_policy_sha256=theory_policy_sha256,
        observable_ids=observable_ids,
    )
