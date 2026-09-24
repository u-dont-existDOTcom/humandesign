from datetime import UTC, datetime

import numpy as np

from hdmatch.evaluation.astrohd_v13_traditions import TraditionSnapshot
from hdmatch.evaluation.astrohd_v13b_lilly_century import (
    lilly_strength_arrays,
    lilly_universe_scores,
)
from hdmatch.evaluation.astrohd_v13b_native import (
    PLANETS,
    lilly_planet_native_strength,
    score_lilly_native,
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
        sidereal_longitudes={planet: 0.0 for planet in PLANETS},
        sidereal_speeds={planet: 0.0 for planet in PLANETS},
        sidereal_ascendant=0.0,
        sidereal_whole_houses={planet: 1 for planet in PLANETS},
    )


def test_vector_strengths_match_scalar_lilly_strengths() -> None:
    snap = snapshot()
    longitudes = np.asarray(
        [[snap.tropical_longitudes[planet]] for planet in PLANETS],
        dtype=np.float64,
    )
    speeds = np.asarray(
        [[snap.tropical_speeds[planet]] for planet in PLANETS],
        dtype=np.float64,
    )
    houses = np.asarray(
        [[snap.regio_houses[planet]] for planet in PLANETS],
        dtype=np.int16,
    )
    vector = lilly_strength_arrays(
        longitudes=longitudes,
        speeds=speeds,
        houses=houses,
        day_chart=np.asarray([snap.day_chart]),
    )
    scalar = np.asarray(
        [lilly_planet_native_strength(snap, planet)["total"] for planet in PLANETS]
    )
    np.testing.assert_allclose(vector[:, 0], scalar)


def test_vector_domain_scoring_matches_scalar_native_scoring() -> None:
    snap = snapshot()
    consensus = {
        "domains": [
            {
                "domain_id": "complex_structure",
                "traditions": [
                    {
                        "tradition": "lilly_traditional_western",
                        "planets": [{"id": "mercury"}],
                        "houses": [{"id": 2}],
                    }
                ],
            },
            {
                "domain_id": "romantic_attachment",
                "traditions": [
                    {
                        "tradition": "lilly_traditional_western",
                        "planets": [{"id": "venus"}],
                        "houses": [{"id": 7}],
                    }
                ],
            },
        ]
    }
    weights = {"complex_structure": 1.0, "romantic_attachment": 0.5}
    longitudes = np.asarray(
        [[snap.tropical_longitudes[planet]] for planet in PLANETS],
        dtype=np.float64,
    )
    speeds = np.asarray(
        [[snap.tropical_speeds[planet]] for planet in PLANETS],
        dtype=np.float64,
    )
    houses = np.asarray(
        [[snap.regio_houses[planet]] for planet in PLANETS],
        dtype=np.int16,
    )
    strengths = lilly_strength_arrays(
        longitudes=longitudes,
        speeds=speeds,
        houses=houses,
        day_chart=np.asarray([snap.day_chart]),
    )
    cusps = np.asarray([snap.regio_cusps], dtype=np.float64)
    for aggregation in ("domain_mean_nonstack", "significator_stack"):
        vector = lilly_universe_scores(
            strengths=strengths,
            cusp_longitudes=cusps,
            consensus_map=consensus,
            behavior_weights=weights,
            aggregation=aggregation,
        )
        scalar = score_lilly_native(
            snap,
            consensus_map=consensus,
            behavior_weights=weights,
            aggregation=aggregation,
        )
        np.testing.assert_allclose(vector[0], scalar["total"])
