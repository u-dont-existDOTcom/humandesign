"""Deterministic compiler for the V4.3/V3.6 mapping-library-v2 schema."""

from __future__ import annotations

from pathlib import Path

from hdmatch.chart.feature_registry import compile_required_feature_registry
from hdmatch.model.v4_3_mapping import (
    CompiledCorroboratingPathwayV2,
    CompiledMappingRuleV2,
    CompiledPathwayV2,
    EmpiricalOnlyMappingRuleSourceV2,
    FrozenMappingRuleSourceV2,
    MappingLibrarySourceV2,
    MappingLibraryV2,
    MappingV2Error,
    StructuralPathwayV2,
    UnresolvedMappingRuleSourceV2,
    load_mapping_library_source_v2,
)
from hdmatch.util import sha256_file


def compile_mapping_library_v2(source: MappingLibrarySourceV2) -> MappingLibraryV2:
    """Compile a source library and derive its exact feature contract.

    The declared feature inventory is a frozen anti-reduction contract.  The
    compiler independently derives the union from every primary, alternative,
    corroborating, and prevalence-parent predicate and requires exact equality.
    """

    source = MappingLibrarySourceV2.model_validate(source.model_dump(mode="json"))
    compiled_rules = tuple(_compile_rule(item) for item in source.frozen_mappings)
    if not compiled_rules:
        raise MappingV2Error("a V4.3 mapping library requires at least one frozen rule")
    derived_feature_ids = tuple(
        sorted(
            {
                feature_id
                for rule in compiled_rules
                for pathway in _compiled_pathways(rule)
                for feature_id in pathway.required_feature_ids
            }
            | set(source.core_architecture_target.required_feature_ids),
            key=lambda item: item.value,
        )
    )
    if derived_feature_ids != source.declared_required_feature_ids:
        missing = sorted(
            set(source.declared_required_feature_ids) - set(derived_feature_ids),
            key=lambda item: item.value,
        )
        undeclared = sorted(
            set(derived_feature_ids) - set(source.declared_required_feature_ids),
            key=lambda item: item.value,
        )
        raise MappingV2Error(
            "derived required-feature union differs from frozen declaration; "
            f"unreferenced_declared={[item.value for item in missing]}, "
            f"undeclared_required={[item.value for item in undeclared]}"
        )
    registry = compile_required_feature_registry(derived_feature_ids)
    return MappingLibraryV2(
        source_library_sha256=source.sha256(),
        behavioral_target_source_id=source.behavioral_target_source_id,
        method_source_ids=source.method_source_ids,
        response_source_mode=source.response_source_mode,
        question_bank_source_id=source.question_bank_source_id,
        source_artifacts=source.source_artifacts,
        constants=source.constants,
        core_architecture_target=source.core_architecture_target,
        declared_frozen_rule_ids=source.declared_frozen_rule_ids,
        declared_observation_ids=source.declared_observation_ids,
        required_feature_registry=registry,
        required_feature_registry_sha256=registry.sha256(),
        rules=compiled_rules,
        unresolved_mappings=tuple(
            item
            for item in source.mappings
            if isinstance(item, UnresolvedMappingRuleSourceV2)
        ),
        empirical_only_mappings=tuple(
            item
            for item in source.mappings
            if isinstance(item, EmpiricalOnlyMappingRuleSourceV2)
        ),
    )


def verify_mapping_source_artifacts(
    source: MappingLibrarySourceV2,
    *,
    repository_root: str | Path,
) -> None:
    """Verify every source binding before compiling a claim-bearing library."""

    root = Path(repository_root).resolve()
    for artifact in source.source_artifacts:
        path = (root / artifact.path).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise MappingV2Error(f"source escapes repository root: {artifact.path}") from exc
        if not path.is_file():
            raise MappingV2Error(f"mapping source artifact is missing: {artifact.path}")
        actual = sha256_file(path)
        if actual != artifact.sha256:
            raise MappingV2Error(
                f"mapping source artifact hash mismatch: {artifact.path}; "
                f"expected={artifact.sha256}, actual={actual}"
            )


def compile_verified_mapping_library_v2(
    source: MappingLibrarySourceV2,
    *,
    repository_root: str | Path,
) -> MappingLibraryV2:
    verify_mapping_source_artifacts(source, repository_root=repository_root)
    return compile_mapping_library_v2(source)


def compile_mapping_library_v2_file(
    source_path: str | Path,
    output_path: str | Path,
    *,
    repository_root: str | Path,
) -> MappingLibraryV2:
    """Verify, compile, and write canonical mapping-library-v2 bytes."""

    source = load_mapping_library_source_v2(source_path)
    compiled = compile_verified_mapping_library_v2(
        source,
        repository_root=repository_root,
    )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(compiled.canonical_bytes())
    return compiled


def _compile_rule(source: FrozenMappingRuleSourceV2) -> CompiledMappingRuleV2:
    corroborator = None
    if source.corroborating_pathway is not None:
        corroborator = CompiledCorroboratingPathwayV2(
            pathway=_compile_pathway(source.corroborating_pathway.pathway),
            independent_of_pathway_ids=(
                source.corroborating_pathway.independent_of_pathway_ids
            ),
            independence_rationale=source.corroborating_pathway.independence_rationale,
            contribution_cap=source.corroborating_pathway.contribution_cap,
        )
    return CompiledMappingRuleV2(
        rule_id=source.rule_id,
        observation_id=source.observation_id,
        behavioral_statement=source.behavioral_statement,
        behavioral_confidence=source.behavioral_confidence,
        measurement_reliability=source.measurement_reliability,
        source_dependency_cluster=source.source_dependency_cluster,
        dependency_cluster=source.dependency_cluster,
        pathway_group_id=source.pathway_group_id,
        pathway_role=source.pathway_role,
        primary_rule_id=source.primary_rule_id,
        elicitation_stage=source.elicitation_stage,
        revision_class=source.revision_class,
        selection_risk=source.selection_risk,
        candidate_direction_visible=source.candidate_direction_visible,
        question_ids=source.question_ids,
        response_rule=source.response_rule,
        primary_pathway=_compile_pathway(source.primary_pathway),
        alternative_pathways=tuple(
            _compile_pathway(item) for item in source.alternative_pathways
        ),
        corroborating_pathway=corroborator,
        sources=source.sources,
        rationale=source.rationale,
    )


def _compile_pathway(source: StructuralPathwayV2) -> CompiledPathwayV2:
    return CompiledPathwayV2(
        pathway_id=source.pathway_id,
        anchor_id=source.predicate.anchor_id,
        predicate=source.predicate,
        dependency_keys=tuple(sorted(source.predicate.dependency_keys)),
        structural_class=source.structural_class,
        structural_salience=source.structural_salience,
        directness_class=source.directness_class,
        mapping_directness=source.mapping_directness,
        flexibility_class=source.flexibility_class,
        flexibility_factor=source.flexibility_factor,
        prevalence_parent_hierarchy=source.prevalence_parent_hierarchy,
        required_feature_ids=source.required_feature_ids,
        sources=source.sources,
        rationale=source.rationale,
    )


def _compiled_pathways(rule: CompiledMappingRuleV2) -> tuple[CompiledPathwayV2, ...]:
    pathways = (rule.primary_pathway, *rule.alternative_pathways)
    if rule.corroborating_pathway is not None:
        pathways = (*pathways, rule.corroborating_pathway.pathway)
    return pathways
