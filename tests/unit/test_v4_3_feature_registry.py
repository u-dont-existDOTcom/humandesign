from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

import hdmatch.chart.feature_registry as feature_registry_module
from hdmatch.chart.calculator import ChartComputation, calculate_chart
from hdmatch.chart.ephemeris import (
    CelestialBody,
    EphemerisMode,
    SwissEphemerisProvider,
)
from hdmatch.chart.feature_registry import (
    CACHEABLE_M0_M2_REGISTRY,
    AdvancedField,
    AdvancedSubstructure,
    CacheableChartStateV2,
    CapabilityStatus,
    ChannelCircuitry,
    ChartFeatureVectorV2,
    CircuitryFeatures,
    FeatureCoverageError,
    FeatureId,
    FeatureTier,
    assess_required_feature_coverage,
    cacheable_serialization_session,
    compile_required_feature_registry,
    require_complete_feature_coverage,
    serialize_cacheable_chart_state,
    serialize_chart_feature_vector,
)

_SOURCE_HASH = "c" * 64


class _DeterministicFakeSwiss:
    FLG_JPLEPH = 1
    FLG_SWIEPH = 2
    FLG_MOSEPH = 4
    FLG_EPHMASK = 7
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
    MEAN_NODE = 10
    TRUE_NODE = 11
    version = "deterministic-fake"

    def __init__(self, planetary_file: Path, lunar_file: Path) -> None:
        self.files = (planetary_file, lunar_file)

    def set_ephe_path(self, _path: str) -> None:
        pass

    def julday(self, year: int, month: int, day: int, hour: float, _calendar: int) -> float:
        midnight = datetime(year, month, day, tzinfo=UTC)
        return float(midnight.toordinal()) + hour / 24.0

    def calc_ut(
        self,
        julian_day: float,
        body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]:
        if body == self.SUN:
            longitude, speed = julian_day % 360.0, 1.0
        else:
            longitude, speed = (body * 17.0 + 0.01 * julian_day) % 360.0, 0.01
        return (longitude, 0.0, 1.0, speed, 0.0, 0.0), flags

    def get_current_file_data(self, index: int) -> tuple[str, float, float, int]:
        return str(self.files[index]), 0.0, 0.0, 441


@pytest.fixture
def production_provider(tmp_path: Path) -> SwissEphemerisProvider:
    return _make_production_provider(tmp_path)


def _make_production_provider(root: Path) -> SwissEphemerisProvider:
    root.mkdir(parents=True, exist_ok=True)
    planetary = root / "sepl_18.se1"
    lunar = root / "semo_18.se1"
    planetary.write_bytes(b"deterministic-planetary-test-file")
    lunar.write_bytes(b"deterministic-lunar-test-file")
    fake = _DeterministicFakeSwiss(planetary, lunar)
    return SwissEphemerisProvider(
        (planetary, lunar),
        _swe_module=fake,  # type: ignore[arg-type]
    )


@pytest.fixture
def computation(production_provider: SwissEphemerisProvider) -> ChartComputation:
    birth = datetime(2000, 1, 1, 12, tzinfo=UTC)
    return calculate_chart(production_provider, birth)


@pytest.fixture
def vector(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> ChartFeatureVectorV2:
    return serialize_chart_feature_vector(computation, provider=production_provider)


def test_required_registry_is_canonical_deterministic_and_typed() -> None:
    first = compile_required_feature_registry(
        (FeatureId.ACTIVATION_LINE, FeatureId.TYPE, FeatureId.TYPE)
    )
    second = compile_required_feature_registry(
        (FeatureId.TYPE.value, FeatureId.ACTIVATION_LINE.value)
    )

    assert first == second
    assert first.sha256() == second.sha256()
    assert first.feature_ids == (FeatureId.ACTIVATION_LINE, FeatureId.TYPE)
    assert first.features[0].tier is FeatureTier.M2
    assert first.features[1].tier is FeatureTier.M0
    assert CACHEABLE_M0_M2_REGISTRY.sha256() == (
        "6a081572beec6053fb0af94c70ec47c1389b57da65b08a96603e331992eb23e9"
    )

    with pytest.raises(FeatureCoverageError, match="cannot be empty"):
        compile_required_feature_registry(())
    with pytest.raises(FeatureCoverageError, match="unknown required feature"):
        compile_required_feature_registry(("invented.favorable_feature",))


def test_complete_vector_serializes_every_m0_m2_structural_family(
    computation: ChartComputation,
    vector: ChartFeatureVectorV2,
) -> None:
    assert vector.schema_version == "chart-feature-vector-v2"
    assert vector.calculation_tier == "M2"
    assert vector.feature_registry_sha256 == CACHEABLE_M0_M2_REGISTRY.sha256()
    assert len(vector.activations) == 2 * len(CelestialBody)
    assert tuple(item.position for item in vector.cardinal_activations) == (
        "personality:sun",
        "personality:earth",
        "design:sun",
        "design:earth",
    )
    assert tuple(item.position for item in vector.node_activations) == (
        "personality:north_node",
        "personality:south_node",
        "design:north_node",
        "design:south_node",
    )
    assert {item.channel for item in vector.complete_channels} == set(
        computation.bodygraph.channels
    )
    assert sum(item.activation_count for item in vector.active_gates) == len(
        vector.activations
    )
    assert all(item.activation_count >= 2 for item in vector.repeated_gates)
    assert vector.architecture.definition_components == tuple(
        tuple(center.value for center in component)
        for component in computation.bodygraph.definition_components
    )
    assert set(vector.architecture.defined_centers) | set(
        vector.architecture.undefined_centers
    ) == {
        "head",
        "ajna",
        "throat",
        "g",
        "heart_ego",
        "sacral",
        "solar_plexus",
        "spleen",
        "root",
    }
    assert vector.incarnation_cross.cardinal_component_key == (
        f"{vector.cardinal_activations[0].gate}/{vector.cardinal_activations[1].gate}|"
        f"{vector.cardinal_activations[2].gate}/{vector.cardinal_activations[3].gate}"
    )
    assert vector.incarnation_cross.name_status is CapabilityStatus.UNAVAILABLE_UNVALIDATED
    assert vector.incarnation_cross.name is None
    assert vector.circuitry.status is CapabilityStatus.UNAVAILABLE_UNVALIDATED
    assert vector.circuitry.channels is None
    assert vector.advanced_substructure.status is CapabilityStatus.UNAVAILABLE_UNVALIDATED
    assert vector.advanced_substructure.enabled_fields == ()
    assert vector.provenance.ephemeris_requested is EphemerisMode.SWIEPH
    assert vector.provenance.ephemeris_requested_flags == 258
    assert vector.provenance.ephemeris_mask == 7
    assert {item.name for item in vector.provenance.ephemeris_files} == {
        "semo_18.se1",
        "sepl_18.se1",
    }
    assert require_complete_feature_coverage(
        vector, CACHEABLE_M0_M2_REGISTRY
    ).required_feature_coverage == 1.0


def test_discrete_feature_hash_does_not_encode_representative_timestamp(
    production_provider: SwissEphemerisProvider,
) -> None:
    birth = datetime(2000, 1, 1, 12, tzinfo=UTC)
    first = serialize_chart_feature_vector(
        calculate_chart(production_provider, birth),
        provider=production_provider,
    )
    second = serialize_chart_feature_vector(
        calculate_chart(production_provider, birth + timedelta(seconds=30)),
        provider=production_provider,
    )

    assert first == second
    assert first.sha256() == second.sha256()


def test_conditional_capabilities_fail_closed_until_values_are_validated(
    vector: ChartFeatureVectorV2,
) -> None:
    registry = compile_required_feature_registry(
        (
            FeatureId.TYPE,
            FeatureId.CIRCUITRY_CHANNEL_METADATA,
            FeatureId.CROSS_NAME,
            FeatureId.COLOR,
        )
    )

    coverage = assess_required_feature_coverage(vector, registry)

    assert coverage.required_feature_coverage == 0.25
    assert coverage.missing_feature_ids == (
        FeatureId.COLOR,
        FeatureId.CIRCUITRY_CHANNEL_METADATA,
        FeatureId.CROSS_NAME,
    )
    with pytest.raises(FeatureCoverageError, match="below 1.0"):
        require_complete_feature_coverage(vector, registry)


def test_enabled_advanced_fields_require_values_at_every_activation(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    advanced = AdvancedSubstructure(
        status=CapabilityStatus.AVAILABLE,
        enabled_fields=(AdvancedField.COLOR,),
        source_sha256=_SOURCE_HASH,
    )
    values = {
        f"{side}:{body.value}": {AdvancedField.COLOR: 1}
        for side in ("personality", "design")
        for body in CelestialBody
    }

    vector = serialize_chart_feature_vector(
        computation,
        provider=production_provider,
        advanced_substructure=advanced,
        advanced_values=values,
    )

    color_registry = compile_required_feature_registry((FeatureId.COLOR,))
    assert require_complete_feature_coverage(
        vector, color_registry
    ).required_feature_coverage == 1.0
    assert FeatureId.TONE not in vector.available_feature_ids

    values.pop("design:pluto")
    with pytest.raises(FeatureCoverageError, match="cover exactly every activation"):
        serialize_chart_feature_vector(
            computation,
            provider=production_provider,
            advanced_substructure=advanced,
            advanced_values=values,
        )


def test_advanced_input_rejects_unused_positions_and_fields(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    advanced = AdvancedSubstructure(
        status=CapabilityStatus.AVAILABLE,
        enabled_fields=(AdvancedField.COLOR,),
        source_sha256=_SOURCE_HASH,
    )
    values: dict[str, dict[AdvancedField | str, int]] = {
        f"{side}:{body.value}": {AdvancedField.COLOR: 1}
        for side in ("personality", "design")
        for body in CelestialBody
    }

    with_extra_position = {**values, "personality:invented": {AdvancedField.COLOR: 1}}
    with pytest.raises(FeatureCoverageError, match="cover exactly every activation"):
        serialize_chart_feature_vector(
            computation,
            provider=production_provider,
            advanced_substructure=advanced,
            advanced_values=with_extra_position,
        )

    with_extra_enabled_field = {position: dict(fields) for position, fields in values.items()}
    with_extra_enabled_field["personality:sun"][AdvancedField.TONE] = 1
    with pytest.raises(FeatureCoverageError, match="differ from the enabled field set"):
        serialize_chart_feature_vector(
            computation,
            provider=production_provider,
            advanced_substructure=advanced,
            advanced_values=with_extra_enabled_field,
        )

    with_unknown_field = {position: dict(fields) for position, fields in values.items()}
    with_unknown_field["personality:sun"]["invented"] = 1
    with pytest.raises(FeatureCoverageError, match="unknown advanced field"):
        serialize_chart_feature_vector(
            computation,
            provider=production_provider,
            advanced_substructure=advanced,
            advanced_values=with_unknown_field,
        )


def test_circuitry_is_usable_only_with_complete_sourced_channel_classification(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    plain = serialize_chart_feature_vector(computation, provider=production_provider)
    circuitry = CircuitryFeatures(
        status=CapabilityStatus.AVAILABLE,
        source_sha256=_SOURCE_HASH,
        channels=tuple(
            ChannelCircuitry(channel=item.channel, circuit="synthetic-test-circuit")
            for item in plain.complete_channels
        ),
    )

    classified = serialize_chart_feature_vector(
        computation,
        provider=production_provider,
        circuitry=circuitry,
    )
    circuitry_registry = compile_required_feature_registry(
        (FeatureId.CIRCUITRY_CHANNEL_METADATA,)
    )

    assert require_complete_feature_coverage(
        classified, circuitry_registry
    ).required_feature_coverage == 1.0

    if circuitry.channels:
        incomplete = CircuitryFeatures(
            status=CapabilityStatus.AVAILABLE,
            source_sha256=_SOURCE_HASH,
            channels=circuitry.channels[:-1],
        )
        with pytest.raises(ValidationError, match="classify every complete channel"):
            serialize_chart_feature_vector(
                computation,
                provider=production_provider,
                circuitry=incomplete,
            )


def test_reduced_or_malformed_vectors_cannot_claim_complete_coverage(
    vector: ChartFeatureVectorV2,
) -> None:
    reduced = vector.model_dump(mode="json")
    reduced.pop("complete_channels")
    with pytest.raises(ValidationError, match="complete_channels"):
        ChartFeatureVectorV2.model_validate(reduced)

    missing_activation = vector.model_dump(mode="json")
    missing_activation["activations"] = missing_activation["activations"][:-1]
    with pytest.raises(ValidationError, match="complete M2 activations required"):
        ChartFeatureVectorV2.model_validate(missing_activation)

    coverage = assess_required_feature_coverage(
        {"schema_version": "chart-features-v1", "type": "projector"},
        CACHEABLE_M0_M2_REGISTRY,
    )
    assert coverage.required_feature_coverage == 0.0
    assert coverage.available_count == 0
    with pytest.raises(FeatureCoverageError, match="schema=dict"):
        require_complete_feature_coverage(
            {"schema_version": "chart-features-v1", "type": "projector"},
            CACHEABLE_M0_M2_REGISTRY,
        )


@pytest.mark.parametrize(
    ("field", "replacement"),
    (
        ("type", "manifestor"),
        ("strategy", "inform"),
        ("authority", "sacral"),
        ("profile", "1/3"),
        ("definition", "split_definition"),
    ),
)
def test_declared_architecture_scalars_must_match_mechanical_bodygraph(
    vector: ChartFeatureVectorV2,
    field: str,
    replacement: str,
) -> None:
    payload = vector.model_dump(mode="json")
    payload["architecture"][field] = replacement

    with pytest.raises(ValidationError, match="mechanically derived"):
        ChartFeatureVectorV2.model_validate(payload)


def test_declared_centers_and_components_must_match_mechanical_bodygraph(
    vector: ChartFeatureVectorV2,
) -> None:
    changed_centers = vector.model_dump(mode="json")
    changed_centers["architecture"]["defined_centers"] = ["head", "root"]
    changed_centers["architecture"]["undefined_centers"] = [
        "ajna",
        "g",
        "heart_ego",
        "sacral",
        "solar_plexus",
        "spleen",
        "throat",
    ]
    changed_centers["architecture"]["definition_components"] = [["head", "root"]]
    with pytest.raises(ValidationError, match="mechanically derived"):
        ChartFeatureVectorV2.model_validate(changed_centers)

    changed_components = vector.model_dump(mode="json")
    changed_components["architecture"]["definition_components"] = [
        ["root"],
        ["spleen"],
    ]
    with pytest.raises(ValidationError, match="mechanically derived"):
        ChartFeatureVectorV2.model_validate(changed_components)


def test_incomplete_channel_center_metadata_must_match_frozen_channel_table(
    vector: ChartFeatureVectorV2,
) -> None:
    payload = vector.model_dump(mode="json")
    assert payload["incomplete_channel_edges"]
    payload["incomplete_channel_edges"][0]["active_center"] = "invented-center"

    with pytest.raises(ValidationError, match="Center metadata differs"):
        ChartFeatureVectorV2.model_validate(payload)


def test_cacheable_state_round_trip_binds_interval_registry_and_feature_hash(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    start = computation.personality_utc
    end = start + timedelta(minutes=17)

    state = serialize_cacheable_chart_state(
        computation,
        provider=production_provider,
        utc_start=start,
        utc_end=end,
        boundary_events=("event-a",),
    )
    replay = CacheableChartStateV2.model_validate_json(state.model_dump_json())

    assert replay == state
    assert state.duration_seconds == 17 * 60
    assert state.representative_utc == computation.personality_utc
    assert state.design_timestamp == computation.design_utc
    assert state.chart_features_sha256 == state.chart_features.sha256()
    assert state.feature_registry_sha256 == CACHEABLE_M0_M2_REGISTRY.sha256()
    assert state.boundary_events == ("event-a",)

    changed_hash = state.model_dump(mode="json")
    changed_hash["chart_features_sha256"] = "0" * 64
    with pytest.raises(ValidationError, match="chart-feature hash"):
        CacheableChartStateV2.model_validate(changed_hash)

    changed_duration = state.model_dump(mode="json")
    changed_duration["duration_seconds"] = 1.0
    with pytest.raises(ValidationError, match="duration"):
        CacheableChartStateV2.model_validate(changed_duration)


def test_non_swieph_or_unhashed_computation_cannot_serialize(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    exploratory_ephemeris = replace(
        computation.metadata.ephemeris,
        requested_ephemeris=EphemerisMode.MOSEPH,
    )
    exploratory = replace(
        computation,
        metadata=replace(computation.metadata, ephemeris=exploratory_ephemeris),
    )
    with pytest.raises(FeatureCoverageError, match="metadata differs"):
        serialize_chart_feature_vector(exploratory, provider=production_provider)

    unhashed_ephemeris = replace(computation.metadata.ephemeris, files=())
    unhashed = replace(
        computation,
        metadata=replace(computation.metadata, ephemeris=unhashed_ephemeris),
    )
    with pytest.raises(FeatureCoverageError, match="metadata differs"):
        serialize_chart_feature_vector(unhashed, provider=production_provider)


def test_cacheable_serialization_requires_live_verified_local_swiss_provider(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    with pytest.raises(FeatureCoverageError, match="strict SwissEphemerisProvider"):
        serialize_chart_feature_vector(
            computation,
            provider=object(),  # type: ignore[arg-type]
        )

    changed_path = Path(computation.metadata.ephemeris.files[0].path)
    changed_path.write_bytes(b"changed-after-chart-calculation")
    with pytest.raises(FeatureCoverageError, match="bytes changed"):
        serialize_chart_feature_vector(computation, provider=production_provider)


def test_serialization_session_rejects_entry_file_mutation(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    changed_path = Path(computation.metadata.ephemeris.files[0].path)
    changed_path.write_bytes(b"changed-before-session-entry")

    with (
        pytest.raises(FeatureCoverageError, match="bytes changed"),
        cacheable_serialization_session(production_provider),
    ):
        pytest.fail("mutated ephemeris bytes must fail before session entry")


def test_serialization_session_rejects_exit_mutation_and_use_after_close(
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    session = cacheable_serialization_session(production_provider)
    changed_path = Path(computation.metadata.ephemeris.files[0].path)

    with pytest.raises(FeatureCoverageError, match="bytes changed"), session:
        session.serialize_chart_feature_vector(
            computation,
            provider=production_provider,
        )
        changed_path.write_bytes(b"changed-before-session-exit")

    with pytest.raises(FeatureCoverageError, match="not active"):
        session.serialize_chart_feature_vector(
            computation,
            provider=production_provider,
        )


def test_serialization_session_rejects_provider_mismatch(
    tmp_path: Path,
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    other_provider = _make_production_provider(tmp_path / "other-provider")
    other_computation = calculate_chart(
        other_provider,
        computation.personality_utc,
    )

    with (
        cacheable_serialization_session(production_provider) as session,
        pytest.raises(FeatureCoverageError, match="different provider"),
    ):
        session.serialize_chart_feature_vector(
            other_computation,
            provider=other_provider,
        )


def test_many_session_serializations_hash_files_only_at_entry_and_exit(
    monkeypatch: pytest.MonkeyPatch,
    computation: ChartComputation,
    production_provider: SwissEphemerisProvider,
) -> None:
    original_sha256_file = feature_registry_module.sha256_file
    hashed_paths: list[Path] = []

    def counted_sha256_file(path: str | Path) -> str:
        hashed_paths.append(Path(path))
        return original_sha256_file(path)

    monkeypatch.setattr(feature_registry_module, "sha256_file", counted_sha256_file)

    with cacheable_serialization_session(production_provider) as session:
        vectors = tuple(
            session.serialize_chart_feature_vector(
                computation,
                provider=production_provider,
            )
            for _ in range(25)
        )

    assert len(hashed_paths) == 2 * len(production_provider.metadata.files)
    assert len({vector.sha256() for vector in vectors}) == 1


def test_serialization_session_reverifies_files_when_body_raises(
    monkeypatch: pytest.MonkeyPatch,
    production_provider: SwissEphemerisProvider,
) -> None:
    original_sha256_file = feature_registry_module.sha256_file
    hashed_paths: list[Path] = []

    def counted_sha256_file(path: str | Path) -> str:
        hashed_paths.append(Path(path))
        return original_sha256_file(path)

    monkeypatch.setattr(feature_registry_module, "sha256_file", counted_sha256_file)

    with (
        pytest.raises(RuntimeError, match="synthetic body failure"),
        cacheable_serialization_session(production_provider),
    ):
        raise RuntimeError("synthetic body failure")

    assert len(hashed_paths) == 2 * len(production_provider.metadata.files)
