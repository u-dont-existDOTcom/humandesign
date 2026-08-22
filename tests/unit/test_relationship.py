from datetime import UTC, datetime

from hdmatch.chart.bodygraph import Authority, Definition, HDType
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.relationship import (
    CardinalActivation,
    CenterConfigurationKeynote,
    ConnectionKind,
    PartnerTimeCandidate,
    PartnershipSnapshot,
    analyze_partnership,
    summarize_uncertain_partner_time,
)


def _partner_a() -> PartnershipSnapshot:
    return PartnershipSnapshot(
        active_gates=frozenset({1, 5, 8, 10, 23, 24, 26, 28, 43, 44, 61}),
        type=HDType.PROJECTOR,
        authority=Authority.SPLENIC,
        profile="2/4",
        definition=Definition.SPLIT,
        cardinals=(
            CardinalActivation(CelestialBody.SUN, "personality", 10, 2),
        ),
    )


def _partner_b(*, extra_gate_15: bool = False) -> PartnershipSnapshot:
    gates = {1, 10, 20, 29, 38, 44, 46}
    if extra_gate_15:
        gates.add(15)
    return PartnershipSnapshot(
        active_gates=frozenset(gates),
        type=HDType.MANIFESTING_GENERATOR,
        authority=Authority.SACRAL,
        profile="6/3",
        definition=Definition.SPLIT,
        cardinals=(
            CardinalActivation(CelestialBody.NORTH_NODE, "personality", 10, 2),
        ),
    )


def test_surface_connection_mechanics() -> None:
    analysis = analyze_partnership(_partner_a(), _partner_b())

    assert analysis.center_configuration is CenterConfigurationKeynote.EIGHT_ONE
    assert analysis.composite_definition is Definition.SPLIT
    assert {center.value for center in analysis.composite_open_centers} == {"solar_plexus"}

    by_channel = {item.channel: item for item in analysis.channel_connections}
    assert by_channel["28-38"].kind is ConnectionKind.ELECTROMAGNETIC

    assert by_channel["1-8"].kind is ConnectionKind.COMPROMISE
    assert by_channel["1-8"].dominant_partner == "a"
    assert by_channel["1-8"].compromised_partner == "b"

    assert by_channel["10-20"].kind is ConnectionKind.COMPROMISE
    assert by_channel["10-20"].dominant_partner == "b"
    assert by_channel["10-20"].compromised_partner == "a"

    assert by_channel["23-43"].kind is ConnectionKind.DOMINANCE
    assert by_channel["23-43"].dominant_partner == "a"
    assert by_channel["24-61"].kind is ConnectionKind.DOMINANCE
    assert by_channel["24-61"].dominant_partner == "a"

    assert by_channel["26-44"].kind is ConnectionKind.COMPROMISE
    assert by_channel["26-44"].dominant_partner == "a"
    assert by_channel["26-44"].compromised_partner == "b"

    assert by_channel["29-46"].kind is ConnectionKind.DOMINANCE
    assert by_channel["29-46"].dominant_partner == "b"

    assert set(analysis.shared_gates) == {1, 10, 44}
    assert len(analysis.sun_earth_node_alignments) == 1
    alignment = analysis.sun_earth_node_alignments[0]
    assert alignment.source_partner == "a"
    assert alignment.target_partner == "b"
    assert alignment.gate == 10
    assert alignment.same_line is True


def test_unknown_time_summary_keeps_stable_and_variable_mechanics_separate() -> None:
    start = datetime(1989, 6, 18, 23, tzinfo=UTC)
    middle = datetime(1989, 6, 19, 12, tzinfo=UTC)
    end = datetime(1989, 6, 19, 23, tzinfo=UTC)
    candidates = (
        PartnerTimeCandidate(start, middle, _partner_b()),
        PartnerTimeCandidate(middle, end, _partner_b(extra_gate_15=True)),
    )

    summary = summarize_uncertain_partner_time(_partner_a(), candidates)
    stable = {(item.channel, item.kind) for item in summary.stable_connections}
    variable = {(item.channel, item.kind) for item in summary.variable_connections}

    assert ("28-38", ConnectionKind.ELECTROMAGNETIC) in stable
    assert ("5-15", ConnectionKind.ELECTROMAGNETIC) in variable
    assert summary.stable_center_configuration is CenterConfigurationKeynote.EIGHT_ONE
    assert summary.center_configuration_varies is False
    assert summary.stable_composite_definition is Definition.SPLIT
    assert summary.composite_definition_varies is False
    assert summary.partner_types_seen == (HDType.MANIFESTING_GENERATOR,)
    assert summary.total_duration_seconds == 24 * 60 * 60
