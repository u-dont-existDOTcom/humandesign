"""Cache-only duration-weighted conditional prevalence for V4.3.

The public builder deliberately accepts cache and trust-lock paths, not candidate
rows.  It opens the cache through the ordinary recovery gate and streams the
complete exact-state universe.  The resulting artifact is therefore unsuitable
for, and cannot be constructed from, a finalist or candidate file.

This module contains no behavioral responses, answer keys, or ranking logic.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import timedelta
from enum import StrEnum
from pathlib import Path
from typing import Final, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from hdmatch.century_cache.models import (
    FEATURE_ID_PATTERN,
    SHA256_PATTERN,
    CenturyStateRecord,
    VerifiedCenturyCache,
    required_feature_ids_sha256,
)
from hdmatch.century_cache.store import (
    iter_verified_century_cache_rows,
    open_century_cache_for_recovery,
)
from hdmatch.century_cache.trust_lock import (
    CenturyCacheTrustLockV1,
    load_century_cache_trust_lock,
)
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)

V43_PREVALENCE_POLICY_VERSION: Final[str] = (
    "v4.3-global-duration-conditional-prevalence-v1"
)
V43_INFORMATION_CAP_RUBRIC_BITS: Final[float] = 6.0
V43_MINIMUM_EFFECTIVE_STATE_EQUIVALENTS: Final[int] = 500
_VERIFIED_PROVIDER_TOKEN: Final[object] = object()


class V43PrevalenceError(ValueError):
    """A V4.3 prevalence input or artifact violates the frozen contract."""


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class V43PredicateOperator(StrEnum):
    """Small, deterministic predicate language over canonical M0-M2 values."""

    EQUALS = "equals"
    EQUALS_ANY = "equals_any"
    SEQUENCE_CONTAINS = "sequence_contains"
    SEQUENCE_CONTAINS_ANY = "sequence_contains_any"
    SEQUENCE_EXCLUDES = "sequence_excludes"
    SEQUENCE_CONTAINS_RECORD = "sequence_contains_record"
    SEQUENCE_EXCLUDES_RECORD = "sequence_excludes_record"
    SEQUENCE_CONTAINS_RECORD_NUMERIC_GTE = (
        "sequence_contains_record_numeric_gte"
    )
    SEQUENCE_CONTAINS_RECORD_NESTED_PREFIX = (
        "sequence_contains_record_nested_prefix"
    )
    PROFILE_HAS_LINE = "profile_has_line"


class V43FeatureClauseV1(_FrozenModel):
    feature_id: str = Field(pattern=FEATURE_ID_PATTERN)
    operator: V43PredicateOperator
    expected: JsonValue

    @model_validator(mode="after")
    def require_operator_value_shape(self) -> V43FeatureClauseV1:
        if self.expected is None:
            raise ValueError("prevalence predicates cannot match an unknown value")
        record_operators = {
            V43PredicateOperator.SEQUENCE_CONTAINS_RECORD,
            V43PredicateOperator.SEQUENCE_EXCLUDES_RECORD,
        }
        sequence_operators = {
            V43PredicateOperator.SEQUENCE_CONTAINS,
            V43PredicateOperator.SEQUENCE_EXCLUDES,
        }
        any_operators = {
            V43PredicateOperator.EQUALS_ANY,
            V43PredicateOperator.SEQUENCE_CONTAINS_ANY,
        }
        if self.operator in record_operators and (
            not isinstance(self.expected, dict) or not self.expected
        ):
            raise ValueError("record predicates require a nonempty JSON object")
        if self.operator in sequence_operators and isinstance(
            self.expected, (dict, list)
        ):
            raise ValueError("scalar sequence predicates require a scalar expected value")
        if self.operator in any_operators and (
            not isinstance(self.expected, list) or not self.expected
        ):
            raise ValueError("any-of predicates require a nonempty JSON list")
        if self.operator is V43PredicateOperator.PROFILE_HAS_LINE and (
            isinstance(self.expected, bool)
            or not isinstance(self.expected, int)
            or not 1 <= self.expected <= 6
        ):
            raise ValueError("profile-line predicates require an integer from 1 through 6")
        if self.operator in {
            V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NUMERIC_GTE,
            V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NESTED_PREFIX,
        }:
            self._validate_structured_record_predicate()
        return self

    def _validate_structured_record_predicate(self) -> None:
        if not isinstance(self.expected, dict):
            raise ValueError("structured record predicates require a JSON object")
        expected_keys = (
            {"match", "field", "minimum"}
            if self.operator
            is V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NUMERIC_GTE
            else {"match", "field", "prefix"}
        )
        if set(self.expected) != expected_keys:
            raise ValueError("structured record predicate fields are incomplete")
        match = self.expected.get("match")
        field = self.expected.get("field")
        if not isinstance(match, dict) or not match or not isinstance(field, str) or not field:
            raise ValueError("structured record predicate match/field is invalid")
        if self.operator is V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NUMERIC_GTE:
            minimum = self.expected.get("minimum")
            if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 1:
                raise ValueError("numeric record predicate minimum must be a positive integer")
        else:
            prefix = self.expected.get("prefix")
            if not isinstance(prefix, str) or not prefix:
                raise ValueError("nested record predicate prefix must be nonempty")


class V43FeaturePredicateV1(_FrozenModel):
    """A preregistered conjunction; post-search conjunction mining is forbidden."""

    clauses: tuple[V43FeatureClauseV1, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def require_canonical_unique_clauses(self) -> V43FeaturePredicateV1:
        identities = tuple(
            (
                clause.feature_id,
                clause.operator.value,
                sha256_json(clause.expected),
            )
            for clause in self.clauses
        )
        if len(identities) != len(set(identities)):
            raise ValueError("prevalence predicate contains duplicate clauses")
        if identities != tuple(sorted(identities)):
            raise ValueError("prevalence predicate clauses must be canonically ordered")
        return self

    @property
    def required_feature_ids(self) -> tuple[str, ...]:
        return tuple(sorted({clause.feature_id for clause in self.clauses}))


class V43PrevalenceParentLevelV1(_FrozenModel):
    level_id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    parent_feature_ids: tuple[str, ...]

    @model_validator(mode="after")
    def require_canonical_features(self) -> V43PrevalenceParentLevelV1:
        if self.parent_feature_ids != tuple(sorted(set(self.parent_feature_ids))):
            raise ValueError("prevalence parent feature IDs must be sorted and unique")
        if any(
            re.fullmatch(FEATURE_ID_PATTERN, item) is None
            for item in self.parent_feature_ids
        ):
            raise ValueError("prevalence parent feature ID is invalid")
        return self


class V43PrevalenceAnchorV1(_FrozenModel):
    anchor_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
    predicate: V43FeaturePredicateV1
    parent_hierarchy: tuple[V43PrevalenceParentLevelV1, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def require_strict_terminal_backoff(self) -> V43PrevalenceAnchorV1:
        level_ids = tuple(level.level_id for level in self.parent_hierarchy)
        if len(level_ids) != len(set(level_ids)):
            raise ValueError("prevalence parent level IDs must be unique")
        if self.parent_hierarchy[-1].parent_feature_ids:
            raise ValueError("prevalence hierarchy must end in an unconditional root level")
        previous = frozenset(self.parent_hierarchy[0].parent_feature_ids)
        for level in self.parent_hierarchy[1:]:
            current = frozenset(level.parent_feature_ids)
            if not current < previous:
                raise ValueError(
                    "prevalence backoff must strictly remove parent features without adding any"
                )
            previous = current
        return self

    @property
    def required_feature_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                set(self.predicate.required_feature_ids).union(
                    *(set(level.parent_feature_ids) for level in self.parent_hierarchy)
                )
            )
        )


class V43PrevalencePlanV1(_FrozenModel):
    """Mapping-derived, pre-search prevalence anchors and parent hierarchy."""

    schema_version: Literal["v4-3-prevalence-plan-v1"] = "v4-3-prevalence-plan-v1"
    model_version: Literal["V4.3"] = "V4.3"
    mapping_artifact_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_required_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    expected_cache_semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    expected_cache_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    required_feature_ids: tuple[str, ...] = Field(min_length=1)
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
                }
            )
        )
        if self.required_feature_ids != derived:
            raise ValueError("prevalence plan required features differ from its predicates")
        if self.required_feature_ids_sha256 != required_feature_ids_sha256(derived):
            raise ValueError("prevalence plan required-feature hash is inconsistent")
        return self

    def sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))

    @property
    def parent_hierarchy_sha256(self) -> str:
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

    schema_version: Literal["v4-3-conditional-prevalence-policy-v1"] = (
        "v4-3-conditional-prevalence-policy-v1"
    )
    policy_version: Literal[
        "v4.3-global-duration-conditional-prevalence-v1"
    ] = "v4.3-global-duration-conditional-prevalence-v1"
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
    schema_version: Literal["v4-3-prevalence-source-v1"] = "v4-3-prevalence-source-v1"
    cache_locator: str = Field(min_length=1)
    cache_version: Literal["century-cache-v1"] = "century-cache-v1"
    cache_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_trust_lock_sha256: str = Field(pattern=SHA256_PATTERN)
    cache_build_spec_sha256: str = Field(pattern=SHA256_PATTERN)
    build_plan_sha256: str = Field(pattern=SHA256_PATTERN)
    reconciliation_aggregate_sha256: str = Field(pattern=SHA256_PATTERN)
    exact_state_provenance_sha256: str = Field(pattern=SHA256_PATTERN)
    logical_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_vector_schema_version: str = Field(min_length=1)
    semantic_feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    feature_registry_sha256: str = Field(pattern=SHA256_PATTERN)
    engine_identity_sha256: str = Field(pattern=SHA256_PATTERN)
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
        if self.parent_values_sha256 != sha256_json(
            [item.model_dump(mode="json") for item in self.parent_values]
        ):
            raise ValueError("prevalence cell parent-value hash is inconsistent")
        return self


class V43AnchorPrevalenceTableV1(_FrozenModel):
    anchor_id: str
    cells: tuple[V43PrevalenceCellV1, ...] = Field(min_length=1)


class V43ConditionalPrevalenceArtifactV1(_FrozenModel):
    """Versioned duration tables for one exact lock-verified global universe."""

    schema_version: Literal["v4-3-conditional-prevalence-artifact-v1"] = (
        "v4-3-conditional-prevalence-artifact-v1"
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
        source_plan_bindings = {
            "semantic feature registry": (
                self.source.semantic_feature_registry_sha256,
                self.plan.expected_cache_semantic_feature_registry_sha256,
            ),
            "physical feature registry": (
                self.source.feature_registry_sha256,
                self.plan.expected_cache_feature_registry_sha256,
            ),
        }
        for label, (actual, expected) in source_plan_bindings.items():
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
            cells = tuple(cell for cell in table.cells if cell.backoff_ordinal == ordinal)
            if not cells:
                raise ValueError(f"prevalence level has no cells for {anchor.anchor_id}")
            if any(cell.level_id != level.level_id for cell in cells):
                raise ValueError(f"prevalence level ID differs from plan for {anchor.anchor_id}")
            if any(
                tuple(item.feature_id for item in cell.parent_values)
                != level.parent_feature_ids
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
            numerators.add(sum(cell.numerator_duration_microseconds for cell in cells))
            for cell in cells:
                expected_minimum = (
                    cell.denominator_duration_microseconds
                    * self.source.minimum_cell_duration_denominator
                    >= self.source.minimum_cell_duration_numerator
                )
                if cell.minimum_effective_size_met != expected_minimum:
                    raise ValueError(
                        f"prevalence minimum-cell decision is inconsistent for {anchor.anchor_id}"
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


@dataclass(frozen=True, slots=True)
class V43PrevalenceProvenance:
    universe_sha256: str
    policy_version: str
    parent_hierarchy_sha256: str
    duration_weighted: Literal[True]
    conditional: Literal[True]
    exact_stable_intervals: Literal[True]
    source_scope: Literal["declared-global-utc-universe"]
    cache_manifest_sha256: str
    cache_trust_lock_sha256: str
    artifact_sha256: str


class VerifiedV43ConditionalPrevalence:
    """Factory-verified provider consumed by the V4.3 scorer."""

    __slots__ = ("_artifact", "_artifact_sha256", "_cell_index", "_token")

    def __init__(
        self,
        *,
        artifact: V43ConditionalPrevalenceArtifactV1,
        artifact_sha256: str,
        _token: object,
    ) -> None:
        if _token is not _VERIFIED_PROVIDER_TOKEN:
            raise V43PrevalenceError(
                "verified V4.3 prevalence providers must come from cache replay verification"
            )
        self._artifact = artifact
        self._artifact_sha256 = artifact_sha256
        self._cell_index = {
            (table.anchor_id, cell.backoff_ordinal, cell.parent_values_sha256): cell
            for table in artifact.tables
            for cell in table.cells
        }
        self._token = _token

    @property
    def provenance(self) -> V43PrevalenceProvenance:
        source = self._artifact.source
        return V43PrevalenceProvenance(
            universe_sha256=source.logical_universe_sha256,
            policy_version=self._artifact.policy.policy_version,
            parent_hierarchy_sha256=self._artifact.parent_hierarchy_sha256,
            duration_weighted=True,
            conditional=True,
            exact_stable_intervals=True,
            source_scope="declared-global-utc-universe",
            cache_manifest_sha256=source.cache_manifest_sha256,
            cache_trust_lock_sha256=source.cache_trust_lock_sha256,
            artifact_sha256=self._artifact_sha256,
        )

    @property
    def artifact(self) -> V43ConditionalPrevalenceArtifactV1:
        return self._artifact

    def estimate(self, anchor_id: str, candidate_context: object) -> V43PrevalenceEstimate:
        if not isinstance(candidate_context, CenturyStateRecord):
            raise V43PrevalenceError(
                "V4.3 prevalence lookup requires a canonical century-cache row"
            )
        source = self._artifact.source
        row_bindings = {
            "feature-vector schema": (
                candidate_context.feature_vector_schema_version,
                source.feature_vector_schema_version,
            ),
            "semantic feature registry": (
                candidate_context.semantic_feature_registry_sha256,
                source.semantic_feature_registry_sha256,
            ),
            "physical feature registry": (
                candidate_context.feature_registry_sha256,
                source.feature_registry_sha256,
            ),
        }
        for label, (actual, expected) in row_bindings.items():
            if actual != expected:
                raise V43PrevalenceError(f"candidate row {label} mismatch")
        try:
            anchor = next(
                item for item in self._artifact.plan.anchors if item.anchor_id == anchor_id
            )
        except StopIteration as exc:
            raise V43PrevalenceError(f"unknown V4.3 prevalence anchor: {anchor_id}") from exc
        features = candidate_context.feature_mapping()
        attempts: list[V43PrevalenceAttempt] = []
        selected: V43PrevalenceCellV1 | None = None
        for ordinal, level in enumerate(anchor.parent_hierarchy):
            parent_values = _parent_values(level, features)
            key = sha256_json([item.model_dump(mode="json") for item in parent_values])
            cell = self._cell_index.get((anchor_id, ordinal, key))
            if cell is None:
                raise V43PrevalenceError(
                    f"prevalence artifact lacks candidate cell at {anchor_id}/{level.level_id}"
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
        if selected is None:  # pragma: no cover - plan validation guarantees terminal root
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
        )


def capped_information_rubric_bits(
    numerator_duration_microseconds: int,
    denominator_duration_microseconds: int,
) -> float:
    """Return deterministic V4.3 capped rubric bits from exact integer durations."""

    if denominator_duration_microseconds <= 0:
        raise V43PrevalenceError("prevalence denominator must be positive")
    if not 0 < numerator_duration_microseconds <= denominator_duration_microseconds:
        raise V43PrevalenceError("prevalence must be in (0, 1]")
    return min(
        V43_INFORMATION_CAP_RUBRIC_BITS,
        math.log2(denominator_duration_microseconds / numerator_duration_microseconds),
    )


def build_v4_3_prevalence_artifact(
    cache_directory: str | Path,
    *,
    trust_lock_path: str | Path,
    plan: V43PrevalencePlanV1,
) -> V43ConditionalPrevalenceArtifactV1:
    """Stream the complete lock-verified cache into a V4.3 prevalence artifact."""

    cache_path = Path(cache_directory)
    lock_path = Path(trust_lock_path)
    initial_lock_sha256 = sha256_file(lock_path)
    lock = load_century_cache_trust_lock(lock_path)
    verified = open_century_cache_for_recovery(
        cache_path,
        trust_lock_path=lock_path,
    )
    _validate_plan_cache_binding(plan, verified)
    artifact = _aggregate_verified_universe(
        verified,
        lock=lock,
        trust_lock_sha256=initial_lock_sha256,
        plan=plan,
    )
    if sha256_file(lock_path) != initial_lock_sha256:
        raise V43PrevalenceError("century-cache trust lock changed during prevalence build")
    if sha256_file(verified.manifest_path) != verified.manifest_sha256:
        raise V43PrevalenceError("century-cache manifest changed during prevalence build")
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
            raise V43PrevalenceError("V4.3 prevalence plan is not canonically encoded")
        return V43PrevalencePlanV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43PrevalenceError):
            raise
        raise V43PrevalenceError(f"invalid V4.3 prevalence plan: {source}") from exc


def verify_v4_3_prevalence_artifact(
    artifact_path: str | Path,
    *,
    cache_directory: str | Path,
    trust_lock_path: str | Path,
    expected_plan: V43PrevalencePlanV1,
) -> VerifiedV43ConditionalPrevalence:
    """Replay the global cache and mint a scorer provider only on exact equality."""

    path = Path(artifact_path)
    raw = path.read_bytes()
    try:
        parsed = json.loads(raw)
        if canonical_json_bytes(parsed) != raw:
            raise V43PrevalenceError("prevalence artifact is not canonically encoded")
        artifact = V43ConditionalPrevalenceArtifactV1.model_validate_json(raw, strict=True)
    except (json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, V43PrevalenceError):
            raise
        raise V43PrevalenceError("invalid V4.3 prevalence artifact") from exc
    if artifact.plan != expected_plan:
        raise V43PrevalenceError("prevalence artifact uses a different frozen plan")
    expected = build_v4_3_prevalence_artifact(
        cache_directory,
        trust_lock_path=trust_lock_path,
        plan=expected_plan,
    )
    if artifact != expected:
        raise V43PrevalenceError(
            "prevalence artifact differs from an independent global-cache replay"
        )
    if path.read_bytes() != raw:
        raise V43PrevalenceError("prevalence artifact changed during verification")
    return VerifiedV43ConditionalPrevalence(
        artifact=artifact,
        artifact_sha256=sha256_bytes(raw),
        _token=_VERIFIED_PROVIDER_TOKEN,
    )


def _validate_plan_cache_binding(
    plan: V43PrevalencePlanV1,
    verified: VerifiedCenturyCache,
) -> None:
    manifest = verified.manifest
    expected = {
        "semantic feature registry": (
            manifest.semantic_feature_registry_sha256,
            plan.expected_cache_semantic_feature_registry_sha256,
        ),
        "physical feature registry": (
            manifest.feature_registry_sha256,
            plan.expected_cache_feature_registry_sha256,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise V43PrevalenceError(f"prevalence plan {label} mismatch")
    available = {item.feature_id for item in manifest.feature_registry}
    missing = sorted(set(plan.required_feature_ids) - available)
    if missing:
        raise V43PrevalenceError(
            f"century cache lacks prevalence-plan features: {missing}"
        )


def _aggregate_verified_universe(
    verified: VerifiedCenturyCache,
    *,
    lock: CenturyCacheTrustLockV1,
    trust_lock_sha256: str,
    plan: V43PrevalencePlanV1,
) -> V43ConditionalPrevalenceArtifactV1:
    manifest = verified.manifest
    reconciliation_sha = manifest.reconciliation_aggregate_sha256
    if reconciliation_sha is None:
        raise V43PrevalenceError(
            "V4.3 prevalence requires reconciliation-bound century-cache provenance"
        )
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
        duration = _duration_microseconds(row.utc_end - row.utc_start)
        total_duration_microseconds += duration
        row_count += 1
        features = row.feature_mapping()
        for anchor in plan.anchors:
            matches = _predicate_matches(anchor.predicate, features)
            for ordinal, level in enumerate(anchor.parent_hierarchy):
                values = _parent_values(level, features)
                key = sha256_json([item.model_dump(mode="json") for item in values])
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
        raise V43PrevalenceError("prevalence stream interval count differs from manifest")
    horizon_duration = _duration_microseconds(
        manifest.utc_end_exclusive - manifest.utc_start
    )
    if total_duration_microseconds != horizon_duration:
        raise V43PrevalenceError("prevalence durations do not cover the declared UTC universe")
    policy = V43ConditionalPrevalencePolicyV1()
    source = V43PrevalenceSourceV1(
        cache_locator=lock.cache_locator,
        cache_manifest_sha256=verified.manifest_sha256,
        cache_trust_lock_sha256=trust_lock_sha256,
        cache_build_spec_sha256=lock.build_spec_sha256,
        build_plan_sha256=manifest.build_plan_sha256,
        reconciliation_aggregate_sha256=reconciliation_sha,
        exact_state_provenance_sha256=sha256_json(
            manifest.exact_state_provenance.model_dump(mode="json")
        ),
        logical_universe_sha256=manifest.logical_universe_sha256,
        feature_vector_schema_version=manifest.feature_vector_schema_version,
        semantic_feature_registry_sha256=manifest.semantic_feature_registry_sha256,
        feature_registry_sha256=manifest.feature_registry_sha256,
        engine_identity_sha256=sha256_json(manifest.engine.model_dump(mode="json")),
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
            total_duration_microseconds * V43_MINIMUM_EFFECTIVE_STATE_EQUIVALENTS
        ),
        minimum_cell_duration_denominator=row_count,
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


def _parent_values(
    level: V43PrevalenceParentLevelV1,
    features: Mapping[str, JsonValue],
) -> tuple[V43ParentValueV1, ...]:
    missing = sorted(set(level.parent_feature_ids) - set(features))
    if missing:
        raise V43PrevalenceError(f"prevalence row lacks parent features: {missing}")
    return tuple(
        V43ParentValueV1(feature_id=feature_id, value=features[feature_id])
        for feature_id in level.parent_feature_ids
    )


def _predicate_matches(
    predicate: V43FeaturePredicateV1,
    features: Mapping[str, JsonValue],
) -> bool:
    missing = sorted(set(predicate.required_feature_ids) - set(features))
    if missing:
        raise V43PrevalenceError(f"prevalence row lacks predicate features: {missing}")
    return all(_clause_matches(clause, features[clause.feature_id]) for clause in predicate.clauses)


def v4_3_predicate_matches(
    predicate: V43FeaturePredicateV1,
    features: Mapping[str, JsonValue],
) -> bool:
    """Evaluate one frozen predicate; missing/malformed M0-M2 data fails closed."""

    return _predicate_matches(predicate, features)


def _clause_matches(clause: V43FeatureClauseV1, actual: JsonValue) -> bool:
    if clause.operator is V43PredicateOperator.EQUALS:
        return actual == clause.expected
    if clause.operator is V43PredicateOperator.EQUALS_ANY:
        expected_values = cast(list[JsonValue], clause.expected)
        return actual in expected_values
    if clause.operator is V43PredicateOperator.PROFILE_HAS_LINE:
        if not isinstance(actual, str):
            raise V43PrevalenceError("profile-line predicate requires a profile string")
        parts = actual.split("/")
        if len(parts) != 2 or any(not part.isdigit() for part in parts):
            raise V43PrevalenceError("profile-line predicate received a malformed profile")
        return cast(int, clause.expected) in {int(part) for part in parts}
    if not isinstance(actual, list):
        raise V43PrevalenceError(
            f"prevalence operator {clause.operator.value} requires a JSON sequence"
        )
    if clause.operator is V43PredicateOperator.SEQUENCE_CONTAINS:
        return clause.expected in actual
    if clause.operator is V43PredicateOperator.SEQUENCE_CONTAINS_ANY:
        expected_values = cast(list[JsonValue], clause.expected)
        return any(item in actual for item in expected_values)
    if clause.operator is V43PredicateOperator.SEQUENCE_EXCLUDES:
        return clause.expected not in actual
    if clause.operator in {
        V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NUMERIC_GTE,
        V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NESTED_PREFIX,
    }:
        return _structured_record_clause_matches(clause, actual)
    expected = cast(dict[str, JsonValue], clause.expected)
    contains = any(
        isinstance(item, dict)
        and all(item.get(field) == value for field, value in expected.items())
        for item in actual
    )
    if clause.operator is V43PredicateOperator.SEQUENCE_CONTAINS_RECORD:
        return contains
    if clause.operator is V43PredicateOperator.SEQUENCE_EXCLUDES_RECORD:
        return not contains
    raise AssertionError(f"unsupported prevalence predicate operator: {clause.operator}")


def _structured_record_clause_matches(
    clause: V43FeatureClauseV1,
    actual: list[JsonValue],
) -> bool:
    expected = cast(dict[str, JsonValue], clause.expected)
    match = cast(dict[str, JsonValue], expected["match"])
    field = cast(str, expected["field"])
    for item in actual:
        if not isinstance(item, dict) or not all(
            item.get(key) == value for key, value in match.items()
        ):
            continue
        nested = item.get(field)
        if clause.operator is V43PredicateOperator.SEQUENCE_CONTAINS_RECORD_NUMERIC_GTE:
            minimum = cast(int, expected["minimum"])
            if isinstance(nested, bool) or not isinstance(nested, (int, float)):
                raise V43PrevalenceError(
                    "numeric record predicate matched a record with nonnumeric content"
                )
            return nested >= minimum
        prefix = cast(str, expected["prefix"])
        if not isinstance(nested, list) or any(
            not isinstance(value, str) for value in nested
        ):
            raise V43PrevalenceError(
                "nested-prefix predicate matched a record with a non-string sequence"
            )
        return any(cast(str, value).startswith(prefix) for value in nested)
    return False


def iter_artifact_cells(
    artifact: V43ConditionalPrevalenceArtifactV1,
) -> Iterator[V43PrevalenceCellV1]:
    """Yield canonical cells for transparent audit/reporting, never ranking."""

    for table in artifact.tables:
        yield from table.cells
