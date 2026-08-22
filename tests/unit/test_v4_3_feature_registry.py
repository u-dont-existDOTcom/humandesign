from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from hdmatch.chart.calculator import ChartComputation, calculate_chart
from hdmatch.chart.ephemeris import (
    CelestialBody,
    EclipticPosition,
    EphemerisFile,
    EphemerisMetadata,
    EphemerisMode,
    NodeConvention,
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
    compile_required_feature_registry,
    require_complete_feature_coverage,
    serialize_cacheable_chart_state,
    serialize_chart_feature_vector,
)

_HASH_A = "a" * 64
_HASH_B = "b" * 64
_SOURCE_HASH = "c" * 64


class _DeterministicProvider:
    def __init__(self, epoch: datetime) -> None:
        self.epoch = epoch
        self._metadata = EphemerisMetadata(
            provider="strict-swieph-test",
            library_version="2.10.03",
            files=(
                EphemerisFile("/public/semo_18.se1", _HASH_A, 100),
                EphemerisFile("/public/sepl_18.se1", _HASH_B, 200),
            ),
            calculation_flags=("SEFLG_SWIEPH", "SEFLG_SPEED"),
            coordinate_frame="geocentric_apparent_tropical_ecliptic_of_date",
            node_convention=NodeConvention.TRUE,
            ephemeris_path="/public",
            requested_ephemeris=EphemerisMode.SWIEPH,
            requested_flags=258,
            ephemeris_mask=7,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        days = (at_utc - self.epoch).total_seconds() / 86400.0
        index = list(CelestialBody).index(body)
        if body is CelestialBody.SUN:
            return EclipticPosition((100.0 + days) % 360.0, 1.0)
        if body is CelestialBody.EARTH:
            return EclipticPosition((280.0 + days) % 360.0, 1.0)
        longitude = (17.0 * index + 0.01 * days) % 360.0
        return EclipticPosition(longitude, 0.01)

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        return 1.1 if body in (CelestialBody.SUN, CelestialBody.EARTH) else 0.02

    def min_solar_speed_degrees_per_day(self) -> float:
        return 0.9


@pytest.fixture
def computation() -> ChartComputation:
    birth = datetime(2000, 1, 1, 12, tzinfo=UTC)
    return calculate_chart(_DeterministicProvider(birth), birth)


@pytest.fixture
def vector(computation: ChartComputation) -> ChartFeatureVectorV2:
    return serialize_chart_feature_vector(computation)


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


def test_discrete_feature_hash_does_not_encode_representative_timestamp() -> None:
    birth = datetime(2000, 1, 1, 12, tzinfo=UTC)
    provider = _DeterministicProvider(birth)
    first = serialize_chart_feature_vector(calculate_chart(provider, birth))
    second = serialize_chart_feature_vector(
        calculate_chart(provider, birth + timedelta(seconds=30))
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
        advanced_substructure=advanced,
        advanced_values=values,
    )

    color_registry = compile_required_feature_registry((FeatureId.COLOR,))
    assert require_complete_feature_coverage(
        vector, color_registry
    ).required_feature_coverage == 1.0
    assert FeatureId.TONE not in vector.available_feature_ids

    values.pop("design:pluto")
    with pytest.raises(ValidationError, match="enabled color is missing"):
        serialize_chart_feature_vector(
            computation,
            advanced_substructure=advanced,
            advanced_values=values,
        )


def test_circuitry_is_usable_only_with_complete_sourced_channel_classification(
    computation: ChartComputation,
) -> None:
    plain = serialize_chart_feature_vector(computation)
    circuitry = CircuitryFeatures(
        status=CapabilityStatus.AVAILABLE,
        source_sha256=_SOURCE_HASH,
        channels=tuple(
            ChannelCircuitry(channel=item.channel, circuit="synthetic-test-circuit")
            for item in plain.complete_channels
        ),
    )

    classified = serialize_chart_feature_vector(computation, circuitry=circuitry)
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
            serialize_chart_feature_vector(computation, circuitry=incomplete)


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


def test_cacheable_state_round_trip_binds_interval_registry_and_feature_hash(
    computation: ChartComputation,
) -> None:
    start = computation.personality_utc
    end = start + timedelta(minutes=17)

    state = serialize_cacheable_chart_state(
        computation,
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
) -> None:
    exploratory_ephemeris = replace(
        computation.metadata.ephemeris,
        requested_ephemeris=EphemerisMode.MOSEPH,
    )
    exploratory = replace(
        computation,
        metadata=replace(computation.metadata, ephemeris=exploratory_ephemeris),
    )
    with pytest.raises(FeatureCoverageError, match="explicitly requested SWIEPH"):
        serialize_chart_feature_vector(exploratory)

    unhashed_ephemeris = replace(computation.metadata.ephemeris, files=())
    unhashed = replace(
        computation,
        metadata=replace(computation.metadata, ephemeris=unhashed_ephemeris),
    )
    with pytest.raises(FeatureCoverageError, match="hashed ephemeris files"):
        serialize_chart_feature_vector(unhashed)
