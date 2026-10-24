"""Role-reversed traditional and modern converse are different algorithms.

Tests include independent old frozen Cartesian/semi-arc reference equations.
All charts synthetic; no empirical outcome/personal natal data.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.astrology.aspect_points import (
    RayAspect,
    RayBranch,
    zodiacal_promissor_ray,
)
from hdmatch.astrology.geometry import (
    EquatorialPoint,
    GeometryMethod,
    GeometryUnavailable,
    direction_arc,
)
from hdmatch.astrology.role_directions import (
    ContactConstruction,
    RotationRegime,
    generate_role_timeline,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.timeline import generate_timeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def natal():
    folder = Path("/home/joel/.local/share/hdmatch/ephemeris/1800-2399")
    if not folder.exists():
        pytest.skip("local Swiss astronomical files unavailable")
    return snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=folder,
    )


def test_rotation_is_not_a_role_swap() -> None:
    fixed = EquatorialPoint(50, 15)
    moving = EquatorialPoint(80, -10)
    known = {
        GeometryMethod.PROPORTIONAL_SEMI_ARC: (42.17434402835047, 304.3418407017051),
        GeometryMethod.PLACIDEAN_UNDER_POLE: (42.20081504892782, 304.34219090551323),
        GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE: (46.449117851278395, 304.30193926497145),
    }
    for method, (expected_forward, expected_traditional) in known.items():
        direct = direction_arc(method, 45, 0, fixed, moving)
        role_reversed = direction_arc(method, 45, 0, moving, fixed)
        modern_reversed = (360 - direct) % 360
        assert direct == pytest.approx(expected_forward, abs=1e-9)
        assert role_reversed == pytest.approx(expected_traditional, abs=1e-9)
        assert abs(role_reversed - modern_reversed) > 8


def test_traditional_converse_moves_significator_not_aspect(natal) -> None:
    results = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
    )
    assert results.evaluated == 882
    assert len(results.directions) == 288
    assert all(r.geometric_fixed_point == "natal_promissor_ray" for r in results.directions)
    assert all(r.geometric_moving_point == "natal_significator_body" for r in results.directions)
    assert all(r.rotation_label == "traditional_role_reversed_converse" for r in results.directions)
    assert all(r.significator not in ("asc", "mc") for r in results.directions)
    ecliptic = natal.ecliptic_lookup()
    for record in results.directions[:40]:
        ray = zodiacal_promissor_ray(
            ecliptic[record.promissor][0],
            aspect=RayAspect(record.aspect),
            branch=RayBranch(record.aspect_offset_branch),
            obliquity_deg=natal.true_obliquity_deg,
        )
        expected = direction_arc(
            GeometryMethod(record.method),
            natal.latitude_deg,
            natal.ramc_deg,
            ray.equatorial,
            natal.lookup()[record.significator],
        )
        assert record.arc_degrees == pytest.approx(expected, abs=1e-9)
        assert record.original_forward_arc_deg == pytest.approx(expected, abs=1e-9)


def test_modern_reverse_rotation_keeps_roles_and_complements_direct(natal) -> None:
    modern = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.MODERN_REVERSE_ROTATION_DIAGNOSTIC,
    )
    assert modern.evaluated == 1176
    assert len(modern.directions) == 364
    assert all(
        rec.geometric_fixed_point in ("natal_significator_body", "natal_angle_circle")
        for rec in modern.directions
    )
    assert all(rec.geometric_moving_point == "promissor_zodiacal_ray" for rec in modern.directions)
    for rec in modern.directions:
        assert rec.arc_degrees == pytest.approx(
            (360 - rec.original_forward_arc_deg) % 360, abs=1e-10
        )
        assert rec.rotation_label == "modern_reverse_rotation_converse"


def test_direct_significator_aspect_is_fixed_ray_moving_body(natal) -> None:
    data = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT,
        regime=RotationRegime.DIRECT_PRIMARY_MOTION,
    )
    assert data.evaluated == 882
    assert len(data.directions) == 288
    assert data.to_dict()["movement_provenance"]["is_significator_aspect_experimental"]
    ecl = natal.ecliptic_lookup()
    pts = natal.lookup()
    for rec in data.directions[:45]:
        assert rec.ray_owner == rec.significator
        assert rec.geometric_fixed_point == "natal_significator_aspect"
        assert rec.geometric_moving_point == "natal_promissor_body"
        assert rec.ray_latitude_deg == 0
        assert rec.significator not in ("asc", "mc")
        placed = zodiacal_promissor_ray(
            ecl[rec.significator][0],
            aspect=RayAspect(rec.aspect),
            branch=RayBranch(rec.aspect_offset_branch),
            obliquity_deg=natal.true_obliquity_deg,
        )
        assert rec.ray_longitude_deg == pytest.approx(placed.ecliptic_longitude_deg)
        assert rec.arc_degrees == pytest.approx(
            direction_arc(
                GeometryMethod(rec.method),
                natal.latitude_deg,
                natal.ramc_deg,
                placed.equatorial,
                pts[rec.promissor],
            ),
            abs=1e-9,
        )


def test_constructions_and_direction_regimes_remain_distinct(natal) -> None:
    direct = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.DIRECT_PRIMARY_MOTION,
    )
    traditional = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
    )
    modern = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.MODERN_REVERSE_ROTATION_DIAGNOSTIC,
    )
    assert direct.evaluated == 1176
    assert traditional.evaluated == 882
    assert modern.evaluated == 1176

    def k(r):
        return (r.method, r.promissor, r.significator, r.aspect, r.aspect_offset_branch)

    dt = {k(r): r for r in direct.directions}
    tr = {k(r): r for r in traditional.directions}
    mr = {k(r): r for r in modern.directions}
    # A direct arc and its strict 360-arc reverse cannot both be <=100°.
    # This follows from the preregistered age window, not a software failure.
    assert not (set(dt) & set(mr))
    shared = set(tr) & set(mr)
    assert shared
    assert any(abs(tr[key].arc_degrees - mr[key].arc_degrees) > 0.001 for key in shared)
    assert traditional.to_dict()["schema_version"] == "astro-primary-direction-role-variants-v1"
    assert "not an endorsement" in direct.to_dict()["movement_provenance"]["source_basis"]


def test_bodily_converse_excludes_moving_angles(natal) -> None:
    roles = generate_role_timeline(
        natal,
        construction=ContactConstruction.BODY_CONJUNCTION,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
    )
    assert roles.evaluated == 126
    assert all(rec.significator not in ("asc", "mc") for rec in roles.directions)
    assert all(rec.ray_owner is None and rec.aspect is None for rec in roles.directions)
    assert all(
        rec.rotation_label == "traditional_role_reversed_converse" for rec in roles.directions
    )


def test_invalid_historical_combinations_fail_closed(natal) -> None:
    with pytest.raises(ValueError, match="direct motion only"):
        generate_role_timeline(
            natal,
            construction=ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT,
            regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
        )
    with pytest.raises(ValueError, match="unresolved"):
        generate_role_timeline(
            natal,
            construction=ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT,
            regime=RotationRegime.MODERN_REVERSE_ROTATION_DIAGNOSTIC,
        )
    with pytest.raises(ValueError, match="accepts no"):
        generate_role_timeline(
            natal,
            construction=ContactConstruction.BODY_CONJUNCTION,
            regime=RotationRegime.DIRECT_PRIMARY_MOTION,
            aspects=(RayAspect.SQUARE,),
        )
    with pytest.raises(ValueError, match="significator projection"):
        generate_role_timeline(
            natal,
            construction=ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT,
            regime=RotationRegime.DIRECT_PRIMARY_MOTION,
            significator_projection="project_to_ecliptic",
        )
    with pytest.raises(ValueError, match="at least one"):
        generate_role_timeline(
            natal,
            construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
            regime=RotationRegime.DIRECT_PRIMARY_MOTION,
            aspects=(),
        )


def test_projection_limited_to_fixed_planet_of_promissor_ray(natal) -> None:
    data = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
        significator_projection="project_to_ecliptic",
        methods=(GeometryMethod.PROPORTIONAL_SEMI_ARC,),
    )
    assert data.directions
    assert all(rec.significator_projection == "project_to_ecliptic" for rec in data.directions)


def test_strict_api_not_altering_frozen_prior_engine(natal) -> None:
    previous = generate_timeline(natal).to_dict()
    frozen = json.loads(
        (
            PROJECT_ROOT / "docs/astrology-research-map/gansten-primary-timeline-20261024/examples/"
            "synthetic_2000_timeline.json"
        ).read_text()
    )
    assert previous == frozen


def test_independent_frozen_cartesian_role_reversed_math() -> None:
    path = (
        PROJECT_ROOT
        / "docs/astrology-research-map/gansten-method-parity-20261023/geometry_reference.py"
    )
    spec = importlib.util.spec_from_file_location("independent_reversal_geometry", path)
    assert spec and spec.loader
    ref = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = ref
    spec.loader.exec_module(ref)
    rng = random.Random(20261024)
    good = 0
    for _ in range(350):
        latitude = rng.uniform(-55, 55)
        ramc = rng.uniform(0, 360)
        prom = EquatorialPoint(rng.uniform(0, 360), rng.uniform(-20, 20))
        sig = EquatorialPoint(rng.uniform(0, 360), rng.uniform(-20, 20))
        rp = ref.EquatorialPoint(prom.ra_deg, prom.dec_deg)
        rs = ref.EquatorialPoint(sig.ra_deg, sig.dec_deg)
        try:
            for method, fn in (
                (GeometryMethod.PROPORTIONAL_SEMI_ARC, ref.proportional_semi_arc_direction),
                (
                    GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE,
                    ref.regiomontanus_position_circle_direction,
                ),
            ):
                expected = fn(latitude, ramc, rp, rs)
                result = direction_arc(method, latitude, ramc, prom, sig)
                assert abs((expected - result + 180) % 360 - 180) < 1e-8
                good += 1
        except (GeometryUnavailable, ref.DomainError):
            continue
    assert good > 500


def test_cli_integration_and_flag_scope(natal, tmp_path: Path) -> None:
    from hdmatch.astrology.cli import main

    base = [
        "--utc",
        "2000-01-01T12:00:00Z",
        "--latitude",
        "45",
        "--longitude-east",
        "0",
        "--ephemeris-dir",
        "/home/joel/.local/share/hdmatch/ephemeris/1800-2399",
    ]
    out = tmp_path / "roles.json"
    assert (
        main(
            base
            + [
                "--profile",
                "role_variants",
                "--contact-construction",
                "zodiacal_significator_aspect",
                "--rotation-regime",
                "direct_primary_motion",
                "--output",
                str(out),
            ]
        )
        == 0
    )
    result = json.loads(out.read_text())
    assert result["movement_provenance"]["construction"] == "zodiacal_significator_aspect"
    assert result["coverage"]["accepted"] == 288
    with pytest.raises(SystemExit) as exc:
        main(
            base
            + [
                "--profile",
                "body_conjunctions",
                "--rotation-regime",
                "traditional_role_reversed_converse",
                "--output",
                str(tmp_path / "invalid.json"),
            ]
        )
    assert exc.value.code == 2
    assert not (tmp_path / "invalid.json").exists()
    with pytest.raises(SystemExit) as exc2:
        main(
            base
            + [
                "--profile",
                "role_variants",
                "--contact-construction",
                "zodiacal_significator_aspect",
                "--rotation-regime",
                "traditional_role_reversed_converse",
                "--output",
                str(tmp_path / "invalid2.json"),
            ]
        )
    assert exc2.value.code == 2


def test_role_reversed_rays_are_not_independent_of_swapped_direct_sig_aspects(natal) -> None:
    """Warn the future validation stage: geometric duplicate, labels differ."""
    backwards = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
    )
    forwards = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_SIGNIFICATOR_ASPECT,
        regime=RotationRegime.DIRECT_PRIMARY_MOTION,
    )
    lookup = {
        (r.method, r.promissor, r.significator, r.aspect, r.aspect_offset_branch): r
        for r in forwards.directions
    }
    assert len(backwards.directions) == len(forwards.directions) == 288
    for rec in backwards.directions:
        # Original promissor P's ray is fixed. Exchanging labels P↔S gives
        # direct motion of the same S body to P's constructed fixed aspect.
        # This proves geometrical duplication, not identical interpretation.
        counterpart = lookup[
            (rec.method, rec.significator, rec.promissor, rec.aspect, rec.aspect_offset_branch)
        ]
        assert rec.ray_owner == counterpart.ray_owner
        assert rec.ray_longitude_deg == pytest.approx(counterpart.ray_longitude_deg, abs=1e-12)
        assert rec.arc_degrees == pytest.approx(counterpart.arc_degrees, abs=1e-10)
        assert rec.symbolic_age_years == pytest.approx(counterpart.symbolic_age_years, abs=1e-10)
        assert rec.rotation_regime != counterpart.rotation_regime
