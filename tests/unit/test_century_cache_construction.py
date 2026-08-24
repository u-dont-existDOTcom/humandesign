from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.century_cache import (
    CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256,
    CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256,
    assemble_verified_exact_shard_set,
    build_verified_exact_state_batch,
    century_build_plan_sha256,
    create_century_build_plan,
)
from hdmatch.century_cache.construction import (
    CenturyCacheConstructionError,
    boundary_audit_from_reconciled_universe,
    century_cache_build_spec_from_plan,
    century_cache_stream_identity_from_plan,
    load_cache_engine_provenance,
)
from hdmatch.chart.ephemeris import SwissEphemerisProvider
from hdmatch.experiments.canonical import sha256_file
from hdmatch.provenance import verify_ephemeris_directory

_ROOT = Path(__file__).resolve().parents[2]
_EPHEMERIS = _ROOT / "data" / "ephemeris"
_ENGINE_RECEIPT = _ROOT / "reports" / "v4_3_migration" / "phase0_engine_validation.json"
_REFERENCE = _ROOT / "tests" / "golden" / "fixtures" / "swieph_phase0_golden_v1.json"


def _plan_and_provider():
    verified = verify_ephemeris_directory(
        source_manifest_path=_EPHEMERIS / "manifest.json",
        ephemeris_directory=_EPHEMERIS,
    )
    provider = SwissEphemerisProvider(
        (_EPHEMERIS / "sepl_18.se1", _EPHEMERIS / "semo_18.se1")
    )
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    plan = create_century_build_plan(
        provider,
        verified,
        utc_start=start,
        utc_end_exclusive=start + timedelta(minutes=1),
        source_commit="8" * 40,
        source_tree_dirty=False,
        engine_validation_sha256=sha256_file(_ENGINE_RECEIPT),
        parity_report_sha256="2" * 64,
        parity_reference_source_locator=(
            "tests/golden/fixtures/swieph_phase0_golden_v1.json"
        ),
        parity_reference_source_sha256=sha256_file(_REFERENCE),
    )
    return plan, provider


def test_plan_constructs_engine_stream_boundary_and_final_spec() -> None:
    plan, provider = _plan_and_provider()
    engine = load_cache_engine_provenance(plan, _ENGINE_RECEIPT)
    identity = century_cache_stream_identity_from_plan(plan, engine=engine)

    assert identity.build_plan_sha256 == century_build_plan_sha256(plan)
    assert identity.semantic_feature_registry_sha256 == (
        CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256
    )
    assert identity.feature_registry_sha256 == (
        CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256
    )
    assert identity.engine.ephemeris_requested == "SWIEPH"
    assert identity.engine.ephemeris_returned == "SWIEPH"

    batch = build_verified_exact_state_batch(
        provider,
        plan.utc_start,
        plan.utc_end_exclusive,
    )
    exact = assemble_verified_exact_shard_set((batch,)).provenance
    boundary = boundary_audit_from_reconciled_universe(plan, exact)
    spec = century_cache_build_spec_from_plan(
        plan,
        engine=engine,
        boundary_audit=boundary,
        reconciliation_aggregate_sha256="3" * 64,
        created_at_utc=datetime(2026, 8, 22, 12, tzinfo=UTC),
    )

    assert spec.build_plan_sha256 == century_build_plan_sha256(plan)
    assert spec.boundary_audit_report_sha256
    assert spec.reconciliation_aggregate_sha256 == "3" * 64
    assert spec.generation_commit == plan.source_commit


def test_engine_receipt_hash_must_match_immutable_plan() -> None:
    plan, _provider = _plan_and_provider()
    changed = plan.model_copy(update={"engine_validation_sha256": "9" * 64})

    with pytest.raises(
        CenturyCacheConstructionError,
        match="SHA-256 differs from the build plan",
    ):
        load_cache_engine_provenance(changed, _ENGINE_RECEIPT)


def test_build_spec_rejects_invalid_reconciliation_hash() -> None:
    plan, _provider = _plan_and_provider()
    engine = load_cache_engine_provenance(plan, _ENGINE_RECEIPT)
    boundary = boundary_audit_from_reconciled_universe(
        plan,
        assemble_verified_exact_shard_set(
            (
                build_verified_exact_state_batch(
                    _provider,
                    plan.utc_start,
                    plan.utc_end_exclusive,
                ),
            )
        ).provenance,
    )

    with pytest.raises(CenturyCacheConstructionError, match="SHA-256 is invalid"):
        century_cache_build_spec_from_plan(
            plan,
            engine=engine,
            boundary_audit=boundary,
            reconciliation_aggregate_sha256="not-a-hash",
            created_at_utc=datetime(2026, 8, 22, tzinfo=UTC),
        )
