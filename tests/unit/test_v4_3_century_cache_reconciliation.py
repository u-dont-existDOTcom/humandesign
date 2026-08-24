from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from hdmatch.century_cache import (
    CenturyStateRecord,
    ExactStateBatchError,
    ExactStateBatchProvenance,
    ExactStateReconciliationError,
    ExactStateReconciliationStream,
    OverlappingVerifiedExactStateBatch,
    ReconciliationStreamFinalization,
    SwissEngineBuildIdentityV1,
    assemble_verified_exact_shard_set,
    build_verified_exact_state_batch,
    canonical_reconciliation_aggregate_bytes,
    canonical_rows_sha256,
    chart_adapter,
    discrete_chart_identity_sha256,
    exact_state_reconciliation_aggregate_sha256,
    reconcile,
    validate_exact_state_reconciliation_aggregate_provenance,
    validate_reconciled_exact_state_chunk,
    validate_reconciliation_stream_finalization,
    validate_verified_exact_shard_set,
)
from hdmatch.chart.calculator import calculate_chart
from hdmatch.chart.ephemeris import CelestialBody, SwissEphemerisProvider
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json
from hdmatch.provenance.swisseph_files import (
    PINNED_UPSTREAM_COMMIT,
    PINNED_UPSTREAM_REPOSITORY,
    EphemerisFilePin,
    EphemerisSourceManifest,
    verify_ephemeris_directory,
)


class _DeterministicFakeSwiss:
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
    version = "deterministic-reconciliation-fake"

    def __init__(self, planetary_file: Path, lunar_file: Path) -> None:
        self.files = (planetary_file, lunar_file)

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
        if body == self.SUN:
            longitude, speed = (julian_day + 261.4998) % 360.0, 1.0
        else:
            longitude, speed = (body * 17.0 + 0.01 * julian_day) % 360.0, 0.01
        return (longitude, 0.0, 1.0, speed, 0.0, 0.0), flags

    def get_current_file_data(self, index: int) -> tuple[str, float, float, int]:
        return str(self.files[index]), 0.0, 0.0, 441


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _provider(
    root: Path,
) -> tuple[SwissEphemerisProvider, SwissEngineBuildIdentityV1]:
    ephemeris = root / "ephemeris"
    ephemeris.mkdir()
    planetary = ephemeris / "sepl_18.se1"
    lunar = ephemeris / "semo_18.se1"
    planetary.write_bytes(b"reconciliation-planetary-test-file")
    lunar.write_bytes(b"reconciliation-lunar-test-file")
    pins = tuple(
        EphemerisFilePin(
            name=path.name,
            bytes=path.stat().st_size,
            sha256=_sha256_file(path),
        )
        for path in (planetary, lunar)
    )
    manifest = EphemerisSourceManifest(
        schema_version="ephemeris-file-manifest-v1",
        provider="Swiss Ephemeris",
        upstream_repository=PINNED_UPSTREAM_REPOSITORY,
        upstream_commit=PINNED_UPSTREAM_COMMIT,
        files=pins,
        tested_range="reconciliation unit fixture only",
        license="test fixture",
    )
    manifest_path = root / "manifest.json"
    manifest_path.write_bytes(canonical_json_bytes(manifest.model_dump(mode="json")))
    verified = verify_ephemeris_directory(
        source_manifest_path=manifest_path,
        ephemeris_directory=ephemeris,
    )
    provider = SwissEphemerisProvider(
        (planetary, lunar),
        _swe_module=_DeterministicFakeSwiss(planetary, lunar),  # type: ignore[arg-type]
    )
    configuration_sha256, file_set_sha256 = provider.calculation_audit_identity_hashes()
    metadata = provider.metadata
    assert metadata.requested_flags is not None
    assert metadata.ephemeris_mask is not None
    return provider, SwissEngineBuildIdentityV1(
        provider="swiss_ephemeris_local_files",
        swiss_library_version=metadata.library_version,
        requested_flags=metadata.requested_flags,
        ephemeris_mask=metadata.ephemeris_mask,
        swieph_flag=_DeterministicFakeSwiss.FLG_SWIEPH,
        node_convention="true",
        provider_configuration_sha256=configuration_sha256,
        canonical_ephemeris_file_set_sha256=file_set_sha256,
        ephemeris_provenance=verified,
    )


def _identity_hash(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _source(
    batch: object,
    start: datetime,
    end: datetime,
    ordinal: int,
    *,
    build_plan: str = "shared-build-plan",
) -> OverlappingVerifiedExactStateBatch:
    from hdmatch.century_cache import VerifiedExactStateBatch

    assert isinstance(batch, VerifiedExactStateBatch)
    return OverlappingVerifiedExactStateBatch._from_factory_verified_batch_for_test(
        batch=batch,
        core_start_utc=start,
        core_end_exclusive=end,
        source_staged_receipt_sha256=_identity_hash(f"receipt-{ordinal}"),
        source_replay_verification_sha256=_identity_hash(f"replay-{ordinal}"),
        source_all_call_audit_sha256=_identity_hash(f"audit-{ordinal}"),
        source_build_plan_sha256=_identity_hash(build_plan),
    )


def _stream(
    provider: SwissEphemerisProvider,
    engine_identity: SwissEngineBuildIdentityV1,
) -> ExactStateReconciliationStream:
    return ExactStateReconciliationStream._for_factory_verified_test_sources(
        provider,
        engine_identity=engine_identity,
    )


def test_equal_state_artificial_cut_is_merged_with_canonical_midpoint(
    tmp_path: Path,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    cut = start + timedelta(seconds=4)
    end = start + timedelta(seconds=8)
    left = build_verified_exact_state_batch(provider, start, cut + timedelta(seconds=2))
    right = build_verified_exact_state_batch(provider, cut - timedelta(seconds=2), end)

    stream = _stream(provider, engine_identity)
    assert stream.append(_source(left, start, cut, 0)) is None
    assert stream.append(_source(right, cut, end, 1)) is None
    finalization = stream.finalize()
    final_batch = finalization.final_chunk.batch
    validate_reconciled_exact_state_chunk(finalization.final_chunk)

    assert len(final_batch.rows) == 1
    row = final_batch.rows[0]
    assert (row.utc_start, row.utc_end) == (start, end)
    assert row.representative_utc == start + (end - start) / 2
    assert row.design_timestamp == calculate_chart(provider, row.representative_utc).design_utc
    assert cut not in (row.utc_start, row.utc_end)
    assert cut - timedelta(seconds=2) not in (row.utc_start, row.utc_end)
    assert cut + timedelta(seconds=2) not in (row.utc_start, row.utc_end)
    aggregate = finalization.aggregate_provenance
    assert aggregate.exact_state_universe_provenance.interval_count == 1
    assert aggregate.exact_state_universe_provenance.canonical_rows_sha256 == (
        canonical_rows_sha256(final_batch.rows)
    )
    assert aggregate.ordered_source_staged_receipt_sha256s == (
        _identity_hash("receipt-0"),
        _identity_hash("receipt-1"),
    )
    assert aggregate.reconciliation_calculation_audit.calculation_call_count > 0
    assert aggregate.reconciliation_calculation_audit_sha256 == sha256_json(
        aggregate.reconciliation_calculation_audit.model_dump(mode="json")
    )
    assert canonical_reconciliation_aggregate_bytes(aggregate).startswith(b'{"')
    assert exact_state_reconciliation_aggregate_sha256(aggregate) == hashlib.sha256(
        canonical_reconciliation_aggregate_bytes(aggregate)
    ).hexdigest()
    validate_exact_state_reconciliation_aggregate_provenance(aggregate)
    validate_reconciliation_stream_finalization(finalization)
    tampered = aggregate.model_copy(
        update={"boundary_event_catalog_sha256": _identity_hash("stale-catalog")}
    )
    with pytest.raises(
        ExactStateReconciliationError,
        match="event catalog is stale",
    ):
        validate_exact_state_reconciliation_aggregate_provenance(tampered)
    mixed_plan_aggregate = aggregate.model_copy(
        update={"build_plan_sha256": _identity_hash("different-plan")}
    )
    with pytest.raises(
        ExactStateReconciliationError,
        match="sources mix build plans",
    ):
        validate_exact_state_reconciliation_aggregate_provenance(
            mixed_plan_aggregate
        )
    with pytest.raises(
        ExactStateReconciliationError,
        match="must be minted by the stream",
    ):
        ReconciliationStreamFinalization(
            final_chunk=finalization.final_chunk,
            aggregate_provenance=aggregate,
            _factory_token=object(),
        )
    object.__setattr__(finalization, "_factory_token", object())
    with pytest.raises(
        ExactStateReconciliationError,
        match="lacks the reconciliation stream factory token",
    ):
        validate_reconciliation_stream_finalization(finalization)


def test_true_boundary_on_core_cut_survives_once_and_chunks_are_writer_adaptable(
    tmp_path: Path,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    end = start + timedelta(minutes=1)
    full = build_verified_exact_state_batch(provider, start, end)
    assert len(full.rows) > 1
    cut = full.rows[0].utc_end
    left = full
    right = full

    stream = _stream(provider, engine_identity)
    assert stream.append(_source(left, start, cut, 0)) is None
    first_chunk = stream.append(_source(right, cut, end, 1))
    assert first_chunk is not None
    assert first_chunk.receipt.duplicate_boundary_event_count >= 1
    finalization = stream.finalize()
    chunks = (first_chunk.batch, finalization.final_chunk.batch)
    rows = tuple(row for chunk in chunks for row in chunk.rows)

    assert rows == full.rows
    events_at_cut = [
        event
        for row in rows
        for event in row.boundary_events
        if f'"at_utc":"{cut.isoformat()}"' in event
    ]
    assert events_at_cut
    assert len(events_at_cut) == len(set(events_at_cut))
    shard_set = assemble_verified_exact_shard_set(chunks)
    validate_verified_exact_shard_set(shard_set)
    assert tuple(shard_set.iter_rows()) == rows
    assert finalization.exact_state_universe_provenance.canonical_rows_sha256 == (
        canonical_rows_sha256(rows)
    )
    assert (
        finalization.aggregate_provenance.reconciliation_calculation_audit.outcome
        == "no_recomputation_required"
    )
    object.__setattr__(finalization, "_final_chunk", first_chunk)
    with pytest.raises(
        ExactStateReconciliationError,
        match="final chunk differs from aggregate output ordering",
    ):
        validate_reconciliation_stream_finalization(finalization)


def test_core_gap_or_overlap_fails_before_any_rows_are_emitted(
    tmp_path: Path,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    cut = start + timedelta(seconds=4)
    end = start + timedelta(seconds=8)
    left = build_verified_exact_state_batch(provider, start, cut + timedelta(seconds=2))
    right = build_verified_exact_state_batch(provider, cut - timedelta(seconds=2), end)
    stream = _stream(provider, engine_identity)
    assert stream.append(_source(left, start, cut, 0)) is None

    with pytest.raises(ExactStateReconciliationError, match="gap or overlap"):
        stream.append(_source(right, cut + timedelta(microseconds=1), end, 1))


def test_mixed_build_plan_sources_fail_before_reconciliation_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    cut = start + timedelta(seconds=4)
    end = start + timedelta(seconds=8)
    left = build_verified_exact_state_batch(provider, start, cut + timedelta(seconds=2))
    right = build_verified_exact_state_batch(provider, cut - timedelta(seconds=2), end)
    stream = _stream(provider, engine_identity)
    assert stream.append(_source(left, start, cut, 0, build_plan="plan-a")) is None

    def must_not_materialize(
        _provider: SwissEphemerisProvider,
        _source: OverlappingVerifiedExactStateBatch,
    ) -> tuple[CenturyStateRecord, ...]:
        raise AssertionError("mixed-plan source reached reconciliation work")

    monkeypatch.setattr(reconcile, "_materialize_core_rows", must_not_materialize)
    with pytest.raises(ExactStateReconciliationError, match="mix immutable build plans"):
        stream.append(_source(right, cut, end, 1, build_plan="plan-b"))


def test_plain_provenance_and_rows_cannot_mint_a_verified_reconciled_batch(
    tmp_path: Path,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    batch = build_verified_exact_state_batch(
        provider,
        start,
        start + timedelta(seconds=4),
    )

    with pytest.raises(ExactStateBatchError, match="factory capability"):
        chart_adapter._mint_reconciled_exact_state_batch(
            batch.rows,
            source_batch=batch,
            stable_interval_partition_sha256=_identity_hash("partition"),
            _reconciliation_factory_token=object(),
        )
    with pytest.raises(TypeError):
        chart_adapter._mint_reconciled_exact_state_batch(
            batch.rows,
            source_provenance=batch.provenance,
            stable_interval_partition_sha256=_identity_hash("partition"),
            _reconciliation_factory_token=object(),
        )
    with pytest.raises(
        ExactStateReconciliationError,
        match="must be minted from staged replay verification",
    ):
        OverlappingVerifiedExactStateBatch(
            batch=batch,
            core_start_utc=start,
            core_end_exclusive=start + timedelta(seconds=4),
            source_staged_receipt_sha256=_identity_hash("fabricated-receipt"),
            source_replay_verification_sha256=_identity_hash("fabricated-replay"),
            source_all_call_audit_sha256=_identity_hash("fabricated-audit"),
            source_build_plan_sha256=_identity_hash("fabricated-plan"),
            _factory_token=object(),
        )

    production_stream = ExactStateReconciliationStream(
        provider,
        engine_identity=engine_identity,
    )
    with pytest.raises(
        ExactStateReconciliationError,
        match="lacks staged replay-verification admission",
    ):
        production_stream.append(
            _source(batch, start, start + timedelta(seconds=4), 0)
        )


def test_overlap_state_disagreement_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    cut = start + timedelta(seconds=4)
    end = start + timedelta(seconds=8)
    left = build_verified_exact_state_batch(provider, start, cut + timedelta(seconds=2))
    right = build_verified_exact_state_batch(provider, cut - timedelta(seconds=2), end)
    stream = _stream(provider, engine_identity)
    assert stream.append(_source(left, start, cut, 0)) is None
    original = reconcile._source_identity_at
    calls = 0

    def disagree_on_second_source(rows: object, at_utc: datetime) -> str:
        nonlocal calls
        calls += 1
        assert isinstance(rows, tuple)
        observed = original(rows, at_utc)
        return observed if calls % 2 else _identity_hash("different-overlap-state")

    monkeypatch.setattr(reconcile, "_source_identity_at", disagree_on_second_source)
    with pytest.raises(ExactStateReconciliationError, match="overlap disagreement"):
        stream.append(_source(right, cut, end, 1))


def test_unexplained_identity_change_at_core_cut_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    end = start + timedelta(minutes=1)
    full = build_verified_exact_state_batch(provider, start, end)
    cut = full.rows[0].utc_end
    original = reconcile._reconcile_overlap

    def hide_exact_seam_event(
        left: OverlappingVerifiedExactStateBatch,
        right: OverlappingVerifiedExactStateBatch,
        seam: datetime,
        *,
        root_tolerance_seconds: float,
    ) -> reconcile._SeamEvidence:
        evidence = original(
            left,
            right,
            seam,
            root_tolerance_seconds=root_tolerance_seconds,
        )
        return reconcile._SeamEvidence(
            overlap_start_utc=evidence.overlap_start_utc,
            overlap_end_exclusive=evidence.overlap_end_exclusive,
            duplicate_boundary_event_count=evidence.duplicate_boundary_event_count,
            excluded_artificial_scan_endpoint_count=(
                evidence.excluded_artificial_scan_endpoint_count
            ),
            exact_event_at_core_cut=False,
        )

    monkeypatch.setattr(reconcile, "_reconcile_overlap", hide_exact_seam_event)
    stream = _stream(provider, engine_identity)
    assert stream.append(_source(full, start, cut, 0)) is None
    with pytest.raises(ExactStateReconciliationError, match="unexplained identity"):
        stream.append(_source(full, cut, end, 1))

    with provider.capture_calculation_audit() as capture:
        provider.position(CelestialBody.SUN, start)
    assert capture.snapshot().calculation_call_count == 1


def test_a_b_a_states_and_both_exact_events_survive_real_stream_state_machine(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    cut = start + timedelta(seconds=4)
    end = start + timedelta(seconds=8)
    left_batch = build_verified_exact_state_batch(
        provider, start, cut + timedelta(seconds=2)
    )
    right_batch = build_verified_exact_state_batch(
        provider, cut - timedelta(seconds=2), end
    )
    base = left_batch.rows[0]
    b_values = list(base.feature_values)
    b_values[0] = b_values[0].model_copy(update={"value": ["fixture-state-b"]})
    design_offset = base.representative_utc - base.design_timestamp

    def event(at_utc: datetime, before_gate: int, after_gate: int) -> str:
        return canonical_json_bytes(
            {
                "after": {"gate": after_gate, "line": 1},
                "at_utc": at_utc.isoformat(),
                "before": {"gate": before_gate, "line": 1},
                "body": "sun",
                "boundary_longitude": 0.0,
                "ephemeris_utc": at_utc.isoformat(),
                "resolution": "line",
                "root_tolerance_seconds": 0.01,
                "schema_version": "chart-boundary-event-v1",
                "side": "personality",
            }
        ).decode("utf-8")

    first_event_at = start + timedelta(seconds=2)
    second_event_at = start + timedelta(seconds=6)
    first_event = event(first_event_at, 1, 2)
    second_event = event(second_event_at, 2, 1)

    def fixture_row(
        label: str,
        row_start: datetime,
        row_end: datetime,
        *,
        state_b: bool,
        boundary_events: tuple[str, ...],
    ) -> CenturyStateRecord:
        representative = row_start + (row_end - row_start) / 2
        return base.model_copy(
            update={
                "state_id": f"FIXTURE-{label}",
                "utc_start": row_start,
                "utc_end": row_end,
                "duration_seconds": (row_end - row_start).total_seconds(),
                "representative_utc": representative,
                "design_timestamp": representative - design_offset,
                "boundary_events": boundary_events,
                "feature_values": tuple(b_values) if state_b else base.feature_values,
            }
        )

    a_left = fixture_row(
        "A-LEFT",
        start,
        first_event_at,
        state_b=False,
        boundary_events=(first_event,),
    )
    b_left = fixture_row(
        "B-LEFT",
        first_event_at,
        cut,
        state_b=True,
        boundary_events=(),
    )
    b_right = fixture_row(
        "B-RIGHT",
        cut,
        second_event_at,
        state_b=True,
        boundary_events=(second_event,),
    )
    a_right = fixture_row(
        "A-RIGHT",
        second_event_at,
        end,
        state_b=False,
        boundary_events=(),
    )
    def injected_core_rows(
        _provider: SwissEphemerisProvider,
        source: OverlappingVerifiedExactStateBatch,
    ) -> tuple[CenturyStateRecord, ...]:
        return (a_left, b_left) if source.core_start_utc == start else (b_right, a_right)

    def injected_overlap(
        _left: OverlappingVerifiedExactStateBatch,
        _right: OverlappingVerifiedExactStateBatch,
        seam: datetime,
        *,
        root_tolerance_seconds: float,
    ) -> reconcile._SeamEvidence:
        assert seam == cut
        assert root_tolerance_seconds == 0.01
        return reconcile._SeamEvidence(
            overlap_start_utc=cut - timedelta(seconds=2),
            overlap_end_exclusive=cut + timedelta(seconds=2),
            duplicate_boundary_event_count=0,
            excluded_artificial_scan_endpoint_count=2,
            exact_event_at_core_cut=False,
        )

    def injected_recompute(
        _provider: SwissEphemerisProvider,
        *,
        start_utc: datetime,
        end_utc: datetime,
        boundary_events: tuple[str, ...],
        expected_identity_sha256: str,
        source_provenance: ExactStateBatchProvenance,
    ) -> CenturyStateRecord:
        del source_provenance
        merged = fixture_row(
            "B-MERGED",
            start_utc,
            end_utc,
            state_b=True,
            boundary_events=boundary_events,
        )
        assert discrete_chart_identity_sha256(merged) == expected_identity_sha256
        return merged

    monkeypatch.setattr(reconcile, "_materialize_core_rows", injected_core_rows)
    monkeypatch.setattr(reconcile, "_reconcile_overlap", injected_overlap)
    monkeypatch.setattr(reconcile, "_recompute_interval", injected_recompute)

    stream = _stream(provider, engine_identity)
    assert stream.append(_source(left_batch, start, cut, 0)) is None
    first_chunk = stream.append(_source(right_batch, cut, end, 1))
    assert first_chunk is not None
    finalization = stream.finalize()
    rows = (*first_chunk.batch.rows, *finalization.final_chunk.batch.rows)
    identities = tuple(discrete_chart_identity_sha256(row) for row in rows)

    assert len(rows) == 3
    assert identities[0] == identities[2] != identities[1]
    assert all(row.duration_seconds > 0.0 for row in rows)
    assert first_event in rows[0].boundary_events
    assert second_event in rows[1].boundary_events
    assert (
        finalization.aggregate_provenance.reconciliation_calculation_audit.outcome
        == "no_recomputation_required"
    )


def test_context_abort_releases_provider_for_a_subsequent_audit(tmp_path: Path) -> None:
    provider, engine_identity = _provider(tmp_path)
    start = datetime(2000, 1, 1, 12, tzinfo=UTC)
    end = start + timedelta(seconds=4)
    batch = build_verified_exact_state_batch(provider, start, end)

    with pytest.raises(RuntimeError, match="abandon fixture"), _stream(
        provider, engine_identity
    ) as stream:
        assert stream.append(_source(batch, start, end, 0)) is None
        raise RuntimeError("abandon fixture")

    with provider.capture_calculation_audit() as capture:
        provider.position(CelestialBody.SUN, start)
    assert capture.snapshot().calculation_call_count == 1
