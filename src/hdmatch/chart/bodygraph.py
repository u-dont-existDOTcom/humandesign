"""Pure mechanical derivation of BodyGraph architecture from activated gates.

Source notes
------------
The official Jovian Archive glossary defines a channel as two activated gates,
defined centers as centers connected by a channel, and Definition as connected
areas (single through quadruple):
https://jovianarchive.com/pages/human-design-dictionary

The complete 36 channel/center table was cross-checked against
https://humandesignsystem.co/en/36-channels-of-the-human-design-chart/ and the
official overview that states there are 36 two-gate channels:
https://jovianarchive.com/pages/channels-in-human-design-the-life-force

Authority precedence and conditions are sourced from the official overview at
https://jovianarchive.com/pages/what-is-inner-authority-in-human-design and the
specific Ego/Self/Mental authority pages linked in ``BODYGRAPH_SOURCE_URLS``.
Type strategies are sourced from
https://jovianarchive.com/pages/type-and-strategy-in-human-design.

These tables compile standard symbolic mechanics only.  They make no claim of
behavioral predictive validity.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Final, Literal

from .ephemeris import CelestialBody

BODYGRAPH_SOURCE_URLS: Final[tuple[str, ...]] = (
    "https://jovianarchive.com/pages/human-design-dictionary",
    "https://jovianarchive.com/pages/channels-in-human-design-the-life-force",
    "https://humandesignsystem.co/en/36-channels-of-the-human-design-chart/",
    "https://jovianarchive.com/pages/what-is-inner-authority-in-human-design",
    "https://jovianarchive.com/pages/ego-manifested-authority-in-human-design-the-will-that-speaks",
    "https://jovianarchive.com/pages/ego-projected-authority-in-human-design-willpower-and-invitations",
    "https://jovianarchive.com/pages/self-projected-authority-in-human-design-the-projectors-voice",
    "https://jovianarchive.com/pages/mental-authority-in-human-design-a-projector-process",
    "https://jovianarchive.com/pages/type-and-strategy-in-human-design",
)


class Center(StrEnum):
    HEAD = "head"
    AJNA = "ajna"
    THROAT = "throat"
    G = "g"
    HEART = "heart_ego"
    SACRAL = "sacral"
    SOLAR_PLEXUS = "solar_plexus"
    SPLEEN = "spleen"
    ROOT = "root"


class HDType(StrEnum):
    MANIFESTOR = "manifestor"
    GENERATOR = "generator"
    MANIFESTING_GENERATOR = "manifesting_generator"
    PROJECTOR = "projector"
    REFLECTOR = "reflector"


class Strategy(StrEnum):
    INFORM = "inform"
    RESPOND = "wait_to_respond"
    WAIT_FOR_INVITATION = "wait_for_invitation"
    WAIT_LUNAR_CYCLE = "wait_lunar_cycle"


class Authority(StrEnum):
    EMOTIONAL = "emotional_solar_plexus"
    SACRAL = "sacral"
    SPLENIC = "splenic"
    EGO_MANIFESTED = "ego_manifested"
    EGO_PROJECTED = "ego_projected"
    SELF_PROJECTED = "self_projected"
    MENTAL_ENVIRONMENTAL = "mental_environmental"
    LUNAR = "lunar"


class Definition(StrEnum):
    NONE = "no_definition"
    SINGLE = "single_definition"
    SPLIT = "split_definition"
    TRIPLE_SPLIT = "triple_split_definition"
    QUADRUPLE_SPLIT = "quadruple_split_definition"


ActivationSide = Literal["personality", "design"]


@dataclass(frozen=True, slots=True)
class GateActivation:
    body: CelestialBody
    side: ActivationSide
    longitude: float
    gate: int
    line: int

    def __post_init__(self) -> None:
        if not 1 <= self.gate <= 64:
            raise ValueError("gate must be 1..64")
        if not 1 <= self.line <= 6:
            raise ValueError("line must be 1..6")
        if not 0.0 <= self.longitude < 360.0:
            raise ValueError("longitude must be in [0, 360)")


@dataclass(frozen=True, slots=True)
class Channel:
    gate_a: int
    gate_b: int
    center_a: Center
    center_b: Center

    @property
    def identifier(self) -> str:
        low, high = sorted((self.gate_a, self.gate_b))
        return f"{low}-{high}"


GATES_BY_CENTER: Final[dict[Center, frozenset[int]]] = {
    Center.HEAD: frozenset({64, 61, 63}),
    Center.AJNA: frozenset({47, 24, 4, 17, 43, 11}),
    Center.THROAT: frozenset({62, 23, 56, 16, 20, 31, 8, 33, 35, 12, 45}),
    Center.G: frozenset({1, 2, 7, 10, 13, 15, 25, 46}),
    Center.HEART: frozenset({21, 26, 40, 51}),
    Center.SACRAL: frozenset({5, 14, 29, 34, 42, 3, 9, 27, 59}),
    Center.SOLAR_PLEXUS: frozenset({6, 37, 22, 36, 30, 55, 49}),
    Center.SPLEEN: frozenset({48, 57, 44, 50, 32, 28, 18}),
    Center.ROOT: frozenset({58, 38, 54, 53, 60, 52, 19, 39, 41}),
}
GATE_TO_CENTER: Final[dict[int, Center]] = {
    gate: center for center, gates in GATES_BY_CENTER.items() for gate in gates
}


def _channel(gate_a: int, gate_b: int) -> Channel:
    return Channel(gate_a, gate_b, GATE_TO_CENTER[gate_a], GATE_TO_CENTER[gate_b])


CHANNELS: Final[tuple[Channel, ...]] = tuple(
    _channel(*pair)
    for pair in (
        (64, 47),
        (61, 24),
        (63, 4),
        (17, 62),
        (43, 23),
        (11, 56),
        (16, 48),
        (20, 57),
        (20, 34),
        (20, 10),
        (31, 7),
        (8, 1),
        (33, 13),
        (45, 21),
        (35, 36),
        (12, 22),
        (25, 51),
        (10, 57),
        (10, 34),
        (2, 14),
        (5, 15),
        (29, 46),
        (32, 54),
        (28, 38),
        (18, 58),
        (44, 26),
        (27, 50),
        (59, 6),
        (42, 53),
        (3, 60),
        (9, 52),
        (19, 49),
        (39, 55),
        (41, 30),
        (37, 40),
        (34, 57),
    )
)


@dataclass(frozen=True, slots=True)
class Bodygraph:
    active_gates: tuple[int, ...]
    channels: tuple[str, ...]
    defined_centers: tuple[Center, ...]
    definition_components: tuple[tuple[Center, ...], ...]
    type: HDType
    strategy: Strategy
    authority: Authority
    profile: str
    definition: Definition


def derive_bodygraph(activations: Iterable[GateActivation]) -> Bodygraph:
    """Derive channels, centers, Type/Strategy/Authority/Profile/Definition."""

    activation_tuple = tuple(activations)
    active_gates = frozenset(item.gate for item in activation_tuple)
    active_channels = tuple(
        channel
        for channel in CHANNELS
        if channel.gate_a in active_gates and channel.gate_b in active_gates
    )
    graph = _center_graph(active_channels)
    defined_centers = frozenset(graph)
    components = _connected_components(graph)
    hd_type = _derive_type(defined_centers, graph)
    strategy = _strategy_for_type(hd_type)
    authority = _derive_authority(hd_type, defined_centers)
    profile = _derive_profile(activation_tuple)
    definition = _definition_for_components(len(components))

    return Bodygraph(
        active_gates=tuple(sorted(active_gates)),
        channels=tuple(channel.identifier for channel in active_channels),
        defined_centers=tuple(sorted(defined_centers, key=lambda item: item.value)),
        definition_components=components,
        type=hd_type,
        strategy=strategy,
        authority=authority,
        profile=profile,
        definition=definition,
    )


def bodygraph_constants_sha256() -> str:
    payload = json.dumps(
        {
            "channels": [
                [item.gate_a, item.gate_b, item.center_a.value, item.center_b.value]
                for item in CHANNELS
            ],
            "gates_by_center": {
                center.value: sorted(gates) for center, gates in GATES_BY_CENTER.items()
            },
            "authority_precedence": [
                item.value
                for item in (
                    Authority.EMOTIONAL,
                    Authority.SACRAL,
                    Authority.SPLENIC,
                    Authority.EGO_MANIFESTED,
                    Authority.EGO_PROJECTED,
                    Authority.SELF_PROJECTED,
                    Authority.MENTAL_ENVIRONMENTAL,
                    Authority.LUNAR,
                )
            ],
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def _center_graph(channels: tuple[Channel, ...]) -> dict[Center, set[Center]]:
    graph: dict[Center, set[Center]] = defaultdict(set)
    for channel in channels:
        graph[channel.center_a].add(channel.center_b)
        graph[channel.center_b].add(channel.center_a)
    return dict(graph)


def _connected_components(graph: dict[Center, set[Center]]) -> tuple[tuple[Center, ...], ...]:
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
    return tuple(sorted(components, key=lambda item: tuple(center.value for center in item)))


def _connected(graph: dict[Center, set[Center]], start: Center, end: Center) -> bool:
    if start not in graph or end not in graph:
        return False
    queue: deque[Center] = deque((start,))
    visited: set[Center] = set()
    while queue:
        current = queue.popleft()
        if current == end:
            return True
        if current in visited:
            continue
        visited.add(current)
        queue.extend(graph[current] - visited)
    return False


def _derive_type(defined: frozenset[Center], graph: dict[Center, set[Center]]) -> HDType:
    if not defined:
        return HDType.REFLECTOR
    motors = (Center.SACRAL, Center.SOLAR_PLEXUS, Center.HEART, Center.ROOT)
    motor_to_throat = any(_connected(graph, motor, Center.THROAT) for motor in motors)
    if Center.SACRAL in defined:
        if motor_to_throat:
            return HDType.MANIFESTING_GENERATOR
        return HDType.GENERATOR
    if motor_to_throat:
        return HDType.MANIFESTOR
    return HDType.PROJECTOR


def _strategy_for_type(hd_type: HDType) -> Strategy:
    return {
        HDType.MANIFESTOR: Strategy.INFORM,
        HDType.GENERATOR: Strategy.RESPOND,
        HDType.MANIFESTING_GENERATOR: Strategy.RESPOND,
        HDType.PROJECTOR: Strategy.WAIT_FOR_INVITATION,
        HDType.REFLECTOR: Strategy.WAIT_LUNAR_CYCLE,
    }[hd_type]


def _derive_authority(hd_type: HDType, defined: frozenset[Center]) -> Authority:
    if hd_type is HDType.REFLECTOR:
        return Authority.LUNAR
    if Center.SOLAR_PLEXUS in defined:
        return Authority.EMOTIONAL
    if Center.SACRAL in defined:
        return Authority.SACRAL
    if Center.SPLEEN in defined:
        return Authority.SPLENIC
    if Center.HEART in defined:
        if hd_type is HDType.MANIFESTOR:
            return Authority.EGO_MANIFESTED
        return Authority.EGO_PROJECTED
    if Center.G in defined:
        return Authority.SELF_PROJECTED
    return Authority.MENTAL_ENVIRONMENTAL


def _derive_profile(activations: tuple[GateActivation, ...]) -> str:
    personality_lines = {
        item.line
        for item in activations
        if item.side == "personality" and item.body is CelestialBody.SUN
    }
    design_lines = {
        item.line
        for item in activations
        if item.side == "design" and item.body is CelestialBody.SUN
    }
    if len(personality_lines) != 1 or len(design_lines) != 1:
        raise ValueError("profile requires exactly one Personality Sun and one Design Sun")
    return f"{personality_lines.pop()}/{design_lines.pop()}"


def _definition_for_components(count: int) -> Definition:
    try:
        return {
            0: Definition.NONE,
            1: Definition.SINGLE,
            2: Definition.SPLIT,
            3: Definition.TRIPLE_SPLIT,
            4: Definition.QUADRUPLE_SPLIT,
        }[count]
    except KeyError as exc:
        raise ValueError(f"unsupported non-standard definition component count: {count}") from exc


if set(GATE_TO_CENTER) != set(range(1, 65)):
    raise RuntimeError("GATES_BY_CENTER must place every gate exactly once")
if len(CHANNELS) != 36 or len({frozenset((c.gate_a, c.gate_b)) for c in CHANNELS}) != 36:
    raise RuntimeError("CHANNELS must contain 36 unique two-gate channels")
