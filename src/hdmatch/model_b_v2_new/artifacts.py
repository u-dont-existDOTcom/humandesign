"""Strict artifacts for the prospective ``MODEL-B-DETAILED-V2-NEW`` model.

The schemas in this module deliberately do not share an identity with the
historical or structural-only Model B artifacts.  A preregistration is the only
input to compilation; the compiled artifact contains no learned or outcome data.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.chart.bodygraph import CHANNELS
from hdmatch.model.mapping_library import (
    MAPPING_DIRECTNESS,
    STRUCTURAL_SALIENCE,
    ContradictionSeverity,
    DirectnessClass,
    StructuralClass,
)
from hdmatch.questionnaire.response import normalize_answer_token

MODEL_ID = "MODEL-B-DETAILED-V2-NEW"
MODEL_VERSION = "V4/V3.2-prospective-detailed-symbolic-v2-new"
BASE_MODEL_ID = "MODEL-A-CORE-V1"
COMPILER_VERSION = "model-b-v2-new-compiler-v1"

_SHA256_PATTERN = r"^[a-f0-9]{64}$"
_ID_PATTERN = r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$"

# Results and candidate-derived material are never valid prospective provenance.
# Matching is intentionally conservative and applies to both paths and URLs.
FORBIDDEN_PROVENANCE_TERMS = frozenset(
    {
        "legacy_runs",
        "legacy-run",
        "search_results",
        "search-result",
        "winning_dates",
        "winning-date",
        "winner",
        "candidate_ranks",
        "candidate-rank",
        "ranked_candidates",
        "ranked-candidates",
        "outcome_support",
        "outcome-support",
        "holdout_results",
        "holdout-result",
        "answer_key",
        "answer-key",
        "reveal_receipt",
        "reveal-receipt",
        "evaluation.json",
    }
)


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ObservationStatus(StrEnum):
    FROZEN = "frozen"
    UNRESOLVED = "unresolved"


class AssignmentScope(StrEnum):
    DISCOVERY = "discovery"


class SourceKind(StrEnum):
    BEHAVIORAL_TARGET = "behavioral_target"
    QUESTIONNAIRE = "candidate_blind_questionnaire"
    METHOD = "v3_v4_method"
    PRIMARY_HD = "primary_hd_source"
    ESTABLISHED_HD = "established_hd_reference"


class SelectorKind(StrEnum):
    COMPLETE_CHANNEL = "complete_channel"
    EXACT_ACTIVATION = "exact_activation"
    DEFINITION = "definition"
    REPEATED_GATE = "repeated_gate"
    EXACT_NODE = "exact_node"
    PROMINENT_ACTIVATION = "prominent_activation"
    QUALIFIED_HANGING_PERSONALITY_EDGE = "qualified_hanging_personality_edge"


class ParentDimension(StrEnum):
    TYPE = "type"
    STRATEGY = "strategy"
    AUTHORITY = "authority"
    PROFILE = "profile"
    DEFINED_CENTERS = "defined_centers"
    DEFINITION = "definition"
    COMPLETE_CHANNELS = "complete_channels"


class ArtifactBinding(FrozenModel):
    """An exact local-file dependency, always relative to the repository root."""

    role: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=_SHA256_PATTERN)

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        return validate_prospective_relative_path(value)


class SourceCatalogEntry(FrozenModel):
    source_id: str = Field(pattern=r"^SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    kind: SourceKind
    title: str = Field(min_length=1)
    local_path: str = Field(min_length=1)
    local_sha256: str = Field(pattern=_SHA256_PATTERN)
    public_url: str | None = None
    locator: str = Field(min_length=1)
    provenance_rationale: str = Field(min_length=1)

    @field_validator("local_path")
    @classmethod
    def validate_local_path(cls, value: str) -> str:
        return validate_prospective_relative_path(value)

    @field_validator("public_url")
    @classmethod
    def validate_public_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.startswith(("https://", "http://")):
            raise ValueError("source URL must use HTTP(S)")
        reject_forbidden_provenance(value)
        return value


class QuestionToken(FrozenModel):
    token: str = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    label: str = Field(min_length=1)
    source_id: str = Field(pattern=r"^SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    source_locator: str = Field(min_length=1)

    @model_validator(mode="after")
    def token_is_mechanical(self) -> QuestionToken:
        if normalize_answer_token(self.label) != self.token:
            raise ValueError("question token must mechanically normalize from its label")
        return self


class QuestionTokenSet(FrozenModel):
    question_id: str = Field(pattern=r"^[A-Z][0-9]{2}$")
    tokens: tuple[QuestionToken, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_tokens(self) -> QuestionTokenSet:
        tokens = tuple(item.token for item in self.tokens)
        if len(tokens) != len(set(tokens)):
            raise ValueError(f"duplicate tokens for question {self.question_id}")
        return self


class CompleteChannelSelector(FrozenModel):
    kind: Literal[SelectorKind.COMPLETE_CHANNEL] = SelectorKind.COMPLETE_CHANNEL
    channel: str = Field(pattern=r"^(?:[1-9]|[1-5][0-9]|6[0-4])-(?:[1-9]|[1-5][0-9]|6[0-4])$")

    @model_validator(mode="after")
    def canonical_channel(self) -> CompleteChannelSelector:
        left, right = (int(value) for value in self.channel.split("-"))
        if left >= right:
            raise ValueError("channel gates must be in ascending canonical order")
        return self


class ExactActivationSelector(FrozenModel):
    kind: Literal[SelectorKind.EXACT_ACTIVATION] = SelectorKind.EXACT_ACTIVATION
    side: Literal["personality", "design"]
    body: Literal["sun", "earth"]
    granularity: Literal["gate", "line", "gate_line"]
    gate: int | None = Field(default=None, ge=1, le=64)
    line: int | None = Field(default=None, ge=1, le=6)
    require_defined_center: Literal[True] = True

    @model_validator(mode="after")
    def exact_fields_for_granularity(self) -> ExactActivationSelector:
        required = {
            "gate": (self.gate is not None, self.line is None),
            "line": (self.gate is None, self.line is not None),
            "gate_line": (self.gate is not None, self.line is not None),
        }[self.granularity]
        if not all(required):
            raise ValueError("activation fields must exactly match the declared granularity")
        return self


class DefinitionSelector(FrozenModel):
    kind: Literal[SelectorKind.DEFINITION] = SelectorKind.DEFINITION
    definition: Literal[
        "no_definition",
        "single_definition",
        "split_definition",
        "triple_split_definition",
        "quadruple_split_definition",
    ]


class RepeatedGateSelector(FrozenModel):
    kind: Literal[SelectorKind.REPEATED_GATE] = SelectorKind.REPEATED_GATE
    gate: int = Field(ge=1, le=64)
    minimum_occurrences: Literal[2] = 2
    require_personality_occurrence: Literal[True] = True
    require_defined_center: Literal[True] = True


class ExactNodeSelector(FrozenModel):
    kind: Literal[SelectorKind.EXACT_NODE] = SelectorKind.EXACT_NODE
    side: Literal["personality", "design"]
    body: Literal["north_node", "south_node"]
    gate: int = Field(ge=1, le=64)
    line: int | None = Field(default=None, ge=1, le=6)


class ProminentActivationSelector(FrozenModel):
    kind: Literal[SelectorKind.PROMINENT_ACTIVATION] = SelectorKind.PROMINENT_ACTIVATION
    side: Literal["personality", "design"]
    body: Literal[
        "moon",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
        "pluto",
    ]
    gate: int = Field(ge=1, le=64)
    require_defined_center: Literal[True] = True


class QualifiedHangingPersonalityEdgeSelector(FrozenModel):
    kind: Literal[SelectorKind.QUALIFIED_HANGING_PERSONALITY_EDGE] = (
        SelectorKind.QUALIFIED_HANGING_PERSONALITY_EDGE
    )
    side: Literal["personality"] = "personality"
    channel: str = Field(pattern=r"^(?:[1-9]|[1-5][0-9]|6[0-4])-(?:[1-9]|[1-5][0-9]|6[0-4])$")
    active_gate: int = Field(ge=1, le=64)
    missing_complement_gate: int = Field(ge=1, le=64)
    require_missing_complement: Literal[True] = True
    require_defined_active_center: Literal[True] = True

    @model_validator(mode="after")
    def qualified_edge_is_canonical(self) -> QualifiedHangingPersonalityEdgeSelector:
        left, right = (int(value) for value in self.channel.split("-"))
        if left >= right:
            raise ValueError("channel gates must be in ascending canonical order")
        if {left, right} != {self.active_gate, self.missing_complement_gate}:
            raise ValueError("hanging edge gates must be exactly the declared channel gates")
        return self


DetailedSelector = Annotated[
    CompleteChannelSelector
    | ExactActivationSelector
    | DefinitionSelector
    | RepeatedGateSelector
    | ExactNodeSelector
    | ProminentActivationSelector
    | QualifiedHangingPersonalityEdgeSelector,
    Field(discriminator="kind"),
]


class ConditionalParentLevel(FrozenModel):
    level_id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    dimensions: tuple[ParentDimension, ...]

    @model_validator(mode="after")
    def dimensions_are_unique(self) -> ConditionalParentLevel:
        if len(self.dimensions) != len(set(self.dimensions)):
            raise ValueError(f"duplicate dimensions in conditional level {self.level_id}")
        return self


class ResponsePrediction(FrozenModel):
    question_id: str = Field(pattern=r"^[A-Z][0-9]{2}$")
    canonical_answer_token: str = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    support_answer_tokens: tuple[str, ...] = Field(min_length=1)
    contradiction_answer_tokens: tuple[str, ...] = ()
    contradiction_severity: ContradictionSeverity = ContradictionSeverity.NONE
    contradiction_rationale: str | None = None

    @model_validator(mode="after")
    def validate_prediction(self) -> ResponsePrediction:
        if self.canonical_answer_token not in self.support_answer_tokens:
            raise ValueError("canonical answer must be a supported answer")
        if len(self.support_answer_tokens) != len(set(self.support_answer_tokens)):
            raise ValueError("support answer tokens must be unique")
        if len(self.contradiction_answer_tokens) != len(set(self.contradiction_answer_tokens)):
            raise ValueError("contradiction answer tokens must be unique")
        overlap = set(self.support_answer_tokens) & set(self.contradiction_answer_tokens)
        if overlap:
            raise ValueError(f"answer tokens cannot be both support and contradiction: {overlap}")
        if self.contradiction_answer_tokens:
            if self.contradiction_severity is ContradictionSeverity.NONE:
                raise ValueError("contradiction tokens require nonzero severity")
            if not self.contradiction_rationale:
                raise ValueError("contradiction tokens require a behavioral-opposition rationale")
            if _is_generic_absence_rationale(self.contradiction_rationale):
                raise ValueError("generic negation or absence is not a behavioral contradiction")
        elif (
            self.contradiction_severity is not ContradictionSeverity.NONE
            or self.contradiction_rationale is not None
        ):
            raise ValueError("contradiction metadata requires explicit opposing answer tokens")
        return self


class StructuralPathway(FrozenModel):
    pathway_id: str = Field(pattern=r"^PATH-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    selector: DetailedSelector
    structural_class: StructuralClass
    structural_salience: float = Field(ge=0.0, le=1.0)
    directness_class: DirectnessClass
    mapping_directness: float = Field(ge=0.0, le=1.0)
    conditional_parent_levels: tuple[ConditionalParentLevel, ...] = Field(min_length=1)
    source_ids: tuple[str, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_frozen_method(self) -> StructuralPathway:
        expected_class = structural_class_for_selector(self.selector)
        if self.structural_class is not expected_class:
            raise ValueError(
                f"selector {self.selector.kind} requires structural class {expected_class}"
            )
        if self.structural_salience != STRUCTURAL_SALIENCE[self.structural_class]:
            raise ValueError("structural salience must equal the frozen V3/V4 constant")
        if self.mapping_directness != MAPPING_DIRECTNESS[self.directness_class]:
            raise ValueError("mapping directness must equal the frozen V3/V4 constant")
        _validate_conditional_hierarchy(self.conditional_parent_levels)
        if len(self.source_ids) != len(set(self.source_ids)):
            raise ValueError("pathway source IDs must be unique")
        return self


class CorroboratingPathway(StructuralPathway):
    independent_of_pathway_ids: tuple[str, ...] = Field(min_length=1)
    independence_rationale: str = Field(min_length=1)


class FrozenObservation(FrozenModel):
    observation_id: str = Field(pattern=r"^OBS-NEW-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    status: Literal[ObservationStatus.FROZEN] = ObservationStatus.FROZEN
    behavioral_statement: str = Field(min_length=1)
    behavioral_confidence: float = Field(gt=0.0, le=1.0)
    dependency_cluster: str = Field(pattern=r"^[A-Z0-9_]+$")
    assignment: Literal["discovery", "holdout"]
    prediction: ResponsePrediction
    primary_pathway: StructuralPathway
    alternative_pathways: tuple[StructuralPathway, ...]
    corroborating_pathway: CorroboratingPathway | None
    source_ids: tuple[str, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_pathways(self) -> FrozenObservation:
        # ``model_fields_set`` prevents an omitted alternatives field from being
        # mistaken for an explicitly preregistered empty alternative set.
        if "alternative_pathways" not in self.model_fields_set:
            raise ValueError("allowed alternative pathways must be explicit, even when empty")
        pathway_ids = (
            self.primary_pathway.pathway_id,
            *(path.pathway_id for path in self.alternative_pathways),
        )
        if len(pathway_ids) != len(set(pathway_ids)):
            raise ValueError("primary and alternative pathway IDs must be unique")
        if self.corroborating_pathway is not None:
            if self.corroborating_pathway.pathway_id in pathway_ids:
                raise ValueError("corroborator pathway ID must be unique")
            if set(self.corroborating_pathway.independent_of_pathway_ids) != set(pathway_ids):
                raise ValueError("corroborator must explicitly address every main pathway")
            corroborator_keys = selector_dependency_keys(self.corroborating_pathway.selector)
            for pathway in (self.primary_pathway, *self.alternative_pathways):
                if corroborator_keys & selector_dependency_keys(
                    pathway.selector
                ) or _definition_channel_dependency(
                    self.corroborating_pathway.selector, pathway.selector
                ):
                    raise ValueError(
                        "corroborator is not dependency-independent of every main pathway"
                    )
        if len(self.source_ids) != len(set(self.source_ids)):
            raise ValueError("observation source IDs must be unique")
        return self


class UnresolvedObservation(FrozenModel):
    """A transparent non-scoreable record with no structural or scoring fields."""

    observation_id: str = Field(pattern=r"^OBS-NEW-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    status: Literal[ObservationStatus.UNRESOLVED] = ObservationStatus.UNRESOLVED
    behavioral_statement: str = Field(min_length=1)
    question_ids: tuple[str, ...]
    source_ids: tuple[str, ...] = Field(min_length=1)
    unresolved_reason: str = Field(min_length=1)


Observation = Annotated[
    FrozenObservation | UnresolvedObservation,
    Field(discriminator="status"),
]


class ModelConstants(FrozenModel):
    information_cap_rubric_bits: float = 6.0
    contradiction_cap_rubric_bits: float = 4.0
    independent_corroboration_cap: float = 0.15
    minimum_effective_reference_size: Literal[500] = 500
    prevalence_weighting: Literal["exact_duration"] = "exact_duration"
    boundary_segmentation: Literal["exact-boundary-events"] = "exact-boundary-events"
    canonical_conflict_policy: Literal["emit_unknown"] = "emit_unknown"

    @model_validator(mode="after")
    def validate_frozen_constants(self) -> ModelConstants:
        if self.information_cap_rubric_bits != 6.0:
            raise ValueError("information cap is frozen at six rubric bits")
        if self.contradiction_cap_rubric_bits != 4.0:
            raise ValueError("contradiction cap is frozen at four rubric bits")
        if self.independent_corroboration_cap != 0.15:
            raise ValueError("independent corroboration cap is frozen at fifteen percent")
        return self


class DiscoveryHoldoutPolicy(FrozenModel):
    assignment_unit: Literal["dependency_cluster"] = "dependency_cluster"
    procedure: Literal["manual_stratified_before_candidate_scoring"] = (
        "manual_stratified_before_candidate_scoring"
    )
    random_seed: None = None
    holdout_cluster_fraction: float = 0.3
    discovery_clusters: tuple[str, ...] = Field(min_length=1)
    holdout_clusters: tuple[str, ...] = Field(min_length=1)
    initial_runtime_scope: Literal["discovery_only"] = "discovery_only"
    holdout_release: Literal["only after discovery candidate/finalist predictions are frozen"] = (
        "only after discovery candidate/finalist predictions are frozen"
    )

    @model_validator(mode="after")
    def validate_split(self) -> DiscoveryHoldoutPolicy:
        if self.holdout_cluster_fraction != 0.3:
            raise ValueError("prospective holdout cluster fraction is frozen at 0.3")
        for label, clusters in (
            ("discovery", self.discovery_clusters),
            ("holdout", self.holdout_clusters),
        ):
            if len(clusters) != len(set(clusters)):
                raise ValueError(f"{label} dependency-cluster IDs must be unique")
            if any(re.fullmatch(r"[A-Z0-9_]+", item) is None for item in clusters):
                raise ValueError(f"{label} dependency-cluster ID is invalid")
        overlap = set(self.discovery_clusters) & set(self.holdout_clusters)
        if overlap:
            raise ValueError(f"discovery and holdout clusters overlap: {sorted(overlap)}")
        total = len(self.discovery_clusters) + len(self.holdout_clusters)
        if len(self.holdout_clusters) / total != self.holdout_cluster_fraction:
            raise ValueError("exact cluster lists do not equal the frozen holdout fraction")
        return self


class PreregistrationArtifact(FrozenModel):
    schema_version: Literal["model-b-v2-new-preregistration-v1"] = (
        "model-b-v2-new-preregistration-v1"
    )
    model_id: Literal["MODEL-B-DETAILED-V2-NEW"] = "MODEL-B-DETAILED-V2-NEW"
    model_version: Literal["V4/V3.2-prospective-detailed-symbolic-v2-new"] = (
        "V4/V3.2-prospective-detailed-symbolic-v2-new"
    )
    base_model_id: Literal["MODEL-A-CORE-V1"] = "MODEL-A-CORE-V1"
    compiler_version: Literal["model-b-v2-new-compiler-v1"] = "model-b-v2-new-compiler-v1"
    preregistered_at_utc: datetime
    behavioral_target: ArtifactBinding
    question_bank: ArtifactBinding
    model_a_base: ArtifactBinding
    local_methods: tuple[ArtifactBinding, ...] = Field(min_length=1)
    source_catalog: tuple[SourceCatalogEntry, ...] = Field(min_length=1)
    question_token_sets: tuple[QuestionTokenSet, ...] = Field(min_length=1)
    constants: ModelConstants = Field(default_factory=ModelConstants)
    discovery_holdout_policy: DiscoveryHoldoutPolicy
    observations: tuple[Observation, ...] = Field(min_length=1)

    @field_validator("preregistered_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("preregistration timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_inventory(self) -> PreregistrationArtifact:
        observation_ids = tuple(item.observation_id for item in self.observations)
        if len(observation_ids) != len(set(observation_ids)):
            raise ValueError("observation IDs must be unique")
        source_ids = tuple(item.source_id for item in self.source_catalog)
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("source catalog IDs must be unique")
        source_set = set(source_ids)
        token_questions = tuple(item.question_id for item in self.question_token_sets)
        if len(token_questions) != len(set(token_questions)):
            raise ValueError("question token sets must be unique")
        token_set = set(token_questions)
        token_sources = {
            token.source_id for item in self.question_token_sets for token in item.tokens
        }
        referenced_sources = set(token_sources)
        for observation in self.observations:
            referenced_sources.update(observation.source_ids)
            if isinstance(observation, FrozenObservation):
                if observation.prediction.question_id not in token_set:
                    raise ValueError(f"missing token set for {observation.prediction.question_id}")
                referenced_sources.update(observation.primary_pathway.source_ids)
                for pathway in observation.alternative_pathways:
                    referenced_sources.update(pathway.source_ids)
                if observation.corroborating_pathway is not None:
                    referenced_sources.update(observation.corroborating_pathway.source_ids)
        unknown_sources = referenced_sources - source_set
        if unknown_sources:
            raise ValueError(f"unknown source IDs: {sorted(unknown_sources)}")
        tokens_by_question = {
            item.question_id: {token.token for token in item.tokens}
            for item in self.question_token_sets
        }
        for observation in self.frozen_observations:
            prediction = observation.prediction
            referenced = {
                prediction.canonical_answer_token,
                *prediction.support_answer_tokens,
                *prediction.contradiction_answer_tokens,
            }
            unknown = referenced - tokens_by_question[prediction.question_id]
            if unknown:
                raise ValueError(
                    f"observation {observation.observation_id} references undeclared "
                    f"question tokens: {sorted(unknown)}"
                )
        assignment_by_cluster: dict[str, str] = {}
        assignment_by_question: dict[str, str] = {}
        for observation in self.frozen_observations:
            previous = assignment_by_cluster.setdefault(
                observation.dependency_cluster, observation.assignment
            )
            if previous != observation.assignment:
                raise ValueError(
                    "every dependency cluster must have exactly one discovery/holdout assignment"
                )
            question_previous = assignment_by_question.setdefault(
                observation.prediction.question_id, observation.assignment
            )
            if question_previous != observation.assignment:
                raise ValueError("every questionnaire question must have exactly one assignment")
        expected_discovery = tuple(
            sorted(
                cluster
                for cluster, assignment in assignment_by_cluster.items()
                if assignment == "discovery"
            )
        )
        expected_holdout = tuple(
            sorted(
                cluster
                for cluster, assignment in assignment_by_cluster.items()
                if assignment == "holdout"
            )
        )
        if set(self.discovery_holdout_policy.discovery_clusters) != set(expected_discovery):
            raise ValueError("discovery cluster list does not match observation assignments")
        if set(self.discovery_holdout_policy.holdout_clusters) != set(expected_holdout):
            raise ValueError("holdout cluster list does not match observation assignments")
        return self

    @property
    def frozen_observations(self) -> tuple[FrozenObservation, ...]:
        return tuple(item for item in self.observations if isinstance(item, FrozenObservation))

    def canonical_bytes(self) -> bytes:
        return canonical_bytes(self)

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


class CompiledPathway(FrozenModel):
    pathway_id: str
    selector: DetailedSelector
    anchor_id: str
    dependency_keys: tuple[str, ...] = Field(min_length=1)
    structural_class: StructuralClass
    structural_salience: float
    directness_class: DirectnessClass
    mapping_directness: float
    conditional_parent_levels: tuple[ConditionalParentLevel, ...] = Field(min_length=1)
    source_ids: tuple[str, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)


class CompiledRule(FrozenModel):
    rule_id: str = Field(pattern=r"^RULE-NEW-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
    observation_id: str
    behavioral_statement: str
    behavioral_confidence: float = Field(gt=0.0, le=1.0)
    dependency_cluster: str
    assignment: Literal["discovery", "holdout"]
    prediction: ResponsePrediction
    primary: CompiledPathway
    alternatives: tuple[CompiledPathway, ...]
    corroborator: CompiledPathway | None
    source_ids: tuple[str, ...]
    rationale: str


class CompiledModelArtifact(FrozenModel):
    schema_version: Literal["model-b-v2-new-compiled-v1"] = "model-b-v2-new-compiled-v1"
    model_id: Literal["MODEL-B-DETAILED-V2-NEW"] = "MODEL-B-DETAILED-V2-NEW"
    model_version: Literal["V4/V3.2-prospective-detailed-symbolic-v2-new"] = (
        "V4/V3.2-prospective-detailed-symbolic-v2-new"
    )
    base_model_id: Literal["MODEL-A-CORE-V1"] = "MODEL-A-CORE-V1"
    compiler_version: Literal["model-b-v2-new-compiler-v1"] = "model-b-v2-new-compiler-v1"
    preregistered_at_utc: datetime
    preregistration_semantic_sha256: str = Field(pattern=_SHA256_PATTERN)
    preregistration_file_sha256: str = Field(pattern=_SHA256_PATTERN)
    behavioral_target: ArtifactBinding
    question_bank: ArtifactBinding
    model_a_base: ArtifactBinding
    local_methods: tuple[ArtifactBinding, ...]
    source_catalog: tuple[SourceCatalogEntry, ...]
    question_token_sets: tuple[QuestionTokenSet, ...]
    constants: ModelConstants
    discovery_holdout_policy: DiscoveryHoldoutPolicy
    rules: tuple[CompiledRule, ...]
    unresolved_observations: tuple[UnresolvedObservation, ...]

    @field_validator("preregistered_at_utc")
    @classmethod
    def require_preregistration_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("compiled preregistration timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def unique_rules(self) -> CompiledModelArtifact:
        rule_ids = tuple(item.rule_id for item in self.rules)
        if len(rule_ids) != len(set(rule_ids)):
            raise ValueError("compiled rule IDs must be unique")
        observation_ids = tuple(item.observation_id for item in self.rules)
        if len(observation_ids) != len(set(observation_ids)):
            raise ValueError("one compiled rule is required per frozen observation")
        assignment_by_cluster: dict[str, str] = {}
        assignment_by_question: dict[str, str] = {}
        for rule in self.rules:
            previous = assignment_by_cluster.setdefault(rule.dependency_cluster, rule.assignment)
            if previous != rule.assignment:
                raise ValueError(
                    "compiled dependency clusters cannot cross discovery/holdout assignments"
                )
            question_previous = assignment_by_question.setdefault(
                rule.prediction.question_id, rule.assignment
            )
            if question_previous != rule.assignment:
                raise ValueError("compiled questionnaire questions cannot cross assignments")
        expected_discovery = tuple(
            sorted(
                cluster
                for cluster, assignment in assignment_by_cluster.items()
                if assignment == "discovery"
            )
        )
        expected_holdout = tuple(
            sorted(
                cluster
                for cluster, assignment in assignment_by_cluster.items()
                if assignment == "holdout"
            )
        )
        if set(self.discovery_holdout_policy.discovery_clusters) != set(expected_discovery):
            raise ValueError("compiled discovery clusters do not match rule assignments")
        if set(self.discovery_holdout_policy.holdout_clusters) != set(expected_holdout):
            raise ValueError("compiled holdout clusters do not match rule assignments")
        return self

    def rules_for_scope(
        self,
        scope: AssignmentScope = AssignmentScope.DISCOVERY,
    ) -> tuple[CompiledRule, ...]:
        if scope is not AssignmentScope.DISCOVERY:
            raise ValueError("the initial V2 runtime exposes discovery scope only")
        return tuple(rule for rule in self.rules if rule.assignment == "discovery")

    def canonical_bytes(self) -> bytes:
        return canonical_bytes(self)

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


class ModelFreezeReceipt(FrozenModel):
    schema_version: Literal["model-b-v2-new-freeze-receipt-v1"] = "model-b-v2-new-freeze-receipt-v1"
    model_id: Literal["MODEL-B-DETAILED-V2-NEW"] = "MODEL-B-DETAILED-V2-NEW"
    model_version: Literal["V4/V3.2-prospective-detailed-symbolic-v2-new"] = (
        "V4/V3.2-prospective-detailed-symbolic-v2-new"
    )
    compiler_version: Literal["model-b-v2-new-compiler-v1"] = "model-b-v2-new-compiler-v1"
    frozen_at_utc: datetime
    source_software_commit: str = Field(pattern=r"^(?:[a-f0-9]{40}|[a-f0-9]{64})$")
    source_software_tree: str = Field(pattern=r"^(?:[a-f0-9]{40}|[a-f0-9]{64})$")
    preregistration: ArtifactBinding
    compiled_artifact: ArtifactBinding
    compiled_semantic_sha256: str = Field(pattern=_SHA256_PATTERN)
    behavioral_target: ArtifactBinding
    question_bank: ArtifactBinding
    model_a_base: ArtifactBinding
    local_methods: tuple[ArtifactBinding, ...] = Field(min_length=1)
    source_catalog: tuple[ArtifactBinding, ...] = Field(min_length=1)

    @field_validator("frozen_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("freeze timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def timestamp_order(self) -> ModelFreezeReceipt:
        # File content, not an unsigned timestamp, is the normative freeze.  The
        # compiler separately verifies preregistration <= freeze.
        roles = tuple(item.role for item in self.source_catalog)
        if len(roles) != len(set(roles)):
            raise ValueError("freeze source-catalog roles must be unique")
        return self


def canonical_bytes(value: BaseModel) -> bytes:
    return json.dumps(
        value.model_dump(mode="json", exclude_none=False),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def load_preregistration(path: str | Path) -> PreregistrationArtifact:
    return PreregistrationArtifact.model_validate_json(Path(path).read_text(encoding="utf-8"))


def load_compiled_artifact(path: str | Path) -> CompiledModelArtifact:
    return CompiledModelArtifact.model_validate_json(Path(path).read_text(encoding="utf-8"))


def load_freeze_receipt(path: str | Path) -> ModelFreezeReceipt:
    return ModelFreezeReceipt.model_validate_json(Path(path).read_text(encoding="utf-8"))


def validate_prospective_relative_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or not path.parts or ".." in path.parts or "." in path.parts:
        raise ValueError("artifact paths must be normalized repository-relative paths")
    if str(path) != normalized:
        raise ValueError("artifact paths must already be normalized")
    reject_forbidden_provenance(normalized)
    return normalized


def reject_forbidden_provenance(value: str) -> None:
    lowered = value.casefold().replace(" ", "_")
    if any(term in lowered for term in FORBIDDEN_PROVENANCE_TERMS):
        raise ValueError(f"forbidden outcome-bearing provenance reference: {value}")


def structural_class_for_selector(selector: DetailedSelector) -> StructuralClass:
    if isinstance(selector, CompleteChannelSelector):
        return StructuralClass.COMPLETE_CHANNEL
    if isinstance(selector, ExactActivationSelector):
        return StructuralClass.CARDINAL_ACTIVATION
    if isinstance(selector, DefinitionSelector):
        return StructuralClass.DEFINITION
    if isinstance(selector, (RepeatedGateSelector, ExactNodeSelector)):
        return StructuralClass.REPEATED_GATE_OR_NODE
    if isinstance(selector, ProminentActivationSelector):
        return StructuralClass.PROMINENT_ACTIVATION
    if isinstance(selector, QualifiedHangingPersonalityEdgeSelector):
        return StructuralClass.HANGING_GATE
    raise AssertionError(f"unsupported selector: {selector}")


def selector_dependency_keys(selector: DetailedSelector) -> frozenset[str]:
    if isinstance(selector, CompleteChannelSelector):
        left, right = selector.channel.split("-")
        return frozenset(
            {
                f"channel:{selector.channel}",
                f"channel-family:{selector.channel}",
                f"gate:{left}",
                f"gate:{right}",
            }
        )
    if isinstance(selector, ExactActivationSelector):
        keys: set[str] = set()
        if selector.gate is not None:
            keys.add(f"gate:{selector.gate}")
            keys.update(_channel_family_keys(selector.gate))
        if selector.line is not None:
            keys.add(f"profile-line:{selector.side}:{selector.line}")
        return frozenset(keys)
    if isinstance(selector, DefinitionSelector):
        return frozenset({f"definition:{selector.definition}"})
    if isinstance(selector, RepeatedGateSelector):
        return frozenset(
            {
                f"gate:{selector.gate}",
                f"repeated-gate:{selector.gate}",
                *_channel_family_keys(selector.gate),
            }
        )
    if isinstance(selector, ExactNodeSelector):
        return frozenset(
            {
                f"activation:{selector.side}:{selector.body}",
                f"node-axis:{selector.side}",
                f"gate:{selector.gate}",
                *_channel_family_keys(selector.gate),
            }
        )
    if isinstance(selector, ProminentActivationSelector):
        return frozenset(
            {
                f"activation:{selector.side}:{selector.body}",
                f"gate:{selector.gate}",
                *_channel_family_keys(selector.gate),
            }
        )
    if isinstance(selector, QualifiedHangingPersonalityEdgeSelector):
        return frozenset(
            {
                f"channel:{selector.channel}",
                f"channel-family:{selector.channel}",
                f"gate:{selector.active_gate}",
            }
        )
    raise AssertionError(f"unsupported selector: {selector}")


def selector_anchor_id(selector: DetailedSelector) -> str:
    payload = json.dumps(
        selector.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    suffix = hashlib.sha256(payload).hexdigest()[:24]
    return f"v2new:{selector.kind.value}:{suffix}"


def _definition_channel_dependency(
    left: DetailedSelector,
    right: DetailedSelector,
) -> bool:
    return (
        isinstance(left, DefinitionSelector) and isinstance(right, CompleteChannelSelector)
    ) or (isinstance(left, CompleteChannelSelector) and isinstance(right, DefinitionSelector))


def _channel_family_keys(gate: int) -> frozenset[str]:
    return frozenset(
        f"channel-family:{channel.identifier}"
        for channel in CHANNELS
        if gate in {channel.gate_a, channel.gate_b}
    )


def _validate_conditional_hierarchy(levels: tuple[ConditionalParentLevel, ...]) -> None:
    level_ids = tuple(level.level_id for level in levels)
    if len(level_ids) != len(set(level_ids)):
        raise ValueError("conditional parent level IDs must be unique")
    if levels[-1].dimensions:
        raise ValueError("conditional parent hierarchy must end with an unconditional level")
    previous = frozenset(levels[0].dimensions)
    for level in levels[1:]:
        current = frozenset(level.dimensions)
        if not current < previous:
            raise ValueError(
                "conditional parent dimensions must be explicitly nested and strictly back off"
            )
        previous = current


def _is_generic_absence_rationale(value: str) -> bool:
    normalized = re.sub(r"[^a-z]+", " ", value.casefold()).strip()
    forbidden_phrases = (
        "structure absent",
        "selector absent",
        "gate absent",
        "channel absent",
        "does not have",
        "not present",
        "missing structure",
        "missing gate",
        "missing channel",
        "mere absence",
        "generic negation",
    )
    if any(phrase in normalized for phrase in forbidden_phrases):
        return True
    absence_terms = ("absent", "absence", "missing", "lacks", "does not contain")
    structure_terms = (
        "selector",
        "structure",
        "gate",
        "channel",
        "activation",
        "definition",
    )
    return any(term in normalized for term in absence_terms) and any(
        term in normalized for term in structure_terms
    )
