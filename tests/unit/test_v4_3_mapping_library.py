from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

import hdmatch.model.v4_3.integration as v43_integration
from hdmatch.century_cache.models import CenturyStateRecord, FeatureValue
from hdmatch.chart.feature_registry import (
    FeatureCoverageError,
    FeatureId,
    compile_required_feature_registry,
)
from hdmatch.model.mapping_library import (
    ContradictionSeverity,
    DirectnessClass,
    MappingLibrary,
    StructuralClass,
    load_mapping_library,
)
from hdmatch.model.v4_3.integration import (
    CanonicalV43ScoringSession,
    V43IntegrationError,
    V43ObservedResponse,
    evaluate_mapping_library_v2,
    mapping_prevalence_parent_hierarchy_sha256,
    mapping_prevalence_plan_sha256,
)
from hdmatch.model.v4_3_compiler import (
    compile_mapping_library_v2,
    compile_mapping_library_v2_file,
    verify_mapping_source_artifacts,
)
from hdmatch.model.v4_3_mapping import (
    FLEXIBILITY_FACTOR,
    STRUCTURAL_SALIENCE,
    ContradictionModeV2,
    CoreArchitectureTargetV2,
    CoreTypeStrategyTargetV2,
    FlexibilityClass,
    FrozenMappingRuleSourceV2,
    MappingLibrarySourceV2,
    MappingLibraryV2,
    MappingStatusV2,
    MappingV2Error,
    PathwayRoleV2,
    PredicateOperatorV2,
    PrevalenceParentLevelV2,
    ResponseContradictionV2,
    ResponseRuleV2,
    ResponseSourceModeV2,
    RevisionClassV2,
    SelectionRiskV2,
    SourceArtifactV2,
    SourceCitationV2,
    SourceRoleV2,
    StructuralPathwayV2,
    StructuralPredicateV2,
    load_mapping_library_source_v2,
    load_mapping_library_v2,
    require_mapping_feature_coverage,
)
from hdmatch.util import sha256_file, sha256_json

ROOT = Path(__file__).resolve().parents[2]
NORMATIVE_SOURCE = "reference/core/v4_3_scoring_algorithm.md"
BEHAVIORAL_TARGET = "reference/core/behavioral_target_combined_v3_6.md"


def _citation() -> SourceCitationV2:
    return SourceCitationV2(
        source_id="SRC-V43-SCORING",
        locator="sections 2, 3, 7",
        rationale="The normative V4.3 mapping fields and factor tables.",
    )


def _target_citation() -> SourceCitationV2:
    return SourceCitationV2(
        source_id="SRC-TARGET-V36",
        locator="V3.6 behavioral distinctions",
        rationale="The exact behavioral statement belongs to the frozen V3.6 target.",
    )


def _root_level() -> PrevalenceParentLevelV2:
    return PrevalenceParentLevelV2(level_id="root", parent_feature_ids=())


def _pathway(
    *,
    pathway_id: str,
    predicate: StructuralPredicateV2,
    structural_class: StructuralClass,
    hierarchy: tuple[PrevalenceParentLevelV2, ...],
    flexibility_class: FlexibilityClass = FlexibilityClass.F1,
    flexibility_factor: float = 1.0,
) -> StructuralPathwayV2:
    return StructuralPathwayV2(
        pathway_id=pathway_id,
        predicate=predicate,
        structural_class=structural_class,
        structural_salience=STRUCTURAL_SALIENCE[structural_class],
        directness_class=DirectnessClass.DIRECT,
        mapping_directness=1.0,
        flexibility_class=flexibility_class,
        flexibility_factor=flexibility_factor,
        prevalence_parent_hierarchy=hierarchy,
        sources=(_citation(),),
        rationale="Frozen test pathway with no candidate-outcome input.",
    )


def _source(
    *,
    alternative_pathways: tuple[StructuralPathwayV2, ...] | None = None,
    declared_required_feature_ids: tuple[FeatureId, ...] | None = None,
    bind_question_bank: bool = False,
) -> MappingLibrarySourceV2:
    primary = _pathway(
        pathway_id="PATH-TYPE-PROJECTOR",
        predicate=StructuralPredicateV2(
            feature_id=FeatureId.TYPE,
            operator=PredicateOperatorV2.EQUALS_ANY,
            values=("projector",),
        ),
        structural_class=StructuralClass.TYPE_STRATEGY,
        hierarchy=(_root_level(),),
    )
    channel_hierarchy = (
        PrevalenceParentLevelV2(
            level_id="type_authority",
            parent_feature_ids=(FeatureId.AUTHORITY, FeatureId.TYPE),
        ),
        PrevalenceParentLevelV2(
            level_id="type",
            parent_feature_ids=(FeatureId.TYPE,),
        ),
        _root_level(),
    )
    channel = _pathway(
        pathway_id="PATH-CHANNEL-1-8",
        predicate=StructuralPredicateV2(
            feature_id=FeatureId.COMPLETE_CHANNELS,
            operator=PredicateOperatorV2.CONTAINS_ANY,
            values=("1-8",),
        ),
        structural_class=StructuralClass.COMPLETE_CHANNEL,
        hierarchy=channel_hierarchy,
        flexibility_class=FlexibilityClass.F2,
        flexibility_factor=FLEXIBILITY_FACTOR[FlexibilityClass.F2],
    )
    alternatives = (channel,) if alternative_pathways is None else alternative_pathways
    mapping = FrozenMappingRuleSourceV2(
        rule_id="RULE-TEST-PROJECTOR",
        observation_id="OBS-TEST-ENTRY",
        status=MappingStatusV2.FROZEN,
        behavioral_statement="Interpersonal entry is recognition-sensitive.",
        behavioral_confidence=0.85,
        measurement_reliability=0.9,
        source_dependency_cluster="ENTRY_RECOGNITION",
        dependency_cluster="ENTRY_RECOGNITION",
        pathway_group_id="ENTRY_RECOGNITION",
        pathway_role=PathwayRoleV2.PRIMARY,
        primary_rule_id="RULE-TEST-PROJECTOR",
        elicitation_stage="development_profile",
        revision_class=RevisionClassV2.R1,
        selection_risk=SelectionRiskV2.MODERATE,
        candidate_direction_visible=False,
        question_ids=(("S04",) if bind_question_bank else ()),
        response_rule=ResponseRuleV2(
            response_dimension_id="RESPONSE-ENTRY",
            canonical_response_token="recognition_sensitive",
            support_response_tokens=("recognition_sensitive",),
            unknown_response_tokens=("context_dependent", "unknown"),
            contradiction=ResponseContradictionV2(
                mode=ContradictionModeV2.NONE,
                opposing_response_tokens=(),
                severity=ContradictionSeverity.NONE,
                rationale="No genuinely opposing response is frozen for this test rule.",
            ),
        ),
        primary_pathway=primary,
        alternative_pathways=alternatives,
        corroborating_pathway=None,
        sources=(_target_citation(),),
        rationale="Test-only schema exercise.",
    )
    required = declared_required_feature_ids or tuple(
        sorted(
            (
                FeatureId.AUTHORITY,
                FeatureId.STRATEGY,
                FeatureId.TYPE,
                FeatureId.COMPLETE_CHANNELS,
            ),
            key=lambda item: item.value,
        )
    )
    source_artifacts = [
        SourceArtifactV2(
            source_id="SRC-TARGET-V36",
            role=SourceRoleV2.BEHAVIORAL_TARGET,
            path=BEHAVIORAL_TARGET,
            sha256=sha256_file(ROOT / BEHAVIORAL_TARGET),
            title="Behavioral Target Combined V3.6",
        ),
        SourceArtifactV2(
            source_id="SRC-V43-SCORING",
            role=SourceRoleV2.METHOD,
            path=NORMATIVE_SOURCE,
            sha256=sha256_file(ROOT / NORMATIVE_SOURCE),
            title="V4.3 Canonical Scoring Algorithm",
        ),
    ]
    if bind_question_bank:
        source_artifacts.append(
            SourceArtifactV2(
                source_id="SRC-QUESTION-BANK",
                role=SourceRoleV2.QUESTION_BANK,
                path="docs/08_data_formats.md",
                sha256=sha256_file(ROOT / "docs/08_data_formats.md"),
                title="Test question-bank binding",
            )
        )
    return MappingLibrarySourceV2(
        behavioral_target_source_id="SRC-TARGET-V36",
        method_source_ids=("SRC-V43-SCORING",),
        response_source_mode=(
            ResponseSourceModeV2.QUESTIONNAIRE
            if bind_question_bank
            else ResponseSourceModeV2.DIRECT_BEHAVIORAL_TARGET
        ),
        question_bank_source_id="SRC-QUESTION-BANK" if bind_question_bank else None,
        source_artifacts=tuple(sorted(source_artifacts, key=lambda item: item.source_id)),
        core_architecture_target=CoreArchitectureTargetV2(
            type_strategy=CoreTypeStrategyTargetV2(
                primary_type="projector",
                primary_strategy="wait_for_invitation",
                alternatives=(),
                partial_compatible_types=(),
            ),
            authority=None,
            diagnostic_centers=None,
            profile=None,
            sources=(_target_citation(),),
            rationale="Test-only frozen Type/Strategy CoreFit target.",
        ),
        declared_frozen_rule_ids=(mapping.rule_id,),
        declared_observation_ids=(mapping.observation_id,),
        declared_required_feature_ids=required,
        mappings=(mapping,),
    )


def test_compiler_derives_deterministic_registry_and_pathway_contract() -> None:
    source = _source()
    first = compile_mapping_library_v2(source)
    second = compile_mapping_library_v2(
        MappingLibrarySourceV2.model_validate(source.model_dump(mode="json"))
    )

    assert first == second
    assert first.sha256() == second.sha256()
    assert first.schema_version == "mapping-library-v2"
    assert first.model_version == "V4.3/V3.6-symbolic-v2"
    assert first.required_feature_registry.feature_ids == (
        FeatureId.AUTHORITY,
        FeatureId.STRATEGY,
        FeatureId.TYPE,
        FeatureId.COMPLETE_CHANNELS,
    )
    assert (
        first.required_feature_registry_sha256
        == first.required_feature_registry.sha256()
    )
    channel = first.rules[0].alternative_pathways[0]
    assert channel.anchor_id == channel.predicate.anchor_id
    assert tuple(level.level_id for level in channel.prevalence_parent_hierarchy) == (
        "type_authority",
        "type",
        "root",
    )
    assert channel.required_feature_ids == (
        FeatureId.AUTHORITY,
        FeatureId.TYPE,
        FeatureId.COMPLETE_CHANNELS,
    )


def test_reduced_library_cannot_silently_shrink_frozen_feature_contract() -> None:
    source = _source()
    frozen_rule = source.frozen_mappings[0]
    reduced_rule = frozen_rule.model_copy(update={"alternative_pathways": ()})
    reduced = source.model_copy(update={"mappings": (reduced_rule,)})

    with pytest.raises(MappingV2Error, match="required-feature union differs"):
        compile_mapping_library_v2(reduced)


def test_undeclared_predicate_requirement_fails_compilation() -> None:
    reduced_declaration = _source(
        declared_required_feature_ids=(FeatureId.TYPE,),
    )

    with pytest.raises(MappingV2Error, match="undeclared_required"):
        compile_mapping_library_v2(reduced_declaration)


def test_compiled_library_rejects_reduced_registry_even_with_matching_new_hash() -> None:
    compiled = compile_mapping_library_v2(_source())
    reduced_registry = compile_required_feature_registry((FeatureId.TYPE,))
    payload = compiled.model_dump(mode="json")
    payload["required_feature_registry"] = reduced_registry.model_dump(mode="json")
    payload["required_feature_registry_sha256"] = reduced_registry.sha256()

    with pytest.raises(ValidationError, match="feature union differs"):
        MappingLibraryV2.model_validate(payload)


def test_one_anchor_cannot_fabricate_multiple_prevalence_hierarchies() -> None:
    source = _source()
    rule = source.frozen_mappings[0]
    duplicate = rule.primary_pathway.model_copy(
        update={
            "pathway_id": "PATH-TYPE-PROJECTOR-DUPLICATE",
            "prevalence_parent_hierarchy": (
                PrevalenceParentLevelV2(
                    level_id="type",
                    parent_feature_ids=(FeatureId.TYPE,),
                ),
                _root_level(),
            ),
        }
    )
    changed_rule = rule.model_copy(update={"alternative_pathways": (duplicate,)})
    changed_source = source.model_copy(
        update={
            "declared_required_feature_ids": (FeatureId.STRATEGY, FeatureId.TYPE),
            "mappings": (changed_rule,),
        }
    )

    with pytest.raises(ValidationError, match="multiple prevalence hierarchies"):
        compile_mapping_library_v2(changed_source)


def test_reduced_candidate_vector_fails_before_predicate_scoring() -> None:
    compiled = compile_mapping_library_v2(_source())

    with pytest.raises(FeatureCoverageError, match="below 1.0"):
        require_mapping_feature_coverage(
            {"type": "projector", "authority": "splenic"},
            compiled,
        )


def test_activation_qualifiers_compile_every_required_feature_family() -> None:
    predicate = StructuralPredicateV2(
        feature_id=FeatureId.PLANETARY_ACTIVATIONS,
        operator=PredicateOperatorV2.MATCHES_ACTIVATION,
        side="design",
        carrier="mars",
        gate=61,
        line=2,
    )

    assert predicate.required_feature_ids == (
        FeatureId.PLANETARY_ACTIVATIONS,
        FeatureId.ACTIVATION_GATE,
        FeatureId.ACTIVATION_LINE,
        FeatureId.ACTIVATION_CARRIER,
        FeatureId.ACTIVATION_SIDE,
    )


def test_hanging_gate_requires_edge_state_not_activation_projection() -> None:
    predicate = StructuralPredicateV2(
        feature_id=FeatureId.HANGING_GATES,
        operator=PredicateOperatorV2.HAS_GATE,
        gate=61,
    )

    assert predicate.required_feature_ids == (
        FeatureId.ACTIVE_GATES,
        FeatureId.HANGING_GATES,
    )
    assert FeatureId.ACTIVATION_GATE not in predicate.required_feature_ids


def test_typed_pathway_role_and_primary_linkage_fail_closed() -> None:
    source = _source()
    primary = source.frozen_mappings[0]

    with pytest.raises(ValidationError, match="primary pathway role"):
        FrozenMappingRuleSourceV2.model_validate(
            {
                **primary.model_dump(mode="json"),
                "primary_rule_id": "RULE-MISSING-PRIMARY",
            }
        )
    with pytest.raises(ValidationError, match="pathway group must equal"):
        FrozenMappingRuleSourceV2.model_validate(
            {
                **primary.model_dump(mode="json"),
                "pathway_group_id": "DIFFERENT_GROUP",
            }
        )


def test_predicate_and_prevalence_shapes_fail_closed() -> None:
    with pytest.raises(ValidationError, match="contains predicates require"):
        StructuralPredicateV2(
            feature_id=FeatureId.TYPE,
            operator=PredicateOperatorV2.CONTAINS_ANY,
            values=("projector",),
        )
    with pytest.raises(ValidationError, match="no unambiguous semantics"):
        StructuralPredicateV2(
            feature_id=FeatureId.CENTERS,
            operator=PredicateOperatorV2.EQUALS_ANY,
            values=("sacral",),
        )
    with pytest.raises(ValidationError, match="contains predicates require"):
        StructuralPredicateV2(
            feature_id=FeatureId.PLANETARY_ACTIVATIONS,
            operator=PredicateOperatorV2.CONTAINS_ANY,
            values=("61",),
        )
    with pytest.raises(ValidationError, match="Cross components require exact"):
        StructuralPredicateV2(
            feature_id=FeatureId.CROSS_COMPONENTS,
            operator=PredicateOperatorV2.EQUALS_ANY,
            values=("cross-ish",),
        )
    with pytest.raises(ValidationError, match="must end with an explicit root"):
        _pathway(
            pathway_id="PATH-BAD-BACKOFF",
            predicate=StructuralPredicateV2(
                feature_id=FeatureId.AUTHORITY,
                operator=PredicateOperatorV2.EQUALS_ANY,
                values=("splenic",),
            ),
            structural_class=StructuralClass.AUTHORITY,
            hierarchy=(
                PrevalenceParentLevelV2(
                    level_id="type",
                    parent_feature_ids=(FeatureId.TYPE,),
                ),
            ),
        )
    with pytest.raises(ValidationError, match="flexibility factor"):
        _pathway(
            pathway_id="PATH-BAD-FLEXIBILITY",
            predicate=StructuralPredicateV2(
                feature_id=FeatureId.TYPE,
                operator=PredicateOperatorV2.EQUALS_ANY,
                values=("projector",),
            ),
            structural_class=StructuralClass.TYPE_STRATEGY,
            hierarchy=(_root_level(),),
            flexibility_class=FlexibilityClass.F2,
            flexibility_factor=1.0,
        )
    with pytest.raises(ValidationError, match="requires structural class"):
        _pathway(
            pathway_id="PATH-BAD-SALIENCE-CLASS",
            predicate=StructuralPredicateV2(
                feature_id=FeatureId.TYPE,
                operator=PredicateOperatorV2.EQUALS_ANY,
                values=("projector",),
            ),
            structural_class=StructuralClass.GENERIC_SYMBOLISM,
            hierarchy=(_root_level(),),
        )


def test_source_bindings_are_verified_before_claim_grade_compilation() -> None:
    source = _source()
    verify_mapping_source_artifacts(source, repository_root=ROOT)
    artifact = source.source_artifacts[0].model_copy(update={"sha256": "0" * 64})
    tampered = source.model_copy(update={"source_artifacts": (artifact,)})

    with pytest.raises(MappingV2Error, match="hash mismatch"):
        verify_mapping_source_artifacts(tampered, repository_root=ROOT)


def test_legacy_mapping_artifact_remains_a_legacy_fixture(tmp_path: Path) -> None:
    legacy_path = ROOT / "mappings/mapping_library_v1.json"
    legacy = load_mapping_library(legacy_path)
    assert isinstance(legacy, MappingLibrary)
    copied = tmp_path / "legacy.json"
    copied.write_bytes(legacy_path.read_bytes())

    with pytest.raises(MappingV2Error, match="legacy artifacts are fixtures only"):
        load_mapping_library_source_v2(copied)


def test_file_compiler_writes_exact_canonical_compiled_bytes(tmp_path: Path) -> None:
    source = _source()
    source_path = tmp_path / "mapping-v2-source.json"
    output_path = tmp_path / "mapping-v2.json"
    source_path.write_bytes(source.canonical_bytes())

    compiled = compile_mapping_library_v2_file(
        source_path,
        output_path,
        repository_root=ROOT,
    )

    assert output_path.read_bytes() == compiled.canonical_bytes()
    assert load_mapping_library_v2(output_path) == compiled


def _candidate_row() -> CenturyStateRecord:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    return CenturyStateRecord(
        state_id="state-test",
        utc_start=start,
        utc_end=start + timedelta(seconds=1),
        duration_seconds=1.0,
        representative_utc=start + timedelta(microseconds=1),
        design_timestamp=start - timedelta(days=88),
        chart_features_sha256="1" * 64,
        feature_vector_schema_version="chart-feature-vector-v2",
        semantic_feature_registry_sha256="2" * 64,
        feature_registry_sha256="3" * 64,
        astronomy_engine_version="test-swisseph",
        ephemeris_file_set_sha256="4" * 64,
        node_convention="true",
        mandala_mapping_version="test-mandala",
        mandala_mapping_sha256="5" * 64,
        bodygraph_mapping_sha256="6" * 64,
        feature_values=(
            FeatureValue(feature_id=FeatureId.AUTHORITY.value, value="splenic"),
            FeatureValue(
                feature_id=FeatureId.STRATEGY.value,
                value="wait_for_invitation",
            ),
            FeatureValue(
                feature_id=FeatureId.TYPE.value,
                value="projector",
            ),
            FeatureValue(
                feature_id=FeatureId.COMPLETE_CHANNELS.value,
                value=[
                    {
                        "channel": "1-8",
                        "gate_a": 1,
                        "gate_b": 8,
                        "center_a": "g",
                        "center_b": "throat",
                    }
                ],
            ),
        ),
    )


def test_v2_adapter_derives_pathways_core_and_unknown_without_caller_scores() -> None:
    compiled = compile_mapping_library_v2(_source())
    evaluated = evaluate_mapping_library_v2(
        compiled,
        _candidate_row(),
        (
            V43ObservedResponse(
                observation_id="OBS-TEST-ENTRY",
                response_token="recognition_sensitive",
            ),
        ),
    )

    observation = evaluated.observations[0]
    assert observation.pathways[0].primary.supports_response
    assert observation.pathways[1].primary.supports_response
    assert observation.pathways[0].primary.structural_class.value == "type_strategy"
    assert observation.pathways[1].primary.structural_class.value == "complete_channel"
    core = {item.block.value: item for item in evaluated.core_blocks}
    assert core["type_strategy"].earned_fraction == 1.0
    assert core["authority"].earned_fraction is None

    neutral = evaluate_mapping_library_v2(
        compiled,
        _candidate_row(),
        (
            V43ObservedResponse(
                observation_id="OBS-TEST-ENTRY",
                response_token="unknown",
            ),
        ),
    )
    assert neutral.observations[0].confidence.effective_confidence == 0.0
    assert not any(
        pathway.primary.supports_response
        for pathway in neutral.observations[0].pathways
    )
    neutral_core = {item.block.value: item for item in neutral.core_blocks}
    assert neutral_core["type_strategy"].earned_fraction == 1.0
    assert neutral_core["authority"].earned_fraction is None
    assert neutral_core["diagnostic_centers"].earned_fraction is None
    assert neutral_core["profile"].earned_fraction is None


def test_response_source_mode_fails_closed_without_matching_provenance() -> None:
    questionnaire = _source(bind_question_bank=True)
    payload = questionnaire.model_dump(mode="json")
    payload["question_bank_source_id"] = None
    with pytest.raises(ValidationError, match="questionnaire response mode requires"):
        MappingLibrarySourceV2.model_validate(payload)

    direct = _source()
    payload = direct.model_dump(mode="json")
    mappings = payload["mappings"]
    assert isinstance(mappings, list)
    mappings[0]["question_ids"] = ["S04"]
    with pytest.raises(ValidationError, match="direct-target mappings cannot claim"):
        MappingLibrarySourceV2.model_validate(payload)


def test_dependency_keys_are_exact_and_link_compounds_to_components() -> None:
    channel_1_8 = StructuralPredicateV2(
        feature_id=FeatureId.COMPLETE_CHANNELS,
        operator=PredicateOperatorV2.CONTAINS_ANY,
        values=("1-8",),
    )
    channel_10_20 = StructuralPredicateV2(
        feature_id=FeatureId.COMPLETE_CHANNELS,
        operator=PredicateOperatorV2.CONTAINS_ANY,
        values=("10-20",),
    )
    gate_1 = StructuralPredicateV2(
        feature_id=FeatureId.ACTIVE_GATES,
        operator=PredicateOperatorV2.HAS_GATE,
        gate=1,
    )
    cross = StructuralPredicateV2(
        feature_id=FeatureId.CROSS_COMPONENTS,
        operator=PredicateOperatorV2.EQUALS_ANY,
        values=("1/2|3/4",),
    )
    cardinal = StructuralPredicateV2(
        feature_id=FeatureId.CARDINAL_ACTIVATIONS,
        operator=PredicateOperatorV2.MATCHES_ACTIVATION,
        side="personality",
        carrier="sun",
        gate=1,
    )

    assert not any(key.startswith("feature:") for key in channel_1_8.dependency_keys)
    assert channel_1_8.dependency_keys.isdisjoint(channel_10_20.dependency_keys)
    assert "gate:1" in channel_1_8.dependency_keys & gate_1.dependency_keys
    assert "cardinal:personality:sun:1" in (
        cross.dependency_keys & cardinal.dependency_keys
    )


class _StrictTestPrevalence:
    def __init__(self, provenance: object) -> None:
        self.provenance = provenance

    def bind_candidate_record(
        self,
        candidate_record: object,
        *,
        cache_manifest_sha256: str,
        mapping_library_sha256: str,
    ) -> object:
        assert isinstance(candidate_record, CenturyStateRecord)
        return SimpleNamespace(
            state_id=candidate_record.state_id,
            candidate_record_sha256=sha256_json(
                candidate_record.model_dump(mode="json")
            ),
            cache_manifest_sha256=cache_manifest_sha256,
            universe_sha256=self.provenance.universe_sha256,
            mapping_library_sha256=mapping_library_sha256,
        )

    def estimate(self, anchor_id: str, candidate_context: object) -> object:
        del candidate_context
        return SimpleNamespace(
            anchor_id=anchor_id,
            artifact_sha256=self.provenance.artifact_sha256,
            plan_sha256=self.provenance.plan_sha256,
            mapping_library_sha256=self.provenance.mapping_library_sha256,
            mapping_prevalence_plan_sha256=(
                self.provenance.mapping_prevalence_plan_sha256
            ),
            required_feature_registry_sha256=(
                self.provenance.required_feature_registry_sha256
            ),
            cache_manifest_sha256=self.provenance.cache_manifest_sha256,
            prevalence=0.5,
            numerator_duration_microseconds=1,
            denominator_duration_microseconds=2,
            universe_sha256=self.provenance.universe_sha256,
            policy_version=self.provenance.policy_version,
            parent_hierarchy_sha256=self.provenance.parent_hierarchy_sha256,
            selected_level_id="root",
            backoff_ordinal=0,
            duration_weighted=True,
            conditional=True,
            exact_stable_intervals=True,
            source_scope="declared-global-utc-universe",
        )


def test_canonical_session_binds_identities_and_mints_only_after_complete_universe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    library = compile_mapping_library_v2(_source(bind_question_bank=True))
    candidate = _candidate_row()
    manifest_hash = "a" * 64
    lock_hash = "b" * 64
    universe_hash = "c" * 64
    build_plan_hash = "d" * 64
    reconciliation_hash = "e" * 64
    engine_hash = "f" * 64
    physical_ids = tuple(item.feature_id for item in candidate.feature_values)
    engine = SimpleNamespace(
        ephemeris_requested="SWIEPH",
        ephemeris_returned="SWIEPH",
        engine_validation_sha256=engine_hash,
        chart_engine_version=candidate.astronomy_engine_version,
        ephemeris_provenance=SimpleNamespace(
            ephemeris_file_set_sha256=candidate.ephemeris_file_set_sha256
        ),
    )
    manifest = SimpleNamespace(
        feature_vector_schema_version=candidate.feature_vector_schema_version,
        semantic_feature_registry_sha256=candidate.semantic_feature_registry_sha256,
        feature_registry_sha256=candidate.feature_registry_sha256,
        feature_registry=tuple(SimpleNamespace(feature_id=item) for item in physical_ids),
        build_plan_sha256=build_plan_hash,
        logical_universe_sha256=universe_hash,
        reconciliation_aggregate_sha256=reconciliation_hash,
        boundary_policy_version="boundary-v1",
        engine=engine,
        node_convention=candidate.node_convention,
        mandala_mapping_sha256=candidate.mandala_mapping_sha256,
        bodygraph_mapping_sha256=candidate.bodygraph_mapping_sha256,
        utc_start=candidate.utc_start,
        utc_end_exclusive=candidate.utc_end,
        interval_count=1,
    )
    cache = SimpleNamespace(
        manifest=manifest,
        manifest_sha256=manifest_hash,
        manifest_path=Path("/verified/manifest.json"),
    )
    build_spec_payload = {"frozen": "build-spec"}
    lock = SimpleNamespace(
        manifest_sha256=manifest_hash,
        build_spec=SimpleNamespace(model_dump=lambda mode: build_spec_payload),
        build_spec_sha256=sha256_json(build_spec_payload),
    )
    provenance = SimpleNamespace(
        anchor_ids=tuple(
            sorted(
                pathway.anchor_id
                for rule in library.rules
                for pathway in (
                    rule.primary_pathway,
                    *rule.alternative_pathways,
                )
            )
        ),
        artifact_sha256="1" * 64,
        plan_sha256="2" * 64,
        mapping_library_sha256=library.sha256(),
        mapping_source_library_sha256=library.source_library_sha256,
        mapping_prevalence_plan_sha256=mapping_prevalence_plan_sha256(library),
        required_feature_registry_sha256=library.required_feature_registry_sha256,
        cache_manifest_sha256=manifest_hash,
        cache_trust_lock_sha256=lock_hash,
        cache_build_plan_sha256=build_plan_hash,
        semantic_feature_registry_sha256=candidate.semantic_feature_registry_sha256,
        physical_feature_registry_sha256=candidate.feature_registry_sha256,
        reconciliation_aggregate_sha256=reconciliation_hash,
        engine_validation_sha256=engine_hash,
        ephemeris_file_set_sha256=candidate.ephemeris_file_set_sha256,
        boundary_policy_version="boundary-v1",
        universe_sha256=universe_hash,
        policy_version="conditional-prevalence-v4.3-v1",
        parent_hierarchy_sha256=mapping_prevalence_parent_hierarchy_sha256(library),
        duration_weighted=True,
        conditional=True,
        exact_stable_intervals=True,
        source_scope="declared-global-utc-universe",
    )
    provider = _StrictTestPrevalence(provenance)
    trust_path = Path("/verified/trust-lock.json")
    monkeypatch.setattr(
        v43_integration,
        "sha256_file",
        lambda path: lock_hash if Path(path) == trust_path else manifest_hash,
    )
    monkeypatch.setattr(v43_integration, "load_century_cache_trust_lock", lambda path: lock)
    monkeypatch.setattr(
        v43_integration,
        "verify_century_cache_against_trust_lock",
        lambda cache_directory, trust_lock_path: cache,
    )
    monkeypatch.setattr(
        v43_integration,
        "iter_verified_century_cache_rows",
        lambda verified: iter((candidate,)),
    )
    session = CanonicalV43ScoringSession.open(
        mapping_library=library,
        cache_directory="/verified/cache",
        trust_lock_path=trust_path,
        prevalence=provider,
    )
    evaluation = session.score_candidate(
        candidate,
        (
            V43ObservedResponse(
                observation_id="OBS-TEST-ENTRY",
                response_token="recognition_sensitive",
            ),
        ),
    )

    assert evaluation.ranked_interval.stable_duration_microseconds == 1_000_000
    with pytest.raises(V43IntegrationError, match="complete declared universe"):
        session.require_complete_universe_compliance(())
    forged = replace(evaluation)
    with pytest.raises(V43IntegrationError, match="not minted"):
        session.require_complete_universe_compliance((forged,))
    complete = session.require_complete_universe_compliance((evaluation,))
    assert complete.compliance.v4_3_compliant
    assert complete.scored_candidate_count == 1

    provenance.mapping_library_sha256 = "9" * 64
    with pytest.raises(V43IntegrationError, match="mapping library identity mismatch"):
        CanonicalV43ScoringSession.open(
            mapping_library=library,
            cache_directory="/verified/cache",
            trust_lock_path=trust_path,
            prevalence=provider,
        )
