from __future__ import annotations

from hdmatch.chart.bodygraph import (
    CHANNELS,
    Authority,
    Center,
    Definition,
    GateActivation,
    HDType,
    Strategy,
    derive_bodygraph,
)
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.chart.rave_mandala import (
    GATE_WIDTH_DEGREES,
    LINE_WIDTH_DEGREES,
    RAVE_GATE_ORDER,
    RAVE_MANDALA_START_DEGREES,
    longitude_to_gate_line,
)


def _activations(
    gates: list[int], *, personality_line: int = 1, design_line: int = 2
) -> list[GateActivation]:
    result = [
        GateActivation(CelestialBody.SUN, "personality", 0.0, gates[0], personality_line),
        GateActivation(CelestialBody.SUN, "design", 0.0, gates[0], design_line),
    ]
    result.extend(
        GateActivation(CelestialBody.MOON, "personality", 0.0, gate, 1) for gate in gates[1:]
    )
    return result


def test_rave_mandala_exact_half_open_boundaries() -> None:
    just_before = longitude_to_gate_line(RAVE_MANDALA_START_DEGREES - 1e-9)
    at_start = longitude_to_gate_line(RAVE_MANDALA_START_DEGREES)
    at_line_two = longitude_to_gate_line(RAVE_MANDALA_START_DEGREES + LINE_WIDTH_DEGREES)
    at_gate_two = longitude_to_gate_line(RAVE_MANDALA_START_DEGREES + GATE_WIDTH_DEGREES)

    assert (just_before.gate, just_before.line) == (60, 6)
    assert (at_start.gate, at_start.line) == (41, 1)
    assert (at_line_two.gate, at_line_two.line) == (41, 2)
    assert (at_gate_two.gate, at_gate_two.line) == (19, 1)
    assert at_start.color is at_start.tone is at_start.base is None
    assert at_start.advanced_substructure_status == "unavailable_unvalidated"


def test_rave_order_is_a_permutation_and_wraps() -> None:
    assert len(RAVE_GATE_ORDER) == 64
    assert set(RAVE_GATE_ORDER) == set(range(1, 65))
    assert longitude_to_gate_line(662.0).gate == 41


def test_bodygraph_constant_tables_are_complete() -> None:
    assert len(CHANNELS) == 36
    assert len({frozenset((item.gate_a, item.gate_b)) for item in CHANNELS}) == 36


def test_manifesting_generator_and_sacral_authority() -> None:
    graph = derive_bodygraph(_activations([34, 20]))

    assert graph.channels == ("20-34",)
    assert graph.defined_centers == (Center.SACRAL, Center.THROAT)
    assert graph.type is HDType.MANIFESTING_GENERATOR
    assert graph.strategy is Strategy.RESPOND
    assert graph.authority is Authority.SACRAL
    assert graph.definition is Definition.SINGLE
    assert graph.profile == "1/2"


def test_manifestor_and_ego_manifested_authority() -> None:
    graph = derive_bodygraph(_activations([21, 45]))

    assert graph.type is HDType.MANIFESTOR
    assert graph.strategy is Strategy.INFORM
    assert graph.authority is Authority.EGO_MANIFESTED


def test_projector_authorities_and_split_definition() -> None:
    self_projected = derive_bodygraph(_activations([1, 8]))
    mental = derive_bodygraph(_activations([61, 24]))
    split_emotional = derive_bodygraph(_activations([64, 47, 37, 40]))

    assert self_projected.type is HDType.PROJECTOR
    assert self_projected.authority is Authority.SELF_PROJECTED
    assert mental.type is HDType.PROJECTOR
    assert mental.authority is Authority.MENTAL_ENVIRONMENTAL
    assert split_emotional.authority is Authority.EMOTIONAL
    assert split_emotional.definition is Definition.SPLIT
    assert len(split_emotional.definition_components) == 2


def test_reflector_has_no_definition_even_with_hanging_gates() -> None:
    graph = derive_bodygraph(_activations([41, 19]))

    assert graph.channels == ()
    assert graph.defined_centers == ()
    assert graph.type is HDType.REFLECTOR
    assert graph.strategy is Strategy.WAIT_LUNAR_CYCLE
    assert graph.authority is Authority.LUNAR
    assert graph.definition is Definition.NONE
