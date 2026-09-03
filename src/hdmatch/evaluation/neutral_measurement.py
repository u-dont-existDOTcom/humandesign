"""Content-neutral measurement framework for Life Patterns behavioral freezes.

This module intentionally contains no substantive Human Design, astrology, AstroHD, or
behavioral construct definitions. It provides immutable/versioned ontology artifacts,
episode-level coding records, evidence-provenance validation, deterministic descriptive
aggregation, annotation exchange objects, and reliability-report contracts.

Substantive construct content remains blocked behind the project's H1 human-only content
authority boundary. Software validity does not establish construct validity or reliability.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

OntologyReleaseStatus = Literal["development", "candidate", "frozen_for_validation"]
ObservableOrigin = Literal["reused", "adapted", "project_specific", "synthetic_placeholder"]
UnitOfAnalysis = Literal["episode", "context", "life_phase", "person_aggregate"]
ValueType = Literal["nominal", "ordinal", "boolean", "continuous"]
ValidityStatus = Literal[
    "unreviewed",
    "content_review_pending",
    "content_reviewed",
    "development_validity_evidence",
    "validation_candidate",
]
ReliabilityStatus = Literal[
    "not_evaluated",
    "development_in_progress",
    "human_baseline_evaluated",
    "automation_evaluated",
]
CodeState = Literal["observed", "contradicted", "mixed", "insufficient", "not_applicable"]
CoderType = Literal["human", "deterministic", "llm"]
CodingRunType = Literal[
    "synthetic_fixture",
    "human_development",
    "automated_development",
    "validation",
]
InputModality = Literal["typed", "voice", "mixed", "unknown"]
TheoryExposureState = Literal[
    "none_detected",
    "participant_spontaneous",
    "prior_exposure_possible",
    "unknown",
]
ReliabilityComparisonType = Literal["human_human", "human_automated", "automated_automated"]
ExternalRelation = Literal[
    "exact_reuse",
    "adapted_from",
    "broader_than",
    "narrower_than",
    "related_to",
]
ScalarValue = str | bool | float

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
_VERSION_PATTERN = r"^(?:\d{4}-\d{2}-\d{2}|v?\d+\.\d+(?:\.\d+)?)$"


class MeasurementModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class ExternalConceptReference(MeasurementModel):
    source_name: str = Field(min_length=1)
    external_id: str = Field(min_length=1)
    relation: ExternalRelation
    source_version: str | None = None
    citation: str = Field(min_length=1)
    source_url: str | None = None


class HumanContentAuthorityReceipt(MeasurementModel):
    schema_version: Literal["life-patterns-h1-content-authority-v1"] = (
        "life-patterns-h1-content-authority-v1"
    )
    content_sha256: str = Field(pattern=_SHA256_PATTERN)
    human_authorship_receipt_sha256: str = Field(pattern=_SHA256_PATTERN)
    exposure_adjudication_receipt_sha256: str = Field(pattern=_SHA256_PATTERN)
    content_review_receipt_sha256: str = Field(pattern=_SHA256_PATTERN)
    authorized_at_utc: datetime

    @field_validator("authorized_at_utc")
    @classmethod
    def authority_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("content-authority timestamp must be timezone-aware")
        return value.astimezone(UTC)


class ObservableDefinition(MeasurementModel):
    observable_id: str = Field(pattern=r"^[A-Z][A-Z0-9_.:-]{2,127}$")
    label: str = Field(min_length=1)
    definition: str = Field(min_length=1)
    unit_of_analysis: UnitOfAnalysis
    value_type: ValueType
    allowed_values: tuple[str, ...] = ()
    numeric_min: float | None = None
    numeric_max: float | None = None
    insufficient_semantics: str = Field(min_length=1)
    not_applicable_semantics: str = Field(min_length=1)
    inclusion_criteria: tuple[str, ...] = Field(min_length=1)
    exclusion_criteria: tuple[str, ...] = Field(min_length=1)
    evidence_requirements: tuple[str, ...] = Field(min_length=1)
    positive_examples: tuple[str, ...] = ()
    negative_or_near_miss_examples: tuple[str, ...] = ()
    ambiguity_examples: tuple[str, ...] = ()
    participant_review_policy: str = Field(min_length=1)
    theory_contamination_policy: str = Field(min_length=1)
    external_references: tuple[ExternalConceptReference, ...] = ()
    origin_status: ObservableOrigin
    validity_status: ValidityStatus = "unreviewed"
    reliability_status: ReliabilityStatus = "not_evaluated"
    supersedes_observable_id: str | None = Field(
        default=None,
        pattern=r"^[A-Z][A-Z0-9_.:-]{2,127}$",
    )
    release_notes: str = Field(min_length=1)

    @model_validator(mode="after")
    def value_contract_is_coherent(self) -> ObservableDefinition:
        if self.value_type in {"nominal", "ordinal"}:
            if len(self.allowed_values) < 2:
                raise ValueError("nominal/ordinal observables require at least two allowed values")
            if len(set(self.allowed_values)) != len(self.allowed_values):
                raise ValueError("allowed values must be unique")
            if self.numeric_min is not None or self.numeric_max is not None:
                raise ValueError("categorical observables cannot define numeric bounds")
        elif self.value_type == "boolean":
            if self.allowed_values:
                raise ValueError("boolean observables do not use string allowed values")
            if self.numeric_min is not None or self.numeric_max is not None:
                raise ValueError("boolean observables cannot define numeric bounds")
        else:
            if self.allowed_values:
                raise ValueError("continuous observables cannot define categorical allowed values")
            if (
                self.numeric_min is not None
                and self.numeric_max is not None
                and self.numeric_min >= self.numeric_max
            ):
                raise ValueError("continuous numeric_min must be smaller than numeric_max")
        if self.origin_status == "reused" and not self.external_references:
            raise ValueError("reused observables require an external concept reference")
        if self.supersedes_observable_id == self.observable_id:
            raise ValueError("an observable cannot supersede itself")
        return self


class OntologyReleasePayload(MeasurementModel):
    schema_version: Literal["life-patterns-neutral-ontology-v1"] = (
        "life-patterns-neutral-ontology-v1"
    )
    ontology_id: str = Field(min_length=1)
    ontology_version: str = Field(pattern=_VERSION_PATTERN)
    release_status: OntologyReleaseStatus
    scope_statement: str = Field(min_length=1)
    observables: tuple[ObservableDefinition, ...] = Field(min_length=1)
    coding_procedure_id: str = Field(min_length=1)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    aggregation_policy_id: str = Field(min_length=1)
    aggregation_policy_sha256: str = Field(pattern=_SHA256_PATTERN)
    theory_contamination_policy_id: str = Field(min_length=1)
    theory_contamination_policy_sha256: str = Field(pattern=_SHA256_PATTERN)
    source_commit: str = Field(min_length=7)
    released_at_utc: datetime
    synthetic_fixture_only: bool
    human_content_authority: HumanContentAuthorityReceipt | None = None
    software_validation_does_not_establish_construct_validity: Literal[True] = True

    @field_validator("released_at_utc")
    @classmethod
    def release_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("ontology release timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("observables")
    @classmethod
    def observable_ids_are_unique(
        cls,
        value: tuple[ObservableDefinition, ...],
    ) -> tuple[ObservableDefinition, ...]:
        ids = [row.observable_id for row in value]
        if len(ids) != len(set(ids)):
            raise ValueError("ontology observable IDs must be unique")
        return value

    @model_validator(mode="after")
    def h1_authority_gate(self) -> OntologyReleasePayload:
        origins = {row.origin_status for row in self.observables}
        if self.synthetic_fixture_only:
            if origins != {"synthetic_placeholder"}:
                raise ValueError(
                    "synthetic ontology releases may contain only synthetic_placeholder observables"
                )
            if self.release_status == "frozen_for_validation":
                raise ValueError("synthetic ontology releases cannot be frozen for validation")
            if self.human_content_authority is not None:
                raise ValueError("synthetic ontology releases must not carry human-content authority")
        elif "synthetic_placeholder" in origins:
            raise ValueError("substantive ontology releases cannot contain synthetic placeholders")
        if self.release_status == "frozen_for_validation" and self.human_content_authority is None:
            raise ValueError(
                "frozen substantive ontology requires an H1 human-content authority receipt"
            )
        return self


class OntologyReleaseArtifact(MeasurementModel):
    schema_version: Literal["life-patterns-neutral-ontology-artifact-v1"] = (
        "life-patterns-neutral-ontology-artifact-v1"
    )
    artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: OntologyReleasePayload


class FreezeEvidenceIndex(MeasurementModel):
    session_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_sha256: dict[str, str]
    source_turn_sha256: dict[str, str]
    episode_source_turn_ids: dict[str, tuple[str, ...]]
    episode_input_modality: dict[str, InputModality]
    participant_revised_episode: dict[str, bool]


class CoderIdentity(MeasurementModel):
    coder_id: str = Field(min_length=1)
    coder_type: CoderType
    version: str = Field(min_length=1)
    implementation_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    training_receipt_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    automation_validation_receipt_sha256: str | None = Field(
        default=None,
        pattern=_SHA256_PATTERN,
    )
    birth_chart_model_blind: Literal[True] = True
    target_model_outputs_available: Literal[False] = False

    @model_validator(mode="after")
    def coder_receipts_match_type(self) -> CoderIdentity:
        if self.coder_type == "human" and self.training_receipt_sha256 is None:
            raise ValueError("human coders require a training receipt")
        if self.coder_type in {"deterministic", "llm"} and self.implementation_sha256 is None:
            raise ValueError("automated coders require a pinned implementation hash")
        return self


class CodedEpisodeRecord(MeasurementModel):
    episode_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    state: CodeState
    coded_value: ScalarValue | None = None
    mixed_values: tuple[ScalarValue, ...] = ()
    coder_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    supporting_source_turn_ids: tuple[str, ...] = ()
    counterevidence_source_turn_ids: tuple[str, ...] = ()
    context_qualifiers: tuple[str, ...] = ()
    life_phase_qualifier: str | None = None
    language: str | None = None
    input_modality: InputModality = "unknown"
    theory_exposure: TheoryExposureState = "unknown"
    source_episode_participant_revised: bool
    annotation_note: str | None = None

    @model_validator(mode="after")
    def code_state_controls_values(self) -> CodedEpisodeRecord:
        if self.state == "observed":
            if self.coded_value is None:
                raise ValueError("observed codes require a coded value")
            if self.mixed_values:
                raise ValueError("observed codes cannot also contain mixed values")
        elif self.state == "mixed":
            if self.coded_value is not None:
                raise ValueError("mixed codes use mixed_values rather than coded_value")
            if len(self.mixed_values) < 2:
                raise ValueError("mixed codes require at least two values")
        else:
            if self.coded_value is not None or self.mixed_values:
                raise ValueError(
                    "contradicted/insufficient/not_applicable codes cannot assert coded values"
                )
        if self.state in {"observed", "contradicted", "mixed"} and not (
            self.supporting_source_turn_ids or self.counterevidence_source_turn_ids
        ):
            raise ValueError("informative codes require explicit source-turn evidence")
        if self.state in {"insufficient", "not_applicable"} and self.coder_confidence is not None:
            raise ValueError("insufficient/not_applicable codes must not imply classifier confidence")
        return self


class CodingRunPayload(MeasurementModel):
    schema_version: Literal["life-patterns-neutral-coding-run-v1"] = (
        "life-patterns-neutral-coding-run-v1"
    )
    session_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_id: str = Field(min_length=1)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    coder: CoderIdentity
    run_type: CodingRunType
    records: tuple[CodedEpisodeRecord, ...]
    created_at_utc: datetime
    birth_data_available_to_coder: Literal[False] = False
    chart_or_model_outputs_available_to_coder: Literal[False] = False

    @field_validator("created_at_utc")
    @classmethod
    def coding_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("coding timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("records")
    @classmethod
    def episode_observable_pairs_are_unique(
        cls,
        value: tuple[CodedEpisodeRecord, ...],
    ) -> tuple[CodedEpisodeRecord, ...]:
        keys = [(row.episode_id, row.observable_id) for row in value]
        if len(keys) != len(set(keys)):
            raise ValueError("coding run repeats an episode-observable pair")
        return value


class CodingRunArtifact(MeasurementModel):
    schema_version: Literal["life-patterns-neutral-coding-run-artifact-v1"] = (
        "life-patterns-neutral-coding-run-artifact-v1"
    )
    coding_run_id: str = Field(pattern=r"^LPC-[0-9A-F]{20}$")
    coding_run_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: CodingRunPayload
    scoreable_for_model_tournament: bool
    scoreability_blockers: tuple[str, ...]


class ValueCount(MeasurementModel):
    value: ScalarValue
    count: int = Field(ge=1)


class ContextCoverage(MeasurementModel):
    context: str = Field(min_length=1)
    episode_record_count: int = Field(ge=1)
    informative_episode_count: int = Field(ge=0)


class PersonObservableSummary(MeasurementModel):
    observable_id: str = Field(min_length=1)
    episode_record_count: int = Field(ge=0)
    applicable_episode_count: int = Field(ge=0)
    informative_episode_count: int = Field(ge=0)
    insufficient_episode_count: int = Field(ge=0)
    not_applicable_episode_count: int = Field(ge=0)
    coverage_fraction: float | None = Field(default=None, ge=0.0, le=1.0)
    state_counts: dict[str, int]
    value_counts: tuple[ValueCount, ...]
    distinct_observed_values: int = Field(ge=0)
    context_coverage: tuple[ContextCoverage, ...]
    aggregation_semantics: Literal[
        "descriptive_distribution_preserving_no_trait_collapse"
    ] = "descriptive_distribution_preserving_no_trait_collapse"


class AnnotationTask(MeasurementModel):
    schema_version: Literal["life-patterns-annotation-task-v1"] = "life-patterns-annotation-task-v1"
    task_id: str = Field(min_length=1)
    freeze_id: str = Field(pattern=r"^BPF-[0-9A-F]{20}$")
    freeze_sha256: str = Field(pattern=_SHA256_PATTERN)
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    episode_id: str = Field(min_length=1)
    episode_title: str = Field(min_length=1)
    episode_narrative: str = Field(min_length=1)
    source_turns: tuple[dict[str, Any], ...]
    observable_ids: tuple[str, ...] = Field(min_length=1)
    coding_guidelines_sha256: str = Field(pattern=_SHA256_PATTERN)
    birth_chart_model_blind: Literal[True] = True


class ConfusionCell(MeasurementModel):
    reference_label: str = Field(min_length=1)
    comparison_label: str = Field(min_length=1)
    count: int = Field(ge=0)


class ObservableReliabilityResult(MeasurementModel):
    observable_id: str = Field(min_length=1)
    n_double_coded: int = Field(ge=1)
    class_distribution: dict[str, int]
    raw_agreement: float = Field(ge=0.0, le=1.0)
    krippendorff_alpha: float | None = Field(default=None, ge=-1.0, le=1.0)
    gwet_ac: float | None = Field(default=None, ge=-1.0, le=1.0)
    abstention_rate: float = Field(ge=0.0, le=1.0)
    adjudication_rate: float = Field(ge=0.0, le=1.0)
    confusion_matrix: tuple[ConfusionCell, ...]
    error_categories: dict[str, int]


class ReliabilityReportPayload(MeasurementModel):
    schema_version: Literal["life-patterns-measurement-reliability-report-v1"] = (
        "life-patterns-measurement-reliability-report-v1"
    )
    ontology_artifact_id: str = Field(pattern=r"^LPO-[0-9A-F]{20}$")
    ontology_sha256: str = Field(pattern=_SHA256_PATTERN)
    coding_procedure_sha256: str = Field(pattern=_SHA256_PATTERN)
    development_corpus_sha256: str = Field(pattern=_SHA256_PATTERN)
    comparison_type: ReliabilityComparisonType
    reference_coder_ids: tuple[str, ...] = Field(min_length=1)
    comparison_coder_ids: tuple[str, ...] = Field(min_length=1)
    observable_results: tuple[ObservableReliabilityResult, ...] = Field(min_length=1)
    created_at_utc: datetime
    does_not_establish_construct_validity: Literal[True] = True

    @field_validator("created_at_utc")
    @classmethod
    def reliability_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("reliability-report timestamp must be timezone-aware")
        return value.astimezone(UTC)


class ReliabilityReportArtifact(MeasurementModel):
    schema_version: Literal["life-patterns-measurement-reliability-artifact-v1"] = (
        "life-patterns-measurement-reliability-artifact-v1"
    )
    report_id: str = Field(pattern=r"^LPR-[0-9A-F]{20}$")
    report_sha256: str = Field(pattern=_SHA256_PATTERN)
    payload: ReliabilityReportPayload


def build_ontology_release(payload: OntologyReleasePayload) -> OntologyReleaseArtifact:
    digest = sha256_json(payload)
    if payload.human_content_authority is not None:
        expected_content = sha256_json(
            {
                "ontology_id": payload.ontology_id,
                "ontology_version": payload.ontology_version,
                "scope_statement": payload.scope_statement,
                "observables": payload.observables,
            }
        )
        if payload.human_content_authority.content_sha256 != expected_content:
            raise ValueError("H1 human-content authority does not bind this ontology content")
    return OntologyReleaseArtifact(
        artifact_id=f"LPO-{digest[:20].upper()}",
        ontology_sha256=digest,
        payload=payload,
    )


def ontology_integrity_errors(artifact: OntologyReleaseArtifact) -> tuple[str, ...]:
    errors: list[str] = []
    digest = sha256_json(artifact.payload)
    if artifact.ontology_sha256 != digest or artifact.artifact_id != f"LPO-{digest[:20].upper()}":
        errors.append("ontology artifact failed content-address verification")
    if artifact.payload.human_content_authority is not None:
        expected_content = sha256_json(
            {
                "ontology_id": artifact.payload.ontology_id,
                "ontology_version": artifact.payload.ontology_version,
                "scope_statement": artifact.payload.scope_statement,
                "observables": artifact.payload.observables,
            }
        )
        if artifact.payload.human_content_authority.content_sha256 != expected_content:
            errors.append("H1 human-content authority does not bind ontology content")
    return tuple(errors)


def observable_semantic_fingerprint(observable: ObservableDefinition) -> str:
    return sha256_json(
        {
            "observable_id": observable.observable_id,
            "definition": observable.definition,
            "unit_of_analysis": observable.unit_of_analysis,
            "value_type": observable.value_type,
            "allowed_values": observable.allowed_values,
            "numeric_min": observable.numeric_min,
            "numeric_max": observable.numeric_max,
            "insufficient_semantics": observable.insufficient_semantics,
            "not_applicable_semantics": observable.not_applicable_semantics,
        }
    )


def ontology_successor_errors(
    previous: OntologyReleaseArtifact,
    successor: OntologyReleaseArtifact,
) -> tuple[str, ...]:
    errors = [*ontology_integrity_errors(previous), *ontology_integrity_errors(successor)]
    if previous.payload.ontology_id != successor.payload.ontology_id:
        errors.append("ontology successor must retain the same ontology_id")
    if previous.payload.ontology_version == successor.payload.ontology_version:
        errors.append("ontology successor must use a new version identifier")
    previous_by_id = {row.observable_id: row for row in previous.payload.observables}
    successor_by_id = {row.observable_id: row for row in successor.payload.observables}
    for observable_id in sorted(previous_by_id.keys() & successor_by_id.keys()):
        if observable_semantic_fingerprint(previous_by_id[observable_id]) != observable_semantic_fingerprint(
            successor_by_id[observable_id]
        ):
            errors.append(
                f"observable {observable_id} changed core meaning under the same stable identifier"
            )
    for row in successor.payload.observables:
        if row.supersedes_observable_id is not None and row.supersedes_observable_id not in previous_by_id:
            errors.append(
                f"observable {row.observable_id} supersedes unknown prior observable {row.supersedes_observable_id}"
            )
    return tuple(dict.fromkeys(errors))


def write_ontology_release(path: str | Path, artifact: OntologyReleaseArtifact) -> Path:
    errors = ontology_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid ontology release: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_ontology_release(path: str | Path) -> OntologyReleaseArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = OntologyReleaseArtifact.model_validate(cast(dict[str, Any], raw))
    errors = ontology_integrity_errors(artifact)
    if errors:
        raise ValueError("invalid ontology release: " + "; ".join(errors))
    return artifact


def freeze_evidence_index_from_artifact(artifact: dict[str, Any]) -> FreezeEvidenceIndex:
    payload = artifact.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("behavioral freeze artifact has no payload")
    digest = sha256_json(payload)
    expected_id = f"BPF-{digest[:20].upper()}"
    if artifact.get("freeze_sha256") != digest or artifact.get("freeze_id") != expected_id:
        raise ValueError("behavioral freeze artifact failed content-address verification")
    source = payload.get("behavioral_source")
    if not isinstance(source, dict):
        raise ValueError("behavioral freeze artifact has no behavioral source")
    episodes_raw = source.get("approved_episodes")
    episode_hashes_raw = source.get("approved_episode_sha256")
    turns_raw = source.get("participant_source_turns")
    turn_hashes_raw = source.get("participant_source_turn_sha256")
    if (
        not isinstance(episodes_raw, list)
        or not isinstance(episode_hashes_raw, dict)
        or not isinstance(turns_raw, list)
        or not isinstance(turn_hashes_raw, dict)
    ):
        raise ValueError("behavioral freeze evidence index is incomplete")
    episodes = cast(list[dict[str, Any]], episodes_raw)
    episode_hashes = cast(dict[str, str], episode_hashes_raw)
    turns = cast(list[dict[str, Any]], turns_raw)
    turn_hashes = cast(dict[str, str], turn_hashes_raw)
    turn_ids: list[str] = []
    for turn in turns:
        turn_id = turn.get("turn_id")
        if not isinstance(turn_id, str) or not turn_id:
            raise ValueError("behavioral freeze contains a source turn with an invalid identity")
        turn_ids.append(turn_id)
    if len(turn_ids) != len(set(turn_ids)):
        raise ValueError("behavioral freeze contains duplicate source-turn identities")
    if set(turn_ids) != set(turn_hashes):
        raise ValueError("behavioral freeze source-turn hash index does not match frozen source turns")
    if not all(
        isinstance(turn_id, str)
        and turn_id
        and isinstance(turn_hash, str)
        and len(turn_hash) == 64
        for turn_id, turn_hash in turn_hashes.items()
    ):
        raise ValueError("behavioral freeze source-turn hash index is invalid")
    for turn in turns:
        turn_id = cast(str, turn["turn_id"])
        if sha256_json(turn) != turn_hashes[turn_id]:
            raise ValueError("behavioral freeze source-turn hash does not match source-turn content")
    episode_sources: dict[str, tuple[str, ...]] = {}
    modalities: dict[str, InputModality] = {}
    revised: dict[str, bool] = {}
    for episode in episodes:
        episode_id = episode.get("episode_id")
        if not isinstance(episode_id, str) or episode_id not in episode_hashes:
            raise ValueError("behavioral freeze contains an unindexed approved episode")
        if sha256_json(episode) != episode_hashes[episode_id]:
            raise ValueError("behavioral freeze approved episode hash does not match episode content")
        source_ids_raw = episode.get("source_turn_ids", [])
        if not isinstance(source_ids_raw, list) or not all(isinstance(row, str) for row in source_ids_raw):
            raise ValueError("approved episode source-turn provenance is invalid")
        source_ids = tuple(cast(list[str], source_ids_raw))
        if not set(source_ids).issubset(turn_hashes):
            raise ValueError("approved episode cites a source turn outside the frozen evidence index")
        episode_sources[episode_id] = source_ids
        modality = episode.get("input_modality", "unknown")
        modalities[episode_id] = modality if modality in {"typed", "voice"} else "unknown"
        revised[episode_id] = bool(episode.get("participant_revision", False))
    session_id = payload.get("session_id")
    if not isinstance(session_id, str):
        raise ValueError("behavioral freeze session identity is invalid")
    return FreezeEvidenceIndex(
        session_id=session_id,
        freeze_id=expected_id,
        freeze_sha256=digest,
        episode_sha256=episode_hashes,
        source_turn_sha256=turn_hashes,
        episode_source_turn_ids=episode_sources,
        episode_input_modality=modalities,
        participant_revised_episode=revised,
    )


def _validate_value_against_definition(record: CodedEpisodeRecord, definition: ObservableDefinition) -> None:
    values: tuple[ScalarValue, ...]
    if record.state == "observed":
        assert record.coded_value is not None
        values = (record.coded_value,)
    elif record.state == "mixed":
        values = record.mixed_values
    else:
        return
    for value in values:
        if definition.value_type in {"nominal", "ordinal"}:
            if not isinstance(value, str) or value not in definition.allowed_values:
                raise ValueError(
                    f"observable {definition.observable_id} received a value outside its categorical codebook"
                )
        elif definition.value_type == "boolean":
            if not isinstance(value, bool):
                raise ValueError(f"observable {definition.observable_id} requires boolean values")
        else:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"observable {definition.observable_id} requires numeric values")
            numeric = float(value)
            if definition.numeric_min is not None and numeric < definition.numeric_min:
                raise ValueError(f"observable {definition.observable_id} value is below numeric_min")
            if definition.numeric_max is not None and numeric > definition.numeric_max:
                raise ValueError(f"observable {definition.observable_id} value is above numeric_max")


def coding_run_integrity_errors(
    payload: CodingRunPayload,
    ontology: OntologyReleaseArtifact,
    evidence: FreezeEvidenceIndex,
) -> tuple[str, ...]:
    errors = [*ontology_integrity_errors(ontology)]
    if payload.session_id != evidence.session_id:
        errors.append("coding run session does not match behavioral freeze")
    if payload.freeze_id != evidence.freeze_id or payload.freeze_sha256 != evidence.freeze_sha256:
        errors.append("coding run does not bind the supplied behavioral freeze")
    if (
        payload.ontology_artifact_id != ontology.artifact_id
        or payload.ontology_sha256 != ontology.ontology_sha256
    ):
        errors.append("coding run does not bind the supplied ontology release")
    if (
        payload.coding_procedure_id != ontology.payload.coding_procedure_id
        or payload.coding_procedure_sha256 != ontology.payload.coding_procedure_sha256
    ):
        errors.append("coding run procedure does not match the ontology release")
    definitions = {row.observable_id: row for row in ontology.payload.observables}
    for record in payload.records:
        definition = definitions.get(record.observable_id)
        if definition is None:
            errors.append(f"coding record references unknown observable {record.observable_id}")
            continue
        if definition.unit_of_analysis != "episode":
            errors.append(
                f"episode coding run cannot directly assign non-episode observable {record.observable_id}"
            )
        if record.episode_id not in evidence.episode_sha256:
            errors.append(f"coding record references unknown frozen episode {record.episode_id}")
            continue
        allowed_turns = set(evidence.episode_source_turn_ids[record.episode_id])
        cited_turns = set(record.supporting_source_turn_ids) | set(record.counterevidence_source_turn_ids)
        if not cited_turns.issubset(allowed_turns):
            errors.append(
                f"coding record for {record.episode_id}/{record.observable_id} cites source turns outside that episode"
            )
        expected_modality = evidence.episode_input_modality[record.episode_id]
        if record.input_modality not in {expected_modality, "unknown"}:
            errors.append(
                f"coding record for {record.episode_id}/{record.observable_id} changes frozen input modality"
            )
        if record.source_episode_participant_revised != evidence.participant_revised_episode[record.episode_id]:
            errors.append(
                f"coding record for {record.episode_id}/{record.observable_id} changes participant-revision provenance"
            )
        try:
            _validate_value_against_definition(record, definition)
        except ValueError as exc:
            errors.append(str(exc))
    return tuple(dict.fromkeys(errors))


def coding_run_scoreability_blockers(
    payload: CodingRunPayload,
    ontology: OntologyReleaseArtifact,
    evidence: FreezeEvidenceIndex,
) -> tuple[str, ...]:
    blockers = list(coding_run_integrity_errors(payload, ontology, evidence))
    if ontology.payload.synthetic_fixture_only:
        blockers.append("synthetic ontology cannot produce scoreable research evidence")
    if ontology.payload.release_status != "frozen_for_validation":
        blockers.append("ontology is not frozen for validation")
    if ontology.payload.human_content_authority is None:
        blockers.append("ontology lacks H1 human-content authority")
    if not payload.records:
        blockers.append("coding run contains no coded episode records")
    definitions = {row.observable_id: row for row in ontology.payload.observables}
    used_ids = sorted({row.observable_id for row in payload.records})
    validity_not_ready = [
        observable_id
        for observable_id in used_ids
        if observable_id in definitions
        and definitions[observable_id].validity_status != "validation_candidate"
    ]
    if validity_not_ready:
        blockers.append(
            "coded observables are not validation candidates: " + ", ".join(validity_not_ready)
        )
    reliability_not_ready = [
        observable_id
        for observable_id in used_ids
        if observable_id in definitions
        and definitions[observable_id].reliability_status
        not in {"human_baseline_evaluated", "automation_evaluated"}
    ]
    if reliability_not_ready:
        blockers.append(
            "coded observables lack a human reliability baseline: "
            + ", ".join(reliability_not_ready)
        )
    if payload.run_type != "validation":
        blockers.append("coding run is not a validation run")
    if payload.coder.coder_type in {"llm", "deterministic"} and (
        payload.coder.automation_validation_receipt_sha256 is None
    ):
        blockers.append("automated coder lacks a human-benchmark validation receipt")
    return tuple(dict.fromkeys(blockers))


def build_coding_run_artifact(
    payload: CodingRunPayload,
    ontology: OntologyReleaseArtifact,
    evidence: FreezeEvidenceIndex,
) -> CodingRunArtifact:
    blockers = coding_run_scoreability_blockers(payload, ontology, evidence)
    digest = sha256_json(payload)
    return CodingRunArtifact(
        coding_run_id=f"LPC-{digest[:20].upper()}",
        coding_run_sha256=digest,
        payload=payload,
        scoreable_for_model_tournament=not blockers,
        scoreability_blockers=blockers,
    )


def coding_run_artifact_integrity_errors(
    artifact: CodingRunArtifact,
    ontology: OntologyReleaseArtifact,
    evidence: FreezeEvidenceIndex,
) -> tuple[str, ...]:
    errors = list(coding_run_integrity_errors(artifact.payload, ontology, evidence))
    digest = sha256_json(artifact.payload)
    if artifact.coding_run_sha256 != digest or artifact.coding_run_id != f"LPC-{digest[:20].upper()}":
        errors.append("coding run artifact failed content-address verification")
    blockers = coding_run_scoreability_blockers(artifact.payload, ontology, evidence)
    if artifact.scoreability_blockers != blockers:
        errors.append("stored coding-run blockers disagree with recomputed blockers")
    if artifact.scoreable_for_model_tournament != (not blockers):
        errors.append("stored coding-run scoreability flag disagrees with recomputed blockers")
    return tuple(dict.fromkeys(errors))


def write_coding_run_artifact(
    path: str | Path,
    artifact: CodingRunArtifact,
    ontology: OntologyReleaseArtifact,
    evidence: FreezeEvidenceIndex,
) -> Path:
    errors = coding_run_artifact_integrity_errors(artifact, ontology, evidence)
    if errors:
        raise ValueError("invalid coding run artifact: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_coding_run_artifact(
    path: str | Path,
    ontology: OntologyReleaseArtifact,
    evidence: FreezeEvidenceIndex,
) -> CodingRunArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = CodingRunArtifact.model_validate(cast(dict[str, Any], raw))
    errors = coding_run_artifact_integrity_errors(artifact, ontology, evidence)
    if errors:
        raise ValueError("invalid coding run artifact: " + "; ".join(errors))
    return artifact


def _value_key(value: ScalarValue) -> tuple[str, str]:
    if isinstance(value, bool):
        return ("bool", "true" if value else "false")
    if isinstance(value, str):
        return ("str", value)
    return ("float", repr(float(value)))


def aggregate_person_observables(
    artifact: CodingRunArtifact,
) -> tuple[PersonObservableSummary, ...]:
    by_observable: dict[str, list[CodedEpisodeRecord]] = defaultdict(list)
    for record in artifact.payload.records:
        by_observable[record.observable_id].append(record)
    summaries: list[PersonObservableSummary] = []
    for observable_id in sorted(by_observable):
        records = by_observable[observable_id]
        state_counts = Counter(record.state for record in records)
        applicable = len(records) - state_counts["not_applicable"]
        informative = (
            state_counts["observed"]
            + state_counts["contradicted"]
            + state_counts["mixed"]
        )
        counts: Counter[tuple[str, str]] = Counter()
        raw_values: dict[tuple[str, str], ScalarValue] = {}
        for record in records:
            values = (
                (record.coded_value,)
                if record.state == "observed" and record.coded_value is not None
                else record.mixed_values
                if record.state == "mixed"
                else ()
            )
            for value in values:
                key = _value_key(value)
                counts[key] += 1
                raw_values[key] = value
        contexts: dict[str, list[CodedEpisodeRecord]] = defaultdict(list)
        for record in records:
            for context in record.context_qualifiers:
                contexts[context].append(record)
        context_coverage = tuple(
            ContextCoverage(
                context=context,
                episode_record_count=len(rows),
                informative_episode_count=sum(
                    row.state in {"observed", "contradicted", "mixed"} for row in rows
                ),
            )
            for context, rows in sorted(contexts.items())
        )
        summaries.append(
            PersonObservableSummary(
                observable_id=observable_id,
                episode_record_count=len(records),
                applicable_episode_count=applicable,
                informative_episode_count=informative,
                insufficient_episode_count=state_counts["insufficient"],
                not_applicable_episode_count=state_counts["not_applicable"],
                coverage_fraction=(informative / applicable) if applicable else None,
                state_counts=dict(sorted(state_counts.items())),
                value_counts=tuple(
                    ValueCount(value=raw_values[key], count=count)
                    for key, count in sorted(counts.items())
                ),
                distinct_observed_values=len(counts),
                context_coverage=context_coverage,
            )
        )
    return tuple(summaries)


def build_annotation_tasks(
    freeze_artifact: dict[str, Any],
    ontology: OntologyReleaseArtifact,
) -> tuple[AnnotationTask, ...]:
    errors = ontology_integrity_errors(ontology)
    if errors:
        raise ValueError("invalid ontology release: " + "; ".join(errors))
    evidence = freeze_evidence_index_from_artifact(freeze_artifact)
    payload = cast(dict[str, Any], freeze_artifact["payload"])
    source = cast(dict[str, Any], payload["behavioral_source"])
    episodes = cast(list[dict[str, Any]], source["approved_episodes"])
    turns = cast(list[dict[str, Any]], source.get("participant_source_turns", []))
    turns_by_id = {
        str(row["turn_id"]): row
        for row in turns
        if isinstance(row.get("turn_id"), str)
    }
    episode_observable_ids = tuple(
        row.observable_id for row in ontology.payload.observables if row.unit_of_analysis == "episode"
    )
    if not episode_observable_ids:
        return ()
    tasks: list[AnnotationTask] = []
    for episode in episodes:
        episode_id = str(episode["episode_id"])
        source_turns = tuple(
            turns_by_id[turn_id]
            for turn_id in evidence.episode_source_turn_ids[episode_id]
            if turn_id in turns_by_id
        )
        tasks.append(
            AnnotationTask(
                task_id=f"{evidence.freeze_id}:{episode_id}",
                freeze_id=evidence.freeze_id,
                freeze_sha256=evidence.freeze_sha256,
                ontology_artifact_id=ontology.artifact_id,
                ontology_sha256=ontology.ontology_sha256,
                episode_id=episode_id,
                episode_title=str(episode.get("title") or episode_id),
                episode_narrative=str(episode.get("narrative") or ""),
                source_turns=source_turns,
                observable_ids=episode_observable_ids,
                coding_guidelines_sha256=ontology.payload.coding_procedure_sha256,
            )
        )
    return tuple(tasks)


def build_reliability_report(
    payload: ReliabilityReportPayload,
) -> ReliabilityReportArtifact:
    digest = sha256_json(payload)
    return ReliabilityReportArtifact(
        report_id=f"LPR-{digest[:20].upper()}",
        report_sha256=digest,
        payload=payload,
    )


def reliability_report_integrity_errors(
    artifact: ReliabilityReportArtifact,
    ontology: OntologyReleaseArtifact,
) -> tuple[str, ...]:
    errors = list(ontology_integrity_errors(ontology))
    digest = sha256_json(artifact.payload)
    if artifact.report_sha256 != digest or artifact.report_id != f"LPR-{digest[:20].upper()}":
        errors.append("reliability report failed content-address verification")
    if (
        artifact.payload.ontology_artifact_id != ontology.artifact_id
        or artifact.payload.ontology_sha256 != ontology.ontology_sha256
    ):
        errors.append("reliability report does not bind the supplied ontology")
    known = {row.observable_id for row in ontology.payload.observables}
    unknown = {row.observable_id for row in artifact.payload.observable_results} - known
    if unknown:
        errors.append(f"reliability report references unknown observables: {sorted(unknown)}")
    return tuple(dict.fromkeys(errors))


def write_reliability_report(
    path: str | Path,
    artifact: ReliabilityReportArtifact,
    ontology: OntologyReleaseArtifact,
) -> Path:
    errors = reliability_report_integrity_errors(artifact, ontology)
    if errors:
        raise ValueError("invalid reliability report: " + "; ".join(errors))
    return write_new_bytes(path, canonical_json_bytes(artifact), mode=0o400)


def load_reliability_report(
    path: str | Path,
    ontology: OntologyReleaseArtifact,
) -> ReliabilityReportArtifact:
    raw: Any = load_json_bytes(path, require_canonical=True)
    artifact = ReliabilityReportArtifact.model_validate(cast(dict[str, Any], raw))
    errors = reliability_report_integrity_errors(artifact, ontology)
    if errors:
        raise ValueError("invalid reliability report: " + "; ".join(errors))
    return artifact
