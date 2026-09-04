"""Mechanical development-ontology projection of the frozen reconciled codebook.

All substantive names, definitions, criteria, evidence requirements, and categorical subcode
identities come directly from the losslessly parsed theory-blind reconciliation. Generic software
policy fields are fixed here. No target-model information is used.

The original v1 projection remains available unchanged. A separate v2 projection can apply the
versioned theory-blind ambiguity-resolution view without rewriting the frozen v1 source.
"""

from __future__ import annotations

from datetime import datetime

from hdmatch.experiments.canonical import sha256_json

from .neutral_measurement import (
    ObservableDefinition,
    OntologyReleaseArtifact,
    OntologyReleasePayload,
    build_ontology_release,
)
from .non_action_resolution import ResolvedCodebookViewArtifactV2
from .reconciled_codebook_source import (
    ReconciledCodebookSourceArtifact,
    reconciled_codebook_source_integrity_errors,
)

_SCOPE_STATEMENT = (
    "Mechanically projected episode-level development ontology from the exact frozen "
    "theory-blind reconciled codebook source."
)
_RESOLVED_SCOPE_STATEMENT = (
    "Mechanically projected episode-level development ontology from the frozen theory-blind "
    "reconciled codebook plus its separately frozen theory-blind ambiguity-resolution amendment."
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


def _resolved_view_errors(
    source: ReconciledCodebookSourceArtifact,
    resolved: ResolvedCodebookViewArtifactV2,
) -> tuple[str, ...]:
    errors = list(reconciled_codebook_source_integrity_errors(source))
    digest = sha256_json(resolved.payload)
    if resolved.view_sha256 != digest or resolved.view_id != f"LPRV-{digest[:20].upper()}":
        errors.append("resolved codebook view failed content-address verification")
    if (
        resolved.payload.base_source_artifact_id != source.artifact_id
        or resolved.payload.base_source_sha256 != source.artifact_sha256
    ):
        errors.append("resolved codebook view does not bind supplied reconciled source")
    source_ids = [row.observable_id for row in source.payload.observables]
    resolved_ids = [row.observable_id for row in resolved.payload.observables]
    if source_ids != resolved_ids:
        errors.append("resolved codebook view does not preserve source observable sequence")
    return tuple(dict.fromkeys(errors))


def observable_definitions_from_resolved_view(
    source: ReconciledCodebookSourceArtifact,
    resolved: ResolvedCodebookViewArtifactV2,
) -> tuple[ObservableDefinition, ...]:
    """Project exact v1 observable text with only the frozen theory-blind subcode amendment applied."""

    errors = _resolved_view_errors(source, resolved)
    if errors:
        raise ValueError("invalid resolved codebook view: " + "; ".join(errors))

    resolved_by_id = {row.observable_id: row for row in resolved.payload.observables}
    definitions: list[ObservableDefinition] = []
    for row in source.payload.observables:
        resolved_row = resolved_by_id[row.observable_id]
        allowed_values = tuple(subcode.subcode_id for subcode in resolved_row.subcodes) + (
            source.payload.universal_other_specified_id,
        )
        amendment_evidence = tuple(
            f"{subcode.subcode_id}: {subcode.minimum_evidence}"
            for subcode in resolved_row.subcodes
            if subcode.resolution_applied
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
                evidence_requirements=(row.minimum_evidence_requirements,) + amendment_evidence,
                participant_review_policy=_PARTICIPANT_REVIEW_POLICY,
                theory_contamination_policy=_THEORY_CONTAMINATION_POLICY,
                origin_status="project_specific",
                validity_status="unreviewed",
                reliability_status="not_evaluated",
                release_notes=(
                    "Mechanical resolved-v2 projection from base reconciled source "
                    f"{source.artifact_id} and theory-blind resolved view {resolved.view_id}. "
                    f"Original provenance: {row.source_provenance}"
                ),
            )
        )
    return tuple(definitions)


def build_development_ontology_from_resolved_view(
    source: ReconciledCodebookSourceArtifact,
    resolved: ResolvedCodebookViewArtifactV2,
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
    """Create a development-only ontology from v1 + theory-blind v2 amendment."""

    payload = OntologyReleasePayload(
        ontology_id=ontology_id,
        ontology_version=ontology_version,
        release_status="development",
        scope_statement=_RESOLVED_SCOPE_STATEMENT,
        observables=observable_definitions_from_resolved_view(source, resolved),
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
