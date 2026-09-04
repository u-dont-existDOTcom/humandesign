"""Structured V2 coding procedure for the theory-blind resolved Life Patterns codebook view."""

from __future__ import annotations

from datetime import datetime

from hdmatch.experiments.canonical import sha256_json

from .neutral_measurement import OntologyReleaseArtifact
from .non_action_resolution import ResolvedCodebookViewArtifactV2
from .reconciled_codebook_source import ReconciledCodebookSourceArtifact
from .structured_annotation_v2 import (
    ObservableProcedureExtensionV2,
    StructuredCodingProcedureArtifactV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_coding_procedure_v2,
)


def resolved_procedure_input_errors(
    *,
    source: ReconciledCodebookSourceArtifact,
    resolved: ResolvedCodebookViewArtifactV2,
    ontology: OntologyReleaseArtifact,
) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(resolved.payload)
    if resolved.view_sha256 != digest or resolved.view_id != f"LPRV-{digest[:20].upper()}":
        errors.append("resolved codebook view failed content-address verification")
    if (
        resolved.payload.base_source_artifact_id != source.artifact_id
        or resolved.payload.base_source_sha256 != source.artifact_sha256
    ):
        errors.append("resolved codebook view does not bind supplied base source")

    ontology_by_id = {row.observable_id: row for row in ontology.payload.observables}
    resolved_by_id = {row.observable_id: row for row in resolved.payload.observables}
    if set(ontology_by_id) != set(resolved_by_id):
        errors.append("resolved codebook and ontology observable sets differ")
    for observable_id, resolved_row in resolved_by_id.items():
        definition = ontology_by_id.get(observable_id)
        if definition is None:
            continue
        expected_values = {row.subcode_id for row in resolved_row.subcodes} | {
            source.payload.universal_other_specified_id
        }
        if set(definition.allowed_values) != expected_values:
            errors.append(
                f"resolved ontology allowed values disagree with resolved view for {observable_id}"
            )
    return tuple(dict.fromkeys(errors))


def build_structured_procedure_from_resolved_view(
    *,
    source: ReconciledCodebookSourceArtifact,
    resolved: ResolvedCodebookViewArtifactV2,
    ontology: OntologyReleaseArtifact,
    coding_manual_sha256: str,
    created_at_utc: datetime,
) -> StructuredCodingProcedureArtifactV2:
    """Build a V2 procedure with the resolved view's exact non-action registry."""

    errors = resolved_procedure_input_errors(source=source, resolved=resolved, ontology=ontology)
    if errors:
        raise ValueError("invalid resolved coding-procedure inputs: " + "; ".join(errors))

    extensions = tuple(
        ObservableProcedureExtensionV2(
            observable_id=observable.observable_id,
            non_action_values=tuple(
                row.subcode_id
                for row in observable.subcodes
                if row.classification == "non_action"
            ),
            other_specified_value=source.payload.universal_other_specified_id,
        )
        for observable in resolved.payload.observables
    )
    return build_structured_coding_procedure_v2(
        StructuredCodingProcedurePayloadV2(
            ontology_artifact_id=ontology.artifact_id,
            ontology_sha256=ontology.ontology_sha256,
            reconciled_codebook_sha256=resolved.view_sha256,
            coding_manual_sha256=coding_manual_sha256,
            observable_extensions=extensions,
            created_at_utc=created_at_utc,
        ),
        ontology,
    )
