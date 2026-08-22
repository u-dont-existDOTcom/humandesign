from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.century_cache.chart_adapter import ExactStateBatchError
from hdmatch.century_cache.reconcile import OverlappingVerifiedExactStateBatch
from hdmatch.century_cache.staging import (
    CANONICAL_CENTURY_END_EXCLUSIVE_UTC,
    CANONICAL_CENTURY_START_UTC,
    StagedCenturyBuildError,
    SwissCalculationAuditV1,
    VerifiedStagedExactStateBatch,
    century_build_plan_sha256,
    create_canonical_century_build_plan,
    create_century_build_plan,
    load_century_build_plan,
    load_staged_exact_state_batch_receipt,
    staged_job_artifact_path,
    staged_job_receipt_path,
    staged_replay_verification_sha256,
    validate_verified_staged_exact_state_batch,
    verify_staged_exact_state_batch,
    write_century_build_plan_new,
    write_staged_exact_state_batch,
)
from hdmatch.chart.ephemeris import CelestialBody, SwissEphemerisProvider
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json
from hdmatch.provenance.swisseph_files import (
    PINNED_UPSTREAM_COMMIT,
    PINNED_UPSTREAM_REPOSITORY,
    VerifiedEphemerisFile,
    VerifiedEphemerisProvenance,
)

SOURCE_COMMIT = "c8f730296ca958e5796f865b84d29cb555ff7a2d"
ENGINE_RECEIPT_SHA256 = "1" * 64
PARITY_REPORT_SHA256 = "2" * 64
PARITY_REFERENCE_SHA256 = "3" * 64


class _AuditedFakeSwiss:
    FLG_JPLEPH = 1
    FLG_SWIEPH = 2
    FLG_MOSEPH = 4
    FLG_EPHMASK = 7
    FLG_SPEED = 256
    GREG_CAL = 1
    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9
    MEAN_NODE = 10
    TRUE_NODE = 11
    version = "deterministic-audited-fake"

    def __init__(
        self,
        planetary_file: Path,
        lunar_file: Path,
        *,
        fallback_on_call: int | None = None,
        speed_delta: float = 0.0,
    ) -> None:
        self.files = (planetary_file, lunar_file)
        self.fallback_on_call = fallback_on_call
        self.speed_delta = speed_delta
        self.call_count = 0

    def set_ephe_path(self, _path: str) -> None:
        pass

    def julday(
        self,
        year: int,
        month: int,
        day: int,
        hour: float,
        _calendar: int,
    ) -> float:
        midnight = datetime(year, month, day, tzinfo=UTC)
        return float(midnight.toordinal()) + hour / 24.0

    def calc_ut(
        self,
        julian_day: float,
        body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]:
        self.call_count += 1
        if body == self.SUN:
            longitude, speed = (julian_day + 261.4998) % 360.0, 1.0
        else:
            longitude, speed = (body * 17.0 + 0.01 * julian_day) % 360.0, 0.01
        returned_flags = flags
        if self.call_count == self.fallback_on_call:
            returned_flags = (flags & ~self.FLG_SWIEPH) | self.FLG_MOSEPH
        return (
            longitude,
            0.0,
            1.0,
            speed + self.speed_delta,
            0.0,
            0.0,
        ), returned_flags

    def get_current_file_data(self, index: int) -> tuple[str, float, float, int]:
        return str(self.files[index]), 0.0, 0.0, 441


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _provider_fixture(
    root: Path,
    *,
    fallback_on_call: int | None = None,
    speed_delta: float = 0.0,
) -> tuple[SwissEphemerisProvider, VerifiedEphemerisProvenance, _AuditedFakeSwiss]:
    ephemeris = root / "ephemeris"
    ephemeris.mkdir(parents=True)
    planetary = ephemeris / "sepl_18.se1"
    lunar = ephemeris / "semo_18.se1"
    planetary.write_bytes(b"staged-test-planetary")
    lunar.write_bytes(b"staged-test-lunar")
    files = (
        VerifiedEphemerisFile(
            name="sepl_18.se1",
            bytes=planetary.stat().st_size,
            sha256=_sha256(planetary),
        ),
        VerifiedEphemerisFile(
            name="semo_18.se1",
            bytes=lunar.stat().st_size,
            sha256=_sha256(lunar),
        ),
    )
    provenance = VerifiedEphemerisProvenance(
        source_repository=PINNED_UPSTREAM_REPOSITORY,
        source_commit=PINNED_UPSTREAM_COMMIT,
        source_manifest_sha256="4" * 64,
        files=files,
        ephemeris_file_set_sha256=sha256_json(
            [item.model_dump(mode="json") for item in files]
        ),
    )
    fake = _AuditedFakeSwiss(
        planetary,
        lunar,
        fallback_on_call=fallback_on_call,
        speed_delta=speed_delta,
    )
    provider = SwissEphemerisProvider(
        (planetary, lunar),
        _swe_module=fake,  # type: ignore[arg-type]
    )
    return provider, provenance, fake


def _plan(
    provider: SwissEphemerisProvider,
    provenance: VerifiedEphemerisProvenance,
    *,
    start: datetime | None = None,
    end: datetime | None = None,
):
    actual_start = datetime(2000, 1, 1, 12, tzinfo=UTC) if start is None else start
    actual_end = actual_start + timedelta(minutes=1) if end is None else end
    return create_century_build_plan(
        provider,
        provenance,
        utc_start=actual_start,
        utc_end_exclusive=actual_end,
        source_commit=SOURCE_COMMIT,
        source_tree_dirty=False,
        engine_validation_sha256=ENGINE_RECEIPT_SHA256,
        parity_report_sha256=PARITY_REPORT_SHA256,
        parity_reference_source_locator="tests/golden/frozen-swieph-reference.json",
        parity_reference_source_sha256=PARITY_REFERENCE_SHA256,
    )


def test_canonical_plan_has_deterministic_year_cores_and_derived_overlap(
    tmp_path: Path,
) -> None:
    provider, provenance, _ = _provider_fixture(tmp_path)
    first = create_canonical_century_build_plan(
        provider,
        provenance,
        source_commit=SOURCE_COMMIT,
        source_tree_dirty=False,
        engine_validation_sha256=ENGINE_RECEIPT_SHA256,
        parity_report_sha256=PARITY_REPORT_SHA256,
        parity_reference_source_locator="tests/golden/frozen-swieph-reference.json",
        parity_reference_source_sha256=PARITY_REFERENCE_SHA256,
    )
    second = create_canonical_century_build_plan(
        provider,
        provenance,
        source_commit=SOURCE_COMMIT,
        source_tree_dirty=False,
        engine_validation_sha256=ENGINE_RECEIPT_SHA256,
        parity_report_sha256=PARITY_REPORT_SHA256,
        parity_reference_source_locator="tests/golden/frozen-swieph-reference.json",
        parity_reference_source_sha256=PARITY_REFERENCE_SHA256,
    )

    assert first == second
    assert century_build_plan_sha256(first) == century_build_plan_sha256(second)
    assert first.utc_start == CANONICAL_CENTURY_START_UTC
    assert first.utc_end_exclusive == CANONICAL_CENTURY_END_EXCLUSIVE_UTC
    assert len(first.jobs) == 101
    assert first.overlap_scan_seconds == 90_001
    assert first.jobs[0].core_utc_start == CANONICAL_CENTURY_START_UTC
    assert first.jobs[0].core_utc_end_exclusive == datetime(1927, 1, 1, tzinfo=UTC)
    assert first.jobs[-1].core_utc_start == datetime(2026, 1, 1, tzinfo=UTC)
    assert first.jobs[-1].core_utc_end_exclusive == (
        CANONICAL_CENTURY_END_EXCLUSIVE_UTC
    )
    assert first.jobs[1].scan_utc_start < first.jobs[1].core_utc_start
    assert first.jobs[1].scan_utc_end_exclusive > first.jobs[1].core_utc_end_exclusive
    for previous, current in zip(first.jobs, first.jobs[1:], strict=False):
        assert previous.core_utc_end_exclusive == current.core_utc_start
        assert previous.scan_utc_end_exclusive > current.core_utc_start
        assert current.scan_utc_start < previous.core_utc_end_exclusive


def test_plan_rejects_naive_timestamps_and_dirty_source_tree(tmp_path: Path) -> None:
    provider, provenance, _ = _provider_fixture(tmp_path)
    with pytest.raises(StagedCenturyBuildError, match="timezone-aware"):
        _plan(provider, provenance, start=datetime(2000, 1, 1, 12))
    with pytest.raises(ValidationError, match="source_tree_dirty"):
        create_century_build_plan(
            provider,
            provenance,
            utc_start=datetime(2000, 1, 1, tzinfo=UTC),
            utc_end_exclusive=datetime(2000, 1, 2, tzinfo=UTC),
            source_commit=SOURCE_COMMIT,
            source_tree_dirty=True,  # type: ignore[arg-type]
            engine_validation_sha256=ENGINE_RECEIPT_SHA256,
            parity_report_sha256=PARITY_REPORT_SHA256,
            parity_reference_source_locator="frozen-reference.json",
            parity_reference_source_sha256=PARITY_REFERENCE_SHA256,
        )


def test_build_plan_persistence_is_canonical_immutable_and_fail_closed(
    tmp_path: Path,
) -> None:
    provider, provenance, _ = _provider_fixture(tmp_path / "provider")
    plan = _plan(provider, provenance)
    plan_path = tmp_path / "staging" / "century-build-plan.json"

    assert write_century_build_plan_new(plan_path, plan) == plan_path
    assert load_century_build_plan(plan_path) == plan
    with pytest.raises(FileExistsError):
        write_century_build_plan_new(plan_path, plan)

    plan_path.write_bytes(plan_path.read_bytes() + b"\n")
    with pytest.raises(StagedCenturyBuildError, match="not canonical JSON"):
        load_century_build_plan(plan_path)


def test_staged_job_is_receipt_last_and_requires_full_deterministic_replay(
    tmp_path: Path,
) -> None:
    provider, provenance, _ = _provider_fixture(tmp_path / "producer")
    plan = _plan(provider, provenance)
    job = plan.jobs[0]
    staging = tmp_path / "staging"
    created_at = datetime(2026, 8, 22, 1, 2, 3, tzinfo=UTC)

    receipt = write_staged_exact_state_batch(
        plan,
        job,
        provider,
        staging,
        created_at_utc=created_at,
    )

    artifact_path = staged_job_artifact_path(staging, job)
    receipt_path = staged_job_receipt_path(staging, job)
    assert artifact_path.is_file()
    assert receipt_path.is_file()
    assert load_staged_exact_state_batch_receipt(receipt_path) == receipt
    assert receipt.created_at_utc == created_at
    audit = receipt.swiss_calculation_audit
    assert audit.calculation_call_count > 0
    assert audit.requested_flags_counts == (
        (audit.requested_flags, audit.calculation_call_count),
    )
    assert audit.returned_mode_bits_counts == (
        (audit.swieph_flag, audit.calculation_call_count),
    )
    assert sum(item[1] for item in audit.calculated_body_counts) == (
        audit.calculation_call_count
    )
    assert sum(item[3] for item in audit.used_file_counts) == audit.calculation_call_count
    assert audit.entry_ephemeris_file_set_sha256 == (
        provenance.ephemeris_file_set_sha256
    )

    replay_provider, replay_provenance, _ = _provider_fixture(tmp_path / "replay")
    replay_plan = _plan(replay_provider, replay_provenance)
    verified = verify_staged_exact_state_batch(
        replay_plan,
        replay_plan.jobs[0],
        replay_provider,
        staging,
    )
    assert verified.batch.rows
    assert verified.producer_receipt == receipt
    assert verified.replay_verification.producer_receipt_sha256 == (
        verified.producer_receipt_sha256
    )
    assert verified.replay_verification_sha256 == staged_replay_verification_sha256(
        verified.replay_verification
    )
    assert verified.replay_verification.all_call_swieph_audit_match is True
    validate_verified_staged_exact_state_batch(verified)
    overlap_source = OverlappingVerifiedExactStateBatch.from_verified_staged_batch(
        verified
    )
    assert overlap_source.batch is verified.batch
    assert overlap_source.core_start_utc == receipt.core_utc_start
    assert overlap_source.core_end_exclusive == receipt.core_utc_end_exclusive
    assert overlap_source.source_build_plan_sha256 == receipt.plan_sha256
    with pytest.raises(
        StagedCenturyBuildError,
        match="must be minted by deterministic replay",
    ):
        VerifiedStagedExactStateBatch(
            batch=verified.batch,
            producer_receipt=verified.producer_receipt,
            producer_receipt_sha256=verified.producer_receipt_sha256,
            replay_verification=verified.replay_verification,
            replay_verification_sha256=verified.replay_verification_sha256,
            _factory_token=object(),
        )
    object.__setattr__(
        verified,
        "_producer_receipt_sha256",
        "0" * 64,
    )
    with pytest.raises(StagedCenturyBuildError, match="receipt hash binding changed"):
        validate_verified_staged_exact_state_batch(verified)


def test_replay_rejects_changed_artifact_bytes_before_scoring(tmp_path: Path) -> None:
    provider, provenance, _ = _provider_fixture(tmp_path / "producer")
    plan = _plan(provider, provenance)
    job = plan.jobs[0]
    staging = tmp_path / "staging"
    write_staged_exact_state_batch(plan, job, provider, staging)
    staged_job_artifact_path(staging, job).write_bytes(b"substituted")

    replay_provider, replay_provenance, _ = _provider_fixture(tmp_path / "replay")
    replay_plan = _plan(replay_provider, replay_provenance)
    with pytest.raises(StagedCenturyBuildError, match="artifact bytes changed"):
        verify_staged_exact_state_batch(
            replay_plan,
            replay_plan.jobs[0],
            replay_provider,
            staging,
        )


def test_replay_compares_full_all_call_audit_even_when_rows_are_unchanged(
    tmp_path: Path,
) -> None:
    provider, provenance, _ = _provider_fixture(tmp_path / "producer")
    plan = _plan(provider, provenance)
    job = plan.jobs[0]
    staging = tmp_path / "staging"
    receipt = write_staged_exact_state_batch(plan, job, provider, staging)
    payload = receipt.model_dump(mode="json")
    audit = dict(payload["swiss_calculation_audit"])
    audit["calculation_trace_sha256"] = "f" * 64
    payload["swiss_calculation_audit"] = audit
    receipt_path = staged_job_receipt_path(staging, job)
    receipt_path.write_bytes(canonical_json_bytes(payload))

    replay_provider, replay_provenance, _ = _provider_fixture(tmp_path / "replay")
    replay_plan = _plan(replay_provider, replay_provenance)
    with pytest.raises(StagedCenturyBuildError, match="all-call SWIEPH audit"):
        verify_staged_exact_state_batch(
            replay_plan,
            replay_plan.jobs[0],
            replay_provider,
            staging,
        )


def test_calculation_trace_binds_returned_longitude_and_speed(tmp_path: Path) -> None:
    first, _, _ = _provider_fixture(tmp_path / "first")
    second, _, _ = _provider_fixture(tmp_path / "second", speed_delta=1e-12)
    at_utc = datetime(2000, 1, 1, tzinfo=UTC)
    with first.capture_calculation_audit() as first_capture:
        first.position(CelestialBody.SUN, at_utc)
    with second.capture_calculation_audit() as second_capture:
        second.position(CelestialBody.SUN, at_utc)

    first_snapshot = first_capture.snapshot()
    second_snapshot = second_capture.snapshot()
    assert first_snapshot.calculation_trace_sha256 != (
        second_snapshot.calculation_trace_sha256
    )
    assert first_snapshot.calculated_body_counts == (("sun", 1),)
    assert first_snapshot.used_file_counts[0][0] == "sepl_18.se1"


def test_non_swieph_audit_cannot_claim_pass() -> None:
    with pytest.raises(ValidationError, match="non-SWIEPH"):
        SwissCalculationAuditV1(
            verification_status="pass",
            engine_identity_sha256="1" * 64,
            canonical_ephemeris_file_set_sha256="2" * 64,
            requested_flags=258,
            ephemeris_mask=7,
            swieph_flag=2,
            calculation_call_count=1,
            requested_flags_counts=((258, 1),),
            returned_flags_counts=((260, 1),),
            returned_mode_bits_counts=((4, 1),),
            calculated_body_counts=(("sun", 1),),
            used_file_counts=(("sepl_18.se1", "3" * 64, 1, 1),),
            calculation_trace_sha256="4" * 64,
            first_calculation_sha256="5" * 64,
            final_calculation_sha256="5" * 64,
            entry_provider_configuration_sha256="6" * 64,
            exit_provider_configuration_sha256="6" * 64,
            entry_ephemeris_file_set_sha256="2" * 64,
            exit_ephemeris_file_set_sha256="2" * 64,
        )


def test_early_middle_final_fallbacks_leave_no_passing_receipt(tmp_path: Path) -> None:
    baseline_provider, baseline_provenance, _ = _provider_fixture(tmp_path / "baseline")
    baseline_plan = _plan(baseline_provider, baseline_provenance)
    baseline_job = baseline_plan.jobs[0]
    baseline_receipt = write_staged_exact_state_batch(
        baseline_plan,
        baseline_job,
        baseline_provider,
        tmp_path / "baseline-staging",
    )
    total = baseline_receipt.swiss_calculation_audit.calculation_call_count
    assert total >= 3

    for label, fallback_call in (
        ("early", 1),
        ("middle", total // 2),
        ("final", total),
    ):
        provider, provenance, _ = _provider_fixture(
            tmp_path / label,
            fallback_on_call=fallback_call,
        )
        plan = _plan(provider, provenance)
        job = plan.jobs[0]
        staging = tmp_path / f"{label}-staging"
        with pytest.raises(ExactStateBatchError, match="requested SWIEPH"):
            write_staged_exact_state_batch(plan, job, provider, staging)
        assert not staged_job_artifact_path(staging, job).exists()
        assert not staged_job_receipt_path(staging, job).exists()
