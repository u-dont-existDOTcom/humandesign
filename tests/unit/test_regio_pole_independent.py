"""Independent Kolev numerical reconstruction; no prediction/participant data.

The 1200-case seed 2004 was explored in scratch before the source contract
was committed: treat it as DEVELOPMENT regression, not an untouched holdout.
The separate 800-case seed 20261026 stays unexecuted until the research
protocol, implementation and this test are published.
"""

from __future__ import annotations

import math
import random

import pytest

from hdmatch.astrology.geometry import (
    EquatorialPoint,
    GeometryMethod,
    direction_arc,
    direction_sense,
)
from hdmatch.astrology.regio_pole_independent import (
    PoleGeometryUnavailable,
    independent_regio_pole_arc,
)


def kolev_example() -> tuple[float, float, EquatorialPoint, EquatorialPoint]:
    """Values transcribed from Kolev mathematical paper, not private data."""
    return (
        53.0,
        222.17357,
        EquatorialPoint(186.1673, -2.6734),  # Sun significator
        EquatorialPoint(261.13, -23.151),  # Jupiter promissor
    )


def test_kolev_published_numerical_example_and_intermediate_pole() -> None:
    lat, meridian, fixed, moving = kolev_example()
    result = independent_regio_pole_arc(lat, meridian, fixed, moving)
    assert result.quadrant == "west_above"
    assert result.sign_above_horizon is True
    assert result.west_of_meridian is True
    # Kolev rounded input coordinates; compare against rounded displayed
    # intermediates with precision honest to the numerical witness.
    assert result.zenith_distance_deg == pytest.approx(52.595667, abs=0.002)
    assert result.significator_pole_deg == pytest.approx(39.375951, abs=0.001)
    assert result.ramc_under_pole_deg == pytest.approx(273.9711, abs=0.001)
    assert result.forward_arc_deg == pytest.approx(56.615053, abs=0.00025)
    assert result.method_provenance.startswith("KOLEV_SECONDARY_")


def test_kolev_example_mathematically_matches_regio_only() -> None:
    lat, meridian, fixed, moving = kolev_example()
    independent = independent_regio_pole_arc(lat, meridian, fixed, moving)
    by_method = {
        method: direction_arc(method, lat, meridian, fixed, moving) for method in GeometryMethod
    }
    assert by_method[GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE] == pytest.approx(
        independent.forward_arc_deg,
        abs=1e-10,
    )
    assert by_method[GeometryMethod.PLACIDEAN_UNDER_POLE] == pytest.approx(
        62.76435915356109,
        abs=1e-8,
    )
    assert by_method[GeometryMethod.PROPORTIONAL_SEMI_ARC] == pytest.approx(
        62.04313286280774,
        abs=1e-8,
    )
    assert all(
        abs(value - independent.forward_arc_deg) > 5.0
        for method, value in by_method.items()
        if method is not GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE
    )
    assert direction_sense(independent.forward_arc_deg)[0] == "direct"


def synthetic_positions(seed: int, n: int):
    """Only pseudorandom mathematical coordinate tuples, never birth data."""
    rng = random.Random(seed)
    for _ in range(n):
        yield (
            rng.uniform(-55, 55),
            rng.uniform(0, 360),
            EquatorialPoint(rng.uniform(0, 360), rng.uniform(-25, 25)),
            EquatorialPoint(rng.uniform(0, 360), rng.uniform(-25, 25)),
        )


def compare_synthetic_geometries(seed: int, n: int) -> dict[str, object]:
    """Raw parity statistic, preserving method family and all quadrants."""
    counts = {}
    largest_delta = 0.0
    for latitude, ramc, sig, prom in synthetic_positions(seed, n):
        independent = independent_regio_pole_arc(latitude, ramc, sig, prom)
        vector = direction_arc(
            GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE,
            latitude,
            ramc,
            sig,
            prom,
        )
        delta = abs((independent.forward_arc_deg - vector + 180.0) % 360.0 - 180.0)
        largest_delta = max(largest_delta, delta)
        counts[independent.quadrant] = counts.get(independent.quadrant, 0) + 1
        assert delta <= 1e-8
    assert sum(counts.values()) == n
    assert set(counts) == {"east_above", "east_below", "west_above", "west_below"}
    return {
        "seed": seed,
        "n": n,
        "quadrants": dict(sorted(counts.items())),
        "maximum_circular_arc_delta_degrees": largest_delta,
        "human_predictive_accuracy": "UNTESTED",
    }


def test_development_1200_synthetic_coordinates_not_validation() -> None:
    result = compare_synthetic_geometries(2004, 1200)
    assert result["n"] == 1200
    assert result["human_predictive_accuracy"] == "UNTESTED"


def test_frozen_post_commit_800_synthetic_holdout_geometry() -> None:
    # This fixed seed/count will be published before its FIRST execution.
    # Holdout applies to independent MATH parity only, not to human outcomes.
    result = compare_synthetic_geometries(20261026, 800)
    assert result["n"] == 800
    assert result["maximum_circular_arc_delta_degrees"] < 1e-8


def test_boundary_failures_are_explicit_not_fake_zero_arc() -> None:
    lat, meridian, sig, prom = kolev_example()
    for invalid in (math.nan, math.inf, -math.inf, 66, -66, 91):
        with pytest.raises((ValueError, PoleGeometryUnavailable)):
            independent_regio_pole_arc(invalid, meridian, sig, prom)
    with pytest.raises(ValueError):
        independent_regio_pole_arc(lat, 360, sig, prom)
    with pytest.raises(ValueError):
        independent_regio_pole_arc(lat, meridian, EquatorialPoint(360, 0), prom)
    with pytest.raises(ValueError):
        independent_regio_pole_arc(lat, meridian, sig, EquatorialPoint(4, 90))


def test_meridian_and_horizon_degeneracy_explicitly_unresolved() -> None:
    sig = EquatorialPoint(100.0, 0.0)
    prom = EquatorialPoint(120.0, 0.0)
    with pytest.raises(PoleGeometryUnavailable, match="meridian"):
        independent_regio_pole_arc(30, 100.0, sig, prom)
    with pytest.raises(PoleGeometryUnavailable, match="horizon"):
        independent_regio_pole_arc(30, 10.0, sig, prom)


def test_preserve_source_provenance_no_full_argoli_or_predictive_claim() -> None:
    source = independent_regio_pole_arc(*kolev_example()).to_dict()
    assert source["method_provenance"] == ("KOLEV_SECONDARY_RECONSTRUCTION_NOT_EXACT_1610_ARGOLI")
    assert "natal_strength" not in source
    assert "predicted_event" not in source


def test_source_hierarchy_and_mathematical_holdout_frozen() -> None:
    import hashlib
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    directory = root / "docs/astrology-research-map/argoli-independent-regio-pole-20261025"
    contract = json.loads((directory / "REGIO_INDEPENDENT_PARITY_PRECOMMIT.json").read_text())
    sample = contract["sample"]
    assert sample["development_seed_already_run_in_exploratory_scratch_before_protocol_commit"]
    assert sample["do_not_count_development_run_as_independent_holdout"]
    assert sample["new_unseen_mathematical_holdout"]["seed"] == 20261026
    assert sample["new_unseen_mathematical_holdout"]["count"] == 800
    assert contract["claims"]["human_predictive_accuracy"] == "UNTESTED"
    assert contract["claims"]["historical_exactness"] == "NOT_AUTHENTICATED_FOR_1610_ARGOLI"
    original = (
        directory
        / "primary_1667_volume/Andrea_Argoli_Primi_Mobilis_Tabulae_1667_original_partial_volume.pdf"
    )
    assert hashlib.sha256(original.read_bytes()).hexdigest() == (
        "b3f93054d64c3ca4318ffaec84e8b7161cdc79d6474bb300efd10787b743df1d"
    )
    assert len(list((directory / "primary_1667_pages").glob("*.png"))) == 3


def test_saved_1200_plus_800_parity_results_and_replay() -> None:
    import importlib.util
    import json
    from pathlib import Path

    directory = (
        Path(__file__).resolve().parents[2]
        / "docs/astrology-research-map/argoli-independent-regio-pole-20261025"
    )
    values = json.loads((directory / "POSITION_CIRCLE_PARITY_REPORT.json").read_text())
    assert values["human_birth_or_event_records_read"] is False
    assert values["history"]["1610_exact_algorithm_authenticated"] is False
    assert values["development_1200_seed2004"]["synthetic_coordinate_cases"] == 1200
    assert values["new_fixed_800_seed20261026"]["synthetic_coordinate_cases"] == 800
    assert values["development_1200_seed2004"]["cases_exceeding_1e_minus_8_deg"] == 0
    assert values["new_fixed_800_seed20261026"]["cases_exceeding_1e_minus_8_deg"] == 0
    assert values["owner_root_combined_forward_blind_validation"] == "OPEN"
    spec = importlib.util.spec_from_file_location(
        "regio_holdout_source_integrity", directory / "verify_regio_parity.py"
    )
    assert spec and spec.loader
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    assert helper.replay()["status"] == "TWO_OF_TWO_PANELS_BITWISE_REPRODUCIBLE"


def test_historical_source_hash_manifest_and_partial_1667_excerpt() -> None:
    import hashlib
    import importlib.util
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    directory = root / "docs/astrology-research-map/argoli-independent-regio-pole-20261025"
    spec = importlib.util.spec_from_file_location(
        "regio_hash_manifest", directory / "verify_regio_parity.py"
    )
    assert spec and spec.loader
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    saved = json.loads((directory / "VERIFICATION.json").read_text())
    assert helper.manifest() == saved
    assert saved["human_predictive_accuracy"] == "UNTESTED"
    assert saved["replay"]["n_later_precommitted_holdout_geometries"] == 800
    for relative, data in saved["file_hashes"].items():
        source = root / relative
        assert hashlib.sha256(source.read_bytes()).hexdigest() == data["sha256"]
