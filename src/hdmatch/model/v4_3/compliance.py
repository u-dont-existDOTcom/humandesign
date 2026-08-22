"""Fail-closed V4.3 compliance assessment independent of cache implementations."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from hdmatch.model.v4_3.contracts import (
    INDEPENDENT_CORROBORATION_CAP,
    MAPPING_LIBRARY_V2_SCHEMA,
    V43_PROTOCOL_VERSION,
    V43_RANKING_POLICY_VERSION,
    V43_SCORING_ENGINE_VERSION,
)

COMPLIANT_STATUS: Literal["compliant"] = "compliant"
NONCOMPLIANT_STATUS: Literal["partial/non-compliant"] = "partial/non-compliant"


class V43ComplianceError(RuntimeError):
    """Raised when a caller requires, but cannot prove, canonical V4.3."""


@dataclass(frozen=True, slots=True)
class V43ComplianceEvidence:
    """Explicit evidence flags; defaults are deliberately absent.

    This is an adapter boundary, not a substitute for verifying the underlying
    cache, ephemeris, prevalence, and mapping artifacts in their owning modules.
    """

    declared_model_version: str
    reduced_model_label: str
    calculation_tier: str
    scoring_tier: str
    mapping_schema_version: str
    required_feature_ids: frozenset[str]
    available_feature_ids: frozenset[str]
    exact_interval_source_verified: bool
    cache_verified: bool
    astronomy_provenance_verified: bool
    ephemeris_requested: str
    ephemeris_returned: str
    flexibility_penalty_enabled: bool
    conditional_prevalence_enabled: bool
    duration_weighted_prevalence_enabled: bool
    prevalence_source_scope: str
    dependency_control_enabled: bool
    corroboration_cap: float
    full_declared_universe_rescored: bool
    scoring_engine_version: str
    ranking_policy_version: str

    def __post_init__(self) -> None:
        if not self.declared_model_version:
            raise ValueError("declared model version must not be empty")
        if not self.reduced_model_label or self.reduced_model_label == V43_PROTOCOL_VERSION:
            raise ValueError("a distinct honest reduced-model label is required")
        if not math.isfinite(self.corroboration_cap) or self.corroboration_cap < 0.0:
            raise ValueError("corroboration cap must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class V43Compliance:
    protocol_version: Literal["V4.3"]
    reported_model_version: str
    status: Literal["compliant", "partial/non-compliant"]
    calculation_tier: str
    scoring_tier: str
    required_feature_count: int
    available_required_feature_count: int
    required_feature_coverage: float
    missing_required_feature_ids: tuple[str, ...]
    simplified: bool
    cache_verified: bool
    ephemeris_requested: str
    ephemeris_returned: str
    flexibility_penalty_enabled: bool
    conditional_prevalence_enabled: bool
    v4_3_compliant: bool
    failure_reasons: tuple[str, ...]


def assess_v4_3_compliance(evidence: V43ComplianceEvidence) -> V43Compliance:
    """Assess all canonical invariants and downgrade incomplete declarations."""

    missing_features = tuple(
        sorted(evidence.required_feature_ids - evidence.available_feature_ids)
    )
    required_count = len(evidence.required_feature_ids)
    available_count = required_count - len(missing_features)
    coverage = available_count / required_count if required_count else 0.0

    failures: list[str] = []
    _require_equal(failures, "declared model version", evidence.declared_model_version, "V4.3")
    _require_equal(failures, "calculation tier", evidence.calculation_tier, "M2")
    _require_equal(failures, "scoring tier", evidence.scoring_tier, "M2")
    _require_equal(
        failures,
        "mapping schema",
        evidence.mapping_schema_version,
        MAPPING_LIBRARY_V2_SCHEMA,
    )
    if required_count == 0:
        failures.append("required feature registry is empty")
    if missing_features:
        failures.append(f"missing required features: {', '.join(missing_features)}")
    _require_true(
        failures,
        "exact interval source is unverified",
        evidence.exact_interval_source_verified,
    )
    _require_true(failures, "century cache is unverified", evidence.cache_verified)
    _require_true(
        failures,
        "astronomy provenance is unverified",
        evidence.astronomy_provenance_verified,
    )
    _require_equal(failures, "requested ephemeris mode", evidence.ephemeris_requested, "SWIEPH")
    _require_equal(failures, "returned ephemeris mode", evidence.ephemeris_returned, "SWIEPH")
    _require_true(
        failures,
        "flexibility penalty is disabled",
        evidence.flexibility_penalty_enabled,
    )
    _require_true(
        failures,
        "conditional prevalence is disabled",
        evidence.conditional_prevalence_enabled,
    )
    _require_true(
        failures,
        "duration-weighted prevalence is disabled",
        evidence.duration_weighted_prevalence_enabled,
    )
    _require_equal(
        failures,
        "prevalence source scope",
        evidence.prevalence_source_scope,
        "declared-global-utc-universe",
    )
    _require_true(failures, "dependency control is disabled", evidence.dependency_control_enabled)
    if evidence.corroboration_cap != INDEPENDENT_CORROBORATION_CAP:
        failures.append("independent corroboration cap is not exactly 0.15")
    _require_true(
        failures,
        "complete declared universe was not rescored",
        evidence.full_declared_universe_rescored,
    )
    _require_equal(
        failures,
        "scoring engine version",
        evidence.scoring_engine_version,
        V43_SCORING_ENGINE_VERSION,
    )
    _require_equal(
        failures,
        "ranking policy version",
        evidence.ranking_policy_version,
        V43_RANKING_POLICY_VERSION,
    )

    compliant = not failures
    reported_model_version = (
        V43_PROTOCOL_VERSION if compliant else evidence.reduced_model_label
    )
    return V43Compliance(
        protocol_version="V4.3",
        reported_model_version=reported_model_version,
        status=COMPLIANT_STATUS if compliant else NONCOMPLIANT_STATUS,
        calculation_tier=evidence.calculation_tier,
        scoring_tier=evidence.scoring_tier,
        required_feature_count=required_count,
        available_required_feature_count=available_count,
        required_feature_coverage=coverage,
        missing_required_feature_ids=missing_features,
        simplified=evidence.calculation_tier != "M2" or evidence.scoring_tier != "M2",
        cache_verified=evidence.cache_verified,
        ephemeris_requested=evidence.ephemeris_requested,
        ephemeris_returned=evidence.ephemeris_returned,
        flexibility_penalty_enabled=evidence.flexibility_penalty_enabled,
        conditional_prevalence_enabled=evidence.conditional_prevalence_enabled,
        v4_3_compliant=compliant,
        failure_reasons=tuple(failures),
    )


def require_v4_3_compliance(evidence: V43ComplianceEvidence) -> V43Compliance:
    """Return a compliant object or fail before any canonical V4.3 claim."""

    compliance = assess_v4_3_compliance(evidence)
    if not compliance.v4_3_compliant:
        details = "; ".join(compliance.failure_reasons)
        raise V43ComplianceError(f"canonical V4.3 compliance failed: {details}")
    return compliance


def _require_true(failures: list[str], message: str, value: bool) -> None:
    if value is not True:
        failures.append(message)


def _require_equal(failures: list[str], label: str, actual: str, expected: str) -> None:
    if actual != expected:
        failures.append(f"{label} must be {expected}, got {actual or '<empty>'}")
