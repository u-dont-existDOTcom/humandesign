from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.design_moment import solve_design_moment
from hdmatch.chart.ephemeris import (
    CelestialBody,
    EclipticPosition,
    EphemerisConfigurationError,
    EphemerisFallbackError,
    EphemerisMetadata,
    NodeConvention,
    SwissEphemerisProvider,
)

REAL_EPHEMERIS_FILES = (
    Path("/tmp/hdmatch-ephe/sepl_18.se1"),
    Path("/tmp/hdmatch-ephe/semo_18.se1"),
)


class LinearProvider:
    def __init__(self, epoch: datetime) -> None:
        self.epoch = epoch
        self._metadata = EphemerisMetadata(
            provider="analytic-test",
            library_version="1",
            files=(),
            calculation_flags=("analytic",),
            coordinate_frame="test",
            node_convention=NodeConvention.TRUE,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        days = (at_utc - self.epoch).total_seconds() / 86400.0
        speed = 1.0 if body in (CelestialBody.SUN, CelestialBody.EARTH) else 0.01
        base = 100.0 + list(CelestialBody).index(body) * 17.0
        return EclipticPosition((base + speed * days) % 360.0, speed)

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        return 1.1 if body in (CelestialBody.SUN, CelestialBody.EARTH) else 0.02

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.9


def test_design_root_is_exact_for_analytic_sun() -> None:
    birth = datetime(2020, 1, 1, 12, tzinfo=UTC)
    provider = LinearProvider(birth)

    result = solve_design_moment(provider, birth)

    assert abs((birth - result.design_utc).total_seconds() - 88 * 86400) < 0.001
    assert result.solved_arc_degrees == pytest.approx(88.0, abs=result.arc_tolerance_degrees)
    assert abs(result.residual_degrees) <= result.arc_tolerance_degrees


def test_discrete_chart_hash_ignores_continuous_longitude_drift() -> None:
    birth = datetime(2020, 1, 1, 12, tzinfo=UTC)
    provider = LinearProvider(birth)

    first = calculate_chart(provider, birth)
    second = calculate_chart(provider, birth.replace(second=30))

    assert first.activations != second.activations
    assert first.stable_features == second.stable_features
    assert first.chart_features_sha256 == second.chart_features_sha256


class FakeSwiss:
    FLG_SWIEPH = 2
    FLG_MOSEPH = 4
    FLG_SPEED = 256
    GREG_CAL = 1
    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9
    TRUE_NODE = 11
    MEAN_NODE = 10
    version = "fake"

    def __init__(self, used_file: Path, returned_flags: int) -> None:
        self.used_file = used_file
        self.returned_flags = returned_flags
        self.ephe_path = ""

    def set_ephe_path(self, path: str) -> None:
        self.ephe_path = path

    def julday(self, *_args: object) -> float:
        return 2451545.0

    def calc_ut(self, *_args: object) -> tuple[tuple[float, ...], int]:
        return (12.0, 0.0, 1.0, 0.9, 0.0, 0.0), self.returned_flags

    def get_current_file_data(self, _index: int) -> tuple[str, float, float, int]:
        return str(self.used_file), 0.0, 0.0, 431


def test_swiss_provider_requires_declared_existing_files(tmp_path: Path) -> None:
    with pytest.raises(EphemerisConfigurationError, match="missing"):
        SwissEphemerisProvider((tmp_path / "sepl_18.se1",))


def test_swiss_provider_rejects_moshier_fallback(tmp_path: Path) -> None:
    ephemeris_file = tmp_path / "sepl_18.se1"
    ephemeris_file.write_bytes(b"declared")
    fake = FakeSwiss(ephemeris_file, FakeSwiss.FLG_MOSEPH)
    provider = SwissEphemerisProvider((ephemeris_file,), _swe_module=fake)  # type: ignore[arg-type]

    with pytest.raises(EphemerisFallbackError, match="Moshier"):
        provider.position(CelestialBody.SUN, datetime(2020, 1, 1, tzinfo=UTC))


def test_swiss_provider_rejects_undeclared_file_use(tmp_path: Path) -> None:
    declared = tmp_path / "sepl_18.se1"
    undeclared = tmp_path / "sepl_24.se1"
    declared.write_bytes(b"declared")
    undeclared.write_bytes(b"undeclared")
    fake = FakeSwiss(undeclared, FakeSwiss.FLG_SWIEPH)
    provider = SwissEphemerisProvider((declared,), _swe_module=fake)  # type: ignore[arg-type]

    with pytest.raises(EphemerisFallbackError, match="undeclared"):
        provider.position(CelestialBody.SUN, datetime(2020, 1, 1, tzinfo=UTC))


def test_swiss_provider_records_hash_and_derives_earth(tmp_path: Path) -> None:
    declared = tmp_path / "sepl_18.se1"
    declared.write_bytes(b"declared")
    fake = FakeSwiss(declared, FakeSwiss.FLG_SWIEPH)
    provider = SwissEphemerisProvider((declared,), _swe_module=fake)  # type: ignore[arg-type]

    earth = provider.position(CelestialBody.EARTH, datetime(2020, 1, 1, tzinfo=UTC))

    assert earth.longitude == 192.0
    assert provider.metadata.files[0].sha256 == (
        "f833228cb8681bbf3e38af9de7a212dfc542b3e3ba1312ec8a45bb2b67605dc7"
    )


@pytest.mark.skipif(
    not all(path.is_file() for path in REAL_EPHEMERIS_FILES),
    reason="official Swiss Ephemeris smoke-test files are not installed",
)
def test_real_swiss_files_pass_strict_used_file_checks() -> None:
    """Fixture provenance: aloistr/swisseph commit 3fd0f956d73898b91cc4f67cf18b21af656d1342."""

    provider = SwissEphemerisProvider(REAL_EPHEMERIS_FILES)
    instant = datetime(1985, 1, 29, tzinfo=UTC)

    sun = provider.position(CelestialBody.SUN, instant)
    moon = provider.position(CelestialBody.MOON, instant)
    node = provider.position(CelestialBody.NORTH_NODE, instant)

    assert sun.longitude == pytest.approx(309.0292946189814, abs=1e-12)
    assert moon.longitude == pytest.approx(37.45341308905593, abs=1e-12)
    assert node.longitude == pytest.approx(54.18370162816338, abs=1e-12)
    hashes = {item.path.rsplit("/", 1)[-1]: item.sha256 for item in provider.metadata.files}
    assert hashes == {
        "semo_18.se1": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
        "sepl_18.se1": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
    }


@pytest.mark.skipif(
    not all(path.is_file() for path in REAL_EPHEMERIS_FILES),
    reason="official Swiss Ephemeris smoke-test files are not installed",
)
def test_real_chart_matches_repository_legacy_engine_record() -> None:
    """Regression evidence only; the legacy record is not independent validation."""

    provider = SwissEphemerisProvider(REAL_EPHEMERIS_FILES)
    birth = datetime(1985, 1, 29, 0, 44, 23, tzinfo=UTC)

    chart = calculate_chart(provider, birth)

    assert (
        abs((chart.design_utc - datetime(1984, 11, 3, 7, 27, 5, tzinfo=UTC)).total_seconds()) < 1.0
    )
    assert chart.bodygraph.type.value == "projector"
    assert chart.bodygraph.authority.value == "splenic"
    assert chart.bodygraph.profile == "2/4"
    assert chart.bodygraph.definition.value == "split_definition"
    assert set(chart.bodygraph.channels) == {"1-8", "23-43", "24-61", "26-44"}
