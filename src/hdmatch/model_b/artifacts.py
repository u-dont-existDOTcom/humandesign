"""Versioned contracts for the detailed V4/V3.2 symbolic feature policy.

Model B deliberately separates mechanically observable chart structures from
behavioral mappings.  The normative repository freezes the former in detail,
but does not supply enough source material to freeze most behavior-to-structure
claims.  An unresolved mapping therefore cannot accidentally become scoreable.
"""

from __future__ import annotations

import hashlib
import json
import re
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class DetailedLayer(StrEnum):
    COMPLETE_CHANNEL = "complete_channel"
    CARDINAL_ACTIVATION = "cardinal_activation"
    DEFINITION = "definition"
    REPEATED_GATE = "repeated_gate"
    THEMATIC_NODE = "thematic_node"
    PROMINENT_ACTIVATION = "prominent_activation"
    HANGING_GATE = "hanging_gate"


SALIENCE_BY_LAYER: dict[DetailedLayer, float] = {
    DetailedLayer.COMPLETE_CHANNEL: 0.80,
    DetailedLayer.CARDINAL_ACTIVATION: 0.75,
    DetailedLayer.DEFINITION: 0.65,
    DetailedLayer.REPEATED_GATE: 0.55,
    DetailedLayer.THEMATIC_NODE: 0.55,
    DetailedLayer.PROMINENT_ACTIVATION: 0.45,
    DetailedLayer.HANGING_GATE: 0.35,
}


class FeatureStatus(StrEnum):
    FROZEN = "frozen"
    UNRESOLVED = "unresolved"


class MappingStatus(StrEnum):
    FROZEN = "frozen"
    UNRESOLVED = "unresolved"
    EMPIRICAL_ONLY = "empirical_only"


class SourceCitation(FrozenModel):
    path: str = Field(min_length=1)
    locator: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


class SourceArtifact(FrozenModel):
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class StructuralFamily(FrozenModel):
    family_id: str = Field(pattern=r"^MBF-[A-Z0-9-]+$")
    layer: DetailedLayer
    feature_status: FeatureStatus
    structural_salience: float = Field(ge=0.0, le=1.0)
    extractor: str = Field(min_length=1)
    conditional_parent_levels: tuple[tuple[str, ...], ...] = Field(min_length=1)
    conditional_parent_status: FeatureStatus
    conditional_parent_unresolved_reason: str | None = None
    dependency_policy_ids: tuple[str, ...] = Field(min_length=1)
    sources: tuple[SourceCitation, ...] = Field(min_length=1)
    unresolved_reason: str | None = None

    @model_validator(mode="after")
    def validate_frozen_constants(self) -> StructuralFamily:
        if self.structural_salience != SALIENCE_BY_LAYER[self.layer]:
            raise ValueError("structural salience must equal the frozen V3 constant")
        if self.conditional_parent_levels[-1] != ():
            raise ValueError("conditional prevalence must end in unconditional backoff")
        for earlier, later in zip(
            self.conditional_parent_levels,
            self.conditional_parent_levels[1:],
            strict=False,
        ):
            if not set(later).issubset(earlier):
                raise ValueError("conditional parent backoff levels must be nested")
        if self.feature_status is FeatureStatus.FROZEN and self.unresolved_reason is not None:
            raise ValueError("frozen feature families cannot have an unresolved reason")
        if self.feature_status is FeatureStatus.UNRESOLVED and not self.unresolved_reason:
            raise ValueError("unresolved feature families require a reason")
        if (
            self.conditional_parent_status is FeatureStatus.FROZEN
            and self.conditional_parent_unresolved_reason is not None
        ):
            raise ValueError("frozen conditional parents cannot have an unresolved reason")
        if (
            self.conditional_parent_status is FeatureStatus.UNRESOLVED
            and not self.conditional_parent_unresolved_reason
        ):
            raise ValueError("unresolved conditional parents require a reason")
        return self


class DependencyPolicy(FrozenModel):
    policy_id: str = Field(pattern=r"^MBD-[A-Z0-9-]+$")
    rule: str = Field(min_length=1)
    sources: tuple[SourceCitation, ...] = Field(min_length=1)


class ConditionalPrevalencePolicy(FrozenModel):
    duration_weighted: Literal[True] = True
    candidate_file_forbidden: Literal[True] = True
    minimum_effective_reference_size: int = Field(default=500, ge=1)
    small_parent_action: Literal["back_off_one_parent_level"] = "back_off_one_parent_level"
    information_cap_rubric_bits: float = 6.0
    sources: tuple[SourceCitation, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_constants(self) -> ConditionalPrevalencePolicy:
        if self.information_cap_rubric_bits != 6.0:
            raise ValueError("V3 single-anchor cap is frozen at 6 rubric bits")
        return self


class UnresolvedBehaviorMapping(FrozenModel):
    mapping_id: str = Field(pattern=r"^MBM-[A-Z0-9-]+$")
    status: Literal[MappingStatus.UNRESOLVED] = MappingStatus.UNRESOLVED
    structural_selector: str = Field(min_length=1)
    question_ids: tuple[str, ...] = ()
    dependency_cluster: str = Field(pattern=r"^[A-Z0-9_]+$")
    sources: tuple[SourceCitation, ...] = Field(min_length=1)
    unresolved_reason: str = Field(min_length=1)
    mapping_directness: None = None
    predicted_response: None = None
    contradiction_rule: None = None


class DetailedAnchor(FrozenModel):
    """One exact detailed structure extracted from a candidate chart."""

    anchor_id: str = Field(min_length=1)
    family_id: str = Field(pattern=r"^MBF-[A-Z0-9-]+$")
    layer: DetailedLayer
    predicate: dict[str, object]
    dependency_keys: tuple[str, ...] = Field(min_length=1)
    structural_salience: float = Field(ge=0.0, le=1.0)
    behavioral_mapping_status: Literal[MappingStatus.UNRESOLVED] = MappingStatus.UNRESOLVED

    @model_validator(mode="after")
    def validate_salience(self) -> DetailedAnchor:
        if self.structural_salience != SALIENCE_BY_LAYER[self.layer]:
            raise ValueError("anchor salience must equal its layer constant")
        return self


class ModelBArtifact(FrozenModel):
    schema_version: Literal["model-b-mapping-library-v1"] = "model-b-mapping-library-v1"
    model_id: Literal["MODEL-B"] = "MODEL-B"
    model_version: Literal["V4/V3.2-detailed-symbolic-v1"] = (
        "V4/V3.2-detailed-symbolic-v1"
    )
    base_model_id: Literal["MODEL-A"] = "MODEL-A"
    base_mapping_path: str = "mappings/mapping_library_v1.json"
    base_mapping_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    question_bank_version: str = Field(min_length=1)
    question_bank_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    source_artifacts: tuple[SourceArtifact, ...] = Field(min_length=1)
    channel_catalog: tuple[str, ...] = Field(min_length=36, max_length=36)
    cardinal_positions: tuple[str, ...] = (
        "personality:sun",
        "personality:earth",
        "design:sun",
        "design:earth",
    )
    node_positions: tuple[str, ...] = (
        "personality:north_node",
        "personality:south_node",
        "design:north_node",
        "design:south_node",
    )
    repeated_gate_minimum_occurrences: Literal[2] = 2
    prominent_activation_allowlist: tuple[str, ...] = ()
    structural_families: tuple[StructuralFamily, ...] = Field(min_length=7, max_length=7)
    dependency_policies: tuple[DependencyPolicy, ...] = Field(min_length=1)
    prevalence_policy: ConditionalPrevalencePolicy
    behavioral_mappings: tuple[UnresolvedBehaviorMapping, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_inventory(self) -> ModelBArtifact:
        channels = tuple(_canonical_channel(item) for item in self.channel_catalog)
        if channels != self.channel_catalog or len(set(channels)) != 36:
            raise ValueError("channel catalog must contain 36 unique canonical channel IDs")
        family_ids = [item.family_id for item in self.structural_families]
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("structural family IDs must be unique")
        if {item.layer for item in self.structural_families} != set(DetailedLayer):
            raise ValueError("artifact must declare every detailed V3 structural layer")
        policy_ids = {item.policy_id for item in self.dependency_policies}
        for family in self.structural_families:
            missing = set(family.dependency_policy_ids) - policy_ids
            if missing:
                raise ValueError(f"family {family.family_id} has unknown policies: {missing}")
        if self.prominent_activation_allowlist:
            raise ValueError(
                "the normative sources do not freeze a prominent-activation allowlist"
            )
        mapping_ids = [item.mapping_id for item in self.behavioral_mappings]
        if len(mapping_ids) != len(set(mapping_ids)):
            raise ValueError("behavioral mapping IDs must be unique")
        return self

    @property
    def family_by_id(self) -> dict[str, StructuralFamily]:
        return {item.family_id: item for item in self.structural_families}

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.model_dump(mode="json", exclude_none=False),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


class ModelBUnresolvedReport(FrozenModel):
    schema_version: Literal["model-b-unresolved-report-v1"] = (
        "model-b-unresolved-report-v1"
    )
    model_id: Literal["MODEL-B"] = "MODEL-B"
    model_version: Literal["V4/V3.2-detailed-symbolic-v1"] = (
        "V4/V3.2-detailed-symbolic-v1"
    )
    artifact_semantic_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    artifact_file_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    frozen_feature_family_count: int = Field(ge=0)
    unresolved_feature_family_count: int = Field(ge=0)
    unresolved_behavior_mapping_count: int = Field(ge=0)
    limitations: tuple[str, ...] = Field(min_length=1)


def load_model_b_artifact(path: str | Path) -> ModelBArtifact:
    return ModelBArtifact.model_validate(json.loads(Path(path).read_text(encoding="utf-8")))


def _canonical_channel(value: str) -> str:
    match = re.fullmatch(r"([1-9]|[1-5][0-9]|6[0-4])-([1-9]|[1-5][0-9]|6[0-4])", value)
    if match is None:
        raise ValueError(f"invalid channel ID: {value}")
    left, right = int(match.group(1)), int(match.group(2))
    if left >= right:
        raise ValueError(f"channel ID must be ascending: {value}")
    return f"{left}-{right}"
