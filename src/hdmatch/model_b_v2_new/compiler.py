"""Deterministic prospective compiler and cryptographic model freeze."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.model import load_mapping_library
from hdmatch.questionnaire.bank import load_question_bank
from hdmatch.util import sha256_file

from .artifacts import (
    COMPILER_VERSION,
    COMPILER_VERSION_V2,
    ArtifactBinding,
    CompiledModelArtifact,
    CompiledModelArtifactV2,
    CompiledPathway,
    CompiledRule,
    FrozenObservation,
    ModelFreezeReceipt,
    ModelFreezeReceiptV2,
    ObservationStatus,
    PreregistrationArtifact,
    PreregistrationArtifactV2,
    SourceCatalogEntry,
    SourceKind,
    StructuralPathway,
    canonical_bytes,
    load_compiled_artifact,
    load_preregistration,
    reject_forbidden_provenance,
    selector_anchor_id,
    selector_dependency_keys,
)
from .provenance import (
    assert_preregistration_provenance_only_equivalent,
    assert_source_catalog_provenance_only_equivalent,
    load_retrieval_manifest,
    load_source_catalog_v2,
    validate_retrieval_manifest_against_source_catalog,
)
from .selectors import validate_selector_mechanics


def compile_model_b_v2_new(
    *,
    repository_root: str | Path,
    preregistration_path: str | Path,
    compiled_output_path: str | Path,
) -> CompiledModelArtifact:
    """Validate and compile one preregistration to byte-stable JSON.

    Every path is explicit.  The output has no compilation clock or environment
    metadata, so compiling identical bytes against identical local dependencies
    produces identical bytes.
    """

    root = _repository_root(repository_root)
    prereg_path = _explicit_file(preregistration_path, "preregistration")
    _ensure_within_repository(root, prereg_path)
    reject_forbidden_provenance(str(prereg_path))
    preregistration = load_preregistration(prereg_path)
    _validate_preregistration(root, preregistration)

    compiled = _build_compiled_artifact(preregistration, prereg_path)
    _validate_compiled_conflicts(compiled)
    output = Path(compiled_output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_bytes(compiled) + b"\n")
    # Parse the exact bytes that were written, guarding serialization drift.
    round_trip = load_compiled_artifact(output)
    if round_trip != compiled:
        raise AssertionError("compiled artifact changed during deterministic serialization")
    return compiled


def freeze_model_b_v2_new(
    *,
    repository_root: str | Path,
    preregistration_path: str | Path,
    compiled_artifact_path: str | Path,
    freeze_receipt_output_path: str | Path,
    source_software_commit: str,
    source_software_tree: str,
    frozen_at_utc: datetime | None = None,
) -> ModelFreezeReceipt:
    """Bind the complete prospective model dependency chain in one receipt."""

    root = _repository_root(repository_root)
    prereg_path = _explicit_file(preregistration_path, "preregistration")
    compiled_path = _explicit_file(compiled_artifact_path, "compiled artifact")
    _ensure_within_repository(root, prereg_path)
    _ensure_within_repository(root, compiled_path)
    preregistration = load_preregistration(prereg_path)
    _validate_preregistration(root, preregistration)
    compiled = load_compiled_artifact(compiled_path)
    _validate_compiled_binding(compiled, preregistration, prereg_path)
    _validate_compiled_conflicts(compiled)

    timestamp = frozen_at_utc or datetime.now(tz=UTC)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("freeze timestamp must be timezone-aware")
    timestamp = timestamp.astimezone(UTC)
    if timestamp < preregistration.preregistered_at_utc:
        raise ValueError("model freeze cannot precede preregistration")

    receipt = _build_freeze_receipt(
        root=root,
        preregistration=preregistration,
        preregistration_path=prereg_path,
        compiled=compiled,
        compiled_path=compiled_path,
        source_software_commit=source_software_commit,
        source_software_tree=source_software_tree,
        frozen_at_utc=timestamp,
    )
    output = Path(freeze_receipt_output_path).resolve()
    _ensure_within_repository(root, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_bytes(receipt) + b"\n")
    return receipt


def _validate_preregistration(root: Path, preregistration: PreregistrationArtifact) -> None:
    expected_compiler = (
        COMPILER_VERSION_V2
        if isinstance(preregistration, PreregistrationArtifactV2)
        else COMPILER_VERSION
    )
    if preregistration.compiler_version != expected_compiler:
        raise ValueError("unsupported prospective compiler version")
    bindings = (
        preregistration.behavioral_target,
        preregistration.question_bank,
        preregistration.model_a_base,
        *preregistration.local_methods,
    )
    for binding in bindings:
        _verify_local_binding(root, binding)
    for source in preregistration.source_catalog:
        _verify_source(root, source)
    if isinstance(preregistration, PreregistrationArtifactV2):
        _validate_v2_provenance(root, preregistration)

    bank_path = root / preregistration.question_bank.path
    question_bank = load_question_bank(bank_path)
    declared_question_ids = {item.question_id for item in preregistration.question_token_sets}
    referenced_question_ids = set(declared_question_ids)
    for observation in preregistration.observations:
        if isinstance(observation, FrozenObservation):
            referenced_question_ids.add(observation.prediction.question_id)
        else:
            referenced_question_ids.update(observation.question_ids)
    unknown_questions = referenced_question_ids - question_bank.question_ids
    if unknown_questions:
        raise ValueError(f"preregistration uses unknown questions: {sorted(unknown_questions)}")

    base_library = load_mapping_library(root / preregistration.model_a_base.path)
    if base_library.question_bank_sha256 != preregistration.question_bank.sha256:
        raise ValueError("Model A and V2 preregistration bind different question-bank bytes")

    source_by_id = {item.source_id: item for item in preregistration.source_catalog}
    for observation in preregistration.frozen_observations:
        _validate_observation_sources(observation, source_by_id)
        for pathway in _all_pathways(observation):
            validate_selector_mechanics(pathway.selector)


def _validate_observation_sources(
    observation: FrozenObservation,
    source_by_id: dict[str, SourceCatalogEntry],
) -> None:
    observation_kinds = {source_by_id[item].kind for item in observation.source_ids}
    if not observation_kinds & {SourceKind.BEHAVIORAL_TARGET, SourceKind.QUESTIONNAIRE}:
        raise ValueError(
            f"observation {observation.observation_id} lacks target/questionnaire provenance"
        )
    for pathway in _all_pathways(observation):
        pathway_kinds = {source_by_id[item].kind for item in pathway.source_ids}
        if not pathway_kinds & {SourceKind.PRIMARY_HD, SourceKind.ESTABLISHED_HD}:
            raise ValueError(
                f"pathway {pathway.pathway_id} lacks an independently sourced HD meaning"
            )


def _compile_observation(observation: FrozenObservation) -> CompiledRule:
    return CompiledRule(
        rule_id=observation.observation_id.replace("OBS-NEW-", "RULE-NEW-", 1),
        observation_id=observation.observation_id,
        behavioral_statement=observation.behavioral_statement,
        behavioral_confidence=observation.behavioral_confidence,
        dependency_cluster=observation.dependency_cluster,
        assignment=observation.assignment,
        prediction=observation.prediction,
        primary=_compile_pathway(observation.primary_pathway),
        alternatives=tuple(_compile_pathway(item) for item in observation.alternative_pathways),
        corroborator=(
            _compile_pathway(observation.corroborating_pathway)
            if observation.corroborating_pathway is not None
            else None
        ),
        source_ids=observation.source_ids,
        rationale=observation.rationale,
    )


def _compile_pathway(pathway: StructuralPathway) -> CompiledPathway:
    return CompiledPathway(
        pathway_id=pathway.pathway_id,
        selector=pathway.selector,
        anchor_id=selector_anchor_id(pathway.selector),
        dependency_keys=tuple(sorted(selector_dependency_keys(pathway.selector))),
        structural_class=pathway.structural_class,
        structural_salience=pathway.structural_salience,
        directness_class=pathway.directness_class,
        mapping_directness=pathway.mapping_directness,
        conditional_parent_levels=pathway.conditional_parent_levels,
        source_ids=pathway.source_ids,
        rationale=pathway.rationale,
    )


def _validate_compiled_binding(
    compiled: CompiledModelArtifact,
    preregistration: PreregistrationArtifact,
    preregistration_path: Path,
) -> None:
    if compiled.preregistration_file_sha256 != sha256_file(preregistration_path):
        raise ValueError("compiled artifact does not bind the current preregistration bytes")
    if compiled.preregistration_semantic_sha256 != preregistration.sha256():
        raise ValueError("compiled artifact does not bind preregistration semantics")
    expected = _build_compiled_artifact(preregistration, preregistration_path)
    if compiled != expected:
        raise ValueError(
            "compiled artifact is not the deterministic compilation of preregistration"
        )


def _build_compiled_artifact(
    preregistration: PreregistrationArtifact,
    preregistration_path: Path,
) -> CompiledModelArtifact:
    rules = tuple(_compile_observation(item) for item in preregistration.frozen_observations)
    unresolved = tuple(
        item for item in preregistration.observations if item.status is ObservationStatus.UNRESOLVED
    )
    if isinstance(preregistration, PreregistrationArtifactV2):
        return CompiledModelArtifactV2(
            preregistered_at_utc=preregistration.preregistered_at_utc,
            preregistration_semantic_sha256=preregistration.sha256(),
            preregistration_file_sha256=sha256_file(preregistration_path),
            behavioral_target=preregistration.behavioral_target,
            question_bank=preregistration.question_bank,
            model_a_base=preregistration.model_a_base,
            local_methods=preregistration.local_methods,
            source_catalog=preregistration.source_catalog,
            question_token_sets=preregistration.question_token_sets,
            constants=preregistration.constants,
            discovery_holdout_policy=preregistration.discovery_holdout_policy,
            rules=rules,
            unresolved_observations=unresolved,
            provenance_amended_at_utc=preregistration.provenance_amended_at_utc,
            previous_preregistration=preregistration.previous_preregistration,
            previous_source_catalog=preregistration.previous_source_catalog,
            source_catalog_artifact=preregistration.source_catalog_artifact,
            retrieval_manifest=preregistration.retrieval_manifest,
        )
    return CompiledModelArtifact(
        preregistered_at_utc=preregistration.preregistered_at_utc,
        preregistration_semantic_sha256=preregistration.sha256(),
        preregistration_file_sha256=sha256_file(preregistration_path),
        behavioral_target=preregistration.behavioral_target,
        question_bank=preregistration.question_bank,
        model_a_base=preregistration.model_a_base,
        local_methods=preregistration.local_methods,
        source_catalog=preregistration.source_catalog,
        question_token_sets=preregistration.question_token_sets,
        constants=preregistration.constants,
        discovery_holdout_policy=preregistration.discovery_holdout_policy,
        rules=rules,
        unresolved_observations=unresolved,
    )


def _build_freeze_receipt(
    *,
    root: Path,
    preregistration: PreregistrationArtifact,
    preregistration_path: Path,
    compiled: CompiledModelArtifact,
    compiled_path: Path,
    source_software_commit: str,
    source_software_tree: str,
    frozen_at_utc: datetime,
) -> ModelFreezeReceipt:
    preregistration_binding = _binding_for_path(root, preregistration_path, "preregistration")
    compiled_binding = _binding_for_path(root, compiled_path, "compiled_artifact")
    source_bindings = tuple(
        ArtifactBinding(
            role=f"source_{source.source_id.removeprefix('SRC-').lower().replace('-', '_')}",
            path=source.local_path,
            sha256=source.local_sha256,
        )
        for source in preregistration.source_catalog
    )
    if isinstance(preregistration, PreregistrationArtifactV2):
        return ModelFreezeReceiptV2(
            frozen_at_utc=frozen_at_utc,
            source_software_commit=source_software_commit,
            source_software_tree=source_software_tree,
            preregistration=preregistration_binding,
            compiled_artifact=compiled_binding,
            compiled_semantic_sha256=compiled.sha256(),
            behavioral_target=preregistration.behavioral_target,
            question_bank=preregistration.question_bank,
            model_a_base=preregistration.model_a_base,
            local_methods=preregistration.local_methods,
            source_catalog=source_bindings,
            previous_preregistration=preregistration.previous_preregistration,
            previous_source_catalog=preregistration.previous_source_catalog,
            source_catalog_artifact=preregistration.source_catalog_artifact,
            retrieval_manifest=preregistration.retrieval_manifest,
        )
    return ModelFreezeReceipt(
        frozen_at_utc=frozen_at_utc,
        source_software_commit=source_software_commit,
        source_software_tree=source_software_tree,
        preregistration=preregistration_binding,
        compiled_artifact=compiled_binding,
        compiled_semantic_sha256=compiled.sha256(),
        behavioral_target=preregistration.behavioral_target,
        question_bank=preregistration.question_bank,
        model_a_base=preregistration.model_a_base,
        local_methods=preregistration.local_methods,
        source_catalog=source_bindings,
    )


def _validate_v2_provenance(
    root: Path,
    preregistration: PreregistrationArtifactV2,
) -> None:
    bindings = (
        preregistration.previous_preregistration,
        preregistration.previous_source_catalog,
        preregistration.source_catalog_artifact,
        preregistration.retrieval_manifest,
    )
    for binding in bindings:
        _verify_local_binding(root, binding)

    previous_path = root / preregistration.previous_preregistration.path
    previous = load_preregistration(previous_path)
    if type(previous) is not PreregistrationArtifact:
        raise ValueError("V2 provenance amendment must bind the original V1 preregistration")
    _validate_preregistration(root, previous)
    assert_preregistration_provenance_only_equivalent(previous, preregistration)

    previous_source_path = root / preregistration.previous_source_catalog.path
    manifest = load_retrieval_manifest(root / preregistration.retrieval_manifest.path)
    if manifest.source_catalog_v1 != preregistration.previous_source_catalog:
        raise ValueError("retrieval manifest binds a different V1 source catalog")
    validate_retrieval_manifest_against_source_catalog(manifest, previous_source_path)

    amended_source = load_source_catalog_v2(root / preregistration.source_catalog_artifact.path)
    amendment = amended_source.provenance_amendment
    if amendment.previous_source_catalog != preregistration.previous_source_catalog:
        raise ValueError("V2 source catalog binds a different prior source catalog")
    if amendment.retrieval_manifest != preregistration.retrieval_manifest:
        raise ValueError("V2 source catalog binds a different retrieval manifest")
    assert_source_catalog_provenance_only_equivalent(previous_source_path, amended_source)

    external_sources = tuple(
        source for source in preregistration.source_catalog if source.public_url is not None
    )
    for source in external_sources:
        if (
            source.local_path != preregistration.source_catalog_artifact.path
            or source.local_sha256 != preregistration.source_catalog_artifact.sha256
        ):
            raise ValueError(
                f"external source {source.source_id} does not bind the V2 source catalog"
            )


def _validate_compiled_conflicts(compiled: CompiledModelArtifact) -> None:
    """Reject known conflicts and leave runtime to fail on conditional overlaps."""

    answers_by_exact_anchor: dict[tuple[str, str], str] = {}
    for rule in compiled.rules:
        for pathway in (rule.primary, *rule.alternatives):
            key = (rule.prediction.question_id, pathway.anchor_id)
            previous = answers_by_exact_anchor.setdefault(
                key, rule.prediction.canonical_answer_token
            )
            if previous != rule.prediction.canonical_answer_token:
                raise ValueError(
                    "the same question/selector has conflicting canonical answers; "
                    "no silent winner is permitted"
                )


def _all_pathways(observation: FrozenObservation) -> tuple[StructuralPathway, ...]:
    corroborator = (
        (observation.corroborating_pathway,)
        if observation.corroborating_pathway is not None
        else ()
    )
    return (observation.primary_pathway, *observation.alternative_pathways, *corroborator)


def _verify_source(root: Path, source: SourceCatalogEntry) -> None:
    reject_forbidden_provenance(source.local_path)
    if source.public_url is not None:
        reject_forbidden_provenance(source.public_url)
    path = root / source.local_path
    if not path.is_file():
        raise ValueError(f"source artifact is missing: {source.local_path}")
    if sha256_file(path) != source.local_sha256:
        raise ValueError(f"source artifact hash mismatch: {source.local_path}")


def _verify_local_binding(root: Path, binding: ArtifactBinding) -> None:
    path = root / binding.path
    if not path.is_file():
        raise ValueError(f"bound artifact is missing: {binding.path}")
    if sha256_file(path) != binding.sha256:
        raise ValueError(f"bound artifact hash mismatch: {binding.path}")


def _binding_for_path(root: Path, path: Path, role: str) -> ArtifactBinding:
    return ArtifactBinding(
        role=role,
        path=path.relative_to(root).as_posix(),
        sha256=sha256_file(path),
    )


def _repository_root(value: str | Path) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise ValueError(f"repository root is not a directory: {root}")
    return root


def _explicit_file(value: str | Path, label: str) -> Path:
    path = Path(value).resolve()
    if not path.is_file():
        raise ValueError(f"{label} is not a file: {path}")
    return path


def _ensure_within_repository(root: Path, path: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ValueError(f"path must be inside the explicit repository root: {path}") from error


def artifact_pretty_json(value: CompiledModelArtifact | ModelFreezeReceipt) -> str:
    """Human-readable view; not used for the byte commitment."""

    return json.dumps(
        value.model_dump(mode="json", exclude_none=False),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
