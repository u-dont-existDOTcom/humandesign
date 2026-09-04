"""Mechanical development-ontology projection of the frozen reconciled codebook.

All substantive names, definitions, criteria, evidence requirements, and categorical subcode
identities come directly from the losslessly parsed theory-blind reconciliation. Generic software
policy fields are fixed here. No target-model information or non-action classification is used.
"""

from __future__ import annotations

from datetime import datetime

from .neutral_measurement import (
    ObservableDefinition,
    OntologyReleaseArtifact,
    OntologyReleasePayload,
    build_ontology_release,
)
from .reconciled_codebook_source import (
    ReconciledCodebookSourceArtifact,
    reconciled_codebook_source_integrity_errors,
)

_SCOPE_STATEMENT = (
    "Mechanically projected episode-level development ontology from the exact frozen "
    "theory-blind reconciled codebook source."
)
_PARTICIPANT_REVIEW_POLICY = (
    "Code only participant-approved frozen episode evidence bound by behavioral-freeze provenance."
)
_THEORY_CONTAMINATION_POLICY = (
    "Target-model, birth, chart, prediction, and model-fit information must be unavailable to coding."
)


def observable_definitions_from_reconciled_source(
    source: ReconciledCodebookSourceArtifact,
) -> tuple[ObservableDefinition, ...]:
    errors = reconciled_codebook_source_integrity_errors(source)
    if errors:
        raise ValueError("invalid reconciled codebook source: " + "; ".join(errors))

    definitions: list[ObservableDefinition] = []
    for row in source.payload.observables:
        allowed_values = tuple(subcode.subcode_id for subcode in row.subcodes) + (
            source.payload.universal_other_specified_id,
        )
        definitions.append(
            ObservableDefinition(
                observable_id=row.observable_id,
                label=row.short_behavioral_name,
                definition=row.operational_definition,
                unit_of_analysis="episode",
                value_type="nominal",
                allowed_values=allowed_values,
                insufficient_semantics=source.payload.universal_insufficient_evidence_text,
                not_applicable_semantics=source.payload.universal_not_applicable_text,
                inclusion_criteria=row.inclusion_criteria,
                exclusion_criteria=row.exclusion_criteria,
                evidence_requirements=(row.minimum_evidence_requirements,),
                participant_review_policy=_PARTICIPANT_REVIEW_POLICY,
                theory_contamination_policy=_THEORY_CONTAMINATION_POLICY,
                origin_status="project_specific",
                validity_status="unreviewed",
                reliability_status="not_evaluated",
                release_notes=(
                    "Mechanical projection from reconciled source "
                    f"{source.artifact_id}; substantive text not rewritten. "
                    f"Original provenance: {row.source_provenance}"
                ),
            )
        )
    return tuple(definitions)


def build_development_ontology_from_reconciled_source(
    source: ReconciledCodebookSourceArtifact,
    *,
    ontology_id: str,
    ontology_version: str,
    coding_manual_id: str,
    coding_manual_sha256: str,
    aggregation_policy_id: str,
    aggregation_policy_sha256: str,
    theory_contamination_policy_id: str,
    theory_contamination_policy_sha256: str,
    source_commit: str,
    released_at_utc: datetime,
) -> OntologyReleaseArtifact:
    """Create a development-only ontology without content-authority promotion."""

    payload = OntologyReleasePayload(
        ontology_id=ontology_id,
        ontology_version=ontology_version,
        release_status="development",
        scope_statement=_SCOPE_STATEMENT,
        observables=observable_definitions_from_reconciled_source(source),
        coding_procedure_id=coding_manual_id,
        coding_procedure_sha256=coding_manual_sha256,
        aggregation_policy_id=aggregation_policy_id,
        aggregation_policy_sha256=aggregation_policy_sha256,
        theory_contamination_policy_id=theory_contamination_policy_id,
        theory_contamination_policy_sha256=theory_contamination_policy_sha256,
        source_commit=source_commit,
        released_at_utc=released_at_utc,
        synthetic_fixture_only=False,
    )
    return build_ontology_release(payload)
