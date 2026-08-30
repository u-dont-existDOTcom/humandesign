from __future__ import annotations

import importlib
from dataclasses import fields
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.chart.bodygraph import Bodygraph, GateActivation
from hdmatch.chart.boundaries import enumerate_chart_boundaries
from hdmatch.chart.calculator import (
    ChartComputation,
    ChartEngineMetadata,
    StableActivation,
    StableChartFeatures,
)
from hdmatch.chart.design_moment import DesignMomentResult
from hdmatch.chart.ephemeris import CelestialBody, EphemerisMetadata, SwissEphemerisProvider
from hdmatch.chart.rave_mandala import MandalaPosition
from hdmatch.natal_time.conformance import (
    FieldClassification,
    audit_swiss_temporal_resolution,
    build_engine_field_inventory,
    independently_enumerate_line_transitions,
)
from hdmatch.runtime.chart_adapter import declared_ephemeris_files

PROJECT_ROOT = Path(__file__).parents[2]
RUNTIME_CLASSES = (
    ChartComputation,
    ChartEngineMetadata,
    StableActivation,
    StableChartFeatures,
    GateActivation,
    Bodygraph,
    DesignMomentResult,
    MandalaPosition,
    EphemerisMetadata,
)


def test_field_inventory_covers_every_canonical_runtime_dataclass_field() -> None:
    inventory = build_engine_field_inventory()
    expected = {
        f"{runtime_class.__name__}.{field.name}"
        for runtime_class in RUNTIME_CLASSES
        for field in fields(runtime_class)
    }
    actual = {item.source_field for item in inventory.fields}

    assert actual == expected
    assert inventory.complete_against_runtime_dataclasses is True
    assert any(
        item.classification is FieldClassification.UNSUPPORTED_OR_UNAVAILABLE
        and item.source_field == "MandalaPosition.color"
        for item in inventory.fields
    )
    assert all(
        item.exclusion_reason is None
        for item in inventory.fields
        if item.included_in_interval_identity
    )
    assert all(
        item.exclusion_reason for item in inventory.fields if not item.included_in_interval_identity
    )


def test_actual_swiss_temporal_grid_is_measured_without_microsecond_claim() -> None:
    files = declared_ephemeris_files(PROJECT_ROOT / "data" / "ephemeris")
    required = {"sepl_18.se1", "semo_18.se1"}
    if not required.issubset({item.name for item in files}):
        pytest.skip("verified local Swiss ephemeris files are unavailable")
    swe = importlib.import_module("swisseph")
    provider = SwissEphemerisProvider(files)

    audit = audit_swiss_temporal_resolution(provider, swe)

    assert audit.adjacent_python_microseconds_are_distinguishable is False
    assert audit.astronomical_microsecond_precision_claimed is False
    assert audit.maximum_observed_equal_julian_day_coordinate_span_microseconds == 40
    assert all(item.julian_day_ulp_microseconds > 40 for item in audit.samples)
    assert all(item.julian_day_ulp_microseconds < 41 for item in audit.samples)
    assert all(item.sun_equal_after_one_microsecond for item in audit.samples)
    assert all(not item.sun_equal_after_julian_quantum_ceiling for item in audit.samples)


def test_independent_design_transition_matches_production_on_engine_grid() -> None:
    files = declared_ephemeris_files(PROJECT_ROOT / "data" / "ephemeris")
    required = {"sepl_18.se1", "semo_18.se1"}
    if not required.issubset({item.name for item in files}):
        pytest.skip("verified local Swiss ephemeris files are unavailable")
    provider = SwissEphemerisProvider(files)
    start = datetime(2024, 1, 15, 1, 9, tzinfo=UTC)
    end = datetime(2024, 1, 15, 1, 10, tzinfo=UTC)
    bodies = (CelestialBody.MOON,)

    production = enumerate_chart_boundaries(
        provider,
        start,
        end,
        bodies=bodies,
        root_tolerance_seconds=0.000001,
    )
    independent = independently_enumerate_line_transitions(
        provider,
        start,
        end,
        bodies=bodies,
        design_root_time_tolerance_seconds=0.000001,
    )
    production_keys = tuple(
        (
            item.at_utc,
            item.side,
            item.body,
            item.before_gate,
            item.before_line,
            item.after_gate,
            item.after_line,
        )
        for item in production
    )
    independent_keys = tuple(
        (
            item.at_utc,
            item.side,
            item.body,
            item.before_gate,
            item.before_line,
            item.after_gate,
            item.after_line,
        )
        for item in independent.transitions
    )

    assert production_keys == independent_keys
    assert len(production_keys) == 1
    assert production_keys[0][1:3] == ("design", bodies[0])
