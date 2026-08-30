from __future__ import annotations

import json
import shutil
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from hdmatch.natal_time.replay import (
    PRODUCTION_INDEX_SCHEMA,
    PRODUCTION_RECEIPT_SCHEMA,
    FixtureExecutor,
    ReplayContext,
    ReplayExpectation,
    ReplayValidationError,
    _run_replay,
    load_synthetic_test_context,
)
from hdmatch.util import canonical_json_bytes, sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
COMMITTED_REPLAY_ROOT = PROJECT_ROOT / "state" / "NATAL-TIME-REAL-ENGINE-REPLAY-V1"
APIA_RECEIPT_ID = "skipped-civil-date-2011-12-30"


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def _context_for_committed_receipts() -> ReplayContext:
    """Reconstruct the exact binding context of the immutable replay receipts."""

    index = _load_json(COMMITTED_REPLAY_ROOT / "index.json")
    expectation_context = load_synthetic_test_context(PROJECT_ROOT)
    return replace(
        expectation_context,
        execution_mode="real_engine_production",
        repository_commit=index["repository_commit"],
        commit_tree_oid=index["commit_tree_oid"],
        source_verification=index["source_verification"],
        source_verification_sha256=index["source_verification_sha256"],
    )


def _committed_receipt_executor(
    context: ReplayContext,
    expectations: tuple[ReplayExpectation, ...],
) -> Sequence[Mapping[str, Any]]:
    """Return prior immutable real-engine receipts without running astronomy.

    These are the exact committed outputs of the earlier real-engine replay,
    not synthetic calculations presented as real-engine results.  This test
    executor exercises only receipt validation and replay orchestration.
    """

    assert context.execution_mode == "real_engine_production"
    return tuple(
        _load_json(COMMITTED_REPLAY_ROOT / "receipts" / f"{item.receipt_id}.json")
        for item in expectations
    )


@pytest.fixture
def committed_context(monkeypatch: pytest.MonkeyPatch) -> ReplayContext:
    context = _context_for_committed_receipts()

    def assert_historical_binding(
        received_context: ReplayContext, _output_root: Path
    ) -> None:
        # The production source gate is separately tested and cannot succeed at
        # today's HEAD for a historical replay commit.  Keep this integration
        # test bound to that exact immutable historical context instead.
        assert received_context == context

    monkeypatch.setattr(
        "hdmatch.natal_time.replay._validate_production_context",
        assert_historical_binding,
    )
    return context


def _run(
    context: ReplayContext,
    output_root: Path,
    executor: FixtureExecutor,
    *,
    aggregate_only: bool = False,
) -> dict[str, Any]:
    return _run_replay(
        context,
        output_root,
        executor=executor,
        aggregate_only=aggregate_only,
        progress=None,
    )


def test_interruption_resume_preserves_receipts_and_matches_clean_run(
    tmp_path: Path, committed_context: ReplayContext
) -> None:
    resumed_root = tmp_path / "resumed"
    assert not resumed_root.exists()
    interrupted_calls: list[str] = []

    def interrupt_after_first_fixture(
        context: ReplayContext,
        expectations: tuple[ReplayExpectation, ...],
    ) -> Sequence[Mapping[str, Any]]:
        interrupted_calls.append(expectations[0].source_fixture_name)
        if len(interrupted_calls) == 2:
            raise RuntimeError("deliberate interruption before aggregate index")
        return _committed_receipt_executor(context, expectations)

    with pytest.raises(RuntimeError, match="deliberate interruption"):
        _run(committed_context, resumed_root, interrupt_after_first_fixture)

    receipts_dir = resumed_root / "receipts"
    partial_receipts = tuple(sorted(receipts_dir.glob("*.json")))
    assert interrupted_calls == ["ordinary_and_multiple_dates", "leap_day"]
    assert len(partial_receipts) == 2 < len(committed_context.expectations)
    assert not (resumed_root / "index.json").exists()

    with pytest.raises(ReplayValidationError, match="missing replay receipt: leap-day"):
        _run(
            committed_context,
            resumed_root,
            _committed_receipt_executor,
            aggregate_only=True,
        )

    preserved = {
        path.name: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in partial_receipts
    }
    resumed_calls: list[str] = []

    def record_resumed_fixture(
        context: ReplayContext,
        expectations: tuple[ReplayExpectation, ...],
    ) -> Sequence[Mapping[str, Any]]:
        resumed_calls.append(expectations[0].source_fixture_name)
        return _committed_receipt_executor(context, expectations)

    resumed_index = _run(committed_context, resumed_root, record_resumed_fixture)

    assert "ordinary_and_multiple_dates" not in resumed_calls
    assert len(tuple(receipts_dir.glob("*.json"))) == 9
    for name, (expected_bytes, expected_mtime_ns) in preserved.items():
        path = receipts_dir / name
        assert path.read_bytes() == expected_bytes
        assert path.stat().st_mtime_ns == expected_mtime_ns

    for expectation in committed_context.expectations:
        payload = _load_json(receipts_dir / f"{expectation.receipt_id}.json")
        assert payload["schema_version"] == PRODUCTION_RECEIPT_SCHEMA
        assert payload["execution_mode"] == "real_engine_production"
        assert payload["synthetic_orchestration_test_only"] is False
        assert payload == _load_json(
            COMMITTED_REPLAY_ROOT / "receipts" / f"{expectation.receipt_id}.json"
        )

    apia = _load_json(receipts_dir / f"{APIA_RECEIPT_ID}.json")
    assert apia["status"] == "fail_closed"
    assert apia["independent_verification"]["status"] == "passed_expected_fail_closed"

    clean_root = tmp_path / "clean"
    assert not clean_root.exists()
    clean_index = _run(committed_context, clean_root, _committed_receipt_executor)

    assert resumed_index == clean_index
    assert resumed_index["schema_version"] == PRODUCTION_INDEX_SCHEMA
    assert (resumed_root / "index.json").read_bytes() == (
        clean_root / "index.json"
    ).read_bytes()
    assert (resumed_root / "index.json").read_bytes() == (
        COMMITTED_REPLAY_ROOT / "index.json"
    ).read_bytes()


def _rewrite_receipt(
    path: Path, key: str, value: Any, *, repair_self_hash: bool
) -> None:
    payload = _load_json(path)
    payload[key] = value
    if repair_self_hash:
        unhashed = deepcopy(payload)
        unhashed.pop("receipt_sha256")
        payload["receipt_sha256"] = sha256_json(unhashed)
    path.write_bytes(canonical_json_bytes(payload) + b"\n")


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("missing", "missing replay receipt: leap-day-2024-02-29"),
        ("duplicated", "duplicate or unexpected replay receipts"),
        ("corrupted", "replay receipt self-hash mismatch"),
        ("wrong_head", "stale or mismatched binding: repository_commit"),
        ("wrong_engine", "stale or mismatched binding: engine_identity_packet_sha256"),
        ("stale", "stale or mismatched binding: source_verification_sha256"),
        ("partially_written", "invalid JSON artifact"),
        ("apia_omitted", f"missing replay receipt: {APIA_RECEIPT_ID}"),
    ],
)
def test_aggregate_rejects_invalid_or_incomplete_receipt_sets(
    tmp_path: Path,
    committed_context: ReplayContext,
    case: str,
    message: str,
) -> None:
    baseline = tmp_path / "baseline"
    _run(committed_context, baseline, _committed_receipt_executor)
    case_root = tmp_path / case
    shutil.copytree(baseline, case_root)
    receipts = case_root / "receipts"
    target = receipts / "leap-day-2024-02-29.json"

    if case == "missing":
        target.unlink()
    elif case == "duplicated":
        shutil.copyfile(target, receipts / "unexpected-copy.json")
    elif case == "corrupted":
        _rewrite_receipt(target, "receipt_sha256", "0" * 64, repair_self_hash=False)
    elif case == "wrong_head":
        _rewrite_receipt(target, "repository_commit", "0" * 40, repair_self_hash=True)
    elif case == "wrong_engine":
        _rewrite_receipt(
            target,
            "engine_identity_packet_sha256",
            "0" * 64,
            repair_self_hash=True,
        )
    elif case == "stale":
        _rewrite_receipt(
            target,
            "source_verification_sha256",
            "0" * 64,
            repair_self_hash=True,
        )
    elif case == "partially_written":
        target.write_bytes(target.read_bytes()[:37])
    elif case == "apia_omitted":
        (receipts / f"{APIA_RECEIPT_ID}.json").unlink()
    else:  # pragma: no cover - parametrization is intentionally exhaustive
        raise AssertionError(f"unknown receipt mutation: {case}")

    with pytest.raises(ReplayValidationError, match=message):
        _run(
            committed_context,
            case_root,
            _committed_receipt_executor,
            aggregate_only=True,
        )
