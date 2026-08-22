"""Deterministic Human Design partnership/connection mechanics.

This module intentionally computes mechanics rather than a compatibility score.
The source framework is Ra Uru Hu's 2005 IHDS ``Partnership Analysis`` course:
start with each individual chart, then inspect the connection-chart surface --
center configuration, splits, and the four connection modes (Electromagnetic,
Dominance, Compromise, Companionship) -- before higher-level Sun/Earth and
Nodal context.

The symbolic framework is not scientifically validated as relationship prediction.
Relationship outputs must remain separate from natal reverse-matching scores.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256
from typing import Literal

from hdmatch.chart.bodygraph import (
    CHANNELS,
    ActivationSide,
    Authority,
    Center,
    Definition,
    HDType,
)
from hdmatch.chart.calculator import ChartComputation
from hdmatch.chart.ephemeris import CelestialBody

PartnerId = Literal["a", "b"]


class ConnectionKind(StrEnum):
    """Ra's four primary connection-channel categories."""

    ELECTROMAGNETIC = "electromagnetic"
    DOMINANCE = "dominance"
    COMPROMISE = "compromise"
    COMPANIONSHIP = "companionship"


class CenterConfigurationKeynote(StrEnum):
    """Ra's surface shorthand for the combined defined/open-center count."""

    NINE_ZERO = "9+0 nowhere to go"
    EIGHT_ONE = "8+1 have some fun"
    SEVEN_TWO = "7+2 work to do"
    SIX_THREE = "6+3 better to be free"
    FIVE_FOUR = "5+4 not a relationship anymore"


@dataclass(frozen=True, slots=True)
class CardinalActivation:
    """Sun/Earth/Node activation retained for higher-level relationship context."""

    body: CelestialBody
    side: ActivationSide
    gate: int
    line: int


@dataclass(frozen=True, slots=True)
class PartnershipSnapshot:
    """The natal information required by the partnership module."""

    active_gates: frozenset[int]
    type: HDType | None = None
    authority: Authority | None = None
    profile: str | None = None
    definition: Definition | None = None
    cardinals: tuple[CardinalActivation, ...] = ()

    def __post_init__(self) -> None:
        if any(gate < 1 or gate > 64 for gate in self.active_gates):
            raise ValueError("active_gates must contain only gates 1..64")


@dataclass(frozen=True, slots=True)
class ConnectionChannel:
    """One complete channel relationship between the two natal charts."""

    channel: str
    kind: ConnectionKind
    dominant_partner: PartnerId | None = None
    compromised_partner: PartnerId | None = None

    def __post_init__(self) -> None:
        if self.kind is ConnectionKind.DOMINANCE:
            if self.dominant_partner is None or self.compromised_partner is not None:
                raise ValueError("dominance requires dominant_partner only")
        elif self.kind is ConnectionKind.COMPROMISE:
            if self.dominant_partner is None or self.compromised_partner is None:
                raise ValueError("compromise requires both partner directions")
            if self.dominant_partner == self.compromised_partner:
                raise ValueError("compromise partners must differ")
        elif self.dominant_partner is not None or self.compromised_partner is not None:
            raise ValueError("electromagnetic/companionship channels are nondirectional")


@dataclass(frozen=True, slots=True)
class SunEarthNodeAlignment:
    """A mechanical Sun/Earth-to-Node gate alignment, without soulmate inference."""

    source_partner: PartnerId
    source_body: CelestialBody
    source_side: ActivationSide
    target_partner: PartnerId
    target_body: CelestialBody
    target_side: ActivationSide
    gate: int
    same_line: bool


@dataclass(frozen=True, slots=True)
class PartnershipAnalysis:
    """Complete deterministic V1 connection-chart surface."""

    partner_a_type: HDType | None
    partner_b_type: HDType | None
    partner_a_authority: Authority | None
    partner_b_authority: Authority | None
    partner_a_profile: str | None
    partner_b_profile: str | None
    composite_active_gates: tuple[int, ...]
    composite_channels: tuple[str, ...]
    composite_defined_centers: tuple[Center, ...]
    composite_open_centers: tuple[Center, ...]
    composite_definition_components: tuple[tuple[Center, ...], ...]
    composite_definition: Definition
    center_configuration: CenterConfigurationKeynote | None
    channel_connections: tuple[ConnectionChannel, ...]
    shared_gates: tuple[int, ...]
    sun_earth_node_alignments: tuple[SunEarthNodeAlignment, ...]
    fingerprint_sha256: str


@dataclass(frozen=True, slots=True)
class _Architecture:
    channels: tuple[str, ...]
    defined_centers: tuple[Center, ...]
    components: tuple[tuple[Center, ...], ...]
    definition: Definition


def snapshot_from_chart(chart: ChartComputation) -> PartnershipSnapshot:
    """Convert one deterministic natal chart into the partnership input surface."""

    cardinal_bodies = {
        CelestialBody.SUN,
        CelestialBody.EARTH,
        CelestialBody.NORTH_NODE,
        CelestialBody.SOUTH_NODE,
    }
    cardinals = tuple(
        CardinalActivation(
            body=item.body,
            side=item.side,
            gate=item.gate,
            line=item.line,
        )
        for item in chart.activations
        if item.body in cardinal_bodies
    )
    bodygraph = chart.bodygraph
    return PartnershipSnapshot(
        active_gates=frozenset(bodygraph.active_gates),
        type=bodygraph.type,
        authority=bodygraph.authority,
        profile=bodygraph.profile,
        definition=bodygraph.definition,
        cardinals=cardinals,
    )


def analyze_partnership(
    partner_a: PartnershipSnapshot,
    partner_b: PartnershipSnapshot,
) -> PartnershipAnalysis:
    """Calculate Ra-style connection mechanics without assigning compatibility."""

    composite_gates = partner_a.active_gates | partner_b.active_gates
    architecture = _architecture_from_gates(composite_gates)
    connections = _classify_channels(partner_a.active_gates, partner_b.active_gates)
    shared_gates = tuple(sorted(partner_a.active_gates & partner_b.active_gates))
    alignments = _sun_earth_node_alignments(partner_a, partner_b)
    all_centers = frozenset(Center)
    defined = frozenset(architecture.defined_centers)
    open_centers = tuple(sorted(all_centers - defined, key=lambda item: item.value))
    center_configuration = _center_configuration(len(defined))

    payload = {
        "partner_a": {
            "type": partner_a.type.value if partner_a.type is not None else None,
            "authority": (
                partner_a.authority.value if partner_a.authority is not None else None
            ),
            "profile": partner_a.profile,
        },
        "partner_b": {
            "type": partner_b.type.value if partner_b.type is not None else None,
            "authority": (
                partner_b.authority.value if partner_b.authority is not None else None
            ),
            "profile": partner_b.profile,
        },
        "composite_active_gates": sorted(composite_gates),
        "composite_channels": list(architecture.channels),
        "defined_centers": [item.value for item in architecture.defined_centers],
        "open_centers": [item.value for item in open_centers],
        "definition_components": [
            [center.value for center in component] for component in architecture.components
        ],
        "definition": architecture.definition.value,
        "center_configuration": (
            center_configuration.value if center_configuration is not None else None
        ),
        "connections": [
            {
                "channel": item.channel,
                "kind": item.kind.value,
                "dominant_partner": item.dominant_partner,
                "compromised_partner": item.compromised_partner,
            }
            for item in connections
        ],
        "shared_gates": list(shared_gates),
        "sun_earth_node_alignments": [
            {
                "source_partner": item.source_partner,
                "source_body": item.source_body.value,
                "source_side": item.source_side,
                "target_partner": item.target_partner,
                "target_body": item.target_body.value,
                "target_side": item.target_side,
                "gate": item.gate,
                "same_line": item.same_line,
            }
            for item in alignments
        ],
    }
    fingerprint = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return PartnershipAnalysis(
        partner_a_type=partner_a.type,
        partner_b_type=partner_b.type,
        partner_a_authority=partner_a.authority,
        partner_b_authority=partner_b.authority,
        partner_a_profile=partner_a.profile,
        partner_b_profile=partner_b.profile,
        composite_active_gates=tuple(sorted(composite_gates)),
        composite_channels=architecture.channels,
        composite_defined_centers=architecture.defined_centers,
        composite_open_centers=open_centers,
        composite_definition_components=architecture.components,
        composite_definition=architecture.definition,
        center_configuration=center_configuration,
        channel_connections=connections,
        shared_gates=shared_gates,
        sun_earth_node_alignments=alignments,
        fingerprint_sha256=fingerprint,
    )


def _classify_channels(
    gates_a: frozenset[int],
    gates_b: frozenset[int],
) -> tuple[ConnectionChannel, ...]:
    results: list[ConnectionChannel] = []
    for channel in CHANNELS:
        ga, gb = channel.gate_a, channel.gate_b
        a_has_a = ga in gates_a
        a_has_b = gb in gates_a
        b_has_a = ga in gates_b
        b_has_b = gb in gates_b
        a_full = a_has_a and a_has_b
        b_full = b_has_a and b_has_b

        if a_full and b_full:
            results.append(ConnectionChannel(channel.identifier, ConnectionKind.COMPANIONSHIP))
            continue
        if a_full:
            if b_has_a or b_has_b:
                results.append(
                    ConnectionChannel(
                        channel.identifier,
                        ConnectionKind.COMPROMISE,
                        dominant_partner="a",
                        compromised_partner="b",
                    )
                )
            else:
                results.append(
                    ConnectionChannel(
                        channel.identifier,
                        ConnectionKind.DOMINANCE,
                        dominant_partner="a",
                    )
                )
            continue
        if b_full:
            if a_has_a or a_has_b:
                results.append(
                    ConnectionChannel(
                        channel.identifier,
                        ConnectionKind.COMPROMISE,
                        dominant_partner="b",
                        compromised_partner="a",
                    )
                )
            else:
                results.append(
                    ConnectionChannel(
                        channel.identifier,
                        ConnectionKind.DOMINANCE,
                        dominant_partner="b",
                    )
                )
            continue
        if (a_has_a and b_has_b) or (a_has_b and b_has_a):
            results.append(ConnectionChannel(channel.identifier, ConnectionKind.ELECTROMAGNETIC))

    return tuple(sorted(results, key=_connection_sort_key))


def _connection_sort_key(item: ConnectionChannel) -> tuple[str, str, str, str]:
    return (
        item.channel,
        item.kind.value,
        item.dominant_partner or "",
        item.compromised_partner or "",
    )


def _architecture_from_gates(gates: frozenset[int]) -> _Architecture:
    active_channels = tuple(
        channel for channel in CHANNELS if channel.gate_a in gates and channel.gate_b in gates
    )
    graph: dict[Center, set[Center]] = defaultdict(set)
    for channel in active_channels:
        graph[channel.center_a].add(channel.center_b)
        graph[channel.center_b].add(channel.center_a)

    components = _connected_components(graph)
    defined_centers = tuple(sorted(graph, key=lambda item: item.value))
    definition = _definition_for_component_count(len(components))
    return _Architecture(
        channels=tuple(sorted(channel.identifier for channel in active_channels)),
        defined_centers=defined_centers,
        components=components,
        definition=definition,
    )


def _connected_components(
    graph: dict[Center, set[Center]],
) -> tuple[tuple[Center, ...], ...]:
    remaining = set(graph)
    components: list[tuple[Center, ...]] = []
    while remaining:
        seed = min(remaining, key=lambda item: item.value)
        queue: deque[Center] = deque((seed,))
        found: set[Center] = set()
        while queue:
            center = queue.popleft()
            if center in found:
                continue
            found.add(center)
            queue.extend(graph[center] - found)
        remaining -= found
        components.append(tuple(sorted(found, key=lambda item: item.value)))
    return tuple(sorted(components, key=lambda group: tuple(item.value for item in group)))


def _definition_for_component_count(count: int) -> Definition:
    values = {
        0: Definition.NONE,
        1: Definition.SINGLE,
        2: Definition.SPLIT,
        3: Definition.TRIPLE_SPLIT,
        4: Definition.QUADRUPLE_SPLIT,
    }
    try:
        return values[count]
    except KeyError as exc:
        raise ValueError(f"unsupported composite definition component count: {count}") from exc


def _center_configuration(count: int) -> CenterConfigurationKeynote | None:
    return {
        9: CenterConfigurationKeynote.NINE_ZERO,
        8: CenterConfigurationKeynote.EIGHT_ONE,
        7: CenterConfigurationKeynote.SEVEN_TWO,
        6: CenterConfigurationKeynote.SIX_THREE,
        5: CenterConfigurationKeynote.FIVE_FOUR,
    }.get(count)


def _sun_earth_node_alignments(
    partner_a: PartnershipSnapshot,
    partner_b: PartnershipSnapshot,
) -> tuple[SunEarthNodeAlignment, ...]:
    sun_earth = {CelestialBody.SUN, CelestialBody.EARTH}
    nodes = {CelestialBody.NORTH_NODE, CelestialBody.SOUTH_NODE}
    alignments: list[SunEarthNodeAlignment] = []
    for source_id, source, target_id, target in (
        ("a", partner_a, "b", partner_b),
        ("b", partner_b, "a", partner_a),
    ):
        for source_activation in source.cardinals:
            if source_activation.body not in sun_earth:
                continue
            for target_activation in target.cardinals:
                if target_activation.body not in nodes:
                    continue
                if source_activation.gate != target_activation.gate:
                    continue
                alignments.append(
                    SunEarthNodeAlignment(
                        source_partner=source_id,
                        source_body=source_activation.body,
                        source_side=source_activation.side,
                        target_partner=target_id,
                        target_body=target_activation.body,
                        target_side=target_activation.side,
                        gate=source_activation.gate,
                        same_line=source_activation.line == target_activation.line,
                    )
                )
    return tuple(
        sorted(
            alignments,
            key=lambda item: (
                item.source_partner,
                item.source_body.value,
                item.source_side,
                item.target_partner,
                item.target_body.value,
                item.target_side,
                item.gate,
                item.same_line,
            ),
        )
    )
