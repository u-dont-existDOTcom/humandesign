from datetime import UTC, datetime

from hdmatch.evaluation.astrohd_v13_traditions import TraditionSnapshot
from hdmatch.evaluation.astrohd_v13b_native import (
    lilly_face_ruler,
    lilly_planet_native_strength,
    lilly_term_ruler,
    lilly_triplicity_ruler,
    score_lilly_native,
    score_parashari_native,
)


def snapshot() -> TraditionSnapshot:
    return TraditionSnapshot(
        when=datetime(2000, 1, 1, tzinfo=UTC),
        tropical_longitudes={
            "sun": 10.0,
            "moon": 40.0,
            "mercury": 70.0,
            "venus": 190.0,
            "mars": 10.0,
            "jupiter": 250.0,
            "saturn": 310.0,
        },
        tropical_speeds={
            "sun": 1.0,
            "moon": 13.0,
            "mercury": 1.0,
            "venus": 1.0,
            "mars": 0.5,
            "jupiter": 0.1,
            "saturn": 0.1,
        },
        tropical_ascendant=65.0,
        regio_cusps=(
            60.0,
            90.0,
            120.0,
            150.0,
            180.0,
            210.0,
            240.0,
            270.0,
            300.0,
            330.0,
            0.0,
            30.0,
        ),
        regio_houses={
            "sun": 11,
            "moon": 12,
            "mercury": 1,
            "venus": 5,
            "mars": 11,
            "jupiter": 7,
            "saturn": 9,
        },
        tropical_whole_houses={
            "sun": 11,
            "moon": 12,
            "mercury": 1,
            "venus": 5,
            "mars": 11,
            "jupiter": 7,
            "saturn": 9,
        },
        day_chart=True,
        sidereal_longitudes={
            "sun": 346.0,
            "moon": 16.0,
            "mercury": 46.0,
            "venus": 166.0,
            "mars": 346.0,
            "jupiter": 226.0,
            "saturn": 286.0,
        },
        sidereal_speeds={
            "sun": 1.0,
            "moon": 13.0,
            "mercury": -1.0,
            "venus": 1.0,
            "mars": 0.5,
            "jupiter": 0.1,
            "saturn": 0.1,
        },
        sidereal_ascendant=41.0,
        sidereal_whole_houses={
            "sun": 11,
            "moon": 12,
            "mercury": 1,
            "venus": 5,
            "mars": 11,
            "jupiter": 7,
            "saturn": 9,
        },
    )


def test_lilly_term_face_and_triplicity_tables() -> None:
    assert lilly_term_ruler("aries", 0.0) == "jupiter"
    assert lilly_term_ruler("aries", 6.0) == "venus"
    assert lilly_term_ruler("capricorn", 24.999) == "mars"
    assert lilly_face_ruler("aries", 0.0) == "mars"
    assert lilly_face_ruler("aries", 10.0) == "sun"
    assert lilly_face_ruler("pisces", 29.999) == "mars"
    assert lilly_triplicity_ruler("cancer", day_chart=True) == "mars"
    assert lilly_triplicity_ruler("cancer", day_chart=False) == "mars"
    assert lilly_triplicity_ruler("gemini", day_chart=True) == "saturn"
    assert lilly_triplicity_ruler("gemini", day_chart=False) == "mercury"


def test_lilly_native_strength_uses_source_points() -> None:
    mercury = lilly_planet_native_strength(snapshot(), "mercury")
    assert mercury["components"] == {
        "own_sign": 5,
        "house": 5,
        "motion": 4,
    }
    assert mercury["total"] == 14.0

    moon = lilly_planet_native_strength(snapshot(), "moon")
    assert moon["components"] == {
        "exaltation": 4,
        "face": 1,
        "house": -5,
    }
    assert moon["total"] == 0.0


def test_lilly_domain_mean_and_stack_are_distinct() -> None:
    consensus = {
        "domains": [
            {
                "domain_id": "complex_structure",
                "traditions": [
                    {
                        "tradition": "lilly_traditional_western",
                        "planets": [{"id": "mercury"}],
                        "houses": [{"id": 2}],
                    },
                    {
                        "tradition": "parashari_jyotish",
                        "planets": [],
                        "houses": [],
                    },
                ],
            }
        ]
    }
    mean = score_lilly_native(
        snapshot(),
        consensus_map=consensus,
        behavior_weights={"complex_structure": 1.0},
        aggregation="domain_mean_nonstack",
    )
    stack = score_lilly_native(
        snapshot(),
        consensus_map=consensus,
        behavior_weights={"complex_structure": 1.0},
        aggregation="significator_stack",
    )
    assert mean["domains"][0]["significators"] == ["mercury", "moon"]
    assert mean["total"] == 7.0
    assert stack["total"] == 14.0


def test_parashari_native_consumes_external_shadbala_strengths() -> None:
    consensus = {
        "domains": [
            {
                "domain_id": "resource_motivation",
                "traditions": [
                    {
                        "tradition": "lilly_traditional_western",
                        "planets": [],
                        "houses": [],
                    },
                    {
                        "tradition": "parashari_jyotish",
                        "planets": [],
                        "houses": [{"id": 2}],
                    },
                ],
            }
        ]
    }
    strengths = {
        "sun": 1.1,
        "moon": 1.2,
        "mercury": 1.3,
        "venus": 1.4,
        "mars": 1.5,
        "jupiter": 1.6,
        "saturn": 1.7,
    }
    result = score_parashari_native(
        snapshot(),
        consensus_map=consensus,
        behavior_weights={"resource_motivation": 0.5},
        shadbala_strengths=strengths,
        aggregation="domain_mean_nonstack",
    )
    # Taurus sidereal Ascendant -> 2nd whole-sign house Gemini -> Mercury lord.
    assert result["domains"][0]["significators"] == ["mercury"]
    assert result["total"] == 0.65
