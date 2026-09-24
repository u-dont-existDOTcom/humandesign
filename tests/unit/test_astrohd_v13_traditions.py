from datetime import UTC, datetime

from hdmatch.evaluation.astrohd_v13_traditions import (
    TraditionSnapshot,
    behavior_weight_variants,
    score_snapshot,
    sign_name,
    tradition_domain_testimonies,
    whole_sign_house,
)


def snap():
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
        regio_cusps=(60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0, 0.0, 30.0),
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


def test_sign_and_whole_sign():
    assert sign_name(29.999) == "aries" and sign_name(30) == "taurus"
    assert whole_sign_house(70, 65) == 1 and whole_sign_house(10, 65) == 11


def test_hellenistic_and_lilly_mercury():
    h = tradition_domain_testimonies(
        snap(), tradition="hellenistic_western", planets=["mercury"], houses=[]
    )
    assert h == {"mercury:domicile": 1, "mercury:joy_house": 1}
    lilly = tradition_domain_testimonies(
        snap(), tradition="lilly_traditional_western", planets=["mercury"], houses=[]
    )
    assert lilly == {
        "mercury:own_sign": 1,
        "mercury:direct": 1,
        "mercury:angular_house": 1,
    }


def test_parashari_house_lord_and_dedup():
    p = tradition_domain_testimonies(snap(), tradition="parashari_jyotish", planets=[], houses=[2])
    assert p["mercury:kendra"] == 1 and p["mercury:retrograde_strength"] == 1
    assert len(p) == len(set(p))


def test_three_aggregation_arms():
    m = {
        "domains": [
            {
                "domain_id": "complex_structure",
                "traditions": [
                    {
                        "tradition": "hellenistic_western",
                        "planets": [{"id": "mercury"}],
                        "houses": [],
                    },
                    {
                        "tradition": "lilly_traditional_western",
                        "planets": [{"id": "mercury"}],
                        "houses": [],
                    },
                    {"tradition": "parashari_jyotish", "planets": [], "houses": []},
                ],
            }
        ]
    }
    s = score_snapshot(snap(), consensus_map=m, behavior_weights={"complex_structure": 1.0})
    assert s["totals"] == {
        "domain_collapse_nonstack": 1.0,
        "cross_tradition_convergence_stack": 2.0,
        "raw_independent_testimony_stack": 5.0,
    }


def test_mixed_positive_negative_collapses_to_zero() -> None:
    mixed = {
        "domains": [
            {
                "domain_id": "emotion_permeability",
                "traditions": [
                    {
                        "tradition": "lilly_traditional_western",
                        "planets": [{"id": "moon"}],
                        "houses": [],
                    }
                ],
            }
        ]
    }
    scores = score_snapshot(
        snap(),
        consensus_map=mixed,
        behavior_weights={"emotion_permeability": 1.0},
    )
    assert scores["domains"][0]["traditions"][0]["testimonies"] == {
        "moon:exaltation": 1,
        "moon:cadent_house": -1,
    }
    assert scores["totals"]["domain_collapse_nonstack"] == 0.0
    assert scores["totals"]["cross_tradition_convergence_stack"] == 0.0
    assert scores["totals"]["raw_independent_testimony_stack"] == 0.0


def test_behavior_weight_variants():
    b = {
        "translations": [
            {"historical_cluster": "a", "relation": "supported", "behavioral_confidence": 0.5},
            {
                "historical_cluster": "b",
                "relation": "not_established",
                "behavioral_confidence": 0.0,
            },
        ]
    }
    c = {
        "historical_merged_cluster_crosswalk": [
            {"historical_cluster": "a", "neutral_domain": "complex_structure"},
            {"historical_cluster": "b", "neutral_domain": "immediate_body_signal"},
        ]
    }
    w = behavior_weight_variants(b, c)
    assert w["equal_domain"] == {"complex_structure": 1.0}
    assert w["frozen_measurement_confidence"] == {"complex_structure": 0.5}
