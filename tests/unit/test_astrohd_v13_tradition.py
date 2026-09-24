from __future__ import annotations

from hdmatch.evaluation.astrohd_v13_tradition import (
    Snapshot,
    evaluate_domain,
    score_candidate,
    whole_sign_house,
)


def _snapshot() -> Snapshot:
    # Tropical Ascendant = 0 Aries. Mercury is in Virgo (own/exaltation)
    # and Regiomontanus house 1. Venus is in Libra. Mars is in Capricorn.
    tropical = {
        "sun": 10.0,
        "moon": 40.0,
        "mercury": 165.0,
        "venus": 190.0,
        "mars": 280.0,
        "jupiter": 100.0,
        "saturn": 305.0,
    }
    speeds = {
        "sun": 1.0,
        "moon": 13.0,
        "mercury": 1.0,
        "venus": 1.0,
        "mars": 0.5,
        "jupiter": 0.1,
        "saturn": 0.1,
    }
    houses = {
        "sun": 1,
        "moon": 2,
        "mercury": 1,
        "venus": 7,
        "mars": 10,
        "jupiter": 4,
        "saturn": 11,
    }
    cusps = tuple(float(index * 30) for index in range(12))
    return Snapshot(
        tropical_longitudes=tropical,
        tropical_speeds=speeds,
        tropical_regio_houses=houses,
        tropical_regio_cusps=cusps,
        tropical_ascendant=0.0,
        sidereal_longitudes=tropical,
        sidereal_speeds=speeds,
        sidereal_ascendant=0.0,
        is_day_chart=True,
    )


def test_whole_sign_house_wraps() -> None:
    assert whole_sign_house(359.0, 1.0) == 12
    assert whole_sign_house(1.0, 359.0) == 2


def test_hellenistic_mercury_uses_dignity_and_angularity_without_sect() -> None:
    evidence = evaluate_domain(
        domain_id="complex_structure",
        tradition_mapping={
            "tradition": "hellenistic_western",
            "planets": [{"id": "mercury"}],
            "houses": [],
        },
        snapshot=_snapshot(),
    )
    assert evidence.net == 2
    assert "mercury:domicile" in evidence.positive
    assert "mercury:exaltation" in evidence.positive
    assert "mercury:whole_sign_angular" not in evidence.positive
    assert "mercury:sect" not in evidence.positive


def test_lilly_planet_counts_source_grounded_testimonies() -> None:
    evidence = evaluate_domain(
        domain_id="complex_structure",
        tradition_mapping={
            "tradition": "lilly_traditional_western",
            "planets": [{"id": "mercury"}],
            "houses": [],
        },
        snapshot=_snapshot(),
    )
    assert evidence.net == 4
    assert set(evidence.positive) == {
        "mercury:domicile",
        "mercury:exaltation",
        "mercury:direct",
        "mercury:positive_house:1",
    }
    assert not evidence.negative


def test_parashari_house_lord_uses_sidereal_house_strength() -> None:
    evidence = evaluate_domain(
        domain_id="resource_motivation",
        tradition_mapping={
            "tradition": "parashari_jyotish",
            "planets": [],
            "houses": [{"id": 2}],
        },
        snapshot=_snapshot(),
    )
    # Aries rising -> 2nd house Taurus -> Venus lord. Venus at Libra is own sign
    # and in whole-sign house 7, a Kendra.
    assert "house2_lord:venus:own_sign" in evidence.positive
    assert "house2_lord:venus:kendra:7" in evidence.positive
    assert not evidence.negative


def test_aggregation_arms_preserve_convergence_vs_raw_stacking() -> None:
    consensus = {
        "domains": [
            {
                "domain_id": "complex_structure",
                "traditions": [
                    {
                        "tradition": "hellenistic_western",
                        "planets": [{"id": "mercury"}],
                        "houses": [],
                        "consensus_abstain": False,
                    },
                    {
                        "tradition": "lilly_traditional_western",
                        "planets": [{"id": "mercury"}],
                        "houses": [],
                        "consensus_abstain": False,
                    },
                    {
                        "tradition": "parashari_jyotish",
                        "planets": [],
                        "houses": [],
                        "consensus_abstain": True,
                    },
                ],
            }
        ]
    }
    scores = score_candidate(
        snapshot=_snapshot(),
        consensus_map=consensus,
        behavioral_confidence={"complex_structure": 0.5},
    )
    assert scores["domain_collapse_nonstack__equal"] == 1
    assert scores["cross_tradition_convergence_stack__equal"] == 2
    assert scores["raw_independent_testimony_stack__equal"] == 6
    assert scores["domain_collapse_nonstack__confidence"] == 0.5
    assert scores["cross_tradition_convergence_stack__confidence"] == 1.0
    assert scores["raw_independent_testimony_stack__confidence"] == 3.0
