"""Bounded, historically differentiated aspect-geometry regression suite.

The Gansten book audit is the interpretation/source locator; this suite tests
only the declared numerical algorithms, not historical authorship or forecasts.
"""

from __future__ import annotations

import json
import os
import random
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.astrology.aspect_points import (
    RayAspect,
    RayBranch,
    aspect_branches,
    ecliptic_to_equatorial,
    mundane_semi_arc_phase_arc,
    zodiacal_promissor_ray,
)
from hdmatch.astrology.aspect_timeline import (
    AspectProfile,
    SignificatorProjection,
    generate_aspect_timeline,
)
from hdmatch.astrology.geometry import (
    EquatorialPoint,
    GeometryMethod,
    _phase,
    _semi_arcs,
    normalize,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.timeline import generate_timeline

EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        "/home/joel/.local/share/hdmatch/ephemeris/1800-2399",
    )
)
MODULE_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def swiss_snapshot():
    if not EPHE.is_dir():
        pytest.skip("owner's official local Swiss source data not installed")
    return snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )


def test_ray_aspect_branches_exclude_duplicate_opposition() -> None:
    assert len(aspect_branches(RayAspect.OPPOSITION)) == 1
    assert len(aspect_branches(RayAspect.SQUARE)) == 2
    assert len(aspect_branches(RayAspect.SEXTILE)) == 2
    assert len(aspect_branches(RayAspect.TRINE)) == 2
    with pytest.raises(ValueError, match="one"):
        zodiacal_promissor_ray(
            20, aspect=RayAspect.OPPOSITION, branch=RayBranch.NEGATIVE, obliquity_deg=23.43
        )


def test_zodiacal_rays_are_ecliptic_not_ra_offsets() -> None:
    eps = 23.4376767
    natal_lon = 350.0
    plus = zodiacal_promissor_ray(
        natal_lon, aspect=RayAspect.SEXTILE, branch=RayBranch.POSITIVE, obliquity_deg=eps
    )
    minus = zodiacal_promissor_ray(
        natal_lon, aspect=RayAspect.SEXTILE, branch=RayBranch.NEGATIVE, obliquity_deg=eps
    )
    opposition = zodiacal_promissor_ray(
        natal_lon, aspect=RayAspect.OPPOSITION, branch=RayBranch.POSITIVE, obliquity_deg=eps
    )
    assert plus.ecliptic_longitude_deg == pytest.approx(50.0)
    assert minus.ecliptic_longitude_deg == pytest.approx(290.0)
    assert opposition.ecliptic_longitude_deg == pytest.approx(170.0)
    assert all(x.ecliptic_latitude_deg == 0 for x in (plus, minus, opposition))
    original_ra = ecliptic_to_equatorial(natal_lon, 0, eps).ra_deg
    wrong_ra = normalize(original_ra + 60)
    assert abs((plus.equatorial.ra_deg - wrong_ra + 180) % 360 - 180) > 1
    assert plus.equatorial.dec_deg > 0


def test_spherical_projection_agrees_with_independent_swiss_cotrans() -> None:
    swe = pytest.importorskip("swisseph")
    rng = random.Random(20261024)
    for _ in range(300):
        lon = rng.uniform(0, 360)
        lat = rng.uniform(-15, 15)
        eps = rng.uniform(22, 25)
        ours = ecliptic_to_equatorial(lon, lat, eps)
        ra, dec, _dist = swe.cotrans((lon, lat, 1.0), -eps)
        assert abs((ours.ra_deg - ra + 180) % 360 - 180) < 1e-9
        assert ours.dec_deg == pytest.approx(dec, abs=1e-9)


def test_spherical_projection_and_rays_fail_closed() -> None:
    for bad in (float("nan"), float("inf")):
        with pytest.raises(ValueError, match="non-finite"):
            ecliptic_to_equatorial(bad, 0, 23.4)
    with pytest.raises(ValueError, match="domain"):
        ecliptic_to_equatorial(10, 91, 23.4)
    with pytest.raises(ValueError, match="domain"):
        ecliptic_to_equatorial(10, 1, -23.4)
    with pytest.raises(ValueError, match="normalized"):
        zodiacal_promissor_ray(
            360, aspect=RayAspect.SQUARE, branch=RayBranch.POSITIVE, obliquity_deg=23.4
        )


def test_swiss_snapshot_retains_both_coordinate_systems(swiss_snapshot) -> None:
    ecl = swiss_snapshot.ecliptic_lookup()
    eq = swiss_snapshot.lookup()
    assert len(ecl) == 7
    assert swiss_snapshot.true_obliquity_deg == pytest.approx(23.437676716, abs=1e-7)
    moon_lon, moon_lat = ecl["moon"]
    assert abs(moon_lat) > 4
    moon_recon = ecliptic_to_equatorial(moon_lon, moon_lat, swiss_snapshot.true_obliquity_deg)
    assert moon_recon.ra_deg == pytest.approx(eq["moon"].ra_deg, abs=1e-9)
    assert moon_recon.dec_deg == pytest.approx(eq["moon"].dec_deg, abs=1e-9)
    assert all(len(x) == 64 for x in dict(swiss_snapshot.ephemeris_file_sha256).values())


def test_old_conjunction_only_timeline_identical_to_frozen_sample(swiss_snapshot) -> None:
    # Adding ecliptic source coordinates must not change the earlier
    # audited conjunction-only output or its chronological ordering.
    actual = generate_timeline(swiss_snapshot).to_dict()
    frozen = json.loads(
        (
            MODULE_ROOT / "docs/astrology-research-map/gansten-primary-timeline-20261024/"
            "examples/synthetic_2000_timeline.json"
        ).read_text()
    )
    assert actual == frozen


def test_zodiacal_and_mundane_profiles_have_distinct_types_and_counts(swiss_snapshot) -> None:
    z = generate_aspect_timeline(
        swiss_snapshot,
        profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
    )
    m = generate_aspect_timeline(
        swiss_snapshot,
        profile=AspectProfile.MUNDANE_PROPORTIONAL_SEMI_ARC,
    )
    assert z.evaluated == 1176
    assert m.evaluated == 392
    assert len(z.directions) == 683
    assert len(m.directions) == 222
    assert z.to_dict()["schema_version"] == m.to_dict()["schema_version"]
    assert z.to_dict()["scope"]["contact"] != m.to_dict()["scope"]["contact"]
    assert all(rec.ray_ecliptic_latitude_degrees == 0 for rec in z.directions)
    assert all(rec.ray_ecliptic_longitude_degrees is None for rec in m.directions)
    assert all(rec.aspect_coordinate_frame.startswith("normalized") for rec in m.directions)
    assert all(rec.aspect_coordinate_frame.startswith("tropical") for rec in z.directions)
    assert [x.symbolic_age_years for x in z.directions] == sorted(
        x.symbolic_age_years for x in z.directions
    )
    assert all(x.direction in ("direct", "converse") for x in z.directions)
    assert (
        z.to_dict()
        == generate_aspect_timeline(
            swiss_snapshot, profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS
        ).to_dict()
    )


def test_latitude_treatment_creates_separate_declared_options(swiss_snapshot) -> None:
    default = generate_aspect_timeline(
        swiss_snapshot,
        profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
        methods=(GeometryMethod.PROPORTIONAL_SEMI_ARC,),
    )
    projected = generate_aspect_timeline(
        swiss_snapshot,
        profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
        methods=(GeometryMethod.PROPORTIONAL_SEMI_ARC,),
        significator_projection=SignificatorProjection.PROJECT_TO_ECLIPTIC,
    )

    def bykey(x):
        return {
            (r.promissor, r.significator, r.ray_aspect, r.ray_offset_branch): r
            for r in x.directions
        }

    a = bykey(default)
    b = bykey(projected)
    both = set(a) & set(b)
    moon_keys = [k for k in both if k[1] == "moon"]
    assert moon_keys
    assert any(abs(a[k].arc_degrees - b[k].arc_degrees) > 0.001 for k in moon_keys)
    assert all(b[k].significator_projection == "project_to_ecliptic" for k in moon_keys)
    angle_keys = [k for k in both if k[1] in ("asc", "mc")]
    assert angle_keys
    assert all(a[k].arc_degrees == pytest.approx(b[k].arc_degrees, abs=1e-10) for k in angle_keys)
    assert all(b[k].significator_projection == "exact_angle" for k in angle_keys)


def test_no_bianchini_and_no_unsupported_mundane_methods(swiss_snapshot) -> None:
    with pytest.raises(ValueError, match="valid"):
        generate_aspect_timeline(
            swiss_snapshot,
            profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
            significator_projection="bianchini_latitude",
        )
    with pytest.raises(ValueError, match="proportional"):
        generate_aspect_timeline(
            swiss_snapshot,
            profile=AspectProfile.MUNDANE_PROPORTIONAL_SEMI_ARC,
            methods=(GeometryMethod.REGIOMONTANIAN_POSITION_CIRCLE,),
        )
    with pytest.raises(ValueError, match="bodily"):
        generate_aspect_timeline(
            swiss_snapshot,
            profile=AspectProfile.MUNDANE_PROPORTIONAL_SEMI_ARC,
            significator_projection=SignificatorProjection.PROJECT_TO_ECLIPTIC,
        )
    with pytest.raises(ValueError, match="at least one"):
        generate_aspect_timeline(
            swiss_snapshot,
            profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS,
            aspects=(),
        )


def test_mundane_semi_arc_aspect_solver_satisfies_phase_equation() -> None:
    rng = random.Random(12024)
    for _ in range(400):
        lat = rng.uniform(-55, 55)
        ramc = rng.uniform(0, 360)
        fixed = EquatorialPoint(rng.uniform(0, 360), rng.uniform(-15, 15))
        moving = EquatorialPoint(rng.uniform(0, 360), rng.uniform(-15, 15))
        aspect = rng.choice(list(RayAspect))
        branch = rng.choice(aspect_branches(aspect))
        arc = mundane_semi_arc_phase_arc(lat, ramc, fixed, moving, aspect=aspect, branch=branch)
        ds1, ns1 = _semi_arcs(lat, fixed.dec_deg)
        ds2, ns2 = _semi_arcs(lat, moving.dec_deg)
        phase1 = _phase(fixed.ra_deg - ramc, ds1, ns1)
        expected_phase = normalize(
            phase1
            + (1 if branch is RayBranch.POSITIVE else -1)
            * {
                RayAspect.SEXTILE: 60,
                RayAspect.SQUARE: 90,
                RayAspect.TRINE: 120,
                RayAspect.OPPOSITION: 180,
            }[aspect]
        )
        encountered_phase = _phase(moving.ra_deg - arc - ramc, ds2, ns2)
        assert abs((encountered_phase - expected_phase + 180) % 360 - 180) < 1e-8


def test_mundane_aspect_zero_offset_matches_existing_conjunction_equation() -> None:
    from hdmatch.astrology.geometry import proportional_semi_arc

    lat, ramc = 45.0, 0.0
    fixed = EquatorialPoint(50, 15)
    moving = EquatorialPoint(80, -10)
    # For 0 offset the frozen geometry must recover the existing algorithm;
    # use phase calculation directly as the exact reference.
    day, night = _semi_arcs(lat, fixed.dec_deg)
    moving_day, moving_night = _semi_arcs(lat, moving.dec_deg)
    phase = _phase(fixed.ra_deg - ramc, day, night)
    from hdmatch.astrology.geometry import _hour_angle

    raw = (moving.ra_deg - ramc - _hour_angle(phase, moving_day, moving_night)) % 360
    assert raw == pytest.approx(proportional_semi_arc(lat, ramc, fixed, moving), abs=1e-12)


def test_profile_specific_error_messages_on_missing_sky_data(swiss_snapshot) -> None:
    from dataclasses import replace

    incomplete = replace(swiss_snapshot, ecliptic_positions=(), true_obliquity_deg=None)
    with pytest.raises(ValueError, match="require Swiss ecliptic"):
        generate_aspect_timeline(incomplete, profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS)
    assert (
        generate_aspect_timeline(
            incomplete,
            profile=AspectProfile.MUNDANE_PROPORTIONAL_SEMI_ARC,
        ).evaluated
        == 392
    )


def test_cli_exposes_profiles_and_preserves_output_file_safety(
    swiss_snapshot, tmp_path: Path
) -> None:
    from hdmatch.astrology.cli import main

    outfile = tmp_path / "aspects.json"
    args = [
        "--utc",
        "2000-01-01T12:00:00Z",
        "--latitude",
        "45",
        "--longitude-east",
        "0",
        "--ephemeris-dir",
        str(EPHE),
        "--profile",
        "zodiacal_promissor_rays",
        "--method",
        "placidean_under_pole",
        "--significator-projection",
        "project_to_ecliptic",
        "--output",
        str(outfile),
    ]
    assert main(args) == 0
    report = json.loads(outfile.read_text())
    assert report["scope"]["profile"] == AspectProfile.ZODIACAL_PROMISSOR_RAYS.value
    assert report["scope"]["method_names"] == ["placidean_under_pole"]
    assert report["scope"]["significator_projection"] == "project_to_ecliptic"
    old = outfile.read_bytes()
    with pytest.raises(SystemExit) as exc:
        main(args)
    assert exc.value.code == 2
    assert outfile.read_bytes() == old


def test_cli_mundane_disallows_unsupported_regio_projection(swiss_snapshot, tmp_path: Path) -> None:
    from hdmatch.astrology.cli import main

    args = [
        "--utc",
        "2000-01-01T12:00:00Z",
        "--latitude",
        "45",
        "--longitude-east",
        "0",
        "--ephemeris-dir",
        str(EPHE),
        "--profile",
        "mundane_proportional_semi_arc",
        "--method",
        "regiomontanian_position_circle",
        "--output",
        str(tmp_path / "must_not_exist.json"),
    ]
    with pytest.raises(SystemExit) as exc:
        main(args)
    assert exc.value.code == 2
    assert not (tmp_path / "must_not_exist.json").exists()
