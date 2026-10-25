"""Directly sourced, limited Lilly 1647 dignity arithmetic—not human validation."""

from __future__ import annotations

import pytest

from hdmatch.astrology.geometry import EquatorialPoint
from hdmatch.astrology.lilly_essential_dignity import (
    CLASSICAL,
    FACES,
    SIGNS,
    TERMS,
    essential_components,
    natal_sun_altitude_deg,
    source_visible_natal_components,
    table_integrity,
    term_ruler,
)
from hdmatch.astrology.sky import DirectionBirthSnapshot


def test_original_table_has_twelve_complete_nonoverlapping_sign_rows() -> None:
    table_integrity()
    assert len(SIGNS) == 12
    assert len(TERMS) == 12
    assert len(FACES) == 12
    for sign in range(12):
        assert len({term_ruler(sign, minute / 60) for minute in range(1800)}) == 5


def test_1647_aries_sect_and_lilly_printed_sun_exaltation_example() -> None:
    # Lilly original p.102: Sun in Aries at NIGHT has exaltation but
    # not fiery triplicity. At 15 Aries it also has his table's solar face.
    day = essential_components("sun", 15.0, is_day_chart=True)
    night = essential_components("sun", 15.0, is_day_chart=False)
    assert day.zodiac_sign == night.zodiac_sign == "aries"
    assert day.dignities_present == ("exaltation", "triplicity", "face")
    assert day.positive_points == 8
    assert night.dignities_present == ("exaltation", "face")
    assert night.positive_points == 5
    assert night.negative_points == day.negative_points == 0


def test_literal_lilly_aries_term_and_face_boundaries_are_half_open() -> None:
    # Lilly pp.104-105: 0-6 Jupiter, 6-14 Venus, 14-21 Mercury,
    # 21-26 Mars, 26-30 Saturn; 0-10 Mars, 10-20 Sun, 20-30 Venus.
    for degree, term in (
        (0, "jupiter"),
        (5.999, "jupiter"),
        (6, "venus"),
        (13.999, "venus"),
        (14, "mercury"),
        (21, "mars"),
        (26, "saturn"),
        (29.999, "saturn"),
    ):
        assert term_ruler(0, degree) == term
    assert essential_components("mars", 0, is_day_chart=True).table_face_ruler == "mars"
    assert essential_components("mars", 10, is_day_chart=True).table_face_ruler == "sun"
    assert essential_components("mars", 20, is_day_chart=True).table_face_ruler == "venus"
    assert essential_components("mars", 30, is_day_chart=True).zodiac_sign == "taurus"


def test_sect_distinguishes_jupiter_night_triplicity() -> None:
    # Literal 1647 table: Jupiter Sagittarius triplicity at NIGHT only.
    day = essential_components("jupiter", 243.0, is_day_chart=True)
    night = essential_components("jupiter", 243.0, is_day_chart=False)
    assert day.dignities_present == ("domicile", "term")
    assert day.positive_points == 7
    assert night.dignities_present == ("domicile", "triplicity", "term")
    assert night.positive_points == 10
    assert day.full_natal_strength.startswith("UNRESOLVED_")


def test_jupiter_cancer_exaltation_not_total_strength() -> None:
    # Jupiter in Cancer +4 exaltation; +2 terms at Cancer 12.
    row = essential_components("jupiter", 102.0, is_day_chart=True)
    assert row.zodiac_sign == "cancer"
    assert row.table_term_ruler == "jupiter"
    assert row.dignities_present == ("exaltation", "term")
    assert row.positive_points == row.partial_net_points == 6
    assert row.full_natal_strength.startswith("UNRESOLVED_")


def test_mercury_virgo_double_positive_vs_pisces_double_negative() -> None:
    virgo = essential_components("mercury", 154.0, is_day_chart=True)
    pisces = essential_components("mercury", 345.0, is_day_chart=True)
    assert virgo.dignities_present == ("domicile", "exaltation", "term")
    assert virgo.positive_points == 11
    assert set(pisces.debilities_present) == {"detriment", "fall"}
    assert pisces.dignities_present == ("term",)
    assert pisces.partial_net_points == -7


def test_peregrine_is_a_separate_explicit_debility() -> None:
    jupiter_gemini = essential_components("jupiter", 80.0, is_day_chart=True)
    assert jupiter_gemini.dignities_present == ()
    assert jupiter_gemini.debilities_present == ("detriment", "peregrine")
    assert jupiter_gemini.partial_net_points == -10


def synthetic_snapshot(*, ramc_deg: float) -> DirectionBirthSnapshot:
    from datetime import UTC, datetime

    return DirectionBirthSnapshot(
        birth_utc=datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=0,
        longitude_east_deg=0,
        ramc_deg=ramc_deg,
        ascendant_ecliptic_lon_deg=0,
        midheaven_ecliptic_lon_deg=0,
        points=(("sun", EquatorialPoint(0, 0)),),
        ephemeris_version="synthetic_only",
        ephemeris_mode="SYNTHETIC_NO_SWISS_CLAIM",
        ephemeris_file_sha256=(),
        ecliptic_positions=tuple((body, 15.0 + 30.0 * i, 0.0) for i, body in enumerate(CLASSICAL)),
    )


def test_independent_geometric_sun_horizon_controls_day_night() -> None:
    noon = synthetic_snapshot(ramc_deg=0)
    midnight = synthetic_snapshot(ramc_deg=180)
    assert natal_sun_altitude_deg(noon) == pytest.approx(90)
    assert natal_sun_altitude_deg(midnight) == pytest.approx(-90)
    day = source_visible_natal_components(noon)
    night = source_visible_natal_components(midnight)
    assert len(day) == len(night) == 7
    assert all(x.chart_sect == "day" for x in day)
    assert all(x.chart_sect == "night" for x in night)
    assert all(x.full_natal_strength.startswith("UNRESOLVED") for x in day)


def test_exact_horizon_does_not_arbitrarily_pick_sect() -> None:
    with pytest.raises(ValueError, match="sect unresolved"):
        source_visible_natal_components(synthetic_snapshot(ramc_deg=90))


def test_invalid_longitudes_and_planets_are_rejected() -> None:
    import math

    for name in ("uranus", "north_node", "asc", "mc"):
        with pytest.raises(ValueError, match="seven classical"):
            essential_components(name, 0, is_day_chart=True)
    for bad_value in (math.inf, -math.inf, math.nan):
        with pytest.raises(ValueError, match="finite"):
            essential_components("jupiter", bad_value, is_day_chart=True)
    for sign, degree in ((12, 5), (-1, 5), (0, 30), (0, -0.1)):
        with pytest.raises(ValueError):
            term_ruler(sign, degree)


def test_repeatable_at_all_exact_sign_and_face_boundaries() -> None:
    for planet in CLASSICAL:
        for sign in range(12):
            for delta in (0, 0.000001, 9.9999, 10, 19.9999, 20, 29.9999):
                longitude = 30.0 * sign + delta
                a = essential_components(planet, longitude, is_day_chart=True)
                b = essential_components(planet, longitude + 360.0, is_day_chart=True)
                assert a.dignities_present == b.dignities_present
                assert a.debilities_present == b.debilities_present
                assert a.partial_net_points == b.partial_net_points
                assert a.sign_index == sign


def test_house_component_simple() -> None:
    from hdmatch.astrology.lilly_essential_dignity import house_component

    assert house_component(1) == (5, True)
    assert house_component(12) == (-5, False)


def test_all_lilly_1647_accidental_house_positions() -> None:
    from hdmatch.astrology.lilly_essential_dignity import house_component

    reference = {
        1: (5, True),
        2: (3, False),
        3: (1, False),
        4: (4, True),
        5: (3, False),
        6: (-2, False),
        7: (4, True),
        8: (-2, False),
        9: (2, False),
        10: (5, True),
        11: (4, False),
        12: (-5, False),
    }
    assert {h: house_component(h) for h in range(1, 13)} == reference
    for bad in (0, 13, -1, 1.5):
        with pytest.raises(ValueError):
            house_component(bad)


def test_swiss_placidus_house_position_opt_in() -> None:
    import os
    from datetime import UTC, datetime

    from hdmatch.astrology.lilly_essential_dignity import swiss_placidus_house
    from hdmatch.astrology.sky import snapshot_from_swiss_files

    ephe = os.getenv("HDMATCH_PRIMARY_DIR_EPHE_DIR")
    if not ephe:
        pytest.skip("official Swiss file integration explicit opt-in")
    natal = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=ephe,
    )
    assert swiss_placidus_house(natal, "sun")[0] == 10
    assert swiss_placidus_house(natal, "jupiter")[2:] == (5, True)
    assert swiss_placidus_house(natal, "mercury")[0] == 9
    with pytest.raises(ValueError):
        swiss_placidus_house(natal, "mc")
