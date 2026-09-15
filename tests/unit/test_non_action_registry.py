from __future__ import annotations

from datetime import UTC, datetime

import pytest

from hdmatch.evaluation.non_action_registry import (
    NonActionClassificationDecision,
    TheoryBlindNonActionRegistryPayload,
    build_structured_procedure_from_non_action_registry,
    build_theory_blind_non_action_registry,
)
from hdmatch.evaluation.reconciled_codebook_source import (
    ReconciledCodebookSourceArtifact,
    ReconciledCodebookSourcePayload,
    ReconciledObservableSource,
    ReconciledSubcodeSource,
)
from hdmatch.evaluation.reconciled_ontology import (
    build_development_ontology_from_reconciled_source,
)
from hdmatch.experiments.canonical import sha256_json

NOW = datetime(2026, 9, 4, 13, 0, tzinfo=UTC)


def _synthetic_source() -> ReconciledCodebookSourceArtifact:
    observables = tuple(
        ReconciledObservableSource(
            observable_id=f"NBM-R{index:02d}",
            heading=f"Synthetic observable {index}",
            short_behavioral_name=f"Synthetic {index}",
            operational_definition="Synthetic structural definition only.",
            inclusion_criteria=("Synthetic inclusion.",),
            exclusion_criteria=("Synthetic exclusion.",),
            subcodes=(
                ReconciledSubcodeSource(
                    subcode_id=f"R{index:02d}-a",
                    description="Synthetic structural value only.",
                ),
            ),
            minimum_evidence_requirements="Synthetic evidence requirement.",
            counterevidence="Synthetic counterevidence.",
            relevant_context_modifiers="Synthetic context.",
            fictional_boundary_examples=("Synthetic boundary example.",),
            common_coding_mistakes="Synthetic coding mistake.",
            source_provenance="SYNTHETIC TEST ONLY.",
            raw_section_sha256=f"{index:064x}",
            raw_section_markdown=f"SYNTHETIC SECTION {index}",
        )
        for index in range(1, 23)
    )
    payload = ReconciledCodebookSourcePayload(
        source_markdown_sha256="a" * 64,
        source_title="SYNTHETIC RECONCILED SOURCE TEST",
        universal_insufficient_evidence_text="Synthetic insufficient semantics.",
        universal_not_applicable_text="Synthetic not-applicable semantics.",
        universal_other_specified_text="Synthetic other-specified semantics.",
        observables=observables,
    )
    digest = sha256_json(payload)
    return ReconciledCodebookSourceArtifact(
        artifact_id=f"LPCB-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def _ontology(source: ReconciledCodebookSourceArtifact):
    return build_development_ontology_from_reconciled_source(
        source,
        ontology_id="synthetic-reconciled-non-action-test",
        ontology_version="v1.0.0",
        coding_manual_id="synthetic-coding-manual",
        coding_manual_sha256="b" * 64,
        aggregation_policy_id="synthetic-aggregation",
        aggregation_policy_sha256="c" * 64,
        theory_contamination_policy_id="synthetic-theory-policy",
        theory_contamination_policy_sha256="d" * 64,
        source_commit="abcdef0123456789abcdef0123456789abcdef01",
        released_at_utc=NOW,
    )


def _decisions(*, ambiguous_last: bool = False):
    return tuple(
        NonActionClassificationDecision(
            observable_id=f"NBM-R{index:02d}",
            subcode_id=f"R{index:02d}-a",
            classification=(
                "ambiguous"
                if ambiguous_last and index == 22
                else "non_action"
                if index == 1
                else "not_non_action"
            ),
            rationale="Synthetic structural classification only.",
        )
        for index in range(1, 23)
    )


def _payload(source, ontology, *, decisions):
    return TheoryBlindNonActionRegistryPayload(
        reconciled_source_artifact_id=source.artifact_id,
        reconciled_source_sha256=source.artifact_sha256,
        ontology_artifact_id=ontology.artifact_id,
        ontology_sha256=ontology.ontology_sha256,
        classification_prompt_sha256="e" * 64,
        author_kind="ai",
        author_or_model_identity="SYNTHETIC-STRUCTURAL-MODEL",
        author_or_model_version="TEST-VERSION",
        decisions=decisions,
        created_at_utc=NOW,
    )


def test_registry_must_cover_every_reconciled_subcode_exactly_once() -> None:
    source = _synthetic_source()
    ontology = _ontology(source)
    incomplete = _payload(source, ontology, decisions=_decisions()[:-1])
    with pytest.raises(ValueError, match="missing reconciled subcodes"):
        build_theory_blind_non_action_registry(
            incomplete,
            source=source,
            ontology=ontology,
        )


def test_ambiguous_classification_blocks_structured_procedure_freeze() -> None:
    source = _synthetic_source()
    ontology = _ontology(source)
    registry = build_theory_blind_non_action_registry(
        _payload(source, ontology, decisions=_decisions(ambiguous_last=True)),
        source=source,
        ontology=ontology,
    )
    with pytest.raises(ValueError, match="ambiguous non-action classifications block"):
        build_structured_procedure_from_non_action_registry(
            registry,
            source=source,
            ontology=ontology,
            coding_manual_sha256="f" * 64,
            created_at_utc=NOW,
        )


def test_complete_registry_generates_non_action_and_other_specified_extensions() -> None:
    source = _synthetic_source()
    ontology = _ontology(source)
    registry = build_theory_blind_non_action_registry(
        _payload(source, ontology, decisions=_decisions()),
        source=source,
        ontology=ontology,
    )
    procedure = build_structured_procedure_from_non_action_registry(
        registry,
        source=source,
        ontology=ontology,
        coding_manual_sha256="f" * 64,
        created_at_utc=NOW,
    )
    extensions = {row.observable_id: row for row in procedure.payload.observable_extensions}
    assert extensions["NBM-R01"].non_action_values == ("R01-a",)
    assert extensions["NBM-R02"].non_action_values == ()
    assert all(row.other_specified_value == "OS" for row in extensions.values())
    assert procedure.payload.reconciled_codebook_sha256 == source.payload.source_markdown_sha256
