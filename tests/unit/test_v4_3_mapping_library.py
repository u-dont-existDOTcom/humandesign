from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

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
from hdmatch.model.v4_3_compiler import (
    compile_mapping_library_v2,
    compile_mapping_library_v2_file,
    verify_mapping_source_artifacts,
)
from hdmatch.model.v4_3_mapping import (
    FLEXIBILITY_FACTOR,
    STRUCTURAL_SALIENCE,
    ContradictionModeV2,
    FlexibilityClass,
    FrozenMappingRuleSourceV2,
    MappingLibrarySourceV2,
    MappingLibraryV2,
    MappingStatusV2,
    MappingV2Error,
    PredicateOperatorV2,
    PrevalenceParentLevelV2,
    ResponseContradictionV2,
    ResponseRuleV2,
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
from hdmatch.util import sha256_file

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
        dependency_cluster="ENTRY_RECOGNITION",
        elicitation_stage="development_profile",
        revision_class=RevisionClassV2.R1,
        selection_risk=SelectionRiskV2.MODERATE,
        candidate_direction_visible=False,
        question_ids=("S04",),
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
            (FeatureId.AUTHORITY, FeatureId.TYPE, FeatureId.COMPLETE_CHANNELS),
            key=lambda item: item.value,
        )
    )
    return MappingLibrarySourceV2(
        behavioral_target_source_id="SRC-TARGET-V36",
        method_source_ids=("SRC-V43-SCORING",),
        source_artifacts=(
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


def test_predicate_and_prevalence_shapes_fail_closed() -> None:
    with pytest.raises(ValidationError, match="contains predicates require"):
        StructuralPredicateV2(
            feature_id=FeatureId.TYPE,
            operator=PredicateOperatorV2.CONTAINS_ANY,
            values=("projector",),
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
