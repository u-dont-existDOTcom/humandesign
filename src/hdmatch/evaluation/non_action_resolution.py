"""Versioned theory-blind resolution of ambiguous Life Patterns non-action subcodes.

The frozen reconciled v1 codebook is never rewritten in place. This module binds the compact
first-pass classification and the separately theory-blind ambiguity-resolution output, validates
that only the originally ambiguous subcodes are revised, and exposes a resolved v2 view for
ontology/procedure construction.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

from .reconciled_codebook_source import (
    ReconciledCodebookSourceArtifact,
    reconciled_codebook_source_integrity_errors,
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
ResolutionKind = Literal["clarify_without_split", "split", "exclude"]
ResolvedClassification = Literal["non_action", "not_non_action"]


class NonActionResolutionModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class CompactNonActionClassification(NonActionResolutionModel):
    schema_version: Literal["life-patterns-non-action-classification-compact-v1"] = (
        "life-patterns-non-action-classification-compact-v1"
    )
    source_scope: Literal["NBM-R01..NBM-R22"] = "NBM-R01..NBM-R22"
    source_subcode_count: int = Field(gt=0)
    rule: str = Field(min_length=1)
    non_action_ids: tuple[str, ...]
    ambiguous_ids: tuple[str, ...]
    counts: dict[str, int]
    provenance: str = Field(min_length=1)

    @model_validator(mode="after")
    def sets_and_counts_are_coherent(self) -> CompactNonActionClassification:
        non_action = set(self.non_action_ids)
        ambiguous = set(self.ambiguous_ids)
        if len(non_action) != len(self.non_action_ids):
            raise ValueError("compact classification repeats a non-action subcode")
        if len(ambiguous) != len(self.ambiguous_ids):
            raise ValueError("compact classification repeats an ambiguous subcode")
        if non_action & ambiguous:
            raise ValueError("compact classification overlaps non-action and ambiguous sets")
        required_keys = {"non_action", "not_non_action", "ambiguous", "total"}
        if set(self.counts) != required_keys:
            raise ValueError("compact classification counts must use exact category keys")
        if self.counts["non_action"] != len(non_action):
            raise ValueError("compact non-action count does not match explicit IDs")
        if self.counts["ambiguous"] != len(ambiguous):
            raise ValueError("compact ambiguous count does not match explicit IDs")
        if self.counts["total"] != self.source_subcode_count:
            raise ValueError("compact total count does not match source subcode count")
        if sum(self.counts[key] for key in ("non_action", "not_non_action", "ambiguous")) != self.counts[
            "total"
        ]:
            raise ValueError("compact category counts do not sum to total")
        return self


class AmbiguityResolutionReplacement(NonActionResolutionModel):
    subcode_id: str = Field(pattern=r"^R\d{2}-[A-Za-z0-9]+$")
    wording: str = Field(min_length=1)
    minimum_evidence: str = Field(min_length=1)
    classification: ResolvedClassification


class AmbiguityResolutionDecision(NonActionResolutionModel):
    observable_id: str = Field(pattern=r"^NBM-R\d{2}$")
    original_subcode_id: str = Field(pattern=r"^R\d{2}-[A-Za-z0-9]+$")
    resolution: ResolutionKind
    replacements: tuple[AmbiguityResolutionReplacement, ...]
    reason: str = Field(min_length=1)

    @field_validator("replacements")
    @classmethod
    def replacement_ids_are_unique(
        cls,
        value: tuple[AmbiguityResolutionReplacement, ...],
    ) -> tuple[AmbiguityResolutionReplacement, ...]:
        ids = [row.subcode_id for row in value]
        if len(ids) != len(set(ids)):
            raise ValueError("ambiguity resolution repeats a replacement subcode ID")
        return value

    @model_validator(mode="after")
    def resolution_shape_is_valid(self) -> AmbiguityResolutionDecision:
        observable_prefix = self.observable_id.replace("NBM-", "") + "-"
        if not self.original_subcode_id.startswith(observable_prefix):
            raise ValueError("original subcode does not belong to observable")
        if any(not row.subcode_id.startswith(observable_prefix) for row in self.replacements):
            raise ValueError("replacement subcode does not belong to observable")
        if self.resolution == "exclude":
            if self.replacements:
                raise ValueError("excluded subcode cannot have replacements")
            return self
        if self.resolution == "clarify_without_split":
            if len(self.replacements) != 1:
                raise ValueError("clarification requires exactly one replacement")
            if self.replacements[0].subcode_id != self.original_subcode_id:
                raise ValueError("clarification must retain original subcode ID")
            return self
        if len(self.replacements) < 2:
            raise ValueError("split resolution requires at least two replacements")
        if any(
            row.subcode_id == self.original_subcode_id
            or not row.subcode_id.startswith(self.original_subcode_id)
            for row in self.replacements
        ):
            raise ValueError("split replacement IDs must extend the original subcode ID")
        return self


class NonActionAmbiguityResolutionPayload(NonActionResolutionModel):
    schema_version: Literal["life-patterns-non-action-ambiguity-resolution-v1"] = (
        "life-patterns-non-action-ambiguity-resolution-v1"
    )
    reconciled_source_artifact_id: str = Field(pattern=r"^LPCB-[0-9A-F]{20}$")
    reconciled_source_sha256: str = Field(pattern=_SHA256_PATTERN)
    compact_classification_sha256: str = Field(pattern=_SHA256_PATTERN)
    resolution_prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    raw_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    normalized_output_sha256: str = Field(pattern=_SHA256_PATTERN)
    author_kind: Literal["human", "ai", "mixed"]
    author_or_model_identity: str | None = None
    author_or_model_version: str | None = None
    fresh_theory_blind_context: Literal[True] = True
    target_theory_information_available: Literal[False] = False
    target_model_outputs_available: Literal[False] = False
    birth_or_chart_data_available: Literal[False] = False
    decisions: tuple[AmbiguityResolutionDecision, ...] = Field(min_length=1)
    created_at_utc: datetime

    @field_validator("created_at_utc")
    @classmethod
    def created_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("ambiguity-resolution timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("decisions")
    @classmethod
    def original_keys_are_unique(
        cls,
        value: tuple[AmbiguityResolutionDecision, ...],
    ) -> tuple[AmbiguityResolutionDecision, ...]:
        keys = [(row.observable_id, row.original_subcode_id) for row in value]
        if len(keys) != len(set(keys)):
            raise ValueError("ambiguity resolution repeats an original subcode")
        return value

    @model_validator(mode="after")
    def ai_resolution_has_model_identity(self) -> NonActionAmbiguityResolutionPayload:
        if self.author_kind in {"ai", "mixed"} and not self.author_or_model_identity:
            raise ValueError("AI-influenced ambiguity resolution requires model identity")
        return self


class NonActionAmbiguityResolutionArtifact(NonActionResolutionModel):
    schema_version: Literal["life-patterns-non-action-ambiguity-resolution-artifact-v1"] = (
        "life-patterns-non-action-ambiguity-resolution-artifact-v1"
    )
    resolution_id: str = Field(pattern=r"^LPAR-[0-9A-F]{20}$")
    resolution_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: NonActionAmbiguityResolutionPayload


class ResolvedSubcodeView(NonActionResolutionModel):
    subcode_id: str = Field(pattern=r"^R\d{2}-[A-Za-z0-9]+$")
    wording: str = Field(min_length=1)
    minimum_evidence: str = Field(min_length=1)
    classification: ResolvedClassification
    source_original_subcode_id: str = Field(pattern=r"^R\d{2}-[A-Za-z0-9]+$")
    resolution_applied: bool


class ResolvedObservableView(NonActionResolutionModel):
    observable_id: str = Field(pattern=r"^NBM-R\d{2}$")
    subcodes: tuple[ResolvedSubcodeView, ...] = Field(min_length=1)


class ResolvedCodebookViewPayloadV2(NonActionResolutionModel):
    schema_version: Literal["life-patterns-resolved-codebook-view-v2"] = (
        "life-patterns-resolved-codebook-view-v2"
    )
    base_source_artifact_id: str = Field(pattern=r"^LPCB-[0-9A-F]{20}$")
    base_source_sha256: str = Field(pattern=_SHA256_PATTERN)
    resolution_id: str = Field(pattern=r"^LPAR-[0-9A-F]{20}$")
    resolution_sha256: str = Field(pattern=_SHA256_PATTERN)
    observables: tuple[ResolvedObservableView, ...] = Field(min_length=1)
    original_subcode_count: int
    resolved_subcode_count: int
    non_action_count: int
    not_non_action_count: int
    base_v1_remains_immutable: Literal[True] = True

    @model_validator(mode="after")
    def resolved_counts_are_coherent(self) -> ResolvedCodebookViewPayloadV2:
        ids = [row.observable_id for row in self.observables]
        expected = [f"NBM-R{index:02d}" for index in range(1, 23)]
        if ids != expected:
            raise ValueError("resolved view must preserve exact R01-R22 observable sequence")
        rows = [subcode for observable in self.observables for subcode in observable.subcodes]
        if len(rows) != self.resolved_subcode_count:
            raise ValueError("resolved subcode count does not match rows")
        if len({row.subcode_id for row in rows}) != len(rows):
            raise ValueError("resolved codebook contains duplicate subcode IDs")
        if self.non_action_count + self.not_non_action_count != self.resolved_subcode_count:
            raise ValueError("resolved classification counts do not cover all subcodes")
        if sum(row.classification == "non_action" for row in rows) != self.non_action_count:
            raise ValueError("resolved non-action count does not match rows")
        return self


class ResolvedCodebookViewArtifactV2(NonActionResolutionModel):
    schema_version: Literal["life-patterns-resolved-codebook-view-artifact-v2"] = (
        "life-patterns-resolved-codebook-view-artifact-v2"
    )
    view_id: str = Field(pattern=r"^LPRV-[0-9A-F]{20}$")
    view_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: ResolvedCodebookViewPayloadV2


def parse_ambiguity_resolution_jsonl(data: bytes) -> tuple[AmbiguityResolutionDecision, ...]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("ambiguity-resolution output is not UTF-8") from exc
    decoder = json.JSONDecoder()
    position = 0
    rows: list[AmbiguityResolutionDecision] = []
    while position < len(text):
        while position < len(text) and text[position].isspace():
            position += 1
        if position >= len(text):
            break
        try:
            value: Any
            value, end = decoder.raw_decode(text, position)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"ambiguity-resolution output contains invalid JSON near character {position}"
            ) from exc
        if not isinstance(value, dict):
            raise ValueError("ambiguity-resolution entries must be JSON objects")
        rows.append(AmbiguityResolutionDecision.model_validate(value))
        position = end
    return tuple(rows)


def load_compact_non_action_classification(path: str | Path) -> CompactNonActionClassification:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return CompactNonActionClassification.model_validate(raw)


def compact_classification_errors(
    compact: CompactNonActionClassification,
    *,
    source: ReconciledCodebookSourceArtifact,
) -> tuple[str, ...]:
    errors = list(reconciled_codebook_source_integrity_errors(source))
    source_ids = {
        subcode.subcode_id
        for observable in source.payload.observables
        for subcode in observable.subcodes
    }
    if len(source_ids) != compact.source_subcode_count:
        errors.append("compact classification source count does not match reconciled source")
    explicit = set(compact.non_action_ids) | set(compact.ambiguous_ids)
    unknown = sorted(explicit - source_ids)
    if unknown:
        errors.append(f"compact classification contains unknown source subcodes: {unknown}")
    derived_not_non = source_ids - explicit
    if len(derived_not_non) != compact.counts["not_non_action"]:
        errors.append("compact derived not-non-action count does not match receipt")
    return tuple(dict.fromkeys(errors))


def ambiguity_resolution_errors(
    artifact: NonActionAmbiguityResolutionArtifact,
    *,
    source: ReconciledCodebookSourceArtifact,
    compact: CompactNonActionClassification,
) -> tuple[str, ...]:
    errors = list(compact_classification_errors(compact, source=source))
    digest = sha256_json(artifact.payload)
    if artifact.resolution_sha256 != digest or artifact.resolution_id != f"LPAR-{digest[:20].upper()}":
        errors.append("ambiguity-resolution artifact failed content-address verification")
    if (
        artifact.payload.reconciled_source_artifact_id != source.artifact_id
        or artifact.payload.reconciled_source_sha256 != source.artifact_sha256
    ):
        errors.append("ambiguity resolution does not bind exact reconciled source")
    if artifact.payload.compact_classification_sha256 != sha256_json(compact):
        errors.append("ambiguity resolution does not bind exact compact classification")

    source_pairs = {
        (observable.observable_id, subcode.subcode_id)
        for observable in source.payload.observables
        for subcode in observable.subcodes
    }
    ambiguous_pairs = {
        (observable.observable_id, subcode.subcode_id)
        for observable in source.payload.observables
        for subcode in observable.subcodes
        if subcode.subcode_id in set(compact.ambiguous_ids)
    }
    actual_pairs = {
        (row.observable_id, row.original_subcode_id) for row in artifact.payload.decisions
    }
    if actual_pairs != ambiguous_pairs:
        errors.append(
            "ambiguity resolution must cover exactly the originally ambiguous source subcodes"
        )

    unaffected_ids = {
        subcode_id for _, subcode_id in source_pairs if subcode_id not in set(compact.ambiguous_ids)
    }
    replacement_ids: set[str] = set()
    for decision in artifact.payload.decisions:
        if (decision.observable_id, decision.original_subcode_id) not in source_pairs:
            errors.append(
                f"ambiguity resolution references unknown original: {decision.observable_id}/{decision.original_subcode_id}"
            )
        for replacement in decision.replacements:
            if replacement.subcode_id in replacement_ids:
                errors.append(f"ambiguity resolution repeats replacement ID: {replacement.subcode_id}")
            replacement_ids.add(replacement.subcode_id)
            if replacement.subcode_id in unaffected_ids:
                errors.append(
                    f"ambiguity resolution replacement collides with unaffected source ID: {replacement.subcode_id}"
                )
    return tuple(dict.fromkeys(errors))


def build_ambiguity_resolution_artifact(
    payload: NonActionAmbiguityResolutionPayload,
    *,
    source: ReconciledCodebookSourceArtifact,
    compact: CompactNonActionClassification,
) -> NonActionAmbiguityResolutionArtifact:
    digest = sha256_json(payload)
    artifact = NonActionAmbiguityResolutionArtifact(
        resolution_id=f"LPAR-{digest[:20].upper()}",
        resolution_sha256=digest,
        payload=payload,
    )
    errors = ambiguity_resolution_errors(artifact, source=source, compact=compact)
    if errors:
        raise ValueError("invalid ambiguity resolution: " + "; ".join(errors))
    return artifact


def build_resolved_codebook_view_v2(
    *,
    source: ReconciledCodebookSourceArtifact,
    compact: CompactNonActionClassification,
    resolution: NonActionAmbiguityResolutionArtifact,
) -> ResolvedCodebookViewArtifactV2:
    errors = ambiguity_resolution_errors(resolution, source=source, compact=compact)
    if errors:
        raise ValueError("invalid ambiguity resolution: " + "; ".join(errors))

    decisions = {row.original_subcode_id: row for row in resolution.payload.decisions}
    non_action_ids = set(compact.non_action_ids)
    observables: list[ResolvedObservableView] = []
    for observable in source.payload.observables:
        resolved_rows: list[ResolvedSubcodeView] = []
        for subcode in observable.subcodes:
            decision = decisions.get(subcode.subcode_id)
            if decision is None:
                resolved_rows.append(
                    ResolvedSubcodeView(
                        subcode_id=subcode.subcode_id,
                        wording=subcode.description,
                        minimum_evidence=observable.minimum_evidence_requirements,
                        classification=(
                            "non_action" if subcode.subcode_id in non_action_ids else "not_non_action"
                        ),
                        source_original_subcode_id=subcode.subcode_id,
                        resolution_applied=False,
                    )
                )
                continue
            for replacement in decision.replacements:
                resolved_rows.append(
                    ResolvedSubcodeView(
                        subcode_id=replacement.subcode_id,
                        wording=replacement.wording,
                        minimum_evidence=replacement.minimum_evidence,
                        classification=replacement.classification,
                        source_original_subcode_id=subcode.subcode_id,
                        resolution_applied=True,
                    )
                )
        observables.append(
            ResolvedObservableView(
                observable_id=observable.observable_id,
                subcodes=tuple(resolved_rows),
            )
        )

    all_rows = [row for observable in observables for row in observable.subcodes]
    payload = ResolvedCodebookViewPayloadV2(
        base_source_artifact_id=source.artifact_id,
        base_source_sha256=source.artifact_sha256,
        resolution_id=resolution.resolution_id,
        resolution_sha256=resolution.resolution_sha256,
        observables=tuple(observables),
        original_subcode_count=compact.source_subcode_count,
        resolved_subcode_count=len(all_rows),
        non_action_count=sum(row.classification == "non_action" for row in all_rows),
        not_non_action_count=sum(row.classification == "not_non_action" for row in all_rows),
    )
    digest = sha256_json(payload)
    return ResolvedCodebookViewArtifactV2(
        view_id=f"LPRV-{digest[:20].upper()}",
        view_sha256=digest,
        payload=payload,
    )


def write_ambiguity_resolution_artifact(
    path: str | Path,
    artifact: NonActionAmbiguityResolutionArtifact,
    *,
    source: ReconciledCodebookSourceArtifact,
    compact: CompactNonActionClassification,
) -> Path:
    errors = ambiguity_resolution_errors(artifact, source=source, compact=compact)
    if errors:
        raise ValueError("invalid ambiguity resolution: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def write_resolved_codebook_view_v2(path: str | Path, artifact: ResolvedCodebookViewArtifactV2) -> Path:
    digest = sha256_json(artifact.payload)
    if artifact.view_sha256 != digest or artifact.view_id != f"LPRV-{digest[:20].upper()}":
        raise ValueError("resolved codebook view failed content-address verification")
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_resolved_codebook_view_v2(path: str | Path) -> ResolvedCodebookViewArtifactV2:
    raw = load_json_bytes(path, require_canonical=True)
    artifact = ResolvedCodebookViewArtifactV2.model_validate(raw)
    digest = sha256_json(artifact.payload)
    if artifact.view_sha256 != digest or artifact.view_id != f"LPRV-{digest[:20].upper()}":
        raise ValueError("resolved codebook view failed content-address verification")
    return artifact
