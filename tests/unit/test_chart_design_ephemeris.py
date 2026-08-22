from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.chart.boundaries import build_production_chart_state_intervals
from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.design_moment import (
    solve_design_moment,
    solve_personality_moment_from_design,
)
from hdmatch.chart.engine_probe import validate_production_engine
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


def test_exact_design_relation_round_trips_through_inverse_solver() -> None:
    birth = datetime(2020, 1, 1, 12, tzinfo=UTC)
    provider = LinearProvider(birth)

    design = solve_design_moment(provider, birth)
    recovered = solve_personality_moment_from_design(provider, design.design_utc)

    assert abs((recovered.birth_utc - birth).total_seconds()) <= 0.01
    assert recovered.design_utc == design.design_utc
    assert recovered.solved_arc_degrees == pytest.approx(
        88.0,
        abs=recovered.arc_tolerance_degrees,
    )


def test_discrete_chart_hash_ignores_continuous_longitude_drift() -> None:
    birth = datetime(2020, 1, 1, 12, tzinfo=UTC)
    provider = LinearProvider(birth)

    first = calculate_chart(provider, birth)
    second = calculate_chart(provider, birth.replace(second=30))

    assert first.activations != second.activations
    assert first.stable_features == second.stable_features
    assert first.chart_features_sha256 == second.chart_features_sha256


class FakeSwiss:
    FLG_JPLEPH = 1
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
        self.calc_calls: list[tuple[object, ...]] = []

    def set_ephe_path(self, path: str) -> None:
        self.ephe_path = path

    def julday(self, *_args: object) -> float:
        return 2451545.0

    def calc_ut(self, *_args: object) -> tuple[tuple[float, ...], int]:
        self.calc_calls.append(_args)
        return (12.0, 0.0, 1.0, 0.9, 0.0, 0.0), self.returned_flags

    def get_current_file_data(self, _index: int) -> tuple[str, float, float, int]:
        return str(self.used_file), 0.0, 0.0, 431


class LinearFakeSwiss(FakeSwiss):
    """One-degree-per-day Sun used to exercise the full Design probe."""

    def julday(
        self,
        year: int,
        month: int,
        day: int,
        hour: float,
        _calendar: int,
    ) -> float:
        whole_hour = int(hour)
        remainder_minutes = (hour - whole_hour) * 60.0
        whole_minute = int(remainder_minutes)
        second = (remainder_minutes - whole_minute) * 60.0
        at_utc = datetime(
            year,
            month,
            day,
            whole_hour,
            whole_minute,
            tzinfo=UTC,
        )
        return at_utc.timestamp() / 86400.0 + second / 86400.0

    def calc_ut(self, *args: object) -> tuple[tuple[float, ...], int]:
        self.calc_calls.append(args)
        julian_day = float(args[0])
        return (
            julian_day % 360.0,
            0.0,
            1.0,
            1.0,
            0.0,
            0.0,
        ), self.returned_flags | self.FLG_SPEED


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


@pytest.mark.parametrize(
    ("returned_flags", "returned_label"),
    (
        (0, "UNKNOWN\\(0\\)"),
        (FakeSwiss.FLG_JPLEPH, "JPLEPH"),
        (FakeSwiss.FLG_SWIEPH | FakeSwiss.FLG_JPLEPH, "UNKNOWN\\(3\\)"),
    ),
)
def test_swiss_provider_requires_exact_returned_ephemeris_mask(
    tmp_path: Path,
    returned_flags: int,
    returned_label: str,
) -> None:
    declared = tmp_path / "sepl_18.se1"
    declared.write_bytes(b"declared")
    fake = FakeSwiss(declared, returned_flags)
    provider = SwissEphemerisProvider((declared,), _swe_module=fake)  # type: ignore[arg-type]

    with pytest.raises(EphemerisFallbackError, match=returned_label):
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
    assert provider.metadata.ephemeris_path == str(tmp_path)
    assert provider.metadata.requested_ephemeris is not None
    assert provider.metadata.requested_ephemeris.value == "SWIEPH"
    assert provider.metadata.requested_flags == FakeSwiss.FLG_SWIEPH | FakeSwiss.FLG_SPEED
    assert provider.metadata.ephemeris_mask == (
        FakeSwiss.FLG_JPLEPH | FakeSwiss.FLG_SWIEPH | FakeSwiss.FLG_MOSEPH
    )
    assert fake.ephe_path == str(tmp_path)
    assert fake.calc_calls[-1][2] == FakeSwiss.FLG_SWIEPH | FakeSwiss.FLG_SPEED

    calculation = provider.position_with_provenance(
        CelestialBody.EARTH,
        datetime(2020, 1, 1, tzinfo=UTC),
    )
    assert calculation.provenance.requested_body is CelestialBody.EARTH
    assert calculation.provenance.calculated_body is CelestialBody.SUN
    assert calculation.provenance.requested_mode.value == "SWIEPH"
    assert calculation.provenance.returned_mode.value == "SWIEPH"
    assert calculation.provenance.returned_flags == FakeSwiss.FLG_SWIEPH
    assert calculation.provenance.derivation == "opposition_of_sun"
    assert calculation.provenance.used_file.sha256 == provider.metadata.files[0].sha256


def test_swiss_provider_rejects_declared_file_mutation_after_initialization(
    tmp_path: Path,
) -> None:
    declared = tmp_path / "sepl_18.se1"
    declared.write_bytes(b"declared")
    fake = FakeSwiss(declared, FakeSwiss.FLG_SWIEPH)
    provider = SwissEphemerisProvider((declared,), _swe_module=fake)  # type: ignore[arg-type]
    declared.write_bytes(b"changed")

    with pytest.raises(EphemerisConfigurationError, match="changed after initialization"):
        provider.verify_declared_files_unchanged()


def test_swiss_production_preflight_requires_exact_swieph_request(tmp_path: Path) -> None:
    declared = tmp_path / "sepl_18.se1"
    declared.write_bytes(b"declared")
    fake = FakeSwiss(declared, FakeSwiss.FLG_SWIEPH)
    provider = SwissEphemerisProvider((declared,), _swe_module=fake)  # type: ignore[arg-type]
    provider._requested_flags = FakeSwiss.FLG_JPLEPH | FakeSwiss.FLG_SPEED

    with pytest.raises(EphemerisConfigurationError, match="not exactly SWIEPH"):
        provider.verify_production_configuration()


def test_production_boundary_calculation_rejects_conflicting_returned_mode(
    tmp_path: Path,
) -> None:
    planetary = tmp_path / "sepl_18.se1"
    lunar = tmp_path / "semo_18.se1"
    planetary.write_bytes(b"planetary")
    lunar.write_bytes(b"lunar")
    fake = LinearFakeSwiss(
        planetary,
        FakeSwiss.FLG_SWIEPH | FakeSwiss.FLG_JPLEPH,
    )
    provider = SwissEphemerisProvider(
        (planetary, lunar),
        _swe_module=fake,  # type: ignore[arg-type]
    )
    start = datetime(2000, 1, 1, tzinfo=UTC)

    with pytest.raises(EphemerisFallbackError, match=r"UNKNOWN\(3\)"):
        build_production_chart_state_intervals(
            provider,
            start,
            start + timedelta(minutes=1),
            bodies=(CelestialBody.MERCURY,),
        )


def test_representative_production_probe_records_returned_flags_and_design_root(
    tmp_path: Path,
) -> None:
    planetary = tmp_path / "sepl_18.se1"
    lunar = tmp_path / "semo_18.se1"
    planetary.write_bytes(b"planetary")
    lunar.write_bytes(b"lunar")
    fake = LinearFakeSwiss(planetary, FakeSwiss.FLG_SWIEPH)
    provider = SwissEphemerisProvider(
        (planetary, lunar),
        _swe_module=fake,  # type: ignore[arg-type]
    )
    instant = datetime(2000, 1, 1, 12, tzinfo=UTC)

    result = validate_production_engine(
        provider,
        instants=(instant,),
        bodies=(CelestialBody.SUN, CelestialBody.MERCURY),
    )

    assert result.validation_status == "pass"
    assert result.ephemeris_requested.value == "SWIEPH"
    assert result.ephemeris_returned.value == "SWIEPH"
    assert len(result.calculation_probes) == 2
    assert all(
        probe.returned_flags & result.ephemeris_mask == FakeSwiss.FLG_SWIEPH
        for probe in result.calculation_probes
    )
    assert result.gate_line_deterministic is True
    assert result.design_root_converged is True
    assert len(result.design_root_probes) == 1
    assert abs(result.design_root_probes[0].residual_degrees) <= 1e-8


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
