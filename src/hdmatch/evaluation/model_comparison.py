"""Read-only structural-resolution comparison for Model A and Model B.

This module does not score questionnaire responses and accepts no answer key.  Its
Model B result is deliberately an upper bound: it asks how finely the mechanically
extracted detailed anchors *could* partition an exact candidate universe if those
anchors were behaviorally observable.  The repository's detailed behavioral
mappings remain unresolved, so this is neither recovery performance nor validation.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from datetime import timedelta
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.model_b.artifacts import MappingStatus, ModelBArtifact
from hdmatch.model_b.predicates import extract_detailed_anchors
from hdmatch.schemas import CandidateState
from hdmatch.util import sha256_json

MODEL_A_ID: Final[Literal["MODEL-A-CORE-V1"]] = "MODEL-A-CORE-V1"
MODEL_B_ID: Final[Literal["MODEL-B-DETAILED-V1"]] = "MODEL-B-DETAILED-V1"


class FrozenAuditModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class StructuralEquivalenceGroup(FrozenAuditModel):
    """Candidate intervals that have one identical structural signature."""

    signature_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    signature: tuple[str, ...] = Field(min_length=1)
    state_ids: tuple[str, ...] = Field(min_length=1)
    interval_count: int = Field(ge=1)
    duration_microseconds: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_group(self) -> StructuralEquivalenceGroup:
        if self.interval_count != len(self.state_ids):
            raise ValueError("interval_count must equal the number of state IDs")
        if self.signature_sha256 != sha256_json(self.signature):
            raise ValueError("signature hash does not match the canonical signature")
        return self


class StructuralResolution(FrozenAuditModel):
    """Exact partition counts for one declared structural signature."""

    model_id: Literal["MODEL-A-CORE-V1", "MODEL-B-DETAILED-V1"]
    signature_scope: Literal[
        "model_a_core",
        "model_a_core_plus_model_b_detailed_anchors",
    ]
    interpretation: str = Field(min_length=1)
    interval_count: int = Field(ge=1)
    total_duration_microseconds: int = Field(ge=1)
    unique_signature_count: int = Field(ge=1)
    singleton_signature_count: int = Field(ge=0)
    largest_equivalence_group_interval_count: int = Field(ge=1)
    largest_equivalence_group_duration_microseconds: int = Field(ge=1)
    duration_collision_numerator_microseconds_squared: int = Field(ge=1)
    duration_collision_denominator_microseconds_squared: int = Field(ge=1)
    equivalence_groups: tuple[StructuralEquivalenceGroup, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_totals(self) -> StructuralResolution:
        groups = self.equivalence_groups
        if self.unique_signature_count != len(groups):
            raise ValueError("unique_signature_count must equal the number of groups")
        if len({group.signature_sha256 for group in groups}) != len(groups):
            raise ValueError("structural signature hashes must be unique")
        if sum(group.interval_count for group in groups) != self.interval_count:
            raise ValueError("equivalence-group interval counts do not cover the universe")
        if sum(group.duration_microseconds for group in groups) != self.total_duration_microseconds:
            raise ValueError("equivalence-group durations do not cover the universe")
        if self.singleton_signature_count != sum(group.interval_count == 1 for group in groups):
            raise ValueError("singleton_signature_count is inconsistent")
        if self.largest_equivalence_group_interval_count != max(
            group.interval_count for group in groups
        ):
            raise ValueError("largest interval-count group is inconsistent")
        if self.largest_equivalence_group_duration_microseconds != max(
            group.duration_microseconds for group in groups
        ):
            raise ValueError("largest duration group is inconsistent")
        collision_numerator = sum(group.duration_microseconds**2 for group in groups)
        if self.duration_collision_numerator_microseconds_squared != collision_numerator:
            raise ValueError("duration collision numerator is inconsistent")
        if (
            self.duration_collision_denominator_microseconds_squared
            != self.total_duration_microseconds**2
        ):
            raise ValueError("duration collision denominator is inconsistent")
        return self


class ModelComparisonAudit(FrozenAuditModel):
    """Deterministic comparison with claims constrained to structural resolution."""

    schema_version: Literal["model-structural-comparison-v1"] = "model-structural-comparison-v1"
    comparison_kind: Literal["structural_resolution_upper_bound_not_behavioral_recovery"] = (
        "structural_resolution_upper_bound_not_behavioral_recovery"
    )
    answer_keys_used: Literal[False] = False
    detailed_behavioral_mapping_status: Literal[MappingStatus.UNRESOLVED] = MappingStatus.UNRESOLVED
    model_b_refines_model_a: Literal[True] = True
    model_a: StructuralResolution
    model_b: StructuralResolution
    signature_count_gain: int = Field(ge=0)
    model_a_groups_split_by_model_b: int = Field(ge=0)
    model_a_groups_not_split_by_model_b: int = Field(ge=0)
    limitations: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_comparison(self) -> ModelComparisonAudit:
        if self.model_a.model_id != MODEL_A_ID or self.model_b.model_id != MODEL_B_ID:
            raise ValueError("comparison must contain the frozen Model A and Model B IDs")
        if self.model_a.interval_count != self.model_b.interval_count:
            raise ValueError("both models must audit the same candidate intervals")
        if self.model_a.total_duration_microseconds != self.model_b.total_duration_microseconds:
            raise ValueError("both models must audit the same candidate duration")
        if self.signature_count_gain != (
            self.model_b.unique_signature_count - self.model_a.unique_signature_count
        ):
            raise ValueError("signature_count_gain is inconsistent")
        if (
            self.model_a_groups_split_by_model_b + self.model_a_groups_not_split_by_model_b
            != self.model_a.unique_signature_count
        ):
            raise ValueError("Model A split counts do not cover every Model A group")
        return self


def model_a_core_signature(state: CandidateState) -> tuple[str, ...]:
    """Return the exact coarse architecture frozen by Model A."""

    chart = state.chart_features
    centers = ",".join(sorted(set(chart.defined_centers)))
    return (
        f"type={chart.type}",
        f"strategy={chart.strategy}",
        f"authority={chart.authority}",
        f"profile={chart.profile}",
        f"defined_centers={centers}",
    )


def model_b_detailed_signature(
    state: CandidateState,
    artifact: ModelBArtifact,
) -> tuple[str, ...]:
    """Return Model A core plus all mechanically extractable Model B anchors.

    Including Model A makes the composite Model B partition a strict refinement (or
    equality) of Model A.  Unresolved candidate anchors are included only because this
    audit is explicitly a structural-resolution upper bound.
    """

    core = tuple(f"model_a::{item}" for item in model_a_core_signature(state))
    anchors = extract_detailed_anchors(
        state.chart_features,
        artifact,
        include_unresolved_candidates=True,
    )
    if any(anchor.behavioral_mapping_status is not MappingStatus.UNRESOLVED for anchor in anchors):
        raise ValueError("structural upper-bound audit requires unresolved detailed mappings")
    return (*core, *(f"model_b_anchor::{anchor.anchor_id}" for anchor in anchors))


def audit_structural_discrimination(
    states: Iterable[CandidateState],
    artifact: ModelBArtifact,
) -> ModelComparisonAudit:
    """Partition one exact candidate universe without responses or answer keys."""

    state_tuple = tuple(
        sorted(states, key=lambda item: (item.start_utc, item.end_utc, item.state_id))
    )
    _validate_universe(state_tuple, artifact)

    model_a_signatures = {state.state_id: model_a_core_signature(state) for state in state_tuple}
    model_b_signatures = {
        state.state_id: model_b_detailed_signature(state, artifact) for state in state_tuple
    }
    model_a = _resolution(
        state_tuple,
        model_a_signatures,
        model_id=MODEL_A_ID,
        signature_scope="model_a_core",
        interpretation=(
            "Coarse type/strategy, authority, profile, and defined-center architecture."
        ),
    )
    model_b = _resolution(
        state_tuple,
        model_b_signatures,
        model_id=MODEL_B_ID,
        signature_scope="model_a_core_plus_model_b_detailed_anchors",
        interpretation=(
            "Structural-resolution upper bound from Model A core plus every extracted "
            "Model B detailed anchor; detailed anchors have no frozen behavioral mapping."
        ),
    )

    model_b_hash_by_state = {
        state_id: sha256_json(signature) for state_id, signature in model_b_signatures.items()
    }
    split = sum(
        len({model_b_hash_by_state[state_id] for state_id in group.state_ids}) > 1
        for group in model_a.equivalence_groups
    )
    return ModelComparisonAudit(
        model_a=model_a,
        model_b=model_b,
        signature_count_gain=model_b.unique_signature_count - model_a.unique_signature_count,
        model_a_groups_split_by_model_b=split,
        model_a_groups_not_split_by_model_b=model_a.unique_signature_count - split,
        limitations=(
            "Model B detailed behavior-to-structure mappings are unresolved and unscoreable.",
            "This partition assumes detailed structural anchors could be observed perfectly; it "
            "is an upper bound, not questionnaire recovery performance.",
            "No answer key, behavioral response, or prediction is consumed by this audit.",
            "The result measures only the supplied exact candidate universe and does not validate "
            "Human Design in humans.",
        ),
    )


def _resolution(
    states: tuple[CandidateState, ...],
    signatures: dict[str, tuple[str, ...]],
    *,
    model_id: Literal["MODEL-A-CORE-V1", "MODEL-B-DETAILED-V1"],
    signature_scope: Literal[
        "model_a_core",
        "model_a_core_plus_model_b_detailed_anchors",
    ],
    interpretation: str,
) -> StructuralResolution:
    grouped: dict[tuple[str, ...], list[CandidateState]] = defaultdict(list)
    for state in states:
        grouped[signatures[state.state_id]].append(state)
    groups = tuple(
        StructuralEquivalenceGroup(
            signature_sha256=sha256_json(signature),
            signature=signature,
            state_ids=tuple(state.state_id for state in members),
            interval_count=len(members),
            duration_microseconds=sum(_duration_microseconds(state) for state in members),
        )
        for signature, members in sorted(grouped.items())
    )
    total_duration = sum(group.duration_microseconds for group in groups)
    return StructuralResolution(
        model_id=model_id,
        signature_scope=signature_scope,
        interpretation=interpretation,
        interval_count=len(states),
        total_duration_microseconds=total_duration,
        unique_signature_count=len(groups),
        singleton_signature_count=sum(group.interval_count == 1 for group in groups),
        largest_equivalence_group_interval_count=max(group.interval_count for group in groups),
        largest_equivalence_group_duration_microseconds=max(
            group.duration_microseconds for group in groups
        ),
        duration_collision_numerator_microseconds_squared=sum(
            group.duration_microseconds**2 for group in groups
        ),
        duration_collision_denominator_microseconds_squared=total_duration**2,
        equivalence_groups=groups,
    )


def _validate_universe(states: tuple[CandidateState, ...], artifact: ModelBArtifact) -> None:
    if not states:
        raise ValueError("candidate universe cannot be empty")
    if artifact.model_id != MODEL_B_ID or artifact.base_model_id != MODEL_A_ID:
        raise ValueError("artifact must declare frozen Model B over frozen Model A")
    state_ids = [state.state_id for state in states]
    if len(state_ids) != len(set(state_ids)):
        raise ValueError("candidate state IDs must be unique")
    for state in states:
        for field, moment in (("start_utc", state.start_utc), ("end_utc", state.end_utc)):
            if moment.tzinfo is None or moment.utcoffset() is None:
                raise ValueError(f"candidate {field} must be timezone-aware UTC")
            if moment.utcoffset() != timedelta(0):
                raise ValueError(f"candidate {field} must have UTC offset zero")
    for previous, current in zip(states, states[1:], strict=False):
        if previous.end_utc != current.start_utc:
            raise ValueError("candidate universe must be one contiguous exact partition")


def _duration_microseconds(state: CandidateState) -> int:
    delta = state.end_utc - state.start_utc
    return ((delta.days * 86_400) + delta.seconds) * 1_000_000 + delta.microseconds
