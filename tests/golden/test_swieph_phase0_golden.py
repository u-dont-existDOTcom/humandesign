from __future__ import annotations

import json
import os
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.ephemeris import (
    DEFAULT_ACTIVATION_BODIES,
    CelestialBody,
    EphemerisFallbackError,
    EphemerisMode,
    SwissEphemerisProvider,
)
from hdmatch.chart.rave_mandala import longitude_to_gate_line

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = Path(__file__).with_name("fixtures") / "swieph_phase0_golden_v1.json"
NATAL_BASELINE_PATH = (
    PROJECT_ROOT / "reference" / "verified_cases" / "joel_verified_natal_baseline_v2.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _local_ephemeris_files() -> tuple[Path, Path] | None:
    roots: list[Path] = []
    configured = os.environ.get("HDMATCH_TEST_EPHEMERIS_PATH")
    if configured:
        roots.append(Path(configured))
    roots.extend((PROJECT_ROOT / "data" / "ephemeris", Path("/tmp/hdmatch-ephe")))
    for root in roots:
        files = (root / "sepl_18.se1", root / "semo_18.se1")
        if all(path.is_file() for path in files):
            return files
    return None


@pytest.fixture
def production_provider() -> Iterator[SwissEphemerisProvider]:
    files = _local_ephemeris_files()
    if files is None:
        pytest.skip(
            "verified Swiss .se1 files are not provisioned; run "
            "python scripts/fetch_swisseph_ephemeris.py"
        )
    provider = SwissEphemerisProvider(files)
    yield provider


def test_representative_universe_gate_lines_are_deterministic_and_golden(
    production_provider: SwissEphemerisProvider,
) -> None:
    golden = _load_json(GOLDEN_PATH)
    expected_hashes = golden["source"]["files"]
    actual_hashes = {
        Path(item.path).name: item.sha256 for item in production_provider.metadata.files
    }

    assert actual_hashes == expected_hashes
    assert production_provider.metadata.library_version == golden["source"][
        "swiss_library_version"
    ]
    assert production_provider.metadata.calculation_flags[:2] == (
        "SEFLG_SWIEPH",
        "SEFLG_SPEED",
    )

    expected_bodies = {body.value for body in DEFAULT_ACTIVATION_BODIES}
    for sample in golden["representative_positions"]:
        instant = _parse_utc(sample["utc"])
        assert set(sample["positions"]) == expected_bodies
        for body in DEFAULT_ACTIVATION_BODIES:
            expected = sample["positions"][body.value]
            first_calculation = production_provider.position_with_provenance(body, instant)
            second_calculation = production_provider.position_with_provenance(body, instant)
            first = first_calculation.position
            second = second_calculation.position
            first_gate_line = longitude_to_gate_line(first.longitude)
            second_gate_line = longitude_to_gate_line(second.longitude)

            assert first == second
            assert first_calculation.provenance == second_calculation.provenance
            assert first_calculation.provenance.requested_body is body
            assert first_calculation.provenance.requested_mode is EphemerisMode.SWIEPH
            assert first_calculation.provenance.returned_mode is EphemerisMode.SWIEPH
            assert (
                first_calculation.provenance.returned_flags
                & first_calculation.provenance.ephemeris_mask
            ) == (
                first_calculation.provenance.requested_flags
                & first_calculation.provenance.ephemeris_mask
            )
            assert Path(first_calculation.provenance.used_file.path).name in expected_hashes
            assert first.longitude == pytest.approx(expected["longitude"], abs=1e-10)
            assert (first_gate_line.gate, first_gate_line.line) == (
                expected["gate"],
                expected["line"],
            )
            assert first_gate_line == second_gate_line


def test_joel_verified_natal_baseline_and_exact_design_root(
    production_provider: SwissEphemerisProvider,
) -> None:
    baseline = _load_json(NATAL_BASELINE_PATH)
    golden = _load_json(GOLDEN_PATH)["joel_exact_design_root"]
    birth_utc = _parse_utc(baseline["birth_input"]["utc"])

    first = calculate_chart(production_provider, birth_utc)
    second = calculate_chart(production_provider, birth_utc)

    assert birth_utc == _parse_utc(golden["birth_utc"])
    assert first.design_utc == second.design_utc
    assert first.chart_features_sha256 == second.chart_features_sha256
    assert abs((first.design_utc - _parse_utc(golden["design_utc"])).total_seconds()) <= 0.01
    assert first.design_root.target_arc_degrees == golden["target_arc_degrees"]
    assert first.design_root.solved_arc_degrees == pytest.approx(
        golden["target_arc_degrees"],
        abs=golden["arc_tolerance_degrees"],
    )
    assert abs(first.design_root.residual_degrees) <= golden["arc_tolerance_degrees"]
    assert first.design_root.time_tolerance_seconds == golden["time_tolerance_seconds"]
    assert abs((birth_utc - first.design_utc).total_seconds() / 86400.0 - 88.0) > 1.0
    birth_sun = production_provider.position(CelestialBody.SUN, birth_utc).longitude
    design_sun = production_provider.position(CelestialBody.SUN, first.design_utc).longitude
    assert (birth_sun - design_sun) % 360.0 == pytest.approx(
        golden["target_arc_degrees"],
        abs=golden["arc_tolerance_degrees"],
    )

    actual_activations = {
        side: {
            item.body.value: f"{item.gate}.{item.line}"
            for item in first.activations
            if item.side == side
        }
        for side in ("personality", "design")
    }
    assert actual_activations == {
        "personality": {
            key.lower().replace(" ", "_"): value
            for key, value in baseline["personality_activations"].items()
        },
        "design": {
            key.lower().replace(" ", "_"): value
            for key, value in baseline["design_activations"].items()
        },
    }

    properties = baseline["foundational_properties"]
    assert first.bodygraph.type.value == properties["type"].lower()
    assert first.bodygraph.strategy.value == "wait_for_invitation"
    assert first.bodygraph.authority.value == properties["authority"].lower()
    assert first.bodygraph.definition.value == "split_definition"
    assert first.bodygraph.profile == properties["profile"]
    assert set(first.bodygraph.channels) == {
        "-".join(sorted(channel.split("-"), key=int)) for channel in baseline["defined_channels"]
    }
    expected_centers = {
        "Head": "head",
        "Ajna": "ajna",
        "Throat": "throat",
        "G": "g",
        "Ego/Heart": "heart_ego",
        "Spleen": "spleen",
    }
    assert {item.value for item in first.bodygraph.defined_centers} == {
        expected_centers[item] for item in baseline["defined_centers"]
    }


class _MoshierFallbackSwiss:
    FLG_JPLEPH = 1
    FLG_SWIEPH = 2
    FLG_MOSEPH = 4
    FLG_EPHMASK = 7
    FLG_SPEED = 256
    GREG_CAL = 1
    SUN = 0
    version = "fallback-test"

    def __init__(self, declared_file: Path) -> None:
        self.declared_file = declared_file
        self.requested_flags: list[int] = []

    def set_ephe_path(self, _path: str) -> None:
        pass

    def julday(self, *_args: object) -> float:
        return 2451545.0

    def calc_ut(self, _julian_day: float, _body: int, flags: int) -> tuple[tuple[float, ...], int]:
        self.requested_flags.append(flags)
        return (12.0, 0.0, 1.0, 0.9, 0.0, 0.0), self.FLG_MOSEPH | self.FLG_SPEED

    def get_current_file_data(self, _index: int) -> tuple[str, float, float, int]:
        return str(self.declared_file), 0.0, 0.0, 441


def test_requested_swieph_to_returned_moshier_fails_before_coordinates_are_accepted(
    tmp_path: Path,
) -> None:
    declared = tmp_path / "sepl_18.se1"
    declared.write_bytes(b"declared-test-file")
    fake = _MoshierFallbackSwiss(declared)
    provider = SwissEphemerisProvider(
        (declared,),
        _swe_module=fake,  # type: ignore[arg-type]
    )

    with pytest.raises(EphemerisFallbackError, match="Moshier|requested SWIEPH"):
        provider.position(CelestialBody.SUN, datetime(2000, 1, 1, tzinfo=UTC))

    assert fake.requested_flags == [fake.FLG_SWIEPH | fake.FLG_SPEED]
