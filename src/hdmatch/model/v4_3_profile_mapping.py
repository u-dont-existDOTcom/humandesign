"""Mechanical migration of the frozen V3.6 profile audit into mapping-library-v2.

Only the two provenance-bearing, pre-ranking mapping JSON files and their declared
method/target documents are inputs.  This module never imports ranking results,
candidate scores, or winner artifacts.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from collections.abc import Set as AbstractSet
from pathlib import Path
from typing import Any, Final, Literal, cast

from hdmatch.chart.bodygraph import Center
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.chart.feature_registry import FeatureId
from hdmatch.experiments.canonical import sha256_bytes, write_new_bytes
from hdmatch.model.mapping_library import (
    MAPPING_DIRECTNESS,
    STRUCTURAL_SALIENCE,
    ContradictionSeverity,
    DirectnessClass,
    StructuralClass,
)
from hdmatch.model.v4_3_compiler import compile_verified_mapping_library_v2
from hdmatch.model.v4_3_mapping import (
    FLEXIBILITY_FACTOR,
    ContradictionModeV2,
    FlexibilityClass,
    FrozenMappingRuleSourceV2,
    MappingConstantsV2,
    MappingLibrarySourceV2,
    MappingLibraryV2,
    MappingStatusV2,
    PathwayRoleV2,
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
)
from hdmatch.util import canonical_json_bytes, sha256_file

FROZEN_MAPPING_PATH: Final[str] = (
    "reference/core/profile_v3_6_v43_mapping_frozen_2026_08_22.json"
)
OVERLAY_MAPPING_PATH: Final[str] = (
    "reference/core/profile_v3_6_v43_mapping_overlay_v2_2026_08_22.json"
)
V43_SCORING_PATH: Final[str] = "reference/core/v4_3_scoring_algorithm.md"
BEHAVIORAL_TARGET_PATH: Final[str] = (
    "reference/core/behavioral_target_combined_v3_6.md"
)
SCORING_POLICY_PATH: Final[str] = "docs/02_scoring_and_model_policy.md"
COVERAGE_AUDIT_PATH: Final[str] = "docs/17_v3_6_profile_mapping_coverage_audit.md"

LESS_CONTAMINATED_SOURCE_PATH: Final[str] = (
    "mappings/v4_3_v3_6_less_contaminated_mapping_library_v2_source.json"
)
LESS_CONTAMINATED_COMPILED_PATH: Final[str] = (
    "mappings/v4_3_v3_6_less_contaminated_mapping_library_v2.json"
)
BEST_CURRENT_SOURCE_PATH: Final[str] = (
    "mappings/v4_3_v3_6_best_current_mapping_library_v2_source.json"
)
BEST_CURRENT_COMPILED_PATH: Final[str] = (
    "mappings/v4_3_v3_6_best_current_mapping_library_v2.json"
)
MIGRATION_RECEIPT_PATH: Final[str] = (
    "mappings/v4_3_v3_6_mapping_library_v2_migration_receipt.json"
)

MappingVariant = Literal["less_contaminated", "best_current_descriptive"]
_EXPECTED_FROZEN_MAPPING_SHA256: Final[str] = (
    "f16565094a1a8eede720dd369dfdd4c0d4700a213520b535de28f8f88dd40afd"
)
_EXPECTED_OVERLAY_MAPPING_SHA256: Final[str] = (
    "03d25392f9639fb985f806d4814743bbb1cf466bc803c42b6bf6ca8588337735"
)
_POST_SELECTION_IDS: Final[frozenset[str]] = frozenset(
    {"PMOON_24_DRIVE", "DMARS_61_DEVELOPMENT"}
)
_TARGET_CONFIDENCE_OVERRIDES: Final[dict[str, float]] = {
    "TYPE_PROJECTOR_ENTRY": 0.85,
}
_SOURCE_ARTIFACTS: Final[tuple[tuple[str, SourceRoleV2, str, str], ...]] = (
    (
        "SRC-COVERAGE-AUDIT",
        SourceRoleV2.PROVENANCE,
        COVERAGE_AUDIT_PATH,
        "V3.6 Profile Mapping Coverage Audit",
    ),
    (
        "SRC-MAPPING-FROZEN",
        SourceRoleV2.PROVENANCE,
        FROZEN_MAPPING_PATH,
        "Frozen V3.6 V4.3 profile-audit mapping",
    ),
    (
        "SRC-MAPPING-OVERLAY",
        SourceRoleV2.PROVENANCE,
        OVERLAY_MAPPING_PATH,
        "Frozen V3.6 V4.3 profile-audit mapping overlay V2",
    ),
    (
        "SRC-SCORING-POLICY",
        SourceRoleV2.METHOD,
        SCORING_POLICY_PATH,
        "Scoring and Model Policy",
    ),
    (
        "SRC-TARGET-V36",
        SourceRoleV2.BEHAVIORAL_TARGET,
        BEHAVIORAL_TARGET_PATH,
        "Behavioral Target Combined V3.6",
    ),
    (
        "SRC-V43-SCORING",
        SourceRoleV2.METHOD,
        V43_SCORING_PATH,
        "V4.3 Canonical Scoring Algorithm",
    ),
)

_PRIMARY_BY_CLUSTER: Final[dict[str, str]] = {
    "AUTHORITY_SOMATIC": "AUTH_SPLENIC_SIGNAL",
    "CENTER_G": "CENTER_G_DEFINED",
    "CENTER_HEART": "CENTER_HEART_DEFINED",
    "CENTER_ROOT": "CENTER_ROOT_OPEN",
    "CENTER_SACRAL": "CENTER_SACRAL_OPEN",
    "CENTER_SOLAR_PLEXUS": "CENTER_SP_OPEN",
    "CENTER_SPLEEN": "CENTER_SPLEEN_DEFINED",
    "CONCENTRATED_FOCUS": "GATE_52_FOCUS",
    "CONSEQUENTIAL_CORRECTION": "CH_18_58_CORRECTION",
    "CONTINUITY_PRESERVATION": "GATE_32_CONTINUITY",
    "ENTERPRISE_PERSUASION_PATTERN": "CH_26_44_ENTERPRISE",
    "EXISTENTIAL_MYSTERY": "CH_24_61_MYSTERY",
    "INSIGHT_TO_STRUCTURE": "CH_23_43_STRUCTURING",
    "MYSTERY_DEVELOPMENT_CARRIER": "DMARS_61_DEVELOPMENT",
    "MYSTERY_DRIVE_CARRIER": "PMOON_24_DRIVE",
    "NEEDS_SENSITIVITY": "GATE_19_NEEDS",
    "ORGANIZED_DETAIL": "CH_17_62_ORGANIZE",
    "ORIGINAL_CONTRIBUTION": "CH_1_8_ORIGINAL",
    "PROFILE_STRUCTURE": "PROFILE_24",
    "PURPOSE_STRUGGLE": "CH_28_38_PURPOSE",
    "RESOURCE_SOVEREIGNTY": "GATE_21_RESOURCES",
    "RETREAT_PRIVACY": "CH_13_33_RETREAT",
    "RHYTHM_ROUTINE": "GATE_5_ROUTINE",
    "TYPE_ENTRY": "TYPE_PROJECTOR_ENTRY",
    "VALUES_RESPONSIBILITY": "GATE_50_VALUES",
}

_UNRESOLVED_CONSTRUCTS: Final[tuple[str, ...]] = (
    "autobiographical calendar/age windows",
    "calculated versus pure gambling risk",
    "confidentiality style",
    "dynamic/relationship/advanced-variable interpretations without a frozen mapping",
    "fine-grained tactile, aroma, music, aesthetic, and environmental preferences",
    "generic caregiving capacity",
    "generic romance, sensuality, attachment, and intimacy",
    "home-sanctuary aesthetics beyond scored retreat/routine/resource constructs",
    "humor style",
    "institutional dissent without a narrow established mapping",
    "nonviolence/de-escalation as a generic trait",
    "sleep-boundary and dream phenomena",
    "sweet-versus-savory and other PHS-style dietary details",
    "travel motives",
)


class ProfileMappingMigrationError(ValueError):
    """The frozen inputs cannot be migrated without changing their meaning."""


def build_profile_mapping_library_source_v2(
    repository_root: str | Path,
    *,
    variant: MappingVariant,
) -> MappingLibrarySourceV2:
    """Build one deterministic source library without inspecting any results."""

    root = Path(repository_root).resolve()
    base, overlay = _load_and_validate_inputs(root)
    records = _merged_mapping_records(base, overlay)
    if variant == "less_contaminated":
        records = tuple(item for item in records if str(item["id"]) not in _POST_SELECTION_IDS)
    elif variant != "best_current_descriptive":
        raise ProfileMappingMigrationError(f"unsupported mapping variant: {variant}")
    rules = tuple(sorted((_mapping_rule(item) for item in records), key=lambda item: item.rule_id))
    contradiction = _contradiction_rule(_only_mapping(base, "contradictions"))
    rules = tuple(sorted((*rules, contradiction), key=lambda item: item.rule_id))
    required = tuple(
        sorted(
            {
                feature_id
                for rule in rules
                for pathway in (rule.primary_pathway, *rule.alternative_pathways)
                for feature_id in pathway.required_feature_ids
            },
            key=lambda item: item.value,
        )
    )
    return MappingLibrarySourceV2(
        behavioral_target_source_id="SRC-TARGET-V36",
        method_source_ids=("SRC-SCORING-POLICY", "SRC-V43-SCORING"),
        question_bank_source_id=None,
        source_artifacts=_source_artifacts(root),
        constants=MappingConstantsV2(),
        declared_frozen_rule_ids=tuple(rule.rule_id for rule in rules),
        declared_observation_ids=tuple(sorted(rule.observation_id for rule in rules)),
        declared_required_feature_ids=required,
        mappings=rules,
    )


def compile_profile_mapping_library_v2(
    repository_root: str | Path,
    *,
    variant: MappingVariant,
) -> MappingLibraryV2:
    source = build_profile_mapping_library_source_v2(
        repository_root,
        variant=variant,
    )
    return compile_verified_mapping_library_v2(
        source,
        repository_root=repository_root,
    )


def generated_profile_mapping_artifacts(
    repository_root: str | Path,
) -> dict[str, bytes]:
    """Return every tracked artifact as deterministic canonical bytes."""

    root = Path(repository_root).resolve()
    less_source = build_profile_mapping_library_source_v2(
        root,
        variant="less_contaminated",
    )
    best_source = build_profile_mapping_library_source_v2(
        root,
        variant="best_current_descriptive",
    )
    less_compiled = compile_verified_mapping_library_v2(less_source, repository_root=root)
    best_compiled = compile_verified_mapping_library_v2(best_source, repository_root=root)
    artifacts = {
        LESS_CONTAMINATED_SOURCE_PATH: less_source.canonical_bytes(),
        LESS_CONTAMINATED_COMPILED_PATH: less_compiled.canonical_bytes(),
        BEST_CURRENT_SOURCE_PATH: best_source.canonical_bytes(),
        BEST_CURRENT_COMPILED_PATH: best_compiled.canonical_bytes(),
    }
    receipt = _migration_receipt(root, artifacts, less_source, best_source)
    artifacts[MIGRATION_RECEIPT_PATH] = canonical_json_bytes(receipt)
    return dict(sorted(artifacts.items()))


def write_profile_mapping_artifacts_new(repository_root: str | Path) -> tuple[Path, ...]:
    """Create the deterministic artifacts and refuse to replace tracked bytes."""

    root = Path(repository_root).resolve()
    artifacts = generated_profile_mapping_artifacts(root)
    existing = sorted(relative for relative in artifacts if (root / relative).exists())
    if existing:
        raise ProfileMappingMigrationError(
            f"refusing to replace mapping artifacts: {existing}"
        )
    destinations: list[Path] = []
    for relative, content in artifacts.items():
        destination = root / relative
        write_new_bytes(destination, content)
        destinations.append(destination)
    return tuple(destinations)


def verify_tracked_profile_mapping_artifacts(repository_root: str | Path) -> None:
    """Fail if any tracked source, compiled library, or receipt byte changes."""

    root = Path(repository_root).resolve()
    expected = generated_profile_mapping_artifacts(root)
    for relative, content in expected.items():
        path = root / relative
        if not path.is_file():
            raise ProfileMappingMigrationError(f"tracked mapping artifact is missing: {relative}")
        if path.read_bytes() != content:
            raise ProfileMappingMigrationError(f"tracked mapping artifact differs: {relative}")


def _load_and_validate_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    actual_frozen_sha256 = sha256_file(root / FROZEN_MAPPING_PATH)
    actual_overlay_sha256 = sha256_file(root / OVERLAY_MAPPING_PATH)
    if actual_frozen_sha256 != _EXPECTED_FROZEN_MAPPING_SHA256:
        raise ProfileMappingMigrationError(
            "frozen mapping source hash changed; "
            f"expected={_EXPECTED_FROZEN_MAPPING_SHA256}, actual={actual_frozen_sha256}"
        )
    if actual_overlay_sha256 != _EXPECTED_OVERLAY_MAPPING_SHA256:
        raise ProfileMappingMigrationError(
            "mapping overlay source hash changed; "
            f"expected={_EXPECTED_OVERLAY_MAPPING_SHA256}, actual={actual_overlay_sha256}"
        )
    base = _load_json_object(root / FROZEN_MAPPING_PATH)
    overlay = _load_json_object(root / OVERLAY_MAPPING_PATH)
    _require_keys(
        base,
        {
            "schema",
            "target_version",
            "created_utc",
            "status",
            "ranking_rule",
            "constants",
            "core",
            "notes",
            "mappings",
            "contradictions",
        },
        "frozen mapping",
    )
    _require_keys(
        overlay,
        {
            "schema",
            "created_utc",
            "status",
            "base_mapping",
            "rationale",
            "overrides",
            "add_mappings",
        },
        "mapping overlay",
    )
    expected = {
        "base schema": (base["schema"], "v4.3-profile-audit-mapping-v1"),
        "target version": (base["target_version"], "V3.6"),
        "base status": (
            base["status"],
            "frozen-before-ranking-best-current-descriptive",
        ),
        "overlay schema": (
            overlay["schema"],
            "v4.3-profile-audit-mapping-overlay-v2",
        ),
        "overlay status": (
            overlay["status"],
            "frozen-before-opening-any-v4.3-profile-ranking",
        ),
        "overlay base": (overlay["base_mapping"], FROZEN_MAPPING_PATH),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise ProfileMappingMigrationError(f"{label} changed: {actual!r}")
    if base["created_utc"] != "2026-08-22T08:55:00Z" or (
        overlay["created_utc"] != "2026-08-22T09:02:00Z"
    ):
        raise ProfileMappingMigrationError("frozen source timestamp changed")
    _validate_frozen_constants(cast(Mapping[str, Any], base["constants"]))
    return base, overlay


def _merged_mapping_records(
    base: Mapping[str, Any],
    overlay: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    base_records = tuple(
        _validated_mapping_record(cast(dict[str, Any], item), origin="base")
        for item in _sequence(base["mappings"], "base mappings")
    )
    additions = tuple(
        _validated_mapping_record(cast(dict[str, Any], item), origin="overlay")
        for item in _sequence(overlay["add_mappings"], "overlay mappings")
    )
    records = {str(item["id"]): dict(item) for item in base_records}
    if len(records) != len(base_records):
        raise ProfileMappingMigrationError("base mapping IDs are not unique")
    overrides_value = overlay["overrides"]
    if not isinstance(overrides_value, Mapping):
        raise ProfileMappingMigrationError("overlay overrides must be an object")
    overrides = cast(Mapping[str, Any], overrides_value)
    if set(overrides) != {"CENTER_ROOT_OPEN", "CENTER_HEART_DEFINED"}:
        raise ProfileMappingMigrationError("overlay override inventory changed")
    for mapping_id, changes_value in overrides.items():
        if mapping_id not in records:
            raise ProfileMappingMigrationError(f"overlay target is missing: {mapping_id}")
        if not isinstance(changes_value, Mapping):
            raise ProfileMappingMigrationError(
                f"overlay override must be an object: {mapping_id}"
            )
        changes = cast(Mapping[str, Any], changes_value)
        _require_keys(
            changes,
            {"confidence", "directness", "flexibility", "behavior"},
            f"override {mapping_id}",
        )
        records[mapping_id].update(changes)
        records[mapping_id]["origin"] = "base+overlay"
    for addition in additions:
        mapping_id = str(addition["id"])
        if mapping_id in records:
            raise ProfileMappingMigrationError(f"overlay duplicates mapping ID: {mapping_id}")
        records[mapping_id] = addition
    return tuple(records[item] for item in sorted(records))


def _validated_mapping_record(
    value: dict[str, Any],
    *,
    origin: Literal["base", "overlay"],
) -> dict[str, Any]:
    allowed = {
        "id",
        "cluster",
        "behavior",
        "confidence",
        "salience",
        "directness",
        "flexibility",
        "predicate",
        "parents",
        "source",
    }
    if origin == "base":
        allowed.add("post_selection")
    _require_keys(value, allowed, f"{origin} mapping", allow_optional={"post_selection"})
    if not isinstance(value["id"], str) or not isinstance(value["cluster"], str):
        raise ProfileMappingMigrationError("mapping ID/cluster must be strings")
    result = dict(value)
    result["origin"] = origin
    return result


def _mapping_rule(record: Mapping[str, Any]) -> FrozenMappingRuleSourceV2:
    mapping_id = str(record["id"])
    normalized = _normalized_id(mapping_id)
    post_selection = bool(record.get("post_selection", False))
    origin = str(record["origin"])
    source_cluster = str(record["cluster"])
    pathway_group_id, pathway_role, primary_mapping_id = _pathway_relationship(
        mapping_id,
        source_cluster,
    )
    source_confidence = _number(record["confidence"], "confidence")
    if mapping_id == "TYPE_PROJECTOR_ENTRY" and source_confidence != 0.9:
        raise ProfileMappingMigrationError(
            "older TYPE_PROJECTOR_ENTRY confidence changed; controlling override "
            "provenance requires source value 0.90"
        )
    behavioral_confidence = _TARGET_CONFIDENCE_OVERRIDES.get(
        mapping_id,
        source_confidence,
    )
    pathway = _pathway(record)
    target_locator = "V3.6 retained target and scoring constraints"
    target_rationale = (
        "The migrated observation is development-profile evidence, not validation."
    )
    if mapping_id == "TYPE_PROJECTOR_ENTRY":
        target_locator = (
            "Invitation/recognition is domain-sensitive; Behavioral confidence: 0.85"
        )
        target_rationale = (
            "The higher-priority V3.6 behavioral target explicitly controls confidence "
            "at 0.85, superseding the older source JSON value 0.90 without using outcomes."
        )
    return FrozenMappingRuleSourceV2(
        rule_id=f"RULE-{normalized}",
        observation_id=f"OBS-{normalized}",
        status=MappingStatusV2.FROZEN,
        behavioral_statement=str(record["behavior"]),
        behavioral_confidence=behavioral_confidence,
        measurement_reliability=1.0,
        source_dependency_cluster=source_cluster,
        dependency_cluster=pathway_group_id,
        pathway_group_id=pathway_group_id,
        pathway_role=pathway_role,
        primary_rule_id=f"RULE-{_normalized_id(primary_mapping_id)}",
        elicitation_stage="development_profile_v3_6",
        revision_class=_revision_class(mapping_id),
        selection_risk=(
            SelectionRiskV2.HIGH if post_selection else SelectionRiskV2.MODERATE
        ),
        candidate_direction_visible=True,
        question_ids=(),
        response_rule=_positive_response_rule(normalized),
        primary_pathway=pathway,
        alternative_pathways=(),
        corroborating_pathway=None,
        sources=(
            _citation(
                "SRC-COVERAGE-AUDIT",
                f"Scored constructs table; cluster {record['cluster']}",
                "Declares the scored construct and its primary/alternative pathway role.",
            ),
            _citation(
                "SRC-TARGET-V36",
                target_locator,
                target_rationale,
            ),
        ),
        rationale=(
            f"Mechanical migration of {mapping_id}; source factors are preserved. "
            + (
                "The controlling V3.6 target confidence 0.85 explicitly overrides the "
                "older frozen mapping value 0.90. "
                if mapping_id == "TYPE_PROJECTOR_ENTRY"
                else "The source behavioral confidence is preserved. "
            )
            + "Measurement reliability is the identity factor 1.0 because the source "
            "exposes no separate reliability estimate. "
            f"Typed pathway role={pathway_role.value}; source dependency cluster="
            f"{source_cluster}; scoring pathway group={pathway_group_id}; "
            f"origin={origin}."
        ),
    )


def _pathway(record: Mapping[str, Any]) -> StructuralPathwayV2:
    mapping_id = str(record["id"])
    predicate = _predicate(cast(Mapping[str, Any], record["predicate"]))
    structural_class = _structural_class(predicate.feature_id)
    salience = _number(record["salience"], "salience")
    if salience != STRUCTURAL_SALIENCE[structural_class]:
        raise ProfileMappingMigrationError(
            f"{mapping_id} salience {salience} does not match {structural_class.value}"
        )
    directness = _directness_class(_number(record["directness"], "directness"))
    flexibility = _flexibility_class(_number(record["flexibility"], "flexibility"))
    source_id = (
        "SRC-MAPPING-OVERLAY"
        if str(record["origin"]) == "overlay"
        else "SRC-MAPPING-FROZEN"
    )
    citations = [
        _citation(
            source_id,
            f"mapping id {mapping_id}",
            str(record["source"]),
        ),
        _citation(
            "SRC-V43-SCORING",
            "sections 2, 3, 7-10",
            "Requires frozen salience, directness, flexibility, parents, and dependencies.",
        ),
    ]
    if str(record["origin"]) == "base+overlay":
        citations.append(
            _citation(
                "SRC-MAPPING-OVERLAY",
                f"overrides.{mapping_id}",
                "The overlay explicitly corrects the frozen behavior/confidence/factors.",
            )
        )
    return StructuralPathwayV2(
        pathway_id=f"PATH-{_normalized_id(mapping_id)}",
        predicate=predicate,
        structural_class=structural_class,
        structural_salience=salience,
        directness_class=directness,
        mapping_directness=MAPPING_DIRECTNESS[directness],
        flexibility_class=flexibility,
        flexibility_factor=FLEXIBILITY_FACTOR[flexibility],
        prevalence_parent_hierarchy=_parent_hierarchy(
            cast(Sequence[object], record["parents"])
        ),
        sources=tuple(citations),
        rationale=(
            f"Verbatim source rationale: {record['source']} External citation provenance "
            "is incomplete in the original frozen mapping: it provides no exact URL, "
            "retrieval timestamp, or retrieved-content hash. No replacement was invented."
        ),
    )


def _contradiction_rule(value: Mapping[str, Any]) -> FrozenMappingRuleSourceV2:
    _require_keys(
        value,
        {"id", "cluster", "behavior", "confidence", "severity", "predicate", "source"},
        "contradiction mapping",
    )
    mapping_id = str(value["id"])
    normalized = _normalized_id(mapping_id)
    severity = _number(value["severity"], "contradiction severity")
    if severity != 0.5:
        raise ProfileMappingMigrationError("frozen contradiction severity changed")
    record = {
        "id": mapping_id,
        "origin": "base",
        "salience": 0.8,
        "directness": 1.0,
        "flexibility": 1.0,
        "predicate": value["predicate"],
        "parents": [],
        "source": value["source"],
    }
    return FrozenMappingRuleSourceV2(
        rule_id=f"RULE-{normalized}",
        observation_id=f"OBS-{normalized}",
        status=MappingStatusV2.FROZEN,
        behavioral_statement=(
            "Complete Channel 16-48 predicts a generalized independent drive to develop "
            "skill through practice; the frozen target explicitly denies that behavior."
        ),
        behavioral_confidence=_number(value["confidence"], "confidence"),
        measurement_reliability=1.0,
        source_dependency_cluster=str(value["cluster"]),
        dependency_cluster=str(value["cluster"]),
        pathway_group_id=str(value["cluster"]),
        pathway_role=PathwayRoleV2.PRIMARY,
        primary_rule_id=f"RULE-{normalized}",
        elicitation_stage="development_profile_v3_6",
        revision_class=RevisionClassV2.R0,
        selection_risk=SelectionRiskV2.MODERATE,
        candidate_direction_visible=True,
        question_ids=(),
        response_rule=ResponseRuleV2(
            response_dimension_id=f"RESPONSE-{normalized}",
            canonical_response_token="generalized_mastery_drive_present",
            support_response_tokens=("generalized_mastery_drive_present",),
            unknown_response_tokens=("context_dependent", "unknown"),
            contradiction=ResponseContradictionV2(
                mode=ContradictionModeV2.DIRECT_OPPOSITION,
                opposing_response_tokens=("denies_generalized_mastery_drive",),
                severity=ContradictionSeverity.MEANINGFUL,
                rationale=str(value["behavior"]),
            ),
        ),
        primary_pathway=_pathway(record),
        alternative_pathways=(),
        corroborating_pathway=None,
        sources=(
            _citation(
                "SRC-MAPPING-FROZEN",
                f"contradiction id {mapping_id}",
                "The source predeclares the only mechanically penalized contradiction.",
            ),
            _citation(
                "SRC-COVERAGE-AUDIT",
                "Explicit contradiction section",
                "Confirms Channel 16-48 and severity 0.50 as the sole contradiction.",
            ),
        ),
        rationale=(
            "The response rule preserves the source polarity: the channel predicts the "
            "positive mastery drive, while the frozen target token is its direct opposition."
        ),
    )


def _predicate(value: Mapping[str, Any]) -> StructuralPredicateV2:
    feature = value.get("feature")
    if feature == "type":
        _require_keys(value, {"feature", "equals"}, "Type predicate")
        return StructuralPredicateV2(
            feature_id=FeatureId.TYPE,
            operator=PredicateOperatorV2.EQUALS_ANY,
            values=(_architecture_value(str(value["equals"])),),
        )
    if feature == "authority":
        _require_keys(value, {"feature", "equals"}, "Authority predicate")
        return StructuralPredicateV2(
            feature_id=FeatureId.AUTHORITY,
            operator=PredicateOperatorV2.EQUALS_ANY,
            values=(_architecture_value(str(value["equals"])),),
        )
    if feature == "center":
        _require_keys(value, {"feature", "name", "defined"}, "Center predicate")
        center = _center_value(str(value["name"]))
        defined = value["defined"]
        if not isinstance(defined, bool):
            raise ProfileMappingMigrationError("Center defined flag must be Boolean")
        return StructuralPredicateV2(
            feature_id=FeatureId.CENTERS,
            operator=(
                PredicateOperatorV2.CONTAINS_ANY
                if defined
                else PredicateOperatorV2.NOT_CONTAINS_ANY
            ),
            values=(center,),
        )
    if feature == "profile":
        _require_keys(value, {"feature", "equals"}, "Profile predicate")
        return StructuralPredicateV2(
            feature_id=FeatureId.PROFILE,
            operator=PredicateOperatorV2.EQUALS_ANY,
            values=(str(value["equals"]),),
        )
    if feature == "profile_has_line":
        _require_keys(value, {"feature", "line"}, "Profile-line predicate")
        return StructuralPredicateV2(
            feature_id=FeatureId.PROFILE,
            operator=PredicateOperatorV2.PROFILE_HAS_LINE,
            values=(str(value["line"]),),
        )
    if feature == "channel":
        _require_keys(value, {"feature", "equals"}, "Channel predicate")
        return StructuralPredicateV2(
            feature_id=FeatureId.COMPLETE_CHANNELS,
            operator=PredicateOperatorV2.CONTAINS_ANY,
            values=(str(value["equals"]),),
        )
    if feature == "gate":
        _require_keys(value, {"feature", "equals"}, "Gate predicate")
        return StructuralPredicateV2(
            feature_id=FeatureId.HANGING_GATES,
            operator=PredicateOperatorV2.HAS_GATE,
            gate=_integer(value["equals"], "Gate"),
        )
    if feature == "activation":
        _require_keys(
            value,
            {"feature", "side", "body", "gate"},
            "Activation predicate",
        )
        side_value = value["side"]
        if side_value not in {"personality", "design"}:
            raise ProfileMappingMigrationError(
                f"Activation side is not canonical: {side_value!r}"
            )
        try:
            carrier = CelestialBody(str(value["body"]))
        except ValueError as exc:
            raise ProfileMappingMigrationError(
                f"Activation carrier is not canonical: {value['body']!r}"
            ) from exc
        return StructuralPredicateV2(
            feature_id=FeatureId.PLANETARY_ACTIVATIONS,
            operator=PredicateOperatorV2.MATCHES_ACTIVATION,
            side=cast(Literal["personality", "design"], side_value),
            carrier=carrier,
            gate=_integer(value["gate"], "Gate"),
        )
    raise ProfileMappingMigrationError(f"unsupported frozen predicate feature: {feature!r}")


def _parent_hierarchy(
    values: Sequence[object],
) -> tuple[PrevalenceParentLevelV2, ...]:
    feature_ids: set[FeatureId] = set()
    for raw in values:
        if not isinstance(raw, Mapping):
            raise ProfileMappingMigrationError("prevalence parent must be an object")
        feature_value = raw.get("feature")
        if not isinstance(feature_value, str):
            raise ProfileMappingMigrationError("prevalence parent feature must be a string")
        mapped = {
            "type": FeatureId.TYPE,
            "authority": FeatureId.AUTHORITY,
            "center": FeatureId.CENTERS,
            "channel": FeatureId.COMPLETE_CHANNELS,
        }.get(feature_value)
        if mapped is None:
            raise ProfileMappingMigrationError(
                f"unsupported prevalence parent: {feature_value!r}"
            )
        feature_ids.add(mapped)
    levels: list[PrevalenceParentLevelV2] = []
    current = set(feature_ids)
    removal_order = (
        FeatureId.COMPLETE_CHANNELS,
        FeatureId.CENTERS,
        FeatureId.AUTHORITY,
        FeatureId.TYPE,
    )
    while current:
        ordered = tuple(sorted(current, key=lambda item: item.value))
        levels.append(
            PrevalenceParentLevelV2(
                level_id="_".join(_feature_label(item) for item in ordered),
                parent_feature_ids=ordered,
            )
        )
        removed = next((item for item in removal_order if item in current), None)
        if removed is None:
            raise ProfileMappingMigrationError("no frozen backoff rule for parent set")
        current.remove(removed)
    levels.append(PrevalenceParentLevelV2(level_id="root", parent_feature_ids=()))
    return tuple(levels)


def _positive_response_rule(normalized_mapping_id: str) -> ResponseRuleV2:
    token = normalized_mapping_id.casefold().replace("-", "_") + "_present"
    return ResponseRuleV2(
        response_dimension_id=f"RESPONSE-{normalized_mapping_id}",
        canonical_response_token=token,
        support_response_tokens=(token,),
        unknown_response_tokens=("context_dependent", "unknown"),
        contradiction=ResponseContradictionV2(
            mode=ContradictionModeV2.NONE,
            opposing_response_tokens=(),
            severity=ContradictionSeverity.NONE,
            rationale="No direct opposing response is declared for this positive mapping.",
        ),
    )


def _migration_receipt(
    root: Path,
    artifacts: Mapping[str, bytes],
    less_source: MappingLibrarySourceV2,
    best_source: MappingLibrarySourceV2,
) -> dict[str, Any]:
    base = _load_json_object(root / FROZEN_MAPPING_PATH)
    overlay = _load_json_object(root / OVERLAY_MAPPING_PATH)
    records = _merged_mapping_records(base, overlay)
    groups = []
    scoring_groups: dict[str, list[tuple[dict[str, Any], PathwayRoleV2, str]]] = {}
    for item in records:
        mapping_id = str(item["id"])
        group_id, role, primary = _pathway_relationship(
            mapping_id,
            str(item["cluster"]),
        )
        scoring_groups.setdefault(group_id, []).append((item, role, primary))
    for cluster in sorted(scoring_groups):
        members = scoring_groups[cluster]
        primary_ids = {primary for _, _, primary in members}
        if len(primary_ids) != 1:
            raise ProfileMappingMigrationError(
                f"scoring pathway group has ambiguous primary: {cluster}"
            )
        primary = next(iter(primary_ids))
        groups.append(
            {
                "dependency_cluster": cluster,
                "primary_mapping_id": primary,
                "alternative_mapping_ids": sorted(
                    str(item["id"])
                    for item, role, _ in members
                    if role
                    in {PathwayRoleV2.ALTERNATIVE, PathwayRoleV2.ALTERNATIVE_HANGING}
                ),
                "dependent_carrier_mapping_ids": sorted(
                    str(item["id"])
                    for item, role, _ in members
                    if role is PathwayRoleV2.DEPENDENT_CARRIER
                ),
                "source_dependency_clusters": sorted(
                    {str(item["cluster"]) for item, _, _ in members}
                ),
                "execution_semantics": (
                    "separate confidence-preserving observations; strongest-per-cluster "
                    "dependency control makes pathways compete rather than sum"
                ),
            }
        )
    return {
        "schema_version": "v4-3-v3-6-mapping-migration-receipt-v1",
        "migration_kind": "mechanical-provenance-preserving-pre-ranking-source-migration",
        "source_files": [
            {
                "path": FROZEN_MAPPING_PATH,
                "sha256": sha256_file(root / FROZEN_MAPPING_PATH),
                "schema": base["schema"],
                "status": base["status"],
                "created_utc": base["created_utc"],
            },
            {
                "path": OVERLAY_MAPPING_PATH,
                "sha256": sha256_file(root / OVERLAY_MAPPING_PATH),
                "schema": overlay["schema"],
                "status": overlay["status"],
                "created_utc": overlay["created_utc"],
                "base_mapping": overlay["base_mapping"],
            },
        ],
        "external_hd_citation_provenance": {
            "status": "incomplete",
            "affected_mapping_ids": sorted(str(item["id"]) for item in records),
            "reason": (
                "The frozen source records descriptive Standard Jovian/IHDS source labels "
                "but no exact URL, retrieval timestamp, or retrieved-content hash. The "
                "migration preserves those labels and does not invent missing provenance."
            ),
        },
        "controlling_source_overrides": [
            {
                "mapping_id": "TYPE_PROJECTOR_ENTRY",
                "field": "behavioral_confidence",
                "older_mapping_value": 0.9,
                "controlling_value": 0.85,
                "controlling_source_id": "SRC-TARGET-V36",
                "controlling_source_path": BEHAVIORAL_TARGET_PATH,
                "locator": (
                    "Invitation/recognition is domain-sensitive; "
                    "Behavioral confidence: 0.85"
                ),
                "rationale": (
                    "The V3.6 behavioral target is newer and controlling. This source-only "
                    "override was applied before scoring and without outcome inspection."
                ),
            }
        ],
        "translation_contract": {
            "alternative_pathway_representation": (
                "Each source mapping remains a separate confidence-bearing observation. "
                "Primary and alternative roles are frozen below, and the shared dependency "
                "cluster plus strongest-per-cluster policy makes them compete rather than "
                "sum. Collapsing them into one V2 rule would discard the distinct frozen "
                "behavioral confidences and statements."
            ),
            "hanging_gate_translation": (
                "Every source predicate whose feature is gate is translated to the exact "
                "HANGING_GATES/HAS_GATE predicate and therefore also requires ACTIVE_GATES; "
                "it does not spuriously require activation projection fields."
            ),
            "post_selection_carrier_dependency_resolution": (
                "PMOON_24_DRIVE and DMARS_61_DEVELOPMENT retain their original source "
                "clusters for provenance, but their scoring dependency/pathway group is "
                "EXISTENTIAL_MYSTERY. They are specific post-selection carriers of Gates "
                "24/61, not independent corroborators, so Channel/component/carrier "
                "evidence cannot double-count. This prospective methodological resolution "
                "uses structural identity only and no ranks, winners, or outcomes."
            ),
            "prevalence_parent_translation": (
                "The exact source parent predicates remain hash-bound in the two source "
                "JSON artifacts. Their ordered feature families compile to the V2 "
                "candidate-context conditional hierarchy, with deterministic strict-subset "
                "backoffs ending at root."
            ),
            "measurement_reliability": (
                "The source provides behavioral confidence but no independent measurement "
                "reliability, so the identity factor 1.0 preserves rather than changes it."
            ),
            "revision_and_selection_metadata": (
                "Revision classes R1 for invitation/persuasion and R2 for somatic-label "
                "disambiguation come from the V3.6 target; other records use R0. Because "
                "V3.6 is explicitly best-current descriptive, candidate-direction visibility "
                "is conservatively true and ordinary selection risk is moderate. The two "
                "source-flagged post-selection carrier mappings use high risk and are absent "
                "from the less-contaminated variant."
            ),
            "contradiction_pathway_factors": (
                "The source contradiction has no support-factor fields because its penalty "
                "uses confidence, severity, and the four-rubric-bit contradiction scale only. "
                "Its schema-required anchor uses canonical complete-Channel salience 0.80, "
                "direct mapping 1.00, and narrow F1 1.00; these do not alter the preserved "
                "contradiction penalty."
            ),
        },
        "variants": [
            _variant_receipt(
                "less_contaminated",
                less_source,
                LESS_CONTAMINATED_SOURCE_PATH,
                LESS_CONTAMINATED_COMPILED_PATH,
                artifacts,
                excluded=sorted(_POST_SELECTION_IDS),
            ),
            _variant_receipt(
                "best_current_descriptive",
                best_source,
                BEST_CURRENT_SOURCE_PATH,
                BEST_CURRENT_COMPILED_PATH,
                artifacts,
                excluded=[],
            ),
        ],
        "pathway_groups": groups,
        "contradiction_mapping": {
            "mapping_id": "CONTRA_16_48_MASTERY_DRIVE",
            "severity": 0.5,
            "status": "translated_as_direct_opposition",
        },
        "untranslated_source_mapping_ids": [],
        "unresolved_unscored_constructs": list(_UNRESOLVED_CONSTRUCTS),
        "non_claims": [
            "No historical result, winner, candidate rank, or support value was an input.",
            "The best-current-descriptive variant is not untouched validation.",
            "Identity measurement reliability 1.0 preserves source confidence because no "
            "separate reliability estimate exists; it is not a new empirical estimate.",
        ],
    }


def _variant_receipt(
    variant: MappingVariant,
    source: MappingLibrarySourceV2,
    source_path: str,
    compiled_path: str,
    artifacts: Mapping[str, bytes],
    *,
    excluded: list[str],
) -> dict[str, Any]:
    return {
        "variant": variant,
        "source_path": source_path,
        "source_sha256": sha256_bytes(artifacts[source_path]),
        "source_semantic_sha256": source.sha256(),
        "compiled_path": compiled_path,
        "compiled_sha256": sha256_bytes(artifacts[compiled_path]),
        "excluded_post_selection_mapping_ids": excluded,
        "frozen_rule_count": len(source.frozen_mappings),
        "required_feature_ids": [item.value for item in source.declared_required_feature_ids],
    }


def _source_artifacts(root: Path) -> tuple[SourceArtifactV2, ...]:
    return tuple(
        SourceArtifactV2(
            source_id=source_id,
            role=role,
            path=path,
            sha256=sha256_file(root / path),
            title=title,
        )
        for source_id, role, path, title in _SOURCE_ARTIFACTS
    )


def _pathway_relationship(
    mapping_id: str,
    source_cluster: str,
) -> tuple[str, PathwayRoleV2, str]:
    if mapping_id in _POST_SELECTION_IDS:
        return (
            "EXISTENTIAL_MYSTERY",
            PathwayRoleV2.DEPENDENT_CARRIER,
            "CH_24_61_MYSTERY",
        )
    primary = _PRIMARY_BY_CLUSTER[source_cluster]
    if mapping_id == primary:
        return source_cluster, PathwayRoleV2.PRIMARY, primary
    role = (
        PathwayRoleV2.ALTERNATIVE_HANGING
        if mapping_id.startswith("GATE_")
        else PathwayRoleV2.ALTERNATIVE
    )
    return source_cluster, role, primary


def _revision_class(mapping_id: str) -> RevisionClassV2:
    if mapping_id in {"TYPE_PROJECTOR_ENTRY", "CH_26_44_ENTERPRISE"}:
        return RevisionClassV2.R1
    if mapping_id == "AUTH_SPLENIC_SIGNAL":
        return RevisionClassV2.R2
    return RevisionClassV2.R0


def _structural_class(feature_id: FeatureId) -> StructuralClass:
    return {
        FeatureId.TYPE: StructuralClass.TYPE_STRATEGY,
        FeatureId.AUTHORITY: StructuralClass.AUTHORITY,
        FeatureId.CENTERS: StructuralClass.DIAGNOSTIC_CENTER,
        FeatureId.PROFILE: StructuralClass.PROFILE,
        FeatureId.COMPLETE_CHANNELS: StructuralClass.COMPLETE_CHANNEL,
        FeatureId.HANGING_GATES: StructuralClass.HANGING_GATE,
        FeatureId.PLANETARY_ACTIVATIONS: StructuralClass.PROMINENT_ACTIVATION,
    }[feature_id]


def _directness_class(value: float) -> DirectnessClass:
    for directness, factor in MAPPING_DIRECTNESS.items():
        if value == factor:
            return directness
    raise ProfileMappingMigrationError(f"unsupported frozen directness: {value}")


def _flexibility_class(value: float) -> FlexibilityClass:
    for flexibility, factor in FLEXIBILITY_FACTOR.items():
        if value == factor:
            return flexibility
    raise ProfileMappingMigrationError(f"unsupported frozen flexibility: {value}")


def _feature_label(value: FeatureId) -> str:
    return {
        FeatureId.TYPE: "type",
        FeatureId.AUTHORITY: "authority",
        FeatureId.CENTERS: "centers",
        FeatureId.COMPLETE_CHANNELS: "channels",
    }[value]


def _architecture_value(value: str) -> str:
    return value.strip().casefold().replace(" ", "_").replace("/", "_")


def _center_value(value: str) -> str:
    centers = {
        "Sacral": Center.SACRAL.value,
        "Solar Plexus": Center.SOLAR_PLEXUS.value,
        "Spleen": Center.SPLEEN.value,
        "Root": Center.ROOT.value,
        "Heart": Center.HEART.value,
        "G": Center.G.value,
    }
    try:
        return centers[value]
    except KeyError as exc:
        raise ProfileMappingMigrationError(f"unknown frozen Center: {value}") from exc


def _normalized_id(value: str) -> str:
    normalized = re.sub(r"[^A-Z0-9]+", "-", value.upper()).strip("-")
    if not normalized:
        raise ProfileMappingMigrationError("mapping ID cannot normalize to empty")
    return normalized


def _citation(source_id: str, locator: str, rationale: str) -> SourceCitationV2:
    return SourceCitationV2(source_id=source_id, locator=locator, rationale=rationale)


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileMappingMigrationError(f"cannot read frozen mapping source: {path}") from exc
    if not isinstance(value, dict):
        raise ProfileMappingMigrationError(f"frozen mapping source is not an object: {path}")
    return cast(dict[str, Any], value)


def _only_mapping(value: Mapping[str, Any], field: str) -> Mapping[str, Any]:
    items = _sequence(value[field], field)
    if len(items) != 1 or not isinstance(items[0], Mapping):
        raise ProfileMappingMigrationError(f"{field} must contain exactly one mapping")
    return cast(Mapping[str, Any], items[0])


def _sequence(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, list):
        raise ProfileMappingMigrationError(f"{label} must be a JSON array")
    return value


def _require_keys(
    value: Mapping[str, Any],
    expected: AbstractSet[str],
    label: str,
    *,
    allow_optional: AbstractSet[str] = frozenset(),
) -> None:
    actual = set(value)
    missing = expected - allow_optional - actual
    extra = actual - expected
    if missing or extra:
        raise ProfileMappingMigrationError(
            f"{label} fields changed; missing={sorted(missing)}, extra={sorted(extra)}"
        )


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProfileMappingMigrationError(f"{label} must be numeric")
    return float(value)


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ProfileMappingMigrationError(f"{label} must be an integer")
    return value


def _validate_frozen_constants(value: Mapping[str, Any]) -> None:
    expected = {
        "information_cap_bits": 6.0,
        "contradiction_cap_bits": 4.0,
        "independent_corroborator_cap": 0.15,
        "minimum_parent_state_equivalents": 500,
    }
    for field, required in expected.items():
        if value.get(field) != required:
            raise ProfileMappingMigrationError(f"frozen source constant changed: {field}")
