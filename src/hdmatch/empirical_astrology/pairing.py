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
    if low_fraction < 0.20:
        errors.append("less_than_20_percent_gap_at_most_15_minutes")
    if high_fraction < 0.20:
        errors.append("less_than_20_percent_gap_at_least_60_minutes")
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
