from __future__ import annotations

import json
import subprocess
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from hdmatch.natal_time.replay import (
    ReplayContext,
    ReplayExpectation,
    ReplayValidationError,
    _event_key,
    _execute_fail_closed,
    _run_replay,
    _validate_receipt,
    build_aggregate_index,
    current_repository_commit,
    fake_receipt_executor,
    load_replay_context,
    load_synthetic_test_context,
    make_receipt,
    run_replay,
    run_synthetic_test_replay,
    verify_production_source,
)
from hdmatch.util import sha256_json

PROJECT_ROOT = Path(__file__).parents[2]
COMMITTED_REPLAY_ROOT = PROJECT_ROOT / "state" / "NATAL-TIME-REAL-ENGINE-REPLAY-V1"


def _context() -> ReplayContext:
    return load_synthetic_test_context(PROJECT_ROOT)


def _production_contract_stub(
    context: ReplayContext,
    expectations: tuple[ReplayExpectation, ...],
) -> Sequence[Mapping[str, Any]]:
    """Build contract-valid test receipts without executing astronomy."""

    receipts: list[dict[str, Any]] = []
    for item in expectations:
        if item.status == "success":
            verification = {
                "status": "passed_exact_event_key_agreement",
                "production_event_count": 0,
                "independent_event_count": 0,
                "independent_enumeration_sha256": "a" * 64,
                "independent_series_certificate_sha256": "b" * 64,
            }
        else:
            verification = {
                "status": "passed_expected_fail_closed",
                "enumeration_allowed": False,
                "failure_type": item.fixture_input["failure_type"],
                "failure_message": item.fixture_input["failure_message"],
            }
        receipts.append(
            make_receipt(
                context,
                item,
                interval_count=item.committed_interval_count,
                ordered_interval_list_sha256="c" * 64,
                ordered_full_state_vector_sha256=(item.committed_ordered_full_state_vector_sha256),
                coverage_receipt_sha256=item.committed_coverage_receipt_sha256,
                result_sha256=item.committed_result_sha256,
                independent_verification=verification,
            )
        )
    return tuple(receipts)


def test_production_event_key_is_the_expected_seven_tuple() -> None:
    encoded = "2024-01-15T01:09:29.742682+00:00|design|moon|6.3->6.4"
    parsed = _event_key(encoded)

    assert parsed == (
        datetime(2024, 1, 15, 1, 9, 29, 742682, tzinfo=UTC),
        "design",
        "moon",
        6,
        3,
        6,
        4,
    )
    assert len(parsed) == 7


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
    complete = fake_receipt_executor()
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
        run_synthetic_test_replay(context, tmp_path, executor=interrupted)
    receipts_dir = tmp_path / "receipts"
    assert len(tuple(receipts_dir.glob("*.json"))) == 2

    resumed_calls: list[str] = []

    def resumed(
        replay_context: ReplayContext,
        expectations: tuple[ReplayExpectation, ...],
    ) -> Sequence[Mapping[str, Any]]:
        resumed_calls.append(expectations[0].source_fixture_name)
        return complete(replay_context, expectations)

    index = run_synthetic_test_replay(context, tmp_path, executor=resumed)
    assert "ordinary_and_multiple_dates" not in resumed_calls
    assert index["successful_civil_day_count"] == 8
    assert index["fail_closed_civil_day_count"] == 1
    assert index["receipt_count"] == 9
    assert index["schema_version"].endswith("synthetic-orchestration-index-v1")
    assert index["real_engine_executed"] is False
    assert index["all_independent_verifications_passed"] is False
    skipped = json.loads((receipts_dir / "skipped-civil-date-2011-12-30.json").read_text())
    assert skipped["status"] == "fail_closed"
    assert skipped["schema_version"].endswith("synthetic-orchestration-receipt-v1")
    assert skipped["independent_verification"] == {
        "status": "synthetic_not_executed",
        "real_engine_executed": False,
        "independent_verification_executed": False,
    }
    ordinary = json.loads(
        (receipts_dir / "ordinary-and-multiple-dates-2024-01-15.json").read_text()
    )
    assert ordinary["ordered_interval_list_scope"].startswith("canonical-model-dumps")
    assert ordinary["ordered_interval_list_sha256"] != ordinary["ordered_full_state_vector_sha256"]
    assert (
        run_synthetic_test_replay(
            context,
            tmp_path,
            executor=complete,
            aggregate_only=True,
        )
        == index
    )


@pytest.mark.parametrize(
    ("key", "value", "rehash", "message"),
    [
        ("receipt_sha256", "0" * 64, False, "self-hash"),
        ("repository_commit", "stale-head", True, "repository_commit"),
        ("engine_identity_packet_sha256", "0" * 64, True, "engine_identity"),
        ("result_sha256", "0" * 64, True, "result_sha256"),
        ("ordered_interval_list_sha256", "0" * 64, True, "existing replay index"),
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
    executor = fake_receipt_executor()
    run_synthetic_test_replay(context, tmp_path, executor=executor)
    target = tmp_path / "receipts" / "leap-day-2024-02-29.json"
    _mutate(target, key, value, rehash=rehash)
    with pytest.raises(ReplayValidationError, match=message):
        run_synthetic_test_replay(context, tmp_path, executor=executor, aggregate_only=True)


def test_aggregate_fails_missing_and_duplicate_receipts(tmp_path: Path) -> None:
    context = _context()
    executor = fake_receipt_executor()
    run_synthetic_test_replay(context, tmp_path, executor=executor)
    receipts = tmp_path / "receipts"
    missing = receipts / "leap-day-2024-02-29.json"
    missing.unlink()
    with pytest.raises(ReplayValidationError, match="missing replay receipt"):
        run_synthetic_test_replay(context, tmp_path, executor=executor, aggregate_only=True)

    duplicate = receipts / "unexpected-copy.json"
    duplicate.write_bytes((receipts / "dst-gap-2024-03-10.json").read_bytes())
    with pytest.raises(ReplayValidationError, match="duplicate or unexpected"):
        run_synthetic_test_replay(context, tmp_path, executor=executor, aggregate_only=True)


def test_load_context_rejects_non_sha_and_mismatched_head() -> None:
    with pytest.raises(ReplayValidationError, match="40-hex"):
        load_replay_context(PROJECT_ROOT, "not-a-commit")
    with pytest.raises(ReplayValidationError, match="does not match current HEAD"):
        load_replay_context(PROJECT_ROOT, "0" * 40)


def test_source_verification_excludes_only_declared_output_root(tmp_path: Path) -> None:
    repository = tmp_path / "repo"
    repository.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(["git", "config", "user.name", "Replay Test"], cwd=repository, check=True)
    subprocess.run(
        ["git", "config", "user.email", "replay@example.invalid"],
        cwd=repository,
        check=True,
    )
    (repository / "source.txt").write_text("source\n")
    subprocess.run(["git", "add", "source.txt"], cwd=repository, check=True)
    subprocess.run(["git", "commit", "-qm", "source"], cwd=repository, check=True)
    commit = current_repository_commit(repository)
    output = repository / "state" / "NATAL-TIME-REAL-ENGINE-REPLAY-V1"
    output.mkdir(parents=True)
    (output / "partial.json").write_text("{}\n")

    receipt = verify_production_source(repository, commit, output)
    assert receipt["head_matches_declared_commit"] is True
    assert receipt["clean_worktree_excluding_output_root"] is True
    assert receipt["output_root_repo_relative"] == ("state/NATAL-TIME-REAL-ENGINE-REPLAY-V1")

    (repository / "source.txt").write_text("dirty\n")
    with pytest.raises(ReplayValidationError, match="dirty outside output root"):
        verify_production_source(repository, commit, output)


def test_actual_apia_execution_fails_closed_with_production_receipt() -> None:
    head = current_repository_commit(PROJECT_ROOT)
    context = load_replay_context(PROJECT_ROOT, head)
    expectation = next(item for item in context.expectations if item.status == "fail_closed")

    receipt = _execute_fail_closed(context, expectation)
    _validate_receipt(context, expectation, receipt)

    assert receipt["execution_mode"] == "real_engine_production"
    assert receipt["real_engine_executor"] is True
    assert receipt["status"] == "fail_closed"
    assert receipt["interval_count"] == 0
    assert receipt["independent_verification"]["status"] == ("passed_expected_fail_closed")


def test_production_rejects_synthetic_context_and_mismatched_independent_counts(
    tmp_path: Path,
) -> None:
    with pytest.raises(ReplayValidationError, match="rejects synthetic"):
        run_replay(_context(), tmp_path)

    from hdmatch.util import sha256_json

    head = current_repository_commit(PROJECT_ROOT)
    context = load_replay_context(PROJECT_ROOT, head)
    expectation = next(item for item in context.expectations if item.status == "success")
    verification = {
        "status": "passed_exact_event_key_agreement",
        "production_event_count": 3,
        "independent_event_count": 3,
        "independent_enumeration_sha256": "a" * 64,
        "independent_series_certificate_sha256": "b" * 64,
    }
    receipt = make_receipt(
        context,
        expectation,
        interval_count=expectation.committed_interval_count,
        ordered_interval_list_sha256="c" * 64,
        ordered_full_state_vector_sha256=(expectation.committed_ordered_full_state_vector_sha256),
        coverage_receipt_sha256=expectation.committed_coverage_receipt_sha256,
        result_sha256=expectation.committed_result_sha256,
        independent_verification=verification,
    )
    _validate_receipt(context, expectation, receipt)

    receipt["independent_verification"]["independent_event_count"] = 2
    receipt["independent_verification_sha256"] = sha256_json(receipt["independent_verification"])
    unhashed = deepcopy(receipt)
    unhashed.pop("receipt_sha256")
    receipt["receipt_sha256"] = sha256_json(unhashed)
    with pytest.raises(ReplayValidationError, match="event counts differ"):
        _validate_receipt(context, expectation, receipt)


def test_source_change_after_executor_writes_no_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    context = replace(_context(), execution_mode="real_engine_production")
    checks = 0

    def source_check(_context: ReplayContext, _output_root: Path) -> None:
        nonlocal checks
        checks += 1
        if checks == 2:
            raise ReplayValidationError("simulated source change after executor")

    monkeypatch.setattr("hdmatch.natal_time.replay._validate_production_context", source_check)
    with pytest.raises(ReplayValidationError, match="after executor"):
        _run_replay(
            context,
            tmp_path,
            executor=_production_contract_stub,
            aggregate_only=False,
            progress=None,
        )
    assert checks == 2
    assert not tuple((tmp_path / "receipts").glob("*.json"))
    assert not (tmp_path / "index.json").exists()


def test_source_change_before_aggregate_writes_no_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    context = replace(_context(), execution_mode="real_engine_production")
    checks = 0

    def source_check(_context: ReplayContext, _output_root: Path) -> None:
        nonlocal checks
        checks += 1
        if checks == 17:
            raise ReplayValidationError("simulated source change before aggregate")

    monkeypatch.setattr("hdmatch.natal_time.replay._validate_production_context", source_check)
    with pytest.raises(ReplayValidationError, match="before aggregate"):
        _run_replay(
            context,
            tmp_path,
            executor=_production_contract_stub,
            aggregate_only=False,
            progress=None,
        )
    assert checks == 17
    assert len(tuple((tmp_path / "receipts").glob("*.json"))) == 9
    assert not (tmp_path / "index.json").exists()


def test_committed_production_replay_index_and_receipts_are_self_consistent() -> None:
    index = json.loads((COMMITTED_REPLAY_ROOT / "index.json").read_text())
    index_unhashed = deepcopy(index)
    embedded_index_sha = index_unhashed.pop("index_sha256")
    assert embedded_index_sha == sha256_json(index_unhashed)

    source = index["source_verification"]
    source_unhashed = deepcopy(source)
    embedded_source_sha = source_unhashed.pop("source_verification_sha256")
    assert embedded_source_sha == sha256_json(source_unhashed)
    assert embedded_source_sha == index["source_verification_sha256"]
    source_tree = subprocess.run(
        ["git", "rev-parse", f"{index['repository_commit']}^{{tree}}"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert source_tree == index["commit_tree_oid"] == source["commit_tree_oid"]

    synthetic_context = load_synthetic_test_context(PROJECT_ROOT)
    context = replace(
        synthetic_context,
        execution_mode="real_engine_production",
        repository_commit=index["repository_commit"],
        commit_tree_oid=index["commit_tree_oid"],
        source_verification=source,
        source_verification_sha256=index["source_verification_sha256"],
    )
    receipt_refs = index["receipt_hashes"]
    assert len(receipt_refs) == len(context.expectations) == 9
    receipts: dict[str, dict[str, Any]] = {}
    for expectation, receipt_ref in zip(context.expectations, receipt_refs, strict=True):
        assert receipt_ref["receipt_id"] == expectation.receipt_id
        receipt_path = COMMITTED_REPLAY_ROOT / "receipts" / f"{expectation.receipt_id}.json"
        receipt = json.loads(receipt_path.read_text())
        _validate_receipt(context, expectation, receipt)
        assert receipt["receipt_sha256"] == receipt_ref["receipt_sha256"]
        receipts[expectation.receipt_id] = receipt

    assert build_aggregate_index(context, receipts) == index
