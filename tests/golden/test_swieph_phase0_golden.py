from __future__ import annotations

import json
import os
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from hdmatch.century_cache import (
    CACHEABLE_M0_M2_FEATURE_COLUMNS,
    CenturyCacheBoundaryAuditReport,
    CenturyCacheBuildSpec,
    CenturyCacheEngineProvenance,
    CenturyCacheEvidenceInputs,
    CenturyCacheParityReport,
    CenturyCacheShardInput,
    assemble_verified_exact_shard_set,
    build_verified_exact_state_batch,
    feature_registry_sha256,
    iter_verified_century_cache_rows,
    write_century_cache_explicit,
)
from hdmatch.century_cache.parity import (
    CenturyCacheParityGenerationError,
    generate_swieph_golden_parity_report,
)
from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.ephemeris import (
    DEFAULT_ACTIVATION_BODIES,
    CelestialBody,
    EphemerisFallbackError,
    EphemerisMode,
    SwissEphemerisProvider,
)
from hdmatch.chart.rave_mandala import longitude_to_gate_line
from hdmatch.cli import main
from hdmatch.experiments.canonical import sha256_file, write_new_canonical_json
from hdmatch.provenance.swisseph_files import verify_ephemeris_directory

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


def test_real_swieph_bounded_exact_cache_writes_and_reverifies(
    production_provider: SwissEphemerisProvider,
    tmp_path: Path,
) -> None:
    """Exercise exact boundaries -> M2 rows -> proof-bound Parquet -> verifier.

    This deliberately covers six hours, not the century.  It is the Phase-1
    production-engine proof fixture and must never be presented as the canonical
    century cache or as a behavioral ranking.
    """

    start = datetime(1985, 1, 29, 10, tzinfo=UTC)
    end = start + timedelta(hours=6)
    exact_batch = build_verified_exact_state_batch(
        production_provider,
        start,
        end,
    )
    exact_shard_set = assemble_verified_exact_shard_set((exact_batch,))
    assert len(exact_batch.rows) > 1
    assert exact_batch.provenance.boundary_event_count > 0

    golden = _load_json(GOLDEN_PATH)
    returned_flags: set[int] = set()
    comparison_count = 0
    max_error = 0.0
    for sample in golden["representative_positions"]:
        instant = _parse_utc(sample["utc"])
        for body in DEFAULT_ACTIVATION_BODIES:
            calculation = production_provider.position_with_provenance(body, instant)
            expected = sample["positions"][body.value]
            error = abs(calculation.position.longitude - float(expected["longitude"]))
            max_error = max(max_error, error)
            comparison_count += 1
            returned_flags.add(calculation.provenance.returned_flags)
            gate_line = longitude_to_gate_line(calculation.position.longitude)
            assert (gate_line.gate, gate_line.line) == (
                expected["gate"],
                expected["line"],
            )

    ephemeris_directory = Path(production_provider.metadata.files[0].path).parent
    source_manifest_path = PROJECT_ROOT / "data" / "ephemeris" / "manifest.json"
    ephemeris_provenance = verify_ephemeris_directory(
        source_manifest_path=source_manifest_path,
        ephemeris_directory=ephemeris_directory,
    )
    engine_validation_path = (
        PROJECT_ROOT
        / "reports"
        / "v4_3_migration"
        / "phase0_engine_validation.json"
    )
    engine_validation_sha256 = sha256_file(engine_validation_path)
    reference_locator = "tests/golden/fixtures/swieph_phase0_golden_v1.json"
    reference_sha256 = sha256_file(GOLDEN_PATH)

    parity = CenturyCacheParityReport(
        schema_version="century-cache-parity-report-v1",
        validation_status="pass",
        engine_validation_sha256=engine_validation_sha256,
        ephemeris_file_set_sha256=ephemeris_provenance.ephemeris_file_set_sha256,
        feature_vector_schema_version=(
            exact_shard_set.provenance.feature_vector_schema_version
        ),
        utc_start=start,
        utc_end_exclusive=end,
        reference_source_locator=reference_locator,
        reference_source_sha256=reference_sha256,
        comparison_count=comparison_count,
        mismatch_count=0,
        tolerance_degrees=1e-9,
        max_abs_longitude_error_degrees=max_error,
    )
    parity_path = tmp_path / "parity-report.json"
    write_new_canonical_json(parity_path, parity)

    exact = exact_shard_set.provenance
    boundary_audit = CenturyCacheBoundaryAuditReport(
        schema_version="century-cache-boundary-audit-report-v1",
        validation_status="pass",
        engine_validation_sha256=engine_validation_sha256,
        logical_universe_sha256=exact.logical_universe_sha256,
        semantic_feature_registry_sha256=exact.semantic_feature_registry_sha256,
        feature_registry_sha256=exact.feature_registry_sha256,
        mandala_mapping_sha256=exact.mandala_mapping_sha256,
        bodygraph_mapping_sha256=exact.bodygraph_mapping_sha256,
        boundary_policy_version=exact.boundary_policy_version,
        design_root_time_tolerance_seconds=exact.design_root_time_tolerance_seconds,
        design_root_arc_tolerance_degrees=exact.design_root_arc_tolerance_degrees,
        utc_start=start,
        utc_end_exclusive=end,
        interval_count=exact.interval_count,
        audited_boundary_event_count=exact.boundary_event_count,
        missing_boundary_count=0,
        gap_count=0,
        overlap_count=0,
        maximality_violation_count=0,
    )
    boundary_audit_path = tmp_path / "boundary-audit-report.json"
    write_new_canonical_json(boundary_audit_path, boundary_audit)

    metadata = production_provider.metadata
    assert metadata.requested_flags is not None
    assert metadata.ephemeris_mask is not None
    engine = CenturyCacheEngineProvenance(
        provider="swiss_ephemeris_local_files",
        chart_engine_version=exact.chart_engine_version,
        swiss_library_version=metadata.library_version,
        engine_validation_sha256=engine_validation_sha256,
        ephemeris_provenance=ephemeris_provenance,
        ephemeris_requested="SWIEPH",
        ephemeris_returned="SWIEPH",
        requested_flags=metadata.requested_flags,
        returned_flags_observed=tuple(sorted(returned_flags)),
        ephemeris_mask=metadata.ephemeris_mask,
        swieph_flag=metadata.requested_flags & metadata.ephemeris_mask,
    )
    spec = CenturyCacheBuildSpec(
        feature_vector_schema_version=exact.feature_vector_schema_version,
        utc_start=start,
        utc_end_exclusive=end,
        feature_registry=CACHEABLE_M0_M2_FEATURE_COLUMNS,
        semantic_feature_registry_sha256=exact.semantic_feature_registry_sha256,
        feature_registry_sha256=feature_registry_sha256(
            CACHEABLE_M0_M2_FEATURE_COLUMNS
        ),
        required_feature_coverage=1.0,
        calculation_tier="M2",
        exact_intervals=True,
        engine=engine,
        node_convention="true",
        mandala_mapping_version=exact.mandala_mapping_version,
        mandala_mapping_sha256=exact.mandala_mapping_sha256,
        bodygraph_mapping_sha256=exact.bodygraph_mapping_sha256,
        boundary_policy_version=exact.boundary_policy_version,
        design_root_time_tolerance_seconds=exact.design_root_time_tolerance_seconds,
        design_root_arc_tolerance_degrees=exact.design_root_arc_tolerance_degrees,
        parity_status="pass",
        parity_report_sha256=sha256_file(parity_path),
        parity_reference_source_locator=reference_locator,
        parity_reference_source_sha256=reference_sha256,
        boundary_audit_status="pass",
        boundary_audit_report_sha256=sha256_file(boundary_audit_path),
        generation_commit="4dce7708afefdaaff4660f44298880fe8ba6b849",
        created_at_utc=datetime(2026, 8, 22, tzinfo=UTC),
    )
    verified = write_century_cache_explicit(
        tmp_path / "bounded-cache",
        spec=spec,
        exact_shard_set=exact_shard_set,
        shards=(
            CenturyCacheShardInput(
                filename="states-bounded.parquet.zst",
                rows=exact_batch.rows,
            ),
        ),
        evidence=CenturyCacheEvidenceInputs(
            engine_validation_path=engine_validation_path,
            parity_report_path=parity_path,
            boundary_audit_report_path=boundary_audit_path,
            parity_reference_source_path=GOLDEN_PATH,
            ephemeris_source_manifest_path=source_manifest_path,
            ephemeris_directory=ephemeris_directory,
        ),
        build_mode="explicit_rebuild",
    )

    assert verified.required_feature_coverage == 1.0
    assert tuple(iter_verified_century_cache_rows(verified)) == exact_batch.rows
    assert verified.manifest.exact_state_provenance == exact


def test_validate_engine_cli_writes_path_free_manifest_binding(
    production_provider: SwissEphemerisProvider,
    tmp_path: Path,
) -> None:
    ephemeris_directory = Path(production_provider.metadata.files[0].path).parent
    output = tmp_path / "engine-validation.json"

    result = main(
        (
            "validate-engine",
            "--ephemeris-mode",
            "swiss",
            "--ephemeris-path",
            str(ephemeris_directory),
            "--source-manifest",
            str(PROJECT_ROOT / "data" / "ephemeris" / "manifest.json"),
            "--output",
            str(output),
        )
    )

    assert result == 0
    receipt = _load_json(output)
    assert receipt["validation_status"] == "pass"
    assert receipt["ephemeris_mode_argument"] == "SWIEPH"
    assert receipt["engine_validation"]["ephemeris_requested"] == "SWIEPH"
    assert receipt["engine_validation"]["ephemeris_returned"] == "SWIEPH"
    assert len(receipt["engine_validation"]["calculation_probes"]) == 33
    assert len(receipt["engine_validation"]["design_root_probes"]) == 3
    assert receipt["ephemeris_provenance"]["source_commit"] == (
        "3fd0f956d73898b91cc4f67cf18b21af656d1342"
    )
    serialized = output.read_text(encoding="utf-8")
    assert str(ephemeris_directory.resolve()) not in serialized


def test_production_parity_report_is_generated_from_exact_reference_bytes(
    production_provider: SwissEphemerisProvider,
    tmp_path: Path,
) -> None:
    ephemeris_directory = Path(production_provider.metadata.files[0].path).parent
    ephemeris_provenance = verify_ephemeris_directory(
        source_manifest_path=PROJECT_ROOT / "data" / "ephemeris" / "manifest.json",
        ephemeris_directory=ephemeris_directory,
    )
    golden = _load_json(GOLDEN_PATH)
    start = _parse_utc(golden["universe"]["start_inclusive"])
    end = _parse_utc(golden["universe"]["end_exclusive"])
    report = generate_swieph_golden_parity_report(
        production_provider,
        ephemeris_provenance,
        golden_reference_path=GOLDEN_PATH,
        reference_source_locator="tests/golden/fixtures/swieph_phase0_golden_v1.json",
        engine_validation_sha256=sha256_file(
            PROJECT_ROOT
            / "reports"
            / "v4_3_migration"
            / "phase0_engine_validation.json"
        ),
        feature_vector_schema_version="chart-feature-vector-v2",
        utc_start=start,
        utc_end_exclusive=end,
    )

    assert report.validation_status == "pass"
    assert report.comparison_count == (
        len(golden["representative_positions"]) * len(DEFAULT_ACTIVATION_BODIES)
    )
    assert report.mismatch_count == 0
    assert report.reference_source_sha256 == sha256_file(GOLDEN_PATH)

    changed = json.loads(GOLDEN_PATH.read_bytes())
    changed["representative_positions"][0]["positions"]["sun"]["longitude"] += 0.01
    changed_path = tmp_path / "changed-golden.json"
    write_new_canonical_json(changed_path, changed)
    with pytest.raises(CenturyCacheParityGenerationError, match="1 mismatches"):
        generate_swieph_golden_parity_report(
            production_provider,
            ephemeris_provenance,
            golden_reference_path=changed_path,
            reference_source_locator="changed-golden.json",
            engine_validation_sha256="0" * 64,
            feature_vector_schema_version="chart-feature-vector-v2",
            utc_start=start,
            utc_end_exclusive=end,
        )


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
