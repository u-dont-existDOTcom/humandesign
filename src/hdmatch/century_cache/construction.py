"""Fail-closed construction of cache identities and final evidence contracts."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.chart.feature_registry import CACHEABLE_M0_M2_REGISTRY
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_bytes, sha256_json

from .chart_adapter import CACHEABLE_M0_M2_FEATURE_COLUMNS
from .evidence import CenturyCacheBoundaryAuditReport, EngineValidationReceipt
from .models import (
    CenturyCacheBuildSpec,
    CenturyCacheEngineProvenance,
    CenturyCacheStreamIdentity,
    ExactStateUniverseProvenance,
)
from .staging import CenturyBuildPlanV1, century_build_plan_sha256


class CenturyCacheConstructionError(ValueError):
    """A persisted Phase-0/2 identity cannot authorize cache construction."""


def _load_canonical_engine_receipt(path: Path) -> tuple[bytes, EngineValidationReceipt]:
    if path.is_symlink():
        raise CenturyCacheConstructionError(
            "engine-validation receipt must not be a symbolic link"
        )
    try:
        raw = path.read_bytes()
        payload = json.loads(raw)
        if canonical_json_bytes(payload) != raw:
            raise ValueError("receipt is not canonical JSON")
        receipt = EngineValidationReceipt.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise CenturyCacheConstructionError(
            "invalid canonical engine-validation receipt"
        ) from exc
    return raw, receipt


def load_cache_engine_provenance(
    plan: CenturyBuildPlanV1,
    engine_validation_path: str | Path,
) -> CenturyCacheEngineProvenance:
    """Re-open Phase-0 evidence and bind it to the immutable build plan."""

    checked_plan = CenturyBuildPlanV1.model_validate(
        plan.model_dump(mode="python"), strict=True
    )
    raw, receipt = _load_canonical_engine_receipt(Path(engine_validation_path))
    receipt_sha256 = sha256_bytes(raw)
    if receipt_sha256 != checked_plan.engine_validation_sha256:
        raise CenturyCacheConstructionError(
            "engine-validation receipt SHA-256 differs from the build plan"
        )
    if receipt.ephemeris_provenance != checked_plan.engine.ephemeris_provenance:
        raise CenturyCacheConstructionError(
            "engine-validation ephemeris provenance differs from the build plan"
        )
    validation = receipt.engine_validation
    expected = {
        "provider": (validation.provider, checked_plan.engine.provider),
        "Swiss library": (
            validation.library_version,
            checked_plan.engine.swiss_library_version,
        ),
        "requested flags": (
            validation.requested_flags,
            checked_plan.engine.requested_flags,
        ),
        "ephemeris mask": (
            validation.ephemeris_mask,
            checked_plan.engine.ephemeris_mask,
        ),
        "node convention": (validation.node_convention, checked_plan.engine.node_convention),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise CenturyCacheConstructionError(
                f"engine-validation {label} differs from the build plan"
            )
    if validation.ephemeris_requested != "SWIEPH" or (
        validation.ephemeris_returned != "SWIEPH"
    ):
        raise CenturyCacheConstructionError(
            "engine-validation receipt does not prove returned SWIEPH"
        )
    observed_flags = tuple(
        sorted({probe.returned_flags for probe in validation.calculation_probes})
    )
    provenance = CenturyCacheEngineProvenance(
        provider=checked_plan.engine.provider,
        chart_engine_version=checked_plan.chart_engine_version,
        swiss_library_version=checked_plan.engine.swiss_library_version,
        engine_validation_sha256=receipt_sha256,
        ephemeris_provenance=checked_plan.engine.ephemeris_provenance,
        ephemeris_requested="SWIEPH",
        ephemeris_returned="SWIEPH",
        requested_flags=checked_plan.engine.requested_flags,
        returned_flags_observed=observed_flags,
        ephemeris_mask=checked_plan.engine.ephemeris_mask,
        swieph_flag=checked_plan.engine.swieph_flag,
    )
    return provenance


def century_cache_stream_identity_from_plan(
    plan: CenturyBuildPlanV1,
    *,
    engine: CenturyCacheEngineProvenance,
) -> CenturyCacheStreamIdentity:
    """Construct every pre-stream row/storage identity from frozen plan bytes."""

    checked_plan = CenturyBuildPlanV1.model_validate(
        plan.model_dump(mode="python"), strict=True
    )
    if engine.engine_validation_sha256 != checked_plan.engine_validation_sha256 or (
        engine.ephemeris_provenance != checked_plan.engine.ephemeris_provenance
    ):
        raise CenturyCacheConstructionError(
            "cache engine provenance differs from the immutable build plan"
        )
    return CenturyCacheStreamIdentity(
        feature_vector_schema_version=(
            CACHEABLE_M0_M2_REGISTRY.feature_vector_schema_version
        ),
        utc_start=checked_plan.utc_start,
        utc_end_exclusive=checked_plan.utc_end_exclusive,
        feature_registry=CACHEABLE_M0_M2_FEATURE_COLUMNS,
        semantic_feature_registry_sha256=(
            checked_plan.semantic_feature_registry_sha256
        ),
        feature_registry_sha256=checked_plan.physical_feature_registry_sha256,
        required_feature_coverage=1.0,
        calculation_tier="M2",
        exact_intervals=True,
        build_plan_sha256=century_build_plan_sha256(checked_plan),
        engine=engine,
        node_convention="true",
        mandala_mapping_version=checked_plan.mandala_mapping_version,
        mandala_mapping_sha256=checked_plan.mandala_mapping_sha256,
        bodygraph_mapping_sha256=checked_plan.bodygraph_mapping_sha256,
        boundary_policy_version=checked_plan.boundary_policy_version,
        design_root_time_tolerance_seconds=(
            checked_plan.design_root_time_tolerance_seconds
        ),
        design_root_arc_tolerance_degrees=(
            checked_plan.design_root_arc_tolerance_degrees
        ),
        generation_commit=checked_plan.source_commit,
    )


def boundary_audit_from_reconciled_universe(
    plan: CenturyBuildPlanV1,
    exact: ExactStateUniverseProvenance,
) -> CenturyCacheBoundaryAuditReport:
    """Mint the final zero-defect boundary report from reconciler provenance."""

    checked_plan = CenturyBuildPlanV1.model_validate(
        plan.model_dump(mode="python"), strict=True
    )
    expected = {
        "UTC start": (exact.utc_start, checked_plan.utc_start),
        "UTC end": (exact.utc_end_exclusive, checked_plan.utc_end_exclusive),
        "boundary policy": (
            exact.boundary_policy_version,
            checked_plan.boundary_policy_version,
        ),
        "semantic registry": (
            exact.semantic_feature_registry_sha256,
            checked_plan.semantic_feature_registry_sha256,
        ),
        "physical registry": (
            exact.feature_registry_sha256,
            checked_plan.physical_feature_registry_sha256,
        ),
        "chart engine": (exact.chart_engine_version, checked_plan.chart_engine_version),
        "ephemeris file set": (
            exact.ephemeris_file_set_sha256,
            checked_plan.engine.canonical_ephemeris_file_set_sha256,
        ),
        "Mandala version": (
            exact.mandala_mapping_version,
            checked_plan.mandala_mapping_version,
        ),
        "Mandala mapping": (
            exact.mandala_mapping_sha256,
            checked_plan.mandala_mapping_sha256,
        ),
        "Bodygraph mapping": (
            exact.bodygraph_mapping_sha256,
            checked_plan.bodygraph_mapping_sha256,
        ),
        "Design-root time tolerance": (
            exact.design_root_time_tolerance_seconds,
            checked_plan.design_root_time_tolerance_seconds,
        ),
        "Design-root arc tolerance": (
            exact.design_root_arc_tolerance_degrees,
            checked_plan.design_root_arc_tolerance_degrees,
        ),
    }
    for label, (actual, required) in expected.items():
        if actual != required:
            raise CenturyCacheConstructionError(
                f"reconciled universe {label} differs from the build plan"
            )
    return CenturyCacheBoundaryAuditReport(
        schema_version="century-cache-boundary-audit-report-v1",
        validation_status="pass",
        engine_validation_sha256=checked_plan.engine_validation_sha256,
        logical_universe_sha256=exact.logical_universe_sha256,
        semantic_feature_registry_sha256=exact.semantic_feature_registry_sha256,
        feature_registry_sha256=exact.feature_registry_sha256,
        mandala_mapping_sha256=exact.mandala_mapping_sha256,
        bodygraph_mapping_sha256=exact.bodygraph_mapping_sha256,
        boundary_policy_version=exact.boundary_policy_version,
        design_root_time_tolerance_seconds=exact.design_root_time_tolerance_seconds,
        design_root_arc_tolerance_degrees=exact.design_root_arc_tolerance_degrees,
        utc_start=exact.utc_start,
        utc_end_exclusive=exact.utc_end_exclusive,
        interval_count=exact.interval_count,
        audited_boundary_event_count=exact.boundary_event_count,
        missing_boundary_count=0,
        gap_count=0,
        overlap_count=0,
        maximality_violation_count=0,
    )


def century_cache_build_spec_from_plan(
    plan: CenturyBuildPlanV1,
    *,
    engine: CenturyCacheEngineProvenance,
    boundary_audit: CenturyCacheBoundaryAuditReport,
    reconciliation_aggregate_sha256: str,
    created_at_utc: datetime,
) -> CenturyCacheBuildSpec:
    """Finalize the manifest contract without reopening or changing plan inputs."""

    identity = century_cache_stream_identity_from_plan(plan, engine=engine)
    if boundary_audit.engine_validation_sha256 != plan.engine_validation_sha256 or (
        boundary_audit.utc_start != plan.utc_start
        or boundary_audit.utc_end_exclusive != plan.utc_end_exclusive
    ):
        raise CenturyCacheConstructionError(
            "boundary audit differs from the immutable build plan"
        )
    if len(reconciliation_aggregate_sha256) != 64 or any(
        character not in "0123456789abcdef"
        for character in reconciliation_aggregate_sha256
    ):
        raise CenturyCacheConstructionError(
            "reconciliation aggregate SHA-256 is invalid"
        )
    if created_at_utc.tzinfo is None or created_at_utc.utcoffset() is None:
        raise CenturyCacheConstructionError(
            "cache creation timestamp must be timezone-aware"
        )
    return CenturyCacheBuildSpec(
        **identity.model_dump(mode="python", exclude={"schema_version"}),
        parity_status="pass",
        parity_report_sha256=plan.parity_report_sha256,
        parity_reference_source_locator=plan.parity_reference_source_locator,
        parity_reference_source_sha256=plan.parity_reference_source_sha256,
        boundary_audit_status="pass",
        boundary_audit_report_sha256=sha256_json(
            boundary_audit.model_dump(mode="json")
        ),
        reconciliation_aggregate_sha256=reconciliation_aggregate_sha256,
        created_at_utc=created_at_utc.astimezone(UTC),
    )
