"""Deterministic Brahe and Placidean solar time-key source/engine tests.

No human natal records; geometry is frozen independently of the timing key.
The historical exactitude is bounded by Gansten's previous research audit
and explicitly documented astronomical/date conventions.
"""

from __future__ import annotations

import copy
import json
import os
import random
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.astrology.aspect_timeline import AspectProfile, generate_aspect_timeline
from hdmatch.astrology.cli import main
from hdmatch.astrology.role_directions import (
    ContactConstruction,
    RotationRegime,
    generate_role_timeline,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files
from hdmatch.astrology.solar_time_keys import (
    SolarRAEngine,
    SolarTimeKey,
    SolarTimeKeyDomainError,
    apply_solar_key,
)
from hdmatch.astrology.timeline import generate_timeline

ROOT = Path(__file__).resolve().parents[2]
EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)


@pytest.fixture(scope="module")
def natal():
    if not EPHE.is_dir():
        pytest.skip("official SWIEPH planetary+Moon files are not available")
    return snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )


@pytest.fixture(scope="module")
def engine(natal):
    return SolarRAEngine(natal, EPHE)


def test_brahe_birth_day_true_midnight_has_strict_bracket(engine) -> None:
    rate, begin, end = engine.birth_date_brahe_rate()
    assert begin < engine.birth_utc < end
    assert begin.isoformat().startswith("2000-01-01T00:03:02")
    assert end.isoformat().startswith("2000-01-02T00:03:31")
    assert rate == pytest.approx(1.1047378415601088, abs=3e-8)
    assert abs(engine._sun_hour_angle_minus_180(begin)) < 2e-6
    assert abs(engine._sun_hour_angle_minus_180(end)) < 2e-6
    assert engine.metadata(SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY).to_dict()[
        "true_solar_midnight_rate_deg_per_symbolic_year"
    ] == pytest.approx(rate)


def test_true_midnight_independently_matches_swiss_lower_transit_three_sites() -> None:
    swe = pytest.importorskip("swisseph")
    root = str(EPHE)
    swe.set_ephe_path(root)
    synthetic = [
        (datetime(2000, 1, 1, 12, tzinfo=UTC), 0.0, 45.0),
        (datetime(2026, 3, 19, 6, tzinfo=UTC), 24.0, 45.0),
        (datetime(2000, 7, 1, 18, tzinfo=UTC), -70.0, -34.0),
    ]
    for birth, lon, lat in synthetic:
        sky = snapshot_from_swiss_files(
            birth,
            latitude_deg=lat,
            longitude_east_deg=lon,
            ephemeris_directory=EPHE,
        )
        clock = SolarRAEngine(sky, EPHE)
        prev, nxt = clock.brahe_midnights()
        for chosen in (prev, nxt):
            status, next_transit = swe.rise_trans(
                clock._jd(chosen) - 0.125,
                swe.SUN,
                swe.CALC_ITRANSIT,
                (lon, lat, 0),
                0,
                15,
                swe.FLG_SWIEPH,
            )
            assert status == 0
            assert abs((next_transit[0] - clock._jd(chosen)) * 86400) < 0.05


def test_brahe_birth_date_is_constant_per_chart_not_mean_rate(engine) -> None:
    rate, _, _ = engine.birth_date_brahe_rate()
    mean = 360.0 / 365.25
    assert abs(rate - mean) > 0.1
    # Brahe uses ONE birth-day rate independent of age, unlike Placidus.
    assert (100 / rate) == pytest.approx(90.5192, abs=0.005)
    assert abs(engine.placidus_age_for_arc(100) - 100 / rate) > 5


def test_placidus_true_solar_arc_age_inverse_across_360_wrap(engine) -> None:
    rng = random.Random(20261024)
    for years in [0, 0.1, 1, 11, 25, 50, 75, 99, 110, 122]:
        arc = engine.true_solar_arc_at_age(years)
        inverted = engine.placidus_age_for_arc(arc)
        assert inverted == pytest.approx(years, abs=2e-7)
        assert engine.true_solar_arc_at_age(inverted) == pytest.approx(arc, abs=2e-7)
    for _ in range(45):
        years = rng.uniform(0.25, 110)
        arc = engine.true_solar_arc_at_age(years)
        inferred = engine.placidus_age_for_arc(arc)
        assert abs(inferred - years) < 2e-7


def test_solar_arc_monotonic_daily_increments(engine) -> None:
    prev = engine.true_solar_arc_at_age(0)
    assert prev == 0
    for d in range(1, 126):
        nxt = engine.true_solar_arc_at_age(float(d))
        assert 0.8 < nxt - prev < 1.15
        prev = nxt
    assert prev > 110


def test_solar_age_domain_and_no_fallback(engine) -> None:
    for arc in (float("nan"), float("inf"), -1, 126):
        with pytest.raises(ValueError):
            engine.placidus_age_for_arc(arc)
    with pytest.raises(ValueError):
        engine.true_solar_arc_at_age(-1)
    with pytest.raises(ValueError):
        engine.true_solar_arc_at_age(130)
    beyond = max(124, engine.true_solar_arc_at_age(125) + 0.1)
    with pytest.raises(SolarTimeKeyDomainError, match="outside"):
        engine.placidus_age_for_arc(beyond)


def test_exact_natal_swiss_file_hash_bound_to_time_key(natal, tmp_path) -> None:
    with pytest.raises(Exception, match="missing"):
        SolarRAEngine(natal, tmp_path)
    real = SolarRAEngine(natal, EPHE)
    assert dict(real.birth.ephemeris_file_sha256) == {
        Path(rec.path).name: rec.sha256 for rec in real.strict.metadata.files
    }
    assert real.strict.metadata.library_version != "unknown"


def test_same_geometry_different_brahe_vs_placidus_age(engine, natal) -> None:
    geometry = generate_timeline(natal, max_age_years=125).to_dict()
    frozen = copy.deepcopy(geometry)
    b = apply_solar_key(
        geometry,
        engine,
        SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY,
        requested_max_age=100,
    )
    p = apply_solar_key(
        geometry,
        engine,
        SolarTimeKey.PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA,
        requested_max_age=100,
    )
    assert geometry == frozen  # no source mutation
    assert len(b["directions"]) == 126
    assert len(p["directions"]) == 114
    assert b["coverage"]["evaluated_method_pair_combinations"] == 168
    assert p["coverage"]["evaluated_method_pair_combinations"] == 168
    for report in (b, p):
        for contact in report["directions"]:
            assert contact["symbolic_age_years"] <= 100
            assert contact["time_key"] == report["solar_time_key"]["method"]
            assert "model_date_utc" in contact
        assert report["coverage"]["source_geometric_oversample_arc_degrees"] == 125.0

    def bykey(rec):
        return rec["method"], rec["promissor"], rec["significator"]

    bb = {bykey(q): q for q in b["directions"]}
    pp = {bykey(q): q for q in p["directions"]}
    shared = set(bb) & set(pp)
    assert shared
    assert all(bb[k]["arc_degrees"] == pp[k]["arc_degrees"] for k in shared)
    assert any(abs(bb[k]["symbolic_age_years"] - pp[k]["symbolic_age_years"]) > 2 for k in shared)


def test_all_contact_families_use_exact_same_fixed_arcs(natal, engine) -> None:
    raw_a = generate_aspect_timeline(
        natal, profile=AspectProfile.ZODIACAL_PROMISSOR_RAYS, max_age_years=125
    ).to_dict()
    raw_r = generate_role_timeline(
        natal,
        construction=ContactConstruction.ZODIACAL_PROMISSOR_RAY,
        regime=RotationRegime.TRADITIONAL_ROLE_REVERSED_CONVERSE,
        max_age_years=125,
    ).to_dict()
    for source in (raw_a, raw_r):
        modified = apply_solar_key(
            source, engine, SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY, requested_max_age=100
        )
        assert modified["directions"]
        assert modified["solar_time_key"]["method"] == "brahe_true_midnight_birth_day"
        assert all(d["time_key"] == "brahe_true_midnight_birth_day" for d in modified["directions"])
        assert all(d["symbolic_age_years"] <= 100 for d in modified["directions"])
        srcarc = {
            (
                x["method"],
                x["promissor"],
                x["significator"],
                x.get("aspect", x.get("ray_aspect")),
                x.get("ray_offset_branch", x.get("aspect_offset_branch")),
            ): x["arc_degrees"]
            for x in source["directions"]
        }
        assert all(
            d["arc_degrees"]
            == srcarc[
                (
                    d["method"],
                    d["promissor"],
                    d["significator"],
                    d.get("aspect", d.get("ray_aspect")),
                    d.get("ray_offset_branch", d.get("aspect_offset_branch")),
                )
            ]
            for d in modified["directions"]
        )


def test_unoversampled_source_refused(natal, engine) -> None:
    source = generate_timeline(natal, max_age_years=100).to_dict()
    with pytest.raises(ValueError, match="125"):
        apply_solar_key(
            source, engine, SolarTimeKey.BRAHE_TRUE_MIDNIGHT_BIRTH_DAY, requested_max_age=100
        )
    with pytest.raises(ValueError, match="100"):
        apply_solar_key(
            generate_timeline(natal, max_age_years=125).to_dict(),
            engine,
            SolarTimeKey.PLACIDUS_CUMULATIVE_TRUE_SOLAR_RA,
            requested_max_age=115,
        )


def test_cli_solar_keys_and_old_default_byte_equivalence(tmp_path) -> None:
    base = [
        "--utc",
        "2000-01-01T12:00:00Z",
        "--latitude",
        "45",
        "--longitude-east",
        "0",
        "--ephemeris-dir",
        str(EPHE),
    ]
    frozen = json.loads(
        (
            ROOT / "docs/astrology-research-map/gansten-primary-timeline-20261024/"
            "examples/synthetic_2000_timeline.json"
        ).read_text()
    )
    default = tmp_path / "default.json"
    assert main(base + ["--output", str(default)]) == 0
    assert json.loads(default.read_text()) == frozen
    for name, count in (
        ("brahe_true_midnight_birth_day", 126),
        ("placidus_cumulative_true_solar_ra", 114),
    ):
        output = tmp_path / f"{name}.json"
        assert main(base + ["--solar-time-key", name, "--output", str(output)]) == 0
        report = json.loads(output.read_text())
        assert len(report["directions"]) == count
        assert report["solar_time_key"]["method"] == name
        assert report["astronomy_provenance"] == frozen["astronomy_provenance"]
        assert all(x["time_key"] == name for x in report["directions"])
    with pytest.raises(SystemExit) as err:
        main(
            base
            + [
                "--solar-time-key",
                "brahe_true_midnight_birth_day",
                "--key",
                "naibod_59m08s_fixed_diagnostic",
                "--output",
                str(tmp_path / "incompatible.json"),
            ]
        )
    assert err.value.code == 2
    assert not (tmp_path / "incompatible.json").exists()
    with pytest.raises(SystemExit) as err:
        main(
            base
            + [
                "--solar-time-key",
                "placidus_cumulative_true_solar_ra",
                "--max-age",
                "120",
                "--output",
                str(tmp_path / "unsupported.json"),
            ]
        )
    assert err.value.code == 2
    assert not (tmp_path / "unsupported.json").exists()


def test_cli_solar_key_on_aspects_and_role_regimes(tmp_path: Path) -> None:
    base = [
        "--utc",
        "2000-01-01T12:00:00Z",
        "--latitude",
        "45",
        "--longitude-east",
        "0",
        "--ephemeris-dir",
        str(EPHE),
        "--max-age",
        "100",
    ]
    arms = [
        ("zodiacal_promissor_rays", None, None),
        ("mundane_proportional_semi_arc", None, None),
        ("role_variants", "zodiacal_promissor_ray", "traditional_role_reversed_converse"),
    ]
    for i, (profile, construction, regime) in enumerate(arms):
        output = tmp_path / f"solar_variants_{i}.json"
        args = base + [
            "--profile",
            profile,
            "--solar-time-key",
            "placidus_cumulative_true_solar_ra",
            "--output",
            str(output),
        ]
        if construction is not None:
            args.extend(["--contact-construction", construction])
        if regime is not None:
            args.extend(["--rotation-regime", regime])
        assert main(args) == 0
        result = json.loads(output.read_text())
        assert result["solar_time_key"]["method"] == "placidus_cumulative_true_solar_ra"
        assert result["coverage"]["max_symbolic_age_years"] == 100
        assert result["directions"]
        assert all(
            record["time_key"] == "placidus_cumulative_true_solar_ra"
            for record in result["directions"]
        )
        assert len(result["directions"]) == len(
            {
                (
                    d["method"],
                    d["promissor"],
                    d["significator"],
                    d.get("ray_aspect", d.get("aspect")),
                    d.get("ray_offset_branch", d.get("aspect_offset_branch")),
                )
                for d in result["directions"]
            }
        )
