"""Theory-blind classification contract for Life Patterns non-action subcodes.

The four-part non-action gate is generic infrastructure, but deciding which substantive subcode
wording asserts non-action is a content-level interpretation. This module records that decision
without making it. A complete registry must classify every reconciled subcode exactly once and
must have no unresolved ambiguity before it can generate a structured coding procedure.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import canonical_json_bytes, load_json_bytes, sha256_json, write_new_bytes

from .neutral_measurement import OntologyReleaseArtifact
from .reconciled_codebook_source import (
    ReconciledCodebookSourceArtifact,
    reconciled_codebook_source_integrity_errors,
)
from .structured_annotation_v2 import (
    ObservableProcedureExtensionV2,
    StructuredCodingProcedureArtifactV2,
    StructuredCodingProcedurePayloadV2,
    build_structured_coding_procedure_v2,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"

NonActionClassification = Literal["non_action", "not_non_action", "ambiguous"]
RegistryAuthorKind = Literal["human", "ai", "mixed"]


class NonActionRegistryModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class NonActionClassificationDecision(NonActionRegistryModel):
    observable_id: str = Field(pattern=r"^NBM-R\d{2}$")
    subcode_id: str = Field(pattern=r"^R\d{2}-[A-Za-z0-9]+$")
    classification: NonActionClassification
    rationale: str = Field(min_length=1)


class TheoryBlindNonActionRegistryPayload(NonActionRegistryModel):
    schema_version: Literal["life-patterns-theory-blind-non-action-registry-v1"] = (
        "life-patterns-theory-blind-non-action-registry-v1"
    )
    reconciled_source_artifact_id: str = Field(pattern=r"^LPCB-[0-9A-F]{20}$")
    reconciled_source_sha256: str = Field(pattern=_SHA256_PATTERN)
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    classification_prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    author_kind: RegistryAuthorKind
    author_or_model_identity: str | None = None
    author_or_model_version: str | None = None
    fresh_theory_blind_context: Literal[True] = True
    target_theory_information_available: Literal[False] = False
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    decisions: tuple[NonActionClassificationDecision, ...] = Field(min_length=1)
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("non-action registry timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("decisions")
    @classmethod
    def decisions_are_unique(
        cls,
        value: tuple[NonActionClassificationDecision, ...],
    ) -> tuple[NonActionClassificationDecision, ...]:
        keys = [(row.observable_id, row.subcode_id) for row in value]
        if len(keys) != len(set(keys)):
            raise ValueError("non-action registry repeats observable/subcode decisions")
        return value

    @model_validator(mode="after")
    def ai_registry_has_model_identity(self) -> TheoryBlindNonActionRegistryPayload:
        if self.author_kind in {"ai", "mixed"} and not self.author_or_model_identity:
            raise ValueError("AI-influenced non-action registry requires model identity")
        return self


class TheoryBlindNonActionRegistryArtifact(NonActionRegistryModel):
    schema_version: Literal["life-patterns-theory-blind-non-action-registry-artifact-v1"] = (
        "life-patterns-theory-blind-non-action-registry-artifact-v1"
    )
    registry_id: str = Field(pattern=r"^LPNA-[0-9A-F]{20}$")
    registry_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: TheoryBlindNonActionRegistryPayload


def non_action_registry_errors(
    artifact: TheoryBlindNonActionRegistryArtifact,
    *,
    source: ReconciledCodebookSourceArtifact,
    ontology: OntologyReleaseArtifact,
) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(artifact.payload)
    if artifact.registry_sha256 != digest or artifact.registry_id != f"LPNA-{digest[:20].upper()}":
        errors.append("non-action registry failed content-address verification")

    source_errors = reconciled_codebook_source_integrity_errors(source)
    errors.extend(source_errors)
    if (
        artifact.payload.reconciled_source_artifact_id != source.artifact_id
        or artifact.payload.reconciled_source_sha256 != source.artifact_sha256
    ):
        errors.append("non-action registry does not bind exact reconciled source")
    if (
        artifact.payload.ontology_artifact_id != ontology.artifact_id
        or artifact.payload.ontology_sha256 != ontology.ontology_sha256
    ):
        errors.append("non-action registry does not bind exact ontology")

    expected = {
        (observable.observable_id, subcode.subcode_id)
        for observable in source.payload.observables
        for subcode in observable.subcodes
    }
    actual = {(row.observable_id, row.subcode_id) for row in artifact.payload.decisions}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"non-action registry is missing reconciled subcodes: {missing}")
    if extra:
        errors.append(f"non-action registry contains unknown reconciled subcodes: {extra}")
    return tuple(dict.fromkeys(errors))


def build_theory_blind_non_action_registry(
    payload: TheoryBlindNonActionRegistryPayload,
    *,
    source: ReconciledCodebookSourceArtifact,
    ontology: OntologyReleaseArtifact,
) -> TheoryBlindNonActionRegistryArtifact:
    digest = sha256_json(payload)
    artifact = TheoryBlindNonActionRegistryArtifact(
        registry_id=f"LPNA-{digest[:20].upper()}",
        registry_sha256=digest,
        payload=payload,
    )
    errors = non_action_registry_errors(artifact, source=source, ontology=ontology)
    if errors:
        raise ValueError("invalid non-action registry: " + "; ".join(errors))
    return artifact


def build_structured_procedure_from_non_action_registry(
    registry: TheoryBlindNonActionRegistryArtifact,
    *,
    source: ReconciledCodebookSourceArtifact,
    ontology: OntologyReleaseArtifact,
    coding_manual_sha256: str,
    created_at_utc: datetime,
) -> StructuredCodingProcedureArtifactV2:
    errors = non_action_registry_errors(registry, source=source, ontology=ontology)
    if errors:
        raise ValueError("invalid non-action registry: " + "; ".join(errors))
    ambiguous = sorted(
        (row.observable_id, row.subcode_id)
        for row in registry.payload.decisions
        if row.classification == "ambiguous"
    )
    if ambiguous:
        raise ValueError(f"ambiguous non-action classifications block procedure freeze: {ambiguous}")

    non_action_by_observable: dict[str, list[str]] = {
        row.observable_id: [] for row in source.payload.observables
    }
    for decision in registry.payload.decisions:
        if decision.classification == "non_action":
            non_action_by_observable[decision.observable_id].append(decision.subcode_id)

    extensions = tuple(
        ObservableProcedureExtensionV2(
            observable_id=row.observable_id,
            non_action_values=tuple(non_action_by_observable[row.observable_id]),
            other_specified_value=source.payload.universal_other_specified_id,
        )
        for row in source.payload.observables
    )
    return build_structured_coding_procedure_v2(
        StructuredCodingProcedurePayloadV2(
            ontology_artifact_id=ontology.artifact_id,
            ontology_sha256=ontology.ontology_sha256,
            reconciled_codebook_sha256=source.payload.source_markdown_sha256,
            coding_manual_sha256=coding_manual_sha256,
            observable_extensions=extensions,
            created_at_utc=created_at_utc,
        ),
        ontology,
    )


def write_theory_blind_non_action_registry(
    path: str | Path,
    artifact: TheoryBlindNonActionRegistryArtifact,
    *,
    source: ReconciledCodebookSourceArtifact,
    ontology: OntologyReleaseArtifact,
) -> Path:
    errors = non_action_registry_errors(artifact, source=source, ontology=ontology)
    if errors:
        raise ValueError("invalid non-action registry: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_theory_blind_non_action_registry(
    path: str | Path,
    *,
    source: ReconciledCodebookSourceArtifact,
    ontology: OntologyReleaseArtifact,
) -> TheoryBlindNonActionRegistryArtifact:
    raw = load_json_bytes(path, require_canonical=True)
    artifact = TheoryBlindNonActionRegistryArtifact.model_validate(raw)
    errors = non_action_registry_errors(artifact, source=source, ontology=ontology)
    if errors:
        raise ValueError("invalid non-action registry: " + "; ".join(errors))
    return artifact
