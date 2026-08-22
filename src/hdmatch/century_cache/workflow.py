"""Explicit, resumable Phase-2 century-cache build workflow."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from hdmatch.chart.ephemeris import SwissEphemerisProvider
from hdmatch.chart.feature_registry import CACHEABLE_M0_M2_REGISTRY
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_file,
    write_new_bytes,
    write_new_canonical_json,
)
from hdmatch.experiments.manifest import git_revision
from hdmatch.provenance.swisseph_files import (
    REQUIRED_EPHEMERIS_FILES,
    VerifiedEphemerisProvenance,
    verify_ephemeris_directory,
)

from .construction import (
    CenturyCacheConstructionError,
    boundary_audit_from_reconciled_universe,
    century_cache_build_spec_from_plan,
    century_cache_stream_identity_from_plan,
    load_cache_engine_provenance,
)
from .evidence import CenturyCacheEvidenceInputs
from .models import CenturyCacheBuildSpec, VerifiedCenturyCache
from .parity import generate_swieph_golden_parity_report
from .publisher import CenturyCachePublicationError, StreamingCenturyCachePublisher
from .reconcile import (
    ExactStateReconciliationStream,
    OverlappingVerifiedExactStateBatch,
    canonical_reconciliation_aggregate_bytes,
    exact_state_reconciliation_aggregate_sha256,
)
from .staging import (
    CenturyBuildJobV1,
    CenturyBuildPlanV1,
    StagedExactStateBatchReceiptV1,
    century_build_plan_sha256,
    create_century_build_plan,
    load_century_build_plan,
    load_staged_exact_state_batch_receipt,
    staged_job_artifact_path,
    staged_job_receipt_path,
    verify_staged_exact_state_batch,
    write_century_build_plan_new,
    write_staged_exact_state_batch,
)
from .store import verify_century_cache_against_trust_lock
from .trust_lock import (
    CenturyCacheTrustLockV1,
    trust_lock_from_verified_cache,
    write_century_cache_trust_lock_new,
)

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


class CenturyCacheWorkflowError(RuntimeError):
    """The explicit cache workflow cannot safely advance or resume."""


@dataclass(frozen=True, slots=True)
class PreparedCenturyBuild:
    plan_path: Path
    plan_sha256: str
    parity_report_path: Path
    parity_report_sha256: str
    job_count: int


@dataclass(frozen=True, slots=True)
class PublishedCenturyBuild:
    verified_cache: VerifiedCenturyCache
    build_spec: CenturyCacheBuildSpec
    trust_lock: CenturyCacheTrustLockV1
    trust_lock_path: Path
    reconciliation_aggregate_path: Path
    boundary_audit_path: Path


def _provider_and_provenance(
    *,
    ephemeris_directory: str | Path,
    ephemeris_source_manifest_path: str | Path,
) -> tuple[SwissEphemerisProvider, VerifiedEphemerisProvenance]:
    directory = Path(ephemeris_directory)
    provenance = verify_ephemeris_directory(
        source_manifest_path=ephemeris_source_manifest_path,
        ephemeris_directory=directory,
    )
    provider = SwissEphemerisProvider(
        tuple(directory / name for name in REQUIRED_EPHEMERIS_FILES)
    )
    provider.verify_production_configuration()
    return provider, provenance


def _require_clean_source_commit(repository_root: Path) -> str:
    try:
        commit, dirty = git_revision(repository_root)
    except RuntimeError as exc:
        raise CenturyCacheWorkflowError("cannot identify the build source tree") from exc
    if dirty:
        raise CenturyCacheWorkflowError(
            "century-cache planning requires a clean committed source tree"
        )
    return commit


def _require_current_source_matches_plan(plan: CenturyBuildPlanV1) -> None:
    try:
        commit, dirty = git_revision(_REPOSITORY_ROOT)
    except RuntimeError as exc:
        raise CenturyCacheWorkflowError(
            "cannot verify the current source tree against the build plan"
        ) from exc
    if dirty or commit != plan.source_commit:
        raise CenturyCacheWorkflowError(
            "current clean source tree differs from the immutable build plan"
        )


def prepare_century_build(
    *,
    repository_root: str | Path,
    utc_start: datetime,
    utc_end_exclusive: datetime,
    ephemeris_directory: str | Path,
    ephemeris_source_manifest_path: str | Path,
    engine_validation_path: str | Path,
    golden_reference_path: str | Path,
    reference_source_locator: str,
    parity_report_path: str | Path,
    plan_path: str | Path,
) -> PreparedCenturyBuild:
    """Generate parity evidence and persist the immutable plan last."""

    root = Path(repository_root).resolve()
    parity_destination = Path(parity_report_path)
    plan_destination = Path(plan_path)
    if parity_destination.exists() or plan_destination.exists():
        raise FileExistsError("parity report or century build plan already exists")
    source_commit = _require_clean_source_commit(root)
    provider, provenance = _provider_and_provenance(
        ephemeris_directory=ephemeris_directory,
        ephemeris_source_manifest_path=ephemeris_source_manifest_path,
    )
    engine_validation_sha256 = sha256_file(engine_validation_path)
    parity = generate_swieph_golden_parity_report(
        provider,
        provenance,
        golden_reference_path=golden_reference_path,
        reference_source_locator=reference_source_locator,
        engine_validation_sha256=engine_validation_sha256,
        feature_vector_schema_version=(
            CACHEABLE_M0_M2_REGISTRY.feature_vector_schema_version
        ),
        utc_start=utc_start,
        utc_end_exclusive=utc_end_exclusive,
    )
    parity_output = write_new_canonical_json(parity_destination, parity)
    plan = create_century_build_plan(
        provider,
        provenance,
        utc_start=utc_start,
        utc_end_exclusive=utc_end_exclusive,
        source_commit=source_commit,
        source_tree_dirty=False,
        engine_validation_sha256=engine_validation_sha256,
        parity_report_sha256=sha256_file(parity_output),
        parity_reference_source_locator=reference_source_locator,
        parity_reference_source_sha256=sha256_file(golden_reference_path),
    )
    load_cache_engine_provenance(plan, engine_validation_path)
    if _require_clean_source_commit(root) != source_commit:
        raise CenturyCacheWorkflowError(
            "source commit changed while the build plan was being prepared"
        )
    output = write_century_build_plan_new(plan_destination, plan)
    return PreparedCenturyBuild(
        plan_path=output,
        plan_sha256=century_build_plan_sha256(plan),
        parity_report_path=parity_output,
        parity_report_sha256=sha256_file(parity_output),
        job_count=len(plan.jobs),
    )


def _job_by_id(plan: CenturyBuildPlanV1, job_id: str) -> CenturyBuildJobV1:
    matches = tuple(job for job in plan.jobs if job.job_id == job_id)
    if len(matches) != 1:
        raise CenturyCacheWorkflowError(f"unknown century build job: {job_id}")
    return matches[0]


def _retained_staged_receipt(
    plan: CenturyBuildPlanV1,
    job: CenturyBuildJobV1,
    staging_directory: Path,
) -> StagedExactStateBatchReceiptV1 | None:
    artifact_path = staged_job_artifact_path(staging_directory, job)
    receipt_path = staged_job_receipt_path(staging_directory, job)
    if not artifact_path.exists() and not receipt_path.exists():
        return None
    if not artifact_path.is_file() or not receipt_path.is_file():
        raise CenturyCacheWorkflowError(
            f"staged job {job.job_id} is partial and cannot be resumed"
        )
    receipt = load_staged_exact_state_batch_receipt(receipt_path)
    if receipt.plan_sha256 != century_build_plan_sha256(plan) or (
        receipt.job_id != job.job_id
    ):
        raise CenturyCacheWorkflowError(
            f"staged job {job.job_id} differs from the immutable plan"
        )
    if artifact_path.stat().st_size != receipt.artifact_size_bytes or (
        sha256_file(artifact_path) != receipt.artifact_sha256
    ):
        raise CenturyCacheWorkflowError(
            f"staged job {job.job_id} artifact bytes changed"
        )
    return receipt


def build_century_staged_job(
    *,
    plan_path: str | Path,
    job_id: str,
    staging_directory: str | Path,
    ephemeris_directory: str | Path,
    ephemeris_source_manifest_path: str | Path,
) -> StagedExactStateBatchReceiptV1:
    """Build one declared job, or retain an exact already-complete artifact."""

    plan = load_century_build_plan(plan_path)
    _require_current_source_matches_plan(plan)
    provider, provenance = _provider_and_provenance(
        ephemeris_directory=ephemeris_directory,
        ephemeris_source_manifest_path=ephemeris_source_manifest_path,
    )
    if provenance != plan.engine.ephemeris_provenance:
        raise CenturyCacheWorkflowError(
            "current ephemeris files differ from the immutable build plan"
        )
    job = _job_by_id(plan, job_id)
    return _build_or_retain_staged_job(
        plan=plan,
        job=job,
        provider=provider,
        staging_directory=Path(staging_directory),
    )


def _build_or_retain_staged_job(
    *,
    plan: CenturyBuildPlanV1,
    job: CenturyBuildJobV1,
    provider: SwissEphemerisProvider,
    staging_directory: Path,
) -> StagedExactStateBatchReceiptV1:
    retained = _retained_staged_receipt(plan, job, staging_directory)
    if retained is not None:
        return retained
    return write_staged_exact_state_batch(
        plan,
        job,
        provider,
        staging_directory,
    )


def build_all_missing_century_jobs(
    *,
    plan_path: str | Path,
    staging_directory: str | Path,
    ephemeris_directory: str | Path,
    ephemeris_source_manifest_path: str | Path,
) -> tuple[StagedExactStateBatchReceiptV1, ...]:
    """Sequential resumable convenience path; jobs remain independently runnable."""

    plan = load_century_build_plan(plan_path)
    _require_current_source_matches_plan(plan)
    provider, provenance = _provider_and_provenance(
        ephemeris_directory=ephemeris_directory,
        ephemeris_source_manifest_path=ephemeris_source_manifest_path,
    )
    if provenance != plan.engine.ephemeris_provenance:
        raise CenturyCacheWorkflowError(
            "current ephemeris files differ from the immutable build plan"
        )
    staging = Path(staging_directory)
    return tuple(
        _build_or_retain_staged_job(
            plan=plan,
            job=job,
            provider=provider,
            staging_directory=staging,
        )
        for job in plan.jobs
    )


def _write_or_require_identical(path: Path, raw: bytes) -> Path:
    if path.is_symlink():
        raise CenturyCacheWorkflowError("build evidence must not be a symbolic link")
    if path.exists():
        if not path.is_file() or path.read_bytes() != raw:
            raise CenturyCacheWorkflowError(
                f"existing build evidence differs: {path.name}"
            )
        return path
    return write_new_bytes(path, raw)


def assemble_and_publish_century_cache(
    *,
    plan_path: str | Path,
    staging_directory: str | Path,
    cache_directory: str | Path,
    cache_locator: str,
    trust_lock_path: str | Path,
    build_evidence_directory: str | Path,
    ephemeris_directory: str | Path,
    ephemeris_source_manifest_path: str | Path,
    engine_validation_path: str | Path,
    parity_report_path: str | Path,
    parity_reference_source_path: str | Path,
    created_at_utc: datetime | None = None,
) -> PublishedCenturyBuild:
    """Replay, reconcile, stream, publish manifest last, lock, and reverify."""

    plan = load_century_build_plan(plan_path)
    _require_current_source_matches_plan(plan)
    replay_provider, provenance = _provider_and_provenance(
        ephemeris_directory=ephemeris_directory,
        ephemeris_source_manifest_path=ephemeris_source_manifest_path,
    )
    if provenance != plan.engine.ephemeris_provenance:
        raise CenturyCacheWorkflowError(
            "current ephemeris files differ from the immutable build plan"
        )
    reconciliation_provider, reconciliation_provenance = _provider_and_provenance(
        ephemeris_directory=ephemeris_directory,
        ephemeris_source_manifest_path=ephemeris_source_manifest_path,
    )
    if reconciliation_provenance != plan.engine.ephemeris_provenance:
        raise CenturyCacheWorkflowError(
            "reconciliation ephemeris files differ from the immutable build plan"
        )
    engine = load_cache_engine_provenance(plan, engine_validation_path)
    identity = century_cache_stream_identity_from_plan(plan, engine=engine)
    publisher = StreamingCenturyCachePublisher(
        cache_directory,
        identity=identity,
        build_mode="explicit_rebuild",
    )
    published = False
    try:
        with ExactStateReconciliationStream(
            reconciliation_provider,
            engine_identity=plan.engine,
            root_tolerance_seconds=plan.design_root_time_tolerance_seconds,
        ) as reconciliation:
            for job in plan.jobs:
                verified_job = verify_staged_exact_state_batch(
                    plan,
                    job,
                    replay_provider,
                    staging_directory,
                )
                source = OverlappingVerifiedExactStateBatch.from_verified_staged_batch(
                    verified_job
                )
                chunk = reconciliation.append(source)
                if chunk is not None:
                    publisher.append_reconciled_chunk(chunk)
            finalization = reconciliation.finalize()

        aggregate = finalization.aggregate_provenance
        if aggregate.build_plan_sha256 != century_build_plan_sha256(plan):
            raise CenturyCacheWorkflowError(
                "reconciliation aggregate differs from the immutable build plan"
            )
        publisher.finish_reconciliation(finalization)
        evidence_directory = Path(build_evidence_directory)
        reconciliation_path = _write_or_require_identical(
            evidence_directory / "reconciliation-aggregate.json",
            canonical_reconciliation_aggregate_bytes(aggregate),
        )
        boundary = boundary_audit_from_reconciled_universe(
            plan,
            aggregate.exact_state_universe_provenance,
        )
        boundary_path = _write_or_require_identical(
            evidence_directory / "boundary-audit-report.json",
            canonical_json_bytes(boundary.model_dump(mode="json")),
        )
        spec = century_cache_build_spec_from_plan(
            plan,
            engine=engine,
            boundary_audit=boundary,
            reconciliation_aggregate_sha256=(
                exact_state_reconciliation_aggregate_sha256(aggregate)
            ),
            created_at_utc=created_at_utc or datetime.now(UTC),
        )
        verified = publisher.finalize_and_publish(
            spec=spec,
            evidence=CenturyCacheEvidenceInputs(
                engine_validation_path=Path(engine_validation_path),
                parity_report_path=Path(parity_report_path),
                boundary_audit_report_path=boundary_path,
                reconciliation_aggregate_path=reconciliation_path,
                parity_reference_source_path=Path(parity_reference_source_path),
                ephemeris_source_manifest_path=Path(
                    ephemeris_source_manifest_path
                ),
                ephemeris_directory=Path(ephemeris_directory),
            ),
        )
        published = True
        lock = trust_lock_from_verified_cache(
            verified,
            build_spec=spec,
            cache_locator=cache_locator,
        )
        lock_path = write_century_cache_trust_lock_new(trust_lock_path, lock)
        independently_verified = verify_century_cache_against_trust_lock(
            cache_directory,
            trust_lock_path=lock_path,
        )
        if independently_verified.manifest_sha256 != verified.manifest_sha256:
            raise CenturyCacheWorkflowError(
                "trust-lock re-verification changed the published manifest identity"
            )
        return PublishedCenturyBuild(
            verified_cache=independently_verified,
            build_spec=spec,
            trust_lock=lock,
            trust_lock_path=lock_path,
            reconciliation_aggregate_path=reconciliation_path,
            boundary_audit_path=boundary_path,
        )
    except (
        CenturyCacheConstructionError,
        CenturyCachePublicationError,
        OSError,
        RuntimeError,
        ValueError,
    ):
        if not published:
            with suppress(OSError, ValueError):
                publisher.abort()
        raise
