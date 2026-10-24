"""Engineering tests for research-only primary-direction timelines.

The historical rulebook and future human predictions are not tested here.
"""

from __future__ import annotations

import json
import math
import os
import random
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.astrology.geometry import (
    EquatorialPoint,
    GeometryMethod,
    GeometryUnavailable,
    direction_arc,
    direction_sense,
)
from hdmatch.astrology.sky import (
    snapshot_from_swiss_files,
)
from hdmatch.astrology.timeline import (
    MODERN_MEAN_TROPICAL_YEAR_DAYS,
    TimeKey,
    degrees_per_symbolic_year,
    generate_timeline,
)


def test_three_exact_gansten_synthetic_methods() -> None:
    fixed = EquatorialPoint(50.0, +15.0)
    moving = EquatorialPoint(80.0, -10.0)
    known = {
        GeometryMethod.PROPORTIONAL_SEMI_ARC: 42.17434402835047,
        GeometryMethod.PLACIDEAN_UNDER_POLE: 42.20081504892782,
        GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE: 46.449117851278395,
    }
    for method, expected in known.items():
        assert direction_arc(method, 45.0, 0.0, fixed, moving) == pytest.approx(expected, abs=1e-10)


def test_signed_zero_boundary_is_direct_not_reversed() -> None:
    fixed = EquatorialPoint(0.25473137480363206, +2.2736895919300677)
    moving = EquatorialPoint(358.75437178465717, -0.5399140988438937)
    arc = direction_arc(
        GeometryMethod.PLACIDEAN_UNDER_POLE, 45.0, 290.80373606057344, fixed, moving
    )
    assert arc == pytest.approx(0.6187055617802457, abs=1e-10)
    assert direction_sense(arc)[0] == "direct"


def test_frozen_morinus_boundary_disagreement_examples() -> None:
    """Cross-check against yesterday's independently saved 9,600-case audit."""
    matrix_path = (
        Path(__file__).resolve().parents[2]
        / "docs/astrology-research-map/gansten-morinus-aodo-issue-20261023"
        / "CROSS_QUADRANT_PARITY.json"
    )
    assert matrix_path.is_file()
    matrix = json.loads(matrix_path.read_text())
    assert matrix["totals"]["valid"] == 9600
    assert matrix["totals"]["bad"] == 591
    for example in matrix["first_mismatches"]:
        lat, ramc, sigra, sigdec, promra, promdec = example["inputs"]
        calculated = direction_arc(
            GeometryMethod.PLACIDEAN_UNDER_POLE,
            lat,
            ramc,
            EquatorialPoint(sigra, sigdec),
            EquatorialPoint(promra, promdec),
        )
        expected = example["reference"]
        residual = (calculated - expected + 180) % 360 - 180
        assert abs(residual) < 1e-7


def test_direct_converse_classification() -> None:
    assert direction_sense(0) == ("direct", 0)
    assert direction_sense(120) == ("direct", 120)
    assert direction_sense(240) == ("converse", 120)
    assert direction_sense(-2) == ("converse", 2)
    assert direction_sense(360) == ("direct", 0)


def test_method_singularity_explicit_not_zero() -> None:
    with pytest.raises(GeometryUnavailable):
        direction_arc(
            GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE,
            90.0 - 1e-4,
            0,
            EquatorialPoint(90, 90),
            EquatorialPoint(0, 10),
        )
    with pytest.raises(ValueError, match="finite"):
        direction_arc(
            GeometryMethod.PROPORTIONAL_SEMI_ARC,
            float("nan"),
            0,
            EquatorialPoint(50, 15),
            EquatorialPoint(80, -10),
        )
    with pytest.raises(ValueError):
        EquatorialPoint(360, 0)
    with pytest.raises(ValueError):
        EquatorialPoint(90, float("nan"))


def test_time_keys_honest_source_separation() -> None:
    ptolemy = TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR
    diagnostic = TimeKey.MODERN_MEAN_SOLAR_DIAGNOSTIC
    assert degrees_per_symbolic_year(ptolemy) == 1.0
    assert degrees_per_symbolic_year(diagnostic) == pytest.approx(
        360 / MODERN_MEAN_TROPICAL_YEAR_DAYS
    )
    assert ptolemy != diagnostic
    with pytest.raises(ValueError):
        degrees_per_symbolic_year("naibod_lilly_original_tables")


def test_birth_requires_declared_swiss_files_and_aware_utc(tmp_path: Path) -> None:
    dt = datetime(2000, 1, 1, 12, tzinfo=UTC)
    with pytest.raises(ValueError, match="offset"):
        snapshot_from_swiss_files(
            datetime(2000, 1, 1, 12),
            latitude_deg=45,
            longitude_east_deg=0,
            ephemeris_directory=tmp_path,
        )
    with pytest.raises(Exception, match="missing"):
        snapshot_from_swiss_files(
            dt,
            latitude_deg=45,
            longitude_east_deg=0,
            ephemeris_directory=tmp_path,
        )
    with pytest.raises(ValueError, match="latitude"):
        snapshot_from_swiss_files(
            dt,
            latitude_deg=70,
            longitude_east_deg=0,
            ephemeris_directory=tmp_path,
        )


def test_randomized_geometry_reference_parity() -> None:
    """Compare against separately frozen analytic/Cartesian reference equations."""
    import importlib.util

    ref_path = (
        Path(__file__).resolve().parents[2]
        / "docs/astrology-research-map/gansten-method-parity-20261023"
        / "geometry_reference.py"
    )
    spec = importlib.util.spec_from_file_location("frozen_independent_gansten_geometry", ref_path)
    assert spec is not None and spec.loader is not None
    import sys

    ref = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = ref
    spec.loader.exec_module(ref)
    rng = random.Random(20261024)
    for _ in range(500):
        lat = rng.uniform(8, 63)
        ramc = rng.uniform(0, 360)
        sigdec = rng.uniform(-19, 19)
        ad = math.degrees(math.asin(math.tan(math.radians(lat)) * math.tan(math.radians(sigdec))))
        sigra = (ramc + rng.uniform(6, 90 + ad - 6)) % 360
        moving = EquatorialPoint(rng.uniform(0, 360), rng.uniform(-15, 15))
        fixed = EquatorialPoint(sigra, sigdec)
        frozen_fixed = ref.EquatorialPoint(fixed.ra_deg, fixed.dec_deg)
        frozen_moving = ref.EquatorialPoint(moving.ra_deg, moving.dec_deg)
        for method, func in [
            (GeometryMethod.PROPORTIONAL_SEMI_ARC, ref.proportional_semi_arc_direction),
            (GeometryMethod.PLACIDEAN_UNDER_POLE, ref.placidean_under_pole_east_upper_north),
            (
                GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE,
                ref.regiomontanus_position_circle_direction,
            ),
        ]:
            actual = direction_arc(method, lat, ramc, fixed, moving)
            expected = func(lat, ramc, frozen_fixed, frozen_moving)
            assert abs((actual - expected + 180) % 360 - 180) < 1e-8


@pytest.mark.skipif(
    not os.environ.get("HDMATCH_PRIMARY_DIR_EPHE_DIR"),
    reason="official Swiss files not available in CI; explicit opt-in integration",
)
def test_end_to_end_swiss_file_timeline_and_provenance() -> None:
    dt = datetime(2000, 1, 1, 12, tzinfo=UTC)
    sky = snapshot_from_swiss_files(
        dt,
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=os.environ["HDMATCH_PRIMARY_DIR_EPHE_DIR"],
    )
    assert sky.ephemeris_mode.startswith("SWIEPH verified")
    assert len(sky.ephemeris_file_sha256) == 2
    assert all(len(sha) == 64 for _name, sha in sky.ephemeris_file_sha256)
    timeline = generate_timeline(sky, max_age_years=100)
    result = timeline.to_dict()
    assert result["schema_version"] == "astro-primary-directions-conjunction-timeline-v1"
    assert result["coverage"]["evaluated_method_pair_combinations"] == 168
    assert result["coverage"]["accepted_records"] == len(timeline.directions)
    assert len(timeline.directions) > 70
    assert all(0 <= d.symbolic_age_years <= 100 for d in timeline.directions)
    assert [d.symbolic_age_years for d in timeline.directions] == sorted(
        d.symbolic_age_years for d in timeline.directions
    )
    assert "no_event_interpretation" in result["technique_provenance"]
    assert result["technique_provenance"]["no_event_interpretation"] is True
    assert timeline.to_dict() == generate_timeline(sky, max_age_years=100).to_dict()
    sun_mc = [d for d in timeline.directions if d.promissor == "sun" and d.significator == "mc"]
    assert len(sun_mc) == 3
    assert all(d.direction == "direct" for d in sun_mc)
    assert all(d.arc_degrees == pytest.approx(0.821313141158, abs=1e-6) for d in sun_mc)
    # Historical literal Naibod table is not yet represented as a time key.
    diagnostic = generate_timeline(
        sky,
        methods=(GeometryMethod.PROPORTIONAL_SEMI_ARC,),
        time_key=TimeKey.MODERN_MEAN_SOLAR_DIAGNOSTIC,
        max_age_years=100,
    )
    diag_sun_mc = next(
        d for d in diagnostic.directions if d.promissor == "sun" and d.significator == "mc"
    )
    assert diag_sun_mc.symbolic_age_years > sun_mc[0].symbolic_age_years


def test_angle_endpoints_agree_across_geometries_with_swiss_files() -> None:
    """Exactly angular contacts reduce to shared meridian/horizon crossings."""
    import os

    from hdmatch.astrology.geometry import ascensional_difference

    eph = os.environ.get("HDMATCH_PRIMARY_DIR_EPHE_DIR")
    if not eph:
        pytest.skip("official Swiss ephemeris files not supplied")
    sky = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=eph,
    )
    points = sky.lookup()
    asc = points["asc"]
    h = (asc.ra_deg - sky.ramc_deg) % 360
    dsa = 90 + ascensional_difference(sky.latitude_deg, asc.dec_deg)
    assert h == pytest.approx(dsa, abs=1e-8)
    for angle in ("asc", "mc"):
        for prom in ("sun", "moon", "saturn"):
            arcs = [
                direction_arc(method, sky.latitude_deg, sky.ramc_deg, points[angle], points[prom])
                for method in GeometryMethod
            ]
            assert max(arcs) - min(arcs) < 1e-8


def test_swiss_file_zero_crossing_has_correct_direct_sense() -> None:
    """Independent astronomical mode switches should not flip contact sense."""
    eph = os.environ.get("HDMATCH_PRIMARY_DIR_EPHE_DIR")
    if not eph:
        pytest.skip("official Swiss ephemeris files not supplied")
    sky = snapshot_from_swiss_files(
        datetime(2026, 3, 19, 6, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=24,
        ephemeris_directory=eph,
    )
    target = sky.lookup()["moon"]
    assert 0 < target.ra_deg < 1
    timeline = generate_timeline(
        sky,
        methods=(GeometryMethod.PLACIDEAN_UNDER_POLE,),
        max_age_years=100,
    )
    records = [r for r in timeline.directions if r.promissor == "sun" and r.significator == "moon"]
    assert len(records) == 1
    assert records[0].direction == "direct"
    assert records[0].arc_degrees == pytest.approx(0.618803403374, abs=1e-6)
