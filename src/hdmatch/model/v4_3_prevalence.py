"""Mapping-bound, cache-only conditional prevalence for V4.3.

The public plan/build/verification paths open the exact canonical mapping-v2
source and compiled bytes and the tracked century-cache trust lock. Callers
cannot substitute candidate rows, caller-asserted mapping hashes, or an
unverified plan. Exact cache intervals are streamed and duration weighted.

This module contains no behavioral responses, answer keys, or ranking logic.
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Final, Literal, TypeGuard

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from hdmatch.century_cache.models import (
    FEATURE_ID_PATTERN,
    SHA256_PATTERN,
    CenturyStateRecord,
    FeatureColumnSpec,
    FeatureStorageType,
    VerifiedCenturyCache,
    required_feature_ids_sha256,
)
from hdmatch.century_cache.parquet import CenturyCacheParquetError, validate_row_features
from hdmatch.century_cache.store import (
    CenturyCacheVerificationError,
    iter_verified_century_cache_rows,
    verify_century_cache,
)
from hdmatch.century_cache.trust_lock import (
    CenturyCacheTrustLockV1,
    century_cache_expectations_from_build_spec,
)
from hdmatch.chart.bodygraph import CHANNELS, GATE_TO_CENTER, Center
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.chart.feature_registry import (
    ActivationFeature,
    ActiveGateFeature,
    CompleteChannelFeature,
    FeatureId,
    PossibleBridgeFeature,
)
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.model.v4_3_compiler import compile_verified_mapping_library_v2
from hdmatch.model.v4_3_mapping import (
    CompiledPathwayV2,
    MappingLibrarySourceV2,
    MappingLibraryV2,
    MappingV2Error,
    PredicateOperatorV2,
    PrevalenceParentLevelV2,
    StructuralPredicateV2,
)
from hdmatch.model.v4_3_prevalence_identity import (
    mapping_prevalence_parent_hierarchy_sha256,
    mapping_prevalence_plan_sha256,
)

V43_PREVALENCE_POLICY_VERSION: Final[str] = (
    "v4.3-global-duration-conditional-prevalence-v2"
)
V43_INFORMATION_CAP_RUBRIC_BITS: Final[float] = 6.0
V43_MINIMUM_EFFECTIVE_STATE_EQUIVALENTS: Final[int] = 500
_VERIFIED_PROVIDER_TOKEN: Final[object] = object()
_CACHE_MEMBER_TOKEN: Final[object] = object()


class V43PrevalenceError(ValueError):
    """A V4.3 prevalence input or artifact violates the frozen contract."""


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class V43PrevalenceAnchorV1(_FrozenModel):
    """One exact compiled mapping predicate and its frozen backoff hierarchy."""

    anchor_id: str = Field(pattern=r"^anchor-v2:[a-f0-9]{64}$")
    predicate: StructuralPredicateV2
    parent_hierarchy: tuple[PrevalenceParentLevelV2, ...] = Field(min_length=1)
    required_feature_ids: tuple[FeatureId, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def require_exact_compiled_identity(self) -> V43PrevalenceAnchorV1:
        if self.anchor_id != self.predicate.anchor_id:
            raise ValueError("prevalence anchor ID differs from its exact predicate")
        required = set(self.predicate.required_feature_ids)
        for level in self.parent_hierarchy:
            required.update(level.parent_feature_ids)
        derived = tuple(sorted(required, key=lambda item: item.value))
        if self.required_feature_ids != derived:
            raise ValueError("prevalence anchor required features differ from derivation")
        return self


class V43PrevalencePlanV1(_FrozenModel):
    """Canonical plan derived only from actual mapping and cache artifacts."""

    schema_version: Literal["v4-3-prevalence-plan-v2"] = (
        "v4-3-prevalence-plan-v2"
    )
    model_version: Literal["V4.3"] = "V4.3"
    mapping_library_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_source_library_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_prevalence_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_required_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    expected_cache_semantic_feature_registry_sha256: str = Field(
        pattern=SHA256_PATTERN
    )
    expected_cache_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_ids: tuple[FeatureId, ...] = Field(min_length=1)
    required_feature_ids_sha256: str = Field(pattern=SHA256_PATTERN)
    anchors: tuple[V43PrevalenceAnchorV1, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def require_complete_canonical_inventory(self) -> V43PrevalencePlanV1:
        anchor_ids = tuple(anchor.anchor_id for anchor in self.anchors)
        if anchor_ids != tuple(sorted(set(anchor_ids))):
            raise ValueError("prevalence anchors must be sorted by unique anchor ID")
        derived = tuple(
            sorted(
                {
                    feature_id
                    for anchor in self.anchors
                    for feature_id in anchor.required_feature_ids
                },
                key=lambda item: item.value,
            )
        )
        if self.required_feature_ids != derived:
            raise ValueError("prevalence plan required features differ from anchors")
        string_ids = tuple(item.value for item in derived)
        if self.required_feature_ids_sha256 != required_feature_ids_sha256(string_ids):
            raise ValueError("prevalence plan required-feature hash is inconsistent")
        if self.mapping_prevalence_plan_sha256 != _anchor_inventory_sha256(
            self.anchors,
            mapping_library_sha256=self.mapping_library_sha256,
            required_feature_registry_sha256=(
                self.mapping_required_feature_registry_sha256
            ),
        ):
            raise ValueError("mapping prevalence-plan hash is inconsistent")
        return self

    def sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))

    @property
    def parent_hierarchy_sha256(self) -> str:
        """Bind every predicate as well as every parent/backoff level."""

        return sha256_json(
            [
                {
                    "anchor_id": anchor.anchor_id,
                    "parent_hierarchy": [
                        level.model_dump(mode="json")
                        for level in anchor.parent_hierarchy
                    ],
                }
                for anchor in self.anchors
            ]
        )


class V43ConditionalPrevalencePolicyV1(_FrozenModel):
    """Frozen V4.3 denominator, backoff, and information-cap rules."""

    schema_version: Literal["v4-3-conditional-prevalence-policy-v2"] = (
        "v4-3-conditional-prevalence-policy-v2"
    )
    policy_version: Literal[
        "v4.3-global-duration-conditional-prevalence-v2"
    ] = "v4.3-global-duration-conditional-prevalence-v2"
    source_scope: Literal["declared-global-utc-universe"] = (
        "declared-global-utc-universe"
    )
    duration_weighting: Literal["exact-stable-interval-microseconds"] = (
        "exact-stable-interval-microseconds"
    )
    candidate_file_frequencies_forbidden: Literal[True] = True
    minimum_effective_state_equivalents: Literal[500] = 500
    state_equivalent_duration_policy: Literal[
        "global-duration-divided-by-exact-interval-count"
    ] = "global-duration-divided-by-exact-interval-count"
    backoff_policy: Literal[
        "first-sufficient-cell-then-strict-next-level-terminal-root"
    ] = "first-sufficient-cell-then-strict-next-level-terminal-root"
    terminal_root_policy: Literal["select-nonempty-root-even-if-below-minimum"] = (
        "select-nonempty-root-even-if-below-minimum"
    )
    zero_prevalence_policy: Literal["fail-closed"] = "fail-closed"
    information_cap_rubric_bits: float = V43_INFORMATION_CAP_RUBRIC_BITS

    @model_validator(mode="after")
    def require_information_cap(self) -> V43ConditionalPrevalencePolicyV1:
        if self.information_cap_rubric_bits != V43_INFORMATION_CAP_RUBRIC_BITS:
            raise ValueError("V4.3 information cap is frozen at six rubric bits")
        return self

    def sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


class V43PrevalenceSourceV1(_FrozenModel):
    schema_version: Literal["v4-3-prevalence-source-v2"] = (
        "v4-3-prevalence-source-v2"
    )
    cache_locator: str = Field(min_length=1)
    cache_version: Literal["century-cache-v1"] = "century-cache-v1"
    cache_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_trust_lock_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_build_spec_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    reconciliation_aggregate_sha256: str = Field(pattern=SHA256_PATTERN)
    exact_state_provenance_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_vector_schema_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
    engine_validation_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_source_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_file_set_sha256: str = Field(pattern=SHA256_PATTERN)
    boundary_policy_version: str = Field(min_length=1)
    generation_commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    utc_start: str = Field(min_length=1)
    utc_end_exclusive: str = Field(min_length=1)
    interval_count: int = Field(gt=0)
    total_duration_microseconds: int = Field(gt=0)
    minimum_cell_duration_numerator: int = Field(gt=0)
    minimum_cell_duration_denominator: int = Field(gt=0)
    mapping_library_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_source_library_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_prevalence_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_minimum_cell_ratio(self) -> V43PrevalenceSourceV1:
        if self.minimum_cell_duration_numerator != (
            self.total_duration_microseconds
            * V43_MINIMUM_EFFECTIVE_STATE_EQUIVALENTS
        ):
            raise ValueError("minimum-cell duration numerator is inconsistent")
        if self.minimum_cell_duration_denominator != self.interval_count:
            raise ValueError("minimum-cell duration denominator is inconsistent")
        return self


class V43ParentValueV1(_FrozenModel):
    feature_id: str = Field(pattern=FEATURE_ID_PATTERN)
    value: JsonValue

    @model_validator(mode="after")
    def reject_unknown_parent(self) -> V43ParentValueV1:
        if self.value is None:
            raise ValueError("prevalence parent values cannot be unknown/null")
        return self


class V43PrevalenceCellV1(_FrozenModel):
    level_id: str
    backoff_ordinal: int = Field(ge=0)
    parent_values: tuple[V43ParentValueV1, ...]
    parent_values_sha256: str = Field(pattern=SHA256_PATTERN)
    numerator_duration_microseconds: int = Field(ge=0)
    denominator_duration_microseconds: int = Field(gt=0)
    minimum_effective_size_met: bool

    @model_validator(mode="after")
    def require_cell_arithmetic(self) -> V43PrevalenceCellV1:
        if self.numerator_duration_microseconds > self.denominator_duration_microseconds:
            raise ValueError("prevalence numerator exceeds denominator")
        feature_ids = tuple(item.feature_id for item in self.parent_values)
        if feature_ids != tuple(sorted(set(feature_ids))):
            raise ValueError("prevalence cell parent values must be sorted and unique")
        if self.parent_values_sha256 != _parent_values_sha256(self.parent_values):
            raise ValueError("prevalence cell parent-value hash is inconsistent")
        return self


class V43AnchorPrevalenceTableV1(_FrozenModel):
    anchor_id: str = Field(pattern=r"^anchor-v2:[a-f0-9]{64}$")
    cells: tuple[V43PrevalenceCellV1, ...] = Field(min_length=1)


class V43ConditionalPrevalenceArtifactV1(_FrozenModel):
    """Versioned duration tables for one exact lock-verified global universe."""

    schema_version: Literal["v4-3-conditional-prevalence-artifact-v2"] = (
        "v4-3-conditional-prevalence-artifact-v2"
    )
    model_version: Literal["V4.3"] = "V4.3"
    source: V43PrevalenceSourceV1
    policy: V43ConditionalPrevalencePolicyV1
    policy_sha256: str = Field(pattern=SHA256_PATTERN)
    plan: V43PrevalencePlanV1
    plan_sha256: str = Field(pattern=SHA256_PATTERN)
    parent_hierarchy_sha256: str = Field(pattern=SHA256_PATTERN)
    tables: tuple[V43AnchorPrevalenceTableV1, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def require_complete_tables(self) -> V43ConditionalPrevalenceArtifactV1:
        if self.policy_sha256 != self.policy.sha256():
            raise ValueError("prevalence policy hash is inconsistent")
        if self.plan_sha256 != self.plan.sha256():
            raise ValueError("prevalence plan hash is inconsistent")
        if self.parent_hierarchy_sha256 != self.plan.parent_hierarchy_sha256:
            raise ValueError("prevalence parent-hierarchy hash is inconsistent")
        bindings = {
            "semantic feature registry": (
                self.source.semantic_feature_registry_sha256,
                self.plan.expected_cache_semantic_feature_registry_sha256,
            ),
            "physical feature registry": (
                self.source.feature_registry_sha256,
                self.plan.expected_cache_feature_registry_sha256,
            ),
            "mapping library": (
                self.source.mapping_library_sha256,
                self.plan.mapping_library_sha256,
            ),
            "mapping source library": (
                self.source.mapping_source_library_sha256,
                self.plan.mapping_source_library_sha256,
            ),
            "mapping prevalence plan": (
                self.source.mapping_prevalence_plan_sha256,
                self.plan.mapping_prevalence_plan_sha256,
            ),
            "mapping required registry": (
                self.source.required_feature_registry_sha256,
                self.plan.mapping_required_feature_registry_sha256,
            ),
        }
        for label, (actual, expected) in bindings.items():
            if actual != expected:
                raise ValueError(f"prevalence source/plan {label} mismatch")
        table_ids = tuple(table.anchor_id for table in self.tables)
        expected_ids = tuple(anchor.anchor_id for anchor in self.plan.anchors)
        if table_ids != expected_ids:
            raise ValueError("prevalence tables differ from the frozen anchor inventory")
        for anchor, table in zip(self.plan.anchors, self.tables, strict=True):
            self._validate_anchor_table(anchor, table)
        return self

    def _validate_anchor_table(
        self,
        anchor: V43PrevalenceAnchorV1,
        table: V43AnchorPrevalenceTableV1,
    ) -> None:
        ordering = tuple(
            (cell.backoff_ordinal, cell.parent_values_sha256) for cell in table.cells
        )
        if ordering != tuple(sorted(ordering)) or len(ordering) != len(set(ordering)):
            raise ValueError(f"prevalence cells are not canonical for {anchor.anchor_id}")
        expected_ordinals = set(range(len(anchor.parent_hierarchy)))
        if {cell.backoff_ordinal for cell in table.cells} != expected_ordinals:
            raise ValueError(f"prevalence table skips a backoff level for {anchor.anchor_id}")
        numerators: set[int] = set()
        for ordinal, level in enumerate(anchor.parent_hierarchy):
            cells = tuple(
                cell for cell in table.cells if cell.backoff_ordinal == ordinal
            )
            if not cells:
                raise ValueError(f"prevalence level has no cells for {anchor.anchor_id}")
            if any(cell.level_id != level.level_id for cell in cells):
                raise ValueError(f"prevalence level ID differs from plan for {anchor.anchor_id}")
            expected_features = tuple(item.value for item in level.parent_feature_ids)
            if any(
                tuple(item.feature_id for item in cell.parent_values)
                != expected_features
                for cell in cells
            ):
                raise ValueError(f"prevalence cell parents differ from plan for {anchor.anchor_id}")
            if sum(cell.denominator_duration_microseconds for cell in cells) != (
                self.source.total_duration_microseconds
            ):
                raise ValueError(
                    "prevalence denominators do not cover universe for "
                    f"{anchor.anchor_id}"
                )
            numerators.add(
                sum(cell.numerator_duration_microseconds for cell in cells)
            )
            for cell in cells:
                expected_minimum = (
                    cell.denominator_duration_microseconds
                    * self.source.minimum_cell_duration_denominator
                    >= self.source.minimum_cell_duration_numerator
                )
                if cell.minimum_effective_size_met != expected_minimum:
                    raise ValueError(
                        "prevalence minimum-cell decision is inconsistent for "
                        f"{anchor.anchor_id}"
                    )
        if len(numerators) != 1:
            raise ValueError(
                "prevalence anchor numerator changes across levels: "
                f"{anchor.anchor_id}"
            )
        root_cells = tuple(
            cell
            for cell in table.cells
            if cell.backoff_ordinal == len(anchor.parent_hierarchy) - 1
        )
        if len(root_cells) != 1 or root_cells[0].parent_values:
            raise ValueError(f"prevalence terminal root is not unique for {anchor.anchor_id}")

    def sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


@dataclass(frozen=True, slots=True)
class V43PrevalenceAttempt:
    level_id: str
    backoff_ordinal: int
    denominator_duration_microseconds: int
    minimum_effective_size_met: bool


@dataclass(frozen=True, slots=True)
class V43PrevalenceEstimate:
    anchor_id: str
    prevalence: float
    numerator_duration_microseconds: int
    denominator_duration_microseconds: int
    universe_sha256: str
    policy_version: str
    parent_hierarchy_sha256: str
    selected_level_id: str
    backoff_ordinal: int
    duration_weighted: Literal[True]
    conditional: Literal[True]
    selected_level_conditional: bool
    exact_stable_intervals: Literal[True]
    source_scope: Literal["declared-global-utc-universe"]
    information_rubric_bits: float
    attempts: tuple[V43PrevalenceAttempt, ...]
    artifact_sha256: str
    plan_sha256: str
    mapping_library_sha256: str
    mapping_source_library_sha256: str
    mapping_prevalence_plan_sha256: str
    required_feature_registry_sha256: str
    cache_manifest_sha256: str


@dataclass(frozen=True, slots=True)
class V43PrevalenceProvenance:
    anchor_ids: tuple[str, ...]
    artifact_sha256: str
    plan_sha256: str
    mapping_library_sha256: str
    mapping_source_library_sha256: str
    mapping_prevalence_plan_sha256: str
    required_feature_registry_sha256: str
    cache_manifest_sha256: str
    cache_trust_lock_sha256: str
    cache_build_plan_sha256: str
    semantic_feature_registry_sha256: str
    physical_feature_registry_sha256: str
    reconciliation_aggregate_sha256: str
    engine_validation_sha256: str
    ephemeris_file_set_sha256: str
    boundary_policy_version: str
    universe_sha256: str
    policy_version: str
    parent_hierarchy_sha256: str
    duration_weighted: Literal[True]
    conditional: Literal[True]
    exact_stable_intervals: Literal[True]
    source_scope: Literal["declared-global-utc-universe"]


class _VerifiedCacheMember:
    __slots__ = (
        "_provider_token",
        "_record",
        "cache_manifest_sha256",
        "candidate_record_sha256",
        "mapping_library_sha256",
        "state_id",
        "universe_sha256",
    )

    def __init__(
        self,
        *,
        record: CenturyStateRecord,
        cache_manifest_sha256: str,
        universe_sha256: str,
        mapping_library_sha256: str,
        provider_token: object,
        _token: object,
    ) -> None:
        if _token is not _CACHE_MEMBER_TOKEN:
            raise V43PrevalenceError(
                "cache members must be minted by a replay-verified provider"
            )
        self._record = record
        self._provider_token = provider_token
        self.state_id = record.state_id
        self.candidate_record_sha256 = sha256_json(record.model_dump(mode="json"))
        self.cache_manifest_sha256 = cache_manifest_sha256
        self.universe_sha256 = universe_sha256
        self.mapping_library_sha256 = mapping_library_sha256


class V43BoundCandidateRecord:
    """Opaque candidate capability bound to one provider/cache/mapping identity."""

    __slots__ = (
        "_provider_token",
        "_record",
        "cache_manifest_sha256",
        "candidate_record_sha256",
        "mapping_library_sha256",
        "state_id",
        "universe_sha256",
    )

    def __init__(self, member: _VerifiedCacheMember, *, _token: object) -> None:
        if _token is not _CACHE_MEMBER_TOKEN:
            raise V43PrevalenceError(
                "bound candidates must be minted by a replay-verified provider"
            )
        self._record = member._record
        self._provider_token = member._provider_token
        self.state_id = member.state_id
        self.candidate_record_sha256 = member.candidate_record_sha256
        self.cache_manifest_sha256 = member.cache_manifest_sha256
        self.universe_sha256 = member.universe_sha256
        self.mapping_library_sha256 = member.mapping_library_sha256


@dataclass(frozen=True, slots=True)
class _MappingBinding:
    library: MappingLibraryV2
    source: MappingLibrarySourceV2
    library_sha256: str
    source_sha256: str
    library_path: Path
    source_path: Path
    library_bytes: bytes
    source_bytes: bytes


@dataclass(frozen=True, slots=True)
class _VerifiedCacheSnapshot:
    verified: VerifiedCenturyCache
    lock: CenturyCacheTrustLockV1
    lock_sha256: str
    lock_path: Path
    lock_bytes: bytes


class VerifiedV43ConditionalPrevalence:
    """Factory-verified provider consumed by the V4.3 scorer."""

    __slots__ = (
        "_artifact",
        "_artifact_sha256",
        "_cache",
        "_cell_index",
        "_membership_iterator",
        "_pending_membership",
        "_provider_token",
        "_token",
    )

    def __init__(
        self,
        *,
        artifact: V43ConditionalPrevalenceArtifactV1,
        artifact_sha256: str,
        cache: VerifiedCenturyCache,
        _token: object,
    ) -> None:
        if _token is not _VERIFIED_PROVIDER_TOKEN:
            raise V43PrevalenceError(
                "verified prevalence providers require cache replay verification"
            )
        self._artifact = artifact
        self._artifact_sha256 = artifact_sha256
        self._cache = cache
        self._cell_index = {
            (table.anchor_id, cell.backoff_ordinal, cell.parent_values_sha256): cell
            for table in artifact.tables
            for cell in table.cells
        }
        self._membership_iterator = iter_verified_century_cache_rows(cache)
        self._pending_membership: CenturyStateRecord | None = None
        self._provider_token = object()
        self._token = _token

    @property
    def provenance(self) -> V43PrevalenceProvenance:
        source = self._artifact.source
        return V43PrevalenceProvenance(
            anchor_ids=tuple(anchor.anchor_id for anchor in self._artifact.plan.anchors),
            artifact_sha256=self._artifact_sha256,
            plan_sha256=self._artifact.plan_sha256,
            mapping_library_sha256=source.mapping_library_sha256,
            mapping_source_library_sha256=source.mapping_source_library_sha256,
            mapping_prevalence_plan_sha256=source.mapping_prevalence_plan_sha256,
            required_feature_registry_sha256=(
                source.required_feature_registry_sha256
            ),
            cache_manifest_sha256=source.cache_manifest_sha256,
            cache_trust_lock_sha256=source.cache_trust_lock_sha256,
            cache_build_plan_sha256=source.cache_build_plan_sha256,
            semantic_feature_registry_sha256=(
                source.semantic_feature_registry_sha256
            ),
            physical_feature_registry_sha256=source.feature_registry_sha256,
            reconciliation_aggregate_sha256=(
                source.reconciliation_aggregate_sha256
            ),
            engine_validation_sha256=source.engine_validation_sha256,
            ephemeris_file_set_sha256=source.ephemeris_file_set_sha256,
            boundary_policy_version=source.boundary_policy_version,
            universe_sha256=source.logical_universe_sha256,
            policy_version=self._artifact.policy.policy_version,
            parent_hierarchy_sha256=self._artifact.parent_hierarchy_sha256,
            duration_weighted=True,
            conditional=True,
            exact_stable_intervals=True,
            source_scope="declared-global-utc-universe",
        )

    @property
    def artifact(self) -> V43ConditionalPrevalenceArtifactV1:
        return self._artifact

    def iter_cache_members(self) -> Iterator[object]:
        """Yield opaque current-cache members without retaining the universe."""

        source = self._artifact.source
        for record in iter_verified_century_cache_rows(self._cache):
            yield _VerifiedCacheMember(
                record=record,
                cache_manifest_sha256=source.cache_manifest_sha256,
                universe_sha256=source.logical_universe_sha256,
                mapping_library_sha256=source.mapping_library_sha256,
                provider_token=self._provider_token,
                _token=_CACHE_MEMBER_TOKEN,
            )

    def bind_candidate_record(
        self,
        record: object,
        *,
        cache_manifest_sha256: str,
        mapping_library_sha256: str,
    ) -> V43BoundCandidateRecord:
        source = self._artifact.source
        if cache_manifest_sha256 != source.cache_manifest_sha256:
            raise V43PrevalenceError("requested cache manifest mismatch")
        if mapping_library_sha256 != source.mapping_library_sha256:
            raise V43PrevalenceError("requested mapping library mismatch")
        if isinstance(record, _VerifiedCacheMember):
            if record._provider_token is not self._provider_token:
                raise V43PrevalenceError("candidate member belongs to another provider")
            member = record
        elif isinstance(record, CenturyStateRecord):
            member = self._bind_next_verified_cache_row(record)
        else:
            raise V43PrevalenceError(
                "candidate is neither a cache row nor a verified member capability"
            )
        bindings = {
            "member cache manifest": (
                member.cache_manifest_sha256,
                source.cache_manifest_sha256,
            ),
            "member universe": (
                member.universe_sha256,
                source.logical_universe_sha256,
            ),
            "member mapping library": (
                member.mapping_library_sha256,
                source.mapping_library_sha256,
            ),
        }
        for label, (actual, expected) in bindings.items():
            if actual != expected:
                raise V43PrevalenceError(f"{label} mismatch")
        return V43BoundCandidateRecord(member, _token=_CACHE_MEMBER_TOKEN)

    def _bind_next_verified_cache_row(
        self,
        candidate: CenturyStateRecord,
    ) -> _VerifiedCacheMember:
        """Match one candidate against the next replay-verified canonical row.

        This bounded cursor is the ordinary scorer path. It proves ordered cache
        membership without retaining a century-wide set of row hashes. A mismatch
        does not advance the cursor, so a substituted candidate cannot skip a row.
        """

        if self._pending_membership is None:
            try:
                self._pending_membership = next(self._membership_iterator)
            except StopIteration as exc:
                raise V43PrevalenceError(
                    "candidate cache membership stream is exhausted"
                ) from exc
        expected = self._pending_membership
        if candidate != expected:
            raise V43PrevalenceError(
                "candidate differs from the next replay-verified cache member"
            )
        self._pending_membership = None
        source = self._artifact.source
        return _VerifiedCacheMember(
            record=expected,
            cache_manifest_sha256=source.cache_manifest_sha256,
            universe_sha256=source.logical_universe_sha256,
            mapping_library_sha256=source.mapping_library_sha256,
            provider_token=self._provider_token,
            _token=_CACHE_MEMBER_TOKEN,
        )

    def estimate(self, anchor_id: str, candidate_context: object) -> V43PrevalenceEstimate:
        if not isinstance(candidate_context, V43BoundCandidateRecord):
            raise V43PrevalenceError(
                "prevalence lookup requires a provider-bound cache member"
            )
        if candidate_context._provider_token is not self._provider_token:
            raise V43PrevalenceError("bound candidate belongs to another provider")
        source = self._artifact.source
        bindings = {
            "candidate cache manifest": (
                candidate_context.cache_manifest_sha256,
                source.cache_manifest_sha256,
            ),
            "candidate universe": (
                candidate_context.universe_sha256,
                source.logical_universe_sha256,
            ),
            "candidate mapping library": (
                candidate_context.mapping_library_sha256,
                source.mapping_library_sha256,
            ),
        }
        for label, (actual, expected) in bindings.items():
            if actual != expected:
                raise V43PrevalenceError(f"{label} mismatch")
        try:
            anchor = next(
                item for item in self._artifact.plan.anchors if item.anchor_id == anchor_id
            )
        except StopIteration as exc:
            raise V43PrevalenceError(f"unknown prevalence anchor: {anchor_id}") from exc
        features = candidate_context._record.feature_mapping()
        registry = _registry_by_id(self._cache.manifest.feature_registry)
        attempts: list[V43PrevalenceAttempt] = []
        selected: V43PrevalenceCellV1 | None = None
        for ordinal, level in enumerate(anchor.parent_hierarchy):
            parent_values = _parent_values(level, features, registry)
            key = _parent_values_sha256(parent_values)
            cell = self._cell_index.get((anchor_id, ordinal, key))
            if cell is None:
                raise V43PrevalenceError(
                    f"prevalence artifact lacks candidate cell at "
                    f"{anchor_id}/{level.level_id}"
                )
            attempts.append(
                V43PrevalenceAttempt(
                    level_id=level.level_id,
                    backoff_ordinal=ordinal,
                    denominator_duration_microseconds=(
                        cell.denominator_duration_microseconds
                    ),
                    minimum_effective_size_met=cell.minimum_effective_size_met,
                )
            )
            is_terminal = ordinal == len(anchor.parent_hierarchy) - 1
            if cell.minimum_effective_size_met or is_terminal:
                selected = cell
                break
        if selected is None:  # pragma: no cover - model guarantees a root
            raise V43PrevalenceError("no frozen prevalence backoff level was selectable")
        bits = capped_information_rubric_bits(
            selected.numerator_duration_microseconds,
            selected.denominator_duration_microseconds,
        )
        return V43PrevalenceEstimate(
            anchor_id=anchor_id,
            prevalence=(
                selected.numerator_duration_microseconds
                / selected.denominator_duration_microseconds
            ),
            numerator_duration_microseconds=(
                selected.numerator_duration_microseconds
            ),
            denominator_duration_microseconds=(
                selected.denominator_duration_microseconds
            ),
            universe_sha256=source.logical_universe_sha256,
            policy_version=self._artifact.policy.policy_version,
            parent_hierarchy_sha256=self._artifact.parent_hierarchy_sha256,
            selected_level_id=selected.level_id,
            backoff_ordinal=selected.backoff_ordinal,
            duration_weighted=True,
            conditional=True,
            selected_level_conditional=bool(selected.parent_values),
            exact_stable_intervals=True,
            source_scope="declared-global-utc-universe",
            information_rubric_bits=bits,
            attempts=tuple(attempts),
            artifact_sha256=self._artifact_sha256,
            plan_sha256=self._artifact.plan_sha256,
            mapping_library_sha256=source.mapping_library_sha256,
            mapping_source_library_sha256=source.mapping_source_library_sha256,
            mapping_prevalence_plan_sha256=source.mapping_prevalence_plan_sha256,
            required_feature_registry_sha256=(
                source.required_feature_registry_sha256
            ),
            cache_manifest_sha256=source.cache_manifest_sha256,
        )


def require_claim_grade_v4_3_prevalence_provider(
    provider: object,
) -> VerifiedV43ConditionalPrevalence:
    """Require the exact verifier-minted provider type and private capability.

    Runtime ``Protocol`` conformance is sufficient for pure scoring experiments,
    but cannot establish claim-grade artifact verification. Subclasses are also
    rejected so a structurally compatible object cannot override verification.
    """

    if not isinstance(provider, VerifiedV43ConditionalPrevalence) or (
        type(provider) is not VerifiedV43ConditionalPrevalence
    ):
        raise V43PrevalenceError(
            "claim-grade scoring requires the nominal verified prevalence provider"
        )
    if provider._token is not _VERIFIED_PROVIDER_TOKEN:
        raise V43PrevalenceError(
            "claim-grade prevalence provider lacks the verifier-minted capability"
        )
    return provider


def capped_information_rubric_bits(
    numerator_duration_microseconds: int,
    denominator_duration_microseconds: int,
) -> float:
    """Return deterministic capped rubric bits from exact integer durations."""

    if denominator_duration_microseconds <= 0:
        raise V43PrevalenceError("prevalence denominator must be positive")
    if not 0 < numerator_duration_microseconds <= denominator_duration_microseconds:
        raise V43PrevalenceError("prevalence must be in (0, 1]")
    return min(
        V43_INFORMATION_CAP_RUBRIC_BITS,
        math.log2(denominator_duration_microseconds / numerator_duration_microseconds),
    )


def derive_v4_3_prevalence_plan(
    cache_directory: str | Path,
    *,
    trust_lock_path: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    mapping_repository_root: str | Path,
) -> V43PrevalencePlanV1:
    """Derive a plan from actual verified mapping and cache bytes."""

    mapping = _load_mapping_binding(
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        mapping_repository_root=mapping_repository_root,
    )
    cache = _open_verified_cache_snapshot(
        cache_directory,
        trust_lock_path=trust_lock_path,
    )
    plan = _derive_plan(mapping, cache.verified)
    _require_snapshot_unchanged(cache)
    _require_mapping_unchanged(mapping)
    return plan


def build_v4_3_prevalence_artifact(
    cache_directory: str | Path,
    *,
    trust_lock_path: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    mapping_repository_root: str | Path,
    prevalence_plan_path: str | Path,
) -> V43ConditionalPrevalenceArtifactV1:
    """Stream the complete lock-verified cache under the exact frozen mapping."""

    mapping = _load_mapping_binding(
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        mapping_repository_root=mapping_repository_root,
    )
    cache = _open_verified_cache_snapshot(
        cache_directory,
        trust_lock_path=trust_lock_path,
    )
    plan = _load_and_match_plan(
        prevalence_plan_path,
        expected=_derive_plan(mapping, cache.verified),
    )
    artifact = _aggregate_verified_universe(cache, mapping=mapping, plan=plan)
    _require_snapshot_unchanged(cache)
    _require_mapping_unchanged(mapping)
    _require_plan_unchanged(prevalence_plan_path, plan)
    return artifact


def write_v4_3_prevalence_artifact_new(
    path: str | Path,
    artifact: V43ConditionalPrevalenceArtifactV1,
) -> Path:
    """Atomically create a canonical immutable prevalence artifact."""

    return write_new_canonical_json(path, artifact)


def write_v4_3_prevalence_plan_new(
    path: str | Path,
    plan: V43PrevalencePlanV1,
) -> Path:
    """Freeze a canonical plan without replacing any prior preregistration."""

    return write_new_canonical_json(path, plan)


def load_v4_3_prevalence_plan(path: str | Path) -> V43PrevalencePlanV1:
    """Load exact canonical plan bytes; malformed or reformatted plans fail."""

    source = Path(path)
    try:
        raw = source.read_bytes()
        parsed = json.loads(raw)
        if canonical_json_bytes(parsed) != raw:
            raise V43PrevalenceError("prevalence plan is not canonically encoded")
        return V43PrevalencePlanV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43PrevalenceError):
            raise
        raise V43PrevalenceError(f"invalid prevalence plan: {source}") from exc


def verify_v4_3_prevalence_artifact(
    artifact_path: str | Path,
    *,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    mapping_repository_root: str | Path,
    prevalence_plan_path: str | Path,
) -> VerifiedV43ConditionalPrevalence:
    """Replay mapping, cache, plan, and durations before minting a provider."""

    path = Path(artifact_path)
    try:
        raw = path.read_bytes()
        parsed = json.loads(raw)
        if canonical_json_bytes(parsed) != raw:
            raise V43PrevalenceError("prevalence artifact is not canonically encoded")
        artifact = V43ConditionalPrevalenceArtifactV1.model_validate_json(
            raw,
            strict=True,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43PrevalenceError):
            raise
        raise V43PrevalenceError("invalid V4.3 prevalence artifact") from exc
    mapping = _load_mapping_binding(
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        mapping_repository_root=mapping_repository_root,
    )
    cache = _open_verified_cache_snapshot(
        cache_directory,
        trust_lock_path=trust_lock_path,
    )
    plan = _load_and_match_plan(
        prevalence_plan_path,
        expected=_derive_plan(mapping, cache.verified),
    )
    expected = _aggregate_verified_universe(cache, mapping=mapping, plan=plan)
    if artifact != expected:
        raise V43PrevalenceError(
            "prevalence artifact differs from independent mapping/cache replay"
        )
    if path.read_bytes() != raw:
        raise V43PrevalenceError("prevalence artifact changed during verification")
    _require_snapshot_unchanged(cache)
    _require_mapping_unchanged(mapping)
    _require_plan_unchanged(prevalence_plan_path, plan)
    return VerifiedV43ConditionalPrevalence(
        artifact=artifact,
        artifact_sha256=sha256_bytes(raw),
        cache=cache.verified,
        _token=_VERIFIED_PROVIDER_TOKEN,
    )


def v4_3_predicate_matches(
    predicate: StructuralPredicateV2,
    features: Mapping[str, JsonValue],
    feature_registry: tuple[FeatureColumnSpec, ...],
) -> bool:
    """Evaluate one exact mapping predicate with strict feature-aware semantics."""

    registry = _registry_by_id(feature_registry)
    expected_ids = tuple(item.feature_id for item in feature_registry)
    actual_ids = tuple(features)
    if set(actual_ids) != set(expected_ids):
        missing = sorted(set(expected_ids) - set(actual_ids))
        extra = sorted(set(actual_ids) - set(expected_ids))
        raise V43PrevalenceError(
            "predicate feature mapping differs from registry; "
            f"missing={missing}, extra={extra}"
        )
    return _predicate_matches(predicate, features, registry)


def iter_artifact_cells(
    artifact: V43ConditionalPrevalenceArtifactV1,
) -> Iterator[V43PrevalenceCellV1]:
    """Yield canonical cells for transparent audit/reporting, never ranking."""

    for table in artifact.tables:
        yield from table.cells


def _load_mapping_binding(
    *,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    mapping_repository_root: str | Path,
) -> _MappingBinding:
    compiled_path = Path(mapping_library_path)
    source_path = Path(mapping_source_library_path)
    try:
        compiled_raw = compiled_path.read_bytes()
        source_raw = source_path.read_bytes()
        compiled_json = json.loads(compiled_raw)
        source_json = json.loads(source_raw)
        if canonical_json_bytes(compiled_json) != compiled_raw:
            raise V43PrevalenceError("compiled mapping library is not canonical")
        if canonical_json_bytes(source_json) != source_raw:
            raise V43PrevalenceError("mapping source library is not canonical")
        library = MappingLibraryV2.model_validate_json(compiled_raw, strict=True)
        source = MappingLibrarySourceV2.model_validate_json(source_raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43PrevalenceError):
            raise
        raise V43PrevalenceError("invalid canonical mapping-library-v2 bytes") from exc
    compiled_sha256 = sha256_bytes(compiled_raw)
    source_sha256 = sha256_bytes(source_raw)
    if compiled_sha256 != library.sha256():
        raise V43PrevalenceError("compiled mapping exact-byte hash is inconsistent")
    if source_sha256 != source.sha256():
        raise V43PrevalenceError("mapping source exact-byte hash is inconsistent")
    if library.source_library_sha256 != source_sha256:
        raise V43PrevalenceError("compiled mapping is bound to another source library")
    try:
        rebuilt = compile_verified_mapping_library_v2(
            source,
            repository_root=mapping_repository_root,
        )
    except (MappingV2Error, OSError, ValueError) as exc:
        raise V43PrevalenceError("mapping source provenance verification failed") from exc
    if rebuilt != library:
        raise V43PrevalenceError(
            "compiled mapping differs from deterministic source recompilation"
        )
    return _MappingBinding(
        library=library,
        source=source,
        library_sha256=compiled_sha256,
        source_sha256=source_sha256,
        library_path=compiled_path,
        source_path=source_path,
        library_bytes=compiled_raw,
        source_bytes=source_raw,
    )


def _require_mapping_unchanged(mapping: _MappingBinding) -> None:
    try:
        current_library = mapping.library_path.read_bytes()
        current_source = mapping.source_path.read_bytes()
    except OSError as exc:
        raise V43PrevalenceError("mapping artifacts became unreadable") from exc
    if current_library != mapping.library_bytes:
        raise V43PrevalenceError("compiled mapping changed during operation")
    if current_source != mapping.source_bytes:
        raise V43PrevalenceError("mapping source changed during operation")


def _anchors_from_mapping(
    library: MappingLibraryV2,
) -> tuple[V43PrevalenceAnchorV1, ...]:
    by_anchor: dict[str, V43PrevalenceAnchorV1] = {}
    for pathway in _mapping_pathways(library):
        anchor = V43PrevalenceAnchorV1(
            anchor_id=pathway.anchor_id,
            predicate=pathway.predicate,
            parent_hierarchy=pathway.prevalence_parent_hierarchy,
            required_feature_ids=pathway.required_feature_ids,
        )
        previous = by_anchor.get(anchor.anchor_id)
        if previous is not None and previous != anchor:
            raise V43PrevalenceError(
                f"one predicate anchor has conflicting parent plans: {anchor.anchor_id}"
            )
        by_anchor[anchor.anchor_id] = anchor
    return tuple(by_anchor[item] for item in sorted(by_anchor))


def _mapping_pathways(library: MappingLibraryV2) -> Iterator[CompiledPathwayV2]:
    for rule in library.rules:
        yield rule.primary_pathway
        yield from rule.alternative_pathways
        if rule.corroborating_pathway is not None:
            yield rule.corroborating_pathway.pathway


def _anchor_inventory_sha256(
    anchors: tuple[V43PrevalenceAnchorV1, ...],
    *,
    mapping_library_sha256: str,
    required_feature_registry_sha256: str,
) -> str:
    return sha256_json(
        {
            "mapping_library_sha256": mapping_library_sha256,
            "required_feature_registry_sha256": required_feature_registry_sha256,
            "anchors": [
                {
                    "anchor_id": anchor.anchor_id,
                    "predicate": anchor.predicate.model_dump(mode="json"),
                    "parent_hierarchy": [
                        level.model_dump(mode="json")
                        for level in anchor.parent_hierarchy
                    ],
                    "required_feature_ids": [
                        item.value for item in anchor.required_feature_ids
                    ],
                }
                for anchor in anchors
            ],
        }
    )


def _derive_plan(
    mapping: _MappingBinding,
    verified: VerifiedCenturyCache,
) -> V43PrevalencePlanV1:
    library = mapping.library
    anchors = _anchors_from_mapping(library)
    required = tuple(
        sorted(
            {
                feature_id
                for anchor in anchors
                for feature_id in anchor.required_feature_ids
            },
            key=lambda item: item.value,
        )
    )
    missing_from_mapping_registry = set(required) - set(
        library.required_feature_registry.feature_ids
    )
    if missing_from_mapping_registry:
        raise V43PrevalenceError(
            "mapping prevalence anchors are absent from the required feature registry: "
            f"{sorted(item.value for item in missing_from_mapping_registry)}"
        )
    registry = _registry_by_id(verified.manifest.feature_registry)
    missing = sorted(item.value for item in required if item.value not in registry)
    if missing:
        raise V43PrevalenceError(f"century cache lacks mapping features: {missing}")
    for anchor in anchors:
        _validate_predicate_compatibility(anchor.predicate, registry)
        for level in anchor.parent_hierarchy:
            for feature_id in level.parent_feature_ids:
                if feature_id.value not in registry:
                    raise V43PrevalenceError(
                        f"cache lacks parent feature: {feature_id.value}"
                    )
    plan = V43PrevalencePlanV1(
        mapping_library_sha256=mapping.library_sha256,
        mapping_source_library_sha256=mapping.source_sha256,
        mapping_prevalence_plan_sha256=mapping_prevalence_plan_sha256(library),
        mapping_required_feature_registry_sha256=(
            library.required_feature_registry_sha256
        ),
        expected_cache_semantic_feature_registry_sha256=(
            verified.manifest.semantic_feature_registry_sha256
        ),
        expected_cache_feature_registry_sha256=(
            verified.manifest.feature_registry_sha256
        ),
        required_feature_ids=required,
        required_feature_ids_sha256=required_feature_ids_sha256(
            tuple(item.value for item in required)
        ),
        anchors=anchors,
    )
    if plan.parent_hierarchy_sha256 != mapping_prevalence_parent_hierarchy_sha256(
        library
    ):
        raise V43PrevalenceError(
            "prevalence parent hierarchy differs from canonical mapping integration"
        )
    return plan


def _load_and_match_plan(
    path: str | Path,
    *,
    expected: V43PrevalencePlanV1,
) -> V43PrevalencePlanV1:
    plan = load_v4_3_prevalence_plan(path)
    if plan != expected:
        raise V43PrevalenceError(
            "frozen prevalence plan is stale or mismatched to mapping/cache bytes"
        )
    if sha256_file(path) != plan.sha256():
        raise V43PrevalenceError("frozen prevalence plan exact-byte hash mismatch")
    return plan


def _require_plan_unchanged(
    path: str | Path,
    plan: V43PrevalencePlanV1,
) -> None:
    try:
        current_sha256 = sha256_file(path)
    except OSError as exc:
        raise V43PrevalenceError("frozen prevalence plan became unreadable") from exc
    if current_sha256 != plan.sha256():
        raise V43PrevalenceError("frozen prevalence plan changed during operation")


def _open_verified_cache_snapshot(
    cache_directory: str | Path,
    *,
    trust_lock_path: str | Path,
) -> _VerifiedCacheSnapshot:
    """Verify from one lock object; no second load can swap expectations."""

    lock_path = Path(trust_lock_path)
    try:
        lock_bytes = lock_path.read_bytes()
        parsed = json.loads(lock_bytes)
        if canonical_json_bytes(parsed) != lock_bytes:
            raise V43PrevalenceError("century-cache trust lock is not canonical")
        lock = CenturyCacheTrustLockV1.model_validate_json(lock_bytes, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43PrevalenceError):
            raise
        raise V43PrevalenceError("invalid century-cache trust lock") from exc
    directory = Path(cache_directory)
    if not (directory / "manifest.json").is_file():
        raise V43PrevalenceError(
            "prevalence requires a prebuilt verified century cache"
        )
    try:
        verified = verify_century_cache(
            directory,
            expectations=century_cache_expectations_from_build_spec(lock.build_spec),
        )
    except CenturyCacheVerificationError as exc:
        raise V43PrevalenceError(f"century-cache verification failed: {exc}") from exc
    _require_cache_matches_lock(verified, lock)
    snapshot = _VerifiedCacheSnapshot(
        verified=verified,
        lock=lock,
        lock_sha256=sha256_bytes(lock_bytes),
        lock_path=lock_path,
        lock_bytes=lock_bytes,
    )
    _require_snapshot_unchanged(snapshot)
    return snapshot


def _require_cache_matches_lock(
    verified: VerifiedCenturyCache,
    lock: CenturyCacheTrustLockV1,
) -> None:
    manifest = verified.manifest
    bindings = {
        "manifest SHA-256": (verified.manifest_sha256, lock.manifest_sha256),
        "logical-universe hash": (
            manifest.logical_universe_sha256,
            lock.logical_universe_sha256,
        ),
        "interval count": (manifest.interval_count, lock.interval_count),
        "exact-state provenance": (
            manifest.exact_state_provenance,
            lock.exact_state_provenance,
        ),
        "ordered shard bindings": (manifest.shards, lock.shards),
    }
    for label, (actual, expected) in bindings.items():
        if actual != expected:
            raise V43PrevalenceError(f"cache {label} differs from trust lock")


def _require_snapshot_unchanged(snapshot: _VerifiedCacheSnapshot) -> None:
    try:
        current_lock = snapshot.lock_path.read_bytes()
    except OSError as exc:
        raise V43PrevalenceError("century-cache trust lock became unreadable") from exc
    if current_lock != snapshot.lock_bytes:
        raise V43PrevalenceError("century-cache trust lock changed during operation")
    if sha256_file(snapshot.verified.manifest_path) != (
        snapshot.verified.manifest_sha256
    ):
        raise V43PrevalenceError("century-cache manifest changed during operation")


def _aggregate_verified_universe(
    cache: _VerifiedCacheSnapshot,
    *,
    mapping: _MappingBinding,
    plan: V43PrevalencePlanV1,
) -> V43ConditionalPrevalenceArtifactV1:
    verified = cache.verified
    manifest = verified.manifest
    reconciliation_sha = manifest.reconciliation_aggregate_sha256
    if reconciliation_sha is None:
        raise V43PrevalenceError(
            "prevalence requires reconciliation-bound cache provenance"
        )
    registry = _registry_by_id(manifest.feature_registry)
    accumulators: dict[
        str,
        list[dict[str, tuple[tuple[V43ParentValueV1, ...], int, int]]],
    ] = {
        anchor.anchor_id: [dict() for _ in anchor.parent_hierarchy]
        for anchor in plan.anchors
    }
    total_duration_microseconds = 0
    row_count = 0
    for row in iter_verified_century_cache_rows(verified):
        try:
            validate_row_features(row, manifest.feature_registry)
        except CenturyCacheParquetError as exc:  # defense in depth after replay gate
            raise V43PrevalenceError("cache row feature validation failed") from exc
        duration = _duration_microseconds(row.utc_end - row.utc_start)
        total_duration_microseconds += duration
        row_count += 1
        features = row.feature_mapping()
        for anchor in plan.anchors:
            matches = _predicate_matches(anchor.predicate, features, registry)
            for ordinal, level in enumerate(anchor.parent_hierarchy):
                values = _parent_values(level, features, registry)
                key = _parent_values_sha256(values)
                previous = accumulators[anchor.anchor_id][ordinal].get(key)
                if previous is None:
                    accumulators[anchor.anchor_id][ordinal][key] = (
                        values,
                        duration if matches else 0,
                        duration,
                    )
                else:
                    previous_values, numerator, denominator = previous
                    if previous_values != values:
                        raise V43PrevalenceError("prevalence cell hash collision")
                    accumulators[anchor.anchor_id][ordinal][key] = (
                        values,
                        numerator + (duration if matches else 0),
                        denominator + duration,
                    )
    if row_count != manifest.interval_count:
        raise V43PrevalenceError("prevalence row count differs from manifest")
    horizon_duration = _duration_microseconds(
        manifest.utc_end_exclusive - manifest.utc_start
    )
    if total_duration_microseconds != horizon_duration:
        raise V43PrevalenceError("prevalence durations do not cover global UTC universe")
    policy = V43ConditionalPrevalencePolicyV1()
    source = V43PrevalenceSourceV1(
        cache_locator=cache.lock.cache_locator,
        cache_manifest_sha256=verified.manifest_sha256,
        cache_trust_lock_sha256=cache.lock_sha256,
        cache_build_spec_sha256=cache.lock.build_spec_sha256,
        cache_build_plan_sha256=manifest.build_plan_sha256,
        reconciliation_aggregate_sha256=reconciliation_sha,
        exact_state_provenance_sha256=sha256_json(
            manifest.exact_state_provenance.model_dump(mode="json")
        ),
        logical_universe_sha256=manifest.logical_universe_sha256,
        feature_vector_schema_version=manifest.feature_vector_schema_version,
        semantic_feature_registry_sha256=(
            manifest.semantic_feature_registry_sha256
        ),
        feature_registry_sha256=manifest.feature_registry_sha256,
        engine_identity_sha256=sha256_json(manifest.engine.model_dump(mode="json")),
        engine_validation_sha256=manifest.engine.engine_validation_sha256,
        ephemeris_source_manifest_sha256=(
            manifest.engine.ephemeris_provenance.source_manifest_sha256
        ),
        ephemeris_file_set_sha256=(
            manifest.engine.ephemeris_provenance.ephemeris_file_set_sha256
        ),
        boundary_policy_version=manifest.boundary_policy_version,
        generation_commit=manifest.generation_commit,
        utc_start=manifest.utc_start.isoformat().replace("+00:00", "Z"),
        utc_end_exclusive=(
            manifest.utc_end_exclusive.isoformat().replace("+00:00", "Z")
        ),
        interval_count=row_count,
        total_duration_microseconds=total_duration_microseconds,
        minimum_cell_duration_numerator=(
            total_duration_microseconds
            * V43_MINIMUM_EFFECTIVE_STATE_EQUIVALENTS
        ),
        minimum_cell_duration_denominator=row_count,
        mapping_library_sha256=mapping.library_sha256,
        mapping_source_library_sha256=mapping.source_sha256,
        mapping_prevalence_plan_sha256=plan.mapping_prevalence_plan_sha256,
        required_feature_registry_sha256=(
            mapping.library.required_feature_registry_sha256
        ),
    )
    tables: list[V43AnchorPrevalenceTableV1] = []
    for anchor in plan.anchors:
        cells: list[V43PrevalenceCellV1] = []
        for ordinal, level in enumerate(anchor.parent_hierarchy):
            for key, (values, numerator, denominator) in sorted(
                accumulators[anchor.anchor_id][ordinal].items()
            ):
                cells.append(
                    V43PrevalenceCellV1(
                        level_id=level.level_id,
                        backoff_ordinal=ordinal,
                        parent_values=values,
                        parent_values_sha256=key,
                        numerator_duration_microseconds=numerator,
                        denominator_duration_microseconds=denominator,
                        minimum_effective_size_met=(
                            denominator * row_count
                            >= total_duration_microseconds
                            * V43_MINIMUM_EFFECTIVE_STATE_EQUIVALENTS
                        ),
                    )
                )
        tables.append(
            V43AnchorPrevalenceTableV1(
                anchor_id=anchor.anchor_id,
                cells=tuple(cells),
            )
        )
    return V43ConditionalPrevalenceArtifactV1(
        source=source,
        policy=policy,
        policy_sha256=policy.sha256(),
        plan=plan,
        plan_sha256=plan.sha256(),
        parent_hierarchy_sha256=plan.parent_hierarchy_sha256,
        tables=tuple(tables),
    )


def _duration_microseconds(value: timedelta) -> int:
    result = (
        value.days * 86_400_000_000
        + value.seconds * 1_000_000
        + value.microseconds
    )
    if result <= 0:
        raise V43PrevalenceError("prevalence interval duration must be positive")
    return result


def _registry_by_id(
    registry: tuple[FeatureColumnSpec, ...],
) -> dict[str, FeatureColumnSpec]:
    result = {item.feature_id: item for item in registry}
    if len(result) != len(registry):
        raise V43PrevalenceError("cache feature registry contains duplicate IDs")
    return result


def _parent_values(
    level: PrevalenceParentLevelV2,
    features: Mapping[str, JsonValue],
    registry: Mapping[str, FeatureColumnSpec],
) -> tuple[V43ParentValueV1, ...]:
    result: list[V43ParentValueV1] = []
    for feature_id in level.parent_feature_ids:
        key = feature_id.value
        if key not in features:
            raise V43PrevalenceError(f"prevalence row lacks parent feature: {key}")
        if key not in registry:
            raise V43PrevalenceError(f"prevalence registry lacks parent feature: {key}")
        value = features[key]
        _validate_feature_value(key, value, registry[key])
        result.append(V43ParentValueV1(feature_id=key, value=value))
    return tuple(result)


def _parent_values_sha256(values: tuple[V43ParentValueV1, ...]) -> str:
    return sha256_json([item.model_dump(mode="json") for item in values])


def _predicate_matches(
    predicate: StructuralPredicateV2,
    features: Mapping[str, JsonValue],
    registry: Mapping[str, FeatureColumnSpec],
) -> bool:
    missing = sorted(
        item.value for item in predicate.required_feature_ids if item.value not in features
    )
    if missing:
        raise V43PrevalenceError(f"prevalence row lacks predicate features: {missing}")
    for required_feature_id in predicate.required_feature_ids:
        required_key = required_feature_id.value
        required_spec = registry.get(required_key)
        if required_spec is None:
            raise V43PrevalenceError(
                f"predicate feature is absent from registry: {required_key}"
            )
        _validate_feature_value(
            required_key,
            features[required_key],
            required_spec,
        )
    feature_key = predicate.feature_id.value
    spec = registry.get(feature_key)
    if spec is None:
        raise V43PrevalenceError(f"predicate feature is absent from registry: {feature_key}")
    _validate_predicate_compatibility(predicate, registry)
    actual = features[feature_key]
    if predicate.operator is PredicateOperatorV2.EQUALS_ANY:
        if not isinstance(actual, str):
            raise V43PrevalenceError("equals_any requires an exact string feature")
        return actual in predicate.values
    if predicate.operator in {
        PredicateOperatorV2.CONTAINS_ANY,
        PredicateOperatorV2.NOT_CONTAINS_ANY,
    }:
        contains = _contains_any(predicate.feature_id, actual, predicate.values)
        return (
            contains
            if predicate.operator is PredicateOperatorV2.CONTAINS_ANY
            else not contains
        )
    if predicate.operator is PredicateOperatorV2.PROFILE_HAS_LINE:
        if not isinstance(actual, str):
            raise V43PrevalenceError("profile_has_line requires a profile string")
        parts = actual.split("/")
        allowed = {"1", "2", "3", "4", "5", "6"}
        if len(parts) != 2 or any(part not in allowed for part in parts):
            raise V43PrevalenceError("profile_has_line received a malformed profile")
        return predicate.values[0] in parts
    if predicate.operator is PredicateOperatorV2.MATCHES_ACTIVATION:
        records = _activation_records(predicate.feature_id, actual)
        return any(_activation_matches(predicate, item) for item in records)
    if predicate.operator is PredicateOperatorV2.HAS_GATE:
        assert predicate.gate is not None
        gate_present = _has_gate(predicate.feature_id, actual, predicate)
        if not gate_present:
            return False
        if predicate.side is not None and predicate.feature_id in {
            FeatureId.HANGING_GATES,
            FeatureId.DORMANT_GATES,
        }:
            active = features.get(FeatureId.ACTIVE_GATES.value)
            active_spec = registry.get(FeatureId.ACTIVE_GATES.value)
            if active_spec is None or active is None:
                raise V43PrevalenceError(
                    "side-qualified Gate requires explicit active-Gate records"
                )
            _validate_feature_value(FeatureId.ACTIVE_GATES.value, active, active_spec)
            active_records = _active_gate_records(active)
            matching = next(
                (item for item in active_records if item.gate == predicate.gate), None
            )
            if matching is None:
                raise V43PrevalenceError(
                    "side-qualified Gate is absent from active-Gate records"
                )
            return any(
                position.startswith(f"{predicate.side}:")
                for position in matching.activation_positions
            )
        return True
    raise V43PrevalenceError(f"unsupported mapping operator: {predicate.operator.value}")


def _validate_predicate_compatibility(
    predicate: StructuralPredicateV2,
    registry: Mapping[str, FeatureColumnSpec],
) -> None:
    feature_key = predicate.feature_id.value
    spec = registry.get(feature_key)
    if spec is None:
        raise V43PrevalenceError(f"predicate feature is absent from registry: {feature_key}")
    operator = predicate.operator
    if operator is PredicateOperatorV2.EQUALS_ANY:
        if spec.storage_type is not FeatureStorageType.STRING:
            raise V43PrevalenceError("equals_any is incompatible with non-string feature")
    elif operator in {
        PredicateOperatorV2.CONTAINS_ANY,
        PredicateOperatorV2.NOT_CONTAINS_ANY,
    }:
        if predicate.feature_id is FeatureId.CENTERS and any(
            value not in {center.value for center in Center}
            for value in predicate.values
        ):
            raise V43PrevalenceError("Center predicate contains an unknown Center")
        compatible = predicate.feature_id in {
            FeatureId.CENTERS,
            FeatureId.COMPLETE_CHANNELS,
        } or spec.storage_type is FeatureStorageType.STRING_LIST
        if not compatible:
            raise V43PrevalenceError(
                f"{operator.value} is incompatible with feature {feature_key}"
            )
    elif operator is PredicateOperatorV2.PROFILE_HAS_LINE:
        if predicate.feature_id is not FeatureId.PROFILE or (
            spec.storage_type is not FeatureStorageType.STRING
        ):
            raise V43PrevalenceError("profile_has_line requires the Profile string feature")
    elif operator is PredicateOperatorV2.MATCHES_ACTIVATION:
        if spec.storage_type is not FeatureStorageType.ACTIVATION_LIST:
            raise V43PrevalenceError(
                "matches_activation requires an activation-list feature"
            )
    elif operator is PredicateOperatorV2.HAS_GATE:
        compatible = (
            spec.storage_type
            in {
                FeatureStorageType.INT64_LIST,
                FeatureStorageType.ACTIVATION_LIST,
            }
            or predicate.feature_id
            in {FeatureId.ACTIVE_GATES, FeatureId.REPEATED_GATES}
        )
        if not compatible:
            raise V43PrevalenceError(
                f"has_gate is incompatible with feature {feature_key}"
            )
    else:  # pragma: no cover - closed enum protects future additions
        raise V43PrevalenceError(f"unsupported mapping operator: {operator.value}")


def _validate_feature_value(
    feature_key: str,
    value: JsonValue,
    spec: FeatureColumnSpec,
) -> None:
    if value is None:
        raise V43PrevalenceError(f"feature {feature_key} is unknown/null")
    storage = spec.storage_type
    if storage is FeatureStorageType.BOOLEAN:
        valid = isinstance(value, bool)
    elif storage is FeatureStorageType.INT64:
        valid = isinstance(value, int) and not isinstance(value, bool)
    elif storage is FeatureStorageType.FLOAT64:
        valid = isinstance(value, float)
    elif storage is FeatureStorageType.STRING:
        valid = isinstance(value, str)
    elif storage is FeatureStorageType.STRING_LIST:
        valid = isinstance(value, list) and all(isinstance(item, str) for item in value)
    elif storage is FeatureStorageType.INT64_LIST:
        valid = isinstance(value, list) and all(
            isinstance(item, int) and not isinstance(item, bool) for item in value
        )
    elif storage is FeatureStorageType.ACTIVATION_LIST:
        _activation_records(FeatureId(feature_key), value)
        valid = True
    elif storage is FeatureStorageType.JSON:
        _validate_known_json_feature(FeatureId(feature_key), value)
        valid = True
    else:  # pragma: no cover - closed storage enum
        valid = False
    if not valid:
        raise V43PrevalenceError(
            f"feature {feature_key} does not match storage type {storage.value}"
        )


def _validate_known_json_feature(feature_id: FeatureId, value: JsonValue) -> None:
    if feature_id is FeatureId.CENTERS:
        _center_sets(value)
    elif feature_id is FeatureId.COMPLETE_CHANNELS:
        _complete_channel_records(value)
    elif feature_id in {FeatureId.ACTIVE_GATES, FeatureId.REPEATED_GATES}:
        _active_gate_records(value)
    elif feature_id is FeatureId.DEFINITION_TOPOLOGY:
        _definition_topology(value)
    elif feature_id is FeatureId.POSSIBLE_BRIDGES:
        _possible_bridge_records(value)
    else:
        canonical_json_bytes(value)


def _center_sets(value: JsonValue) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not isinstance(value, dict) or set(value) != {"defined", "undefined"}:
        raise V43PrevalenceError("Center feature must have exact defined/undefined fields")
    defined = value["defined"]
    undefined = value["undefined"]
    if not isinstance(defined, list) or not all(isinstance(item, str) for item in defined):
        raise V43PrevalenceError("defined Centers must be a string list")
    if not isinstance(undefined, list) or not all(
        isinstance(item, str) for item in undefined
    ):
        raise V43PrevalenceError("undefined Centers must be a string list")
    if len(set(defined)) != len(defined) or len(set(undefined)) != len(undefined):
        raise V43PrevalenceError("Center lists must not contain duplicates")
    if set(defined) & set(undefined):
        raise V43PrevalenceError("defined and undefined Centers must be disjoint")
    defined_values = tuple(item for item in defined if isinstance(item, str))
    undefined_values = tuple(item for item in undefined if isinstance(item, str))
    if defined_values != tuple(sorted(defined_values)) or undefined_values != tuple(
        sorted(undefined_values)
    ):
        raise V43PrevalenceError("Center lists must use canonical sorted order")
    if set(defined_values) | set(undefined_values) != {
        center.value for center in Center
    }:
        raise V43PrevalenceError("Centers must partition the exact nine-center registry")
    return (
        defined_values,
        undefined_values,
    )


def _contains_any(
    feature_id: FeatureId,
    actual: JsonValue,
    expected: tuple[str, ...],
) -> bool:
    if feature_id is FeatureId.CENTERS:
        defined, _undefined = _center_sets(actual)
        return any(item in defined for item in expected)
    if feature_id is FeatureId.COMPLETE_CHANNELS:
        channels = _complete_channel_records(actual)
        return any(item.channel in expected for item in channels)
    if not isinstance(actual, list) or not all(isinstance(item, str) for item in actual):
        raise V43PrevalenceError("contains predicate requires a strict string list")
    return any(item in actual for item in expected)


def _complete_channel_records(value: JsonValue) -> tuple[CompleteChannelFeature, ...]:
    if not isinstance(value, list):
        raise V43PrevalenceError("complete Channels must be a record list")
    result: list[CompleteChannelFeature] = []
    expected = {"channel", "gate_a", "gate_b", "center_a", "center_b"}
    for item in value:
        if not isinstance(item, dict) or set(item) != expected:
            raise V43PrevalenceError("malformed or unknown complete-Channel fields")
        if (
            not isinstance(item["channel"], str)
            or not isinstance(item["center_a"], str)
            or not isinstance(item["center_b"], str)
            or not _strict_int(item["gate_a"])
            or not _strict_int(item["gate_b"])
        ):
            raise V43PrevalenceError("malformed complete-Channel field types")
        try:
            record = CompleteChannelFeature.model_validate(item, strict=True)
        except ValueError as exc:
            raise V43PrevalenceError("malformed complete-Channel values") from exc
        known_channels = {channel.identifier for channel in CHANNELS}
        if record.channel not in known_channels or (
            {record.center_a, record.center_b}
            != {
                GATE_TO_CENTER[record.gate_a].value,
                GATE_TO_CENTER[record.gate_b].value,
            }
        ):
            raise V43PrevalenceError(
                "complete Channel differs from the frozen Bodygraph registry"
            )
        result.append(record)
    return tuple(result)


def _active_gate_records(value: JsonValue) -> tuple[ActiveGateFeature, ...]:
    if not isinstance(value, list):
        raise V43PrevalenceError("active/repeated Gates must be a record list")
    result: list[ActiveGateFeature] = []
    expected = {"gate", "activation_count", "activation_positions"}
    for item in value:
        if not isinstance(item, dict) or set(item) != expected:
            raise V43PrevalenceError("malformed or unknown active-Gate fields")
        gate = item["gate"]
        activation_count = item["activation_count"]
        positions = item["activation_positions"]
        if (
            not _strict_int(gate)
            or not _strict_int(activation_count)
            or not isinstance(positions, list)
            or not all(isinstance(position, str) for position in positions)
        ):
            raise V43PrevalenceError("malformed active-Gate field types")
        canonical_positions = tuple(
            f"{side}:{body.value}"
            for side in ("design", "personality")
            for body in CelestialBody
        )
        typed_positions = tuple(
            position for position in positions if isinstance(position, str)
        )
        if (
            typed_positions != tuple(sorted(typed_positions))
            or any(position not in canonical_positions for position in typed_positions)
        ):
            raise V43PrevalenceError(
                "active-Gate positions must use canonical side/carrier identities"
            )
        try:
            result.append(
                ActiveGateFeature(
                    gate=gate,
                    activation_count=activation_count,
                    activation_positions=typed_positions,
                )
            )
        except ValueError as exc:
            raise V43PrevalenceError("malformed active-Gate values") from exc
    return tuple(result)


def _definition_topology(value: JsonValue) -> tuple[tuple[str, ...], ...]:
    if not isinstance(value, list):
        raise V43PrevalenceError("Definition topology must be a component list")
    known = {center.value for center in Center}
    components: list[tuple[str, ...]] = []
    for component in value:
        if (
            not isinstance(component, list)
            or not component
            or not all(isinstance(center, str) for center in component)
        ):
            raise V43PrevalenceError("Definition component has a malformed shape")
        typed = tuple(center for center in component if isinstance(center, str))
        if typed != tuple(sorted(set(typed))) or not set(typed) <= known:
            raise V43PrevalenceError("Definition component is noncanonical")
        components.append(typed)
    result = tuple(components)
    if result != tuple(sorted(result)):
        raise V43PrevalenceError("Definition components must be canonically sorted")
    flattened = tuple(center for component in result for center in component)
    if len(flattened) != len(set(flattened)):
        raise V43PrevalenceError("Definition components must be disjoint")
    return result


def _possible_bridge_records(value: JsonValue) -> tuple[PossibleBridgeFeature, ...]:
    if not isinstance(value, list):
        raise V43PrevalenceError("possible Bridges must be a record list")
    expected = {
        "missing_gate",
        "active_complement_gate",
        "channel",
        "definition_component_indexes",
    }
    known_channels = {channel.identifier for channel in CHANNELS}
    result: list[PossibleBridgeFeature] = []
    for item in value:
        if not isinstance(item, dict) or set(item) != expected:
            raise V43PrevalenceError("malformed or unknown possible-Bridge fields")
        missing_gate = item["missing_gate"]
        complement = item["active_complement_gate"]
        channel = item["channel"]
        indexes = item["definition_component_indexes"]
        if (
            not _strict_int(missing_gate)
            or not _strict_int(complement)
            or not isinstance(channel, str)
            or channel not in known_channels
            or {missing_gate, complement}
            != {int(gate) for gate in channel.split("-")}
            or not isinstance(indexes, list)
            or len(indexes) != 2
            or not all(_strict_int(index) for index in indexes)
        ):
            raise V43PrevalenceError("malformed possible-Bridge field types")
        typed_indexes = tuple(index for index in indexes if _strict_int(index))
        try:
            result.append(
                PossibleBridgeFeature(
                    missing_gate=missing_gate,
                    active_complement_gate=complement,
                    channel=channel,
                    definition_component_indexes=(
                        typed_indexes[0],
                        typed_indexes[1],
                    ),
                )
            )
        except ValueError as exc:
            raise V43PrevalenceError("malformed possible-Bridge values") from exc
    return tuple(result)


def _activation_records(
    feature_id: FeatureId,
    value: JsonValue,
) -> tuple[ActivationFeature, ...]:
    if not isinstance(value, list):
        raise V43PrevalenceError(
            f"activation feature {feature_id.value} must be a record list"
        )
    result: list[ActivationFeature] = []
    expected = {"body", "side", "gate", "line", "color", "tone", "base"}
    allowed_bodies = {body.value: body for body in CelestialBody}
    for item in value:
        if not isinstance(item, dict) or set(item) != expected:
            raise V43PrevalenceError("malformed or unknown activation fields")
        body = item["body"]
        side = item["side"]
        gate = item["gate"]
        line = item["line"]
        color = item["color"]
        tone = item["tone"]
        base = item["base"]
        if (
            not isinstance(body, str)
            or body not in allowed_bodies
            or not isinstance(side, str)
            or side not in {"personality", "design"}
            or not _strict_int(gate)
            or not _strict_int(line)
            or not _strict_optional_int(color)
            or not _strict_optional_int(tone)
            or not _strict_optional_int(base)
        ):
            raise V43PrevalenceError("malformed activation field types")
        try:
            result.append(
                ActivationFeature(
                    body=allowed_bodies[body],
                    side="personality" if side == "personality" else "design",
                    gate=gate,
                    line=line,
                    color=color,
                    tone=tone,
                    base=base,
                )
            )
        except ValueError as exc:
            raise V43PrevalenceError("malformed activation values") from exc
    return tuple(result)


def _strict_int(value: JsonValue) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool)


def _strict_optional_int(value: JsonValue) -> TypeGuard[int | None]:
    return value is None or _strict_int(value)


def _activation_matches(
    predicate: StructuralPredicateV2,
    record: ActivationFeature,
) -> bool:
    return all(
        actual == expected
        for actual, expected in (
            (record.side, predicate.side),
            (record.body, predicate.carrier),
            (record.gate, predicate.gate),
            (record.line, predicate.line),
        )
        if expected is not None
    )


def _has_gate(
    feature_id: FeatureId,
    actual: JsonValue,
    predicate: StructuralPredicateV2,
) -> bool:
    assert predicate.gate is not None
    if feature_id in {FeatureId.HANGING_GATES, FeatureId.DORMANT_GATES}:
        if not isinstance(actual, list) or not all(
            isinstance(item, int) and not isinstance(item, bool) for item in actual
        ):
            raise V43PrevalenceError("hanging/dormant Gates must be an integer list")
        return predicate.gate in actual
    if feature_id in {FeatureId.ACTIVE_GATES, FeatureId.REPEATED_GATES}:
        for record in _active_gate_records(actual):
            if record.gate != predicate.gate:
                continue
            return (
                predicate.minimum_occurrences is None
                or record.activation_count >= predicate.minimum_occurrences
            )
        return False
    return any(
        record.gate == predicate.gate and _activation_matches(predicate, record)
        for record in _activation_records(feature_id, actual)
    )
