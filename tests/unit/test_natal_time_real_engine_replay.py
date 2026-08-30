from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from hdmatch.natal_time.replay import (
    ReplayContext,
    ReplayExpectation,
    ReplayValidationError,
    fake_receipt_executor,
    load_replay_context,
    run_replay,
)

PROJECT_ROOT = Path(__file__).parents[2]
TEST_COMMIT = "fixture-replay-test-commit"


def _verification(expectation: ReplayExpectation) -> dict[str, Any]:
    if expectation.status == "fail_closed":
        return {
            "status": "passed_expected_fail_closed",
            "enumeration_allowed": False,
            "failure_type": "ValueError",
        }
    return {
        "status": "passed_exact_event_key_agreement",
        "production_event_count": expectation.committed_interval_count - 1,
        "independent_event_count": expectation.committed_interval_count - 1,
        "independent_enumeration_sha256": "a" * 64,
    }


def _context() -> ReplayContext:
    return load_replay_context(PROJECT_ROOT, TEST_COMMIT)


def _mutate(path: Path, key: str, value: Any, *, rehash: bool = False) -> None:
    payload = json.loads(path.read_text())
    payload[key] = value
    if rehash:
        from hdmatch.util import sha256_json

        unhashed = deepcopy(payload)
        unhashed.pop("receipt_sha256")
        payload["receipt_sha256"] = sha256_json(unhashed)
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")


def test_replay_is_fixture_granular_resumable_and_fail_closed(tmp_path: Path) -> None:
    context = _context()
    complete = fake_receipt_executor(_verification)
    calls: list[str] = []

    def interrupted(
        replay_context: ReplayContext,
        expectations: tuple[ReplayExpectation, ...],
    ) -> Sequence[Mapping[str, Any]]:
        calls.append(expectations[0].source_fixture_name)
        if len(calls) == 2:
            raise RuntimeError("simulated interruption")
        return complete(replay_context, expectations)

    with pytest.raises(RuntimeError, match="simulated interruption"):
        run_replay(context, tmp_path, executor=interrupted)
    receipts_dir = tmp_path / "receipts"
    assert len(tuple(receipts_dir.glob("*.json"))) == 2

    resumed_calls: list[str] = []

    def resumed(
        replay_context: ReplayContext,
        expectations: tuple[ReplayExpectation, ...],
    ) -> Sequence[Mapping[str, Any]]:
        resumed_calls.append(expectations[0].source_fixture_name)
        return complete(replay_context, expectations)

    index = run_replay(context, tmp_path, executor=resumed)
    assert "ordinary_and_multiple_dates" not in resumed_calls
    assert index["successful_civil_day_count"] == 8
    assert index["fail_closed_civil_day_count"] == 1
    assert index["receipt_count"] == 9
    skipped = json.loads(
        (receipts_dir / "skipped-civil-date-2011-12-30.json").read_text()
    )
    assert skipped["status"] == "fail_closed"
    assert skipped["independent_verification"]["enumeration_allowed"] is False
    assert run_replay(context, tmp_path, aggregate_only=True) == index


@pytest.mark.parametrize(
    ("key", "value", "rehash", "message"),
    [
        ("receipt_sha256", "0" * 64, False, "self-hash"),
        ("repository_commit", "stale-head", True, "repository_commit"),
        ("engine_identity_packet_sha256", "0" * 64, True, "engine_identity"),
        ("result_sha256", "0" * 64, True, "result_sha256"),
    ],
)
def test_aggregate_fails_tampered_stale_wrong_engine_and_mismatch(
    tmp_path: Path,
    key: str,
    value: str,
    rehash: bool,
    message: str,
) -> None:
    context = _context()
    run_replay(context, tmp_path, executor=fake_receipt_executor(_verification))
    target = tmp_path / "receipts" / "leap-day-2024-02-29.json"
    _mutate(target, key, value, rehash=rehash)
    with pytest.raises(ReplayValidationError, match=message):
        run_replay(context, tmp_path, aggregate_only=True)


def test_aggregate_fails_missing_and_duplicate_receipts(tmp_path: Path) -> None:
    context = _context()
    run_replay(context, tmp_path, executor=fake_receipt_executor(_verification))
    receipts = tmp_path / "receipts"
    missing = receipts / "leap-day-2024-02-29.json"
    missing.unlink()
    with pytest.raises(ReplayValidationError, match="missing replay receipt"):
        run_replay(context, tmp_path, aggregate_only=True)

    duplicate = receipts / "unexpected-copy.json"
    duplicate.write_bytes((receipts / "dst-gap-2024-03-10.json").read_bytes())
    with pytest.raises(ReplayValidationError, match="duplicate or unexpected"):
        run_replay(context, tmp_path, aggregate_only=True)
