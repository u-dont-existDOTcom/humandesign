"""Pure synthetic validators for pre-inference role and reference separation.

This module validates protocol structure only. It contains no participant
inference, chart semantics, questionnaire content, or operating thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DataRole(StrEnum):
    DEVELOPMENT = "development"
    CALIBRATION = "calibration"
    LOCKED_VALIDATION = "locked_validation"


class ReferenceActor(StrEnum):
    CANDIDATE_CONSTRUCTOR = "candidate_constructor"
    MEASUREMENT_DEVELOPER = "measurement_developer"
    MODEL_DEVELOPER = "model_developer"
    INFERENCE_PROCEDURE = "inference_procedure"
    REFERENCE_CUSTODIAN = "reference_custodian"
    INDEPENDENT_CALIBRATION_EVALUATOR = "independent_calibration_evaluator"
    INDEPENDENT_VALIDATION_EVALUATOR = "independent_validation_evaluator"


class ReferencePurpose(StrEnum):
    REFERENCE_CUSTODY = "reference_custody"
    CANDIDATE_CONSTRUCTION = "candidate_construction"
    MEASUREMENT_DEVELOPMENT = "measurement_development"
    MODEL_FITTING = "model_fitting"
    PROCEDURE_EXECUTION = "procedure_execution"
    STOPPING = "stopping"
    RETURNED_SET_CONSTRUCTION = "returned_set_construction"
    POST_FREEZE_CALIBRATION_COMPARISON = "post_freeze_calibration_comparison"
    POST_FREEZE_VALIDATION_COMPARISON = "post_freeze_validation_comparison"


@dataclass(frozen=True, slots=True)
class RoleAssignment:
    observation_id: str
    participant_id: str
    role: DataRole
    alias_keys: tuple[str, ...] = ()
    household_keys: tuple[str, ...] = ()
    relationship_keys: tuple[str, ...] = ()
    shared_record_source_keys: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ReferenceAccessEvent:
    participant_id: str
    actor: ReferenceActor
    purpose: ReferencePurpose
    method_frozen: bool
    output_frozen: bool


@dataclass(frozen=True, slots=True)
class ContaminationEvent:
    role: DataRole
    methodology_changed_after_outcome_access: bool = False
    relationship_evidence_used_for_natal_inference: bool = False


_EDGE_VIOLATION_CODES = {
    "same_participant": "cross_role_same_participant",
    "alias": "cross_role_alias",
    "household": "cross_role_household",
    "relationship": "cross_role_relationship",
    "shared_record_source": "cross_role_shared_record_source",
}


def _shared(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    return bool(set(left).intersection(right))


def _edge_reasons(left: RoleAssignment, right: RoleAssignment) -> tuple[str, ...]:
    reasons: list[str] = []
    if left.participant_id == right.participant_id:
        reasons.append("same_participant")
    if _shared(left.alias_keys, right.alias_keys):
        reasons.append("alias")
    if _shared(left.household_keys, right.household_keys):
        reasons.append("household")
    if _shared(left.relationship_keys, right.relationship_keys):
        reasons.append("relationship")
    if _shared(left.shared_record_source_keys, right.shared_record_source_keys):
        reasons.append("shared_record_source")
    return tuple(reasons)


def connected_component_violations(
    assignments: tuple[RoleAssignment, ...],
) -> tuple[str, ...]:
    """Detect any identity/relationship/source component assigned across roles."""

    observation_ids = [assignment.observation_id for assignment in assignments]
    if len(set(observation_ids)) != len(observation_ids):
        raise ValueError("observation_id values must be unique")

    adjacency: list[set[int]] = [set() for _ in assignments]
    edge_reasons: dict[tuple[int, int], tuple[str, ...]] = {}
    for left_index, left in enumerate(assignments):
        for right_index in range(left_index + 1, len(assignments)):
            reasons = _edge_reasons(left, assignments[right_index])
            if not reasons:
                continue
            adjacency[left_index].add(right_index)
            adjacency[right_index].add(left_index)
            edge_reasons[(left_index, right_index)] = reasons

    violations: set[str] = set()
    unseen = set(range(len(assignments)))
    while unseen:
        root = min(unseen)
        component: set[int] = set()
        pending = [root]
        while pending:
            current = pending.pop()
            if current in component:
                continue
            component.add(current)
            unseen.discard(current)
            pending.extend(adjacency[current] - component)

        roles = {assignments[index].role for index in component}
        if len(roles) <= 1:
            continue
        for (left_index, right_index), reasons in edge_reasons.items():
            if left_index in component and right_index in component:
                violations.update(_EDGE_VIOLATION_CODES[reason] for reason in reasons)

    return tuple(sorted(violations))


def reference_access_violations(events: tuple[ReferenceAccessEvent, ...]) -> tuple[str, ...]:
    """Allow T_i only for post-freeze independent calibration/validation comparison."""

    violations: set[str] = set()
    for event in events:
        if event.actor is ReferenceActor.REFERENCE_CUSTODIAN:
            if event.purpose is not ReferencePurpose.REFERENCE_CUSTODY:
                violations.add("reference_leakage")
            continue
        if event.actor is ReferenceActor.INDEPENDENT_CALIBRATION_EVALUATOR:
            if event.purpose is not ReferencePurpose.POST_FREEZE_CALIBRATION_COMPARISON:
                violations.add("reference_leakage")
                continue
            if not event.method_frozen:
                violations.add("calibration_method_not_frozen")
            if not event.output_frozen:
                violations.add("calibration_output_not_frozen")
            continue
        if event.actor is ReferenceActor.INDEPENDENT_VALIDATION_EVALUATOR:
            if event.purpose is not ReferencePurpose.POST_FREEZE_VALIDATION_COMPARISON:
                violations.add("reference_leakage")
                continue
            if not event.method_frozen:
                violations.add("validation_method_not_frozen")
            if not event.output_frozen:
                violations.add("validation_output_not_frozen")
            continue
        violations.add("reference_leakage")
    return tuple(sorted(violations))


def reference_assignment_violations(
    assignments: tuple[RoleAssignment, ...], events: tuple[ReferenceAccessEvent, ...]
) -> tuple[str, ...]:
    """Require evaluator comparison events to match the participant's assigned role."""

    roles_by_participant: dict[str, set[DataRole]] = {}
    for assignment in assignments:
        roles_by_participant.setdefault(assignment.participant_id, set()).add(assignment.role)

    violations: set[str] = set()
    for event in events:
        roles = roles_by_participant.get(event.participant_id)
        if roles is None:
            violations.add("reference_event_unknown_participant")
            continue
        if (
            event.actor is ReferenceActor.INDEPENDENT_CALIBRATION_EVALUATOR
            and roles != {DataRole.CALIBRATION}
        ):
            violations.add("reference_role_mismatch")
        if (
            event.actor is ReferenceActor.INDEPENDENT_VALIDATION_EVALUATOR
            and roles != {DataRole.LOCKED_VALIDATION}
        ):
            violations.add("reference_role_mismatch")
    return tuple(sorted(violations))


def contamination_violations(events: tuple[ContaminationEvent, ...]) -> tuple[str, ...]:
    """Detect outcome-driven adaptation and relationship-assisted natal inference."""

    violations: set[str] = set()
    for event in events:
        if event.relationship_evidence_used_for_natal_inference:
            violations.add("relationship_evidence_assisted_inference")
        if not event.methodology_changed_after_outcome_access:
            continue
        if event.role is DataRole.CALIBRATION:
            violations.add("calibration_became_development")
        elif event.role is DataRole.LOCKED_VALIDATION:
            violations.add("validation_became_development")
    return tuple(sorted(violations))


def validate_synthetic_case(
    assignments: tuple[RoleAssignment, ...],
    reference_events: tuple[ReferenceAccessEvent, ...] = (),
    contamination_events: tuple[ContaminationEvent, ...] = (),
) -> tuple[str, ...]:
    """Return stable violation codes for a fully structured synthetic case."""

    return tuple(
        sorted(
            {
                *connected_component_violations(assignments),
                *reference_access_violations(reference_events),
                *reference_assignment_violations(assignments, reference_events),
                *contamination_violations(contamination_events),
            }
        )
    )
