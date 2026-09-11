"""Mechanical response graph for the accepted Life Patterns facet/relation contract v5.

This module is intentionally theory-neutral. It implements the record containment,
referential-integrity, stage-local cardinality, hybrid-component, absence-gate, provenance,
and anti-double-counting rules that passed the independent blind v5 contract review.
Historical Structured Annotation V2 models remain immutable.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Annotated, Any, Callable, Literal, Mapping, TypeVar, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

ResponseState = Literal["observed", "insufficient", "not_applicable"]
Cardinality = Literal["zero_or_one", "zero_one_or_multiple"]
WindowKind = Literal[
    "action_window",
    "preselection_search_opportunity",
    "preaction_window",
    "transition_observation_window",
    "allocation_interval",
    "checking_opportunity_window",
    "endpoint_assessment_window",
    "goal_followup_window",
    "preprompt_request_opportunity",
    "request_opportunity_window",
    "offer_use_window",
    "communication_opportunity_window",
    "preconsequence_communication_window",
    "remedial_response_window",
    "repeated_position_exchange_window",
    "resumed_contact_discussion_window",
    "repair_opportunity_window",
    "repair_trajectory_window",
]
SpecificityDisposition = Literal[
    "direct",
    "narrow_replaces_broad",
    "component_of_ordered_trajectory",
    "cross_facet_copresence",
    "derived_not_countable",
]
ComponentRole = Literal["affirmative", "absence"]
GateStatus = Literal["established", "not_established", "unclear"]
IndependenceClass = Literal[
    "single_bounded_behavioral_occurrence",
    "derived_status_of_same_occurrence",
    "repeated_series_self_report",
    "sampled_opportunity",
    "external_record_occurrence",
]
TemporalRelation = Literal["before", "immediately_before"]

V5_CONTRACT_SCHEMA_VERSION = "life-patterns-facet-relation-contract-v5-candidate"
V5_CONTRACT_VERSION = "5.0.0-candidate"
V5_REVIEW_COMMIT = "ce04642146c41a7d5d94f85360572c78de887682"
V5_REPAIR_COMMIT = "320cb577f4adfbcc644c986f7f532feef0fbe80b"

# These are the non-hybrid absence-dependent values carried by the theory-blind
# non-action classification plus the v2 R07-a split. Each requires a separately
# represented absence component and four-part gate when selected. Hybrid values
# are read from the accepted contract at runtime because that mapping is already
# normative there.
V5_NON_HYBRID_ABSENCE_DEPENDENT_VALUE_IDS = frozenset(
    {
        "R01-h",
        "R03-h",
        "R05-R8",
        "R07-a2",
        "R08-c",
        "R08-f",
        "R10-k",
        "R11-G7",
        "R13-g",
        "R14-i",
        "R15-l",
        "R16-l",
        "R17-h",
        "R19-f",
        "R21-k",
        "R22-g",
    }
)


class V5Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class EventStageScope(V5Model):
    scope_type: Literal["event_stage"] = "event_stage"
    event_stage_id: str = Field(min_length=1)


class MeasurementWindowScope(V5Model):
    scope_type: Literal["measurement_window"] = "measurement_window"
    window_id: str = Field(min_length=1)


CardinalityScope = Annotated[
    EventStageScope | MeasurementWindowScope,
    Field(discriminator="scope_type"),
]


class FacetGroupV5(V5Model):
    facet_group_id: str = Field(min_length=1)
    facet_id: str = Field(min_length=1)
    state: ResponseState
    cardinality: Cardinality
    cardinality_scope: CardinalityScope
    allowed_value_ids: tuple[str, ...]
    assertion_ids: tuple[str, ...] = ()

    @model_validator(mode="after")
    def state_and_assertions(self) -> FacetGroupV5:
        if len(self.allowed_value_ids) != len(set(self.allowed_value_ids)):
            raise ValueError("facet group repeats an allowed value id")
        if len(self.assertion_ids) != len(set(self.assertion_ids)):
            raise ValueError("facet group repeats an assertion id")
        if self.state == "observed" and not self.assertion_ids:
            raise ValueError("observed facet group requires at least one value assertion")
        if self.state != "observed" and self.assertion_ids:
            raise ValueError("insufficient/not-applicable facet group cannot contain value assertions")
        if self.cardinality == "zero_or_one" and len(self.assertion_ids) > 1:
            raise ValueError("zero_or_one facet group contains more than one value assertion")
        return self


class MeasurementWindowV5(V5Model):
    window_id: str = Field(min_length=1)
    window_kind: WindowKind
    event_stage_ids: tuple[str, ...] = ()
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)


class EventStageV5(V5Model):
    event_stage_id: str = Field(min_length=1)
    state: ResponseState
    evidence_unit_id: str = Field(min_length=1)
    assertion_ids: tuple[str, ...] = ()
    component_assertion_ids: tuple[str, ...] = ()
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def state_and_assertions(self) -> EventStageV5:
        if self.state != "observed" and self.assertion_ids:
            raise ValueError("insufficient/not-applicable event stage cannot contain value assertions")
        return self


class ValueAssertionV5(V5Model):
    assertion_id: str = Field(min_length=1)
    value_id: str = Field(min_length=1)
    facet_id: str = Field(min_length=1)
    facet_group_id: str = Field(min_length=1)
    event_stage_id: str = Field(min_length=1)
    evidence_unit_id: str = Field(min_length=1)
    component_assertion_ids: tuple[str, ...] = ()
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)
    specificity_disposition: SpecificityDisposition = "direct"


class ComponentAssertionV5(V5Model):
    component_assertion_id: str = Field(min_length=1)
    parent_value_id: str = Field(min_length=1)
    facet_id: str = Field(min_length=1)
    facet_group_id: str = Field(min_length=1)
    event_stage_id: str = Field(min_length=1)
    evidence_unit_id: str = Field(min_length=1)
    component_role: ComponentRole
    state: ResponseState
    proposition: str = Field(min_length=1)
    source_provenance_ids: tuple[str, ...] = ()
    absence_condition_id: str | None = None

    @model_validator(mode="after")
    def role_and_absence_condition(self) -> ComponentAssertionV5:
        if self.component_role == "affirmative" and self.absence_condition_id is not None:
            raise ValueError("affirmative component cannot carry an absence condition")
        if self.component_role == "absence" and self.absence_condition_id is None:
            raise ValueError("absence component requires an absence condition")
        if self.state == "observed" and not self.source_provenance_ids:
            raise ValueError("observed component requires exact source provenance")
        return self


class AbsenceConditionV5(V5Model):
    absence_condition_id: str = Field(min_length=1)
    qualified_assertion_id: str | None = None
    qualified_component_id: str = Field(min_length=1)
    absent_actor: str = Field(min_length=1)
    absent_proposition_id: str = Field(min_length=1)
    absent_proposition: str = Field(min_length=1)
    window_id: str = Field(min_length=1)
    awareness: GateStatus
    opportunity: GateStatus
    feasibility: GateStatus
    established_nonoccurrence: GateStatus
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)

    @property
    def all_established(self) -> bool:
        return all(
            value == "established"
            for value in (
                self.awareness,
                self.opportunity,
                self.feasibility,
                self.established_nonoccurrence,
            )
        )


class SourceProvenanceV5(V5Model):
    source_provenance_id: str = Field(min_length=1)
    source_record_id: str = Field(min_length=1)
    locator: str | dict[str, Any]
    exact_segment_hash: str | None = None
    exact_text_available: bool | None = None


class EvidenceUnitV5(V5Model):
    evidence_unit_id: str = Field(min_length=1)
    response_scope_id: str = Field(min_length=1)
    event_stage_ids: tuple[str, ...] = Field(min_length=1)
    independence_class: IndependenceClass


class TemporalEdgeV5(V5Model):
    from_event_stage_id: str = Field(min_length=1)
    to_event_stage_id: str = Field(min_length=1)
    relation: TemporalRelation
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def no_self_edge(self) -> TemporalEdgeV5:
        if self.from_event_stage_id == self.to_event_stage_id:
            raise ValueError("temporal edge cannot point from a stage to itself")
        return self


class ObservableResponseV5(V5Model):
    schema_version: Literal["life-patterns-observable-response-v5"] = (
        "life-patterns-observable-response-v5"
    )
    response_id: str = Field(min_length=1)
    observable_id: str = Field(min_length=1)
    response_scope_id: str = Field(min_length=1)
    state: ResponseState
    facet_groups: tuple[FacetGroupV5, ...] = ()
    value_assertions: tuple[ValueAssertionV5, ...] = ()
    component_assertions: tuple[ComponentAssertionV5, ...] = ()
    absence_conditions: tuple[AbsenceConditionV5, ...] = ()
    source_provenance_records: tuple[SourceProvenanceV5, ...] = ()
    measurement_windows: tuple[MeasurementWindowV5, ...] = ()
    event_stages: tuple[EventStageV5, ...] = ()
    temporal_edges: tuple[TemporalEdgeV5, ...] = ()
    evidence_units: tuple[EvidenceUnitV5, ...] = ()
    development_only: Literal[True] = True
    validation_use_forbidden: Literal[True] = True

    @model_validator(mode="after")
    def response_state_is_coherent(self) -> ObservableResponseV5:
        if self.state == "observed" and not any(
            group.state == "observed" for group in self.facet_groups
        ):
            raise ValueError("observed response requires at least one observed facet group")
        if self.state != "observed" and self.value_assertions:
            raise ValueError("insufficient/not-applicable response cannot contain value assertions")
        return self


def load_facet_relation_contract_v5(path: str | Path) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Life Patterns facet/relation contract must be a JSON object")
    value = cast(dict[str, Any], raw)
    if value.get("schema_version") != V5_CONTRACT_SCHEMA_VERSION:
        raise ValueError("unexpected Life Patterns facet/relation contract schema")
    if value.get("contract_version") != V5_CONTRACT_VERSION:
        raise ValueError("unexpected Life Patterns facet/relation contract version")
    authority = value.get("authority") or {}
    if not isinstance(authority, Mapping) or authority.get("independent_v4_re_review_commit") != (
        "f5f02c976b11fbabc7c136f9c80fbd312600d91d"
    ):
        raise ValueError("v5 contract does not bind the accepted v4 blind re-review")
    status = value.get("status") or {}
    if not isinstance(status, Mapping) or status.get("target_theory_information_used") is not False:
        raise ValueError("v5 contract is not target-theory blind")
    return value


def project_facet_relation_contract_v5_path() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "state"
        / "LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json"
    )


def load_project_facet_relation_contract_v5() -> dict[str, Any]:
    return load_facet_relation_contract_v5(project_facet_relation_contract_v5_path())


_RecordT = TypeVar("_RecordT")


def _unique_ids(
    records: tuple[_RecordT, ...],
    id_getter: Callable[[_RecordT], str],
    label: str,
    errors: list[str],
) -> dict[str, _RecordT]:
    values = [id_getter(record) for record in records]
    duplicates = sorted(key for key, count in Counter(values).items() if count > 1)
    if duplicates:
        errors.append(f"{label} contains duplicate ids: {', '.join(duplicates)}")
    return {id_getter(record): record for record in records}


def _require(
    ref: str,
    mapping: Mapping[str, _RecordT],
    context: str,
    errors: list[str],
) -> _RecordT | None:
    value = mapping.get(ref)
    if value is None:
        errors.append(f"{context} references unknown id {ref}")
    return value


def _require_many(
    refs: tuple[str, ...],
    mapping: Mapping[str, _RecordT],
    context: str,
    errors: list[str],
) -> None:
    if len(refs) != len(set(refs)):
        errors.append(f"{context} repeats an id")
    for ref in refs:
        _require(ref, mapping, context, errors)


def _scope_key(scope: CardinalityScope) -> tuple[str, str]:
    if isinstance(scope, EventStageScope):
        return ("event_stage", scope.event_stage_id)
    return ("measurement_window", scope.window_id)


def _observable_profile(contract: Mapping[str, Any], observable_id: str) -> Mapping[str, Any]:
    profiles = contract.get("observable_facet_profiles") or {}
    if isinstance(profiles, Mapping):
        profile = profiles.get(observable_id)
        if isinstance(profile, Mapping):
            return cast(Mapping[str, Any], profile)
    default = contract.get("default_observable_profile") or {}
    if isinstance(default, Mapping):
        return cast(Mapping[str, Any], default)
    return {}


def _find_facet_spec(profile: Mapping[str, Any], facet_id: str) -> Mapping[str, Any] | None:
    facets = profile.get("facets") or {}
    if not isinstance(facets, Mapping):
        return None
    value = facets.get(facet_id)
    return cast(Mapping[str, Any], value) if isinstance(value, Mapping) else None


def _check_acyclic(edges: tuple[TemporalEdgeV5, ...]) -> bool:
    graph: dict[str, set[str]] = defaultdict(set)
    nodes: set[str] = set()
    for edge in edges:
        graph[edge.from_event_stage_id].add(edge.to_event_stage_id)
        nodes.add(edge.from_event_stage_id)
        nodes.add(edge.to_event_stage_id)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return False
        if node in visited:
            return True
        visiting.add(node)
        for child in graph.get(node, ()):
            if not visit(child):
                return False
        visiting.remove(node)
        visited.add(node)
        return True

    return all(visit(node) for node in nodes)


def observable_response_v5_errors(
    response: ObservableResponseV5,
    *,
    contract: Mapping[str, Any],
    valid_source_record_ids: set[str] | None = None,
) -> tuple[str, ...]:
    """Return deterministic contract violations for one v5 observable response graph."""

    errors: list[str] = []
    if contract.get("schema_version") != V5_CONTRACT_SCHEMA_VERSION:
        return ("response validator received the wrong facet/relation contract",)

    groups = _unique_ids(response.facet_groups, lambda row: row.facet_group_id, "facet_groups", errors)
    assertions = _unique_ids(
        response.value_assertions, lambda row: row.assertion_id, "value_assertions", errors
    )
    components = _unique_ids(
        response.component_assertions,
        lambda row: row.component_assertion_id,
        "component_assertions",
        errors,
    )
    absences = _unique_ids(
        response.absence_conditions,
        lambda row: row.absence_condition_id,
        "absence_conditions",
        errors,
    )
    provenance = _unique_ids(
        response.source_provenance_records,
        lambda row: row.source_provenance_id,
        "source_provenance_records",
        errors,
    )
    windows = _unique_ids(
        response.measurement_windows, lambda row: row.window_id, "measurement_windows", errors
    )
    stages = _unique_ids(response.event_stages, lambda row: row.event_stage_id, "event_stages", errors)
    evidence = _unique_ids(
        response.evidence_units, lambda row: row.evidence_unit_id, "evidence_units", errors
    )

    for source in response.source_provenance_records:
        if valid_source_record_ids is not None and source.source_record_id not in valid_source_record_ids:
            errors.append(
                f"source provenance {source.source_provenance_id} cites source outside supplied task"
            )

    stage_to_units: Counter[str] = Counter()
    for evidence_unit in response.evidence_units:
        if evidence_unit.response_scope_id != response.response_scope_id:
            errors.append(f"evidence unit {evidence_unit.evidence_unit_id} has the wrong response_scope_id")
        _require_many(
            evidence_unit.event_stage_ids,
            stages,
            f"evidence unit {evidence_unit.evidence_unit_id}",
            errors,
        )
        for stage_id in evidence_unit.event_stage_ids:
            stage_to_units[stage_id] += 1

    assertion_stage_backrefs: Counter[str] = Counter()
    component_stage_backrefs: Counter[str] = Counter()
    for stage in response.event_stages:
        _require(stage.evidence_unit_id, evidence, f"event stage {stage.event_stage_id}", errors)
        _require_many(stage.assertion_ids, assertions, f"event stage {stage.event_stage_id}", errors)
        _require_many(
            stage.component_assertion_ids,
            components,
            f"event stage {stage.event_stage_id}",
            errors,
        )
        _require_many(
            stage.source_provenance_ids,
            provenance,
            f"event stage {stage.event_stage_id}",
            errors,
        )
        for assertion_id in stage.assertion_ids:
            assertion_stage_backrefs[assertion_id] += 1
        for component_id in stage.component_assertion_ids:
            component_stage_backrefs[component_id] += 1
        stage_evidence = evidence.get(stage.evidence_unit_id)
        if stage_evidence is not None and stage.event_stage_id not in stage_evidence.event_stage_ids:
            errors.append(
                f"event stage {stage.event_stage_id} is not back-referenced by evidence unit "
                f"{stage.evidence_unit_id}"
            )
        if stage_to_units[stage.event_stage_id] != 1:
            errors.append(f"event stage {stage.event_stage_id} must occur in exactly one evidence unit")

    for window in response.measurement_windows:
        _require_many(window.event_stage_ids, stages, f"measurement window {window.window_id}", errors)
        _require_many(
            window.source_provenance_ids,
            provenance,
            f"measurement window {window.window_id}",
            errors,
        )

    profile = _observable_profile(contract, response.observable_id)
    group_scope_keys: set[tuple[str, tuple[str, str]]] = set()
    assertion_group_backrefs: Counter[str] = Counter()
    for group in response.facet_groups:
        key = (group.facet_id, _scope_key(group.cardinality_scope))
        if key in group_scope_keys:
            errors.append(
                f"facet {group.facet_id} repeats the same cardinality scope "
                f"{_scope_key(group.cardinality_scope)}"
            )
        group_scope_keys.add(key)
        _require_many(group.assertion_ids, assertions, f"facet group {group.facet_group_id}", errors)
        for assertion_id in group.assertion_ids:
            assertion_group_backrefs[assertion_id] += 1

        spec = _find_facet_spec(profile, group.facet_id)
        if spec is None:
            errors.append(
                f"facet group {group.facet_group_id} uses facet {group.facet_id} outside observable profile"
            )
        else:
            if group.cardinality != spec.get("cardinality"):
                errors.append(f"facet group {group.facet_group_id} has wrong cardinality")
            scope_spec = spec.get("cardinality_scope") or {}
            expected_scope = scope_spec.get("scope_type") if isinstance(scope_spec, Mapping) else None
            if group.cardinality_scope.scope_type != expected_scope:
                errors.append(f"facet group {group.facet_group_id} has wrong cardinality scope type")
            explicit_values = spec.get("value_ids")
            if isinstance(explicit_values, list) and set(group.allowed_value_ids) != set(explicit_values):
                errors.append(f"facet group {group.facet_group_id} allowed values disagree with profile")
            if isinstance(group.cardinality_scope, MeasurementWindowScope):
                scope_window = _require(
                    group.cardinality_scope.window_id,
                    windows,
                    f"facet group {group.facet_group_id}",
                    errors,
                )
                expected_kind = scope_spec.get("window_kind") if isinstance(scope_spec, Mapping) else None
                if scope_window is not None and expected_kind and scope_window.window_kind != expected_kind:
                    errors.append(
                        f"facet group {group.facet_group_id} uses wrong measurement-window kind"
                    )
            else:
                _require(
                    group.cardinality_scope.event_stage_id,
                    stages,
                    f"facet group {group.facet_group_id}",
                    errors,
                )

        for assertion_id in group.assertion_ids:
            assertion_ref = assertions.get(assertion_id)
            if assertion_ref is None:
                continue
            if (
                assertion_ref.facet_group_id != group.facet_group_id
                or assertion_ref.facet_id != group.facet_id
            ):
                errors.append(f"assertion {assertion_id} disagrees with its facet group")
            if assertion_ref.value_id not in group.allowed_value_ids:
                errors.append(f"assertion {assertion_id} uses value outside its facet group")
            if isinstance(group.cardinality_scope, EventStageScope):
                if assertion_ref.event_stage_id != group.cardinality_scope.event_stage_id:
                    errors.append(
                        f"assertion {assertion_id} is outside its event-stage cardinality scope"
                    )
            else:
                membership_window = windows.get(group.cardinality_scope.window_id)
                if (
                    membership_window is not None
                    and assertion_ref.event_stage_id not in membership_window.event_stage_ids
                ):
                    errors.append(
                        f"assertion {assertion_id} is outside its measurement-window scope"
                    )

    component_parent_backrefs: Counter[str] = Counter()
    selected_parent_by_component: dict[str, str] = {}
    for assertion in response.value_assertions:
        group_ref = _require(
            assertion.facet_group_id,
            groups,
            f"assertion {assertion.assertion_id}",
            errors,
        )
        stage_ref = _require(
            assertion.event_stage_id,
            stages,
            f"assertion {assertion.assertion_id}",
            errors,
        )
        _require(assertion.evidence_unit_id, evidence, f"assertion {assertion.assertion_id}", errors)
        _require_many(
            assertion.component_assertion_ids,
            components,
            f"assertion {assertion.assertion_id}",
            errors,
        )
        _require_many(
            assertion.source_provenance_ids,
            provenance,
            f"assertion {assertion.assertion_id}",
            errors,
        )
        for component_id in assertion.component_assertion_ids:
            component_parent_backrefs[component_id] += 1
            selected_parent_by_component.setdefault(component_id, assertion.assertion_id)
        if assertion_group_backrefs[assertion.assertion_id] != 1:
            errors.append(f"assertion {assertion.assertion_id} must occur in exactly one facet group")
        if assertion_stage_backrefs[assertion.assertion_id] != 1:
            errors.append(f"assertion {assertion.assertion_id} must occur in exactly one event stage")
        if group_ref is not None and (
            group_ref.facet_id != assertion.facet_id
            or assertion.value_id not in group_ref.allowed_value_ids
        ):
            errors.append(f"assertion {assertion.assertion_id} does not match its facet group")
        if stage_ref is not None and stage_ref.evidence_unit_id != assertion.evidence_unit_id:
            errors.append(f"assertion {assertion.assertion_id} evidence unit disagrees with event stage")

    hybrid_values_raw = contract.get("hybrid_value_components") or {}
    hybrid_values = set(hybrid_values_raw) if isinstance(hybrid_values_raw, Mapping) else set()
    absence_dependent_values = hybrid_values | set(V5_NON_HYBRID_ABSENCE_DEPENDENT_VALUE_IDS)
    absence_by_component: Counter[str] = Counter()
    for component in response.component_assertions:
        component_group = _require(
            component.facet_group_id,
            groups,
            f"component {component.component_assertion_id}",
            errors,
        )
        component_stage = _require(
            component.event_stage_id,
            stages,
            f"component {component.component_assertion_id}",
            errors,
        )
        _require(
            component.evidence_unit_id,
            evidence,
            f"component {component.component_assertion_id}",
            errors,
        )
        _require_many(
            component.source_provenance_ids,
            provenance,
            f"component {component.component_assertion_id}",
            errors,
        )
        if component_stage_backrefs[component.component_assertion_id] != 1:
            errors.append(
                f"component {component.component_assertion_id} must occur in exactly one event stage"
            )
        if component_parent_backrefs[component.component_assertion_id] > 1:
            errors.append(
                f"component {component.component_assertion_id} belongs to more than one parent assertion"
            )
        if component_group is not None:
            if component_group.facet_id != component.facet_id:
                errors.append(f"component {component.component_assertion_id} has wrong facet id")
            if component.parent_value_id not in component_group.allowed_value_ids:
                errors.append(
                    f"component {component.component_assertion_id} parent value is outside facet"
                )
        if (
            component_stage is not None
            and component_stage.evidence_unit_id != component.evidence_unit_id
        ):
            errors.append(
                f"component {component.component_assertion_id} evidence unit disagrees with event stage"
            )
        if component.component_role == "affirmative" and component.parent_value_id not in hybrid_values:
            errors.append(
                f"affirmative component {component.component_assertion_id} refers to non-hybrid parent "
                f"{component.parent_value_id}"
            )
        if component.component_role == "absence" and component.parent_value_id not in absence_dependent_values:
            errors.append(
                f"absence component {component.component_assertion_id} refers to value without an absence dependency "
                f"{component.parent_value_id}"
            )
        if component.component_role == "absence" and component.absence_condition_id:
            condition_ref = _require(
                component.absence_condition_id,
                absences,
                f"component {component.component_assertion_id}",
                errors,
            )
            if condition_ref is not None:
                absence_by_component[component.component_assertion_id] += 1
                if condition_ref.qualified_component_id != component.component_assertion_id:
                    errors.append(
                        f"absence condition {condition_ref.absence_condition_id} points to a different component"
                    )
                if component.state == "observed" and not condition_ref.all_established:
                    errors.append(
                        f"observed absence component {component.component_assertion_id} lacks a fully established gate"
                    )
                if condition_ref.all_established and component.state != "observed":
                    errors.append(
                        f"fully established absence condition {condition_ref.absence_condition_id} "
                        "has a non-observed component"
                    )

    for condition in response.absence_conditions:
        component_ref = _require(
            condition.qualified_component_id,
            components,
            f"absence condition {condition.absence_condition_id}",
            errors,
        )
        _require(
            condition.window_id,
            windows,
            f"absence condition {condition.absence_condition_id}",
            errors,
        )
        _require_many(
            condition.source_provenance_ids,
            provenance,
            f"absence condition {condition.absence_condition_id}",
            errors,
        )
        if component_ref is not None:
            if component_ref.component_role != "absence":
                errors.append(
                    f"absence condition {condition.absence_condition_id} qualifies a non-absence component"
                )
            if component_ref.absence_condition_id != condition.absence_condition_id:
                errors.append(
                    f"absence condition {condition.absence_condition_id} lacks component back-reference"
                )

        selected_parent_id = selected_parent_by_component.get(condition.qualified_component_id)
        if selected_parent_id is None:
            if condition.qualified_assertion_id is not None:
                errors.append(
                    f"absence condition {condition.absence_condition_id} names a parent assertion "
                    "when its component has no selected parent"
                )
        elif condition.qualified_assertion_id != selected_parent_id:
            errors.append(
                f"absence condition {condition.absence_condition_id} must name its selected parent assertion"
            )

        if condition.qualified_assertion_id is not None:
            parent_ref = _require(
                condition.qualified_assertion_id,
                assertions,
                f"absence condition {condition.absence_condition_id}",
                errors,
            )
            if parent_ref is not None and component_ref is not None:
                if component_ref.component_assertion_id not in parent_ref.component_assertion_ids:
                    errors.append(
                        f"absence condition {condition.absence_condition_id} parent does not contain its component"
                    )
                if (
                    parent_ref.value_id != component_ref.parent_value_id
                    or parent_ref.facet_id != component_ref.facet_id
                    or parent_ref.facet_group_id != component_ref.facet_group_id
                    or parent_ref.event_stage_id != component_ref.event_stage_id
                    or parent_ref.evidence_unit_id != component_ref.evidence_unit_id
                ):
                    errors.append(
                        f"absence condition {condition.absence_condition_id} parent/component bindings disagree"
                    )

    for component in response.component_assertions:
        if (
            component.component_role == "absence"
            and absence_by_component[component.component_assertion_id] != 1
        ):
            errors.append(
                f"absence component {component.component_assertion_id} must resolve to exactly one absence condition"
            )

    for assertion in response.value_assertions:
        children = [components.get(component_id) for component_id in assertion.component_assertion_ids]
        roles = {child.component_role for child in children if child is not None}
        if assertion.value_id in hybrid_values:
            if len(children) != 2 or roles != {"affirmative", "absence"}:
                errors.append(
                    f"hybrid assertion {assertion.assertion_id} must contain one affirmative and one absence component"
                )
        elif assertion.value_id in V5_NON_HYBRID_ABSENCE_DEPENDENT_VALUE_IDS:
            if len(children) != 1 or roles != {"absence"}:
                errors.append(
                    f"absence-dependent assertion {assertion.assertion_id} must contain exactly one absence component"
                )
        elif assertion.component_assertion_ids:
            errors.append(
                f"non-component assertion {assertion.assertion_id} cannot contain component assertions"
            )

        if assertion.value_id in absence_dependent_values:
            for child in children:
                if child is None:
                    continue
                if child.state != "observed":
                    errors.append(
                        f"selected absence-dependent assertion {assertion.assertion_id} contains non-observed component"
                    )
                if (
                    child.parent_value_id != assertion.value_id
                    or child.facet_id != assertion.facet_id
                    or child.facet_group_id != assertion.facet_group_id
                    or child.event_stage_id != assertion.event_stage_id
                    or child.evidence_unit_id != assertion.evidence_unit_id
                ):
                    errors.append(
                        f"absence-dependent assertion {assertion.assertion_id} component bindings disagree"
                    )

    duplicate_fact_keys: Counter[tuple[str, str, str]] = Counter(
        (row.facet_id, row.value_id, row.event_stage_id) for row in response.value_assertions
    )
    if any(count > 1 for count in duplicate_fact_keys.values()):
        errors.append("same sourced facet fact is duplicated across value assertions")

    for edge in response.temporal_edges:
        _require(edge.from_event_stage_id, stages, "temporal edge", errors)
        _require(edge.to_event_stage_id, stages, "temporal edge", errors)
        _require_many(edge.source_provenance_ids, provenance, "temporal edge", errors)
    if not _check_acyclic(response.temporal_edges):
        errors.append("temporal edges must form an acyclic partial order")

    return tuple(dict.fromkeys(errors))


def assert_valid_observable_response_v5(
    response: ObservableResponseV5,
    *,
    contract: Mapping[str, Any],
    valid_source_record_ids: set[str] | None = None,
) -> None:
    errors = observable_response_v5_errors(
        response,
        contract=contract,
        valid_source_record_ids=valid_source_record_ids,
    )
    if errors:
        raise ValueError("invalid Life Patterns v5 response: " + "; ".join(errors))
