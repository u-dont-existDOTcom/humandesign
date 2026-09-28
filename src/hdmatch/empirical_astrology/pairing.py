"""Outcome-blind deterministic selection for the frozen same-hospital design."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date

from .features import (
    BirthRecord,
    PairFeatures,
    build_pair_features,
    deterministic_pair_id,
    entity_hash,
    pair_eligibility_errors,
)
from .protocol import CohortEntities, ensure_disjoint_cohorts
from .provenance import VerifiedBirthInput


class DesignNotLaunchable(ValueError):
    """Raised when a candidate roster fails a frozen prospective design gate."""


def retain_one_per_relationship_component(
    records: Iterable[BirthRecord],
    *,
    protocol_version: str,
    base_seed: int,
) -> tuple[BirthRecord, ...]:
    """Keep the smallest participant hash in each known relationship component."""

    grouped: dict[str, list[BirthRecord]] = defaultdict(list)
    for record in records:
        grouped[record.relationship_component_id].append(record)
    retained: list[BirthRecord] = []
    for component in sorted(grouped):
        ranked = sorted(
            grouped[component],
            key=lambda record: (
                entity_hash(
                    "participant",
                    record.participant_id,
                    protocol_version=protocol_version,
                    base_seed=base_seed,
                ),
                record.participant_id.encode("utf-8"),
            ),
        )
        retained.append(ranked[0])
    return tuple(sorted(retained, key=lambda record: record.participant_id.encode("utf-8")))


def retain_one_hospital_per_network(
    records: Iterable[BirthRecord],
    *,
    protocol_version: str,
    base_seed: int,
) -> tuple[BirthRecord, ...]:
    """Keep all records from the smallest hashed hospital in each network."""

    by_network: dict[str, list[BirthRecord]] = defaultdict(list)
    for record in records:
        by_network[record.network_id].append(record)
    retained: list[BirthRecord] = []
    for network in sorted(by_network):
        hospitals = {record.hospital_id for record in by_network[network]}
        selected = min(
            hospitals,
            key=lambda hospital: (
                entity_hash(
                    "hospital",
                    hospital,
                    protocol_version=protocol_version,
                    base_seed=base_seed,
                ),
                hospital.encode("utf-8"),
            ),
        )
        retained.extend(record for record in by_network[network] if record.hospital_id == selected)
    return tuple(sorted(retained, key=lambda record: record.participant_id.encode("utf-8")))


def allocate_networks_to_cohorts(
    network_ids: Iterable[str],
    *,
    protocol_version: str,
    base_seed: int,
) -> dict[str, tuple[str, ...]]:
    """Allocate exactly forty eligible networks alternately to cohorts A and B."""

    unique = set(network_ids)
    if len(unique) < 40:
        raise DesignNotLaunchable("fewer than 40 independent eligible networks")
    ranked = sorted(
        unique,
        key=lambda network: (
            entity_hash(
                "network",
                network,
                protocol_version=protocol_version,
                base_seed=base_seed,
            ),
            network.encode("utf-8"),
        ),
    )[:40]
    return {"A": tuple(ranked[0::2]), "B": tuple(ranked[1::2])}


def _eligible_edges(
    records: Sequence[BirthRecord],
    *,
    protocol_version: str,
    base_seed: int,
) -> list[tuple[str, BirthRecord, BirthRecord]]:
    grouped: dict[tuple[object, ...], list[BirthRecord]] = defaultdict(list)
    for record in records:
        grouped[record.matching_stratum].append(record)
    edges: list[tuple[str, BirthRecord, BirthRecord]] = []
    for stratum in sorted(grouped, key=repr):
        members = sorted(grouped[stratum], key=lambda record: record.participant_id.encode())
        for index, left in enumerate(members):
            for right in members[index + 1 :]:
                if pair_eligibility_errors(left, right):
                    continue
                edge_id = deterministic_pair_id(
                    left.participant_id,
                    right.participant_id,
                    protocol_version=protocol_version,
                    base_seed=base_seed,
                )
                edges.append((edge_id, left, right))
    return sorted(
        edges,
        key=lambda edge: (
            edge[0],
            edge[1].participant_id.encode(),
            edge[2].participant_id.encode(),
        ),
    )


def greedy_disjoint_pairs(
    records: Sequence[BirthRecord],
    *,
    protocol_version: str,
    base_seed: int,
) -> tuple[PairFeatures, ...]:
    """Select deterministic disjoint eligible edges before outcomes exist."""

    used: set[str] = set()
    accepted: list[PairFeatures] = []
    for _, left, right in _eligible_edges(
        records,
        protocol_version=protocol_version,
        base_seed=base_seed,
    ):
        if left.participant_id in used or right.participant_id in used:
            continue
        accepted.append(
            build_pair_features(
                left,
                right,
                protocol_version=protocol_version,
                base_seed=base_seed,
            )
        )
        used.update((left.participant_id, right.participant_id))
    return tuple(accepted)


@dataclass(frozen=True, slots=True)
class HospitalPairSelection:
    hospital_id: str
    network_id: str
    selected_pairs: tuple[PairFeatures, ...]
    informative_birth_dates: int
    fraction_gap_at_most_15_minutes: float
    fraction_gap_at_least_60_minutes: float
    launch_gate_errors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CohortPairSelection:
    """Twenty frozen hospitals plus cohort-scoped exposure-support results."""

    cohort_label: str
    hospital_selections: tuple[HospitalPairSelection, ...]
    selected_pairs: tuple[PairFeatures, ...]
    fraction_gap_at_most_15_minutes: float
    fraction_gap_at_least_60_minutes: float
    launch_gate_errors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SelectionExclusion:
    """Outcome-blind roster exclusion retained for the design audit trail."""

    participant_id: str
    reason: str


@dataclass(frozen=True, slots=True)
class ProspectiveDesign:
    """Only integrated path that can satisfy the mechanical selection boundary."""

    cohort_a: CohortPairSelection
    cohort_b: CohortPairSelection
    cohort_a_entities: CohortEntities
    cohort_b_entities: CohortEntities
    exclusions: tuple[SelectionExclusion, ...]
    development_hospital_overlap: tuple[str, ...]
    development_network_overlap: tuple[str, ...]


def select_hospital_pairs(
    records: Sequence[BirthRecord],
    *,
    protocol_version: str,
    base_seed: int,
    strict_prospective_gate: bool = True,
) -> HospitalPairSelection:
    """Apply the frozen within-hospital selection and support audit.

    The function never reselects after a date/support failure.  Setting
    ``strict_prospective_gate=False`` exposes the frozen selection for mechanical
    development diagnostics while retaining all gate errors in the result.
    """

    hospitals = {record.hospital_id for record in records}
    networks = {record.network_id for record in records}
    if len(hospitals) != 1 or len(networks) != 1:
        raise ValueError("select_hospital_pairs requires one hospital in one network")
    accepted = greedy_disjoint_pairs(
        records,
        protocol_version=protocol_version,
        base_seed=base_seed,
    )
    by_date: dict[date, list[PairFeatures]] = defaultdict(list)
    for pair in accepted:
        by_date[pair.local_birth_date].append(pair)
    retained = [
        pair
        for local_date in sorted(by_date)
        if len(by_date[local_date]) >= 2
        for pair in by_date[local_date]
    ]
    selected = tuple(sorted(retained, key=lambda pair: pair.pair_id)[:100])
    date_counts = Counter(pair.local_birth_date for pair in selected)
    informative_dates = sum(count >= 2 for count in date_counts.values())
    total = len(selected)
    low_fraction = sum(pair.center_gap_hours <= 0.25 for pair in selected) / total if total else 0.0
    high_fraction = sum(pair.center_gap_hours >= 1.0 for pair in selected) / total if total else 0.0
    errors: list[str] = []
    if total != 100:
        errors.append("selected_pair_count_not_100")
    if informative_dates < 20:
        errors.append("fewer_than_20_informative_birth_dates")
    if strict_prospective_gate and errors:
        raise DesignNotLaunchable(", ".join(errors))
    return HospitalPairSelection(
        hospital_id=next(iter(hospitals)),
        network_id=next(iter(networks)),
        selected_pairs=selected,
        informative_birth_dates=informative_dates,
        fraction_gap_at_most_15_minutes=low_fraction,
        fraction_gap_at_least_60_minutes=high_fraction,
        launch_gate_errors=tuple(errors),
    )


def validate_cohort_pair_support(
    selections: Sequence[HospitalPairSelection],
    *,
    cohort_label: str,
    strict_prospective_gate: bool = True,
) -> CohortPairSelection:
    """Apply the frozen exposure fractions once per complete cohort.

    The per-hospital gates remain exactly 100 pairs and at least 20 final
    informative dates.  A failed cohort is never repaired by replacing a site.
    """

    if cohort_label not in {"A", "B", "development"}:
        raise ValueError("cohort_label must be A, B, or development")
    frozen = tuple(selections)
    errors: list[str] = []
    if len(frozen) != 20:
        errors.append("hospital_count_not_20")
    hospitals = [selection.hospital_id for selection in frozen]
    networks = [selection.network_id for selection in frozen]
    if len(hospitals) != len(set(hospitals)):
        errors.append("duplicate_hospital")
    if len(networks) != len(set(networks)):
        errors.append("duplicate_network")
    for selection in frozen:
        errors.extend(
            f"{selection.hospital_id}:{reason}" for reason in selection.launch_gate_errors
        )
        if len(selection.selected_pairs) != 100:
            marker = f"{selection.hospital_id}:selected_pair_count_not_100"
            if marker not in errors:
                errors.append(marker)
        if selection.informative_birth_dates < 20:
            marker = f"{selection.hospital_id}:fewer_than_20_informative_birth_dates"
            if marker not in errors:
                errors.append(marker)
    selected = tuple(pair for selection in frozen for pair in selection.selected_pairs)
    total = len(selected)
    low_fraction = sum(pair.center_gap_hours <= 0.25 for pair in selected) / total if total else 0.0
    high_fraction = sum(pair.center_gap_hours >= 1.0 for pair in selected) / total if total else 0.0
    if total != 2000:
        errors.append("selected_pair_count_not_2000")
    if low_fraction < 0.20:
        errors.append("less_than_20_percent_gap_at_most_15_minutes_per_cohort")
    if high_fraction < 0.20:
        errors.append("less_than_20_percent_gap_at_least_60_minutes_per_cohort")
    if strict_prospective_gate and errors:
        raise DesignNotLaunchable(", ".join(errors))
    return CohortPairSelection(
        cohort_label=cohort_label,
        hospital_selections=frozen,
        selected_pairs=selected,
        fraction_gap_at_most_15_minutes=low_fraction,
        fraction_gap_at_least_60_minutes=high_fraction,
        launch_gate_errors=tuple(errors),
    )


def _entities_for_selection(
    selection: CohortPairSelection,
    records_by_participant: dict[str, BirthRecord],
) -> CohortEntities:
    participant_ids = frozenset(
        participant for pair in selection.selected_pairs for participant in pair.participant_ids
    )
    return CohortEntities(
        participant_ids=participant_ids,
        relationship_component_ids=frozenset(
            records_by_participant[participant].relationship_component_id
            for participant in participant_ids
        ),
        hospital_ids=frozenset(pair.hospital_id for pair in selection.selected_pairs),
        network_ids=frozenset(pair.network_id for pair in selection.selected_pairs),
    )


def build_prospective_design(
    verified_inputs: Sequence[VerifiedBirthInput],
    *,
    protocol_version: str,
    base_seed: int,
    development_entities: CohortEntities | None = None,
) -> ProspectiveDesign:
    """Run the mandatory outcome-blind roster-to-pairs design pipeline.

    Low-level helpers remain useful for diagnostics, but a caller cannot obtain a
    ``ProspectiveDesign`` without global relationship retention, hospital/network
    allocation, both cohort support gates, and development/A/B isolation checks.
    """

    inputs = tuple(verified_inputs)
    if not inputs:
        raise DesignNotLaunchable("candidate roster is empty")
    if not all(isinstance(item, VerifiedBirthInput) for item in inputs):
        raise DesignNotLaunchable("candidate roster has not crossed the verified input boundary")
    frozen = tuple(item.record for item in inputs)
    participant_ids = [record.participant_id for record in frozen]
    if len(participant_ids) != len(set(participant_ids)):
        raise DesignNotLaunchable("duplicate or contradictory participant ID")
    hospital_network: dict[str, str] = {}
    for record in frozen:
        previous = hospital_network.setdefault(record.hospital_id, record.network_id)
        if previous != record.network_id:
            raise DesignNotLaunchable("one hospital maps to multiple network IDs")

    exclusions: list[SelectionExclusion] = []
    after_components = retain_one_per_relationship_component(
        frozen,
        protocol_version=protocol_version,
        base_seed=base_seed,
    )
    retained_ids = {record.participant_id for record in after_components}
    exclusions.extend(
        SelectionExclusion(record.participant_id, "relationship_component_retention")
        for record in frozen
        if record.participant_id not in retained_ids
    )
    after_hospitals = retain_one_hospital_per_network(
        after_components,
        protocol_version=protocol_version,
        base_seed=base_seed,
    )
    hospital_ids = {record.participant_id for record in after_hospitals}
    exclusions.extend(
        SelectionExclusion(record.participant_id, "hospital_retention")
        for record in after_components
        if record.participant_id not in hospital_ids
    )

    by_network: dict[str, list[BirthRecord]] = defaultdict(list)
    for record in after_hospitals:
        by_network[record.network_id].append(record)
    eligible: dict[str, HospitalPairSelection] = {}
    for network in sorted(by_network):
        selection = select_hospital_pairs(
            by_network[network],
            protocol_version=protocol_version,
            base_seed=base_seed,
            strict_prospective_gate=False,
        )
        if selection.launch_gate_errors:
            exclusions.extend(
                SelectionExclusion(
                    record.participant_id,
                    "hospital_design_gate:" + ",".join(selection.launch_gate_errors),
                )
                for record in by_network[network]
            )
        else:
            eligible[network] = selection
    allocation = allocate_networks_to_cohorts(
        eligible,
        protocol_version=protocol_version,
        base_seed=base_seed,
    )
    allocated_networks = set(allocation["A"]) | set(allocation["B"])
    for network in sorted(set(eligible) - allocated_networks):
        exclusions.extend(
            SelectionExclusion(record.participant_id, "network_outside_seeded_first_40")
            for record in by_network[network]
        )

    cohort_a = validate_cohort_pair_support(
        [eligible[network] for network in allocation["A"]],
        cohort_label="A",
    )
    cohort_b = validate_cohort_pair_support(
        [eligible[network] for network in allocation["B"]],
        cohort_label="B",
    )
    records_by_participant = {record.participant_id: record for record in after_hospitals}
    entities_a = _entities_for_selection(cohort_a, records_by_participant)
    entities_b = _entities_for_selection(cohort_b, records_by_participant)
    ensure_disjoint_cohorts(entities_a, entities_b)

    selected_ids = entities_a.participant_ids | entities_b.participant_ids
    already_excluded = {entry.participant_id for entry in exclusions}
    exclusions.extend(
        SelectionExclusion(record.participant_id, "not_selected_by_frozen_pairing")
        for record in after_hospitals
        if record.participant_id not in selected_ids
        and record.participant_id not in already_excluded
    )

    hospital_overlap: tuple[str, ...] = ()
    network_overlap: tuple[str, ...] = ()
    if development_entities is not None:
        participant_overlap = development_entities.participant_ids & selected_ids
        component_overlap = development_entities.relationship_component_ids & (
            entities_a.relationship_component_ids | entities_b.relationship_component_ids
        )
        if participant_overlap:
            raise DesignNotLaunchable("development participant overlap")
        if component_overlap:
            raise DesignNotLaunchable("development relationship-component overlap")
        hospital_overlap = tuple(
            sorted(
                development_entities.hospital_ids
                & (entities_a.hospital_ids | entities_b.hospital_ids)
            )
        )
        network_overlap = tuple(
            sorted(
                development_entities.network_ids & (entities_a.network_ids | entities_b.network_ids)
            )
        )
    return ProspectiveDesign(
        cohort_a=cohort_a,
        cohort_b=cohort_b,
        cohort_a_entities=entities_a,
        cohort_b_entities=entities_b,
        exclusions=tuple(
            sorted(exclusions, key=lambda item: (item.participant_id.encode(), item.reason))
        ),
        development_hospital_overlap=hospital_overlap,
        development_network_overlap=network_overlap,
    )
