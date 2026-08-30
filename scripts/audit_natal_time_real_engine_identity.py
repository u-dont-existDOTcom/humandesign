"""Emit a synthetic-only identity and precision packet for the canonical chart engine."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import platform
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hdmatch.chart.bodygraph import bodygraph_constants_sha256
from hdmatch.chart.calculator import CHART_ENGINE_VERSION, calculate_chart
from hdmatch.chart.ephemeris import SwissEphemerisProvider
from hdmatch.chart.rave_mandala import (
    LINE_WIDTH_DEGREES,
    RAVE_MANDALA_START_DEGREES,
    longitude_to_gate_line,
    mandala_constants_sha256,
)
from hdmatch.experiments.canonical import write_new_bytes
from hdmatch.natal_time.conformance import (
    audit_swiss_temporal_resolution,
    build_engine_field_inventory,
)
from hdmatch.natal_time.provenance import timezone_file_sha256
from hdmatch.runtime.chart_adapter import declared_ephemeris_files
from hdmatch.util import canonical_json_bytes, sha256_file, sha256_json

CREATED_AT = datetime(2026, 8, 30, 5, 0, tzinfo=UTC)
SYNTHETIC_REFERENCE_UTC = datetime(2000, 1, 3, 12, 0, tzinfo=UTC)
PINNED_SWISSEPH_COMMIT = "3fd0f956d73898b91cc4f67cf18b21af656d1342"
PINNED_EPHEMERIS_FILES = {
    "semo_18.se1": {
        "sha256": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
        "size_bytes": 1_304_771,
    },
    "sepl_18.se1": {
        "sha256": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
        "size_bytes": 484_061,
    },
}
ENGINE_SOURCE_FILES = (
    "src/hdmatch/chart/bodygraph.py",
    "src/hdmatch/chart/boundaries.py",
    "src/hdmatch/chart/calculator.py",
    "src/hdmatch/chart/design_moment.py",
    "src/hdmatch/chart/ephemeris.py",
    "src/hdmatch/chart/rave_mandala.py",
    "src/hdmatch/runtime/chart_adapter.py",
)
TIMEZONE_FIXTURE_ZONES = (
    "UTC",
    "America/New_York",
    "Australia/Lord_Howe",
    "Africa/Monrovia",
    "Pacific/Apia",
    "Asia/Kathmandu",
)


def _runtime_identity() -> dict[str, Any]:
    facts: dict[str, Any] = {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build": platform.python_build(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "byteorder": sys.byteorder,
        "packages": {
            name: importlib.metadata.version(name) for name in ("pyswisseph", "pydantic", "tzdata")
        },
    }
    return {"facts": facts, "sha256": sha256_json(facts)}


def _source_identity(repository_root: Path) -> dict[str, Any]:
    files = tuple(
        {
            "path": relative,
            "sha256": sha256_file(repository_root / relative),
        }
        for relative in ENGINE_SOURCE_FILES
    )
    return {"files": files, "aggregate_sha256": sha256_json(files)}


def _verify_ephemeris(provider: SwissEphemerisProvider) -> tuple[dict[str, Any], ...]:
    records = tuple(
        {
            "name": Path(item.path).name,
            "sha256": item.sha256,
            "size_bytes": item.size_bytes,
        }
        for item in provider.metadata.files
    )
    actual = {item["name"]: item for item in records}
    if set(actual) != set(PINNED_EPHEMERIS_FILES):
        raise RuntimeError(f"unexpected canonical ephemeris file set: {sorted(actual)}")
    for name, expected in PINNED_EPHEMERIS_FILES.items():
        if actual[name]["sha256"] != expected["sha256"]:
            raise RuntimeError(f"ephemeris digest mismatch: {name}")
        if actual[name]["size_bytes"] != expected["size_bytes"]:
            raise RuntimeError(f"ephemeris size mismatch: {name}")
    return records


def _equality_probe() -> dict[str, Any]:
    import math

    boundary = RAVE_MANDALA_START_DEGREES + 17 * LINE_WIDTH_DEGREES
    before = longitude_to_gate_line(math.nextafter(boundary, -math.inf))
    equal = longitude_to_gate_line(boundary)
    after = longitude_to_gate_line(math.nextafter(boundary, math.inf))
    return {
        "boundary_longitude": boundary,
        "binary64_predecessor": before.longitude,
        "binary64_successor": after.longitude,
        "predecessor_gate_line": [before.gate, before.line],
        "equality_gate_line": [equal.gate, equal.line],
        "successor_gate_line": [after.gate, after.line],
        "equality_enters_new_half_open_sector": (
            (equal.gate, equal.line) == (after.gate, after.line)
            and (before.gate, before.line) != (equal.gate, equal.line)
        ),
    }


def _utc_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def build_packet(
    repository_root: Path,
    repository_commit: str,
    ephemeris_path: Path,
) -> dict[str, Any]:
    provider = SwissEphemerisProvider(declared_ephemeris_files(ephemeris_path))
    ephemeris_files = _verify_ephemeris(provider)
    swe = importlib.import_module("swisseph")
    temporal = audit_swiss_temporal_resolution(provider, swe)
    inventory = build_engine_field_inventory()
    chart = calculate_chart(
        provider,
        SYNTHETIC_REFERENCE_UTC,
        design_time_tolerance_seconds=temporal.design_root_time_tolerance_seconds,
        design_arc_tolerance_degrees=temporal.design_root_arc_tolerance_degrees,
    )
    sample_mandala = longitude_to_gate_line(chart.activations[0].longitude)
    source = _source_identity(repository_root)
    dependency_lock = repository_root / "requirements-dev.lock"
    timezone_files = tuple(
        {"iana_timezone": zone, "sha256": timezone_file_sha256(zone)}
        for zone in TIMEZONE_FIXTURE_ZONES
    )

    provider_metadata = asdict(provider.metadata)
    provider_metadata["files"] = ephemeris_files
    packet: dict[str, Any] = {
        "schema_version": "natal-real-engine-identity-packet-v3",
        "created_at_utc": CREATED_AT.isoformat().replace("+00:00", "Z"),
        "repository_commit": repository_commit,
        "synthetic_only": True,
        "qualification_status": "pending_pro_review",
        "canonical_engine": {
            "chart_engine_version": CHART_ENGINE_VERSION,
            "implementation": "hdmatch.chart.calculator.calculate_chart",
            "runtime_adapter": "hdmatch.runtime.chart_adapter.ExactChartAdapter",
            "selection_status": "unambiguous_repository_default",
            "selection_evidence": (
                "AGENTS.md, runtime adapter, CLI, relationship prediction code, and project "
                "documentation all require strict local-file Swiss Ephemeris; synthetic and "
                "astronomy-reference providers are test/parity surfaces only"
            ),
            "source_identity": source,
        },
        "ephemeris": {
            "upstream_repository": "aloistr/swisseph",
            "upstream_commit": PINNED_SWISSEPH_COMMIT,
            "provider_metadata": provider_metadata,
            "fallback_permitted": False,
        },
        "constants": {
            "mandala_constants_sha256": mandala_constants_sha256(),
            "bodygraph_constants_sha256": bodygraph_constants_sha256(),
        },
        "dependency_lock": {
            "path": "requirements-dev.lock",
            "sha256": sha256_file(dependency_lock),
        },
        "runtime": _runtime_identity(),
        "timezone_database": {
            "version": importlib.metadata.version("tzdata"),
            "fixture_zone_files": timezone_files,
            "aggregate_sha256": sha256_json(timezone_files),
        },
        "temporal_resolution": temporal.model_dump(mode="json"),
        "temporal_resolution_sha256": temporal.content_sha256,
        "mandala_equality_probe": _equality_probe(),
        "field_inventory": inventory.model_dump(mode="json"),
        "field_inventory_sha256": inventory.content_sha256,
        "synthetic_engine_sample": {
            "personality_utc": _utc_text(chart.personality_utc),
            "design_utc": _utc_text(chart.design_utc),
            "design_root": {
                **asdict(chart.design_root),
                "birth_utc": _utc_text(chart.design_root.birth_utc),
                "design_utc": _utc_text(chart.design_root.design_utc),
                "bracket_start_utc": _utc_text(chart.design_root.bracket_start_utc),
                "bracket_end_utc": _utc_text(chart.design_root.bracket_end_utc),
            },
            "activation_count": len(chart.activations),
            "stable_feature_sha256": chart.chart_features_sha256,
            "advanced_substructure": {
                "color": sample_mandala.color,
                "tone": sample_mandala.tone,
                "base": sample_mandala.base,
                "status": sample_mandala.advanced_substructure_status,
            },
        },
        "claim_limits": {
            "astronomical_microsecond_precision": False,
            "human_predictive_validity": False,
            "ranking": False,
            "weights": False,
            "probability": False,
            "relationship_evidence": False,
            "production_qualification": False,
        },
    }
    packet["packet_sha256"] = sha256_json(packet)
    return packet


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository-commit", required=True)
    parser.add_argument("--ephemeris", type=Path, default=Path("data/ephemeris"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.repository_root.resolve(strict=True)
    packet = build_packet(root, args.repository_commit, args.ephemeris)
    encoded = canonical_json_bytes(packet) + b"\n"
    if args.output is None:
        print(encoded.decode(), end="")
    else:
        write_new_bytes(args.output, encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
