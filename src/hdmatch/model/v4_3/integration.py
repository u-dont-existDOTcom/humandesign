"""Canonical artifact adapter for MappingLibraryV2 and the pure V4.3 scorer.

This module is the only canonical-claim path.  It verifies a lock-backed cache,
derives candidate evaluations from compiled predicates and public responses, and
requires a prevalence provider whose plan/artifact/cache identities are bound to
the same mapping and exact universe.  It never accepts compliance booleans.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Final, cast

from pydantic import JsonValue

from hdmatch.century_cache.models import CenturyStateRecord, VerifiedCenturyCache
from hdmatch.century_cache.store import (
    iter_verified_century_cache_rows,
    verify_century_cache_against_trust_lock,
)
from hdmatch.century_cache.trust_lock import (
    CenturyCacheTrustLockV1,
    load_century_cache_trust_lock,
)
from hdmatch.chart.feature_registry import FeatureId
from hdmatch.experiments.canonical import sha256_file, sha256_json
from hdmatch.model.mapping_library import (
    DirectnessClass as MappingDirectnessClass,
)
from hdmatch.model.mapping_library import (
    StructuralClass as MappingStructuralClass,
)
from hdmatch.model.v4_3.compliance import (
    V43Compliance,
    _mint_verified_v4_3_compliance_evidence,
    require_v4_3_compliance,
)
from hdmatch.model.v4_3.contracts import (
    ConditionalPrevalenceCandidateBindingLike,
    ConditionalPrevalenceProvider,
    CoreBlock,
    CoreBlockAvailability,
    CoreBlockEvaluation,
    DirectnessClass,
    EvaluatedContradiction,
    EvaluatedPathway,
    EvaluatedStructuralAnchor,
    FlexibilityClass,
    ObservationConfidence,
    ObservationEvaluation,
    ResponseDisposition,
    StructuralClass,
    V43ScoringInput,
)
from hdmatch.model.v4_3.ranking import ScoredExactInterval
from hdmatch.model.v4_3.scoring import (
    GLOBAL_PREVALENCE_SOURCE_SCOPE,
    V43CandidateScore,
    score_v4_3,
)
from hdmatch.model.v4_3_mapping import (
    CompiledMappingRuleV2,
    CompiledPathwayV2,
    ContradictionModeV2,
    MappingLibraryV2,
    PredicateOperatorV2,
    StructuralPredicateV2,
)
from hdmatch.model.v4_3_mapping import (
    FlexibilityClass as MappingFlexibilityClass,
)

_SESSION_TOKEN: Final[object] = object()
_CARDINAL_POSITIONS: Final[tuple[str, ...]] = (
    "personality:sun",
    "personality:earth",
    "design:sun",
    "design:earth",
)

_STRUCTURAL_CLASS_ADAPTER: Final[dict[MappingStructuralClass, StructuralClass]] = {
    MappingStructuralClass.TYPE_STRATEGY: StructuralClass.TYPE_STRATEGY,
    MappingStructuralClass.AUTHORITY: StructuralClass.AUTHORITY,
    MappingStructuralClass.DIAGNOSTIC_CENTER: StructuralClass.DIAGNOSTIC_CENTER,
    MappingStructuralClass.PROFILE: StructuralClass.PROFILE,
    MappingStructuralClass.COMPLETE_CHANNEL: StructuralClass.COMPLETE_CHANNEL,
    MappingStructuralClass.CARDINAL_ACTIVATION: StructuralClass.CARDINAL_SUN_EARTH,
    MappingStructuralClass.DEFINITION: StructuralClass.DEFINITION,
    MappingStructuralClass.REPEATED_GATE_OR_NODE: StructuralClass.REPEATED_GATE_OR_NODE,
    MappingStructuralClass.PROMINENT_ACTIVATION: (
        StructuralClass.PROMINENT_PLANETARY_ACTIVATION
    ),
    MappingStructuralClass.HANGING_GATE: StructuralClass.ORDINARY_HANGING_GATE,
    MappingStructuralClass.GENERIC_SYMBOLISM: StructuralClass.GENERIC_SYMBOLISM,
}
_DIRECTNESS_CLASS_ADAPTER: Final[dict[MappingDirectnessClass, DirectnessClass]] = {
    MappingDirectnessClass.DIRECT: DirectnessClass.DIRECT,
    MappingDirectnessClass.STRONG: DirectnessClass.STRONG,
    MappingDirectnessClass.PLAUSIBLE: DirectnessClass.PLAUSIBLE,
    MappingDirectnessClass.NONE: DirectnessClass.NONE,
}
_FLEXIBILITY_CLASS_ADAPTER: Final[
    dict[MappingFlexibilityClass, FlexibilityClass]
] = {
    MappingFlexibilityClass.F1: FlexibilityClass.F1_NARROW,
    MappingFlexibilityClass.F2: FlexibilityClass.F2_MODERATE,
    MappingFlexibilityClass.F3: FlexibilityClass.F3_BROAD,
    MappingFlexibilityClass.F4: FlexibilityClass.F4_VERY_FLEXIBLE,
}
_CORE_CLASS_TO_BLOCK: Final[dict[StructuralClass, CoreBlock]] = {
    StructuralClass.TYPE_STRATEGY: CoreBlock.TYPE_STRATEGY,
    StructuralClass.AUTHORITY: CoreBlock.AUTHORITY,
    StructuralClass.DIAGNOSTIC_CENTER: CoreBlock.DIAGNOSTIC_CENTERS,
    StructuralClass.PROFILE: CoreBlock.PROFILE,
}

if set(_STRUCTURAL_CLASS_ADAPTER) != set(MappingStructuralClass):
    raise RuntimeError("V4.3 structural-class adapter is incomplete")
if set(_DIRECTNESS_CLASS_ADAPTER) != set(MappingDirectnessClass):
    raise RuntimeError("V4.3 directness-class adapter is incomplete")
if set(_FLEXIBILITY_CLASS_ADAPTER) != set(MappingFlexibilityClass):
    raise RuntimeError("V4.3 flexibility-class adapter is incomplete")


class V43IntegrationError(RuntimeError):
    """A canonical adapter identity, coverage, or predicate invariant failed."""


@dataclass(frozen=True, slots=True)
class V43ObservedResponse:
    observation_id: str
    response_token: str

    def __post_init__(self) -> None:
        if not self.observation_id or not self.response_token:
            raise ValueError("V4.3 responses require observation ID and token")


@dataclass(frozen=True, slots=True)
class CanonicalV43Bindings:
    mapping_library_sha256: str
    mapping_source_library_sha256: str
    required_feature_registry_sha256: str
    mapping_prevalence_plan_sha256: str
    question_bank_sha256: str
    prevalence_artifact_sha256: str
    prevalence_plan_sha256: str
    prevalence_parent_hierarchy_sha256: str
    cache_manifest_sha256: str
    cache_trust_lock_sha256: str
    logical_universe_sha256: str


@dataclass(frozen=True, slots=True)
class CanonicalV43CandidateEvaluation:
    state_id: str
    candidate_record_sha256: str
    response_set_sha256: str
    scoring_input: V43ScoringInput
    score: V43CandidateScore
    ranked_interval: ScoredExactInterval
    bindings: CanonicalV43Bindings
    _mint_token: object | None = field(default=None, init=False, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class CanonicalV43CompleteUniverseResult:
    compliance: V43Compliance
    scored_candidate_count: int
    logical_universe_sha256: str
    response_set_sha256: str
    bindings: CanonicalV43Bindings


class CanonicalV43ScoringSession:
    """A session opened only from current trust-verified artifact bytes."""

    __slots__ = (
        "_cache",
        "_library",
        "_prevalence",
        "_response_set_sha256",
        "_trust_lock",
        "_trust_lock_path",
        "_token",
        "bindings",
    )

    def __init__(
        self,
        *,
        library: MappingLibraryV2,
        cache: VerifiedCenturyCache,
        trust_lock: CenturyCacheTrustLockV1,
        trust_lock_path: Path,
        prevalence: ConditionalPrevalenceProvider,
        bindings: CanonicalV43Bindings,
        _token: object,
    ) -> None:
        if _token is not _SESSION_TOKEN:
            raise V43IntegrationError("canonical V4.3 sessions must use the verified factory")
        self._library = library
        self._cache = cache
        self._trust_lock = trust_lock
        self._trust_lock_path = trust_lock_path
        self._prevalence = prevalence
        self._response_set_sha256: str | None = None
        self.bindings = bindings
        self._token = _token

    @classmethod
    def open(
        cls,
        *,
        mapping_library: MappingLibraryV2,
        cache_directory: str | Path,
        trust_lock_path: str | Path,
        prevalence: ConditionalPrevalenceProvider,
    ) -> CanonicalV43ScoringSession:
        if not isinstance(prevalence, ConditionalPrevalenceProvider):
            raise V43IntegrationError(
                "prevalence provider lacks the strict verified candidate-binding interface"
            )
        library = MappingLibraryV2.model_validate(
            mapping_library.model_dump(mode="json")
        )
        lock_path = Path(trust_lock_path)
        lock_hash = sha256_file(lock_path)
        lock = load_century_cache_trust_lock(lock_path)
        cache = verify_century_cache_against_trust_lock(
            cache_directory,
            trust_lock_path=lock_path,
        )
        if lock.manifest_sha256 != cache.manifest_sha256:
            raise V43IntegrationError("cache/trust-lock manifest identity mismatch")
        try:
            bindings = _verify_canonical_artifact_bindings(
                library=library,
                cache=cache,
                trust_lock=lock,
                trust_lock_sha256=lock_hash,
                prevalence=prevalence,
            )
        except AttributeError as exc:
            raise V43IntegrationError(
                "prevalence provider provenance lacks a mandatory V4.3 identity binding"
            ) from exc
        _require_unchanged(cache, lock_path, lock_hash)
        return cls(
            library=library,
            cache=cache,
            trust_lock=lock,
            trust_lock_path=lock_path,
            prevalence=prevalence,
            bindings=bindings,
            _token=_SESSION_TOKEN,
        )

    def score_candidate(
        self,
        candidate: CenturyStateRecord,
        responses: tuple[V43ObservedResponse, ...],
    ) -> CanonicalV43CandidateEvaluation:
        _require_unchanged(
            self._cache,
            self._trust_lock_path,
            self.bindings.cache_trust_lock_sha256,
        )
        self._require_current_provider_bindings()
        record_hash = sha256_json(candidate.model_dump(mode="json"))
        _verify_record_cache_bindings(candidate, self._cache)
        binding = self._prevalence.bind_candidate_record(
            candidate,
            cache_manifest_sha256=self.bindings.cache_manifest_sha256,
            mapping_library_sha256=self.bindings.mapping_library_sha256,
        )
        _verify_candidate_binding(
            binding,
            candidate=candidate,
            candidate_record_sha256=record_hash,
            bindings=self.bindings,
        )
        response_set_sha256 = sha256_json(
            [
                {
                    "observation_id": item.observation_id,
                    "response_token": item.response_token,
                }
                for item in sorted(responses, key=lambda value: value.observation_id)
            ]
        )
        if self._response_set_sha256 is None:
            self._response_set_sha256 = response_set_sha256
        elif response_set_sha256 != self._response_set_sha256:
            raise V43IntegrationError(
                "one canonical universe rescore cannot mix response sets"
            )
        scoring_input = evaluate_mapping_library_v2(
            self._library,
            candidate,
            responses,
        )
        score = score_v4_3(scoring_input, self._prevalence)
        duration_microseconds = _exact_duration_microseconds(candidate)
        ranked = ScoredExactInterval(
            candidate_id=candidate.state_id,
            utc_start=candidate.utc_start,
            stable_duration_microseconds=duration_microseconds,
            score=score,
        )
        evaluation = CanonicalV43CandidateEvaluation(
            state_id=candidate.state_id,
            candidate_record_sha256=record_hash,
            response_set_sha256=response_set_sha256,
            scoring_input=scoring_input,
            score=score,
            ranked_interval=ranked,
            bindings=self.bindings,
        )
        object.__setattr__(evaluation, "_mint_token", _SESSION_TOKEN)
        return evaluation

    def require_complete_universe_compliance(
        self,
        evaluations: tuple[CanonicalV43CandidateEvaluation, ...],
    ) -> CanonicalV43CompleteUniverseResult:
        """Mint compliance only after every exact cache row was scored once, in order."""

        _require_unchanged(
            self._cache,
            self._trust_lock_path,
            self.bindings.cache_trust_lock_sha256,
        )
        self._require_current_provider_bindings()
        if len(evaluations) != self._cache.manifest.interval_count:
            raise V43IntegrationError("complete declared universe was not rescored")
        if any(item._mint_token is not _SESSION_TOKEN for item in evaluations):
            raise V43IntegrationError(
                "candidate evaluation was not minted by the canonical scoring session"
            )
        if self._response_set_sha256 is None or any(
            item.response_set_sha256 != self._response_set_sha256 for item in evaluations
        ):
            raise V43IntegrationError("complete-universe response-set identity mismatch")
        if any(item.bindings != self.bindings for item in evaluations):
            raise V43IntegrationError("candidate evaluation artifact bindings differ")
        observed = tuple(
            (item.state_id, item.candidate_record_sha256) for item in evaluations
        )
        expected = tuple(
            (row.state_id, sha256_json(row.model_dump(mode="json")))
            for row in iter_verified_century_cache_rows(self._cache)
        )
        if observed != expected:
            raise V43IntegrationError(
                "scored record identities/order differ from the verified complete universe"
            )
        required = frozenset(
            item.value for item in self._library.required_feature_registry.feature_ids
        )
        compliance = require_v4_3_compliance(
            _mint_verified_v4_3_compliance_evidence(
                required_feature_ids=required,
                available_feature_ids=required,
                ephemeris_requested=self._cache.manifest.engine.ephemeris_requested,
                ephemeris_returned=self._cache.manifest.engine.ephemeris_returned,
                prevalence_source_scope=self._prevalence.provenance.source_scope,
            )
        )
        return CanonicalV43CompleteUniverseResult(
            compliance=compliance,
            scored_candidate_count=len(evaluations),
            logical_universe_sha256=self._cache.manifest.logical_universe_sha256,
            response_set_sha256=self._response_set_sha256,
            bindings=self.bindings,
        )

    def _require_current_provider_bindings(self) -> None:
        try:
            current = _verify_canonical_artifact_bindings(
                library=self._library,
                cache=self._cache,
                trust_lock=self._trust_lock,
                trust_lock_sha256=self.bindings.cache_trust_lock_sha256,
                prevalence=self._prevalence,
            )
        except AttributeError as exc:
            raise V43IntegrationError(
                "prevalence provider provenance changed or became incomplete"
            ) from exc
        if current != self.bindings:
            raise V43IntegrationError(
                "prevalence provider artifact bindings changed after session open"
            )


def evaluate_mapping_library_v2(
    library: MappingLibraryV2,
    candidate: CenturyStateRecord,
    responses: tuple[V43ObservedResponse, ...],
) -> V43ScoringInput:
    """Pure, non-claiming MappingLibraryV2-to-scorer adapter."""

    validated = MappingLibraryV2.model_validate(library.model_dump(mode="json"))
    features = candidate.feature_mapping()
    required = {item.value for item in validated.required_feature_registry.feature_ids}
    available = {key for key, value in features.items() if value is not None}
    missing = tuple(sorted(required - available))
    if missing:
        raise V43IntegrationError(
            f"candidate required-feature coverage is below 1.0: {missing}"
        )
    by_observation = _validate_response_inventory(validated, responses)
    raw_observations = tuple(
        _evaluate_rule(rule, by_observation[rule.observation_id], features)
        for rule in sorted(validated.rules, key=lambda item: item.observation_id)
    )
    observations = _merge_structural_dependency_components(raw_observations)
    return V43ScoringInput(
        candidate_context=candidate,
        observations=observations,
        core_blocks=_derive_core_blocks(observations),
    )


def mapping_prevalence_parent_hierarchy_sha256(library: MappingLibraryV2) -> str:
    pathways = _unique_prevalence_pathways(library)
    return sha256_json(
        [
            {
                "anchor_id": pathway.anchor_id,
                "parent_hierarchy": [
                    level.model_dump(mode="json")
                    for level in pathway.prevalence_parent_hierarchy
                ],
            }
            for pathway in pathways
        ]
    )


def mapping_prevalence_plan_sha256(library: MappingLibraryV2) -> str:
    """Hash the exact mapping-derived predicate/parent plan expected of prevalence."""

    pathways = _unique_prevalence_pathways(library)
    return sha256_json(
        {
            "mapping_library_sha256": library.sha256(),
            "required_feature_registry_sha256": (
                library.required_feature_registry_sha256
            ),
            "anchors": [
                {
                    "anchor_id": pathway.anchor_id,
                    "predicate": pathway.predicate.model_dump(mode="json"),
                    "parent_hierarchy": [
                        level.model_dump(mode="json")
                        for level in pathway.prevalence_parent_hierarchy
                    ],
                    "required_feature_ids": [
                        item.value for item in pathway.required_feature_ids
                    ],
                }
                for pathway in pathways
            ],
        }
    )


def _verify_canonical_artifact_bindings(
    *,
    library: MappingLibraryV2,
    cache: VerifiedCenturyCache,
    trust_lock: CenturyCacheTrustLockV1,
    trust_lock_sha256: str,
    prevalence: ConditionalPrevalenceProvider,
) -> CanonicalV43Bindings:
    manifest = cache.manifest
    provenance = prevalence.provenance
    question_bank_sha256 = _question_bank_sha256(library)
    mapping_hash = library.sha256()
    hierarchy_hash = mapping_prevalence_parent_hierarchy_sha256(library)
    mapping_plan_hash = mapping_prevalence_plan_sha256(library)
    required_anchor_ids = tuple(
        pathway.anchor_id for pathway in _unique_prevalence_pathways(library)
    )
    if tuple(provenance.anchor_ids) != required_anchor_ids:
        raise V43IntegrationError("prevalence plan anchor inventory differs from mapping")
    expected: dict[str, tuple[object, object]] = {
        "mapping library": (provenance.mapping_library_sha256, mapping_hash),
        "mapping source library": (
            provenance.mapping_source_library_sha256,
            library.source_library_sha256,
        ),
        "mapping required-feature registry": (
            provenance.required_feature_registry_sha256,
            library.required_feature_registry_sha256,
        ),
        "mapping-derived prevalence plan": (
            provenance.mapping_prevalence_plan_sha256,
            mapping_plan_hash,
        ),
        "prevalence parent hierarchy": (
            provenance.parent_hierarchy_sha256,
            hierarchy_hash,
        ),
        "cache manifest": (provenance.cache_manifest_sha256, cache.manifest_sha256),
        "cache trust lock": (provenance.cache_trust_lock_sha256, trust_lock_sha256),
        "cache build plan": (
            provenance.cache_build_plan_sha256,
            manifest.build_plan_sha256,
        ),
        "logical universe": (
            provenance.universe_sha256,
            manifest.logical_universe_sha256,
        ),
        "semantic registry": (
            provenance.semantic_feature_registry_sha256,
            manifest.semantic_feature_registry_sha256,
        ),
        "physical registry": (
            provenance.physical_feature_registry_sha256,
            manifest.feature_registry_sha256,
        ),
        "reconciliation": (
            provenance.reconciliation_aggregate_sha256,
            manifest.reconciliation_aggregate_sha256,
        ),
        "engine validation": (
            provenance.engine_validation_sha256,
            manifest.engine.engine_validation_sha256,
        ),
        "ephemeris file set": (
            provenance.ephemeris_file_set_sha256,
            manifest.engine.ephemeris_provenance.ephemeris_file_set_sha256,
        ),
        "boundary policy": (
            provenance.boundary_policy_version,
            manifest.boundary_policy_version,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise V43IntegrationError(f"{label} identity mismatch")
    if trust_lock.build_spec_sha256 != sha256_json(
        trust_lock.build_spec.model_dump(mode="json")
    ):
        raise V43IntegrationError("trust-lock build spec identity mismatch")
    for label, value in (
        ("prevalence artifact", provenance.artifact_sha256),
        ("prevalence plan", provenance.plan_sha256),
    ):
        _require_sha256(label, value)
    if provenance.duration_weighted is not True:
        raise V43IntegrationError("prevalence is not duration weighted")
    if provenance.conditional is not True:
        raise V43IntegrationError("conditional prevalence is not active")
    if provenance.exact_stable_intervals is not True:
        raise V43IntegrationError("prevalence is not based on exact stable intervals")
    if provenance.source_scope != GLOBAL_PREVALENCE_SOURCE_SCOPE:
        raise V43IntegrationError("candidate-pool prevalence is forbidden")
    return CanonicalV43Bindings(
        mapping_library_sha256=mapping_hash,
        mapping_source_library_sha256=library.source_library_sha256,
        required_feature_registry_sha256=library.required_feature_registry_sha256,
        mapping_prevalence_plan_sha256=mapping_plan_hash,
        question_bank_sha256=question_bank_sha256,
        prevalence_artifact_sha256=provenance.artifact_sha256,
        prevalence_plan_sha256=provenance.plan_sha256,
        prevalence_parent_hierarchy_sha256=hierarchy_hash,
        cache_manifest_sha256=cache.manifest_sha256,
        cache_trust_lock_sha256=trust_lock_sha256,
        logical_universe_sha256=manifest.logical_universe_sha256,
    )


def _question_bank_sha256(library: MappingLibraryV2) -> str:
    source_id = library.question_bank_source_id
    if source_id is None:
        raise V43IntegrationError("canonical V4.3 requires a bound question-bank source")
    try:
        return next(item.sha256 for item in library.source_artifacts if item.source_id == source_id)
    except StopIteration as exc:  # pragma: no cover - MappingLibraryV2 validates this
        raise V43IntegrationError("question-bank source binding is missing") from exc


def _validate_response_inventory(
    library: MappingLibraryV2,
    responses: tuple[V43ObservedResponse, ...],
) -> dict[str, str]:
    by_observation = {item.observation_id: item.response_token for item in responses}
    if len(by_observation) != len(responses):
        raise V43IntegrationError("response observations must be unique")
    required = {item.observation_id for item in library.rules}
    if set(by_observation) != required:
        raise V43IntegrationError(
            "responses must explicitly cover every frozen scoreable observation"
        )
    return by_observation


def _evaluate_rule(
    rule: CompiledMappingRuleV2,
    response_token: str,
    features: dict[str, JsonValue],
) -> ObservationEvaluation:
    response_rule = rule.response_rule
    support_tokens = set(response_rule.support_response_tokens)
    unknown_tokens = set(response_rule.unknown_response_tokens)
    contradiction_tokens = set(response_rule.contradiction.opposing_response_tokens)
    if response_token in support_tokens | contradiction_tokens:
        disposition = ResponseDisposition.SCORABLE
    elif response_token in unknown_tokens:
        disposition = ResponseDisposition.UNKNOWN
    else:
        raise V43IntegrationError(
            f"unrecognized response token for {rule.observation_id}: {response_token}"
        )
    confidence = ObservationConfidence(
        behavioral_confidence=rule.behavioral_confidence,
        measurement_reliability=rule.measurement_reliability,
        disposition=disposition,
    )
    main_pathways = (rule.primary_pathway, *rule.alternative_pathways)
    corroborator_source = (
        rule.corroborating_pathway.pathway
        if rule.corroborating_pathway is not None
        else None
    )
    pathways = tuple(
        _evaluate_pathway(
            pathway,
            corroborator_source,
            response_token=response_token,
            support_tokens=support_tokens,
            contradiction_tokens=contradiction_tokens,
            contradiction_mode=response_rule.contradiction.mode,
            contradiction_severity=float(response_rule.contradiction.severity.value),
            disposition=disposition,
            features=features,
        )
        for pathway in main_pathways
    )
    return ObservationEvaluation(
        observation_id=rule.observation_id,
        dependency_cluster=rule.dependency_cluster,
        confidence=confidence,
        pathways=pathways,
    )


def _evaluate_pathway(
    pathway: CompiledPathwayV2,
    corroborator: CompiledPathwayV2 | None,
    *,
    response_token: str,
    support_tokens: set[str],
    contradiction_tokens: set[str],
    contradiction_mode: ContradictionModeV2,
    contradiction_severity: float,
    disposition: ResponseDisposition,
    features: dict[str, JsonValue],
) -> EvaluatedPathway:
    primary_matches = _predicate_matches(pathway.predicate, features)
    primary = _evaluate_anchor(
        pathway,
        supports=(
            disposition.is_scorable
            and response_token in support_tokens
            and primary_matches
        ),
        features=features,
    )
    evaluated_corroborator = None
    if corroborator is not None:
        corr_matches = _predicate_matches(corroborator.predicate, features)
        evaluated_corroborator = _evaluate_anchor(
            corroborator,
            supports=(
                disposition.is_scorable
                and response_token in support_tokens
                and corr_matches
            ),
            features=features,
        )
    contradiction = EvaluatedContradiction(
        opposes_response=(
            disposition.is_scorable
            and contradiction_mode is ContradictionModeV2.DIRECT_OPPOSITION
            and response_token in contradiction_tokens
            and primary_matches
        ),
        severity=contradiction_severity,
    )
    return EvaluatedPathway(
        pathway_id=pathway.pathway_id,
        primary=primary,
        corroborator=evaluated_corroborator,
        contradiction=contradiction,
    )


def _evaluate_anchor(
    pathway: CompiledPathwayV2,
    *,
    supports: bool,
    features: dict[str, JsonValue],
) -> EvaluatedStructuralAnchor:
    structural_class = _STRUCTURAL_CLASS_ADAPTER[pathway.structural_class]
    directness_class = _DIRECTNESS_CLASS_ADAPTER[pathway.directness_class]
    flexibility_class = _FLEXIBILITY_CLASS_ADAPTER[pathway.flexibility_class]
    keys = _resolved_dependency_keys(pathway.predicate, features)
    return EvaluatedStructuralAnchor(
        anchor_id=pathway.anchor_id,
        mechanism_keys=tuple(sorted(keys)),
        supports_response=supports,
        structural_class=structural_class,
        structural_salience=pathway.structural_salience,
        directness_class=directness_class,
        directness_factor=pathway.mapping_directness,
        flexibility_class=flexibility_class,
        flexibility_factor=pathway.flexibility_factor,
    )


def _predicate_matches(
    predicate: StructuralPredicateV2,
    features: dict[str, JsonValue],
) -> bool:
    try:
        raw = features[predicate.feature_id.value]
    except KeyError as exc:
        raise V43IntegrationError(
            f"candidate lacks predicate feature {predicate.feature_id.value}"
        ) from exc
    operator = predicate.operator
    if operator is PredicateOperatorV2.PROFILE_HAS_LINE:
        value = _require_string(predicate.feature_id, raw)
        return predicate.values[0] in value.split("/")
    if operator is PredicateOperatorV2.MATCHES_ACTIVATION:
        activations = _activation_records(predicate.feature_id, features)
        return any(_activation_matches(item, predicate) for item in activations)
    if operator is PredicateOperatorV2.HAS_GATE:
        return _has_gate(predicate, raw, features)
    if operator is PredicateOperatorV2.EQUALS_ANY:
        value = _require_string(predicate.feature_id, raw)
        return value in predicate.values
    members = _collection_members(predicate.feature_id, raw)
    matched = bool(set(predicate.values) & members)
    if operator is PredicateOperatorV2.CONTAINS_ANY:
        return matched
    if operator is PredicateOperatorV2.NOT_CONTAINS_ANY:
        return not matched
    raise V43IntegrationError(f"unsupported predicate operator: {operator.value}")


def _collection_members(feature_id: FeatureId, raw: JsonValue) -> set[str]:
    if feature_id is FeatureId.CENTERS:
        record = _require_record(feature_id, raw)
        return set(_string_sequence(feature_id, record.get("defined")))
    if feature_id is FeatureId.COMPLETE_CHANNELS:
        return _record_field_members(feature_id, raw, "channel", str)
    if feature_id in {FeatureId.ACTIVE_GATES, FeatureId.REPEATED_GATES}:
        return _record_field_members(feature_id, raw, "gate", int)
    if feature_id in {FeatureId.HANGING_GATES, FeatureId.DORMANT_GATES}:
        return {str(item) for item in _integer_sequence(feature_id, raw)}
    if feature_id is FeatureId.CIRCUITRY_CHANNEL_METADATA:
        return _record_field_members(feature_id, raw, "channel", str)
    raise V43IntegrationError(
        f"contains predicate is ambiguous for feature {feature_id.value}"
    )


def _record_field_members(
    feature_id: FeatureId,
    raw: JsonValue,
    field: str,
    expected_type: type[str] | type[int],
) -> set[str]:
    values: set[str] = set()
    for item in _record_sequence(feature_id, raw):
        value = item.get(field)
        if expected_type is int:
            if isinstance(value, bool) or not isinstance(value, int):
                raise V43IntegrationError(f"{feature_id.value}.{field} must be an integer")
        elif not isinstance(value, str):
            raise V43IntegrationError(f"{feature_id.value}.{field} must be a string")
        values.add(str(value))
    return values


def _has_gate(
    predicate: StructuralPredicateV2,
    raw: JsonValue,
    features: dict[str, JsonValue],
) -> bool:
    assert predicate.gate is not None
    if predicate.feature_id in {FeatureId.HANGING_GATES, FeatureId.DORMANT_GATES}:
        if predicate.gate not in _integer_sequence(predicate.feature_id, raw):
            return False
        if predicate.side is None:
            return True
        active = _record_sequence(
            FeatureId.ACTIVE_GATES,
            features[FeatureId.ACTIVE_GATES.value],
        )
        return any(
            item.get("gate") == predicate.gate
            and any(
                isinstance(position, str) and position.startswith(f"{predicate.side}:")
                for position in cast(list[object], item.get("activation_positions", []))
            )
            for item in active
        )
    if predicate.feature_id is FeatureId.POSSIBLE_BRIDGES:
        return any(
            item.get("missing_gate") == predicate.gate
            for item in _record_sequence(predicate.feature_id, raw)
        )
    records = _activation_records(predicate.feature_id, features)
    if predicate.feature_id in {FeatureId.ACTIVE_GATES, FeatureId.REPEATED_GATES}:
        for item in records:
            if item.get("gate") != predicate.gate:
                continue
            count = item.get("activation_count")
            if isinstance(count, bool) or not isinstance(count, int):
                raise V43IntegrationError("activation_count must be an integer")
            return predicate.minimum_occurrences is None or count >= predicate.minimum_occurrences
        return False
    return any(_activation_matches(item, predicate) for item in records)


def _activation_records(
    feature_id: FeatureId,
    features: dict[str, JsonValue],
) -> tuple[dict[str, JsonValue], ...]:
    projected = {
        FeatureId.ACTIVATION_SIDE,
        FeatureId.ACTIVATION_CARRIER,
        FeatureId.ACTIVATION_GATE,
        FeatureId.ACTIVATION_LINE,
        FeatureId.COLOR,
        FeatureId.TONE,
        FeatureId.BASE,
    }
    source_id = FeatureId.PLANETARY_ACTIVATIONS if feature_id in projected else feature_id
    return _record_sequence(source_id, features[source_id.value])


def _activation_matches(
    record: dict[str, JsonValue], predicate: StructuralPredicateV2
) -> bool:
    checks = (
        ("side", predicate.side),
        ("body", predicate.carrier.value if predicate.carrier is not None else None),
        ("gate", predicate.gate),
        ("line", predicate.line),
    )
    return all(expected is None or record.get(field) == expected for field, expected in checks)


def _resolved_dependency_keys(
    predicate: StructuralPredicateV2,
    features: dict[str, JsonValue],
) -> frozenset[str]:
    keys = set(predicate.dependency_keys)
    if predicate.feature_id in {FeatureId.CROSS_NAME, FeatureId.CROSS_COMPONENTS}:
        raw = features.get(FeatureId.CROSS_COMPONENTS.value)
        if not isinstance(raw, str):
            raise V43IntegrationError("Cross predicates require exact cardinal components")
        gates = _parse_cross_components(raw)
        keys.add(f"cross:{raw}")
        for position, gate in zip(_CARDINAL_POSITIONS, gates, strict=True):
            keys.update({f"gate:{gate}", f"cardinal:{position}:{gate}"})
    return frozenset(keys)


def _parse_cross_components(value: str) -> tuple[int, int, int, int]:
    try:
        parts = tuple(int(item) for axis in value.split("|") for item in axis.split("/"))
    except ValueError as exc:
        raise V43IntegrationError("invalid Cross component value") from exc
    if len(parts) != 4 or any(not 1 <= item <= 64 for item in parts):
        raise V43IntegrationError("invalid Cross component value")
    return parts


def _derive_core_blocks(
    observations: tuple[ObservationEvaluation, ...],
) -> tuple[CoreBlockEvaluation, ...]:
    by_block: dict[CoreBlock, dict[str, tuple[float, float]]] = defaultdict(dict)
    for observation in observations:
        ceff = observation.confidence.effective_confidence
        for block in CoreBlock:
            directness = max(
                (
                    pathway.primary.directness_factor
                    for pathway in observation.pathways
                    if _CORE_CLASS_TO_BLOCK.get(pathway.primary.structural_class) is block
                    and pathway.primary.supports_response
                ),
                default=0.0,
            )
            if any(
                _CORE_CLASS_TO_BLOCK.get(pathway.primary.structural_class) is block
                for pathway in observation.pathways
            ):
                previous = by_block[block].get(observation.dependency_cluster, (0.0, 0.0))
                by_block[block][observation.dependency_cluster] = (
                    max(previous[0], directness),
                    max(previous[1], ceff),
                )
    evaluations: list[CoreBlockEvaluation] = []
    for block in CoreBlock:
        clusters = by_block.get(block, {})
        denominator = sum(confidence for _, confidence in clusters.values())
        if denominator == 0.0:
            evaluations.append(
                CoreBlockEvaluation(
                    block=block,
                    availability=CoreBlockAvailability.UNREPORTABLE,
                    earned_fraction=None,
                )
            )
            continue
        numerator = sum(support * confidence for support, confidence in clusters.values())
        evaluations.append(
            CoreBlockEvaluation(
                block=block,
                availability=CoreBlockAvailability.REPORTABLE,
                earned_fraction=numerator / denominator,
            )
        )
    return tuple(evaluations)


def _merge_structural_dependency_components(
    observations: tuple[ObservationEvaluation, ...],
) -> tuple[ObservationEvaluation, ...]:
    """Union frozen behavioral clusters that reuse one exact chart mechanism.

    Mapping authors retain their declared behavioral cluster labels.  The runtime
    adds the stricter structural dependency relation so a Channel/component Gate,
    Cross/cardinal, or repeated exact anchor can never survive as two independent
    scoring contributions merely because the source used two cluster names.
    """

    parent = list(range(len(observations)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    owner_by_declared_cluster: dict[str, int] = {}
    owner_by_mechanism: dict[str, int] = {}
    for index, observation in enumerate(observations):
        previous_cluster = owner_by_declared_cluster.setdefault(
            observation.dependency_cluster,
            index,
        )
        union(index, previous_cluster)
        keys = {
            key
            for pathway in observation.pathways
            for anchor in (
                pathway.primary,
                *((pathway.corroborator,) if pathway.corroborator is not None else ()),
            )
            for key in anchor.dependency_keys
        }
        for key in sorted(keys):
            previous_owner = owner_by_mechanism.setdefault(key, index)
            union(index, previous_owner)

    members_by_root: dict[int, list[int]] = defaultdict(list)
    for index in range(len(observations)):
        members_by_root[find(index)].append(index)
    component_id_by_index: dict[int, str] = {}
    for indexes in members_by_root.values():
        declared = tuple(
            sorted({observations[index].dependency_cluster for index in indexes})
        )
        component_id = (
            declared[0]
            if len(declared) == 1
            else f"structural-dependency:{sha256_json(list(declared))}"
        )
        for index in indexes:
            component_id_by_index[index] = component_id
    return tuple(
        replace(
            observation,
            dependency_cluster=component_id_by_index[index],
        )
        for index, observation in enumerate(observations)
    )


def _verify_record_cache_bindings(
    record: CenturyStateRecord, cache: VerifiedCenturyCache
) -> None:
    manifest = cache.manifest
    expected: dict[str, tuple[object, object]] = {
        "feature-vector schema": (
            record.feature_vector_schema_version,
            manifest.feature_vector_schema_version,
        ),
        "semantic registry": (
            record.semantic_feature_registry_sha256,
            manifest.semantic_feature_registry_sha256,
        ),
        "physical registry": (
            record.feature_registry_sha256,
            manifest.feature_registry_sha256,
        ),
        "chart engine": (record.astronomy_engine_version, manifest.engine.chart_engine_version),
        "ephemeris file set": (
            record.ephemeris_file_set_sha256,
            manifest.engine.ephemeris_provenance.ephemeris_file_set_sha256,
        ),
        "node convention": (record.node_convention, manifest.node_convention),
        "Mandala mapping": (record.mandala_mapping_sha256, manifest.mandala_mapping_sha256),
        "Bodygraph mapping": (
            record.bodygraph_mapping_sha256,
            manifest.bodygraph_mapping_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise V43IntegrationError(f"candidate/cache {label} mismatch")
    if not manifest.utc_start <= record.utc_start < record.utc_end <= manifest.utc_end_exclusive:
        raise V43IntegrationError("candidate interval lies outside the declared cache universe")
    physical_ids = tuple(item.feature_id for item in manifest.feature_registry)
    if tuple(record.feature_mapping()) != physical_ids:
        raise V43IntegrationError("candidate physical feature inventory differs from cache")


def _verify_candidate_binding(
    binding: ConditionalPrevalenceCandidateBindingLike,
    *,
    candidate: CenturyStateRecord,
    candidate_record_sha256: str,
    bindings: CanonicalV43Bindings,
) -> None:
    expected = {
        "state ID": (binding.state_id, candidate.state_id),
        "candidate record": (
            binding.candidate_record_sha256,
            candidate_record_sha256,
        ),
        "cache manifest": (
            binding.cache_manifest_sha256,
            bindings.cache_manifest_sha256,
        ),
        "universe": (binding.universe_sha256, bindings.logical_universe_sha256),
        "mapping library": (
            binding.mapping_library_sha256,
            bindings.mapping_library_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise V43IntegrationError(f"prevalence candidate-binding {label} mismatch")


def _require_unchanged(
    cache: VerifiedCenturyCache,
    trust_lock_path: Path,
    trust_lock_sha256: str,
) -> None:
    if sha256_file(trust_lock_path) != trust_lock_sha256:
        raise V43IntegrationError("century-cache trust lock changed after verification")
    if sha256_file(cache.manifest_path) != cache.manifest_sha256:
        raise V43IntegrationError("century-cache manifest changed after verification")


def _exact_duration_microseconds(record: CenturyStateRecord) -> int:
    delta = record.utc_end - record.utc_start
    return delta.days * 86_400_000_000 + delta.seconds * 1_000_000 + delta.microseconds


def _all_rule_pathways(rule: CompiledMappingRuleV2) -> tuple[CompiledPathwayV2, ...]:
    pathways = (rule.primary_pathway, *rule.alternative_pathways)
    if rule.corroborating_pathway is not None:
        pathways = (*pathways, rule.corroborating_pathway.pathway)
    return pathways


def _unique_prevalence_pathways(
    library: MappingLibraryV2,
) -> tuple[CompiledPathwayV2, ...]:
    by_anchor: dict[str, CompiledPathwayV2] = {}
    for rule in library.rules:
        for pathway in _all_rule_pathways(rule):
            by_anchor.setdefault(pathway.anchor_id, pathway)
    return tuple(by_anchor[item] for item in sorted(by_anchor))


def _require_string(feature_id: FeatureId, value: JsonValue) -> str:
    if not isinstance(value, str):
        raise V43IntegrationError(f"{feature_id.value} must be a string")
    return value


def _require_record(
    feature_id: FeatureId, value: JsonValue
) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise V43IntegrationError(f"{feature_id.value} must be an object")
    return value


def _record_sequence(
    feature_id: FeatureId, value: JsonValue
) -> tuple[dict[str, JsonValue], ...]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise V43IntegrationError(f"{feature_id.value} must be a record sequence")
    return tuple(cast(dict[str, JsonValue], item) for item in value)


def _integer_sequence(feature_id: FeatureId, value: JsonValue) -> tuple[int, ...]:
    if not isinstance(value, list) or any(
        isinstance(item, bool) or not isinstance(item, int) for item in value
    ):
        raise V43IntegrationError(f"{feature_id.value} must be an integer sequence")
    return tuple(cast(int, item) for item in value)


def _string_sequence(feature_id: FeatureId, value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise V43IntegrationError(f"{feature_id.value} must be a string sequence")
    return tuple(cast(str, item) for item in value)


def _require_sha256(label: str, value: str) -> None:
    if len(value) != 64 or any(item not in "0123456789abcdef" for item in value):
        raise V43IntegrationError(f"{label} identity is not a lowercase SHA-256")
