from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from hdmatch.evaluation.reconciled_codebook_source import parse_reconciled_codebook_file
from hdmatch.evaluation.reconciled_ontology import (
    build_development_ontology_from_reconciled_source,
    observable_definitions_from_reconciled_source,
)

CODEBOOK_PATH = Path(
    "state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md"
)


def test_projection_copies_all_22_observables_and_exact_subcode_ids() -> None:
    source = parse_reconciled_codebook_file(CODEBOOK_PATH)
    definitions = observable_definitions_from_reconciled_source(source)
    assert len(definitions) == 22
    assert [row.observable_id for row in definitions] == [
        f"NBM-R{index:02d}" for index in range(1, 23)
    ]

    r01 = definitions[0]
    source_r01 = source.payload.observables[0]
    assert r01.label == source_r01.short_behavioral_name
    assert r01.definition == source_r01.operational_definition
    assert r01.inclusion_criteria == source_r01.inclusion_criteria
    assert r01.exclusion_criteria == source_r01.exclusion_criteria
    assert r01.evidence_requirements == (source_r01.minimum_evidence_requirements,)
    assert r01.allowed_values == tuple(row.subcode_id for row in source_r01.subcodes) + ("OS",)
    assert r01.validity_status == "unreviewed"
    assert r01.reliability_status == "not_evaluated"

    r05 = next(row for row in definitions if row.observable_id == "NBM-R05")
    assert "R05-O1" in r05.allowed_values
    assert "R05-R9" in r05.allowed_values
    assert r05.allowed_values[-1] == "OS"


def test_development_projection_cannot_accidentally_claim_validation_authority() -> None:
    source = parse_reconciled_codebook_file(CODEBOOK_PATH)
    ontology = build_development_ontology_from_reconciled_source(
        source,
        ontology_id="life-patterns-neutral-reconciled-development",
        ontology_version="v1.0.0",
        coding_manual_id="life-patterns-automated-coding-prompt-v2",
        coding_manual_sha256="1" * 64,
        aggregation_policy_id="life-patterns-descriptive-aggregation-v1",
        aggregation_policy_sha256="2" * 64,
        theory_contamination_policy_id="life-patterns-theory-blind-policy-v1",
        theory_contamination_policy_sha256="3" * 64,
        source_commit="abcdef0123456789abcdef0123456789abcdef01",
        released_at_utc=datetime(2026, 9, 4, 12, 30, tzinfo=UTC),
    )
    assert ontology.payload.release_status == "development"
    assert ontology.payload.human_content_authority is None
    assert ontology.payload.theory_blind_content_authority is None
    assert ontology.payload.synthetic_fixture_only is False
    assert len(ontology.payload.observables) == 22
