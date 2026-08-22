from __future__ import annotations

import json
import re
import shutil
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
from pydantic import ValidationError

from hdmatch.century_cache.models import CenturyStateRecord, FeatureValue
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.chart.feature_registry import FeatureId
from hdmatch.model.mapping_library import (
    ContradictionSeverity,
    DirectnessClass,
    StructuralClass,
)
from hdmatch.model.v4_3.integration import (
    V43ObservedResponse,
    evaluate_mapping_library_v2,
)
from hdmatch.model.v4_3.scoring import score_v4_3
from hdmatch.model.v4_3_mapping import (
    ContradictionModeV2,
    MappingLibrarySourceV2,
    MappingLibraryV2,
    MappingStatusV2,
    PathwayRoleV2,
    PredicateOperatorV2,
    SelectionRiskV2,
    load_mapping_library_source_v2,
    load_mapping_library_v2,
)
from hdmatch.model.v4_3_profile_mapping import (
    BEHAVIORAL_TARGET_PATH,
    BEST_CURRENT_COMPILED_PATH,
    BEST_CURRENT_SOURCE_PATH,
    COVERAGE_AUDIT_PATH,
    FROZEN_MAPPING_PATH,
    LESS_CONTAMINATED_COMPILED_PATH,
    LESS_CONTAMINATED_SOURCE_PATH,
    MIGRATION_RECEIPT_PATH,
    OVERLAY_MAPPING_PATH,
    SCORING_POLICY_PATH,
    V43_SCORING_PATH,
    ProfileMappingMigrationError,
    build_profile_mapping_library_source_v2,
    compile_profile_mapping_library_v2,
    generated_profile_mapping_artifacts,
    verify_tracked_profile_mapping_artifacts,
    write_profile_mapping_artifacts_new,
)
from hdmatch.util import sha256_file

ROOT = Path(__file__).resolve().parents[2]

GOLDEN_SHA256 = {
    BEST_CURRENT_COMPILED_PATH: (
        "3c3a0ae72f336c623a058f9d1188f27d2115f4e04bfbfed1a37c5b19180e071c"
    ),
    BEST_CURRENT_SOURCE_PATH: (
        "6e2b4317f25f49995e24afc920442de66916f3e91846517793b0abd616a58439"
    ),
    LESS_CONTAMINATED_COMPILED_PATH: (
        "75f43809abed11bd381fa1c17ac17288d511f155672f0dcc652606a167f4b53b"
    ),
    LESS_CONTAMINATED_SOURCE_PATH: (
        "3a380b0de83965e3c46099909f7b5e8d403b47d50e26632ac5bf854fa69d2e05"
    ),
    MIGRATION_RECEIPT_PATH: (
        "01918c7457871bf85412e46ca3fde49ae999bf92bbf9ad9fc5c216890d407d72"
    ),
}
POST_SELECTION_IDS = {"DMARS_61_DEVELOPMENT", "PMOON_24_DRIVE"}


class _NoEstimatePrevalence:
    def __init__(self, library: MappingLibraryV2) -> None:
        hashes = {field: "a" * 64 for field in (
            "artifact_sha256",
            "plan_sha256",
            "cache_manifest_sha256",
            "cache_trust_lock_sha256",
            "cache_build_plan_sha256",
            "semantic_feature_registry_sha256",
            "physical_feature_registry_sha256",
            "reconciliation_aggregate_sha256",
            "engine_validation_sha256",
            "ephemeris_file_set_sha256",
            "universe_sha256",
            "parent_hierarchy_sha256",
        )}
        self.provenance = SimpleNamespace(
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
            mapping_library_sha256=library.sha256(),
            mapping_source_library_sha256=library.source_library_sha256,
            mapping_prevalence_plan_sha256="b" * 64,
            required_feature_registry_sha256=(
                library.required_feature_registry_sha256
            ),
            policy_version="conditional-prevalence-v4.3-test",
            boundary_policy_version="exact-boundary-test",
            duration_weighted=True,
            conditional=True,
            exact_stable_intervals=True,
            source_scope="declared-global-utc-universe",
            **hashes,
        )

    def bind_candidate_record(
        self,
        candidate_record: object,
        *,
        cache_manifest_sha256: str,
        mapping_library_sha256: str,
    ) -> object:
        del candidate_record, cache_manifest_sha256, mapping_library_sha256
        raise AssertionError("pure scorer test must not mint a cache-row capability")

    def estimate(self, anchor_id: str, candidate_context: object) -> object:
        del anchor_id, candidate_context
        raise AssertionError("unknown responses must not request prevalence estimates")


class _UnitEstimatePrevalence(_NoEstimatePrevalence):
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
            prevalence=1.0,
            numerator_duration_microseconds=1,
            denominator_duration_microseconds=1,
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


def _unknown_candidate(
    library: MappingLibraryV2,
    *,
    candidate_type: str = "projector",
    candidate_strategy: str = "wait_for_invitation",
    candidate_authority: str = "splenic",
    defined_centers: frozenset[str] = frozenset({"g", "heart_ego", "spleen"}),
    candidate_profile: str = "2/4",
) -> CenturyStateRecord:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    all_centers = {
        "ajna",
        "g",
        "head",
        "heart_ego",
        "root",
        "sacral",
        "solar_plexus",
        "spleen",
        "throat",
    }
    feature_values: dict[FeatureId, object] = {
        FeatureId.TYPE: candidate_type,
        FeatureId.STRATEGY: candidate_strategy,
        FeatureId.AUTHORITY: candidate_authority,
        FeatureId.CENTERS: {
            "defined": sorted(defined_centers),
            "undefined": sorted(all_centers - defined_centers),
        },
        FeatureId.PROFILE: candidate_profile,
        FeatureId.COMPLETE_CHANNELS: [],
        FeatureId.ACTIVE_GATES: [],
        FeatureId.HANGING_GATES: [],
        FeatureId.PLANETARY_ACTIVATIONS: [],
        FeatureId.ACTIVATION_GATE: [],
        FeatureId.ACTIVATION_CARRIER: [],
        FeatureId.ACTIVATION_SIDE: [],
    }
    return CenturyStateRecord(
        state_id=(
            f"population-adapter-{candidate_type}-{candidate_strategy}-"
            f"{candidate_authority}-{candidate_profile}"
        ),
        utc_start=start,
        utc_end=start + timedelta(seconds=1),
        duration_seconds=1.0,
        representative_utc=start,
        design_timestamp=start - timedelta(days=88),
        chart_features_sha256="1" * 64,
        feature_vector_schema_version="chart-feature-vector-v2",
        semantic_feature_registry_sha256="2" * 64,
        feature_registry_sha256="3" * 64,
        astronomy_engine_version="test-swisseph",
        ephemeris_file_set_sha256="4" * 64,
        node_convention="true",
        mandala_mapping_version="test",
        mandala_mapping_sha256="5" * 64,
        bodygraph_mapping_sha256="6" * 64,
        feature_values=tuple(
            FeatureValue(feature_id=feature_id.value, value=cast(Any, feature_values[feature_id]))
            for feature_id in library.required_feature_registry.feature_ids
        ),
    )


def _json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def _unknown_responses(library: MappingLibraryV2) -> tuple[V43ObservedResponse, ...]:
    return tuple(
        V43ObservedResponse(
            observation_id=rule.observation_id,
            response_token="unknown",
        )
        for rule in library.rules
    )


def _mapping_records() -> dict[str, dict[str, Any]]:
    base = _json_object(ROOT / FROZEN_MAPPING_PATH)
    overlay = _json_object(ROOT / OVERLAY_MAPPING_PATH)
    records = {
        str(item["id"]): dict(item)
        for item in cast(list[dict[str, Any]], base["mappings"])
    }
    for mapping_id, changes in cast(
        dict[str, dict[str, Any]], overlay["overrides"]
    ).items():
        records[mapping_id].update(changes)
    for item in cast(list[dict[str, Any]], overlay["add_mappings"]):
        records[str(item["id"])] = dict(item)
    return records


def _rule_id(mapping_id: str) -> str:
    normalized = re.sub(r"[^A-Z0-9]+", "-", mapping_id.upper()).strip("-")
    return f"RULE-{normalized}"


def _copy_inputs(destination: Path) -> None:
    for relative in (
        FROZEN_MAPPING_PATH,
        OVERLAY_MAPPING_PATH,
        V43_SCORING_PATH,
        BEHAVIORAL_TARGET_PATH,
        SCORING_POLICY_PATH,
        COVERAGE_AUDIT_PATH,
    ):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def test_tracked_artifacts_are_exact_deterministic_golden_bytes() -> None:
    generated = generated_profile_mapping_artifacts(ROOT)

    assert set(generated) == set(GOLDEN_SHA256)
    for relative, expected_sha256 in GOLDEN_SHA256.items():
        assert (ROOT / relative).read_bytes() == generated[relative]
        assert sha256_file(ROOT / relative) == expected_sha256
    verify_tracked_profile_mapping_artifacts(ROOT)


def test_both_variants_parse_and_recompile_exactly() -> None:
    for variant, source_path, compiled_path in (
        (
            "less_contaminated",
            LESS_CONTAMINATED_SOURCE_PATH,
            LESS_CONTAMINATED_COMPILED_PATH,
        ),
        ("best_current_descriptive", BEST_CURRENT_SOURCE_PATH, BEST_CURRENT_COMPILED_PATH),
    ):
        source = load_mapping_library_source_v2(ROOT / source_path)
        compiled = load_mapping_library_v2(ROOT / compiled_path)

        assert MappingLibrarySourceV2.model_validate(
            source.model_dump(mode="json")
        ) == source
        assert MappingLibraryV2.model_validate(compiled.model_dump(mode="json")) == compiled
        assert compile_profile_mapping_library_v2(ROOT, variant=variant) == compiled
        assert compiled.source_library_sha256 == source.sha256()
        assert compiled.required_feature_registry_sha256 == (
            compiled.required_feature_registry.sha256()
        )


def test_actual_tracked_artifact_declares_direct_target_response_source() -> None:
    library = load_mapping_library_v2(ROOT / LESS_CONTAMINATED_COMPILED_PATH)
    target_source = next(
        item
        for item in library.source_artifacts
        if item.source_id == library.behavioral_target_source_id
    )
    assert library.response_source_mode.value == "direct_behavioral_target"
    assert target_source.sha256 == sha256_file(ROOT / target_source.path)
    assert library.question_bank_source_id is None


@pytest.mark.parametrize(
    "compiled_path",
    (LESS_CONTAMINATED_COMPILED_PATH, BEST_CURRENT_COMPILED_PATH),
)
def test_both_variants_adapt_and_score_without_structural_reuse(
    compiled_path: str,
) -> None:
    library = load_mapping_library_v2(ROOT / compiled_path)
    candidate = _unknown_candidate(library)
    responses = _unknown_responses(library)

    adapted = evaluate_mapping_library_v2(library, candidate, responses)
    score = score_v4_3(adapted, _NoEstimatePrevalence(library))

    observations = {item.observation_id: item for item in adapted.observations}
    mystery_cluster = observations["OBS-CH-24-61-MYSTERY"].dependency_cluster
    assert observations["OBS-GATE-24-RETURN-ALT"].dependency_cluster == mystery_cluster
    assert observations["OBS-GATE-61-MYSTERY-ALT"].dependency_cluster == mystery_cluster
    if compiled_path == BEST_CURRENT_COMPILED_PATH:
        assert observations["OBS-PMOON-24-DRIVE"].dependency_cluster == mystery_cluster
        assert observations["OBS-DMARS-61-DEVELOPMENT"].dependency_cluster == mystery_cluster
    assert score.evidence_rubric_bits == 0.0
    assert score.contradiction_rubric_bits == 0.0
    assert score.detailed_support == 0.0


@pytest.mark.parametrize(
    ("candidate_overrides", "expected_fractions", "expected_core_fit"),
    (
        ({}, (1.0, 1.0, 1.0, 1.0), 100.0),
        (
            {"candidate_type": "generator", "candidate_strategy": "wait_to_respond"},
            (0.0, 1.0, 1.0, 1.0),
            70.0,
        ),
        (
            {"candidate_strategy": "inform"},
            (0.0, 1.0, 1.0, 1.0),
            70.0,
        ),
        (
            {"candidate_authority": "emotional_solar_plexus"},
            (1.0, 0.0, 1.0, 1.0),
            70.0,
        ),
        (
            {"defined_centers": frozenset({"g", "heart_ego", "root", "spleen"})},
            (1.0, 1.0, 5.0 / 6.0, 1.0),
            100.0 * (30.0 + 30.0 + 25.0 * 5.0 / 6.0 + 15.0) / 100.0,
        ),
        ({"candidate_profile": "5/1"}, (1.0, 1.0, 1.0, 0.0), 85.0),
        ({"candidate_profile": "1/5"}, (1.0, 1.0, 1.0, 0.0), 85.0),
        ({"candidate_profile": "2/5"}, (1.0, 1.0, 1.0, 0.5), 92.5),
        ({"candidate_profile": "5/4"}, (1.0, 1.0, 1.0, 0.5), 92.5),
        ({"candidate_profile": "4/2"}, (1.0, 1.0, 1.0, 1.0 / 3.0), 90.0),
    ),
)
def test_actual_canonical_corefit_uses_exact_architecture_not_detailed_rules(
    candidate_overrides: dict[str, object],
    expected_fractions: tuple[float, float, float, float],
    expected_core_fit: float,
) -> None:
    library = load_mapping_library_v2(ROOT / LESS_CONTAMINATED_COMPILED_PATH)
    candidate = _unknown_candidate(library, **candidate_overrides)  # type: ignore[arg-type]
    adapted = evaluate_mapping_library_v2(
        library,
        candidate,
        _unknown_responses(library),
    )
    score = score_v4_3(adapted, _NoEstimatePrevalence(library))

    assert tuple(item.earned_fraction for item in adapted.core_blocks) == pytest.approx(
        expected_fractions
    )
    assert all(item.availability.value == "reportable" for item in adapted.core_blocks)
    assert score.core_fit == pytest.approx(expected_core_fit)
    assert score.detailed_support == 0.0


def test_line_five_detailed_support_cannot_leak_into_profile_corefit() -> None:
    library = load_mapping_library_v2(ROOT / LESS_CONTAMINATED_COMPILED_PATH)
    responses = list(_unknown_responses(library))
    line_five = next(
        rule
        for rule in library.rules
        if rule.observation_id == "OBS-PROFILE-LINE5-PROJECTION"
    )
    responses = [
        (
            V43ObservedResponse(
                observation_id=item.observation_id,
                response_token=line_five.response_rule.canonical_response_token,
            )
            if item.observation_id == line_five.observation_id
            else item
        )
        for item in responses
    ]
    adapted = evaluate_mapping_library_v2(
        library,
        _unknown_candidate(library, candidate_profile="5/1"),
        tuple(responses),
    )
    score = score_v4_3(adapted, _UnitEstimatePrevalence(library))

    profile = next(item for item in adapted.core_blocks if item.block.value == "profile")
    assert profile.earned_fraction == 0.0
    assert score.core_fit == pytest.approx(85.0)
    assert score.detailed_support > 0.0


def test_less_contaminated_excludes_only_the_two_post_selection_carriers() -> None:
    less = load_mapping_library_v2(ROOT / LESS_CONTAMINATED_COMPILED_PATH)
    best = load_mapping_library_v2(ROOT / BEST_CURRENT_COMPILED_PATH)
    less_rule_ids = {item.rule_id for item in less.rules}
    best_rule_ids = {item.rule_id for item in best.rules}

    assert len(less.rules) == 43
    assert len(best.rules) == 45
    assert best_rule_ids - less_rule_ids == {_rule_id(item) for item in POST_SELECTION_IDS}
    assert less_rule_ids < best_rule_ids
    assert FeatureId.PLANETARY_ACTIVATIONS not in (
        less.required_feature_registry.feature_ids
    )
    assert FeatureId.ACTIVATION_GATE not in less.required_feature_registry.feature_ids
    assert {
        FeatureId.PLANETARY_ACTIVATIONS,
        FeatureId.ACTIVATION_CARRIER,
        FeatureId.ACTIVATION_GATE,
        FeatureId.ACTIVATION_SIDE,
    }.issubset(best.required_feature_registry.feature_ids)


def test_every_frozen_mapping_preserves_behavior_confidence_factors_and_predicate() -> None:
    records = _mapping_records()
    source = load_mapping_library_source_v2(ROOT / BEST_CURRENT_SOURCE_PATH)
    rules = {item.rule_id: item for item in source.frozen_mappings}

    assert len(records) == 44
    for mapping_id, record in records.items():
        rule = rules[_rule_id(mapping_id)]
        pathway = rule.primary_pathway
        predicate = pathway.predicate
        original = cast(dict[str, Any], record["predicate"])

        assert rule.status is MappingStatusV2.FROZEN
        assert rule.behavioral_statement == record["behavior"]
        expected_confidence = (
            0.85 if mapping_id == "TYPE_PROJECTOR_ENTRY" else record["confidence"]
        )
        assert rule.behavioral_confidence == expected_confidence
        assert rule.measurement_reliability == 1.0
        assert rule.source_dependency_cluster == record["cluster"]
        if mapping_id in POST_SELECTION_IDS:
            assert rule.dependency_cluster == "EXISTENTIAL_MYSTERY"
            assert rule.pathway_group_id == "EXISTENTIAL_MYSTERY"
            assert rule.pathway_role is PathwayRoleV2.DEPENDENT_CARRIER
            assert rule.primary_rule_id == _rule_id("CH_24_61_MYSTERY")
        else:
            assert rule.dependency_cluster == record["cluster"]
            assert rule.pathway_group_id == record["cluster"]
        assert pathway.structural_salience == record["salience"]
        assert pathway.mapping_directness == record["directness"]
        assert pathway.flexibility_factor == record["flexibility"]
        assert f"mapping id {mapping_id}" in {
            item.locator for item in pathway.sources
        }
        assert str(record["source"]) in pathway.rationale

        feature = original["feature"]
        if feature == "type":
            assert predicate.feature_id is FeatureId.TYPE
            assert predicate.values == (str(original["equals"]).casefold(),)
        elif feature == "authority":
            assert predicate.feature_id is FeatureId.AUTHORITY
            assert predicate.values == (str(original["equals"]).casefold(),)
        elif feature == "center":
            assert predicate.feature_id is FeatureId.CENTERS
            expected_operator = (
                PredicateOperatorV2.CONTAINS_ANY
                if original["defined"]
                else PredicateOperatorV2.NOT_CONTAINS_ANY
            )
            assert predicate.operator is expected_operator
        elif feature == "profile":
            assert predicate.feature_id is FeatureId.PROFILE
            assert predicate.operator is PredicateOperatorV2.EQUALS_ANY
            assert predicate.values == (original["equals"],)
        elif feature == "profile_has_line":
            assert predicate.feature_id is FeatureId.PROFILE
            assert predicate.operator is PredicateOperatorV2.PROFILE_HAS_LINE
            assert predicate.values == (str(original["line"]),)
        elif feature == "channel":
            assert predicate.feature_id is FeatureId.COMPLETE_CHANNELS
            assert predicate.operator is PredicateOperatorV2.CONTAINS_ANY
            assert predicate.values == (original["equals"],)
        elif feature == "gate":
            assert predicate.feature_id is FeatureId.HANGING_GATES
            assert predicate.operator is PredicateOperatorV2.HAS_GATE
            assert predicate.gate == original["equals"]
            assert FeatureId.ACTIVE_GATES in pathway.required_feature_ids
        else:
            assert feature == "activation"
            assert predicate.feature_id is FeatureId.PLANETARY_ACTIVATIONS
            assert predicate.operator is PredicateOperatorV2.MATCHES_ACTIVATION
            assert predicate.side == original["side"]
            assert predicate.carrier is CelestialBody(str(original["body"]))
            assert predicate.gate == original["gate"]


def test_documented_primary_alternative_and_hanging_groups_are_frozen() -> None:
    receipt = _json_object(ROOT / MIGRATION_RECEIPT_PATH)
    groups = {
        item["dependency_cluster"]: item
        for item in cast(list[dict[str, Any]], receipt["pathway_groups"])
    }

    assert groups["AUTHORITY_SOMATIC"] == {
        "dependency_cluster": "AUTHORITY_SOMATIC",
        "primary_mapping_id": "AUTH_SPLENIC_SIGNAL",
        "alternative_mapping_ids": ["GATE_57_SOMATIC_ALT"],
        "dependent_carrier_mapping_ids": [],
        "source_dependency_clusters": ["AUTHORITY_SOMATIC"],
        "execution_semantics": (
            "separate confidence-preserving observations; strongest-per-cluster "
            "dependency control makes pathways compete rather than sum"
        ),
    }
    assert groups["ORIGINAL_CONTRIBUTION"]["primary_mapping_id"] == "CH_1_8_ORIGINAL"
    assert groups["ORIGINAL_CONTRIBUTION"]["alternative_mapping_ids"] == [
        "GATE_1_ORIGINAL_ALT",
        "GATE_8_CONTRIBUTION_ALT",
    ]
    assert groups["EXISTENTIAL_MYSTERY"]["primary_mapping_id"] == "CH_24_61_MYSTERY"
    assert groups["EXISTENTIAL_MYSTERY"]["alternative_mapping_ids"] == [
        "CH_47_64_MEANING_ALT",
        "GATE_24_RETURN_ALT",
        "GATE_61_MYSTERY_ALT",
    ]
    assert groups["EXISTENTIAL_MYSTERY"]["dependent_carrier_mapping_ids"] == [
        "DMARS_61_DEVELOPMENT",
        "PMOON_24_DRIVE",
    ]
    assert groups["EXISTENTIAL_MYSTERY"]["source_dependency_clusters"] == [
        "EXISTENTIAL_MYSTERY",
        "MYSTERY_DEVELOPMENT_CARRIER",
        "MYSTERY_DRIVE_CARRIER",
    ]
    assert groups["PROFILE_STRUCTURE"]["alternative_mapping_ids"] == [
        "PROFILE_LINE5_PROJECTION",
        "PROFILE_LINE6_PHASES",
    ]

    source = load_mapping_library_source_v2(ROOT / BEST_CURRENT_SOURCE_PATH)
    by_id = {item.rule_id: item for item in source.frozen_mappings}
    roles = {item.pathway_role for item in source.frozen_mappings}
    assert roles == set(PathwayRoleV2)
    assert sum(
        item.pathway_role
        in {PathwayRoleV2.ALTERNATIVE, PathwayRoleV2.ALTERNATIVE_HANGING}
        for item in source.frozen_mappings
    ) == 19
    gate_alternatives = {
        mapping_id
        for group in groups.values()
        for mapping_id in group["alternative_mapping_ids"]
        if mapping_id.startswith("GATE_")
    }
    assert gate_alternatives
    for mapping_id in gate_alternatives:
        rule = by_id[_rule_id(mapping_id)]
        assert rule.pathway_role is PathwayRoleV2.ALTERNATIVE_HANGING
        assert rule.primary_rule_id != rule.rule_id
        assert rule.primary_pathway.structural_class is StructuralClass.HANGING_GATE
        assert rule.primary_pathway.predicate.feature_id is FeatureId.HANGING_GATES
        assert FeatureId.ACTIVATION_GATE not in rule.primary_pathway.required_feature_ids


def test_typed_group_linkage_rejects_missing_or_cross_group_primary() -> None:
    source = load_mapping_library_source_v2(ROOT / BEST_CURRENT_SOURCE_PATH)
    payload = source.model_dump(mode="json")
    mappings = cast(list[dict[str, Any]], payload["mappings"])
    carrier = next(
        item for item in mappings if item["rule_id"] == _rule_id("PMOON_24_DRIVE")
    )
    carrier["primary_rule_id"] = "RULE-MISSING"
    with pytest.raises(ValidationError, match="unknown primary"):
        MappingLibrarySourceV2.model_validate(payload)

    payload = source.model_dump(mode="json")
    mappings = cast(list[dict[str, Any]], payload["mappings"])
    carrier = next(
        item for item in mappings if item["rule_id"] == _rule_id("PMOON_24_DRIVE")
    )
    carrier["primary_rule_id"] = _rule_id("TYPE_PROJECTOR_ENTRY")
    with pytest.raises(ValidationError, match="across pathway groups"):
        MappingLibrarySourceV2.model_validate(payload)


def test_source_overrides_and_single_direct_contradiction_are_preserved() -> None:
    source = load_mapping_library_source_v2(ROOT / BEST_CURRENT_SOURCE_PATH)
    rules = {item.rule_id: item for item in source.frozen_mappings}

    root_rule = rules[_rule_id("CENTER_ROOT_OPEN")]
    assert root_rule.behavioral_confidence == 0.75
    assert root_rule.primary_pathway.mapping_directness == 0.75
    assert root_rule.primary_pathway.directness_class is DirectnessClass.STRONG
    heart_rule = rules[_rule_id("CENTER_HEART_DEFINED")]
    assert heart_rule.behavioral_confidence == 0.9
    assert heart_rule.primary_pathway.mapping_directness == 1.0
    assert heart_rule.primary_pathway.directness_class is DirectnessClass.DIRECT
    projector = rules[_rule_id("TYPE_PROJECTOR_ENTRY")]
    assert projector.behavioral_confidence == 0.85
    assert any(
        item.source_id == "SRC-TARGET-V36"
        and "Behavioral confidence: 0.85" in item.locator
        for item in projector.sources
    )

    contradiction = rules[_rule_id("CONTRA_16_48_MASTERY_DRIVE")]
    response = contradiction.response_rule
    assert response.contradiction.mode is ContradictionModeV2.DIRECT_OPPOSITION
    assert response.contradiction.severity is ContradictionSeverity.MEANINGFUL
    assert response.contradiction.opposing_response_tokens == (
        "denies_generalized_mastery_drive",
    )
    assert contradiction.primary_pathway.predicate.values == ("16-48",)
    assert sum(
        item.response_rule.contradiction.mode
        is ContradictionModeV2.DIRECT_OPPOSITION
        for item in source.frozen_mappings
    ) == 1


def test_receipt_binds_source_freeze_and_marks_missing_external_provenance() -> None:
    receipt = _json_object(ROOT / MIGRATION_RECEIPT_PATH)
    sources = {item["path"]: item for item in receipt["source_files"]}

    assert sources[FROZEN_MAPPING_PATH] == {
        "path": FROZEN_MAPPING_PATH,
        "sha256": "f16565094a1a8eede720dd369dfdd4c0d4700a213520b535de28f8f88dd40afd",
        "schema": "v4.3-profile-audit-mapping-v1",
        "status": "frozen-before-ranking-best-current-descriptive",
        "created_utc": "2026-08-22T08:55:00Z",
    }
    assert sources[OVERLAY_MAPPING_PATH]["sha256"] == (
        "03d25392f9639fb985f806d4814743bbb1cf466bc803c42b6bf6ca8588337735"
    )
    assert sources[OVERLAY_MAPPING_PATH]["created_utc"] == "2026-08-22T09:02:00Z"
    provenance = receipt["external_hd_citation_provenance"]
    assert provenance["status"] == "incomplete"
    assert set(provenance["affected_mapping_ids"]) == set(_mapping_records())
    assert "does not invent missing provenance" in provenance["reason"]
    assert receipt["controlling_source_overrides"] == [
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
    ]
    carrier_resolution = receipt["translation_contract"][
        "post_selection_carrier_dependency_resolution"
    ]
    assert "not independent corroborators" in carrier_resolution
    assert "no ranks, winners, or outcomes" in carrier_resolution
    assert receipt["untranslated_source_mapping_ids"] == []
    assert len(receipt["unresolved_unscored_constructs"]) == 14
    assert "historical result" in receipt["non_claims"][0]


def test_source_bytes_and_tracked_artifact_tamper_fail_closed(tmp_path: Path) -> None:
    _copy_inputs(tmp_path)
    source_path = tmp_path / FROZEN_MAPPING_PATH
    source_path.write_bytes(source_path.read_bytes() + b"\n")

    with pytest.raises(ProfileMappingMigrationError, match="source hash changed"):
        build_profile_mapping_library_source_v2(
            tmp_path,
            variant="best_current_descriptive",
        )

    clean = tmp_path / "clean"
    _copy_inputs(clean)
    for relative, content in generated_profile_mapping_artifacts(clean).items():
        destination = clean / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    tracked = clean / BEST_CURRENT_COMPILED_PATH
    tracked.write_bytes(tracked.read_bytes() + b"\n")
    with pytest.raises(ProfileMappingMigrationError, match="tracked mapping artifact differs"):
        verify_tracked_profile_mapping_artifacts(clean)


def test_writer_refuses_partial_or_complete_overwrite(tmp_path: Path) -> None:
    _copy_inputs(tmp_path)
    existing = tmp_path / BEST_CURRENT_COMPILED_PATH
    existing.parent.mkdir(parents=True, exist_ok=True)
    existing.write_bytes(b"do-not-overwrite")

    with pytest.raises(ProfileMappingMigrationError, match="refusing to replace"):
        write_profile_mapping_artifacts_new(tmp_path)

    assert existing.read_bytes() == b"do-not-overwrite"
    assert not (tmp_path / LESS_CONTAMINATED_SOURCE_PATH).exists()


def test_post_selection_risk_is_explicit_and_only_on_best_current_carriers() -> None:
    source = load_mapping_library_source_v2(ROOT / BEST_CURRENT_SOURCE_PATH)
    high_risk = {
        item.rule_id
        for item in source.frozen_mappings
        if item.selection_risk is SelectionRiskV2.HIGH
    }

    assert high_risk == {_rule_id(item) for item in POST_SELECTION_IDS}
    for mapping_id in POST_SELECTION_IDS:
        rule = next(
            item for item in source.frozen_mappings if item.rule_id == _rule_id(mapping_id)
        )
        assert rule.primary_pathway.structural_class is StructuralClass.PROMINENT_ACTIVATION
